"""
Example: Webhook Protection
Shows webhook spam detection and removal.
"""
import discord
from discord.ext import commands
from securex import SecureX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await sx.enable(whitelist=[123456789])
    print("🛡️ Webhook protection active!")

@sx.on_threat_detected
async def handle_webhook_threat(threat):
    """Handle webhook spam"""
    if threat.type == "webhook_spam":
        print(f"🚨 Webhook spam detected in #{threat.target_name}")
        print(f"   All webhooks removed: {threat.prevented}")
        print(f"   Details: {threat.details}")

@bot.command()
async def webhook_info(ctx):
    """Show webhook protection info"""
    embed = discord.Embed(
        title="🛡️ Webhook Protection",
        description="Prevents webhook spam attacks",
        color=discord.Color.red()
    )
    embed.add_field(
        name="Detection",
        value="Monitors webhook creation events\nDetects spam patterns (multiple webhooks in short time)",
        inline=False
    )
    embed.add_field(
        name="Response",
        value="• Removes all webhooks in affected channel\n• Prevents webhook spam raids\n• Alerts administrators",
        inline=False
    )
    embed.add_field(
        name="Whitelist",
        value="Whitelisted users can create webhooks normally",
        inline=False
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
