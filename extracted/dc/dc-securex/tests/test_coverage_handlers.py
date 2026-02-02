import pytest
import asyncio
import discord
from datetime import datetime, timezone, timedelta
from securex import SecureX
from unittest.mock import Mock, AsyncMock, patch, MagicMock

class MockAuditLog:
    def __init__(self, entries):
        self.entries = entries
    def __aiter__(self):
        return self
    async def __anext__(self):
        if not self.entries:
            raise StopAsyncIteration
        return self.entries.pop(0)

@pytest.mark.asyncio
class TestHandlersExhaustive:
    """Exhaustive tests for securex/handlers/ to reach 100% coverage"""

    async def test_channel_handler_full(self):
        """Test ChannelHandler branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        handler = sx.channel_handler
        
        guild = Mock(spec=discord.Guild)
        guild.id = 777
        guild.owner_id = 111
        
        # 1. _is_authorized branches
        sx.whitelist.is_whitelisted = AsyncMock(return_value=True)
        assert await handler._is_authorized(guild, 111) is True # Owner
        assert await handler._is_authorized(guild, 123) is True # Bot
        assert await handler._is_authorized(guild, 888) is True # Whitelisted
        
        sx.whitelist.is_whitelisted.return_value = False
        assert await handler._is_authorized(guild, 999) is False # Not whitelisted

        # 2. on_channel_delete branches
        channel = Mock(spec=discord.TextChannel)
        channel.guild = guild
        channel.id = 555
        channel.name = "test-channel"
        
        with patch.object(sx.backup_manager, 'restore_channel', new_callable=AsyncMock) as mock_restore:
            # A. Authorized deletion (Owner)
            entry_auth = Mock()
            entry_auth.target.id = 555
            entry_auth.user = Mock()
            entry_auth.user.id = 111 # Owner
            entry_auth.user.name = "Owner"
            entry_auth.created_at = datetime.now(timezone.utc)
            guild.audit_logs.return_value = MockAuditLog([entry_auth])
            await handler.on_channel_delete(channel)
            mock_restore.assert_not_called()

            # B. Authorized deletion (Bot)
            entry_bot = Mock()
            entry_bot.target.id = 555
            entry_bot.user = Mock()
            entry_bot.user.id = 123 # Bot
            entry_bot.created_at = datetime.now(timezone.utc)
            guild.audit_logs.return_value = MockAuditLog([entry_bot])
            await handler.on_channel_delete(channel)
            mock_restore.assert_not_called()

            # C. Unauthorized deletion (Success)
            entry_unauth = Mock()
            entry_unauth.target.id = 555
            entry_unauth.user = Mock()
            entry_unauth.user.id = 999
            entry_unauth.user.name = "Violator"
            entry_unauth.created_at = datetime.now(timezone.utc)
            guild.audit_logs.return_value = MockAuditLog([entry_unauth])
            mock_restore.return_value = Mock()
            await handler.on_channel_delete(channel)
            mock_restore.assert_called_once()
            mock_restore.reset_mock()
            
            # D. Category channel restoration
            category = Mock(spec=discord.CategoryChannel)
            category.guild = guild
            category.id = 666
            category.name = "Test Category"
            entry_cat = Mock()
            entry_cat.target.id = 666
            entry_cat.user = Mock()
            entry_cat.user.id = 999
            entry_cat.created_at = datetime.now(timezone.utc)
            guild.audit_logs.return_value = MockAuditLog([entry_cat])
            new_cat = Mock()
            mock_restore.return_value = new_cat
            with patch.object(sx.backup_manager, 'restore_category_children', new_callable=AsyncMock) as mock_cat:
                await handler.on_channel_delete(category)
                mock_cat.assert_called_once()

        # E. Too old entry
        entry_old = Mock()
        entry_old.created_at = datetime.now(timezone.utc) - timedelta(seconds=60)
        guild.audit_logs.return_value = MockAuditLog([entry_old])
        await handler.on_channel_delete(channel)

        # F. Entry not found
        guild.audit_logs.return_value = MockAuditLog([])
        await handler.on_channel_delete(channel)

        # G. Exception path
        guild.audit_logs.side_effect = Exception("Audit Log Error")
        await handler.on_channel_delete(channel)

        # 3. on_channel_update branches
        before, after = Mock(), Mock()
        after.guild = guild
        after.id = 555
        
        # No change
        before.overwrites = {"a": 1}
        after.overwrites = {"a": 1}
        before.position = 1
        after.position = 1
        guild.audit_logs.side_effect = None
        await handler.on_channel_update(before, after)
        
        # Unauthorized update
        after.overwrites = {"a": 2}
        entry_upd = Mock()
        entry_upd.action = discord.AuditLogAction.channel_update
        entry_upd.target.id = 555
        entry_upd.user = Mock()
        entry_upd.user.id = 999
        entry_upd.created_at = datetime.now(timezone.utc)
        guild.audit_logs.return_value = MockAuditLog([entry_upd])
        with patch.object(sx.backup_manager, 'restore_channel_permissions', new_callable=AsyncMock) as mock_upd:
            await handler.on_channel_update(before, after)
            mock_upd.assert_called_once()
            
            # Too old in update
            entry_upd.created_at = datetime.now(timezone.utc) - timedelta(seconds=60)
            guild.audit_logs.return_value = MockAuditLog([entry_upd])
            await handler.on_channel_update(before, after)

        # Exception update
        guild.audit_logs.side_effect = Exception("Audit Log Error")
        await handler.on_channel_update(before, after)

    async def test_role_handler_full(self):
        """Test RoleHandler branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        handler = sx.role_handler
        
        guild = Mock(spec=discord.Guild)
        guild.id = 777
        guild.owner_id = 111
        
        # 1. _is_authorized
        sx.whitelist.is_whitelisted = AsyncMock(return_value=False)
        assert await handler._is_authorized(guild, 111) is True # Owner
        assert await handler._is_authorized(guild, 123) is True # Bot

        # 2. on_role_delete
        role = Mock(spec=discord.Role)
        role.guild = guild
        role.id = 444
        role.name = "test-role"
        
        entry = Mock()
        entry.target.id = 444
        entry.user = Mock()
        entry.user.id = 999
        entry.created_at = datetime.now(timezone.utc)
        guild.audit_logs.return_value = MockAuditLog([entry])
        
        with patch.object(sx.backup_manager, 'restore_role', new_callable=AsyncMock) as mock_rest:
            mock_rest.return_value = True
            await handler.on_role_delete(role)
            mock_rest.assert_called_once()
            
            # too old
            entry.created_at = datetime.now(timezone.utc) - timedelta(seconds=60)
            guild.audit_logs.return_value = MockAuditLog([entry])
            await handler.on_role_delete(role)

        # Exception
        guild.audit_logs.side_effect = Exception("Audit error")
        await handler.on_role_delete(role)

        # 3. on_role_update
        before, after = Mock(), Mock()
        after.guild = guild
        after.id = 444
        after.name = "Role"
        before.position = 1
        after.position = 1
        before.permissions = discord.Permissions(0)
        after.permissions = discord.Permissions(8)
        
        entry_upd = Mock()
        entry_upd.action = discord.AuditLogAction.role_update
        entry_upd.target.id = 444
        entry_upd.user = Mock()
        entry_upd.user.id = 999
        entry_upd.created_at = datetime.now(timezone.utc)
        guild.audit_logs.side_effect = None
        guild.audit_logs.return_value = MockAuditLog([entry_upd])
        
        with patch.object(sx.backup_manager, 'restore_role_permissions', new_callable=AsyncMock) as mock_upd:
            mock_upd.return_value = True
            await handler.on_role_update(before, after)
            mock_upd.assert_called_once()
            
            # too old
            entry_upd.created_at = datetime.now(timezone.utc) - timedelta(seconds=60)
            guild.audit_logs.return_value = MockAuditLog([entry_upd])
            await handler.on_role_update(before, after)

            # No positional/perm change
            after.permissions = before.permissions
            await handler.on_role_update(before, after)

        # Exception in update - make audit_logs raise during iteration
        after.permissions = discord.Permissions(8)  # Change permissions again
        
        class ExceptionIterator:
            def __init__(self):
                pass
            def __aiter__(self):
                return self
            async def __anext__(self):
                raise Exception("Audit log iteration error")
        
        guild.audit_logs.side_effect = None
        guild.audit_logs.return_value = ExceptionIterator()
        await handler.on_role_update(before, after)

    async def test_member_handler_full(self):
        """Test MemberHandler branches for 100% coverage"""
        bot = Mock(spec=discord.Client)
        bot.user = Mock(id=123)
        sx = SecureX(bot)
        handler = sx.member_handler
        
        guild = Mock(spec=discord.Guild)
        guild.id = 777
        guild.owner_id = 111
        
        # _is_authorized
        sx.whitelist.is_whitelisted = AsyncMock(return_value=False)
        assert await handler._is_authorized(guild, 111) is True
        assert await handler._is_authorized(guild, 123) is True

        user = Mock(spec=discord.User)
        user.id = 222
        user.name = "Victim"
        
        # on_member_ban
        entry = Mock()
        entry.target.id = 222
        entry.user = Mock()
        entry.user.id = 999
        entry.created_at = datetime.now(timezone.utc)
        guild.audit_logs.return_value = MockAuditLog([entry])
        guild.unban = AsyncMock()
        
        await handler.on_member_ban(guild, user)
        guild.unban.assert_called_once()
        
        # entry not found (line 68 coverage)
        guild.audit_logs.return_value = MockAuditLog([])
        await handler.on_member_ban(guild, user)
        
        # too old
        entry.created_at = datetime.now(timezone.utc) - timedelta(seconds=60)
        guild.audit_logs.return_value = MockAuditLog([entry])
        await handler.on_member_ban(guild, user)
        
        # unban failure (Forbidden)
        entry.created_at = datetime.now(timezone.utc)
        guild.audit_logs.return_value = MockAuditLog([entry])
        guild.unban.side_effect = discord.Forbidden(Mock(), "test")
        await handler.on_member_ban(guild, user) 

        # Exception
        guild.audit_logs.side_effect = Exception("audit error")
        await handler.on_member_ban(guild, user)

        # on_member_update
        before, after = Mock(), Mock()
        after.guild = guild
        after.id = 222
        after.name = "Victim"
        
        role_def = Mock(spec=discord.Role)
        role_def.is_default = Mock(return_value=True) # Line 90 branch
        
        role_dang = Mock(spec=discord.Role)
        role_dang.is_default = Mock(return_value=False)
        role_dang.permissions = discord.Permissions(administrator=True)
        role_dang.name = "AdminRole"
        
        before.roles = []
        after.roles = [role_def, role_dang]
        
        entry_upd = Mock()
        entry_upd.action = discord.AuditLogAction.member_role_update
        entry_upd.target.id = 222
        entry_upd.user = Mock()
        entry_upd.user.id = 999
        entry_upd.created_at = datetime.now(timezone.utc)
        guild.audit_logs.side_effect = None
        guild.audit_logs.return_value = MockAuditLog([entry_upd])
        
        after.remove_roles = AsyncMock()
        await handler.on_member_update(before, after)
        after.remove_roles.assert_called_once_with(role_dang, reason="SecureX: Removed dangerous roles (unauthorized update)")
        
        # remove_roles failure (Exception path line 106)
        after.remove_roles.reset_mock()
        after.remove_roles.side_effect = discord.HTTPException(Mock(status=400), "Fail")
        guild.audit_logs.return_value = MockAuditLog([entry_upd])
        await handler.on_member_update(before, after)
        
        # too old update
        entry_upd.created_at = datetime.now(timezone.utc) - timedelta(seconds=60)
        guild.audit_logs.return_value = MockAuditLog([entry_upd])
        await handler.on_member_update(before, after)

        # Exception in member update
        guild.audit_logs.side_effect = Exception("member error")
        await handler.on_member_update(before, after)
        
        # Test roles unchanged (covers line 68)
        before.roles = [role_def, role_dang]
        after.roles = [role_def, role_dang]  # Same roles
        guild.audit_logs.side_effect = None
        await handler.on_member_update(before, after)

