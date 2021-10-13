import discord
from discord.ext import commands

from utils.constants import *
from utils.logging import log


class Anilist(commands.Cog, name="Anilist", description="XXX"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )


def setup(bot):
    bot.add_cog(Anilist(bot))
