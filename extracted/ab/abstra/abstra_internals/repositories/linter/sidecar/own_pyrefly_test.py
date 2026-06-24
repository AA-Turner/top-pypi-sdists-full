"""The linter sidecar child runs its OWN pyrefly (consolidated default).

After dropping the reverse-RPC ("lsp_diagnostics") path, TypeCheckingRule
resolves diagnostics from the child's local pyrefly (the language_server _lsp
singleton, spawned lazily). These tests cover:

- get_diagnostics() always uses the local _lsp (no provider indirection);
- _kill_own_pyrefly() tears down the child's pyrefly before os._exit (the
  graceful shutdown path skips atexit, so without this it would orphan);
- the reverse-RPC machinery is gone (regression lock).
"""

from unittest.mock import MagicMock

from abstra_internals.controllers import language_server
from abstra_internals.repositories.linter.sidecar import __main__ as sidecar_main
from abstra_internals.repositories.linter.sidecar.client import SidecarLinterRepository
from abstra_internals.repositories.linter.sidecar.server import SidecarLinterServer

# ── diagnostics route: local pyrefly only ───────────────────────────


def test_get_diagnostics_uses_local_lsp(monkeypatch):
    fake_lsp = MagicMock()
    fake_lsp.get_diagnostics.return_value = [{"severity": 1}]
    monkeypatch.setattr(language_server, "_lsp", fake_lsp)

    result = language_server.get_diagnostics("print(1)")

    assert result == [{"severity": 1}]
    fake_lsp.get_diagnostics.assert_called_once_with("print(1)")


def test_get_diagnostics_degrades_to_empty_on_error(monkeypatch):
    fake_lsp = MagicMock()
    fake_lsp.get_diagnostics.side_effect = RuntimeError("pyrefly down")
    monkeypatch.setattr(language_server, "_lsp", fake_lsp)

    assert language_server.get_diagnostics("print(1)") == []


# ── orphan prevention: kill the owned pyrefly before os._exit ────────


def test_kill_own_pyrefly_kills_running_process(monkeypatch):
    proc = MagicMock()
    proc.poll.return_value = None  # still running
    fake_lsp = MagicMock()
    fake_lsp._process = proc
    monkeypatch.setattr(language_server, "_lsp", fake_lsp)

    sidecar_main._kill_own_pyrefly()

    proc.kill.assert_called_once()


def test_kill_own_pyrefly_noop_when_no_process(monkeypatch):
    fake_lsp = MagicMock()
    fake_lsp._process = None
    monkeypatch.setattr(language_server, "_lsp", fake_lsp)

    # Must not raise.
    sidecar_main._kill_own_pyrefly()


def test_kill_own_pyrefly_skips_already_dead_process(monkeypatch):
    proc = MagicMock()
    proc.poll.return_value = 0  # already exited
    fake_lsp = MagicMock()
    fake_lsp._process = proc
    monkeypatch.setattr(language_server, "_lsp", fake_lsp)

    sidecar_main._kill_own_pyrefly()

    proc.kill.assert_not_called()


# ── regression lock: reverse-RPC machinery is gone ──────────────────


def test_reverse_rpc_machinery_removed():
    # The editor no longer exposes a diagnostics-provider hook...
    assert not hasattr(language_server, "set_diagnostics_provider")
    assert not hasattr(language_server, "_diagnostics_provider")
    # ...the child server no longer sends reverse diagnostics requests...
    assert not hasattr(SidecarLinterServer, "request_diagnostics")
    # ...and the editor client no longer runs a reverse-request loop.
    assert not hasattr(SidecarLinterRepository, "_reverse_loop")
    assert not hasattr(SidecarLinterRepository, "_ensure_reverse_thread_locked")
