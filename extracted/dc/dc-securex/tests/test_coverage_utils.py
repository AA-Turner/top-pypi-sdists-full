import pytest
import asyncio
import discord
import os
import json
from datetime import datetime, timezone
from securex.models import ThreatEvent, BackupInfo, RestoreResult, WhitelistChange, UserToken
from securex.utils.punishment import PunishmentExecutor
from securex.utils.whitelist import WhitelistManager
from unittest.mock import Mock, AsyncMock, patch

@pytest.mark.asyncio
class TestUtilsExhaustive:
    """Exhaustive tests for models, punishment, and whitelist to reach 100% coverage"""

    async def test_models_full(self):
        """Test all models serialization"""
        # ThreatEvent
        te = ThreatEvent(
            type="test", guild_id=1, actor_id=2, target_id=3, target_name="n",
            prevented=True, restored=True, timestamp=datetime.now(timezone.utc)
        )
        d = te.to_dict()
        assert d['type'] == "test"
        assert isinstance(d['timestamp'], str)
        assert te.to_json().startswith('{"type": "test"')

        # BackupInfo
        bi = BackupInfo(guild_id=1, timestamp=datetime.now(timezone.utc), channel_count=5, role_count=10, backup_path="/p")
        bd = bi.to_dict()
        assert bd['channel_count'] == 5

        # RestoreResult
        rr = RestoreResult(success=True, items_restored=5, items_failed=0)
        assert rr.to_dict()['success'] is True

        # WhitelistChange
        wc = WhitelistChange(guild_id=1, user_id=2, action="added")
        assert wc.to_dict()['action'] == "added"
        
        # UserToken
        ut = UserToken(guild_id=123, token="test_token", set_by=999, description="Test")
        assert ut.guild_id == 123
        assert ut.token == "test_token"
        assert ut.last_used is None
        ut.mark_used()
        assert ut.last_used is not None
        ud = ut.to_dict()
        assert ud['guild_id'] == 123
        assert isinstance(ud['timestamp'], str)

    async def test_punishment_full(self):
        """Test all punishment branches"""
        bot = Mock()
        executor = PunishmentExecutor(bot)
        guild = Mock()
        user = Mock(id=123)
        sdk = Mock()
        sdk.timeout_duration = 60
        sdk.notify_punished_user = True
        
        # sdk is None
        assert await executor.punish(guild, user, "type", sdk=None) == "none"
        
        # action is none
        sdk.punishments = {"type": "none"}
        assert await executor.punish(guild, user, "type", sdk=sdk) == "none"
        
        # Not a member
        guild.get_member.return_value = None
        sdk.punishments = {"type": "kick"}
        assert await executor.punish(guild, user, "type", sdk=sdk) == "kick"
        
        # Owner bypass
        member = Mock(id=123)
        guild.owner_id = 123
        guild.get_member.return_value = member
        assert await executor.punish(guild, user, "type", sdk=sdk) == "kick"
        
        # Warn
        guild.owner_id = 999
        sdk.punishments = {"type": "warn"}
        assert await executor.punish(guild, user, "type", sdk=sdk) == "warn"
        
        # Timeout
        sdk.punishments = {"type": "timeout"}
        member.timeout = AsyncMock()
        member.send = AsyncMock()
        assert await executor.punish(guild, user, "type", sdk=sdk) == "timeout"
        member.timeout.assert_called_once()
        
        # Kick
        sdk.punishments = {"type": "kick"}
        member.kick = AsyncMock()
        assert await executor.punish(guild, user, "type", sdk=sdk) == "kick"
        
        # Ban
        sdk.punishments = {"type": "ban"}
        member.ban = AsyncMock()
        assert await executor.punish(guild, user, "type", sdk=sdk) == "ban"
        
        # Forbidden error
        member.ban.side_effect = discord.Forbidden(Mock(), "fail")
        await executor.punish(guild, user, "type", sdk=sdk)
        
        # General Exception
        member.ban.side_effect = Exception("err")
        await executor.punish(guild, user, "type", sdk=sdk)

        # Notify user branches
        member.send.side_effect = discord.Forbidden(Mock(), "fail")
        await executor._notify_user(member, "type", "ban", "details", sdk)
        member.send.side_effect = Exception("err")
        await executor._notify_user(member, "type", "ban", "details", sdk)

    async def test_whitelist_full(self, tmp_path):
        """Test whitelist manager branches"""
        sdk = Mock()
        sdk.bot = Mock()
        sdk._trigger_callbacks = AsyncMock()
        
        # Patch data_dir to tmp_path
        with patch("securex.utils.whitelist.Path", return_value=tmp_path):
            # We need to be careful with Path inheritance. 
            # Better to just set manager.data_dir directly if possible, but __init__ sets it.
            # Let's patch WhitelistManager's Path in its module.
            with patch("securex.utils.whitelist.Path") as mock_path:
                mock_path.return_value = tmp_path
                mock_storage = Mock()
                # Patch all async methods used by WhitelistManager
                mock_storage.load_all_whitelists = AsyncMock(return_value={})
                mock_storage.get_whitelist_users = AsyncMock(return_value=set())
                mock_storage.add_whitelist_user = AsyncMock()
                mock_storage.remove_whitelist_user = AsyncMock()
                mock_storage.clear_whitelist = AsyncMock()
                manager = WhitelistManager(sdk, mock_storage)
                manager.data_dir = tmp_path # Ensure it's set

                # add/is_whitelisted
                await manager.add(777, 123)
                assert await manager.is_whitelisted(777, 123) is True
                assert await manager.is_whitelisted(777, 999) is False

                # remove
                await manager.remove(777, 123)
                assert await manager.is_whitelisted(777, 123) is False
                assert 123 not in await manager.get_all(777)
                
                # get_all
                await manager.add(777, 456)
                all_whitelisted = await manager.get_all(777)
                assert 456 in all_whitelisted
                
                # Preload (success)
                mock_storage.load_all_whitelists = AsyncMock(return_value={888: {1, 2}})
                manager._cache_loaded = False
                await manager.preload_all()
                assert await manager.is_whitelisted(888, 1) is True
                
                # Preload (already loaded)
                await manager.preload_all()
                
                # Preload (error)
                mock_storage.load_all_whitelists = AsyncMock(side_effect=Exception("Storage error"))
                manager._cache_loaded = False
                await manager.preload_all()
                
                # clear
                await manager.clear(777)
                assert len(await manager.get_all(777)) == 0
                
                # Load fallback in remove
                mock_storage.get_whitelist_users = AsyncMock(return_value={8})
                manager._whitelists.pop(998, None)
                await manager.remove(998, 8)
                assert 8 not in await manager.get_all(998)
                
                # Load fallback in get_all
                mock_storage.get_whitelist_users = AsyncMock(return_value={7})
                manager._whitelists.pop(997, None)
                all_7 = await manager.get_all(997)
                assert 7 in all_7
                
                # Load fallback in is_whitelisted
                mock_storage.get_whitelist_users = AsyncMock(return_value={9})
                manager._whitelists.pop(999, None)
                assert await manager.is_whitelisted(999, 9) is True
    
    async def test_whitelist_load_fallback_clear(self):
        """Test clear() when whitelist needs to be loaded first"""
        sdk = Mock()
        sdk._trigger_callbacks = AsyncMock()
        storage = Mock()
        storage.get_whitelist_users = AsyncMock(return_value={1, 2, 3})
        storage.clear_whitelist = AsyncMock()
        storage.load_all_whitelists = AsyncMock(return_value={})
        
        manager = WhitelistManager(sdk, storage)
        
        # Clear when not yet loaded
        await manager.clear(777)
        
        # Should have called storage methods
        storage.clear_whitelist.assert_called_once()
    
    async def test_whitelist_add_when_not_preloaded(self):
        """Test adding when cache not yet loaded"""
        sdk = Mock()
        sdk._trigger_callbacks = AsyncMock()
        storage = Mock()
        storage.get_whitelist_users = AsyncMock(return_value=set())
        storage.add_whitelist_user = AsyncMock()
        storage.load_all_whitelists = AsyncMock(return_value={})
        
        manager = WhitelistManager(sdk, storage)
        # Add without preloading first  
        await manager.add(777, 123)
        
        # Should load first, then add
        storage.get_whitelist_users.assert_called_once()
        storage.add_whitelist_user.assert_called_once()
    
    async def test_whitelist_save_and_init_fallback(self):
        """Test _save_whitelist (line 52) and initialization fallback in add (line 59)"""
        sdk = Mock()
        sdk._trigger_callbacks = AsyncMock()
        storage = Mock()
        storage.get_whitelist_users = AsyncMock(return_value=set())  # Returns empty, triggers line 59
        storage.add_whitelist_user = AsyncMock()
        storage.load_all_whitelists = AsyncMock(return_value={})
        
        manager = WhitelistManager(sdk, storage)
        
        # Add to a guild that doesn't exist yet (triggers line 56-59)
        await manager.add(999, 123)
        
        # The whitelist should now exist
        assert 999 in manager._whitelists
        assert 123 in manager._whitelists[999]
        
        # Test _save_whitelist directly (covers line 52 - the pass statement)
        await manager._save_whitelist(999)  # This is a no-op but covers the line


