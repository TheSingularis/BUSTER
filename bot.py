import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Buster(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.status")

bot = Buster(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"BUSTER is online as {bot.user} (ID: {bot.user.id})") # type: ignore
    print(f"Connected to {len(bot.guilds)} guild(s)")

if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
