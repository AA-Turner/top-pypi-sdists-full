"""Inject truststore globally so the OS trust store backs all HTTPS clients.

Cross-platform — truststore selects the backend per-OS:
  - macOS: Security framework (login + System Keychain; honors MDM-pushed CAs)
  - Windows: Schannel (Current User + Local Machine cert stores; honors GPO/Intune)
  - Linux: OpenSSL system CA bundle (/etc/ssl/certs, distro-managed)

Per truststore docs, ``inject_into_ssl()`` is for applications/scripts only and
must NOT be called from a library/package's ``__init__.py``. It is invoked
explicitly at the top of each entrypoint module (main.py, aiwatch.py, hook
workers) before any HTTPS-using import.
"""

from __future__ import annotations

import sys

_INJECTED = False
_MIN_PYTHON = (3, 10)


def inject() -> None:
    """Patch ``ssl`` so default contexts delegate to the OS trust store.

    Idempotent — repeated calls are no-ops. Fails fast on Python < 3.10
    (truststore prerequisite); pyproject already enforces this, the runtime
    check is defensive for sdist installs that bypass the metadata.
    """
    global _INJECTED
    if _INJECTED:
        return
    if sys.version_info < _MIN_PYTHON:
        raise RuntimeError(
            f"runlayer requires Python {_MIN_PYTHON[0]}.{_MIN_PYTHON[1]}+ "
            f"(truststore prerequisite); got "
            f"{sys.version_info[0]}.{sys.version_info[1]}"
        )
    import truststore  # noqa: PLC0415 - keep import lazy until version check passes

    truststore.inject_into_ssl()
    _INJECTED = True
