"""Unit tests for the fidelity harness's platform-routing logic.

The fidelity harness compares VFS output against GNU coreutils output. On Linux
the system binaries under /usr/bin are already GNU; on macOS brew installs them
as `g`-prefixed binaries. Either way the harness must run the resolved binary
while keeping argv[0] = the SHORT command name, because real GNU coreutils label
their diagnostics from the parent-supplied argv[0] ("ls: ...", "rmdir: ...").
Passing the resolved path as argv[0] (the old behaviour) made every error
comparison fail on Linux/CI with a "/usr/bin/ls: ..." prefix. These tests pin
that mechanism without depending on brew being installed.
"""
from __future__ import annotations

import asyncio
import subprocess

import pytest

from . import harness as harness_mod
from .harness import FidelityHarness, _resolve_gnu_binary


def test_real_runner_keeps_short_argv0_and_routes_via_executable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A shell-script shim can't model this (a script's $0 is the script path,
    # never the caller's argv[0]), so we capture the actual subprocess call and
    # assert the two properties that make real GNU coreutils emit the canonical
    # short-name prefix: argv[0] is the short command name, and the resolved GNU
    # binary is supplied out-of-band via executable=.
    resolved = "/opt/gnu/bin/gls"
    monkeypatch.setattr(
        harness_mod,
        "_resolve_gnu_binary",
        lambda name: resolved if name == "ls" else None,
    )

    captured: dict[str, object] = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        captured["executable"] = kwargs.get("executable")
        return subprocess.CompletedProcess(args, 2, stdout=b"", stderr=b"")

    monkeypatch.setattr(harness_mod.subprocess, "run", fake_run)

    h = FidelityHarness({})
    try:
        res = asyncio.run(h.run_real(["ls", "/missing"]))
    finally:
        h.cleanup()

    assert res.exit_code == 2
    # argv[0] stays the short name -> child diagnostics read "ls: ...".
    assert captured["args"][0] == "ls"
    # the real program is the resolved GNU binary, passed independently of argv.
    assert captured["executable"] == resolved


def test_real_runner_no_executable_override_for_non_coreutils(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Commands outside the coreutils allowlist are run by PATH lookup of argv[0]
    # (executable=None), never rerouted.
    captured: dict[str, object] = {}

    def fake_run(args, **kwargs):
        captured["args"] = args
        captured["executable"] = kwargs.get("executable")
        return subprocess.CompletedProcess(args, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(harness_mod.subprocess, "run", fake_run)

    h = FidelityHarness({})
    try:
        asyncio.run(h.run_real(["some_custom_tool", "--flag"]))
    finally:
        h.cleanup()

    assert captured["args"][0] == "some_custom_tool"
    assert captured["executable"] is None


def test_resolve_gnu_binary_finds_nothing_outside_brew_paths() -> None:
    # Sanity check on the resolver itself: in absence of brew coreutils on
    # macOS, _resolve_gnu_binary should return None for `ls`.
    import sys

    if sys.platform.startswith("linux"):
        # On Linux we genuinely expect to find /usr/bin/ls.
        assert _resolve_gnu_binary("ls") is not None
    else:
        # On macOS without brew coreutils, gls won't be in /opt/homebrew/bin.
        # If brew coreutils ARE installed, this assertion is harmless — the
        # path will be a real one, which is also valid.
        result = _resolve_gnu_binary("ls")
        assert result is None or result.endswith("/gls")