# Storage factory tests
def test_create_sqlite_backend(tmp_path):
    """Test creating SQLite backend"""
    from securex.storage import create_storage_backend, SqliteStorageBackend
    db_path = tmp_path / "test.db"
    storage = create_storage_backend("sqlite", db_path=str(db_path))
    assert isinstance(storage, SqliteStorageBackend)
    assert storage.db_path == db_path


def test_create_sqlite_backend_default_path():
    """Test creating SQLite backend with default path"""
    from securex.storage import create_storage_backend, SqliteStorageBackend
    storage = create_storage_backend("sqlite")
    assert isinstance(storage, SqliteStorageBackend)


def test_create_postgres_backend_without_url():
    """Test creating PostgreSQL backend without URL raises ValueError"""
    from securex.storage import create_storage_backend
    with pytest.raises(ValueError, match="url"):
        create_storage_backend("postgres")


def test_create_unknown_backend():
    """Test creating unknown backend type raises ValueError"""
    from securex.storage import create_storage_backend
    with pytest.raises(ValueError, match="Unknown storage backend"):
        create_storage_backend("invalid_backend_type")


def test_base_storage_is_abstract():
    """Test that BaseStorageBackend cannot be instantiated directly"""
    from securex.storage.base_storage import BaseStorageBackend
    with pytest.raises(TypeError):
        BaseStorageBackend()


