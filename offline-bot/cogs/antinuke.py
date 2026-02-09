import discord
from discord.ext import commands
import time
from config import OWNER_ID

NUKE_THRESHOLD = 5
TIME_WINDOW = 8

actions = {}  # user_id: [timestamps]

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_roles = {}
        self.deleted_channels = {}

    def record_action(self, user_id):
        now = time.time()
        ts = [t for t in actions.get(user_id, []) if now - t < TIME_WINDOW]
        ts.append(now)
        actions[user_id] = ts
        return len(ts)

    async def punish_and_revert(self, guild, user, reason):
        member = guild.get_member(user.id)
        if member:
            await member.edit(roles=[])
            await member.ban(reason=reason)
        owner = guild.get_member(OWNER_ID)
        if owner:
            await owner.send(f"🚨 ANTI-NUKE triggered!\nUser: {user}\nReason: {reason}")

        # Recreate roles
        for rdata in self.deleted_roles.values():
            await guild.create_role(**rdata)
        self.deleted_roles.clear()

        # Recreate channels
        for cdata in self.deleted_channels.values():
            await guild.create_text_channel(**cdata)
        self.deleted_channels.clear()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        self.deleted_roles[role.id] = {
            "name": role.name,
            "permissions": role.permissions,
            "colour": role.color,
            "hoist": role.hoist,
            "mentionable": role.mentionable
        }
        async for entry in role.guild.audit_logs(limit=1):
            if entry.user.id == OWNER_ID:
                return
            if self.record_action(entry.user.id) >= NUKE_THRESHOLD:
                await self.punish_and_revert(role.guild, entry.user, "Mass role deletion")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        self.deleted_channels[channel.id] = {
            "name": channel.name,
            "category": channel.category,
            "overwrites": channel.overwrites,
            "type": channel.type,
            "position": channel.position
        }
        async for entry in channel.guild.audit_logs(limit=1):
            if entry.user.id == OWNER_ID:
                return
            if self.record_action(entry.user.id) >= NUKE_THRESHOLD:
                await self.punish_and_revert(channel.guild, entry.user, "Mass channel deletion")

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
