import pytest
import asyncio
import discord
import json
from securex import SecureX
from securex.models import ThreatEvent
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime

@pytest.mark.asyncio
class TestWorkersExhaustive:
    """Exhaustive tests for securex/workers/ to reach 100% coverage"""

    async def test_action_worker_full(self):
        """Test ActionWorker branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        worker = sx.action_worker
        
        # 1. Test start/stop
        await worker.start()
        await worker.start() 
        assert worker._worker_task is not None
        await worker.stop()
        assert worker._worker_task is None

        # 2. Test _worker_loop
        entry_mock = Mock(spec=discord.AuditLogEntry)
        entry_mock.action = discord.AuditLogAction.channel_create
        entry_mock.user = Mock(id=999, name="TestUser")
        entry_mock.guild = Mock(id=777, owner_id=111)
        worker.action_queue = Mock(spec=asyncio.Queue)
        worker.action_queue.get = AsyncMock(side_effect=[entry_mock, Exception("Queue error"), asyncio.CancelledError])
        with patch.object(worker, '_process_entry', new_callable=AsyncMock) as mock_process:
            await worker._worker_loop()
            mock_process.assert_called_once()

        # 3. Test _process_entry branches
        guild = Mock(spec=discord.Guild)
        guild.id = 777
        guild.owner_id = 111
        
        # A. Bot executor
        entry_bot = Mock(user=Mock(id=123))
        await worker._process_entry(entry_bot)
        
        # B. Owner executor
        entry_owner = Mock(user=Mock(id=111), guild=guild)
        await worker._process_entry(entry_owner)
        
        # C. Whitelisted executor
        entry_wl = Mock(user=Mock(id=888), guild=guild)
        sx.whitelist_cache[777] = {888}
        await worker._process_entry(entry_wl)
        
        # D. Unknown violation type
        entry_unknown = Mock(user=Mock(id=999), guild=guild, action=9999)
        await worker._process_entry(entry_unknown)
        
        # E. bot_add violation (Success)
        target_bot = Mock(id=555)
        target_bot.name = "MyBot"
        bot_member = Mock(spec=discord.Member)
        bot_member.ban = AsyncMock()
        guild.get_member = Mock(return_value=bot_member)
        entry_bot_add = Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.bot_add, target=target_bot)
        entry_bot_add.user.name = "Violator"
        await worker._process_entry(entry_bot_add)
        bot_member.ban.assert_called_once()
        
        # F. bot_add violation (Failure)
        bot_member.ban.side_effect = Exception("Ban failed")
        await worker._process_entry(entry_bot_add)

        # G. Instant ban types (member_kick)
        entry_kick = Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.kick)
        entry_kick.user.name = "Violator"
        guild.ban = AsyncMock()
        await worker._process_entry(entry_kick)
        guild.ban.assert_called_once()
        
        # H. Instant ban types failure
        guild.ban.side_effect = Exception("Guild ban failed")
        await worker._process_entry(entry_kick)

        # I. General punishment SUCCESS
        sx.punishments["role_create"] = "kick"
        entry_role = Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.role_create, target=Mock(id=444))
        entry_role.target.name = "EvilRole"
        entry_role.user.name = "Violator"
        sx.punisher.punish = AsyncMock(return_value="kick")
        await worker._process_entry(entry_role)

        # J. General punishment exception
        sx.punisher.punish.side_effect = Exception("Punish failed")
        await worker._process_entry(entry_role)

        # K. Error path line 114
        with patch.object(worker, 'action_map', side_effect=Exception("Map error")):
             await worker._process_entry(None)

    async def test_cleanup_worker_full(self):
        """Test CleanupWorker branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        worker = sx.cleanup_worker
        
        await worker.start()
        await worker.stop()

        entry_mock = Mock()
        worker.cleanup_queue = Mock()
        worker.cleanup_queue.get = AsyncMock(side_effect=[entry_mock, Exception("Loop error"), asyncio.CancelledError])
        with patch.object(worker, '_process_entry', new_callable=AsyncMock) as mock_process:
            await worker._worker_loop()
            mock_process.assert_called_once()

        guild = Mock(spec=discord.Guild)
        guild.id = 777
        guild.owner_id = 111
        
        await worker._process_entry(Mock(user=Mock(id=123), guild=guild))
        await worker._process_entry(Mock(user=Mock(id=111), guild=guild))
        sx.whitelist_cache[777] = {888}
        await worker._process_entry(Mock(user=Mock(id=888), guild=guild))
        
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.ban))
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.role_create, target=None))

        role = Mock()
        role.name = "EvilRole"
        role.delete = AsyncMock()
        guild.get_role = Mock(return_value=role)
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.role_create, target=Mock(id=55)))
        role.delete.assert_called_once()
        
        channel = Mock()
        channel.name = "EvilChannel"
        channel.delete = AsyncMock()
        guild.get_channel = Mock(return_value=channel)
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.channel_create, target=Mock(id=66)))
        channel.delete.assert_called_once()
        
        webhook = Mock(id=77)
        webhook.name = "EvilWebhook"
        webhook.delete = AsyncMock()
        guild.webhooks = AsyncMock(return_value=[webhook])
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.webhook_create, target=Mock(id=77)))
        webhook.delete.assert_called_once()
        
        role.delete.side_effect = discord.Forbidden(Mock(), "test")
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.role_create, target=Mock(id=55)))

        role.delete.side_effect = Exception("Boom")
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.role_create, target=Mock(id=55)))

        # General loop exception line 94
        with patch.object(worker, 'bot', side_effect=Exception("Bot error")):
             await worker._process_entry(None)

    async def test_log_worker_full(self):
        """Test LogWorker branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        worker = sx.log_worker
        
        await worker.start()
        await worker.stop()
        
        entry_mock = Mock()
        worker.log_queue = Mock()
        worker.log_queue.get = AsyncMock(side_effect=[entry_mock, Exception("Log error"), asyncio.CancelledError])
        with patch.object(worker, '_process_entry', new_callable=AsyncMock) as mock_process:
            await worker._worker_loop()
            mock_process.assert_called_once()
        
        guild = Mock(id=777, owner_id=111)
        await worker._process_entry(Mock(user=Mock(id=123), guild=guild))
        await worker._process_entry(Mock(user=Mock(id=999), guild=guild, action=9999))
        
        sx._trigger_callbacks = AsyncMock()
        entry = Mock(user=Mock(id=999), guild=guild, action=discord.AuditLogAction.role_create, target=Mock(id=55), created_at=None)
        await worker._process_entry(entry)
        sx._trigger_callbacks.assert_called_once()
        
        sx._trigger_callbacks.side_effect = Exception("Callback error")
        await worker._process_entry(entry)

    async def test_guild_worker_full(self, tmp_path):
        """Test GuildWorker branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        
        tokens_file = tmp_path / "user_tokens.json"
        sx.backup_dir = tmp_path
        
        worker = sx.guild_worker
        worker._tokens_file = tokens_file

        # 0. Successful token load
        tokens_file.write_text(json.dumps({"123": "token123"}))
        await worker._load_tokens()
        assert worker.get_user_token(123) == "token123"

        # 1. start/stop
        await worker.start()
        await worker.stop()
        
        with patch("json.load", side_effect=Exception("JSON error")):
            tokens_file.write_text("{}")
            await worker._load_tokens()
            
        with patch("json.dump", side_effect=Exception("Dump error")):
            await worker._save_tokens()

        await worker.set_user_token(777, "token123")
        assert worker.get_user_token(777) == "token123"
        await worker.remove_user_token(777)
        assert worker.get_user_token(777) is None
        await worker.remove_user_token(999)

        entry_mock = Mock(action=discord.AuditLogAction.guild_update, user=Mock(id=999))
        entry_mock.changes = [Mock(key="name", before="Old", after="New")]
        worker.sdk.guild_queue = Mock()
        worker.sdk.guild_queue.get = AsyncMock(side_effect=[
            Mock(action=discord.AuditLogAction.ban),
            Mock(action=discord.AuditLogAction.guild_update, user=Mock(id=123)),
            Mock(action=discord.AuditLogAction.guild_update, user=Mock(id=999), changes=[]),
            entry_mock,
            Exception("Loop error"),
            asyncio.CancelledError
        ])
        with patch.object(worker, '_restore_guild_settings', new_callable=AsyncMock) as mock_restore:
            await worker._restoration_loop()
            assert mock_restore.call_count == 2

        assert await worker._restore_vanity_via_api(777, "vanity") is False
        await worker.set_user_token(777, "token123")
        
        with patch("aiohttp.ClientSession.patch") as mock_patch:
            mock_resp = MagicMock()
            mock_resp.status = 200
            mock_patch.return_value.__aenter__.return_value = mock_resp
            
            assert await worker._restore_vanity_via_api(777, "vanity") is True
            
            mock_resp.status = 400
            mock_resp.text = AsyncMock(return_value="error")
            assert await worker._restore_vanity_via_api(777, "vanity") is False
            
            mock_patch.side_effect = Exception("Network error")
            assert await worker._restore_vanity_via_api(777, "vanity") is False

        guild = Mock(spec=discord.Guild)
        guild.id = 777
        guild.edit = AsyncMock()
        
        sx.backup_manager.get_guild_settings = AsyncMock(return_value=None)
        await worker._restore_guild_settings(guild)
        
        backup = {
            "name": "Old",
            "vanity_url_code": "old-v",
            "icon": "icon-data",
            "banner": "banner-data",
            "description": "desc"
        }
        sx.backup_manager.get_guild_settings = AsyncMock(return_value=backup)
        
        changes = {
            "vanity_url_code": ("old-v", "new-v"),
            "name": ("Old", "New"),
            "icon": ("h1", "h2"),
            "banner": ("b1", "b2"),
            "description": ("d1", "d2")
        }
        
        with patch.object(worker, '_restore_vanity_via_api', return_value=True):
            await worker._restore_guild_settings(guild)
            guild.edit.assert_called_once()
            
        # Vanity fail branch
        with patch.object(worker, '_restore_vanity_via_api', return_value=False):
            await worker._restore_guild_settings(guild)

        guild.edit.side_effect = discord.HTTPException(Mock(status=400), "Bad request")
        await worker._restore_guild_settings(guild)
        
        mock_resp = Mock(status=400)
        ex = discord.HTTPException(mock_resp, "err")
        ex.code = 50035
        guild.edit.side_effect = ex
        await worker._restore_guild_settings(guild)
        
        guild.edit.side_effect = Exception("Critical fail")
        await worker._restore_guild_settings(guild)
    
    async def test_guild_worker_owner_and_whitelist_checks(self, tmp_path):
        """Test guild worker skips restoration for owner and whitelisted users (lines 101, 105)"""
        from securex import SecureX
        import discord
        
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot, backup_dir=str(tmp_path))
        
        # Set up caches
        sx.whitelist_cache = {777: {888}}  # User 888 is whitelisted
        sx.backup_dir = tmp_path
        sx.backup_manager.get_guild_settings = AsyncMock(return_value=None)
        
        worker = sx.guild_worker
        
        # Test 1: Guild owner makes change (should skip - line 101)
        entry1 = Mock()
        entry1.action = discord.AuditLogAction.guild_update
        entry1.user = Mock(id=999)  # Owner ID
        entry1.guild = Mock(id=777, owner_id=999)  # Same as executor
        entry1.changes = [Mock()]
        
        # Create test entries
        sx.guild_queue.get = AsyncMock(side_effect=[entry1, asyncio.CancelledError])
        
        # Run worker - should exit without calling restore
        try:
            await worker._restoration_loop()
        except asyncio.CancelledError:
            pass
        
        # Should not have attempted restoration (owner check on line 101)
        sx.backup_manager.get_guild_settings.assert_not_called()
        
        # Test 2: Whitelisted user makes change (should skip - line 105)
        sx.backup_manager.get_guild_settings.reset_mock()
        entry2 = Mock()
        entry2.action = discord.AuditLogAction.guild_update
        entry2.user = Mock(id=888)  # Whitelisted user
        entry2.guild = Mock(id=777, owner_id=999)  # Different owner
        entry2.changes = [Mock()]
        
        sx.guild_queue.get = AsyncMock(side_effect=[entry2, asyncio.CancelledError])
        
        try:
            await worker._restoration_loop()
        except asyncio.CancelledError:
            pass
        
        # Should not have attempted restoration (whitelist check on line 105)
        sx.backup_manager.get_guild_settings.assert_not_called()
