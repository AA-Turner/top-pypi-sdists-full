"""Airbyte theme settings for the connector version manager."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from prefab_ui.themes import Theme

THEME_MODE_ENV_VAR = "AIRBYTE_OPS_WEBAPP_THEME_MODE"
AIRBYTE_ASSETS_DIR = Path(__file__).with_name("assets")
AIRBYTE_LOGO_FOR_LIGHT_BG_PATH = (
    AIRBYTE_ASSETS_DIR / "airbyte_logo_color_dark_transparent.svg"
)
AIRBYTE_LOGO_FOR_DARK_BG_PATH = (
    AIRBYTE_ASSETS_DIR / "airbyte_logo_color_light_transparent.svg"
)
AIRBYTE_INK = "#140F43"
AIRBYTE_PRIMARY = "#5D51D5"
AIRBYTE_SECONDARY = "#D763EC"
AIRBYTE_LAVENDER = "#CECBF2"
AIRBYTE_DARK_CARD = "#282255"
AIRBYTE_DARK_PANEL = "#201A4D"
AIRBYTE_THEME_LIGHT_CSS = {
    "background": "#FFFFFF",
    "foreground": "#140F43",
    "card": "#FFFFFF",
    "card-foreground": "#140F43",
    "popover": "#FFFFFF",
    "popover-foreground": "#140F43",
    "primary": "#5D51D5",
    "primary-foreground": "#FFFFFF",
    "secondary": "#CECBF2",
    "secondary-foreground": "#140F43",
    "muted": "#CECBF2",
    "muted-foreground": "#140F43",
    "accent": "#EFC1F7",
    "accent-foreground": "#140F43",
    "border": "#CECBF2",
    "input": "#CECBF2",
    "ring": "#D763EC",
    "info": "#5D51D5",
    "info-foreground": "#FFFFFF",
    "success": "#5D51D5",
    "success-foreground": "#FFFFFF",
}
AIRBYTE_THEME_DARK_CSS = {
    "background": "#140F43",
    "foreground": "#FFFFFF",
    "card": "color-mix(in srgb, #140F43 88%, #5D51D5 12%)",
    "card-foreground": "#FFFFFF",
    "popover": "color-mix(in srgb, #140F43 84%, #5D51D5 16%)",
    "popover-foreground": "#FFFFFF",
    "primary": "#5D51D5",
    "primary-foreground": "#FFFFFF",
    "secondary": "#D763EC",
    "secondary-foreground": "#FFFFFF",
    "muted": "color-mix(in srgb, #140F43 72%, #CECBF2 28%)",
    "muted-foreground": "#CECBF2",
    "accent": "#D763EC",
    "accent-foreground": "#FFFFFF",
    "border": "color-mix(in srgb, #CECBF2 30%, transparent)",
    "input": "color-mix(in srgb, #CECBF2 26%, transparent)",
    "ring": "#D763EC",
    "info": "#5D51D5",
    "info-foreground": "#FFFFFF",
    "success": "#CECBF2",
    "success-foreground": "#140F43",
}


def _css_vars(css_vars: dict[str, str]) -> str:
    return "\n".join(f"  --{key}: {value};" for key, value in css_vars.items())


AIRBYTE_THEME_MODE_CSS = f"""
.airbyte-mode-light {{
{_css_vars(AIRBYTE_THEME_LIGHT_CSS)}
}}
.airbyte-mode-dark {{
{_css_vars(AIRBYTE_THEME_DARK_CSS)}
}}
@media (prefers-color-scheme: dark) {{
  .airbyte-mode-system {{
{_css_vars(AIRBYTE_THEME_DARK_CSS)}
  }}
}}
"""
AIRBYTE_THEME_CSS = (
    AIRBYTE_THEME_MODE_CSS
    + """
