"""
Role protection handler for SecureX SDK.
"""
import discord
import asyncio
from datetime import datetime, timedelta


class RoleHandler:
    """Handles role protection logic"""
    
    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = sdk.bot
        self.backup_manager = sdk.backup_manager
        self.whitelist = sdk.whitelist
    
    async def _is_authorized(self, guild: discord.Guild, user_id: int) -> bool:
        """Check if user is authorized"""
        if guild.owner_id == user_id:
            return True
        if user_id == self.bot.user.id:
            return True
        return await self.whitelist.is_whitelisted(guild.id, user_id)
    
    async def on_role_delete(self, role: discord.Role):
        """Restore unauthorized role deletions"""
        try:
            guild = role.guild
            await asyncio.sleep(1)
            
            
            from datetime import timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=30)
            
            async for entry in guild.audit_logs(limit=50, action=discord.AuditLogAction.role_delete):
                if entry.created_at < cutoff_time:
                    break
                    
                if entry.target.id == role.id:
                    if not await self._is_authorized(guild, entry.user.id):
                        if await self.backup_manager.restore_role(guild, role.id):
                            print(f"🔄 Restored unauthorized role deletion: {role.name}")
                    break
        except Exception:
            pass
    
    async def on_role_update(self, before: discord.Role, after: discord.Role):
        """Restore unauthorized role permission changes"""
        try:
            
            if before.position == after.position and before.permissions == after.permissions:
                return
            
            guild = after.guild
            await asyncio.sleep(0.3)
            
            
            from datetime import timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=30)
            
            async for entry in guild.audit_logs(limit=50, oldest_first=False):
                if entry.created_at < cutoff_time:
                    break
                    
                if entry.action == discord.AuditLogAction.role_update:
                    if entry.target.id == after.id:
                        if not await self._is_authorized(guild, entry.user.id):
                            if await self.backup_manager.restore_role_permissions(guild, after.id):
                                print(f"🔄 Restored unauthorized role update: {after.name}")
                        break
        except Exception:
            pass
