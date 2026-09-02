"""Tests for ``runlayer_cli.truststore_init``.

Cross-platform — runs unchanged on macOS, Linux, Windows. ``truststore`` picks
the OS-native backend automatically (Security framework / CryptoAPI / OpenSSL).
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from unittest.mock import patch

import pytest
import truststore

from runlayer_cli import truststore_init


@pytest.fixture(autouse=True)
def _reset_injected_flag():
    """Reset the module-level guard so each test sees a clean state.

    Inject() runs once per process; tests need to re-trigger the inject path
    independently. Restoring after the test prevents leaking the reset into
    later tests that import from runlayer_cli (which may have already run
    inject() via an entrypoint module).
    """
    original = truststore_init._INJECTED
    truststore_init._INJECTED = False
    try:
        yield
    finally:
        truststore_init._INJECTED = original


def test_inject_calls_truststore_once():
    with patch.object(truststore, "inject_into_ssl") as mock_inject:
        truststore_init.inject()
        truststore_init.inject()
        truststore_init.inject()

    assert mock_inject.call_count == 1


def test_inject_sets_injected_flag():
    with patch.object(truststore, "inject_into_ssl"):
        assert truststore_init._INJECTED is False
        truststore_init.inject()
        assert truststore_init._INJECTED is True


def test_inject_raises_on_python_below_3_10():
    fake = (3, 9, 0)
    with patch.object(sys, "version_info", fake):
        with pytest.raises(RuntimeError, match=r"Python 3\.10\+"):
            truststore_init.inject()


def test_inject_does_not_import_truststore_when_version_check_fails():
    """Version guard runs before the truststore import — fail fast on old Pythons.

    Truststore itself requires 3.10+; importing it on 3.9 would raise a less
    helpful error. The guard ensures ours wins.
    """
    fake = (3, 9, 0)
    with patch.object(sys, "version_info", fake):
        with patch.object(truststore, "inject_into_ssl") as mock_inject:
            with pytest.raises(RuntimeError):
                truststore_init.inject()
    assert mock_inject.call_count == 0


def test_default_ssl_context_uses_truststore_after_inject():
    """``ssl.create_default_context()`` returns a ``truststore.SSLContext``.

    Smoke test that injection actually patches the global ssl module, not just
    a no-op. Runs in a subprocess so the global ``ssl`` patch does not leak
    into other tests (truststore patches ``ssl.SSLContext`` for both client
    and server protocols, which breaks tests that spin up TLS servers).
    """
    probe = textwrap.dedent(
        """
        import ssl
        import truststore
        from runlayer_cli import truststore_init

        truststore_init.inject()
        ctx = ssl.create_default_context()
        assert isinstance(ctx, truststore.SSLContext), type(ctx)
        print("ok")
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", probe],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"smoke probe failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert "ok" in result.stdout


# Subprocess probes below verify the docs-mandated boundary: library imports and
# the thin aiwatch module top must not patch ssl; HTTPS-using branches must.

_PROBE_TEMPLATE = textwrap.dedent(
    """
    import truststore

    _calls = []

    def _spy():
        _calls.append(1)

    truststore.inject_into_ssl = _spy

    {import_stmt}

    print(f"calls={{len(_calls)}}")
    """
).strip()


def _run_inject_probe(import_stmt: str) -> subprocess.CompletedProcess[str]:
    probe = _PROBE_TEMPLATE.format(import_stmt=import_stmt)
    return subprocess.run(
        [sys.executable, "-c", probe],
        capture_output=True,
        text=True,
        check=False,
    )


def test_importing_package_does_not_inject():
    """`import runlayer_cli` MUST NOT call inject_into_ssl().

    Truststore docs explicitly forbid inject_into_ssl() from a library/package
    __init__.py because it patches the global ssl module for every importer.
    """
    result = _run_inject_probe("import runlayer_cli")
    assert result.returncode == 0, result.stderr
    assert "calls=0" in result.stdout, (
        f"importing runlayer_cli unexpectedly called inject_into_ssl():\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_importing_aiwatch_entrypoint_defers_injection():
    """The hook daemon-client path must stay truststore-free."""
    result = _run_inject_probe("import runlayer_cli.aiwatch")
    assert result.returncode == 0, result.stderr
    assert "calls=0" in result.stdout, (
        f"importing runlayer_cli.aiwatch unexpectedly called inject_into_ssl():\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_building_aiwatch_cli_injects():
    """Cold CLI construction injects before importing HTTPS-using commands."""
    result = _run_inject_probe(
        "import runlayer_cli.aiwatch as aiwatch; aiwatch._build_app()"
    )
    assert result.returncode == 0, result.stderr
    assert "calls=1" in result.stdout, (
        f"building the aiwatch CLI did not call inject_into_ssl():\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_importing_hook_transcript_worker_injects():
    """Hook transcript stream worker is its own subprocess and must inject."""
    result = _run_inject_probe("import runlayer_cli.hook._transcript_stream_worker")
    assert result.returncode == 0, result.stderr
    assert "calls=1" in result.stdout, (
        f"importing transcript worker did not call inject_into_ssl():\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )
