"""TDD for run_hooks orchestrator wiring."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest


def _fake_cfg(model="ollama:qwen3-coder-next"):
    from sage.config import SageConfig
    return SageConfig(default_model=model, rag_top_k=4)


def test_on_session_start_blocks_below_floor(tmp_path):
    from sage.core.run_hooks import on_session_start
    cfg = _fake_cfg(model="ollama:llama3.2")
    result = on_session_start(cfg, tmp_path, skip_readiness=True, skip_skeleton=True)
    assert result.ok is False
    assert "below" in result.message.lower() or "floor" in result.message.lower()


def test_on_session_start_passes_strong_model(tmp_path):
    from sage.core.run_hooks import on_session_start
    cfg = _fake_cfg(model="ollama:qwen3-coder-next")
    result = on_session_start(cfg, tmp_path, skip_readiness=True,
                              skip_skeleton=True)
    assert result.ok is True
    assert result.floor_passed is True


def test_on_session_start_skip_floor_lets_small_model_through(tmp_path):
    from sage.core.run_hooks import on_session_start
    cfg = _fake_cfg(model="ollama:llama3.2")
    result = on_session_start(cfg, tmp_path, skip_floor=True,
                              skip_readiness=True, skip_skeleton=True)
    assert result.ok is True


def test_on_session_start_skeleton_applied_for_empty_dir(tmp_path):
    from sage.core.run_hooks import on_session_start
    cfg = _fake_cfg(model="ollama:qwen3-coder-next")
    result = on_session_start(
        cfg, tmp_path,
        skip_readiness=True,
        user_first_prompt="Build a React + Node.js fullstack app",
    )
    assert result.ok is True
    assert result.skeleton_applied  # something matched
    # Skeleton files actually written
    assert any(tmp_path.rglob("*"))


def test_on_session_start_skeleton_skipped_when_dir_already_populated(tmp_path):
    from sage.core.run_hooks import on_session_start
    # Pre-populate with >5 files
    for i in range(10):
        (tmp_path / f"existing_{i}.txt").write_text(f"file {i}")
    cfg = _fake_cfg()
    result = on_session_start(
        cfg, tmp_path, skip_readiness=True,
        user_first_prompt="Build a React + Node.js fullstack app",
    )
    assert result.skeleton_applied == ""


def test_on_session_start_readiness_failure_aborts(tmp_path):
    from sage.core.run_hooks import on_session_start
    cfg = _fake_cfg()

    def bad_send(prompt, *, model, system):
        return "I would write hello world but I don't really feel like it."

    result = on_session_start(cfg, tmp_path, send_fn=bad_send,
                              skip_skeleton=True)
    assert result.ok is False
    assert "readiness" in result.message.lower() or "FILE:" in result.message


def test_on_pre_turn_grammar_for_tool_prompt(tmp_path):
    from sage.core.run_hooks import on_pre_turn
    cfg = _fake_cfg()
    ctx = on_pre_turn(user_prompt="Implement a server endpoint",
                      cwd=tmp_path, cfg=cfg)
    assert ctx.enforce_grammar is True


def test_on_pre_turn_no_grammar_for_question(tmp_path):
    from sage.core.run_hooks import on_pre_turn
    cfg = _fake_cfg()
    ctx = on_pre_turn(user_prompt="What is OAuth?", cwd=tmp_path, cfg=cfg)
    assert ctx.enforce_grammar is False


def test_on_pre_turn_picks_planner_coder_pair(tmp_path):
    from sage.core.run_hooks import on_pre_turn
    cfg = _fake_cfg()
    ctx = on_pre_turn(
        user_prompt="Implement OAuth", cwd=tmp_path, cfg=cfg,
        available_models=["ollama:llama3.2:latest", "ollama:qwen3-coder-next:latest"],
    )
    # Coder should be the strong coder
    assert "coder" in ctx.coder_model.lower()
    # Planner should be the smaller model
    assert ctx.planner_model != ctx.coder_model


def test_on_post_turn_logs_to_telemetry(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.run_hooks import on_session_start, on_post_turn
    from sage.core.run_hooks import current_telemetry

    cfg = _fake_cfg()
    on_session_start(cfg, tmp_path, skip_readiness=True, skip_skeleton=True)
    on_post_turn(user_prompt="hi", output="ok", cfg=cfg, success=True)
    on_post_turn(user_prompt="bad", output="x", cfg=cfg, success=False,
                 validator_signals=["protocol_leak"])

    log = current_telemetry()
    assert log is not None
    events = log.read()
    assert len(events) == 2
    assert events[1]["validator_signal"] == "protocol_leak"


def test_run_guard_singleton_initialized_after_session_start(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.run_hooks import on_session_start, current_run_guard
    cfg = _fake_cfg()
    on_session_start(cfg, tmp_path, skip_readiness=True, skip_skeleton=True)
    assert current_run_guard() is not None
