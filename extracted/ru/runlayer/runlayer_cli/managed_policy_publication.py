"""Invalidate macOS managed-policy caches after runtime-owned plist changes.

The cache notification requires unsupported Apple SPI. Keep it in a bounded
child so a missing symbol, native crash, or hang cannot stop reconciliation.
The child publishes domain names only; it never writes preferences or profiles.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import contextmanager, suppress
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys


POLICY_PUBLICATION_SENTINEL = "__publish_managed_policy__"
PUBLICATION_REJECTED = 2
_MANAGED_ROOT = Path("/Library/Managed Preferences")
_MAX_PAYLOAD_BYTES = 4096
_FAILURE = "macOS managed browser policy publication failed"


def _valid_domains(domains: object) -> bool:
    return (
        isinstance(domains, list)
        and 0 < len(domains) <= 64
        and all(
            isinstance(domain, str)
            and len(domain) <= 255
            and domain.isascii()
            and "." in domain
            and all(
                label and all(char.isalnum() or char in "_-" for char in label)
                for label in domain.split(".")
            )
            for domain in domains
        )
    )


def publish_managed_policy(paths: Iterable[Path]) -> None:
    """Publish even unchanged files: a running reader may have cached absence."""
    if sys.platform != "darwin":
        return
    domains = sorted(
        {
            path.stem
            for path in paths
            if path.parent == _MANAGED_ROOT and path.suffix == ".plist"
        }
    )
    if not domains:
        return
    payload = json.dumps(domains).encode()
    if not _valid_domains(domains) or len(payload) > _MAX_PAYLOAD_BYTES:
        raise OSError(_FAILURE)
    command = (
        [sys.executable, POLICY_PUBLICATION_SENTINEL]
        if getattr(sys, "frozen", False)
        else [sys.executable, "-m", "runlayer_cli.managed_policy_publication"]
    )
    try:
        subprocess.run(
            command,
            input=payload,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        raise OSError(_FAILURE) from None


@contextmanager
def publish_policy_changes(paths: Iterable[Path]) -> Iterator[None]:
    """Publish partial writes too, preserving the original mutation failure."""
    try:
        yield
    except BaseException:
        with suppress(OSError):
            publish_managed_policy(paths)
        raise
    else:
        publish_managed_policy(paths)


def _publish_native(domains: list[str]) -> None:
    import ctypes as c

    cf = c.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
    cf.CFDataCreate.argtypes = [c.c_void_p, c.c_char_p, c.c_long]
    cf.CFDataCreate.restype = c.c_void_p
    cf.CFPropertyListCreateWithData.argtypes = [
        c.c_void_p,
        c.c_void_p,
        c.c_ulong,
        c.c_void_p,
        c.c_void_p,
    ]
    cf.CFPropertyListCreateWithData.restype = c.c_void_p
    cf._CFPreferencesManagementStatusChangedForDomains.argtypes = [c.c_void_p]
    cf._CFPreferencesManagementStatusChangedForDomains.restype = None
    cf.CFRelease.argtypes = [c.c_void_p]
    cf.CFRelease.restype = None
    content = plistlib.dumps(domains)
    data = cf.CFDataCreate(None, content, len(content))
    if not data:
        raise OSError(_FAILURE)
    native_domains = None
    try:
        native_domains = cf.CFPropertyListCreateWithData(None, data, 0, None, None)
        if not native_domains:
            raise OSError(_FAILURE)
        # Public notifications alone leave cfprefsd's managed-source cache stale.
        cf._CFPreferencesManagementStatusChangedForDomains(native_domains)
    finally:
        if native_domains:
            cf.CFRelease(native_domains)
        cf.CFRelease(data)


def main() -> int:
    if sys.platform != "darwin" or os.geteuid() != 0:
        return PUBLICATION_REJECTED
    try:
        payload = sys.stdin.buffer.read(_MAX_PAYLOAD_BYTES + 1)
        domains = json.loads(payload)
        if len(payload) > _MAX_PAYLOAD_BYTES or not _valid_domains(domains):
            return PUBLICATION_REJECTED
        _publish_native(domains)
    except Exception:
        return PUBLICATION_REJECTED
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
