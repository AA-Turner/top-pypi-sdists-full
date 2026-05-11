"""TDD for T8 (RAG-pre-turn), T10 (telemetry), T14 (floor model in install)
plus the bootstrap install bug regression."""

from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path

import pytest


# ════════════════════════════════════════════════════════════════════════
# T10: Telemetry
# ════════════════════════════════════════════════════════════════════════

def test_telemetry_logger_appends_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.telemetry import TelemetryLogger
    log = TelemetryLogger(session_id="abc")
    log.log_turn(
        prompt="hi",
        model="ollama:qwen3-coder-next",
        output="FILE: hello.js\n```js\nconsole.log('hi');\n```",
        validator_signal=None,
        success=True,
    )
    log.log_turn(
        prompt="bad",
        model="ollama:tiny",
        output="garbage",
        validator_signal="protocol_leak",
        success=False,
    )
    events = log.read()
    assert len(events) == 2
    assert events[0]["model"] == "ollama:qwen3-coder-next"
    assert events[1]["validator_signal"] == "protocol_leak"


def test_telemetry_aggregator_summarizes_failures(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.telemetry import TelemetryLogger, summarize
    log = TelemetryLogger(session_id="s1")
    for _ in range(5):
        log.log_turn(prompt="q", model="m1", output="ok", validator_signal=None, success=True)
    for _ in range(3):
        log.log_turn(prompt="q", model="m1", output="x", validator_signal="protocol_leak", success=False)
    summary = summarize(session_id="s1")
    assert summary["total"] == 8
    assert summary["failed"] == 3
    assert summary["signals"]["protocol_leak"] == 3


def test_telemetry_redacts_secrets_in_prompt(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.telemetry import TelemetryLogger
    log = TelemetryLogger(session_id="s")
    log.log_turn(
        prompt="my OPENAI_API_KEY=sk-abc123def456 please use it",
        model="m", output="ok", validator_signal=None, success=True,
    )
    events = log.read()
    assert "sk-abc123def456" not in events[0]["prompt"]
    assert "REDACTED" in events[0]["prompt"] or "***" in events[0]["prompt"]


def test_telemetry_handles_missing_session(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.telemetry import summarize
    summary = summarize(session_id="nonexistent")
    assert summary["total"] == 0


# ════════════════════════════════════════════════════════════════════════
# T8 + T14: Bootstrap improvements
# ════════════════════════════════════════════════════════════════════════

def test_bootstrap_install_uses_safe_upgrade_strategy():
    """Regression: --upgrade without --upgrade-strategy=only-if-needed
    bricked the user's venv during the previous bootstrap run."""
    from sage.core.bootstrap import phase_install_optional_deps
    import inspect
    src = inspect.getsource(phase_install_optional_deps)
    # The fix must be in place in the source
    assert "only-if-needed" in src or "--no-deps" in src


def test_bootstrap_floor_model_default_includes_qwen_coder_7b():
    """T14: install flow should pull qwen2.5-coder-7b as the floor model."""
    from sage.core.bootstrap import BootstrapOptions
    opts = BootstrapOptions()
    # The default model list should include either qwen2.5-coder-7b or
    # qwen3-coder-next as the strong coder
    has_coder = any("coder" in m for m in opts.ollama_models)
    assert has_coder, f"no coder in {opts.ollama_models}"


def test_bootstrap_phase_install_calls_pip_with_only_if_needed(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    import importlib

    # Force one missing dep
    def fake_import(name):
        if name == "sqlite_vec":
            raise ImportError("missing")
        return types.SimpleNamespace()
    monkeypatch.setattr(importlib, "import_module", fake_import)

    from sage.core import bootstrap
    captured = {}
    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(bootstrap.subprocess, "run", fake_run)

    bootstrap.phase_install_optional_deps(bootstrap.BootstrapOptions(quiet=True))
    cmd = captured["cmd"]
    assert "pip" in " ".join(cmd) or any(p == "pip" for p in cmd)
    # Must constrain transitive deps so we don't break rich/pip/etc.
    assert "--upgrade-strategy" in cmd or "only-if-needed" in " ".join(cmd) or "--no-deps" in cmd


# ════════════════════════════════════════════════════════════════════════
# T8: RAG pre-turn
# ════════════════════════════════════════════════════════════════════════

def test_rag_pre_turn_helper_skips_when_index_present(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.rag_preturn import ensure_rag_indexed

    # Create a dummy DB so the function thinks an index exists
    import hashlib
    proj_hash = hashlib.sha1(str(tmp_path.resolve()).encode()).hexdigest()[:12]
    db_dir = tmp_path / ".sage" / "rag"
    db_dir.mkdir(parents=True)
    db_path = db_dir / f"{proj_hash}.db"
    db_path.touch()

    # Fake stat → recent file → don't reindex
    result = ensure_rag_indexed(tmp_path, max_age_seconds=3600)
    assert result.indexed is False  # already exists, not stale
    assert result.skipped is True


def test_rag_pre_turn_helper_indexes_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    proj = tmp_path / "p"
    proj.mkdir()
    (proj / "x.py").write_text("def x(): pass")

    # Stub OllamaEmbedder
    class _StubEmbedder:
        dim = 4
        def embed(self, texts): return [[1.0, 0, 0, 0]] * len(texts)

    import sage.core.rag as rag
    monkeypatch.setattr(rag, "OllamaEmbedder", lambda *a, **kw: _StubEmbedder())

    from sage.core.rag_preturn import ensure_rag_indexed
    result = ensure_rag_indexed(proj)
    assert result.indexed is True
