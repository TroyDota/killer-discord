import discord
from discord.ext import commands
import logging
import asyncio
import random

from killer.cogs import init_cogs

log = logging.getLogger("killer")


class DiscordManager:
    def __init__(self, bot, private_loop, command_prefix):
        self.bot = bot
        self.private_loop = private_loop
        self.client = commands.Bot(
            command_prefix=command_prefix, loop=self.private_loop
        )
        init_cogs(self.client)

        @self.client.event
        async def on_ready():
            log.info("Ready!")

    async def start(self, token):
        try:
            await self.client.login(token)
        except discord.LoginFailure:
            log.exception("Invalid discord client credentials")
            return
        except discord.HTTPException:
            log.error("Failed to connect, issued a restart...")
            asyncio.sleep(random.randint(1000, 5000) / 1000)
            self.private_loop.create_task(self.start(token))
            return
        try:
            await self.client.connect()
        except discord.GatewayNotFound:
            await self.client.close()
            log.error("Discord is currently down... Issued a reconenct")
            asyncio.sleep(random.randint(1000, 5000) / 1000)
            self.private_loop.create_task(self.start(token))
            return
        except discord.ConnectionClosed:
            log.error("Discord Connection Closed...")
