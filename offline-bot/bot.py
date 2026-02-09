import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Optional: keep_alive for Replit / free hosts
from webserver import keep_alive
keep_alive()


# ──────────────────────────────
# ENV + CONFIG
# ──────────────────────────────
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing from .env")

# ──────────────────────────────
# INTENTS
# ──────────────────────────────
intents = discord.Intents.all()
intents.message_content = True

# ──────────────────────────────
# BOT INSTANCE
# ──────────────────────────────
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    owner_id=OWNER_ID
)

# ──────────────────────────────
# COGS TO LOAD
# ──────────────────────────────
COGS = [
    "cogs.verification",
    "cogs.tickets",
    "cogs.moderation",
    "cogs.antinuke",
    "cogs.owner_commands"
]

# ──────────────────────────────
# EVENTS
# ──────────────────────────────
@bot.event
async def on_ready():
    print("────────────────────────────────")
    print(f"Logged in as: {bot.user}")
    print(f"User ID: {bot.user.id}")
    print("────────────────────────────────")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {len(synced)}")
    except Exception as e:
        print(f"[ERROR] Slash sync failed: {e}")

    print("Bot is fully ready.")

# ──────────────────────────────
# ERROR HANDLING
# ──────────────────────────────
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You do not have permission to use this command.")
    elif isinstance(error, commands.NotOwner):
        await ctx.send("❌ Owner-only command.")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(f"[ERROR] {error}")
        await ctx.send("⚠️ An unexpected error occurred.")

# ──────────────────────────────
# LOAD COGS
# ──────────────────────────────
async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"[LOADED] {cog}")
        except Exception as e:
            print(f"[FAILED] {cog}: {e}")

# ──────────────────────────────
# MAIN ENTRY
# ──────────────────────────────
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    if KEEP_ALIVE_AVAILABLE:
        keep_alive()
    asyncio.run(main())
