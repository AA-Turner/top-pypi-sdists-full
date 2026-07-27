"""Exhaustive smoke tests for every Sage CLI command + slash command.

main.py is 581KB and imports a lot of sub-modules; we must amortize that
cost across all tests. Strategy:
  - One module-scoped pre-import (no fixture, top-level) loads main.py once
  - Loop-based tests rather than 80 parametrize permutations
  - Slash command coverage is via static dispatcher-branch presence checks
    (real REPL drive would need an open subprocess; not worth it for smoke)
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner


# ── Pre-import (one-time, paid at collection) ───────────────────────

# Resetting the module here means failures load a clear traceback; the
# 581KB import is paid once per pytest invocation.
_main = importlib.import_module("sage.main")
_app = _main.app
_runner = CliRunner()


# ── Command inventories ────────────────────────────────────────────

_TOP_LEVEL = (
    "run", "ask",
    "models", "install", "update",
    "sync", "sync-catalog", "pull",
    "train-all", "train", "use", "rm",
    "login", "logout", "whoami", "fix-llama-cpp",
)
_SECRETS = ("gitignore",)
_SMS = ("setup", "start", "stop", "logs", "status", "devices",
        "unregister", "test", "diagnose")
_SMS_CONTACTS = ("list", "add", "remove")
_CONFIG = ("show", "set", "get", "init")
_EXT = ("search", "detect", "auto-pick", "finetune", "route",
        "internet-test", "bootstrap")
_RAG = ("index", "query", "status")
_CORPUS = ("build", "push", "pull")
_DATASETS = ("list", "mirror")


# ── Helpers ────────────────────────────────────────────────────────

def _help_ok(argv: list[str]) -> tuple[bool, str]:
    """Return (ok, message)."""
    result = _runner.invoke(_app, argv)
    if result.exit_code != 0:
        return False, f"`sage {' '.join(argv)}` exit={result.exit_code}\n{result.stdout}"
    if "Traceback" in result.stdout:
        return False, f"`sage {' '.join(argv)}` printed traceback:\n{result.stdout}"
    return True, ""


# ── Bulk help-doesn't-crash check ──────────────────────────────────

def test_every_top_level_command_help():
    failures = []
    for cmd in _TOP_LEVEL:
        ok, msg = _help_ok([cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "Help failures:\n" + "\n".join(failures)


def test_every_sms_command_help():
    failures = []
    for cmd in _SMS:
        ok, msg = _help_ok(["sms", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "Help failures:\n" + "\n".join(failures)


def test_every_sms_contacts_command_help():
    failures = []
    for cmd in _SMS_CONTACTS:
        ok, msg = _help_ok(["sms", "contacts", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "Help failures:\n" + "\n".join(failures)


def test_every_config_command_help():
    failures = []
    for cmd in _CONFIG:
        ok, msg = _help_ok(["config", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "\n".join(failures)


def test_secrets_help():
    for cmd in _SECRETS:
        ok, msg = _help_ok(["secrets", cmd, "--help"])
        assert ok, msg


def test_every_ext_command_help():
    failures = []
    for cmd in _EXT:
        ok, msg = _help_ok(["ext", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "\n".join(failures)


def test_every_rag_command_help():
    failures = []
    for cmd in _RAG:
        ok, msg = _help_ok(["rag", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "\n".join(failures)


def test_every_corpus_command_help():
    failures = []
    for cmd in _CORPUS:
        ok, msg = _help_ok(["corpus", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "\n".join(failures)


def test_every_datasets_command_help():
    failures = []
    for cmd in _DATASETS:
        ok, msg = _help_ok(["ext", "datasets", cmd, "--help"])
        if not ok:
            failures.append(msg)
    assert not failures, "\n".join(failures)


def test_top_level_help_does_not_crash():
    ok, msg = _help_ok(["--help"])
    assert ok, msg


# ── Functional checks for the most-used commands ──────────────────

def test_config_show_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    import sage.config
    monkeypatch.setattr(sage.config, "CONFIG_PATH", tmp_path / ".sage" / "config.json")
    result = _runner.invoke(_app, ["config", "show"])
    assert result.exit_code == 0


def test_config_set_and_get_round_trip(tmp_path, monkeypatch):
    import sage.config
    cfg_path = tmp_path / ".sage" / "config.json"
    monkeypatch.setattr(sage.config, "CONFIG_PATH", cfg_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    set_result = _runner.invoke(_app, ["config", "set", "temperature", "0.5"])
    assert set_result.exit_code == 0
    get_result = _runner.invoke(_app, ["config", "get", "temperature"])
    assert get_result.exit_code == 0
    assert "0.5" in get_result.stdout


def test_ext_detect_runs_in_empty_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = _runner.invoke(_app, ["ext", "detect"])
    assert result.exit_code == 0


def test_ext_auto_pick_runs(monkeypatch):
    import sage.core.auto_model as am
    monkeypatch.setattr(am, "list_installed_models", lambda: [])
    result = _runner.invoke(_app, ["ext", "auto-pick"])
    assert result.exit_code == 0


def test_ext_route_classifies_simple_prompt(monkeypatch):
    import sage.core.auto_model as am
    from sage.core.auto_model import Candidate
    monkeypatch.setattr(am, "list_installed_models", lambda: [
        Candidate("ollama:llama3.2", "ollama", "llama3.2", 2.0, False),
    ])
    result = _runner.invoke(_app, ["ext", "route", "rename foo to bar"])
    assert result.exit_code == 0
    assert "Difficulty:" in result.stdout


def test_ext_datasets_list_runs():
    result = _runner.invoke(_app, ["ext", "datasets", "list"])
    assert result.exit_code == 0
    assert "codealpaca" in result.stdout or "mbpp" in result.stdout


def test_ext_bootstrap_runs_with_all_no_flags(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    import sage.config
    monkeypatch.setattr(sage.config, "CONFIG_PATH", tmp_path / ".sage" / "config.json")
    monkeypatch.chdir(tmp_path)
    result = _runner.invoke(_app, [
        "ext", "bootstrap", "--quiet",
        "--no-pull-models", "--no-set-default", "--no-prewarm",
        "--no-build-llama-cpp", "--no-install-deps",
        "--no-build-rag", "--no-mirror-datasets",
    ])
    assert result.exit_code == 0


# ── Slash command branch presence (static check on repl.py) ───────

_SLASH_COMMANDS = (
    "/exit", "/quit", "/q",
    "/help", "/clear", "/undo",
    "/model", "/models",
    "/status", "/read", "/test", "/files",
    "/compact", "/think",
    "/autoorg", "/system", "/history",
    "/version", "/update",
)


def test_every_slash_command_has_dispatcher_branch():
    """Each slash command listed in chat must have a `command == "/X"`
    branch in repl.py or cli_core.py's dispatcher. This is a regression guard against
    handlers being silently deleted."""
    src = Path("sage/core/repl.py").read_text("utf-8", errors="replace") + Path("sage/cli_core.py").read_text("utf-8", errors="replace")
    failures = []
    for slash in _SLASH_COMMANDS:
        if f'"{slash}"' not in src and f"'{slash}'" not in src:
            failures.append(slash)
    assert not failures, f"Missing dispatcher branches: {failures}"


# ── Coverage assertions ───────────────────────────────────────────

def test_all_top_level_commands_appear_in_help():
    result = _runner.invoke(_app, ["--help"])
    assert result.exit_code == 0
    missing = [c for c in _TOP_LEVEL if c not in result.stdout]
    assert not missing, f"Missing from --help: {missing}"


def test_ext_subapp_appears_in_help():
    result = _runner.invoke(_app, ["ext", "--help"])
    assert result.exit_code == 0
    missing = [c for c in _EXT if c not in result.stdout]
    assert not missing, f"Missing from `ext --help`: {missing}"
