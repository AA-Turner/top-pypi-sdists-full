"""
Example: Whitelist Management
Shows how to manage authorized users.
"""
import discord
from discord.ext import commands
from securex import SecureX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
    # Enable with initial whitelist
    await sx.enable(
        whitelist=[bot.owner_id]  # Bot owner is whitelisted
    )
    
    print("🛡️ Protection active with whitelist!")

@bot.command()
@commands.is_owner()
async def whitelist_add(ctx, user: discord.Member):
    """Add user to whitelist"""
    await sx.whitelist.add(ctx.guild.id, user.id)
    await ctx.send(f"✅ {user.mention} added to whitelist!")
    print(f"Added {user} to whitelist")

@bot.command()
@commands.is_owner()
async def whitelist_remove(ctx, user: discord.Member):
    """Remove user from whitelist"""
    await sx.whitelist.remove(ctx.guild.id, user.id)
    await ctx.send(f"❌ {user.mention} removed from whitelist")
    print(f"Removed {user} from whitelist")

@bot.command()
@commands.is_owner()
async def whitelist_check(ctx, user: discord.Member):
    """Check if user is whitelisted"""
    is_whitelisted = await sx.whitelist.is_whitelisted(ctx.guild.id, user.id)
    
    if is_whitelisted:
        await ctx.send(f"✅ {user.mention} is whitelisted")
    else:
        await ctx.send(f"❌ {user.mention} is NOT whitelisted")

@bot.command()
@commands.is_owner()
async def whitelist_list(ctx):
    """Show all whitelisted users"""
    whitelisted = await sx.whitelist.get_whitelisted_users(ctx.guild.id)
    
    if not whitelisted:
        await ctx.send("No whitelisted users")
        return
    
    embed = discord.Embed(
        title="📋 Whitelisted Users",
        color=discord.Color.green()
    )
    
    users_text = []
    for user_id in whitelisted:
        user = ctx.guild.get_member(user_id)
        if user:
            users_text.append(f"• {user.mention} ({user})")
        else:
            users_text.append(f"• User ID: {user_id}")
    
    embed.description = "\n".join(users_text)
    await ctx.send(embed=embed)

@bot.command()
async def whitelist_info(ctx):
    """Show whitelist information"""
    embed = discord.Embed(
        title="🔐 Whitelist System",
        description="Controls who can make server changes",
        color=discord.Color.gold()
    )
    embed.add_field(
        name="Automatically Whitelisted",
        value="• Server owner\n• Bot itself",
        inline=False
    )
    embed.add_field(
        name="Whitelisted Users Can",
        value="• Create/delete channels\n• Create/delete roles\n• Modify permissions\n• Add bots\n• Ban/kick members",
        inline=False
    )
    embed.add_field(
        name="Non-Whitelisted Users",
        value="Actions are blocked and reverted",
        inline=False
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
