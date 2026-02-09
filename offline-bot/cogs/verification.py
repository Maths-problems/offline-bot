# cogs/verification.py
import discord
from discord.ext import commands
from utils.checks import is_owner

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # IDs will be set via owner commands
        self.bot.verification_role_id = getattr(bot, "verification_role_id", None)
        self.bot.verify_channel_id = getattr(bot, "verify_channel_id", None)

    # -------------------- OWNER COMMANDS --------------------
    @is_owner()
    @commands.hybrid_command(name="owner_setverificationrole")
    async def owner_set_verification_role(self, ctx, role: discord.Role):
        """Sets the role to give users after verifying"""
        self.bot.verification_role_id = role.id
        await ctx.send(f"✅ Verification role set to: {role.mention}")

    @is_owner()
    @commands.hybrid_command(name="owner_setverifychannel")
    async def owner_set_verify_channel(self, ctx, channel: discord.TextChannel):
        """Sets the verification channel"""
        self.bot.verify_channel_id = channel.id
        await ctx.send(f"✅ Verification channel set to: {channel.mention}")

    @is_owner()
    @commands.hybrid_command(name="owner_addverificationui")
    async def owner_add_verification_ui(self, ctx):
        """Sends the persistent verification button embed"""
        verify_channel = self.bot.get_channel(self.bot.verify_channel_id)
        if not verify_channel:
            await ctx.send("❌ Verification channel not set")
            return

        embed = discord.Embed(
            title="Verify Yourself",
            description="Click the button below to verify and access the server!",
            color=discord.Color.blue()
        )

        view = discord.ui.View(timeout=None)  # Persistent button

        button = discord.ui.Button(label="Verify", style=discord.ButtonStyle.blurple)

        async def button_callback(interaction: discord.Interaction):
            role_id = getattr(self.bot, "verification_role_id", None)
            if not role_id:
                await interaction.response.send_message("❌ Verification role not set.", ephemeral=True)
                return

            verified_role = interaction.guild.get_role(role_id)
            if verified_role in interaction.user.roles:
                await interaction.response.send_message("✅ You are already verified.", ephemeral=True)
                return

            # Assign the role
            await interaction.user.add_roles(verified_role)

            # Unlock all channels except the verification channel
            for channel in interaction.guild.text_channels:
                if channel.id != verify_channel.id:
                    await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

            await interaction.response.send_message("✅ You are now verified!", ephemeral=True)

        button.callback = button_callback
        view.add_item(button)

        await verify_channel.send(embed=embed, view=view)

# -------------------- SETUP --------------------
async def setup(bot):
    await bot.add_cog(Verification(bot))
