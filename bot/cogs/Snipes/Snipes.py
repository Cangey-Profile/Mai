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


from discord.ext import commands
from discord.ext.commands import BucketType

from typing import Union

from helpers.constants import *
from helpers.logging import log
from helpers.custommeta import CustomCog as Cog

from db.models import Guild, Snipe


class Snipes(
    Cog,
    name="Snipes",
    description="Snipe Deleted or Edited Messages",
    emoji=Emoji.SNIPER,
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.delete_snipes = {}
        self.edit_snipes = {}

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(
            f"[bright_green][EXTENSION][/bright_green][blue3] {type(self).__name__} READY[/blue3]"
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return

        self.delete_snipes[message.channel] = message

    @commands.Cog.listener()
    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ):
        if before.author.bot:
            return

        self.edit_snipes[after.channel] = (before, after)

    @commands.group(
        invoke_without_subcommand=True, description="Manage Snipe Commands"
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, read_messages=True)
    @commands.bot_has_guild_permissions(send_messages=True, read_messages=True)
    async def snipe(self, ctx: commands.Context) -> None:
        guild = await Guild.get_or_none(discord_id=ctx.guild.id)

        snipe = (await Snipe.get_or_create(guild=guild))[0]

        snipe_enabled = snipe.enabled

        if not snipe_enabled:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `Snipe` Module Disabled.",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        if ctx.invoked_subcommand is None:
            try:
                sniped_message = self.delete_snipes[ctx.channel]
            except KeyError:
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} There are no deleted messages to snipe!",
                )
                await ctx.send(embed=embed, delete_after=15)
                return
            else:
                result = discord.Embed(
                    color=Colors.DEFAULT,
                    description=sniped_message.content,
                    timestamp=sniped_message.created_at,
                )
                result.set_author(
                    name=sniped_message.author.display_name,
                    icon_url=sniped_message.author.avatar.url,
                )
                await ctx.send(embed=result)

    @commands.cooldown(1, 2, BucketType.user)
    @snipe.command(
        name="edit", description="View Edited Messages", brief="snipe edit"
    )
    async def snipe_edit(self, ctx: commands.Context) -> None:
        guild = await Guild.get_or_none(discord_id=ctx.guild.id)

        snipe = (await Snipe.get_or_create(guild=guild))[0]

        snipe_enabled = snipe.enabled

        if not snipe_enabled:
            embed = discord.Embed(
                color=Colors.ERROR,
                description=f"{Emoji.ERROR} `Snipe` Module Disabled.",
            )
            await ctx.send(embed=embed, delete_after=15)
            return

        try:
            before, after = self.edit_snipes[ctx.channel]
        except KeyError:
            await ctx.send(
                "There are no message edits in this channel to snipe!"
            )
        else:
            result = discord.Embed(
                color=Colors.DEFAULT, timestamp=after.edited_at
            )
            result.add_field(name="Before", value=before.content, inline=False)
            result.add_field(name="After", value=after.content, inline=False)
            result.set_author(
                name=after.author.display_name, icon_url=after.author.avatar.url
            )
            await ctx.send(embed=result)

    @commands.cooldown(1, 2, BucketType.user)
    @snipe.command(
        name="toggle",
        description="Toggle Snipes On Or Off",
        brief="snipe toggle on\nsnipe toggle off\nsnipe toggle True\nsnipe toggle False",
    )
    @commands.bot_has_permissions(
        send_messages=True,
        read_messages=True,
        manage_messages=True,
        manage_channels=True,
    )
    @commands.bot_has_guild_permissions(
        send_messages=True,
        read_messages=True,
        manage_messages=True,
        manage_channels=True,
    )
    async def snipe_toggle(
        self, ctx: commands.Context, toggle: Union[bool, str]
    ) -> None:
        if type(toggle) is str:
            if toggle == "on":
                toggle = True
            elif toggle == "off":
                toggle = False
            elif toggle != "on" or "off":
                embed = discord.Embed(
                    color=Colors.ERROR,
                    description=f"{Emoji.ERROR} `toggle` expects `on`/`off`, not `{str(toggle)}`",
                )
                await ctx.send(embed=embed)
                return

        guild = await Guild.get_or_none(discord_id=ctx.guild.id)

        snipe = (await Snipe.get_or_create(guild=guild))[0]

        snipe.enabled = toggle
        await snipe.save(update_fields=["enabled"])
        await snipe.refresh_from_db(fields=["enabled"])
        embed = discord.Embed(
            color=Colors.DEFAULT,
            description=f"**Snipe Toggled To:** `{toggle}`",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Snipes(bot))
