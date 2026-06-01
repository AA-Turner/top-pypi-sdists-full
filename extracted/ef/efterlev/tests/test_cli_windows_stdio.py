"""Regression test for v0.1.27's Windows stdout/stderr UTF-8 reconfigure.

v0.1.26's release-smoke matrix Windows-2022 cell hit
`UnicodeEncodeError: 'charmap' codec can't encode character '\\u26a0'
in position 2` when `efterlev scan` emitted warning messages
containing the U+26A0 (WARNING SIGN) emoji. Windows console default
encoding is cp1252; cp1252 can't encode U+26A0 (or any other non-
Latin-1 character). v0.1.27 reconfigures stdout + stderr to UTF-8 at
CLI import time on Windows.

This test is platform-independent: it reads `cli/main.py` and asserts
the platform-gated reconfigure block is present. A regression that
removes it would re-break Windows; this test fails on macOS / Linux
dev laptops without needing a Windows runner.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cli import main as cli_main_module


def test_cli_main_reconfigures_stdio_to_utf8_on_windows() -> None:
    """Hard-pin the v0.1.27 fix shape against accidental reversion.

    A regression that drops the stdio.reconfigure block from
    cli/main.py would re-break Windows: any CLI command path that
    emits a non-Latin-1 character (most notably U+26A0 used in
    scan-warning lines) would raise UnicodeEncodeError and crash
    the command. Pin the platform check + both stdio reconfigure
    calls structurally.
    """
    src = Path(cli_main_module.__file__).read_text(encoding="utf-8")

    # The Windows branch must be present.
    assert 'if sys.platform == "win32":' in src, (
        "cli/main.py must include the platform check to reconfigure "
        "stdout/stderr — without it, Windows console (cp1252) can't "
        "encode emoji + non-Latin-1 chars in CLI output."
    )

    # Both stdout AND stderr must be reconfigured.
    assert 'sys.stdout.reconfigure(encoding="utf-8")' in src, (
        "cli/main.py must call sys.stdout.reconfigure(encoding='utf-8') on "
        "Windows so non-Latin-1 chars in stdout output don't crash the CLI."
    )
    assert 'sys.stderr.reconfigure(encoding="utf-8")' in src, (
        "cli/main.py must call sys.stderr.reconfigure(encoding='utf-8') on "
        "Windows — many user-facing warnings go to stderr, not stdout."
    )


def test_warning_emoji_present_in_cli_output_paths() -> None:
    """Sanity: the U+26A0 character that triggered the bug really is
    used in CLI output. If a future cleanup removes all non-ASCII
    chars from CLI strings, the reconfigure becomes a belt-and-
    suspenders defense (still worth keeping). This test documents
    the current usage so removing the reconfigure can't be justified
    by 'we don't emit such characters anymore.'"""
    src = Path(cli_main_module.__file__).read_text(encoding="utf-8")
    # Don't lock the exact count (it can grow); just lock that at
    # least one non-Latin-1 character is used in the file.
    assert "⚠" in src, (
        "If U+26A0 is no longer used in cli/main.py, that's fine — but "
        "document the change here. The reconfigure block stays as a "
        "defense for any future non-Latin-1 character that might be "
        "added (em-dashes, smart quotes, other symbols)."
    )
