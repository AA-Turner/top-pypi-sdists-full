"""Airbyte theme settings for the connector version manager."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from prefab_ui.themes import Theme

THEME_MODE_ENV_VAR = "AIRBYTE_OPS_WEBAPP_THEME_MODE"

# CSS injected directly into the Prefab renderer iframe (bypasses Theme).
# Theme CSS only reaches the outer page; this constant is read by serve.py's
# _inject_renderer_overrides() to patch the iframe <head>.
RENDERER_OVERRIDE_CSS = """\
.pf-dialog-content {
  max-width: 56rem !important;
  width: min(56rem, 90vw) !important;
  max-height: 85vh !important;
  overflow-y: auto !important;
}
/* Sticky table headers: keep the header row visible while the body scrolls.
   The default renderer wraps every table in a `.pf-table-container` whose
   `overflow-x: auto` promotes overflow on both axes (per the CSS spec, an
   `auto` on one axis forces the `visible` on the other to compute to `auto`),
   which traps `position: sticky` so the header can never stick. Relaxing the
   container to `visible` frees the header to stick to the nearest real scroll
   parent instead. That parent is a height-capped scroll wrapper (e.g. the org
   lookup modal's `max-h-[50vh]` column, or the CVM tab lists) which owns
   `overflow: auto` on BOTH axes -- so wide tables still scroll horizontally
   there rather than bleeding out of the modal/panel. The header needs an
   opaque background so scrolling rows don't show through. */
