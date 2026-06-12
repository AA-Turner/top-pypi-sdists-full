"""Tests for smplkit.account.models — account-settings active-record models."""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock

import pytest

from smplkit.account.models import AccountSettings, AsyncAccountSettings, _AccountSettingsBase


# ---------------------------------------------------------------------------
# _AccountSettingsBase / AccountSettings / AsyncAccountSettings
# ---------------------------------------------------------------------------


class TestAccountSettingsBase:
    def test_default_init(self):
        settings = _AccountSettingsBase.__new__(_AccountSettingsBase)
        _AccountSettingsBase.__init__(settings)
        assert settings._data == {}

    def test_init_with_data(self):
        settings = _AccountSettingsBase.__new__(_AccountSettingsBase)
        _AccountSettingsBase.__init__(settings, data={"environment_order": ["prod", "staging"]})
        assert settings._data == {"environment_order": ["prod", "staging"]}

    def test_raw_getter(self):
        settings = AccountSettings(data={"foo": "bar"})
        assert settings.raw == {"foo": "bar"}

    def test_raw_setter(self):
        settings = AccountSettings(data={"foo": "bar"})
        settings.raw = {"baz": "qux"}
        assert settings._data == {"baz": "qux"}

    def test_environment_order_getter_empty(self):
        settings = AccountSettings()
        assert settings.environment_order == []

    def test_environment_order_getter_with_value(self):
        settings = AccountSettings(data={"environment_order": ["prod", "staging"]})
        assert settings.environment_order == ["prod", "staging"]

    def test_environment_order_setter(self):
        settings = AccountSettings()
        settings.environment_order = ["prod", "staging", "dev"]
        assert settings._data["environment_order"] == ["prod", "staging", "dev"]

    def test_repr(self):
        settings = AccountSettings(data={"foo": 1})
        r = repr(settings)
        assert "AccountSettings" in r

    def test_apply(self):
        s1 = AccountSettings(data={"foo": 1})
        s2 = AccountSettings(data={"bar": 2})
        s1._apply(s2)
        assert s1._data == {"bar": 2}


class TestAccountSettingsSave:
    def test_save_no_client_raises(self):
        settings = AccountSettings(data={"foo": 1})
        with pytest.raises(RuntimeError, match="without a client"):
            settings.save()

    def test_save_calls_client_save(self):
        mock_client = MagicMock()
        updated = AccountSettings(mock_client, data={"environment_order": ["prod"]})
        mock_client._save.return_value = updated
        settings = AccountSettings(mock_client, data={"environment_order": []})
        settings.save()
        mock_client._save.assert_called_once_with({"environment_order": []})
        assert settings._data == {"environment_order": ["prod"]}


class TestAsyncAccountSettingsSave:
    def test_save_no_client_raises(self):
        settings = AsyncAccountSettings(data={"foo": 1})
        with pytest.raises(RuntimeError, match="without a client"):
            asyncio.run(settings.save())

    def test_save_calls_client_save(self):
        async def _run():
            mock_client = MagicMock()
            updated = AsyncAccountSettings(mock_client, data={"environment_order": ["prod"]})

            async def fake_save(data):
                return updated

            mock_client._save = fake_save
            settings = AsyncAccountSettings(mock_client, data={})
            await settings.save()
            assert settings._data == {"environment_order": ["prod"]}

        asyncio.run(_run())
