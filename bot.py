import discord
import datetime
from discord.ext import commands

colors = {
    "BAN": discord.Colour.red(),
    "KICK": discord.Colour.orange(),
    "UNBAN": discord.Colour.green(),
    "VOICE_CHANGE": discord.Colour.teal(),
}


class AuditLogger(commands.Cog, name="AuditLogger"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(
            description=f"@{user}",
            colour=colors["BAN"],
            timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc),
        )
        perp = None
        reason = None
        async for _log in guild.audit_logs(limit=5):
            if _log.action != discord.AuditLogAction.ban:
                continue
            if _log.target.id == user.id:
                perp = _log.user
                reason = _log.reason
                break

        if perp:
            embed.add_field(name="Banned By", value=perp.mention, inline=False)
        if reason:
            embed.add_field(name="Reason", value=str(reason), inline=False)

        embed.set_footer(text="User ID: " + str(user.id))
        embed.set_author(
            name=f"{user} has been banned from the guild",
            url=user.avatar_url,
            icon_url=user.avatar_url,
        )
        embed.set_thumbnail(url=user.avatar_url)
        await self._send_event(guild, embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(
            description=f"@{user}",
            colour=colors["UNBAN"],
            timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc),
        )
        perp = None
        reason = None

        async for _log in guild.audit_logs(limit=5):
            if _log.action != discord.AuditLogAction.unban:
                continue
            if _log.target.id == user.id:
                perp = _log.user
                reason = _log.reason
                break

        if perp:
            embed.add_field(name="Unbanned By", value=perp.mention, inline=False)
        if reason:
            embed.add_field(name="Reason", value=str(reason), inline=False)

        embed.set_footer(text="User ID: " + str(user.id))
        embed.set_author(
            name=f"{user} has been unbanned from the guild",
            url=user.avatar_url,
            icon_url=user.avatar_url,
        )
        embed.set_thumbnail(url=user.avatar_url)
        await self._send_event(guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        embed = discord.Embed(
            description=f"@{member}",
            colour=colors["KICK"],
            timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc),
        )
        perp = None
        reason = None
        async for _log in guild.audit_logs(limit=5):
            if _log.action != discord.AuditLogAction.kick:
                continue
            if _log.target.id == member.id:
                perp = _log.user
                reason = _log.reason
                break

        if perp:
            embed.add_field(name="Kicked by", value=perp.mention, inline=False)
        if reason:
            embed.add_field(name="Reason", value=str(reason), inline=False)

        embed.add_field(
            name="Total Users:", value=str(len(guild.members)), inline=False
        )
        embed.set_footer(text="User ID: " + str(member.id))
        embed.set_author(
            name=f"{member} has left the guild",
            url=member.avatar_url,
            icon_url=member.avatar_url,
        )
        embed.set_thumbnail(url=member.avatar_url)
        await self._send_event(guild, embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc),
            colour=colors["VOICE_CHANGE"],
        )
        embed.set_author(name=f"{member} Voice State Update")
        worth_updating = False
        description = ""
        action = discord.AuditLogAction.member_update
        if before.deaf != after.deaf:
            worth_updating = True
            if after.deaf:
                description += member.mention + " was deafened.\n"
            else:
                description += member.mention + " was undeafened.\n"
        elif before.mute != after.mute:
            worth_updating = True
            if after.mute:
                description += member.mention + " was muted.\n"
            else:
                description += member.mention + " was unmuted.\n"
        elif before.channel != after.channel:
            if after.channel is None:
                worth_updating = True
                action = discord.AuditLogAction.member_disconnect
                description += member.mention + " has left\n" + before.channel.name
            elif after.channel and before.channel:
                worth_updating = True
                action = discord.AuditLogAction.member_move
                description += (
                    member.mention
                    + " has moved from "
                    + before.channel.name
                    + " to "
                    + after.channel.name
                )

        embed.description = description

        if not worth_updating:
            return

        perp = None
        reason = None
        async for _log in guild.audit_logs(limit=2):
            if _log.action == action and (
                not _log.target or (_log.target and _log.target.id == member.id)
            ):
                perp = _log.user
                if _log.reason:
                    reason = _log.reason
                break

        if not perp:
            return

        embed.add_field(name="Updated by", value=perp.mention, inline=False)
        if reason:
            embed.add_field(name="Reason ", value=reason, inline=False)

        await self._send_event(guild, embed)

    async def _send_event(self, guild: discord.Guild, embed: discord.Embed):
        channel = discord.utils.get(guild.text_channels, name="event-logs")
        await channel.send(embed=embed)


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


cogs = [AuditLogger, Commands]


def init_cogs(bot):
    for cog in cogs:
        bot.add_cog(cog(bot))


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="$")
    init_cogs(bot)

    @bot.event
    async def on_ready():
        print("Ready")
        await bot.change_presence(
            activity=discord.Streaming(name="HI", url="https://twitch.tv/yikes")
        )

    bot.run("NzE1MTIzOTAyODI5MDM1NTcy.Xs4pEA.WgqNn5iUYmjghc02PsXOGujaZhA")
