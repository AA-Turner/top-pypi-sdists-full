"""
Punishment executor for anti-nuke violations.
Handles kick, ban, timeout, and warn actions.
"""
import discord
from datetime import timedelta
from typing import Optional


class PunishmentExecutor:
    """Executes punishment actions on violators"""
    
    def __init__(self, bot):
        """Initialize with bot instance"""
        self.bot = bot
    
    async def punish(
        self, 
        guild: discord.Guild, 
        user: discord.User,
        violation_type: str,
        details: str = None,
        sdk = None
    ) -> str:
        """
        Execute punishment on violator based on violation type.
        
        Args:
            guild: The guild where violation occurred
            user: The user who committed the violation
            violation_type: Type of violation (e.g., "channel_delete")
            details: Optional details about the violation
            sdk: SDK instance for accessing punishment config
            
        Returns:
            The punishment action that was applied ("none", "warn", "timeout", "kick", "ban")
        """
        if sdk is None:
            return "none"
            
        
        action = await sdk.get_punishment(guild.id, violation_type)
        
        if action == "none":
            return action
        
        member = guild.get_member(user.id)
        if not member:
            print(f"Cannot punish {user}: not a member")
            return action
        
        
        if member.id == guild.owner_id:
            print(f"Cannot punish server owner {user}")
            return action
        
        
        
        try:
            if action == "warn":
                
                print(f"⚠️ Warned {user} for {violation_type}")
                
            elif action == "timeout":
                duration = timedelta(seconds=sdk.timeout_duration)
                await member.timeout(duration, reason=f"SecureX: {violation_type}")
                print(f"⏱️ Timed out {user} for {sdk.timeout_duration}s ({violation_type})")
                
            elif action == "kick":
                await member.kick(reason=f"SecureX: {violation_type}")
                print(f"👢 Kicked {user} for {violation_type}")
                
            elif action == "ban":
                await member.ban(reason=f"SecureX: {violation_type}", delete_message_days=0)
                print(f"🔨 Banned {user} for {violation_type}")
            
            if sdk.notify_punished_user:
                await self._notify_user(member, violation_type, action, details, sdk)
        
                
        except discord.Forbidden:
            print(f"❌ Missing permissions to {action} {user}")
        except Exception as e:
            print(f"Error punishing {user}: {e}")
        
        return action
    
    async def _notify_user(
        self, 
        member: discord.Member, 
        violation_type: str, 
        action: str, 
        details: Optional[str],
        sdk
    ):
        """Send DM notification to punished user"""
        try:
            
            readable_type = violation_type.replace("_", " ").title()
            
            embed = discord.Embed(
                title="🚨 Anti-Nuke Violation Detected",
                description=f"You triggered anti-nuke protection in **{member.guild.name}**",
                color=discord.Color.red()
            )
            embed.add_field(name="Violation Type", value=readable_type, inline=False)
            if details:
                embed.add_field(name="Details", value=details, inline=False)
            embed.add_field(
                name="Action Taken", 
                value=f"**{action.title()}**", 
                inline=False
            )
            
            if action == "timeout":
                mins = sdk.timeout_duration // 60
                embed.add_field(name="Duration", value=f"{mins} minutes", inline=False)
            
            await member.send(embed=embed)
            print(f"📨 Sent punishment notification to {member}")
        except discord.Forbidden:
            print(f"Cannot DM {member} (DMs disabled)")
        except Exception as e:
            print(f"Error notifying {member}: {e}")
