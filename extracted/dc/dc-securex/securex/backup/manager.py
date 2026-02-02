"""
Complete backup and restoration manager.
Extracted from cogs/antinuke.py backup logic.
"""
import discord
import json
import asyncio
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Union
from ..models import BackupInfo, RestoreResult


class BackupManager:
    """Manages server backups and restoration"""
    
    def __init__(self, sdk, storage):
        self.sdk = sdk
        self.bot = sdk.bot
        self.storage = storage  # Storage backend (JSON or PostgreSQL)
        self.backup_dir = sdk.backup_dir  # Still used for legacy compatibility
        
        # In-memory caches for fast access
        self._channel_cache: Dict[int, Dict] = {}  
        self._role_cache: Dict[int, Dict] = {}
        self._guild_cache: Dict[int, Dict] = {}
        self._cache_loaded = False
        self._refresh_task = None
        self._guild_locks: Dict[int, asyncio.Lock] = {}

    def _get_guild_lock(self, guild_id: int) -> asyncio.Lock:
        """Get or create an async lock for a specific guild"""
        if guild_id not in self._guild_locks:
            self._guild_locks[guild_id] = asyncio.Lock()
        return self._guild_locks[guild_id]
    
    async def create_backup(self, guild_id: int) -> BackupInfo:
        """Create complete backup for a guild"""
        try:
            guild = self.bot.get_guild(guild_id)
            if not guild:
                return BackupInfo(
                    guild_id=guild_id,
                    timestamp=datetime.now(timezone.utc),
                    channel_count=0,
                    role_count=0,
                    backup_path="",
                    success=False
                )
            
            
            channel_count = await self._backup_channels(guild)
            
            
            role_count = await self._backup_roles(guild)
            
            
            await self._backup_guild_settings(guild)
            
            backup_info = BackupInfo(
                guild_id=guild_id,
                timestamp=datetime.now(timezone.utc),
                channel_count=channel_count,
                role_count=role_count,
                backup_path=str(self.backup_dir),
                success=True
            )
            
            
            await self._update_guild_cache(guild_id)
            
            
            await self.sdk._trigger_callbacks('backup_completed', backup_info)
            
            return backup_info
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return BackupInfo(
                guild_id=guild_id,
                timestamp=datetime.now(timezone.utc),
                channel_count=0,
                role_count=0,
                backup_path="",
                success=False
            )
    
    async def _backup_channels(self, guild: discord.Guild) -> int:
        """Backup all channels using storage backend"""
        backup_data = {
            "guild_id": guild.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "channels": []
        }
        
        for channel in guild.channels:
            channel_data = {
                "id": channel.id,
                "name": channel.name,
                "type": str(channel.type),
                "position": channel.position,
                "category_id": channel.category.id if channel.category else None,
                "permissions": {}
            }
            
            # Backup permissions
            for target, overwrite in channel.overwrites.items():
                target_id = str(target.id)
                channel_data["permissions"][target_id] = {
                    "type": "role" if isinstance(target, discord.Role) else "member",
                    "allow": overwrite.pair()[0].value,
                    "deny": overwrite.pair()[1].value
                }
            
            # Type-specific backup data
            if channel.type == discord.ChannelType.text:
                channel_data["text_properties"] = {
                    "topic": getattr(channel, 'topic', None),
                    "slowmode_delay": getattr(channel, 'slowmode_delay', 0),
                    "nsfw": getattr(channel, 'nsfw', False)
                }
            elif channel.type == discord.ChannelType.voice:
                channel_data["voice_properties"] = {
                    "bitrate": getattr(channel, 'bitrate', 64000),
                    "user_limit": getattr(channel, 'user_limit', 0)
                }
            elif channel.type == discord.ChannelType.stage_voice:
                channel_data["stage_properties"] = {
                    "bitrate": getattr(channel, 'bitrate', 64000)
                }
            
            backup_data["channels"].append(channel_data)
        
        # Save to storage backend (SQLite/PostgreSQL)
        await self.storage.save_channel_backup(guild.id, backup_data)
        
        # Update cache
        self._channel_cache[guild.id] = backup_data
        
        return len(backup_data["channels"])
    
    async def _backup_roles(self, guild: discord.Guild) -> int:
        """Backup all roles using storage backend"""
        backup_data = {
            "guild_id": guild.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "roles": []
        }
        
        # Backup all non-default roles
        for role in guild.roles:
            if role.is_default():  
                continue
            
            role_data = {
                "id": role.id,
                "name": role.name,
                "permissions": role.permissions.value,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
                "position": role.position
            }
            
            backup_data["roles"].append(role_data)
        
        # Save to storage backend (SQLite/PostgreSQL)
        await self.storage.save_role_backup(guild.id, backup_data)
        
        # Update cache
        self._role_cache[guild.id] = backup_data
        
        return len(backup_data["roles"])
    
    async def restore_category_children(self, guild: discord.Guild, old_category_id: int, new_category: discord.CategoryChannel):
        """
        Restore all child channels that belonged to a category.
        Called after a category is restored to recreate its children.
        """
        try:
            # Load from storage instead of file
            backup = await self.storage.load_channel_backup(guild.id)
            if not backup:
                print(f"No channel backup found for guild {guild.id}")
                return
            
            # Find children of the old category
            child_channels = [
                ch for ch in backup["channels"]
                if ch.get("category_id") == old_category_id
            ]
            
            if not child_channels:
                print(f"No child channels found for category {new_category.name} (old ID: {old_category_id})")
                return
            
            
            child_channels = sorted(child_channels, key=lambda x: x.get("position", 0))
            
            print(f"Restoring {len(child_channels)} child channels for category: {new_category.name}")
            print(f"   Creating in sorted order (positions: {[ch.get('position') for ch in child_channels]})")
            
            
            for ch_data in child_channels:
                try:
                    
                    existing = guild.get_channel(ch_data["id"])
                    if existing:
                        
                        if existing.category != new_category:
                            
                            await existing.edit(category=new_category, reason="SecureX: Move orphaned channel to restored category")
                            print(f"✅ Moved existing channel to category: {existing.name}")
                        else:
                            print(f"Channel {ch_data['name']} already in correct category, skipping")
                        continue
                    
                    
                    channel_type_str = ch_data["type"]
                    
                    
                    overwrites = {}
                    for target_id, perm_data in ch_data.get("permissions", {}).items():
                        try:
                            target_id = int(target_id)
                            if perm_data["type"] == "role":
                                target = guild.get_role(target_id)
                            else:
                                target = guild.get_member(target_id)
                            
                            if target:
                                overwrites[target] = discord.PermissionOverwrite.from_pair(
                                    discord.Permissions(perm_data["allow"]),
                                    discord.Permissions(perm_data["deny"])
                                )
                        except Exception as e:
                            print(f"Error preparing permissions for {target_id}: {e}")
                    
                    
                    new_channel = None
                    
                    if "text" in channel_type_str.lower():
                        
                        props = ch_data.get("text_properties", {})
                        new_channel = await guild.create_text_channel(
                            name=ch_data["name"],
                            category=new_category,
                            topic=props.get("topic"),
                            slowmode_delay=props.get("slowmode_delay", 0),
                            nsfw=props.get("nsfw", False),
                            overwrites=overwrites,
                            reason="SecureX: Restore category child"
                        )
                    
                    elif "voice" in channel_type_str.lower():
                        
                        props = ch_data.get("voice_properties", {})
                        new_channel = await guild.create_voice_channel(
                            name=ch_data["name"],
                            category=new_category,
                            bitrate=props.get("bitrate", 64000),
                            user_limit=props.get("user_limit", 0),
                            overwrites=overwrites,
                            reason="SecureX: Restore category child"
                        )
                    
                    elif "stage" in channel_type_str.lower():
                        
                        props = ch_data.get("stage_properties", {})
                        new_channel = await guild.create_stage_channel(
                            name=ch_data["name"],
                            category=new_category,
                            overwrites=overwrites,
                            reason="SecureX: Restore category child"
                        )
                    
                    if new_channel:
                        print(f"✅ Restored child channel: {new_channel.name} (auto-position: {new_channel.position})")
                    
                    
                    await asyncio.sleep(0.3)
                    
                except Exception as e:
                    print(f"Error restoring child channel {ch_data.get('name')}: {e}")
            
            
            
            print(f"📝 Updating backup with new category ID: {old_category_id} → {new_category.id}")
            
            
            for ch_data in backup["channels"]:
                if ch_data.get("category_id") == old_category_id:
                    
                    ch_data["category_id"] = new_category.id
                    
                    
                    existing = guild.get_channel(ch_data["id"])
                    if existing and existing.category == new_category:
                        
                        ch_data["id"] = existing.id
            
            
            with open(backup_file, 'w') as f:
                json.dump(backup, f, indent=2)
            
            
            if guild.id in self._channel_cache:
                self._channel_cache[guild.id] = backup
            
            print(f"✅ Backup updated - child channels now reference category {new_category.id}")
            print(f"✅ Finished restoring children for category: {new_category.name}")
            
        except Exception as e:
            print(f"Error in restore_category_children: {e}")
 
    def start_auto_backup(self, interval_minutes: int = 30):
        """Start automatic backup task"""
        async def auto_backup_task():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                try:
                    
                    for guild in self.bot.guilds:
                        await self.create_backup(guild.id)
                    
                    
                    await asyncio.sleep(interval_minutes * 60)
                except Exception as e:
                    print(f"Error in auto backup: {e}")
                    await asyncio.sleep(60)  
        
        
        self.bot.loop.create_task(auto_backup_task())

    

    async def restore_channel(self, guild: discord.Guild, channel: discord.abc.GuildChannel) -> Optional[discord.abc.GuildChannel]:
        """Restore a deleted channel from backup"""
        try:
            print(f"🛠️ [Debug] Attempting to restore channel: {channel.name} ({channel.id})")
            
            # Load from cache or storage backend
            backup = self._channel_cache.get(guild.id)
            if not backup:
                print(f"📂 [Debug] Cache miss for guild {guild.id}. Loading from storage...")
                backup = await self.storage.load_channel_backup(guild.id)
                if not backup:
                    print(f"❌ [Debug] No backup found in storage")
                    return None
                self._channel_cache[guild.id] = backup  
            
            
            ch_data = None
            channel_index = None
            for i, data in enumerate(backup["channels"]):
                if data["id"] == channel.id:
                    ch_data = data
                    channel_index = i
                    break
            
            if not ch_data:
                print(f"❌ [Debug] Channel ID {channel.id} not found in backup data.")
                return None
            
            print(f"📦 [Debug] Found channel data in backup. Type: {ch_data['type']}")
            
            
            category = None
            if ch_data.get("category_id"):
                category = guild.get_channel(ch_data["category_id"])
            
            
            new_channel = None
            channel_type = ch_data["type"]
            
            if "text" in channel_type.lower():
                text_props = ch_data.get("text_properties", {})
                new_channel = await guild.create_text_channel(
                    name=ch_data["name"],
                    category=category,
                    topic=text_props.get("topic"),
                    slowmode_delay=text_props.get("slowmode_delay", 0),
                    nsfw=text_props.get("nsfw", False),
                    reason="SecureX: Restoring deleted channel"
                )
            elif "voice" in channel_type.lower():
                voice_props = ch_data.get("voice_properties", {})
                new_channel = await guild.create_voice_channel(
                    name=ch_data["name"],
                    category=category,
                    bitrate=voice_props.get("bitrate", 64000),
                    user_limit=voice_props.get("user_limit", 0),
                    reason="SecureX: Restoring deleted channel"
                )
            elif "category" in channel_type.lower():
                new_channel = await guild.create_category(
                    name=ch_data["name"],
                    reason="SecureX: Restoring deleted category"
                )
            elif "stage" in channel_type.lower():
                stage_props = ch_data.get("stage_properties", {})
                new_channel = await guild.create_stage_channel(
                    name=ch_data["name"],
                    category=category,
                    bitrate=stage_props.get("bitrate", 64000),
                    reason="SecureX: Restoring deleted channel"
                )
            
            if not new_channel:
                return None
            
            
            target_position = ch_data.get("order_index", ch_data["position"])
            
            
            try:
                await new_channel.edit(position=target_position)
                print(f"✅ Restored channel: {new_channel.name} ({channel_type}) at order_index {target_position}")
            except discord.Forbidden:
                print(f"⚠️ Cannot set position for {new_channel.name}")
            except Exception as e:
                print(f"⚠️ Failed to set position for {new_channel.name}: {e}")
            
            
            if ch_data.get("permissions"):
                for target_id, perm_data in ch_data["permissions"].items():
                    try:
                        target_id = int(target_id)
                        target = guild.get_role(target_id) if perm_data["type"] == "role" else guild.get_member(target_id)
                        
                        if target:
                            overwrite = discord.PermissionOverwrite.from_pair(
                                discord.Permissions(perm_data["allow"]),
                                discord.Permissions(perm_data["deny"])
                            )
                            await new_channel.set_permissions(target, overwrite=overwrite)
                    except Exception as e:
                        print(f"Error restoring permission: {e}")
            
            
            if guild.id in self._channel_cache and channel_index is not None:
                self._channel_cache[guild.id]["channels"][channel_index]["id"] = new_channel.id
                
                
                # Save updated backup to storage
                await self.storage.save_channel_backup(guild.id, self._channel_cache[guild.id])
            
            return new_channel
            
        except Exception as e:
            print(f"Error restoring channel: {e}")
            return None
    
    async def restore_channel_permissions(self, guild: discord.Guild, channel_id: int) -> bool:
        """Restore channel permissions from backup"""
        try:
            # Load from storage instead of file
            backup = await self.storage.load_channel_backup(guild.id)
            if not backup:
                return False
            
            # Find channel in backup
            ch_data = None
            for data in backup["channels"]:
                if data["id"] == channel_id:
                    ch_data = data
                    break
            
            if not ch_data:
                return False
            
            channel = guild.get_channel(channel_id)
            if not channel:
                return False
            
            
            if ch_data.get("permissions"):
                for target_id, perm_data in ch_data["permissions"].items():
                    try:
                        target_id = int(target_id)
                        target = guild.get_role(target_id) if perm_data["type"] == "role" else guild.get_member(target_id)
                        
                        if target:
                            overwrite = discord.PermissionOverwrite.from_pair(
                                discord.Permissions(perm_data["allow"]),
                                discord.Permissions(perm_data["deny"])
                            )
                            await channel.set_permissions(target, overwrite=overwrite)
                    except Exception:
                        pass
            
            return True
            
        except Exception as e:
            print(f"Error restoring channel permissions: {e}")
            return False
    
    async def restore_role(self, guild: discord.Guild, role_id: int) -> bool:
        """Restore a deleted role from backup"""
        try:
            # Load from cache or storage backend
            backup = self._role_cache.get(guild.id)
            if not backup:
                backup = await self.storage.load_role_backup(guild.id)
                if not backup:
                    return False
                self._role_cache[guild.id] = backup  
            
            
            target_role_data = None
            role_index = None
            for i, role_data in enumerate(backup["roles"]):
                if role_data["id"] == role_id:
                    target_role_data = role_data
                    role_index = i
                    break
            
            if not target_role_data:
                return False
                
            
            new_role = await guild.create_role(
                name=target_role_data["name"],
                permissions=discord.Permissions(target_role_data["permissions"]),
                color=discord.Color(target_role_data["color"]),
                hoist=target_role_data["hoist"],
                mentionable=target_role_data["mentionable"],
                reason="SecureX: Restoring deleted role"
            )
            
            
            try:
                await guild.edit_role_positions(positions={new_role: target_role_data["position"]})
                print(f"✅ Restored role: {new_role.name} at position {target_role_data['position']}")
            except discord.Forbidden:
                print(f"⚠️ Cannot set position for {new_role.name} - bot hierarchy too low")
            except Exception as e:
                print(f"⚠️ Failed to set position for {new_role.name}: {e}")
            
            
            if guild.id in self._role_cache and role_index is not None:
                # Update ID in cache
                self._role_cache[guild.id]["roles"][role_index]["id"] = new_role.id
                
                # Save updated backup to storage
                await self.storage.save_role_backup(guild.id, self._role_cache[guild.id])
            
            return True
        except Exception as e:
            print(f"Error restoring role: {e}")
            return False
    
    async def restore_role_permissions(self, guild: discord.Guild, role_id: int) -> bool:
        """Restore role permissions from backup"""
        try:
            # Load from storage instead of file
            backup = await self.storage.load_role_backup(guild.id)
            if not backup:
                return False
            
            # Find role in backup
            for role_data in backup["roles"]:
                if role_data["id"] == role_id:
                    role = guild.get_role(role_id)
                    if not role:
                        return False
                    
                    # Restore only permissions, NOT position
                    # (setting position via edit() causes Discord to move role to bottom)
                    await role.edit(
                        permissions=discord.Permissions(role_data["permissions"]),
                        reason="SecureX: Restoring role permissions"
                    )
                    
                    return True
            
            return False
        except Exception as e:
            print(f"Error restoring role permissions: {e}")
            return False
    
  


    
    
    async def preload_all(self):
        """
        Preload ALL backups into memory on startup.
        Call this in enable() to warm the cache.
        """
        if self._cache_loaded:
            return
        
        print("🔄 Preloading backups into cache...")
        channel_count = 0
        role_count = 0
        
        
    async def preload_all(self):
        """Preload all backups from storage into cache"""
        if self._cache_loaded:
            return
            
        try:
            # 1. Load generic guild settings
            all_settings = await self.storage.load_all_guild_settings()
            if all_settings:
                # Convert back to int keys if needed, though load_all_guild_settings should handle it
                self._guild_cache = all_settings
            
            # 2. We can't efficiently preload ALL channel/role backups without a specific API
            # For now, we'll mark as loaded and verify individual guilds on demand.
            # This is much more efficient than scanning files anyway.
            
            self._cache_loaded = True
            
        except Exception as e:
            print(f"Error preloading backups: {e}")
    
    async def _update_guild_cache(self, guild_id: int):
        """Update cache for a specific guild after backup"""
        try:
            # Load from storage
            channel_backup = await self.storage.load_channel_backup(guild_id)
            if channel_backup:
                self._channel_cache[guild_id] = channel_backup
            
            role_backup = await self.storage.load_role_backup(guild_id)
            if role_backup:
                self._role_cache[guild_id] = role_backup
                
        except Exception as e:
            print(f"Error updating cache for guild {guild_id}: {e}")
    
        """Start background task to refresh cache every 10 minutes"""
        if self._refresh_task is None:
            self._refresh_task = asyncio.create_task(self._auto_refresh_loop())
            print("🔄 Started backup cache auto-refresh (every 10 minutes)")
    
    async def _auto_refresh_loop(self):
        """Background task: refresh cache every 10 minutes"""
        while True:
            try:
                await asyncio.sleep(600)  
                
                print("🔄 Refreshing backup cache...")
                
                
                for guild in self.bot.guilds:
                    await self._update_guild_cache(guild.id)
                    
                    # Also refresh guild settings (vanity, name, etc.)
                    await self._backup_guild_settings(guild)
                    
                    await asyncio.sleep(0.1)  
                
                print("✅ Backup cache refreshed")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in auto-refresh loop: {e}")
    
    def start_auto_refresh(self):
        """Start background cache refresh task"""
        if self._refresh_task is None or self._refresh_task.done():
            self._refresh_task = asyncio.create_task(self._auto_refresh_loop())
    
    
    
    async def _backup_guild_settings(self, guild: discord.Guild) -> Dict:
        """Backup guild settings using storage backend"""
        try:
            backup_data = {
                "guild_id": guild.id,
                "vanity_url_code": guild.vanity_url_code,
                "name": guild.name,
                "icon": str(guild.icon) if guild.icon else None,
                "banner": str(guild.banner) if guild.banner else None,
                "description": guild.description,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Save to storage backend (SQLite/PostgreSQL)
            await self.storage.save_guild_settings(guild.id, backup_data)
            
            # Update cache
            self._guild_cache[guild.id] = backup_data
            
            return backup_data
            
        except Exception as e:
            print(f"Error backing up guild settings: {e}")
            return {}
    
    async def _save_all_guild_settings(self):
        """Save all guild settings - DEPRECATED"""
        pass
    
    async def _load_all_guild_settings(self):
        """Load all guild settings from storage"""
        try:
            settings = await self.storage.load_all_guild_settings()
            if settings:
                self._guild_cache = settings
                print(f"✅ Loaded guild settings for {len(self._guild_cache)} server(s)")
        except Exception as e:
            print(f"Error loading guild settings: {e}")
    
    async def update_guild_vanity(self, guild_id: int, vanity_code: str):
        """Update vanity URL in backup and cache (for authorized changes)"""
        try:
            if guild_id in self._guild_cache:
                self._guild_cache[guild_id]["vanity_url_code"] = vanity_code
                self._guild_cache[guild_id]["timestamp"] = datetime.now(timezone.utc).isoformat()
            else:
                self._guild_cache[guild_id] = {
                    "guild_id": guild_id,
                    "vanity_url_code": vanity_code,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            await self._save_all_guild_settings()
            print(f"✅ Updated vanity backup: discord.gg/{vanity_code}")
            
        except Exception as e:
            print(f"Error updating guild vanity: {e}")
    
    async def get_guild_vanity(self, guild_id: int) -> Optional[str]:
        """Get backed up vanity URL from storage"""
        settings = await self.get_guild_settings(guild_id)
        return settings.get("vanity_url_code") if settings else None
    
    async def get_guild_settings(self, guild_id: int) -> Optional[Dict]:
        """Get backed up guild settings"""
        try:
            if guild_id in self._guild_cache:
                return self._guild_cache[guild_id]
            
            await self._load_all_guild_settings()
            
            if guild_id in self._guild_cache:
                return self._guild_cache[guild_id]
            
            return None
            
        except Exception as e:
            print(f"Error getting guild settings: {e}")
