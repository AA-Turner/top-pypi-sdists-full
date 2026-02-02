"""
Comprehensive tests for SQLite storage backend to achieve 100% coverage.
"""

import pytest
import asyncio
import aiosqlite
from pathlib import Path
from securex.storage import SqliteStorageBackend


@pytest.mark.asyncio
class TestSqliteStorage:
    """Comprehensive tests for SQLite storage backend"""
    
    async def test_initialization(self, tmp_path):
        """Test database initialization and WAL mode"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        db_path = tmp_path / "test_init.db"
        storage = SqliteStorageBackend(db_path=str(db_path))
        
        # Initialize by making a query
        await storage.save_channel_backup(123, {"test": "data"})
        
        # Verify WAL mode is enabled
        async with aiosqlite.connect(db_path) as conn:
            async with conn.execute("PRAGMA journal_mode") as cursor:
                mode = await cursor.fetchone()
                assert mode[0].lower() == "wal"
    
    # ===== Channel Backup Tests =====
    
    async def test_save_and_load_channel_backup(self, tmp_path):
        """Test saving and loading channel backups"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        backup_data = {
            "channels": [
                {"id": 1, "name": "general", "type": "text"},
                {"id": 2, "name": "voice", "type": "voice"}
            ]
        }
        
        # Save
        await storage.save_channel_backup(12345, backup_data)
        
        # Load
        loaded = await storage.load_channel_backup(12345)
        assert loaded == backup_data
    
    async def test_load_nonexistent_channel_backup(self, tmp_path):
        """Test loading a channel backup that doesn't exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        loaded = await storage.load_channel_backup(99999)
        assert loaded is None
    
    async def test_overwrite_channel_backup(self, tmp_path):
        """Test overwriting an existing channel backup"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Save first backup
        await storage.save_channel_backup(123, {"version": 1})
        
        # Overwrite with new backup
        await storage.save_channel_backup(123, {"version": 2})
        
        # Verify latest version
        loaded = await storage.load_channel_backup(123)
        assert loaded["version"] == 2
    
    # ===== Role Backup Tests =====
    
    async def test_save_and_load_role_backup(self, tmp_path):
        """Test saving and loading role backups"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        backup_data = {
            "roles": [
                {"id": 10, "name": "Admin", "permissions": 8},
                {"id": 20, "name": "Member", "permissions": 0}
            ]
        }
        
        # Save
        await storage.save_role_backup(12345, backup_data)
        
        # Load
        loaded = await storage.load_role_backup(12345)
        assert loaded == backup_data
    
    async def test_load_nonexistent_role_backup(self, tmp_path):
        """Test loading a role backup that doesn't exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        loaded = await storage.load_role_backup(99999)
        assert loaded is None
    
    async def test_overwrite_role_backup(self, tmp_path):
        """Test overwriting an existing role backup"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.save_role_backup(123, {"version": 1})
        await storage.save_role_backup(123, {"version": 2})
        
        loaded = await storage.load_role_backup(123)
        assert loaded["version"] == 2
    
    # ===== Guild Settings Tests =====
    
    async def test_save_and_load_guild_settings(self, tmp_path):
        """Test saving and loading guild settings"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        settings = {
            "name": "Test Server",
            "vanity_url_code": "testserver",
            "icon": "icon_hash",
            "banner": "banner_hash"
        }
        
        await storage.save_guild_settings(12345, settings)
        loaded = await storage.load_guild_settings(12345)
        assert loaded == settings
    
    async def test_load_nonexistent_guild_settings(self, tmp_path):
        """Test loading guild settings that don't exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        loaded = await storage.load_guild_settings(99999)
        assert loaded is None
    
    async def test_load_all_guild_settings(self, tmp_path):
        """Test loading all guild settings"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Save multiple guild settings
        await storage.save_guild_settings(111, {"name": "Server 1"})
        await storage.save_guild_settings(222, {"name": "Server 2"})
        await storage.save_guild_settings(333, {"name": "Server 3"})
        
        # Load all
        all_settings = await storage.load_all_guild_settings()
        assert len(all_settings) == 3
        assert all_settings[111]["name"] == "Server 1"
        assert all_settings[222]["name"] == "Server 2"
        assert all_settings[333]["name"] == "Server 3"
    
    async def test_load_all_guild_settings_empty(self, tmp_path):
        """Test loading all guild settings when none exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        all_settings = await storage.load_all_guild_settings()
        assert all_settings == {}
    
    async def test_save_all_guild_settings(self, tmp_path):
        """Test saving all guild settings at once"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        settings_dict = {
            111: {"name": "Server 1"},
            222: {"name": "Server 2"},
            333: {"name": "Server 3"}
        }
        
        await storage.save_all_guild_settings(settings_dict)
        
        # Verify all were saved
        loaded = await storage.load_all_guild_settings()
        assert len(loaded) == 3
        assert loaded[111]["name"] == "Server 1"
    
    # ===== Whitelist Tests =====
    
    async def test_add_and_get_whitelist_users(self, tmp_path):
        """Test adding users to whitelist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Add users
        await storage.add_whitelist_user(12345, 111)
        await storage.add_whitelist_user(12345, 222)
        await storage.add_whitelist_user(12345, 333)
        
        # Get all users
        users = await storage.get_whitelist_users(12345)
        assert users == {111, 222, 333}
    
    async def test_get_whitelist_users_empty(self, tmp_path):
        """Test getting whitelist users when none exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        users = await storage.get_whitelist_users(99999)
        assert users == set()
    
    async def test_add_duplicate_whitelist_user(self, tmp_path):
        """Test adding the same user twice (should not error)"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.add_whitelist_user(123, 111)
        await storage.add_whitelist_user(123, 111)  # Duplicate
        
        users = await storage.get_whitelist_users(123)
        assert users == {111}  # Should only appear once
    
    async def test_remove_whitelist_user(self, tmp_path):
        """Test removing a user from whitelist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Add users
        await storage.add_whitelist_user(123, 111)
        await storage.add_whitelist_user(123, 222)
        
        # Remove one
        await storage.remove_whitelist_user(123, 111)
        
        # Verify
        users = await storage.get_whitelist_users(123)
        assert users == {222}
    
    async def test_remove_nonexistent_whitelist_user(self, tmp_path):
        """Test removing a user that isn't whitelisted (should not error)"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.remove_whitelist_user(123, 999)  # Doesn't exist
        # Should not raise an error
    
    async def test_is_whitelisted(self, tmp_path):
        """Test checking if a user is whitelisted"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.add_whitelist_user(123, 111)
        
        assert await storage.is_whitelisted(123, 111) is True
        assert await storage.is_whitelisted(123, 222) is False
    
    async def test_clear_whitelist(self, tmp_path):
        """Test clearing all whitelisted users for a guild"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Add users
        await storage.add_whitelist_user(123, 111)
        await storage.add_whitelist_user(123, 222)
        await storage.add_whitelist_user(123, 333)
        
        # Clear
        await storage.clear_whitelist(123)
        
        # Verify
        users = await storage.get_whitelist_users(123)
        assert users == set()
    
    async def test_load_all_whitelists(self, tmp_path):
        """Test loading all whitelists at once"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Add users to multiple guilds
        await storage.add_whitelist_user(111, 1)
        await storage.add_whitelist_user(111, 2)
        await storage.add_whitelist_user(222, 3)
        await storage.add_whitelist_user(333, 4)
        await storage.add_whitelist_user(333, 5)
        
        # Load all
        whitelists = await storage.load_all_whitelists()
        assert len(whitelists) == 3
        assert whitelists[111] == {1, 2}
        assert whitelists[222] == {3}
        assert whitelists[333] == {4, 5}
    
    async def test_load_all_whitelists_empty(self, tmp_path):
        """Test loading all whitelists when none exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        whitelists = await storage.load_all_whitelists()
        assert whitelists == {}
    
    # ===== User Token Tests =====
    
    async def test_save_and_load_user_token(self, tmp_path):
        """Test saving and loading user tokens"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.save_user_token(
            123, 
            "test_token_123", 
            set_by=999,
            description="Test token"
        )
        
        token_data = await storage.load_user_token(123)
        assert token_data["token"] == "test_token_123"
        assert token_data["set_by"] == 999
        assert token_data["description"] == "Test token"
        assert token_data["last_used"] is None
        assert token_data["created_at"] is not None
    
    async def test_load_nonexistent_user_token(self, tmp_path):
        """Test loading a token that doesn't exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        token = await storage.load_user_token(99999)
        assert token is None
    
    async def test_save_user_token_minimal(self, tmp_path):
        """Test saving a token with minimal parameters"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.save_user_token(123, "token123")
        
        token_data = await storage.load_user_token(123)
        assert token_data["token"] == "token123"
        assert token_data["set_by"] is None
        assert token_data["description"] is None
    
    async def test_update_token_last_used(self, tmp_path):
        """Test updating the last_used timestamp"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Save token
        await storage.save_user_token(123, "token123")
        
        # Update last_used
        await storage.update_token_last_used(123)
        
        # Verify
        token_data = await storage.load_user_token(123)
        assert token_data["last_used"] is not None
    
    async def test_load_all_user_tokens(self, tmp_path):
        """Test loading all user tokens"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        # Save multiple tokens
        await storage.save_user_token(111, "token1", set_by=1, description="First")
        await storage.save_user_token(222, "token2", set_by=2, description="Second")
        await storage.save_user_token(333, "token3")
        
        # Load all
        all_tokens = await storage.load_all_user_tokens()
        assert len(all_tokens) == 3
        assert all_tokens[111]["token"] == "token1"
        assert all_tokens[222]["token"] == "token2"
        assert all_tokens[333]["token"] == "token3"
    
    async def test_load_all_user_tokens_empty(self, tmp_path):
        """Test loading all tokens when none exist"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        tokens = await storage.load_all_user_tokens()
        assert tokens == {}
    
    async def test_overwrite_user_token(self, tmp_path):
        """Test overwriting an existing token"""
        storage = SqliteStorageBackend(db_path=str(tmp_path / "test.db"))
        await storage.save_user_token(123, "old_token")
        await storage.save_user_token(123, "new_token", description="Updated")
        
        token_data = await storage.load_user_token(123)
        assert token_data["token"] == "new_token"
        assert token_data["description"] == "Updated"
