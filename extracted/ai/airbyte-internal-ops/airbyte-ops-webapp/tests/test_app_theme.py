"""Tests for Airbyte Ops Webapp UI theme settings."""

import pytest

from airbyte_ops_webapp import theme as theme_module
from airbyte_ops_webapp.theme import PANEL_CARD_CLASS, AbCard


def test_theme_defaults_to_dark(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(theme_module.THEME_MODE_ENV_VAR, raising=False)

    assert theme_module._theme_mode() == "dark"
    assert "dark" in theme_module._app_root_class().split()


def test_theme_can_follow_system_preference(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(theme_module.THEME_MODE_ENV_VAR, "system")

    assert theme_module._theme_mode() is None


def test_logo_svgs_use_transparent_backgrounds() -> None:
    assert "<rect" not in theme_module._airbyte_logo_svg_for_light_bg()
    assert "<rect" not in theme_module._airbyte_logo_svg_for_dark_bg()
    assert "#615EFF" in theme_module._airbyte_logo_svg_for_dark_bg()


def test_ab_component_applies_defaults_without_caller_props() -> None:
    card = AbCard()

    assert card.css_class == PANEL_CARD_CLASS
    assert card.style["padding"] == "1rem"
    assert "background" in card.style


def test_ab_component_merges_defaults_under_caller_props() -> None:
    card = AbCard(css_class="mt-4", style={"padding": "0"})

    # Semantic class is prepended; caller class is preserved after it.
    assert card.css_class == f"{PANEL_CARD_CLASS} mt-4"
    # Caller wins on conflicting keys, but non-conflicting defaults remain.
    assert card.style["padding"] == "0"
    assert "background" in card.style
