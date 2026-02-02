"""
Whitelist management for SecureX SDK.
Strictly per-guild - no cross-server whitelisting.
"""
import json
import aiofiles
from pathlib import Path
from typing import List, Set
from ..models import WhitelistChange


class WhitelistManager:
    """Manages whitelisted users per guild (guild-specific only)"""
    
    def __init__(self, sdk, storage):
        self.sdk = sdk
        self.storage = storage  # Storage backend (JSON or PostgreSQL)
        
        # In-memory cache for fast whitelist checks
        self._whitelists: dict[int, Set[int]] = {}
        self._cache_loaded = False
    
    async def preload_all(self):
        """
        Preload ALL whitelists into memory on startup.
        Call this in enable() to warm the cache.
        """
        if self._cache_loaded:
            return
        
        try:
            # Load all whitelists from storage backend
            self._whitelists = await self.storage.load_all_whitelists()
            self._cache_loaded = True
        except Exception as e:
            print(f"❌ Error preloading whitelists: {e}")
            # Ensure it's not marked as loaded if it failed
            self._cache_loaded = False
    
    async def _load_whitelist(self, guild_id: int):
        """Load whitelist from storage (fallback if not preloaded)"""
        users = await self.storage.get_whitelist_users(guild_id)
        self._whitelists[guild_id] = users
    
    async def _save_whitelist(self, guild_id: int):
        """Save whitelist via storage backend"""
        # Storage backend handles the actual save
        # Cache is already updated, so nothing to do here
        pass
    
    async def add(self, guild_id: int, user_id: int, moderator_id: int = None):
        """Add user to guild whitelist"""
        if guild_id not in self._whitelists:
            await self._load_whitelist(guild_id)
            if guild_id not in self._whitelists:
                self._whitelists[guild_id] = set()
        
        self._whitelists[guild_id].add(user_id)
        
        # Save to storage backend
        await self.storage.add_whitelist_user(guild_id, user_id)
        
        # Trigger callback
        change = WhitelistChange(
            guild_id=guild_id,
            user_id=user_id,
            action="added",
            moderator_id=moderator_id
        )
        await self.sdk._trigger_callbacks('whitelist_changed', change)
    
    async def remove(self, guild_id: int, user_id: int, moderator_id: int = None):
        """Remove user from guild whitelist"""
        if guild_id not in self._whitelists:
            await self._load_whitelist(guild_id)
        
        if guild_id in self._whitelists:
            self._whitelists[guild_id].discard(user_id)
            
            # Save to storage backend
            await self.storage.remove_whitelist_user(guild_id, user_id)
            
            # Trigger callback
            change = WhitelistChange(
                guild_id=guild_id,
                user_id=user_id,
                action="removed",
                moderator_id=moderator_id
            )
            await self.sdk._trigger_callbacks('whitelist_changed', change)
    
    async def get_all(self, guild_id: int) -> List[int]:
        """Get all whitelisted users for guild"""
        if guild_id not in self._whitelists:
            await self._load_whitelist(guild_id)
        return list(self._whitelists.get(guild_id, set()))
    
    async def is_whitelisted(self, guild_id: int, user_id: int) -> bool:
        """
        Check if user is whitelisted in specific guild.
        Uses cached data - instant response (no file I/O).
        """
        if guild_id not in self._whitelists:
            await self._load_whitelist(guild_id)
        
        return user_id in self._whitelists.get(guild_id, set())
    
    async def clear(self, guild_id: int):
        """Clear all whitelisted users for a guild"""
        self._whitelists[guild_id] = set()
        await self.storage.clear_whitelist(guild_id)

