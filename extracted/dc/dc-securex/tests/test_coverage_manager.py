import pytest
import asyncio
import discord
import os
import json
from datetime import datetime, timezone, timedelta
from securex import SecureX
from securex.backup.manager import BackupManager
from securex.models import BackupInfo
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from types import SimpleNamespace

@pytest.mark.asyncio
class TestManagerFinalBoss:
    """Comprehensive manager tests for maximum coverage"""

    async def test_comprehensive_coverage(self, tmp_path):
        """Complete test covering all BackupManager functionality"""
        bot = MagicMock()
        bot.is_closed.return_value = True
        bot.wait_until_ready = AsyncMock()
        bot.user = MagicMock(id=123, name="Bot")
        
        sx = SecureX(bot, backup_dir=str(tmp_path))
        manager = sx.backup_manager
        
        def make_role(id, name, pos=0, is_def=False):
            r = MagicMock(spec=discord.Role)
            r.id = id; r.name = name; r.position = pos
            r.is_default.return_value = is_def
            r.managed = False; r.hoist = True; r.mentionable = True
            r.color = SimpleNamespace(value=0xFF)
            r.permissions = SimpleNamespace(value=8)
            r.__hash__.return_value = id
            r.__eq__ = lambda s, o: getattr(o, 'id', None) == id
            r.edit = AsyncMock()
            return r

        def make_chan(id, name, type, cat=None):
            c = MagicMock(spec=discord.abc.GuildChannel)
            if type == discord.ChannelType.text:
                c = MagicMock(spec=discord.TextChannel)
                c.topic = "t"; c.nsfw = False; c.slowmode_delay = 0
            elif type == discord.ChannelType.voice:
                c = MagicMock(spec=discord.VoiceChannel)
                c.bitrate = 64000; c.user_limit = 0
            elif type == discord.ChannelType.category:
                c = MagicMock(spec=discord.CategoryChannel)
            elif type == discord.ChannelType.stage_voice:
                c = MagicMock(spec=discord.StageChannel)
                c.bitrate = 64000
            c.id = id; c.name = name; c.type = type; c.position = 0; c.category = cat
            c.overwrites = {}
            c.__hash__.return_value = id
            c.__eq__ = lambda s, o: getattr(o, 'id', None) == id
            c.edit = AsyncMock()
            c.set_permissions = AsyncMock()
            return c

        guild = MagicMock(spec=discord.Guild)
        guild.id = 777; guild.name = "G"; guild.owner_id = 999
        guild.icon = None; guild.banner = None; guild.description = None; guild.vanity_url_code = "v"
        bot.get_guild.return_value = guild
        bot.guilds = [guild]
        
        r1 = make_role(1, "R1", 1)
        everyone = make_role(777, "@everyone", 0, True)
        guild.roles = [everyone, r1]
        
        cat1 = make_chan(10, "C1", discord.ChannelType.category)
        txt1 = make_chan(11, "T1", discord.ChannelType.text, cat1)
        voi1 = make_chan(12, "V1", discord.ChannelType.voice, cat1)
        stg1 = make_chan(13, "S1", discord.ChannelType.stage_voice, cat1)
        txt1.overwrites = {r1: discord.PermissionOverwrite(administrator=True)}
        guild.channels = [cat1, txt1, voi1, stg1]

        with patch("asyncio.sleep", AsyncMock()), patch("aiohttp.ClientSession.get") as mock_get:
            mock_resp = MagicMock(); mock_resp.read = AsyncMock(return_value=b"i"); mock_resp.status = 200
            mock_get.return_value.__aenter__.return_value = mock_resp
            
            # === CORE FLOW TESTS ===
            await manager.create_backup(guild.id)
            
            await manager.restore_channel(guild, make_chan(999, "X", discord.ChannelType.text))
            manager._channel_cache.pop(guild.id, None)
            guild.create_text_channel = AsyncMock(return_value=make_chan(111, "T", discord.ChannelType.text))
            guild.create_voice_channel = AsyncMock(return_value=make_chan(112, "V", discord.ChannelType.voice))
            guild.create_stage_channel = AsyncMock(return_value=make_chan(113, "S", discord.ChannelType.stage_voice))
            guild.create_category = AsyncMock(return_value=make_chan(114, "C", discord.ChannelType.category))
            guild.get_channel.return_value = None
            for cid, ctype in [(10, discord.ChannelType.category), (11, discord.ChannelType.text), (12, discord.ChannelType.voice), (13, discord.ChannelType.stage_voice)]:
                await manager.restore_channel(guild, make_chan(cid, "N", ctype))
            guild.create_text_channel.return_value.edit.side_effect = discord.Forbidden(Mock(), "F")
            await manager.restore_channel(guild, make_chan(11, "N", discord.ChannelType.text))
            guild.create_text_channel.return_value.edit.side_effect = None

            # Category children restoration
            with patch.object(manager, 'backup_dir', tmp_path / "empty"):
                await manager.restore_category_children(guild, 10, make_chan(105, "NC", discord.ChannelType.category))
            await manager.restore_category_children(guild, 99, make_chan(105, "NC", discord.ChannelType.category))
            cat_new = make_chan(105, "NC", discord.ChannelType.category)
            existing_same = make_chan(11, "E", discord.ChannelType.text, cat_new)
            guild.get_channel.side_effect = lambda cid: existing_same if cid == 11 else None
            await manager.restore_category_children(guild, 10, cat_new)
            cat_wrong = make_chan(999, "W", discord.ChannelType.category)
            existing_diff = make_chan(11, "E", discord.ChannelType.text, cat_wrong)
            guild.get_channel.side_effect = lambda cid: existing_diff if cid == 11 else None
            await manager.restore_category_children(guild, 10, cat_new)
            member1 = MagicMock(spec=discord.Member, id=888)
            member1.__hash__.return_value = 888
            guild.get_member.return_value = member1
            backup_file = manager.backup_dir / f"channels_{guild.id}.json"
            with open(backup_file, 'r') as f:
                data = json.load(f)
            data["channels"][1]["permissions"]["888"] = {"type": "member", "allow": 1, "deny": 0}
            with open(backup_file, 'w') as f:
                json.dump(data, f)
            manager._channel_cache.pop(guild.id, None)
            guild.get_channel.side_effect = None
            guild.get_channel.return_value = None
            await manager.restore_category_children(guild, 10, cat_new)
            guild.get_role.return_value = None
            guild.get_member.return_value = None
            await manager.restore_category_children(guild, 10, cat_new)
            guild.get_role.return_value = r1

            # Channel permissions
            guild.get_channel.return_value = make_chan(11, "T", discord.ChannelType.text)
            guild.get_channel.return_value.set_permissions = AsyncMock()
            await manager.restore_channel_permissions(guild, 11)
            guild.get_channel.return_value.set_permissions.side_effect = Exception("E")
            await manager.restore_channel_permissions(guild, 11)

            # Role restoration
            await manager.restore_role(guild, 999)
            guild.create_role = AsyncMock(return_value=make_role(101, "R", 5))
            guild.edit_role_positions = AsyncMock(side_effect=discord.Forbidden(Mock(), "F"))
            await manager.restore_role(guild, 1)
            guild.edit_role_positions.side_effect = Exception("E")
            await manager.restore_role(guild, 1)
            guild.edit_role_positions.side_effect = None

            # Role permissions
            guild.get_role.return_value = None
            await manager.restore_role_permissions(guild, 1)
            guild.get_role.return_value = r1
            await manager.restore_role_permissions(guild, 1)
            r1.edit.side_effect = Exception("E")
            await manager.restore_role_permissions(guild, 1)

            # Loops
            bot.is_closed.side_effect = [False, True]
            with patch.object(manager, 'create_backup', side_effect=Exception("L")):
                with patch.object(bot.loop, 'create_task') as mock_t:
                    manager.start_auto_backup()
                    await mock_t.call_args[0][0]
            with patch.object(manager, 'preload_all', AsyncMock()):
                 with patch("asyncio.sleep", side_effect=[None, asyncio.CancelledError]):
                      try:
                          await manager._auto_refresh_loop()
                      except asyncio.CancelledError:
                          pass

            # Misc operations
            await manager.update_guild_vanity(777, "NEW")
            await manager.get_guild_settings(777)
            with patch("builtins.open", side_effect=Exception("E")):
                 await manager._save_all_guild_settings()
            bot.get_guild.return_value = None
            await manager.create_backup(666)
            (tmp_path / "channels_999.json").write_text("invalid")
            await manager.preload_all()
            manager._guild_cache = {}
            await manager.update_guild_vanity(555, "V")
        
        # === EDGE CASE TESTS ===
        bot.guilds = []
        
        # Lock management
        lock1 = manager._get_guild_lock(999)
        lock2 = manager._get_guild_lock(999)
        assert lock1 is lock2
        lock3 = manager._get_guild_lock(888)
        assert lock3 is not lock1
        
        # Exception paths
        with patch.object(manager, '_backup_channels', side_effect=Exception("TEST")):
            result = await manager.create_backup(777)
            assert result.success is False
        
        # Auto-refresh task management
        manager._refresh_task = asyncio.create_task(asyncio.sleep(0))
        await asyncio.sleep(0.01)
        manager.start_auto_refresh()
        manager._refresh_task = None
        manager.start_auto_refresh()
        assert manager._refresh_task is not None
        manager._refresh_task.cancel()
        try:
            await manager._refresh_task
        except asyncio.CancelledError:
            pass
        
        # Refresh loop exception handling
        bot.guilds = [MagicMock(id=777)]
        with patch.object(manager, '_update_guild_cache', AsyncMock(side_effect=Exception("E"))):
            with patch("asyncio.sleep", side_effect=[None, asyncio.CancelledError]):
                try:
                    await manager._auto_refresh_loop()
                except asyncio.CancelledError:
                    pass
        
        # Guild settings loading
        (tmp_path / "guild_settings.json").write_text("invalid json")
        await manager._load_all_guild_settings()
        (tmp_path / "guild_settings.json").write_text('{"777": {"guild_id": 777, "vanity_url_code": "test"}}')
        await manager._load_all_guild_settings()
        assert 777 in manager._guild_cache
        
        # Vanity URL operations
        manager._guild_cache = {}
        vanity = await manager.get_guild_vanity(777)
        assert vanity == "test"
        vanity = await manager.get_guild_vanity(999)
        assert vanity is None
        with patch.object(manager, '_load_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            manager._guild_cache = {}
            vanity = await manager.get_guild_vanity(777)
            assert vanity is None
        manager._guild_cache[888] = {"vanity_url_code": "cached"}
        vanity = await manager.get_guild_vanity(888)
        assert vanity == "cached"
        
        # Guild settings operations
        manager._guild_cache[777] = {"guild_id": 777, "name": "Test"}
        settings = await manager.get_guild_settings(777)
        assert settings["name"] == "Test"
        manager._guild_cache = {}
        settings = await manager.get_guild_settings(777)
        assert settings["guild_id"] == 777
        settings = await manager.get_guild_settings(999)
        assert settings is None
        with patch.object(manager, '_load_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            manager._guild_cache = {}
            settings = await manager.get_guild_settings(777)
        
        # Exception handling
        with patch.object(manager, '_save_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            await manager.update_guild_vanity(888, "code")
        guild2 = MagicMock(spec=discord.Guild)
        guild2.id = 999; guild2.vanity_url_code = None; guild2.name = "Test"
        guild2.icon = None; guild2.banner = None; guild2.description = None
        with patch.object(manager, '_save_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            result = await manager._backup_guild_settings(guild2)
            assert result == {} or result.get("guild_id") == 999
        with patch("builtins.open", side_effect=Exception("E")):
            await manager._update_guild_cache(777)
        manager._cache_loaded = True
        await manager.preload_all()
        
        # Permission restoration edge cases
        guild2.get_channel = MagicMock(return_value=None)
        guild2.get_role = MagicMock(return_value=None)
        result = await manager.restore_channel_permissions(guild2, 123)
        assert result is False
        (tmp_path / "channels_999.json").write_text('{"channels": [{"id": 456, "permissions": {}}]}')
        result = await manager.restore_channel_permissions(guild2, 123)
        assert result is False
        (tmp_path / "channels_999.json").write_text('{"channels": [{"id": 123, "permissions": {}}]}')
        result = await manager.restore_channel_permissions(guild2, 123)
        assert result is False
        result = await manager.restore_role_permissions(guild2, 123)
        assert result is False
        (tmp_path / "roles_999.json").write_text('{"roles": [{"id": 456, "permissions": 8}]}')
        result = await manager.restore_role_permissions(guild2, 123)
        assert result is False
        (tmp_path / "roles_999.json").write_text('{"roles": [{"id": 123, "permissions": 8, "position": 5}]}')
        result = await manager.restore_role_permissions(guild2, 123)
        assert result is False
        role = make_role(123, "TestRole")
        guild2.get_role.return_value = role
        result = await manager.restore_role_permissions(guild2, 123)
        assert result is True
        role.edit.side_effect = Exception("E")
        result = await manager.restore_role_permissions(guild2, 123)
        assert result is False
        
        # Successful permission restoration
        perm_backup = {"channels": [{"id": 123, "permissions": {"456": {"type": "role", "allow": 8, "deny": 0}}}]}
        (tmp_path / "channels_999.json").write_text(json.dumps(perm_backup))
        chan = make_chan(123, "Test", discord.ChannelType.text)
        guild2.get_channel.return_value = chan
        test_role = make_role(456, "Role")
        guild2.get_role.return_value = test_role
        result = await manager.restore_channel_permissions(guild2, 123)
        assert result is True

    async def test_missing_coverage_edge_cases(self, tmp_path):
        """Test all remaining edge cases to hit 100% coverage"""
        bot = MagicMock()
        bot.is_closed.return_value = True
        bot.wait_until_ready = AsyncMock()
        bot.user = MagicMock(id=123, name="Bot")
        bot.guilds = []
        
        sx = SecureX(bot, backup_dir=str(tmp_path))
        manager = sx.backup_manager
        
        # Test _get_guild_lock creates new locks
        lock1 = manager._get_guild_lock(999)
        lock2 = manager._get_guild_lock(999)
        assert lock1 is lock2
        lock3 = manager._get_guild_lock(888)
        assert lock3 is not lock1
        
        # Test create_backup exception path
        with patch.object(manager, '_backup_channels', side_effect=Exception("TEST")):
            result = await manager.create_backup(777)
            assert result.success is False
        
        # Test start_auto_refresh when task already exists
        manager._refresh_task = asyncio.create_task(asyncio.sleep(0))
        await asyncio.sleep(0.01)
        manager.start_auto_refresh()
        
        # Test start_auto_refresh when task is None
        manager._refresh_task = None
        manager.start_auto_refresh()
        assert manager._refresh_task is not None
        manager._refresh_task.cancel()
        try:
            await manager._refresh_task
        except asyncio.CancelledError:
            pass
        
        # Test _auto_refresh_loop exception handling
        bot.guilds = [MagicMock(id=777)]
        with patch.object(manager, '_update_guild_cache', AsyncMock(side_effect=Exception("E"))):
            with patch("asyncio.sleep", side_effect=[None, asyncio.CancelledError]):
                try:
                    await manager._auto_refresh_loop()
                except asyncio.CancelledError:
                    pass
        
        # Test _load_all_guild_settings with invalid JSON
        (tmp_path / "guild_settings.json").write_text("invalid json")
        await manager._load_all_guild_settings()
        
        # Test _load_all_guild_settings when file exists with valid data
        (tmp_path / "guild_settings.json").write_text('{"777": {"guild_id": 777, "vanity_url_code": "test"}}')
        await manager._load_all_guild_settings()
        assert 777 in manager._guild_cache
        
        # Test get_guild_vanity when not in cache but in file
        manager._guild_cache = {}
        vanity = await manager.get_guild_vanity(777)
        assert vanity == "test"
        
        # Test get_guild_vanity when not found anywhere
        vanity = await manager.get_guild_vanity(999)
        assert vanity is None
        
        # Test get_guild_vanity exception handling
        with patch.object(manager, '_load_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            manager._guild_cache = {}
            vanity = await manager.get_guild_vanity(777)
            assert vanity is None
        
        # Test get_guild_settings when already in cache
        manager._guild_cache[777] = {"guild_id": 777, "name": "Test"}
        settings = await manager.get_guild_settings(777)
        assert settings["name"] == "Test"
        
        # Test get_guild_settings when not in cache but in file
        manager._guild_cache = {}
        settings = await manager.get_guild_settings(777)
        assert settings["guild_id"] == 777
        
        # Test get_guild_settings when not found
        settings = await manager.get_guild_settings(999)
        assert settings is None
        
        # Test get_guild_settings exception handling
        with patch.object(manager, '_load_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            manager._guild_cache = {}
            settings = await manager.get_guild_settings(777)
        
        # Test update_guild_vanity exception handling
        with patch.object(manager, '_save_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            await manager.update_guild_vanity(888, "code")
        
        # Test _backup_guild_settings exception handling
        guild = MagicMock(spec=discord.Guild)
        guild.id = 999
        guild.vanity_url_code = None
        guild.name = "Test"
        guild.icon = None
        guild.banner = None
        guild.description = None
        
        with patch.object(manager, '_save_all_guild_settings', AsyncMock(side_effect=Exception("E"))):
            result = await manager._backup_guild_settings(guild)
            assert result == {} or result.get("guild_id") == 999
        
        # Test _update_guild_cache exception handling
        with patch("builtins.open", side_effect=Exception("E")):
            await manager._update_guild_cache(777)
        
        # Test preload_all when already loaded
        manager._cache_loaded = True
        await manager.preload_all()
        
        # Test restore_channel_permissions with missing backup file
        guild = MagicMock(spec=discord.Guild)
        guild.id = 999
        result = await manager.restore_channel_permissions(guild, 123)
        assert result is False
        
        # Test restore_channel_permissions with missing channel data
        (tmp_path / "channels_999.json").write_text('{"channels": [{"id": 456, "permissions": {}}]}')
        result = await manager.restore_channel_permissions(guild, 123)
        assert result is False
        
        # Test restore_channel_permissions with missing channel
        (tmp_path / "channels_999.json").write_text('{"channels": [{"id": 123, "permissions": {}}]}')
        guild.get_channel.return_value = None
        result = await manager.restore_channel_permissions(guild, 123)
        assert result is False
        
        # Test restore_role_permissions with missing backup file
        result = await manager.restore_role_permissions(guild, 123)
        assert result is False
        
        # Test restore_role_permissions with missing role data
        (tmp_path / "roles_999.json").write_text('{"roles": [{"id": 456, "permissions": 8}]}')
        result = await manager.restore_role_permissions(guild, 123)
        assert result is False
        
        # Test restore_role_permissions with missing role
        (tmp_path / "roles_999.json").write_text('{"roles": [{"id": 123, "permissions": 8, "position": 5}]}')
        guild.get_role.return_value = None
        result = await manager.restore_role_permissions(guild, 123)
        assert result is False
        
        # Test restore_role_permissions successful path
        role = MagicMock(spec=discord.Role)
        role.edit = AsyncMock()
        guild.get_role.return_value = role
        result = await manager.restore_role_permissions(guild, 123)
        assert result is True
        
        # Test restore_role_permissions exception handling
        role.edit.side_effect = Exception("E")
        result = await manager.restore_role_permissions(guild, 123)
        assert result is False
        
        # Helper functions for additional tests
        def make_chan(id, name, type, cat=None):
            c = MagicMock(spec=discord.abc.GuildChannel)
            if type == discord.ChannelType.text:
                c = MagicMock(spec=discord.TextChannel)
                c.topic = "t"; c.nsfw = False; c.slowmode_delay = 0
            c.id = id; c.name = name; c.type = type; c.position = 0; c.category = cat
            c.overwrites = {}
            c.__hash__.return_value = id
            c.edit = AsyncMock()
            c.set_permissions = AsyncMock()
            return c
        
        def make_role(id, name):
            r = MagicMock(spec=discord.Role)
            r.id = id; r.name = name
            r.__hash__.return_value = id
            return r
        
        guild2 = MagicMock(spec=discord.Guild)
        guild2.id = 999
        guild2.get_channel = MagicMock(return_value=None)
        guild2.get_role = MagicMock(return_value=None)


        # Test restore_channel_permissions success path
        perm_backup = {
            "channels": [{
                "id": 123,
                "permissions": {
                    "456": {"type": "role", "allow": 8, "deny": 0}
                }
            }]
        }
        (tmp_path / f"channels_{guild.id}.json").write_text(json.dumps(perm_backup))
        
        chan = make_chan(123, "Test", discord.ChannelType.text)
        guild.get_channel.return_value = chan
        role = make_role(456, "Role")
        guild.get_role.return_value = role
        
        result = await manager.restore_channel_permissions(guild, 123)
        assert result is True
        
        # Test get_guild_vanity when in cache from start
        manager._guild_cache[888] = {"vanity_url_code": "cached"}
        vanity = await manager.get_guild_vanity(888)
        assert vanity == "cached"
