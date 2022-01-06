"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import discord

from anilist.async_client import Client

from typing import Optional
from discord.ext import commands

from helpers.constants import *
from helpers.logging import log


class Anilist(
    commands.Cog,
    name="Anilist",
    description="Get Info About Your Favorite Anime, Characters And Other Stuff!",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Client()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.group(
        invoke_without_command=True,
        name="anilist",
        description="Anilist Commands",
    )
    @commands.guild_only()
    async def anilist(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @anilist.command(
        name="user",
        description="Get Information About A User",
        brief="anilist user xGhoul",
    )
    async def anilist_user(
        self, ctx: commands.Context, username: Optional[str]
    ) -> None:
        user = await self.client.get_user(username)
        return

    @anilist.command(
        name="anime",
        description="Get Information About An Anime",
        brief="anilist anime One Piece",
    )
    async def anilist_anime(
        self, ctx: commands.Context, *, anime: Optional[str]
    ) -> None:
        anime = await self.client.get_anime(anime)
        return

    @anilist.command(
        name="manga",
        description="Get Information About An Manga",
        brief="anilist manga Sun Ken Rock",
    )
    async def anilist_manga(
        self, ctx: commands.Context, *, manga: Optional[str]
    ) -> None:
        manga = await self.client.get_manga(manga)
        return

    @anilist.command(
        name="character",
        description="Get Information About An Character",
        brief="anilist character Ken Kaneki",
    )
    async def anilist_character(
        self, ctx: commands.Context, *, character: Optional[str]
    ) -> None:
        character = await self.client.get_character(character)
        return


def setup(bot):
    bot.add_cog(Anilist(bot))