def test_create_postgres_backend_with_pool_params():
    """Test creating PostgreSQL backend with pool parameters (covers lines 44-47)"""
    from securex.storage import create_storage_backend
    
    try:
        storage = create_storage_backend(
            "postgres",
            url="postgresql://localhost/test",
            pool_size=15,
            max_overflow=30
        )
        from securex.storage.postgres_storage import PostgresStorageBackend
        assert isinstance(storage, PostgresStorageBackend)
        assert storage.min_pool_size == 15
        assert storage.max_pool_size == 30
    except ImportError:
        # asyncpg not installed, skip
        pytest.skip("asyncpg not installed")


def test_storage_init_imports_postgres():
    """Test that storage/__init__.py properly imports PostgreSQL backend"""
    try:
        import securex.storage
        # Check if PostgresStorageBackend is in __all__
        assert 'create_storage_backend' in securex.storage.__all__
        assert 'SqliteStorageBackend' in securex.storage.__all__
        
        # Try to import PostgresStorageBackend if available
        from securex.storage.postgres_storage import PostgresStorageBackend
        assert 'PostgresStorageBackend' in securex.storage.__all__
    except ImportError:
        # asyncpg not installed, PostgresStorageBackend shouldn't be in __all__
        import securex.storage
        assert 'PostgresStorageBackend' not in securex.storage.__all__
