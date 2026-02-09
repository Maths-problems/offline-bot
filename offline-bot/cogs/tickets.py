import discord
from discord.ext import commands, tasks
from discord.ui import View, Button
from utils.checks import is_owner
from datetime import datetime, timedelta

TICKET_CATEGORY = "Tickets"

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.ticket_counter = getattr(bot, "ticket_counter", {})
        self.bot.ticket_support_roles = getattr(bot, "ticket_support_roles", set())
        self.active_tickets = {}  # channel_id: close_time
        self.autoclose.start()

    @tasks.loop(minutes=5)
    async def autoclose(self):
        now = datetime.utcnow()
        for cid, close_time in list(self.active_tickets.items()):
            if now >= close_time:
                channel = self.bot.get_channel(cid)
                if channel:
                    await channel.delete()
                self.active_tickets.pop(cid)

    @is_owner()
    @commands.hybrid_command(name="owner_addticketui")
    async def owner_add_ticket_ui(self, ctx, *, content: str):
        """Owner-only: add ticket button UI"""
        embed = discord.Embed(title="Support Tickets", description=content, color=discord.Color.blue())
        view = View()

        button = Button(label="Open Ticket", style=discord.ButtonStyle.blurple)

        async def button_callback(interaction: discord.Interaction):
            guild_id = interaction.guild.id
            number = self.bot.ticket_counter.get(guild_id, 0) + 1
            self.bot.ticket_counter[guild_id] = number

            category = discord.utils.get(interaction.guild.categories, name=TICKET_CATEGORY)
            if not category:
                category = await interaction.guild.create_category(TICKET_CATEGORY)

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True)
            }

            channel_name = f"ticket-{number}"
            channel = await interaction.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
            self.active_tickets[channel.id] = datetime.utcnow() + timedelta(hours=24)
            await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

        button.callback = button_callback
        view.add_item(button)
        await ctx.send(embed=embed, view=view)

    @is_owner()
    @commands.hybrid_command(name="owner_addticketsupportrole")
    async def owner_add_ticket_support_role(self, ctx, role: discord.Role):
        self.bot.ticket_support_roles.add(role.id)
        await ctx.send(f"✅ {role.name} can manage tickets")

    @commands.hybrid_command(name="closeticket")
    async def close_ticket(self, ctx):
        allowed = False
        if ctx.author.id in self.bot.ticket_support_roles:
            allowed = True
        if any(r.id in self.bot.ticket_support_roles for r in ctx.author.roles):
            allowed = True
        if ctx.author.id == ctx.guild.owner_id:
            allowed = True

        if ctx.channel.category and ctx.channel.category.name == TICKET_CATEGORY:
            if allowed:
                await ctx.send("🗑️ Closing ticket...", delete_after=3)
                await ctx.channel.delete()
            else:
                await ctx.send("❌ You cannot close this ticket")
        else:
            await ctx.send("❌ Use this in a ticket channel only")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
