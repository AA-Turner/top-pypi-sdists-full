"""
cvc.agent.settings — Multi-level settings hierarchy for CVC.

Implements a Claude Code-style settings system with 4 levels of precedence:

  1. CLI arguments (highest) — --allowedTools, --disallowedTools, --model
  2. .cvc/settings.local.json — project-local, not committed
  3. .cvc/settings.json — project-shared, checked into git
  4. ~/.cvc/settings.json — user-global, all projects

Settings schema:
    {
        "permissions": {
            "allow": ["Bash(npm run *)", "Read"],
            "deny": ["Bash(rm -rf *)"],
            "ask": ["Edit", "WebFetch"]
        },
        "env": {
            "NODE_ENV": "development"
        },
        "hooks": {
            "PreToolUse": [...],
            "PostToolUse": [...]
        },
        "outputStyle": "default",
        "autoMemoryEnabled": true,
        "alwaysThinkingEnabled": false,
        "autoCompactThreshold": 95,
        "enabledPlugins": {}
    }

Merge logic:
  - deny rules: union across all levels (deny anywhere → denied everywhere)
  - allow rules: higher precedence overrides lower
  - env vars: higher precedence overrides lower (per key)
  - hooks: merged (all levels' hooks fire)
  - scalar values: highest precedence wins
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.settings")


@dataclass
class TelegramConfig:
    enabled: bool = False
    bot_token: str = ""
    allowlist: list[int] = field(default_factory=list)
    streaming_mode: str = "block"  # "block" or "partial"
    approval_target: str = "dm"


@dataclass
class CvcSettings:
    """Merged settings from all levels."""

    # Permissions
    permission_allow: list[str] = field(default_factory=list)
    permission_deny: list[str] = field(default_factory=list)
    permission_ask: list[str] = field(default_factory=list)

    # Environment variables to inject
    env: dict[str, str] = field(default_factory=dict)

    # Hooks configuration
    hooks: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    # UI / behavior
    output_style: str = "default"
    auto_memory_enabled: bool = True
    always_thinking_enabled: bool = False
    auto_compact_threshold: int = 95

    # Plugins
    enabled_plugins: dict[str, bool] = field(default_factory=dict)

    # Trust & Plan modes
    trust_mode: str = "smart"  # "strict" | "smart" | "yolo"
    plan_display: str = "plan-auto"  # "plan-approve" | "plan-auto" | "plan-quiet"
    trusted_commands: list[str] = field(default_factory=list)
    blocked_commands: list[str] = field(default_factory=list)

    # Telegram integration
    telegram: TelegramConfig = field(default_factory=TelegramConfig)

    # CLI overrides (set at runtime, not from files)
    cli_allowed_tools: list[str] = field(default_factory=list)
    cli_disallowed_tools: list[str] = field(default_factory=list)

    @property
    def allow_permissions(self) -> list[str]:
        """All allow rules (settings + CLI)."""
        return self.permission_allow + self.cli_allowed_tools

    @property
    def deny_permissions(self) -> list[str]:
        """All deny rules (settings + CLI)."""
        return self.permission_deny + self.cli_disallowed_tools

    @property
    def hooks_flat(self) -> list[dict[str, Any]]:
        """Flatten hooks dict into a list with 'event' key for HookEngine."""
        result: list[dict[str, Any]] = []
        for event, hook_list in self.hooks.items():
            for hook in hook_list:
                h = dict(hook)
                h.setdefault("event", event)
                result.append(h)
        return result

    def to_dict(self) -> dict[str, Any]:
        """Serialize all settings to a JSON-friendly dict."""
        return {
            "permissions": {
                "allow": self.permission_allow,
                "deny": self.permission_deny,
                "ask": self.permission_ask,
            },
            "env": dict(self.env),
            "hooks": {k: list(v) for k, v in self.hooks.items()},
            "outputStyle": self.output_style,
            "autoMemoryEnabled": self.auto_memory_enabled,
            "alwaysThinkingEnabled": self.always_thinking_enabled,
            "autoCompactThreshold": self.auto_compact_threshold,
            "enabledPlugins": dict(self.enabled_plugins),
            "trust_mode": self.trust_mode,
            "plan_display": self.plan_display,
            "trusted_commands": list(self.trusted_commands),
            "blocked_commands": list(self.blocked_commands),
            "telegram": {
                "enabled": self.telegram.enabled,
                "bot_token": self.telegram.bot_token,
                "allowlist": self.telegram.allowlist,
                "streaming_mode": self.telegram.streaming_mode,
                "approval_target": self.telegram.approval_target,
            },
        }


def load_settings(workspace: Path | None = None) -> CvcSettings:
    """
    Load and merge settings from all levels.

    Levels (lowest → highest precedence):
      1. ~/.cvc/settings.json (user global)
      2. .cvc/settings.json (project shared)
      3. .cvc/settings.local.json (project local)
      4. CLI arguments (applied separately via set_cli_overrides)

    Parameters
    ----------
    workspace : Path or None
        Project root directory. If None, uses current working directory.

    Returns
    -------
    CvcSettings
        Merged settings object.
    """
    workspace = (workspace or Path.cwd()).resolve()
    merged = CvcSettings()

    # Securely load secrets from .env if present
    try:
        from dotenv import load_dotenv
        env_path = workspace / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
    except ImportError:
        logger.warning("python-dotenv not installed; relying on existing os.environ")

    # Level 1: User global settings
    user_settings_path = Path.home() / ".cvc" / "settings.json"
    _merge_from_file(merged, user_settings_path, level="user")

    # Level 2: Project shared settings
    project_shared = workspace / ".cvc" / "settings.json"
    _merge_from_file(merged, project_shared, level="project")

    # Level 3: Project local settings (not committed)
    project_local = workspace / ".cvc" / "settings.local.json"
    _merge_from_file(merged, project_local, level="local")

    # Apply environment variables from settings
    for key, val in merged.env.items():
        if key not in os.environ:  # Don't override existing env vars
            os.environ[key] = val

    # v3.3.42 — Removed TELEGRAM_BOT_TOKEN / TELEGRAM_ALLOWED_USERS env
    # fallbacks. The canonical source-of-truth for Telegram secrets is
    # ``~/.cvc/channels/telegram.yaml``, written by ``cvc setup`` and
    # read by the registry-driven Telegram adapter. Falling back to
    # env vars here caused two problems:
    #   1. A legacy ``<project>/.env`` file would silently re-introduce
    #      a stale token into the live config, undoing any rotation.
    #   2. Shipping a project-root ``.env`` leaks user secrets on any
    #      clone or distribution of the CVC source.
    # Users who want Telegram on a fresh machine run ``cvc setup`` and
    # the wizard writes their token to the per-user channels file.
    # If the channels file is missing, the Telegram adapter starts
    # with ``enabled=False`` — the safe default.

    return merged


def set_cli_overrides(
    settings: CvcSettings,
    allowed_tools: list[str] | None = None,
    disallowed_tools: list[str] | None = None,
) -> None:
    """Apply CLI-level overrides (highest precedence)."""
    if allowed_tools:
        settings.cli_allowed_tools = allowed_tools
    if disallowed_tools:
        settings.cli_disallowed_tools = disallowed_tools


def save_project_settings(workspace: Path, key: str, value: Any, local: bool = False) -> None:
    """
    Save a setting to the project settings file.

    Parameters
    ----------
    workspace : Path
        Project root directory.
    key : str
        Dot-separated key path (e.g., 'permissions.allow').
    value : Any
        Value to set.
    local : bool
        If True, save to settings.local.json instead of settings.json.
    """
    filename = "settings.local.json" if local else "settings.json"
    settings_path = workspace / ".cvc" / filename

    # Load existing
    data: dict[str, Any] = {}
    if settings_path.exists():
        try:
            data = json.loads(settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    # Set nested key
    parts = key.split(".")
    target = data
    for part in parts[:-1]:
        if part not in target or not isinstance(target[part], dict):
            target[part] = {}
        target = target[part]
    target[parts[-1]] = value

    # Write back
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _merge_from_file(merged: CvcSettings, path: Path, level: str) -> None:
    """Load a single settings file and merge into the accumulated settings."""
    if not path.exists():
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Failed to load settings from %s: %s", path, e)
        return

    if not isinstance(data, dict):
        return

    logger.debug("Loaded %s settings from %s", level, path)

    # Permissions — deny rules are UNION'd (deny anywhere = denied everywhere)
    perms = data.get("permissions", {})
    if isinstance(perms, dict):
        deny = perms.get("deny", [])
        if isinstance(deny, list):
            for rule in deny:
                if rule not in merged.permission_deny:
                    merged.permission_deny.append(rule)

        # Allow and Ask — higher precedence overwrites
        allow = perms.get("allow", [])
        if isinstance(allow, list):
            merged.permission_allow = allow + [
                r for r in merged.permission_allow if r not in allow
            ]

        ask = perms.get("ask", [])
        if isinstance(ask, list):
            merged.permission_ask = ask + [
                r for r in merged.permission_ask if r not in ask
            ]

    # Environment — higher precedence overwrites per key
    env = data.get("env", {})
    if isinstance(env, dict):
        merged.env.update(env)

    # Hooks — merged (all levels fire)
    hooks = data.get("hooks", {})
    if isinstance(hooks, dict):
        for event, hook_list in hooks.items():
            if isinstance(hook_list, list):
                if event not in merged.hooks:
                    merged.hooks[event] = []
                merged.hooks[event].extend(hook_list)

    # Scalar values — higher precedence wins
    if "outputStyle" in data:
        merged.output_style = data["outputStyle"]
    if "autoMemoryEnabled" in data:
        merged.auto_memory_enabled = bool(data["autoMemoryEnabled"])
    if "alwaysThinkingEnabled" in data:
        merged.always_thinking_enabled = bool(data["alwaysThinkingEnabled"])
    if "autoCompactThreshold" in data:
        merged.auto_compact_threshold = int(data["autoCompactThreshold"])

    # Trust & plan modes
    if "trust_mode" in data:
        val = data["trust_mode"]
        if val in ("strict", "smart", "yolo"):
            merged.trust_mode = val
    if "plan_display" in data:
        val = data["plan_display"]
        if val in ("plan-approve", "plan-auto", "plan-quiet"):
            merged.plan_display = val
    if "trusted_commands" in data and isinstance(data["trusted_commands"], list):
        merged.trusted_commands = data["trusted_commands"]
    if "blocked_commands" in data and isinstance(data["blocked_commands"], list):
        merged.blocked_commands = data["blocked_commands"]

    # Plugins — merge enabled states
    plugins = data.get("enabledPlugins", {})
    if isinstance(plugins, dict):
        merged.enabled_plugins.update(plugins)

    # Telegram configuration
    tg = data.get("telegram", {})
    if isinstance(tg, dict):
        if "enabled" in tg:
            merged.telegram.enabled = bool(tg["enabled"])
        if "bot_token" in tg:
            merged.telegram.bot_token = str(tg["bot_token"])
        if "allowlist" in tg:
            merged.telegram.allowlist = [int(x) for x in tg["allowlist"] if isinstance(x, (int, str)) and str(x).isdigit()]
        if "streaming_mode" in tg:
            merged.telegram.streaming_mode = str(tg["streaming_mode"])
        if "approval_target" in tg:
            merged.telegram.approval_target = str(tg["approval_target"])
