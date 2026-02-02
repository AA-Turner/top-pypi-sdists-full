"""
Example: Advanced Usage with Custom Callbacks
Shows how to use all callbacks and create custom threat handling.
"""
import discord
from discord.ext import commands
from securex import SecureX
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)

# Track threats for statistics
threat_stats = {
    "channel_create": 0,
    "channel_delete": 0,
    "channel_update": 0,
    "role_create": 0,
    "role_delete": 0,
    "role_update": 0,
    "member_join": 0,
    "member_ban": 0,
    "member_remove": 0,
    "webhook_spam": 0
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await sx.enable(whitelist=[bot.owner_id])
    print("🛡️ All protection systems active!")

# === Threat Detection Callback ===
@sx.on_threat_detected
async def handle_threat(threat):
    """Main threat handler - logs and tracks all threats"""
    # Update statistics
    threat_stats[threat.type] = threat_stats.get(threat.type, 0) + 1
    
    # Log to console
    print(f"🚨 [{threat.type.upper()}] Threat detected")
    print(f"   Actor: {threat.actor_id}")
    print(f"   Target: {threat.target_name} (ID: {threat.target_id})")
    print(f"   Prevented: {threat.prevented}")
    print(f"   Restored: {threat.restored}")
    
    # Send to log channel
    log_channel_id = 123456789  # Replace with your log channel ID
    log_channel = bot.get_channel(log_channel_id)
    
    if log_channel:
        embed = discord.Embed(
            title=f"🚨 {threat.type.replace('_', ' ').title()}",
            color=discord.Color.red(),
            timestamp=threat.timestamp
        )
        embed.add_field(name="Actor", value=f"<@{threat.actor_id}>", inline=True)
        embed.add_field(name="Target", value=threat.target_name, inline=True)
        embed.add_field(name="Status", value="✅ Prevented & Restored" if threat.restored else "✅ Prevented", inline=False)
        
        if threat.details:
            details_text = "\n".join(f"• {k}: {v}" for k, v in threat.details.items())
            embed.add_field(name="Details", value=details_text, inline=False)
        
        await log_channel.send(embed=embed)

# === Backup Completion Callback ===
@sx.on_backup_completed
async def on_backup(backup_info):
    """Called when backup completes"""
    print(f"💾 Backup completed: {backup_info.channel_count} channels, {backup_info.role_count} roles")

# === Restore Completion Callback ===
@sx.on_restore_completed
async def on_restore(restore_result):
    """Called when restoration completes"""
    print(f"🔄 Restore completed: {restore_result}")

# === Whitelist Change Callback ===
@sx.on_whitelist_changed
async def on_whitelist_change(data):
    """Called when whitelist is modified"""
    print(f"🔐 Whitelist changed: {data}")

# === Commands ===
@bot.command()
@commands.has_permissions(administrator=True)
async def threat_stats(ctx):
    """Show threat statistics"""
    total_threats = sum(threat_stats.values())
    
    embed = discord.Embed(
        title="📊 Threat Statistics",
        description=f"Total threats prevented: **{total_threats}**",
        color=discord.Color.blue()
    )
    
    # Group by category
    channel_threats = threat_stats["channel_create"] + threat_stats["channel_delete"] + threat_stats["channel_update"]
    role_threats = threat_stats["role_create"] + threat_stats["role_delete"] + threat_stats["role_update"]
    member_threats = threat_stats["member_join"] + threat_stats["member_ban"] + threat_stats["member_remove"]
    webhook_threats = threat_stats["webhook_spam"]
    
    embed.add_field(name="🔸 Channel Threats", value=channel_threats, inline=True)
    embed.add_field(name="🎭 Role Threats", value=role_threats, inline=True)
    embed.add_field(name="👥 Member Threats", value=member_threats, inline=True)
    embed.add_field(name="🔗 Webhook Threats", value=webhook_threats, inline=True)
    
    # Detailed breakdown
    details = []
    for threat_type, count in sorted(threat_stats.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            details.append(f"• {threat_type}: {count}")
    
    if details:
        embed.add_field(name="Breakdown", value="\n".join(details), inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def reset_stats(ctx):
    """Reset threat statistics"""
    global threat_stats
    threat_stats = {k: 0 for k in threat_stats.keys()}
    await ctx.send("✅ Threat statistics reset")

@bot.command()
async def protection_status(ctx):
    """Show all protection systems status"""
    embed = discord.Embed(
        title="🛡️ Protection Status",
        color=discord.Color.green()
    )
    
    # Role monitor
    monitor_status = "✅ Active" if sx.role_monitor.enabled else "❌ Disabled"
    embed.add_field(
        name="Role Position Monitor",
        value=f"{monitor_status}\nInterval: 5 seconds",
        inline=True
    )
    
    # Whitelist count
    whitelisted = await sx.whitelist.get_whitelisted_users(ctx.guild.id)
    embed.add_field(
        name="Whitelist",
        value=f"{len(whitelisted)} users",
        inline=True
    )
    
    # Threat count
    total_threats = sum(threat_stats.values())
    embed.add_field(
        name="Threats Prevented",
        value=f"{total_threats} total",
        inline=True
    )
    
    embed.add_field(
        name="Protected Features",
        value="✅ Channels\n✅ Roles\n✅ Members\n✅ Webhooks\n✅ Positions\n✅ Permissions",
        inline=False
    )
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
