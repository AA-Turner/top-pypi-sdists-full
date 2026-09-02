"""Tests for load_credentials."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import (
    BrowserCredentialError,
    BrowserCredentials,
    load_credentials,
)


class TestLoadCredentials:
    """Tests for load_credentials."""

    def test_loads_literal_values(self, tmp_path) -> None:
        path = tmp_path / "creds.json"
        path.write_text(
            json.dumps({"username": "u", "password": "p", "2fa_secret": "s"}),
            encoding="utf-8",
        )
        creds = load_credentials(path)
        assert creds == BrowserCredentials(username="u", password="p", totp_secret="s")

    def test_uses_default_path_when_none(self, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
        path = tmp_path / "default.json"
        path.write_text(
            json.dumps({"username": "u", "password": "p", "2fa_secret": "s"}),
            encoding="utf-8",
        )
        monkeypatch.setattr(browser_apply_autofix, "_default_credentials_path", lambda: path)
        creds = load_credentials(None)
        assert creds.username == "u"

    def test_read_error_raises(self, tmp_path) -> None:
        missing = tmp_path / "nope.json"
        with pytest.raises(BrowserCredentialError, match="Cannot read"):
            load_credentials(missing)

    def test_invalid_json_raises(self, tmp_path) -> None:
        path = tmp_path / "bad.json"
        path.write_text("{not json", encoding="utf-8")
        with pytest.raises(BrowserCredentialError, match="Invalid JSON"):
            load_credentials(path)

    def test_non_object_json_raises(self, tmp_path) -> None:
        path = tmp_path / "bad-shape.json"
        path.write_text(json.dumps([]), encoding="utf-8")
        with pytest.raises(BrowserCredentialError, match="must contain a JSON object"):
            load_credentials(path)

    def test_missing_field_raises(self, tmp_path) -> None:
        path = tmp_path / "missing.json"
        path.write_text(json.dumps({"username": "u", "password": "p"}), encoding="utf-8")
        with pytest.raises(BrowserCredentialError, match="Missing credential field"):
            load_credentials(path)
