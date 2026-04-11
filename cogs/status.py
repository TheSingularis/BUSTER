import json
import asyncio

from discord.ext import commands, tasks
import discord
import config

class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel = None
        self.status_message_id = None
        self.message = None

    async def cog_load(self):
        # Try to load state.json and fetch the existing message id
        try:
            with open("state.json", "r") as f:
                state = json.load(f)
            self.status_message_id = state.get("status_message_id")
        except FileNotFoundError:
            self.status_message_id = None

    # Wait for the bot to start up before pinging channels
    @commands.Cog.listener()
    async def on_ready(self):
        # Grab the status channel
        channel = self.bot.get_channel(config.STATUS_CHANNEL_ID)
        self.channel = channel
        assert isinstance(channel, discord.TextChannel)

        results = await asyncio.gather(*[service.check() for service in config.SERVICES])
        embed = self.build_embed(list(zip(config.SERVICES, results)))

        # If no message id saved
        if self.status_message_id is None:
            self.message = await self.create_status_message(embed)
        else:
            try:
                self.message = await self.channel.fetch_message(self.status_message_id)
                await self.message.edit(embed=embed)
            except discord.NotFound:
                self.message = await self.create_status_message(embed)

        # Start the polling loop
        self.poll.start()

    # Handle the polling loop
    @tasks.loop(seconds=config.POLL_INTERVAL_SECONDS)
    async def poll(self):
        if self.message is None:
            return
        results = await asyncio.gather(*[service.check() for service in config.SERVICES])
        embed = self.build_embed(list(zip(config.SERVICES, results)))
        await self.message.edit(embed=embed)

    # But dont start the loop until its ready
    @poll.before_loop
    async def before_poll(self):
        await self.bot.wait_until_ready()

    async def create_status_message(self, embed: discord.Embed) -> discord.Message:
        message = await self.channel.send(embed=embed)
        await message.pin()
        with open("state.json", "w") as f:
            json.dump({"status_message_id": message.id}, f)
        return message

    def build_embed(self, pairs) -> discord.Embed:
        all_up = all(status.up for _, status in pairs)
        color = discord.Color.green() if all_up else discord.Color.red()
        embed = discord.Embed(
            title="BUSTER - Service Status",
            color=color,
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(text="Last updated")
        for service, status in pairs:
            indicator = "✅" if status.up else "❌"
            ms = f"{status.response_ms}ms" if status.response_ms is not None else "unreachable"
            embed.add_field(name="\u200b", value=f"{indicator} \u200b [{service.name}]({service.url})", inline=True)
            embed.add_field(name="\u200b", value="->", inline=True)
            embed.add_field(name="\u200b", value=f"{ms}", inline=True)
        return embed

async def setup(bot: commands.Bot):
    await bot.add_cog(StatusCog(bot))
