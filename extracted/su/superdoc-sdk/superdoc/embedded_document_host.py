from __future__ import annotations

import platform

from .embedded_platform import ensure_executable, resolve_companion_binary, resolve_embedded_target
from .errors import SuperDocError


def _binary_name(target: str) -> str:
    return 'superdoc-document-host.exe' if target.startswith('windows-') else 'superdoc-document-host'


def resolve_embedded_document_host_path() -> str:
    target = resolve_embedded_target()
    if target is None:
        raise SuperDocError(
            'No embedded SuperDoc document host is available for this platform.',
            code='UNSUPPORTED_PLATFORM',
            details={'platform': platform.system(), 'machine': platform.machine()},
        )

    path = resolve_companion_binary(target, _binary_name(target))
    if path is None:
        raise SuperDocError(
            'Embedded SuperDoc document host is missing for this platform.',
            code='DOCUMENT_HOST_BINARY_MISSING',
            details={'target': target},
        )

    ensure_executable(path)
    return path
