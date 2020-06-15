import discord
import asyncio
import logging

from killer.managers.discord_manager import DiscordManager

log = logging.getLogger("killer")


class Bot:
    def __init__(self, config):
        self.config = config
        self.private_loop = asyncio.get_event_loop()
        self.discord_bot = DiscordManager(self, self.private_loop, self.command_prefix)
        self.running = False

    @property
    def token(self):
        return self.config["main"]["token"]

    @property
    def command_prefix(self):
        return self.config["main"]["prefix"]

    def run(self):
        self.private_loop.set_exception_handler(self._exception_handler)
        try:
            self.running = True
            self.private_loop.run_forever()
        except KeyboardInterrupt:
            log.debug("Shutting down.")
        finally:
            self.running = False
            self.private_loop.run_until_complete(self.private_loop.shutdown_asyncgens())
            self.private_loop.close()

    def start(self):
        self.private_loop.create_task(self.discord_bot.start(self.token))

    def _exception_handler(self, loop, context):
        if self.running:
            log.error(context["message"])
            raise context.get("exception", Exception(context["message"]))
