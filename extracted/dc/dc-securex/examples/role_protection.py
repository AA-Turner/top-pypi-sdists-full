"""
Example: Role Protection with Position Monitoring
Shows role protection and automatic position restoration.
"""
import discord
from discord.ext import commands
from securex import SecureX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
    # Enable with role monitoring (enabled by default)
    await sx.enable(whitelist=[123456789])
    
    print("🛡️ Role protection + position monitoring active!")
    print("   - Prevents unauthorized role creation/deletion")
    print("   - Restores role positions every 5 seconds")
    print("   - Reverts role permission changes")

@sx.on_threat_detected
async def handle_role_threat(threat):
    """Handle role-related threats"""
    if threat.type in ["role_create", "role_delete", "role_update"]:
        print(f"🚨 Role threat: {threat.type}")
        print(f"   Role: {threat.target_name}")
        print(f"   Actor: {threat.actor_id}")

@bot.command()
async def role_info(ctx):
    """Show role protection info"""
    monitor_status = "✅ Active" if sx.role_monitor.enabled else "❌ Disabled"
    
    embed = discord.Embed(
        title="🛡️ Role Protection",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Position Monitor",
        value=f"Status: {monitor_status}\nCheck Interval: 5 seconds\nMethod: Bulk endpoint",
        inline=False
    )
    embed.add_field(
        name="Protected Actions",
        value="• Role creation\n• Role deletion\n• Position changes\n• Permission changes",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def toggle_monitor(ctx):
    """Toggle role position monitoring"""
    if sx.role_monitor.enabled:
        sx.role_monitor.stop()
        await ctx.send("🛑 Position monitoring stopped")
    else:
        sx.role_monitor.start()
        await ctx.send("🔍 Position monitoring started")

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
