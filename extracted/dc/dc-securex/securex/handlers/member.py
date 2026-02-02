"""
Member protection handler (bot/ban/kick protection).
"""
import discord
import asyncio


class MemberHandler:
    """Handles member-related protection"""
    
    
    DANGEROUS_PERMISSIONS = frozenset([
        'administrator',
        'kick_members',
        'ban_members',
        'manage_guild',
        'manage_roles',
        'manage_channels',
        'manage_webhooks',
        'manage_emojis',
        'mention_everyone',
        'manage_expressions'
    ])
    
    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = sdk.bot
        self.whitelist = sdk.whitelist
    
    async def _is_authorized(self, guild: discord.Guild, user_id: int) -> bool:
        """Check if user is authorized"""
        if guild.owner_id == user_id:
            return True
        if user_id == self.bot.user.id:
            return True
        return await self.whitelist.is_whitelisted(guild.id, user_id)
    
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        """Restore banned victims (punishment handled by action worker)"""
        try:
            await asyncio.sleep(0.5)
            
            
            from datetime import datetime, timezone, timedelta
            cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=30)
            
            async for entry in guild.audit_logs(limit=50, action=discord.AuditLogAction.ban):
                if entry.created_at < cutoff_time:
                    break
                    
                if entry.target.id == user.id:
                    if not await self._is_authorized(guild, entry.user.id):
                        
                        try:
                            await guild.unban(user, reason="SecureX: Restoring banned member")
                            print(f"🔄 Unbanned unauthorized member ban: {user.name}")
                        except (discord.errors.Forbidden, discord.errors.HTTPException):
                            pass
                    break
        except Exception as e:
            print(f"Error in on_member_ban: {e}")

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Check for dangerous permissions and remove unauthorized roles"""
        try:
            
            if before.roles == after.roles:
                return
            
            guild = after.guild
            await asyncio.sleep(0.5)
            
            
            from datetime import datetime, timezone, timedelta
            cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=30)
            
            async for entry in guild.audit_logs(limit=50, action=discord.AuditLogAction.member_role_update):
                if entry.created_at < cutoff_time:
                    break
                if entry.target.id == after.id:
                    
                    is_authorized = await self._is_authorized(guild, entry.user.id)
                    
                    if not is_authorized:
                        
                        dangerous_roles = []
                        
                        for role in after.roles:
                            if role.is_default():  
                                continue
                            
                            
                            permissions = role.permissions
                            for perm_name in self.DANGEROUS_PERMISSIONS:
                                if getattr(permissions, perm_name, False):
                                    dangerous_roles.append(role)
                                    break  
                        
                        
                        if dangerous_roles:
                            try:
                                await after.remove_roles(*dangerous_roles, reason="SecureX: Removed dangerous roles (unauthorized update)")
                                role_names = ", ".join([r.name for r in dangerous_roles])
                                print(f"🛡️ Bulk removed {len(dangerous_roles)} dangerous role(s) from {after.name}: {role_names}")
                            except (discord.errors.Forbidden, discord.errors.HTTPException) as e:
                                print(f"⚠️ Failed to remove roles: {e}")
                    
                    break
        except Exception as e:
            print(f"Error in on_member_update: {e}")
