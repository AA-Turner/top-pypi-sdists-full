"""One-shot relocation of legacy usage state into the XDG directories.

Historically the usage subsystem wrote under ``~/.claude/pysae-ai-tools/`` (next to Claude's own
files). Everything now lives under the XDG data/cache dirs (see :mod:`.account`,
:mod:`.pricing_source`, :mod:`.icon`). This module moves any pre-existing legacy state to its new
home exactly once, triggered off the hot path (see ``pysae_ai_tools.migrate``). Idempotent and
best-effort: a no-op once nothing is left under the old location.
"""

import json
import shutil
from pathlib import Path

from . import account, icon, pricing_source
from .config import load_config

_CLAUDE_DIR = Path.home() / ".claude" / "pysae-ai-tools"

# Flat state files that predate per-account partitioning (a single account's state, un-namespaced).
_STATE_FILES = (
    "usage-cache.json",
    "usage-lock.json",
    "prime-state.json",
    "prime.log",
    "usage-warn-state.json",
    "usage-overage.json",
    "usage-history.jsonl",
    "usage-history-last.json",
    "usage-unblock.json",
)
_HISTORY_FILE = "usage-history.jsonl"


def _merge_history(src: Path, dest: Path) -> None:
    """Union the two append-only history logs by sample ``ts`` into ``dest`` (dedup, oldest first)."""
    lines: dict[float, str] = {}
    for path in (dest, src):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = parsed.get("ts") if isinstance(parsed, dict) else None
            if isinstance(ts, (int, float)):
                lines[float(ts)] = line
    dest.write_text("\n".join(lines[k] for k in sorted(lines)) + "\n", encoding="utf-8")


def _move(src: Path, dest: Path) -> None:
    """Move ``src`` to ``dest``. If ``dest`` already exists, merge history by ts, else drop the
    legacy copy (the partitioned ``dest`` is the live one). Best-effort — never raises."""
    try:
        if not src.exists():
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            shutil.move(str(src), str(dest))
        elif src.name == _HISTORY_FILE:
            _merge_history(src, dest)
            src.unlink()
        else:
            src.unlink()
    except OSError:
        pass


def _migrate_accounts() -> None:
    """Relocate already-partitioned ``accounts/<key>/`` subdirs to the XDG data dir."""
    old_accounts = _CLAUDE_DIR / "accounts"
    if not old_accounts.is_dir():
        return
    for old_sub in old_accounts.iterdir():
        if not old_sub.is_dir():
            continue
        new_sub = account.ACCOUNTS_DIR / old_sub.name
        for entry in old_sub.iterdir():
            _move(entry, new_sub / entry.name)
        try:
            old_sub.rmdir()
        except OSError:
            pass
    try:
        old_accounts.rmdir()
    except OSError:
        pass


def _migrate_flat_state() -> None:
    """Very old installs kept flat state files directly under the legacy dir (pre-per-account).
    Partition them into the active account's dir; leave them if no account is identifiable."""
    if not any((_CLAUDE_DIR / name).exists() for name in _STATE_FILES):
        return
    active = account.current_account()
    if active is None:
        return
    target = account.state_dir(active)
    account.write_account_meta(active)
    for name in _STATE_FILES:
        _move(_CLAUDE_DIR / name, target / name)


def migrate_legacy() -> None:
    """Relocate all legacy usage state from ``~/.claude/pysae-ai-tools`` into the XDG dirs."""
    _migrate_accounts()
    _migrate_flat_state()
    _move(_CLAUDE_DIR / "pricing-cache.json", pricing_source.CACHE_PATH)
    _move(_CLAUDE_DIR / "claude-icon.svg", icon.ICON_CACHE)
    load_config()  # flushes the very-old usage-config.json into config.toml (and deletes it)
