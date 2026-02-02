"""
Example: Member Protection
Shows bot verification, ban/kick prevention, and DM invites.
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
    print("🛡️ Member protection active!")

@sx.on_threat_detected
async def handle_member_threat(threat):
    """Handle member-related threats"""
    if threat.type == "member_join":
        # Bot was added without authorization
        print(f"🚨 Unauthorized bot: {threat.target_name}")
        print(f"   Added by: {threat.actor_id}")
        print(f"   Kicked: {threat.prevented}")
    
    elif threat.type == "member_ban":
        # Unauthorized ban detected
        print(f"🚨 Unauthorized ban: {threat.target_name}")
        print(f"   Banned by: {threat.actor_id}")
        print(f"   User invited back via DM: {threat.restored}")
    
    elif threat.type == "member_remove":
        # Unauthorized kick detected
        print(f"🚨 Unauthorized kick: {threat.target_name}")
        print(f"   Kicked by: {threat.actor_id}")
        print(f"   User invited back via DM: {threat.restored}")

@bot.command()
async def member_info(ctx):
    """Show member protection features"""
    embed = discord.Embed(
        title="🛡️ Member Protection",
        description="Prevents unauthorized member actions",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Bot Verification",
        value="• Kicks unauthorized bot additions\n• Only whitelisted users can add bots",
        inline=False
    )
    embed.add_field(
        name="Ban/Kick Protection",
        value="• Detects unauthorized bans/kicks\n• Sends DM invite to affected user\n• User can rejoin via invite link",
        inline=False
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
