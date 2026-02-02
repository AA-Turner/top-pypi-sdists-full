"""
Example: Backup Management
Shows how to create and manage server backups.
"""
import discord
from discord.ext import commands
from securex import SecureX

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
sx = SecureX(bot)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
    # Enable with automatic backups
    await sx.enable(
        whitelist=[bot.owner_id],
        auto_backup=True  # Creates backups automatically
    )
    
    print("💾 Backup system active!")

@sx.on_backup_completed
async def on_backup(backup_info):
    """Called when backup completes"""
    print(f"💾 Backup completed for guild {backup_info.guild_id}")
    print(f"   Channels: {backup_info.channel_count}")
    print(f"   Roles: {backup_info.role_count}")
    print(f"   Path: {backup_info.backup_path}")

@bot.command()
@commands.has_permissions(administrator=True)
async def backup_create(ctx):
    """Force create a backup right now"""
    msg = await ctx.send("💾 Creating backup...")
    
    backup_info = await sx.create_backup(ctx.guild.id)
    
    embed = discord.Embed(
        title="✅ Backup Created",
        color=discord.Color.green()
    )
    embed.add_field(name="Channels", value=backup_info.channel_count, inline=True)
    embed.add_field(name="Roles", value=backup_info.role_count, inline=True)
    embed.add_field(name="Timestamp", value=backup_info.timestamp.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    
    await msg.edit(content=None, embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def backup_info(ctx):
    """Show backup system information"""
    import json
    from pathlib import Path
    
    backup_dir = sx.backup_dir
    
    # Count backup files
    channel_backups = list(backup_dir.glob(f"channels_{ctx.guild.id}.json"))
    role_backups = list(backup_dir.glob(f"roles_{ctx.guild.id}.json"))
    
    embed = discord.Embed(
        title="💾 Backup System",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Backup Location",
        value=f"`{backup_dir}`",
        inline=False
    )
    
    if channel_backups:
        with open(channel_backups[0]) as f:
            data = json.load(f)
            timestamp = data.get("timestamp", "Unknown")
            channel_count = len(data.get("channels", []))
        
        embed.add_field(
            name="Channel Backup",
            value=f"✅ {channel_count} channels\nLast: {timestamp[:19]}",
            inline=True
        )
    else:
        embed.add_field(name="Channel Backup", value="❌ No backup", inline=True)
    
    if role_backups:
        with open(role_backups[0]) as f:
            data = json.load(f)
            timestamp = data.get("timestamp", "Unknown")
            role_count = len(data.get("roles", []))
        
        embed.add_field(
            name="Role Backup",
            value=f"✅ {role_count} roles\nLast: {timestamp[:19]}",
            inline=True
        )
    else:
        embed.add_field(name="Role Backup", value="❌ No backup", inline=True)
    
    embed.add_field(
        name="What's Backed Up",
        value="• Channel names, positions, permissions\n• Role names, positions, permissions\n• Category structure",
        inline=False
    )
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run("YOUR_TOKEN")
