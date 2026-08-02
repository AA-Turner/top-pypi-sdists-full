"""One-shot relocation of on-disk state to the XDG directories.

Older versions scattered runtime state between ``~/.config/pysae-ai-tools`` and a hardcoded
``~/.claude/pysae-ai-tools``. Everything now follows the XDG convention (config / data / cache), with
Claude-specific state namespaced under ``assistants/claude/``. This orchestrator moves any legacy
state to its new home exactly once — triggered from ``self_update`` after the installer succeeds,
never on the hot path. Each per-subsystem step is best-effort and idempotent, so it is a no-op on a
fresh install or in CI, and safe to re-run.

As a root wiring module (like ``self_update`` / ``uninstall``) it may import across groups; it is
excluded from the ``tach`` layering check.
"""

from pathlib import Path

from .env import cache as env_cache
from .internal.detect_context import detect as detect_context
from .pysae.api.common import tokens as pysae_tokens
from .tracker import hook as tracker_hook
from .usage import migrate as usage_migrate

_CLAUDE_DIR = Path.home() / ".claude" / "pysae-ai-tools"


def run_migration() -> None:
    """Relocate every subsystem's legacy state, then drop the now-empty legacy root."""
    for step in (
        usage_migrate.migrate_legacy,
        env_cache.migrate_legacy,
        pysae_tokens.migrate_legacy,
        detect_context.migrate_legacy,
        tracker_hook.migrate_legacy,
    ):
        try:
            step()
        except Exception:  # noqa: BLE001 — a migration failure must never break self-update
            pass
    try:
        _CLAUDE_DIR.rmdir()  # removes the legacy root only once every subsystem relocated out of it
    except OSError:
        pass
