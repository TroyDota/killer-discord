import logging
import discord
from discord.ext import commands

log = logging.getLogger("killer")


class Commands(commands.Cog, name="CustomCommands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def member(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        status = {
            discord.Status.dnd: "<:DoNotDisturb:717300897339801640>",
            discord.Status.do_not_disturb: "<:DoNotDisturb:717300897339801640>",
            discord.Status.online: "<:Online:717300882835767327>",
            discord.Status.idle: "<:Idle:717300910832746606>",
            discord.Status.invisible: "<:Offline:717300928822378536>",
            discord.Status.offline: "<:Offline:717300928822378536>",
        }.get(member.status)

        if isinstance(member.activity, discord.activity.Streaming):
            status = "<:Streaming:717300942860714104>"

        if not status:
            return

        embed = discord.Embed(color=0x56136F)
        embed.add_field(
            name="**Member Information**",
            value=f"**Username: `{member}`\nID: `{member.id}`\nStatus: {status}\nBot: `{'Yes' if member.bot else 'No'}`\nRegister: `{member.created_at.strftime('%B %d, %Y')}`**",
            inline=True,
        )
        embed.add_field(
            name="**Server Information**",
            value=f"**Nickname: `{member.nick or 'No'}`\nJoin: `{member.joined_at.strftime('%B %d, %Y')}`\nRoles: **{' '.join([role.mention for role in member.roles][1:])}",
            inline=True,
        )
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def eval(self, ctx, *args):
        try:
            await ctx.send(eval(" ".join(list(args))))
        except Exception as e:
            await ctx.send(str(e))
