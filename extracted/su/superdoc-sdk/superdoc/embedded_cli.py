from __future__ import annotations

import platform
from importlib import resources
from pathlib import Path
from typing import Optional

from .embedded_platform import ensure_executable, resolve_companion_binary, resolve_embedded_target
from .errors import SuperDocError


def _resolve_binary_name(target: str) -> str:
    return 'superdoc.exe' if target.startswith('windows-') else 'superdoc'


def _resolve_from_vendor_fallback(target: str) -> Optional[str]:
    """Try #2: legacy _vendor/cli/ path (source/dev environments only).

    This path only exists when running from a source checkout with
    manually staged binaries — it is NOT shipped in published wheels.
    """
    binary_name = _resolve_binary_name(target)
    resource = resources.files('superdoc').joinpath('_vendor', 'cli', target, binary_name)
    try:
        candidate = Path(str(resource))
    except Exception:
        return None
    return str(candidate) if candidate.exists() else None


def resolve_embedded_cli_path() -> str:
    target = resolve_embedded_target()
    if target is None:
        raise SuperDocError(
            'No embedded SuperDoc CLI binary is available for this platform.',
            code='UNSUPPORTED_PLATFORM',
            details={'platform': platform.system(), 'machine': platform.machine()},
        )

    path = resolve_companion_binary(target, _resolve_binary_name(target))

    # Legacy vendor fallback (source/dev only — not shipped in wheels)
    if path is None:
        path = _resolve_from_vendor_fallback(target)

    if path is None:
        raise SuperDocError(
            f'Embedded SuperDoc CLI binary is missing for this platform.\n'
            f'Install the companion package: pip install superdoc-sdk-cli-{target}\n'
            f'Or set SUPERDOC_CLI_BIN to a compatible superdoc binary path.',
            code='CLI_BINARY_MISSING',
            details={'target': target},
        )

    ensure_executable(path)
    return path
