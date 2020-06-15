from .audit_log import AuditLogger
from .commands import Commands

cogs = [AuditLogger, Commands]


def init_cogs(bot):
    for cog in cogs:
        bot.add_cog(cog(bot))
