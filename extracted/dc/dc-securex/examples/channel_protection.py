"""
Example: Channel Protection
Shows how SecureX detects and prevents unauthorized channel changes.
"""
import discord
from discord.ext import commands
from securex import SecureX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
    # Enable protection - whitelisted users can make changes
    await sx.enable(
        whitelist=[123456789],  # Add trusted admin user IDs
        auto_backup=True
    )
    
    print("🛡️ Channel protection active!")

@sx.on_threat_detected
async def handle_channel_threat(threat):
    """Handle channel-related threats"""
    if threat.type in ["channel_create", "channel_delete", "channel_update"]:
        print(f"🚨 Channel threat: {threat.type}")
        print(f"   Channel: {threat.target_name}")
        print(f"   Actor: {threat.actor_id}")
        print(f"   Action prevented: {threat.prevented}")
        print(f"   Restored: {threat.restored}")

@bot.command()
async def test_protection(ctx):
    """Test channel protection by trying to create/delete channels"""
    await ctx.send(
        "**Channel Protection Features:**\n"
        "✅ Prevents unauthorized channel creation\n"
        "✅ Restores deleted channels\n"
        "✅ Reverts permission changes\n"
        "\n**Try these as a non-whitelisted user:**\n"
        "• Create a new channel\n"
        "• Delete a channel\n"
        "• Change channel permissions"
    )

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
