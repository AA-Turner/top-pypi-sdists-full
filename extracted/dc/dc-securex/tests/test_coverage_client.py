import pytest
import asyncio
import discord
from securex import SecureX
from unittest.mock import Mock, AsyncMock, patch, MagicMock

@pytest.mark.asyncio
class TestClientExhaustive:
    """Exhaustive tests for securex/client.py to reach 100% coverage"""

    async def test_audit_log_listener_success(self):
        """Test on_audit_log_entry_create when everything is normal"""
        bot = Mock(spec=discord.Client)
        sx = SecureX(bot)
        
        # Mock queues
        sx.action_queue = Mock(spec=asyncio.Queue)
        sx.action_queue.put = AsyncMock()
        sx.log_queue = Mock(spec=asyncio.Queue)
        sx.log_queue.put = AsyncMock()
        sx.cleanup_queue = Mock(spec=asyncio.Queue)
        sx.cleanup_queue.put = AsyncMock()
        sx.guild_queue = Mock(spec=asyncio.Queue)
        sx.guild_queue.put = AsyncMock()
        
        # Get the listener
        listeners = bot.event.call_args_list
        listener_func = None
        for call in listeners:
            if call[0][0].__name__ == 'on_audit_log_entry_create':
                listener_func = call[0][0]
                break
        
        entry = Mock(spec=discord.AuditLogEntry)
        await listener_func(entry)
        
        sx.action_queue.put.assert_called_once_with(entry)
        sx.log_queue.put.assert_called_once_with(entry)
        sx.cleanup_queue.put.assert_called_once_with(entry)
        sx.guild_queue.put.assert_called_once_with(entry)

    async def test_audit_log_listener_queue_full(self):
        """Test on_audit_log_entry_create when queues are full"""
        bot = Mock(spec=discord.Client)
        sx = SecureX(bot)
        
        # Mock queues to raise QueueFull
        sx.action_queue = Mock(spec=asyncio.Queue)
        sx.action_queue.put = AsyncMock(side_effect=asyncio.QueueFull)
        
        # Get the listener
        listeners = bot.event.call_args_list
        listener_func = None
        for call in listeners:
            if call[0][0].__name__ == 'on_audit_log_entry_create':
                listener_func = call[0][0]
                break
        
        assert listener_func is not None
        
        entry = Mock(spec=discord.AuditLogEntry)
        # Should catch QueueFull and print warning
        await listener_func(entry)

    def test_client_postgres_without_url(self):
        """Test client raises ValueError when postgres_backend specified without URL"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=1234567)
        
        with pytest.raises(ValueError, match="postgres_url required"):
            SecureX(bot, storage_backend="postgres")
    
    def test_client_postgres_with_url(self, tmp_path):
        """Test client with PostgreSQL backend"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=1234567)
        
        try:
            client = SecureX(
                bot,
                storage_backend="postgres",
                postgres_url="postgresql://localhost/test",
                postgres_pool_size=5
            )
            # Should create postgres backend
            from securex.storage.postgres_storage import PostgresStorageBackend
            assert isinstance(client.storage, PostgresStorageBackend)
        except ImportError:
            # asyncpg not installed, skip
            pytest.skip("asyncpg not installed")

    @pytest.mark.asyncio
    async def test_client_enable_with_postgres_initialization(self, tmp_path):
        """Test client.enable() initializes PostgreSQL storage backend"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=1234567)
        
        try:
            client = SecureX(
                bot,
                backup_dir=str(tmp_path),
                storage_backend="postgres",
                postgres_url="postgresql://localhost/test"
            )
            
            # Mock the initialize method
            client.storage.initialize = AsyncMock()
            
            await client.enable(guild_id=12345, whitelist=[1, 2, 3])
            
            # Should have called initialize
            client.storage.initialize.assert_called_once()
        except ImportError:
            pytest.skip("asyncpg not installed")

    async def test_registered_events(self):
        """Test all registered Discord event listeners in client.py"""
        bot = Mock(spec=discord.Client)
        sx = SecureX(bot)
        
        event_mappers = {}
        for call in bot.event.call_args_list:
            func = call[0][0]
            event_mappers[func.__name__] = func
            
        # 1. on_guild_channel_delete
        channel = Mock()
        sx.channel_handler.on_channel_delete = AsyncMock()
        await event_mappers['on_guild_channel_delete'](channel)
        sx.channel_handler.on_channel_delete.assert_called_once_with(channel)

        # 2. on_guild_channel_update
        before, after = Mock(), Mock()
        sx.channel_handler.on_channel_update = AsyncMock()
        await event_mappers['on_guild_channel_update'](before, after)
        sx.channel_handler.on_channel_update.assert_called_once_with(before, after)

        # 3. on_guild_role_delete
        role = Mock()
        sx.role_handler.on_role_delete = AsyncMock()
        await event_mappers['on_guild_role_delete'](role)
        sx.role_handler.on_role_delete.assert_called_once_with(role)

        # 4. on_guild_role_update
        before_r, after_r = Mock(), Mock()
        sx.role_handler.on_role_update = AsyncMock()
        await event_mappers['on_guild_role_update'](before_r, after_r)
        sx.role_handler.on_role_update.assert_called_once_with(before_r, after_r)

        # 5. on_member_ban
        guild, user = Mock(), Mock()
        sx.member_handler.on_member_ban = AsyncMock()
        await event_mappers['on_member_ban'](guild, user)
        sx.member_handler.on_member_ban.assert_called_once_with(guild, user)

        # 6. on_member_update
        before_m, after_m = Mock(), Mock()
        sx.member_handler.on_member_update = AsyncMock()
        await event_mappers['on_member_update'](before_m, after_m)
        sx.member_handler.on_member_update.assert_called_once_with(before_m, after_m)

    async def test_callback_decorators_and_triggering(self):
        """Test @sx.on decorators and _trigger_callbacks logic"""
        bot = Mock()
        sx = SecureX(bot)
        
        # Test async callback
        mock_async_cb = AsyncMock()
        sx.on('threat_detected')(mock_async_cb)
        
        # Test sync callback
        mock_sync_cb = MagicMock()
        sx.on('threat_detected')(mock_sync_cb)
        
        await sx._trigger_callbacks('threat_detected', "arg1", extra="data")
        
        mock_async_cb.assert_called_once_with("arg1", extra="data")
        mock_sync_cb.assert_called_once_with("arg1", extra="data")
        
        # Test callback with exception
        fail_cb = Mock(side_effect=Exception("Callback failed"))
        sx.on('threat_detected')(fail_cb)
        # Should not raise exception
        await sx._trigger_callbacks('threat_detected')
        
        # Test triggering non-existent event
        await sx._trigger_callbacks('non_existent')
        
        # Test convenience properties
        sx.on_threat_detected(lambda x: x)
        sx.on_backup_completed(lambda x: x)
        sx.on_restore_completed(lambda x: x)
        sx.on_whitelist_changed(lambda x: x)
        
        assert len(sx._callbacks['threat_detected']) == 4 # 2 from before + 1 fail + 1 lambda
        assert len(sx._callbacks['backup_completed']) == 1

    async def test_enable_full(self):
        """Test sx.enable with full set of parameters for max coverage"""
        bot = Mock()
        sx = SecureX(bot)
        
        sx.whitelist.preload_all = AsyncMock()
        sx.whitelist.get_all = AsyncMock(return_value=[1, 2])
        sx.whitelist.add = AsyncMock()
        sx.backup_manager.preload_all = AsyncMock()
        sx.backup_manager.create_backup = AsyncMock(return_value=Mock(success=True, channel_count=5, role_count=10))
        
        # Mock start_auto_backup and start_auto_refresh manually
        sx.backup_manager.start_auto_backup = MagicMock()
        sx.backup_manager.start_auto_refresh = MagicMock()
        
        await sx.enable(
            guild_id=123,
            whitelist=[3],
            auto_backup=True,
            punishments={"channel_delete": "kick"},
            notify_user=True
        )
        
        assert sx.whitelist_cache[123] == {1, 2, 3}
        assert sx.punishment_cache[123]["channel_delete"] == "kick"
        sx.backup_manager.start_auto_backup.assert_called_once()
        sx.backup_manager.start_auto_refresh.assert_called_once()

    async def test_enable_minimal(self):
        """Test sx.enable with minimal parameters"""
        bot = Mock()
        sx = SecureX(bot)
        
        # Mocking to avoid real side effects
        sx.whitelist.preload_all = AsyncMock()
        sx.backup_manager.preload_all = AsyncMock()
        sx.backup_manager.start_auto_backup = MagicMock()
        sx.backup_manager.start_auto_refresh = MagicMock()
        
        await sx.enable(auto_backup=False)
        
        # These should NOT be called if auto_backup is False
        sx.backup_manager.start_auto_backup.assert_not_called()
        sx.backup_manager.start_auto_refresh.assert_not_called()

    async def test_proxy_methods(self):
        """Test create_backup, restore_channel, and restore_role proxy methods"""
        bot = Mock()
        sx = SecureX(bot)
        
        # restore_channel
        sx.backup_manager.restore_channel = AsyncMock(return_value="new_channel")
        res = await sx.restore_channel(Mock(), Mock())
        assert res == "new_channel"
        
        # restore_role
        sx.backup_manager.restore_role = AsyncMock(return_value=True)
        res = await sx.restore_role(Mock(), 999)
        assert res is True
        
        # create_backup
        sx.backup_manager.create_backup = AsyncMock(return_value="backup_info")
        res = await sx.create_backup(123)
        assert res == "backup_info"
