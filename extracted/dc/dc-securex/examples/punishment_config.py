"""
Example: Configuring Punishment Actions

Shows how to configure different punishment actions for different violation types.
"""
import discord
from discord.ext import commands
from securex import SecureX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
    # Example 1: Ban for destructive actions, kick for spam
    await sx.enable(
        punishments={
            "channel_delete": "ban",      # Ban anyone who deletes channels
            "role_delete": "ban",          # Ban anyone who deletes roles
            "channel_create": "kick",      # Kick channel spammers
            "role_create": "kick"          # Kick role spammers
        },
        notify_user=True  # DM violators about punishment
    )
    
    print("✅ Punishment system enabled")


@sx.on_threat_detected
async def log_threat(threat):
    """Log all threats with punishment info"""
    print(f"""
    🚨 Threat Detected:
       Type: {threat.type}
       Actor: {threat.actor_id}
       Target: {threat.target_name}
       Restored: {threat.restored}
       Punishment: {threat.punishment_action or 'none'}
    """)


# Example 2: Use timeouts for most violations
@bot.command()
@commands.is_owner()
async def setup_timeout_mode(ctx):
    """Configure SDK to use timeouts instead of bans"""
    await sx.enable(
        punishments={
            "channel_delete": "timeout",
            "channel_create": "timeout",
            "role_delete": "timeout",
            "role_create": "timeout",
            "channel_update": "warn"  # Just warn for minor changes
        },
        timeout_duration=1800,  # 30 minutes
        notify_user=True
    )
    await ctx.send("✅ Configured timeout mode (30 min)")


# Example 3: Strict mode - ban everything
@bot.command()
@commands.is_owner()
async def setup_strict_mode(ctx):
    """Ban all unauthorized actions"""
    await sx.enable(
        punishments={
            "channel_delete": "ban",
            "channel_create": "ban",
            "channel_update": "ban",
            "role_delete": "ban",
            "role_create": "ban",
            "role_update": "ban"
        },
        notify_user=True
    )
    await ctx.send("⚠️ Strict mode enabled - all violations = ban")


# Example 4: Lenient mode - just warnings
@bot.command()
@commands.is_owner()
async def setup_lenient_mode(ctx):
    """Just warn violators without taking action"""
    await sx.enable(
        punishments={
            "channel_delete": "warn",
            "channel_create": "warn",
            "role_delete": "warn",
            "role_create": "warn"
        },
        notify_user=True
    )
    await ctx.send("ℹ️ Lenient mode - warnings only")


bot.run("YOUR_BOT_TOKEN")
