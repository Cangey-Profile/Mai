"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import humanize
import datetime

from typing import List, Mapping, Optional

from discord import Embed
from discord.ext import commands

from helpers.constants import *

from config.ext.parser import config


class MaiHelpCommand(commands.HelpCommand):
    def command_not_found(self, string: str) -> str:
        return f"{Emoji.ERROR} The command `{self.context.clean_prefix}{string}` was not found!, If you would like this command to be added suggest it in our [support server]({Links.SUPPORT_SERVER_INVITE})"

    def subcommand_not_found(
        self, command: commands.Command, string: str
    ) -> str:
        return f"{Emoji.ERROR} I don't have the command `{command.qualified_name} {string}`, If you would like this command to be added suggest it in our [support server]({Links.SUPPORT_SERVER_INVITE})"

    async def dispatch_help(self, help_embed: Embed) -> None:
        dest = self.get_destination()
        await dest.send(embed=help_embed)

    async def send_error_message(self, error: str) -> None:
        embed = Embed(
            title="Error :\\", description=f"{error}", color=Colors.ERROR_COLOR
        )
        await self.dispatch_help(embed)

    async def send_bot_help(
        self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]
    ) -> None:
        bot = self.context.bot
        latest_news = f"`•` Dashboard Coming Soon\n`•` [Nerd](https://github.com/FrostByte266) Is Now A Core Developer\n`•` Updates Are Going To Be Slower Because Of School"
        embed = Embed(
            title=f"{bot.user.name} Help",
            description=f"__**{Emoji.NOTIFICATION} {bot.user.name} News**__\n{latest_news}\n\n**{Emoji.CHECKMARK} Here are all my modules!**",
            color=Colors.EMBED_COLOR,
        )
        embed.set_author(
            name=bot.user.name,
            icon_url=Links.BOT_AVATAR_URL,
            url=Links.BOT_DOCUMENTATION_URL,
        )
        embed.set_thumbnail(url=Links.BOT_AVATAR_URL)
        embed.set_footer(
            text=f"Requested By {self.context.author.name}",
            icon_url=self.context.author.avatar.url,
        )
        for cog in self.context.bot.cogs.values():
            # TODO: SEPERATE INTO CATEGORIES INSTEAD OF ALL COGS
            embed.add_field(
                name=cog.qualified_name,
                value=f"`{self.context.clean_prefix}help {cog.qualified_name}`",
            )
        await self.dispatch_help(embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed = Embed(
            title=f"Help For: `{command.name}`", color=Colors.EMBED_COLOR
        )
        embed.add_field(
            name=f"{Emoji.QUESTION} What does this command do?",
            value=command.description
            if command.description is not None
            else "No Description",
            inline=False,
        )
        embed.add_field(
            name="Usage",
            value=f"`{self.get_command_signature(command)}`",
            inline=False,
        )

        examples = (
            f"{command.brief}" if command.brief is not None else "No Examples."
        )

        embed.add_field(name="Examples", value=examples, inline=False)

        if command._buckets._cooldown is None:
            embed.add_field(name="Cooldown", value=f"`0`", inline=False)
        else:
            delta = datetime.timedelta(seconds=command._buckets._cooldown.per)
            cooldown = humanize.precisedelta(delta, format="%0.0f")
            embed.add_field(
                name="Cooldown", value=f"`{cooldown}`", inline=False
            )

        await self.dispatch_help(embed)

    async def send_group_help(self, group: commands.Group) -> None:
        embed = Embed(
            title=f"Help For Command: `{group.name}`", color=Colors.EMBED_COLOR
        )
        embed.add_field(
            name=f"{Emoji.QUESTION} What does this command do?",
            value=group.description
            if group.description is not None
            else "No Description",
            inline=False,
        )
        embed.add_field(
            name="Usage",
            value=f"`{self.get_command_signature(group)}`",
            inline=False,
        )

        subcommand_help = [
            f"**`{self.get_command_signature(command)}`**\n{command.description}"
            for command in group.commands
        ]
        newline = "\n"
        embed.add_field(
            name="Related commands",
            value=f"\n{newline.join(subcommand_help)}",
            inline=False,
        )
        await self.dispatch_help(embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        embed = Embed(
            title=f"Help For Module: `{cog.qualified_name}`",
            color=Colors.EMBED_COLOR,
        )
        embed.add_field(
            name=f"{Emoji.QUESTION} What does this category do?",
            value=cog.description
            if cog.description is not None
            else "No Description",
            inline=False,
        )
        for command in cog.walk_commands():
            if command.parent is None:
                embed.add_field(
                    name=f"`{self.context.clean_prefix}{command.name}`",
                    value=command.description
                    if command.description is not None
                    else "No Command Description",
                    inline=False,
                )
        await self.dispatch_help(embed)
