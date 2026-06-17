"""Runtime detection: is this process the AI Watch binary?

The ``aiwatch`` binary must resolve host from MDM-managed config and per-user
secrets from the keychain only — never ``~/.runlayer/config.yaml``. ``config.py``
gates ``load_config``/``save_config`` on ``is_aiwatch_runtime()`` so a stray
developer config can never redirect an MDM-deployed agent.

Two signals mark the aiwatch runtime:

1. A process-global flag set by ``mark_aiwatch_runtime()`` at the aiwatch
   binary entrypoint (``aiwatch.py:main``). The unfrozen
   ``python -m runlayer_cli.hook`` / transcript-worker paths are the
   pip-installed ``runlayer`` package, not the MDM aiwatch binary, so they do
   NOT mark the flag — they must read ``~/.runlayer/config.yaml`` for host +
   credential resolution.
2. The frozen-aiwatch bundle idiom (``is_frozen_aiwatch_bundle``: ``sys.frozen``
   + the exe stem starts with ``aiwatch``), also reused by
   ``credential_store._service_name``. The full frozen ``runlayer`` bundle has a
   different exe name, so it is never treated as aiwatch. This covers the frozen
   aiwatch hook + transcript worker (both re-exec the aiwatch binary).

Stdlib-only so it stays importable inside the aiwatch PyInstaller closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

_aiwatch_runtime = False


def mark_aiwatch_runtime() -> None:
    """Mark this process as the aiwatch runtime (call at the aiwatch entrypoints)."""
    global _aiwatch_runtime
    _aiwatch_runtime = True


def reset_aiwatch_runtime() -> None:
    """Clear the aiwatch runtime flag. Used in tests."""
    global _aiwatch_runtime
    _aiwatch_runtime = False


def is_frozen_aiwatch_bundle() -> bool:
    """True when this is the frozen aiwatch PyInstaller bundle.

    ``sys.frozen`` + the exe stem starts with ``aiwatch``. The full frozen
    ``runlayer`` bundle has a different exe name, so it is never matched. Shared
    by ``credential_store._service_name`` so the detection stays in sync if the
    exe stem ever changes.
    """
    return getattr(sys, "frozen", False) and Path(
        sys.executable
    ).stem.lower().startswith("aiwatch")


def is_aiwatch_runtime() -> bool:
    """True when running as the aiwatch binary (process flag or frozen bundle)."""
    return _aiwatch_runtime or is_frozen_aiwatch_bundle()
