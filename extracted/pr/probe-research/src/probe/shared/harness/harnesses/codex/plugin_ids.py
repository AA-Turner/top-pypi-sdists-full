"""Codex's PluginInstaller ledger: the plugin tables in its config.toml."""

from __future__ import annotations


def _codex_plugin_ids() -> list[str]:
    """Every `[plugins."<plugin>@<marketplace>"]` table in Codex's config.toml,
    which `codex plugin add` writes and `codex plugin list` reads (enabled or
    not, as the list shows them). A missing file is Codex with nothing added."""
    from probe.foundation.compat.compat import tomllib
    from probe.shared.harness.harnesses.codex import config as codex_config

    try:
        parsed = tomllib.loads(codex_config.config_path().read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    plugins = parsed.get("plugins")
    return [key for key in plugins if isinstance(key, str)] if isinstance(plugins, dict) else []
