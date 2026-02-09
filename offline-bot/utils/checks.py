from discord.ext import commands
from config import OWNER_ID

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)

def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator or ctx.author.id == OWNER_ID
    return commands.check(predicate)