.pf-table-container {
  overflow: visible !important;
}
.pf-table-header {
  position: sticky !important;
  top: 0;
  z-index: 2;
}
.pf-table-header,
.pf-table-header tr,
.pf-table-header .pf-table-head {
  background: var(--background);
}
"""
AIRBYTE_ASSETS_DIR = Path(__file__).parent.parent / "assets"
AIRBYTE_LOGO_FOR_LIGHT_BG_PATH = (
    AIRBYTE_ASSETS_DIR / "airbyte_logo_color_dark_transparent.svg"
)
AIRBYTE_LOGO_FOR_DARK_BG_PATH = (
    AIRBYTE_ASSETS_DIR / "airbyte_logo_color_light_transparent.svg"
)
CONNECTOR_VERSION_MANAGER_ICON_PATH = (
    AIRBYTE_ASSETS_DIR / "connector_version_manager_icon.svg"
)
MORE_TOOLS_ICON_PATH = AIRBYTE_ASSETS_DIR / "more_tools_icon.svg"
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
  background: var(--background) !important;
}
html,
body {
  min-height: 100%;
}
* {
  box-sizing: border-box;
}
.pf-app-root {
  min-height: 100vh;
  width: 100%;
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
  width: 100%;
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
.airbyte-app-root button[data-variant="info"],
.airbyte-app-root .pf-button-variant-info {
  background: var(--info) !important;
  border-color: var(--info) !important;
  color: var(--info-foreground) !important;
}
.airbyte-app-root button[data-variant="destructive"],
.airbyte-app-root .pf-button-variant-destructive {
  color: #FFFFFF !important;
}
.airbyte-page {
  margin-left: auto;
  margin-right: auto;
  max-width: 80rem;
  width: 100%;
}
.airbyte-page-surface {
  background: var(--background);
  color: var(--foreground);
  min-height: 100vh;
  padding: 1.5rem;
}
.airbyte-hero-card {
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--card) 92%, var(--primary) 8%), var(--card)) !important;
  border: 0 !important;
  border-radius: 0.75rem;
  color: var(--card-foreground) !important;
  overflow: hidden;
  padding: 1rem;
  box-shadow: 0 25px 50px -12px color-mix(in srgb, var(--primary) 20%, transparent);
}
.airbyte-panel-card,
.airbyte-status-card,
.airbyte-preview-card,
.airbyte-success-card,
.airbyte-error-card,
.airbyte-mock-card {
  background: var(--card) !important;
  border-color: var(--border) !important;
  border-style: solid;
  border-width: 1px;
  border-radius: 0.75rem;
  color: var(--card-foreground) !important;
  padding: 1rem;
  box-shadow: 0 10px 15px -3px color-mix(in srgb, var(--background) 20%, transparent);
}
.airbyte-tool-card {
  height: 100%;
  padding: 0.5rem;
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
.airbyte-error-card {
  border-color: color-mix(in srgb, #ff6b6b 70%, transparent) !important;
}
.airbyte-env-banner {
  align-items: center;
  color: #fff;
  display: flex;
  flex-shrink: 0;
  font-size: 0.8125rem;
  font-weight: 600;
  gap: 0.5rem;
  justify-content: center;
  letter-spacing: 0.02em;
  padding: 0.375rem 1rem;
  text-align: center;
  width: 100%;
}
.airbyte-env-banner a {
  color: #fff !important;
  text-decoration: underline !important;
}
.airbyte-version-footer {
  align-items: center;
  color: #ccc;
  display: flex;
  font-size: 0.75rem;
  gap: 0.75rem;
  justify-content: center;
  opacity: 0.5;
  padding: 0.75rem 1rem;
}
.airbyte-version-footer a {
  color: #ccc;
  text-decoration: underline;
}
.airbyte-primary-link {
  align-items: center;
  background: var(--primary);
  border-radius: 0.625rem;
  color: #ffffff;
  display: inline-flex;
  font-weight: 700;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  text-decoration: none;
  width: fit-content;
}
.airbyte-tool-icon {
  align-items: center;
  border-radius: 0.75rem;
  color: var(--foreground);
  display: flex;
  font-weight: 700;
  height: 2.75rem;
  justify-content: center;
  letter-spacing: 0.04em;
  width: 2.75rem;
}
.airbyte-code-surface {
  background: #0f0b33;
  border: 1px solid rgba(206, 203, 242, 0.3);
  border-radius: 0.375rem;
  color: #cecbf2;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.8125rem;
  line-height: 1.5;
  overflow-x: auto;
  padding: 0.75rem;
  white-space: pre-wrap;
}
.airbyte-mode-light .airbyte-code-surface {
  background: #f7f6ff;
  border: 1px solid #cecbf2;
  color: #140f43;
}
.airbyte-detail-box {
  margin-top: 0.75rem;
  padding: 16px;
  background: #1a1545;
  border: 1px solid rgba(206, 203, 242, 0.2);
  border-radius: 6px;
  font-size: 0.85rem;
}
.airbyte-breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}
.airbyte-breadcrumb-nav a {
  color: var(--muted-foreground);
  text-decoration: none;
  transition: color 0.15s;
}
.airbyte-breadcrumb-nav a:hover {
  color: var(--primary);
  text-decoration: underline;
}
.airbyte-breadcrumb-nav .breadcrumb-separator {
  color: var(--muted-foreground);
  opacity: 0.6;
}
.airbyte-breadcrumb-nav .breadcrumb-current {
  color: var(--foreground);
  font-weight: 600;
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
  align-items: flex-start !important;
  display: flex !important;
  flex-wrap: wrap;
  justify-content: space-between !important;
  width: 100%;
}
.airbyte-hero-copy {
  flex: 1 1 28rem;
  min-width: 0;
}
.airbyte-hero-actions {
  flex: 0 0 auto;
}
.airbyte-stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  overflow-wrap: anywhere;
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
PAGE_SURFACE_CLASS = "airbyte-page-surface"
HERO_CARD_CLASS = "airbyte-hero-card"
PANEL_CARD_CLASS = "airbyte-panel-card"
TOOL_CARD_CLASS = "airbyte-tool-card"
MOCK_CARD_CLASS = "airbyte-mock-card"
PREVIEW_CARD_CLASS = "airbyte-preview-card"
SUCCESS_CARD_CLASS = "airbyte-success-card"
ERROR_CARD_CLASS = "airbyte-error-card"
STATUS_CARD_CLASS = "airbyte-status-card"
CODE_BLOCK_CLASS = "airbyte-code-block"
CODE_SURFACE_CLASS = "airbyte-code-surface"
TABLE_SCROLL_CLASS = "airbyte-table-scroll"
DETAIL_BOX_CLASS = "airbyte-detail-box"
PRIMARY_LINK_CLASS = "airbyte-primary-link"
TOOL_ICON_CLASS = "airbyte-tool-icon"
STAT_VALUE_CLASS = "airbyte-stat-value"
VERSION_FOOTER_CLASS = "airbyte-version-footer"
ENV_BANNER_DOT_CLASS = "inline-block w-[7px] h-[7px] rounded-full bg-[#fbbf24]"
# Anchor styling for banner/footer links. The `.airbyte-env-banner a` and
# `.airbyte-version-footer a` rules live in `AIRBYTE_THEME_CSS`, which never
# reaches the Prefab renderer iframe, so links carry these Tailwind utilities
# to stay styled inside the renderer.
ENV_BANNER_LINK_CLASS = "text-white underline"
VERSION_FOOTER_LINK_CLASS = "text-[#ccc] underline"
AIRBYTE_LOGO_CLASS = "airbyte-logo"
BUTTON_INFO_CLASS = "bg-[#5D51D5] text-white border-[#5D51D5] hover:bg-[#4D43BE]"
BUTTON_OUTLINE_CLASS = "bg-[#282255] text-white border-[#CECBF24D] hover:bg-[#332B6B]"
BUTTON_DESTRUCTIVE_CLASS = "bg-[#B42318] text-white border-[#B42318] hover:bg-[#912018]"
ENV_BANNER_CLASS = "airbyte-env-banner"
BREADCRUMB_NAV_CLASS = "airbyte-breadcrumb-nav"
COMBOBOX_CLASS = "bg-[#282255] text-white border-[#CECBF24D] hover:bg-[#332B6B]"


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
    return f"{APP_ROOT_CLASS} airbyte-mode-dark dark"


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


def _connector_version_manager_icon_svg() -> str:
    return CONNECTOR_VERSION_MANAGER_ICON_PATH.read_text(encoding="utf-8")


def _more_tools_icon_svg() -> str:
    return MORE_TOOLS_ICON_PATH.read_text(encoding="utf-8")


def _airbyte_theme() -> Theme:
    return Theme(
        light_css=AIRBYTE_THEME_LIGHT_CSS,
        dark_css=AIRBYTE_THEME_DARK_CSS,
        css=AIRBYTE_THEME_CSS,
        mode=_theme_mode(),
    )
