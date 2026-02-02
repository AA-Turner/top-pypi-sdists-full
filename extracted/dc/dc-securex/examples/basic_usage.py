"""
SecureX SDK - Basic Usage Example
Shows how to use the SDK with automatic role position monitoring enabled by default.
"""
import discord
from discord.ext import commands
from securex import SecureX

# Create bot with all intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Initialize SecureX SDK
sx = SecureX(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"📊 Guilds: {len(bot.guilds)}")
    
    # Enable anti-nuke protection
    # Role position monitoring is ENABLED BY DEFAULT since v1.2.1
    await sx.enable(
        whitelist=[YOUR_USER_ID_HERE],  # Add trusted user IDs optional
        auto_backup=True,
        role_position_monitoring=True  # Already True by default!
    )
    
    print("✅ SecureX enabled!")

# Optional: Listen to threat events
@sx.on_threat_detected
async def handle_threat(threat):
    """Called when a threat is detected and prevented"""
    print(f"🚨 Threat detected: {threat.type}")
    print(f"   Actor: {threat.actor_id}")
    print(f"   Target: {threat.target_name}")
    print(f"   Prevented: {threat.prevented}")
    print(f"   Restored: {threat.restored}")

# Commands
@bot.command()
@commands.has_permissions(administrator=True)
async def backup(ctx):
    """Force create a backup"""
    await sx.backup_manager.create_backup(ctx.guild.id)
    await ctx.send("✅ Backup created!")

@bot.command()
@commands.has_permissions(administrator=True)
async def monitor_status(ctx):
    """Check role monitor status"""
    status = "✅ Active" if sx.role_monitor.enabled else "❌ Disabled"
    await ctx.send(f"**Role Position Monitor:** {status}\n**Check Interval:** 5 seconds")

@bot.command()
@commands.has_permissions(administrator=True)
async def stop_monitor(ctx):
    """Stop role position monitoring"""
    sx.role_monitor.stop()
    await ctx.send("🛑 Role position monitoring stopped")

@bot.command()
@commands.has_permissions(administrator=True)
async def start_monitor(ctx):
    """Start role position monitoring"""
    sx.role_monitor.start()
    await ctx.send("🔍 Role position monitoring started")

# Run bot
if __name__ == "__main__":
    bot.run("YOUR_BOT_TOKEN_HERE")
