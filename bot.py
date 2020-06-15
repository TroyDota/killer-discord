import discord
from discord.ext import commands

from cogs import init_cogs

if __name__ == "__main__":
    bot = commands.Bot(command_prefix="$")
    init_cogs(bot)

    @bot.event
    async def on_ready():
        print("Ready")
        await bot.change_presence(activity=discord.Streaming(name="HI", url="https://twitch.tv/yikes"))

    bot.run("xyz")
