"""Tests for Airbyte Ops Webapp UI theme settings."""

import pytest

from airbyte_ops_webapp import theme as theme_module


def test_theme_defaults_to_dark(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(theme_module.THEME_MODE_ENV_VAR, raising=False)

    assert theme_module._theme_mode() == "dark"


def test_theme_can_follow_system_preference(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(theme_module.THEME_MODE_ENV_VAR, "system")

    assert theme_module._theme_mode() is None


def test_logo_svgs_use_transparent_backgrounds() -> None:
    assert "<rect" not in theme_module._airbyte_logo_svg_for_light_bg()
    assert "<rect" not in theme_module._airbyte_logo_svg_for_dark_bg()
    assert "#615EFF" in theme_module._airbyte_logo_svg_for_dark_bg()
