"""
Channel protection handler for SecureX SDK.
"""
import discord
import asyncio
from datetime import datetime, timedelta


class ChannelHandler:
    """Handles channel protection logic"""
    
    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = sdk.bot
        self.backup_manager = sdk.backup_manager
        self.whitelist = sdk.whitelist
    
    async def _is_authorized(self, guild: discord.Guild, user_id: int) -> bool:
        """Check if user is authorized (owner or whitelisted)"""
        if guild.owner_id == user_id:
            return True
        if user_id == self.bot.user.id:
            return True
        return await self.whitelist.is_whitelisted(guild.id, user_id)
    
 
    async def on_channel_delete(self, channel: discord.abc.GuildChannel):
        """Restore unauthorized channel deletions"""
        try:
            guild = channel.guild
            print(f"🔍 [Debug] Channel deleted: {channel.name} ({channel.id})")
            await asyncio.sleep(1)
            
            
            from datetime import timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=30)
            
            found_entry = False
            async for entry in guild.audit_logs(limit=50, action=discord.AuditLogAction.channel_delete):
                if entry.created_at < cutoff_time:
                    break
                    
                if entry.target.id == channel.id:
                    found_entry = True
                    authorized = await self._is_authorized(guild, entry.user.id)
                    print(f"👤 [Debug] Executor: {entry.user.name} ({entry.user.id}) | Authorized: {authorized}")
                    
                    if not authorized:
                        print(f"🛠️ [Debug] Unauthorized deletion detected. Triggering restoration...")
                        
                        new_channel = await self.backup_manager.restore_channel(guild, channel)
                        if new_channel:
                            print(f"🔄 Restored unauthorized channel deletion: {channel.name}")
                        
                        
                        if new_channel and isinstance(channel, discord.CategoryChannel):
                            await self.backup_manager.restore_category_children(
                                guild, 
                                channel.id,
                                new_channel  
                            )
                    else:
                        print(f"✅ [Debug] Deletion by authorized user. Skipping restoration.")
                    break
            
            if not found_entry:
                print(f"⚠️ [Debug] Could not find audit log entry for channel deletion of {channel.name}")
                        
        except Exception as e:
            print(f"❌ [Debug] Error in on_channel_delete: {e}")
    
    async def on_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        """Restore unauthorized channel permission changes"""
        try:
            
            if (before.overwrites == after.overwrites and 
                before.position == after.position):
                return
            
            guild = after.guild
            await asyncio.sleep(0.5)
            
            
            from datetime import timezone
            cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=30)
            
            async for entry in guild.audit_logs(limit=50, oldest_first=False):
                if entry.created_at < cutoff_time:
                    break
                    
                if entry.action == discord.AuditLogAction.channel_update:
                    if entry.target and entry.target.id == after.id:
                        if not await self._is_authorized(guild, entry.user.id):
                            await self.backup_manager.restore_channel_permissions(guild, after.id)
                        break
        except Exception:
            pass