body {
  margin: 0;
  background: var(--background);
}
.pf-app-root {
  min-height: 100vh;
  background:
    radial-gradient(circle at 14% 0%, color-mix(in srgb, #5D51D5 36%, transparent) 0, transparent 32rem),
    radial-gradient(circle at 86% 12%, color-mix(in srgb, #D763EC 28%, transparent) 0, transparent 28rem),
    var(--background);
  color: var(--foreground);
}
.airbyte-app-root {
  min-height: 100vh;
  background: var(--background) !important;
  color: var(--foreground) !important;
  padding: 1.5rem;
}
.airbyte-app-root input,
.airbyte-app-root textarea,
.airbyte-app-root select {
  background: var(--card) !important;
  border-color: var(--border) !important;
  color: var(--foreground) !important;
}
.airbyte-app-root button[data-variant="outline"],
.airbyte-app-root .pf-button-variant-outline {
  background: var(--card) !important;
  border-color: var(--border) !important;
  color: var(--foreground) !important;
}
.airbyte-page {
  margin-left: auto;
  margin-right: auto;
  max-width: 80rem;
}
.airbyte-hero-card {
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--card) 92%, var(--primary) 8%), var(--card)) !important;
  border: 0 !important;
  color: var(--card-foreground) !important;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px color-mix(in srgb, var(--primary) 20%, transparent);
}
.airbyte-panel-card,
.airbyte-status-card,
.airbyte-preview-card,
.airbyte-success-card,
.airbyte-mock-card {
  background: var(--card) !important;
  border-color: var(--border) !important;
  color: var(--card-foreground) !important;
  box-shadow: 0 10px 15px -3px color-mix(in srgb, var(--background) 20%, transparent);
}
.airbyte-mock-card {
  border-color: color-mix(in srgb, var(--secondary) 50%, transparent) !important;
}
.airbyte-preview-card {
  border-color: color-mix(in srgb, var(--primary) 50%, transparent) !important;
}
.airbyte-success-card {
  border-color: color-mix(in srgb, var(--secondary) 70%, transparent) !important;
}
.airbyte-code-block {
  background: var(--background) !important;
  border: 1px solid var(--border) !important;
  border-radius: 0.375rem;
  color: var(--muted-foreground) !important;
  font-size: 0.875rem;
  overflow-x: auto;
  padding: 1rem;
}
.airbyte-hero-header {
  flex-wrap: wrap;
}
.airbyte-logo {
  display: block !important;
  height: 4rem;
  max-width: 10rem;
  overflow: hidden;
  width: 10rem;
}
.airbyte-logo svg {
  display: block !important;
  height: 4rem !important;
  width: 10rem !important;
}
.airbyte-logo-for-dark-bg {
  display: none !important;
}
.dark .airbyte-logo-for-dark-bg,
.airbyte-mode-dark .airbyte-logo-for-dark-bg {
  display: block !important;
}
.dark .airbyte-logo-for-light-bg,
.airbyte-mode-dark .airbyte-logo-for-light-bg {
  display: none !important;
}
@media (prefers-color-scheme: dark) {
  .airbyte-mode-system .airbyte-logo-for-dark-bg {
    display: block !important;
  }
  .airbyte-mode-system .airbyte-logo-for-light-bg {
    display: none !important;
  }
}
"""
)
APP_ROOT_CLASS = "airbyte-app-root"
PAGE_CLASS = "airbyte-page"
HERO_CARD_CLASS = "airbyte-hero-card"
PANEL_CARD_CLASS = "airbyte-panel-card"
MOCK_CARD_CLASS = "airbyte-mock-card"
PREVIEW_CARD_CLASS = "airbyte-preview-card"
SUCCESS_CARD_CLASS = "airbyte-success-card"
STATUS_CARD_CLASS = "airbyte-status-card"
CODE_BLOCK_CLASS = "airbyte-code-block"
AIRBYTE_LOGO_CLASS = "airbyte-logo"


def _theme_mode() -> Literal["light", "dark"] | None:
    theme_mode = os.getenv(THEME_MODE_ENV_VAR, "dark").strip().lower()
    if theme_mode == "system":
        return None
    if theme_mode == "light":
        return "light"
    return "dark"


def _app_root_class() -> str:
    theme_mode = os.getenv(THEME_MODE_ENV_VAR, "dark").strip().lower()
    if theme_mode == "system":
        return f"{APP_ROOT_CLASS} airbyte-mode-system"
    if theme_mode == "light":
        return f"{APP_ROOT_CLASS} airbyte-mode-light"
    return f"{APP_ROOT_CLASS} airbyte-mode-dark"


def _airbyte_logo_svg_for_light_bg() -> str:
    return AIRBYTE_LOGO_FOR_LIGHT_BG_PATH.read_text(encoding="utf-8")


def _airbyte_logo_svg_for_dark_bg() -> str:
    return AIRBYTE_LOGO_FOR_DARK_BG_PATH.read_text(encoding="utf-8")


def _is_light_theme() -> bool:
    return os.getenv(THEME_MODE_ENV_VAR, "dark").strip().lower() == "light"


def _airbyte_logo_svg() -> str:
    if _is_light_theme():
        return _airbyte_logo_svg_for_light_bg()
    return _airbyte_logo_svg_for_dark_bg()


def _page_style() -> dict[str, str]:
    if _is_light_theme():
        return {
            "background": "#FFFFFF",
            "color": AIRBYTE_INK,
            "minHeight": "100vh",
            "padding": "1.5rem",
        }
    return {
        "background": AIRBYTE_INK,
        "color": "#FFFFFF",
        "minHeight": "100vh",
        "padding": "1.5rem",
    }


def _card_style(*, accent: str | None = None) -> dict[str, str]:
    if _is_light_theme():
        border = accent or AIRBYTE_LAVENDER
        return {
            "background": "#FFFFFF",
            "border": f"1px solid {border}",
            "borderRadius": "0.75rem",
            "boxShadow": "0 10px 15px -3px rgba(20, 15, 67, 0.08)",
            "color": AIRBYTE_INK,
        }
    border = accent or "rgba(206, 203, 242, 0.3)"
    return {
        "background": AIRBYTE_DARK_PANEL,
        "border": f"1px solid {border}",
        "borderRadius": "0.75rem",
        "boxShadow": "0 10px 15px -3px rgba(0, 0, 0, 0.35)",
        "color": "#FFFFFF",
    }


def _hero_style() -> dict[str, str]:
    style = _card_style(accent="transparent")
    if _is_light_theme():
        style["background"] = "#FFFFFF"
    else:
        style["background"] = AIRBYTE_DARK_CARD
    return style


def _code_surface_style() -> dict[str, str]:
    if _is_light_theme():
        return {
            "background": "#F7F6FF",
            "border": f"1px solid {AIRBYTE_LAVENDER}",
            "borderRadius": "0.375rem",
            "color": AIRBYTE_INK,
            "fontFamily": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
            "fontSize": "0.8125rem",
            "lineHeight": "1.5",
            "overflowX": "auto",
            "padding": "0.75rem",
            "whiteSpace": "pre-wrap",
        }
    return {
        "background": "#0F0B33",
        "border": "1px solid rgba(206, 203, 242, 0.3)",
        "borderRadius": "0.375rem",
        "color": AIRBYTE_LAVENDER,
        "fontFamily": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
        "fontSize": "0.8125rem",
        "lineHeight": "1.5",
        "overflowX": "auto",
        "padding": "0.75rem",
        "whiteSpace": "pre-wrap",
    }


def _airbyte_theme() -> Theme:
    return Theme(
        light_css=AIRBYTE_THEME_LIGHT_CSS,
        dark_css=AIRBYTE_THEME_DARK_CSS,
        css=AIRBYTE_THEME_CSS,
        mode=_theme_mode(),
    )
