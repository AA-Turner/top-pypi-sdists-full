# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for `airbyte_ops_mcp.cloud_admin.registry_lookup`."""

from __future__ import annotations

import pytest
import requests
from airbyte.exceptions import PyAirbyteInputError

from airbyte_ops_mcp.cloud_admin import registry_lookup


class _FakeResponse:
    """Minimal stand-in for `requests.Response` used by the registry fetch."""

    def __init__(
        self,
        *,
        status_code: int = 200,
        json_error: bool = False,
        text: str = "",
    ) -> None:
        self.status_code = status_code
        self.text = text
        self._json_error = json_error

    def json(self) -> dict:
        if self._json_error:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return {"sources": [], "destinations": []}


@pytest.fixture(autouse=True)
def _clear_registry_cache() -> None:
    """Clear the TTL cache so each case triggers a fresh fetch."""
    registry_lookup._registry_cache.clear()


def test_fetch_cloud_registry_wraps_malformed_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        registry_lookup.requests,
        "get",
        lambda *_a, **_k: _FakeResponse(json_error=True),
    )
    with pytest.raises(PyAirbyteInputError, match="malformed JSON"):
        registry_lookup._fetch_cloud_registry()


def test_fetch_cloud_registry_wraps_non_200(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        registry_lookup.requests,
        "get",
        lambda *_a, **_k: _FakeResponse(status_code=503, text="upstream down"),
    )
    with pytest.raises(PyAirbyteInputError, match="non-200"):
        registry_lookup._fetch_cloud_registry()


def test_fetch_cloud_registry_wraps_request_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(*_a: object, **_k: object) -> _FakeResponse:
        raise requests.ConnectTimeout("timed out")

    monkeypatch.setattr(registry_lookup.requests, "get", _raise)
    with pytest.raises(PyAirbyteInputError, match="request failed"):
        registry_lookup._fetch_cloud_registry()
