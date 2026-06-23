"""Tests for the telemetry remote-config download behaviour."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from tabpfn_common_utils.telemetry.core import config as config_module


@pytest.fixture(autouse=True)
def _clear_ttl_cache():
    """Clear the lru_cache on download_config between tests.

    download_config is wrapped by @ttl_cache (which itself uses functools.lru_cache).
    functools.wraps preserves the underlying cached callable as __wrapped__, so we
    can clear it directly to ensure each test sees a fresh fetch.
    """
    config_module.download_config.__wrapped__.cache_clear()  # type: ignore[attr-defined]
    yield
    config_module.download_config.__wrapped__.cache_clear()  # type: ignore[attr-defined]


def _mock_response(status_code: int, json_payload=None, raise_on_json: bool = False):
    resp = MagicMock(spec=requests.Response)
    resp.status_code = status_code
    if raise_on_json:
        resp.json.side_effect = ValueError("not json")
    else:
        resp.json.return_value = json_payload
    return resp


def test_download_config_returns_payload_on_200():
    payload = {"enabled": True, "sampling_rate": 0.5}
    with patch.object(
        config_module.requests, "get", return_value=_mock_response(200, payload)
    ):
        assert config_module.download_config() == payload


def test_download_config_fails_closed_on_network_exception():
    """If requests.get raises (timeout, DNS, firewall, etc.), default to disabled."""
    with patch.object(
        config_module.requests,
        "get",
        side_effect=requests.exceptions.ConnectionError("boom"),
    ):
        assert config_module.download_config() == {"enabled": False}


def test_download_config_fails_closed_on_timeout():
    with patch.object(
        config_module.requests, "get", side_effect=requests.exceptions.Timeout("slow")
    ):
        assert config_module.download_config() == {"enabled": False}


@pytest.mark.parametrize("status", [403, 404, 500, 503])
def test_download_config_fails_closed_on_non_200(status: int):
    with patch.object(
        config_module.requests,
        "get",
        return_value=_mock_response(status, {"enabled": True}),
    ):
        assert config_module.download_config() == {"enabled": False}


def test_download_config_fails_closed_on_invalid_json():
    """If the body isn't parseable JSON, default to disabled."""
    with patch.object(
        config_module.requests,
        "get",
        return_value=_mock_response(200, raise_on_json=True),
    ):
        assert config_module.download_config() == {"enabled": False}


@pytest.mark.parametrize(
    "payload",
    [
        [1, 2, 3],  # list
        "enabled",  # string
        42,  # int
        None,  # null
        {"foo": "bar"},  # dict missing "enabled"
        {},  # empty dict
    ],
)
def test_download_config_fails_closed_on_malformed_shape(payload):
    """If the JSON parses but isn't a dict with an 'enabled' key, default to disabled."""
    with patch.object(
        config_module.requests, "get", return_value=_mock_response(200, payload)
    ):
        assert config_module.download_config() == {"enabled": False}


def test_download_config_uses_env_override(monkeypatch):
    """Respects TABPFN_TELEMETRY_CONFIG_URL when set."""
    monkeypatch.setenv("TABPFN_TELEMETRY_CONFIG_URL", "https://example.test/cfg.json")
    with patch.object(
        config_module.requests,
        "get",
        return_value=_mock_response(200, {"enabled": True}),
    ) as mock_get:
        config_module.download_config()
        called_url = (
            mock_get.call_args.args[0]
            if mock_get.call_args.args
            else mock_get.call_args.kwargs.get("url")
        )
        assert called_url == "https://example.test/cfg.json"
