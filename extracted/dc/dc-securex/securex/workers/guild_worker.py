"""
Guild Restoration Worker - Restores server name and vanity URL only
Triggered by GuildHandler when unauthorized changes are detected
Supports per-guild user tokens with file storage and memory caching
"""
import asyncio
import discord
import aiohttp
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class GuildWorker:
    """Background worker for guild settings restoration"""
    
    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = sdk.bot
        self._worker_task = None
        
        # Per-guild user tokens
        self._user_tokens: Dict[int, str] = {}  # guild_id -> user_token (cache)
        # self._tokens_file = sdk.backup_dir / "user_tokens.json"  # Removed in v3.2.7
    

    
    async def _save_tokens(self):
        """Save user tokens to storage"""
        try:
            # We don't need to save all at once anymore as we save individual tokens
            # But for legacy compatibility or bulk updates:
            for guild_id, token in self._user_tokens.items():
                await self.sdk.storage.save_user_token(int(guild_id), token)
        except Exception as e:
            print(f"Error saving user tokens: {e}")
    
    async def set_user_token(self, guild_id: int, token: str):
        """Set user token for a specific guild"""
        self._user_tokens[guild_id] = token
        
        # Save to storage
        try:
            await self.sdk.storage.save_user_token(guild_id, token)
            print(f"✅ User token set for guild {guild_id}")
        except Exception as e:
            print(f"Error saving token for guild {guild_id}: {e}")
            
    def get_user_token(self, guild_id: int) -> Optional[str]:
        """Get user token for a guild (from cache)"""
        return self._user_tokens.get(guild_id)
        
    async def load_token_from_storage(self, guild_id: int) -> Optional[str]:
        """Load token from storage for a specific guild (if not in cache)"""
        try:
            data = await self.sdk.storage.load_user_token(guild_id)
            if data and "token" in data:
                token = data["token"]
                self._user_tokens[guild_id] = token
                return token
        except Exception as e:
            print(f"Error loading token for guild {guild_id}: {e}")
        return None
    
    async def remove_user_token(self, guild_id: int):
        """Remove user token for a guild"""
        if guild_id in self._user_tokens:
            del self._user_tokens[guild_id]
            # Ideally we should remove from storage too, but BaseStorageBackend 
            # might not have a delete method for tokens yet.
            # For now we'll just overwrite with empty or handle as best effort.
            pass
        if guild_id in self._user_tokens:
            del self._user_tokens[guild_id]
            await self._save_tokens()
            print(f"❌ User token removed for guild {guild_id}")
    
    async def start(self):
        """Start the guild restoration worker"""
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._restoration_loop())
            print("⚡ Guild Restoration Worker started")
    
    async def stop(self):
        """Stop the worker"""
        if self._worker_task:
            self._worker_task.cancel()
            self._worker_task = None
    
    async def _restoration_loop(self):
        """Background loop for guild restoration"""
        while True:
            try:
                entry = await self.sdk.guild_queue.get()
                
                # Only process guild_update actions
                if entry.action != discord.AuditLogAction.guild_update:
                    continue
                
                # Extract changes from entry
                guild = entry.guild
                executor = entry.user
                
                # Skip if bot did it
                if executor.id == self.bot.user.id:
                    continue
                
                # Check authorization
                if executor.id == guild.owner_id:
                    continue
                
                whitelist_set = self.sdk.whitelist_cache.get(guild.id, set())
                if executor.id in whitelist_set:
                    continue
                
                # Unauthorized change - restore from backup
                print(f"🔍 Unauthorized guild update by {executor.name}")
                await self._restore_guild_settings(guild)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in guild restoration loop: {e}")
                import traceback
                traceback.print_exc()
    
    async def _restore_vanity_via_api(self, guild_id: int, vanity_code: str) -> bool:
        """Restore vanity URL using user token and Discord API"""
        user_token = self.get_user_token(guild_id)
        
        if not user_token:
            print(f"⚠️ No user token set for guild {guild_id}! Cannot restore vanity URL.")
            print(f"   Use: await sx.guild_worker.set_user_token({guild_id}, 'USER_TOKEN')")
            return False
        
        try:
            url = f"https://discord.com/api/v9/guilds/{guild_id}/vanity-url"
            headers = {
                "authorization": user_token,
                "content-type": "application/json"
            }
            payload = {"code": vanity_code}
            
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        return True
                    else:
                        error_text = await response.text()
                        print(f"⚠️ Failed to restore vanity: {response.status} - {error_text}")
                        return False
        except Exception as e:
            print(f"Error restoring vanity via API: {e}")
            return False
    
    async def _restore_guild_settings(self, guild):
        """Restore guild settings from backup (simple and reliable)"""
        try:
            print(f"🔧 Restoring guild: {guild.name}")
            start_time = datetime.now()
            
            # Get backup data
            backup_data = await self.sdk.backup_manager.get_guild_settings(guild.id)
            if not backup_data:
                print(f"⚠️ No backup found for guild {guild.name}")
                return
            
            restore_params = {}
            restored_items = []
            
            # Always restore to backup name
            if backup_data.get("name"):
                restore_params["name"] = backup_data["name"]
                restored_items.append(f"name ({backup_data['name']})")
            
            # Restore vanity URL if available
            if backup_data.get("vanity_url_code"):
                old_vanity = backup_data["vanity_url_code"]
                vanity_success = await self._restore_vanity_via_api(guild.id, old_vanity)
                if vanity_success:
                    restored_items.append(f"vanity (discord.gg/{old_vanity})")
            
            # Apply restoration
            if restore_params:
                await guild.edit(**restore_params, reason="SecureX: Restoring unauthorized changes")
            
            if restored_items:
                elapsed = (datetime.now() - start_time).total_seconds() * 1000
                print(f"⚡ Restored in {elapsed:.0f}ms: {', '.join(restored_items)}")
            
        except Exception as e:
            import traceback
            print(f"❌ Restoration error: {e}")
            traceback.print_exc()
