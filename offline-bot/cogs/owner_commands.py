import discord
from discord.ext import commands
from utils.checks import is_owner

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "server_settings"):
            bot.server_settings = {}

    @is_owner()
    @commands.hybrid_command(name="owner_setwelcomechannel")
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        self.bot.server_settings[ctx.guild.id] = self.bot.server_settings.get(ctx.guild.id, {})
        self.bot.server_settings[ctx.guild.id]["welcome_channel"] = channel.id
        await ctx.send(f"✅ Welcome channel set to {channel.mention}")

    @is_owner()
    @commands.hybrid_command(name="owner_setleaveschannel")
    async def set_leaves_channel(self, ctx, channel: discord.TextChannel):
        self.bot.server_settings[ctx.guild.id] = self.bot.server_settings.get(ctx.guild.id, {})
        self.bot.server_settings[ctx.guild.id]["leaves_channel"] = channel.id
        await ctx.send(f"✅ Leaves channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(OwnerCommands(bot))
