import discord
from discord.ext import commands
from utils.checks import is_admin

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="kick")
    @is_admin()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked {member} | {reason}")

    @commands.hybrid_command(name="ban")
    @is_admin()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member} | {reason}")

    @commands.hybrid_command(name="timeout")
    @is_admin()
    async def timeout(self, ctx, member: discord.Member, minutes: int):
        await member.timeout(discord.utils.utcnow() + discord.timedelta(minutes=minutes))
        await ctx.send(f"⏱️ Timed out {member} for {minutes} minutes")

    @commands.hybrid_command(name="addrole")
    @is_admin()
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"➕ Added {role} to {member}")

    @commands.hybrid_command(name="striprole")
    @is_admin()
    async def striprole(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"➖ Removed {role} from {member}")

    @commands.hybrid_command(name="stripall")
    @is_admin()
    async def stripall(self, ctx, member: discord.Member):
        await member.edit(roles=[])
        await ctx.send(f"🚨 All roles stripped from {member}")

    @commands.hybrid_command(name="purge")
    @is_admin()
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Deleted {amount} messages", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
