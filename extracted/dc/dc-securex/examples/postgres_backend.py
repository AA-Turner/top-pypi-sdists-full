"""
Example: Using SecureX SDK with PostgreSQL storage backend
"""

import discord
from securex import SecureX
import os

# Create your Discord bot
bot = discord.Bot(intents=discord.Intents.all())

# Option 1: JSON Storage (default, no changes needed)
sdk_json = SecureX(bot=bot)

# Option 2: PostgreSQL Storage
sdk_postgres = SecureX(
    bot=bot,
    storage_backend="postgres",
    postgres_url=os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/securex"),
    postgres_pool_size=15  # Optional: customize pool size
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # Enable SDK with PostgreSQL
    await sdk_postgres.enable(
        guild_id=12345678901234567,  # Your guild ID
        whitelist=[111111111111111111],  # Your user ID
        auto_backup=True,
        punishments={
            "channel_delete": "ban",
            "role_create": "kick"
        }
    )
    
    print("✅ SecureX enabled with PostgreSQL backend!")
    print(f"✅ Connection pool: {sdk_postgres.storage.pool.get_size()} connections")

# Event callback example
@sdk_postgres.on_threat_detected
async def handle_threat(event):
    print(f"🚨 Threat detected: {event.type}")
    print(f"   Actor: {event.actor_id}")
    print(f"   Target: {event.target_name}")
    print(f"   Prevented: {event.prevented}")
    print(f"   Punishment: {event.punishment_action}")

# Graceful shutdown
@bot.event
async def on_disconnect():
    # Close PostgreSQL connection pool
    await sdk_postgres.disable()

# Run bot
bot.run("YOUR_BOT_TOKEN")
