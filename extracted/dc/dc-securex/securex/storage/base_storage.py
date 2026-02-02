"""
Base storage backend abstract class.
All storage implementations must inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Set


class BaseStorageBackend(ABC):
    """Abstract base class for storage backends"""
    
    # ===== Backup Operations =====
    
    @abstractmethod
    async def save_channel_backup(self, guild_id: int, backup_data: dict) -> None:
        """Save channel backup data for a guild"""
        pass
    
    @abstractmethod
    async def load_channel_backup(self, guild_id: int) -> Optional[dict]:
        """Load channel backup data for a guild"""
        pass
    
    @abstractmethod
    async def save_role_backup(self, guild_id: int, backup_data: dict) -> None:
        """Save role backup data for a guild"""
        pass
    
    @abstractmethod
    async def load_role_backup(self, guild_id: int) -> Optional[dict]:
        """Load role backup data for a guild"""
        pass
    
    @abstractmethod
    async def save_guild_settings(self, guild_id: int, settings_data: dict) -> None:
        """Save guild settings (vanity, name, icon, etc.)"""
        pass
    
    @abstractmethod
    async def load_guild_settings(self, guild_id: int) -> Optional[dict]:
        """Load guild settings"""
        pass
    
    @abstractmethod
    async def load_all_guild_settings(self) -> Dict[int, dict]:
        """Load all guild settings at once (for cache preloading)"""
        pass
    
    @abstractmethod
    async def save_all_guild_settings(self, all_settings: Dict[int, dict]) -> None:
        """Save all guild settings at once"""
        pass
    
    # ===== Whitelist Operations =====
    
    @abstractmethod
    async def add_whitelist_user(self, guild_id: int, user_id: int) -> None:
        """Add a user to guild whitelist"""
        pass
    
    @abstractmethod
    async def remove_whitelist_user(self, guild_id: int, user_id: int) -> None:
        """Remove a user from guild whitelist"""
        pass
    
    @abstractmethod
    async def get_whitelist_users(self, guild_id: int) -> Set[int]:
        """Get all whitelisted users for a guild"""
        pass
    
    @abstractmethod
    async def is_whitelisted(self, guild_id: int, user_id: int) -> bool:
        """Check if a user is whitelisted in a guild"""
        pass
    
    @abstractmethod
    async def clear_whitelist(self, guild_id: int) -> None:
        """Clear all whitelisted users for a guild"""
        pass
    
    @abstractmethod
    async def load_all_whitelists(self) -> Dict[int, Set[int]]:
        """Load all whitelists at once (for cache preloading)"""
        pass
    
    # ===== User Token Operations =====
    
    @abstractmethod
    async def save_user_token(self, guild_id: int, token: str, set_by: Optional[int] = None, 
                            description: Optional[str] = None) -> None:
        """Save user token for a guild"""
        pass
    
    @abstractmethod
    async def load_user_token(self, guild_id: int) -> Optional[dict]:
        """Load user token for a guild"""
        pass
    
    @abstractmethod
    async def update_token_last_used(self, guild_id: int) -> None:
        """Update last_used timestamp for a token"""
        pass
    
    @abstractmethod
    async def load_all_user_tokens(self) -> Dict[int, dict]:
        """Load all user tokens at once"""
        pass
