"""Tests for smplkit.account._client — account settings sync + async sub-clients."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from smplkit.account._client import AsyncSettingsClient, SettingsClient
from smplkit.account.models import AccountSettings, AsyncAccountSettings


# ---------------------------------------------------------------------------
# SettingsClient (sync)
# ---------------------------------------------------------------------------


class Test_SettingsClient:
    def _make_client(self):
        return SettingsClient("http://app:8000", "sk_test")

    def test_get(self):
        with patch("smplkit.account._client.httpx.Client") as MockClient:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b'{"environment_order":["prod"]}'
            mock_resp.json.return_value = {"environment_order": ["prod"]}
            MockClient.return_value.__enter__.return_value.get.return_value = mock_resp
            client = self._make_client()
            settings = client.get()
            assert isinstance(settings, AccountSettings)
            assert settings.environment_order == ["prod"]

    def test_get_empty_response(self):
        with patch("smplkit.account._client.httpx.Client") as MockClient:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"null"
            mock_resp.json.return_value = None
            MockClient.return_value.__enter__.return_value.get.return_value = mock_resp
            client = self._make_client()
            settings = client.get()
            assert settings._data == {}

    def test_save(self):
        with patch("smplkit.account._client.httpx.Client") as MockClient:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b'{"environment_order":["prod","staging"]}'
            mock_resp.json.return_value = {"environment_order": ["prod", "staging"]}
            MockClient.return_value.__enter__.return_value.put.return_value = mock_resp
            client = self._make_client()
            result = client._save({"environment_order": ["prod", "staging"]})
            assert isinstance(result, AccountSettings)
            assert result.environment_order == ["prod", "staging"]

    def test_save_empty_response(self):
        with patch("smplkit.account._client.httpx.Client") as MockClient:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"null"
            mock_resp.json.return_value = None
            MockClient.return_value.__enter__.return_value.put.return_value = mock_resp
            client = self._make_client()
            result = client._save({})
            assert result._data == {}


# ---------------------------------------------------------------------------
# AsyncSettingsClient
# ---------------------------------------------------------------------------


class Test_AsyncSettingsClient:
    def _make_client(self):
        return AsyncSettingsClient("http://app:8000", "sk_test")

    def test_get(self):
        async def _run():
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b'{"environment_order":["prod"]}'
            mock_resp.json.return_value = {"environment_order": ["prod"]}

            async_ctx = AsyncMock()
            async_ctx.__aenter__ = AsyncMock(return_value=async_ctx)
            async_ctx.__aexit__ = AsyncMock(return_value=False)
            async_ctx.get = AsyncMock(return_value=mock_resp)

            with patch("smplkit.account._client.httpx.AsyncClient", return_value=async_ctx):
                client = self._make_client()
                settings = await client.get()
                assert isinstance(settings, AsyncAccountSettings)
                assert settings.environment_order == ["prod"]

        asyncio.run(_run())

    def test_get_empty_response(self):
        async def _run():
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"null"
            mock_resp.json.return_value = None

            async_ctx = AsyncMock()
            async_ctx.__aenter__ = AsyncMock(return_value=async_ctx)
            async_ctx.__aexit__ = AsyncMock(return_value=False)
            async_ctx.get = AsyncMock(return_value=mock_resp)

            with patch("smplkit.account._client.httpx.AsyncClient", return_value=async_ctx):
                client = self._make_client()
                settings = await client.get()
                assert settings._data == {}

        asyncio.run(_run())

    def test_save(self):
        async def _run():
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b'{"environment_order":["prod","staging"]}'
            mock_resp.json.return_value = {"environment_order": ["prod", "staging"]}

            async_ctx = AsyncMock()
            async_ctx.__aenter__ = AsyncMock(return_value=async_ctx)
            async_ctx.__aexit__ = AsyncMock(return_value=False)
            async_ctx.put = AsyncMock(return_value=mock_resp)

            with patch("smplkit.account._client.httpx.AsyncClient", return_value=async_ctx):
                client = self._make_client()
                result = await client._save({"environment_order": ["prod", "staging"]})
                assert isinstance(result, AsyncAccountSettings)
                assert result.environment_order == ["prod", "staging"]

        asyncio.run(_run())

    def test_save_empty_response(self):
        async def _run():
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.content = b"null"
            mock_resp.json.return_value = None

            async_ctx = AsyncMock()
            async_ctx.__aenter__ = AsyncMock(return_value=async_ctx)
            async_ctx.__aexit__ = AsyncMock(return_value=False)
            async_ctx.put = AsyncMock(return_value=mock_resp)

            with patch("smplkit.account._client.httpx.AsyncClient", return_value=async_ctx):
                client = self._make_client()
                result = await client._save({})
                assert result._data == {}

        asyncio.run(_run())
