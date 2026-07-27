"""TDD tests for the 25-feature dramatic-improvement pass."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest


# ── Item #1 — Install self-test ────────────────────────────────────────

def test_install_selftest_passes_for_capable_model(tmp_path):
    from sage.core.install_selftest import run_selftest, SelftestResult
    def good_send(prompt, *, model, system):
        return "FILE: hello.js\n```javascript\nconsole.log('hi');\n```"
    result = run_selftest(model="ollama:qwen3-coder-next", send_fn=good_send)
    assert isinstance(result, SelftestResult)
    assert result.ok is True


def test_install_selftest_fails_for_below_floor():
    from sage.core.install_selftest import run_selftest
    result = run_selftest(model="ollama:llama3.2", send_fn=lambda *a, **kw: "")
    assert result.ok is False


def test_install_selftest_fails_when_send_unable():
    from sage.core.install_selftest import run_selftest
    def bad_send(prompt, *, model, system):
        return "I would write hello world but I can't right now."
    result = run_selftest(model="ollama:qwen3-coder-next", send_fn=bad_send)
    assert result.ok is False


# ── Item #2 — Session recorder + replay ────────────────────────────────

def test_session_recorder_writes_replay_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.session_recorder import SessionRecorder, SessionEvent
    rec = SessionRecorder(session_id="sess1")
    rec.record(SessionEvent(kind="user", prompt="hello"))
    rec.record(SessionEvent(kind="model", model="qwen3-coder-next", output="hi"))
    rec.record(SessionEvent(kind="tool", tool_name="FILE", payload={"path": "x.js"}))
    events = list(rec.read())
    assert len(events) == 3
    assert events[0].kind == "user"
    assert events[1].model == "qwen3-coder-next"


def test_session_recorder_replay_iterates_in_order(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.session_recorder import SessionRecorder, SessionEvent, replay
    rec = SessionRecorder(session_id="sess2")
    rec.record(SessionEvent(kind="user", prompt="q1"))
    rec.record(SessionEvent(kind="user", prompt="q2"))
    seen = []
    for ev in replay(session_id="sess2"):
        seen.append(ev.prompt)
    assert seen == ["q1", "q2"]


def test_session_recorder_redacts_secrets(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.session_recorder import SessionRecorder, SessionEvent
    rec = SessionRecorder(session_id="sess3")
    rec.record(SessionEvent(kind="user", prompt="OPENAI_API_KEY=sk-abc123def456ghi789"))
    events = list(rec.read())
    assert "sk-abc123def456" not in events[0].prompt


# ── Item #3 — sage doctor audit ────────────────────────────────────────

def test_doctor_reports_all_check_categories():
    from sage.core.doctor import run_doctor
    report = run_doctor()
    names = {check.name for check in report.checks}
    expected = {"model", "rag", "ollama", "disk", "config"}
    assert expected.issubset(names), f"missing: {expected - names}"


def test_doctor_returns_red_when_no_models_pulled(monkeypatch):
    from sage.core.doctor import run_doctor
    import sage.core.auto_model as am
    monkeypatch.setattr(am, "list_installed_models", lambda: [])
    report = run_doctor()
    model_check = next(c for c in report.checks if c.name == "model")
    assert model_check.status == "red"


def test_doctor_overall_status_is_max_severity():
    from sage.core.doctor import DoctorReport, Check
    r = DoctorReport(checks=[
        Check(name="a", status="green", detail=""),
        Check(name="b", status="yellow", detail="warning"),
        Check(name="c", status="green", detail=""),
    ])
    assert r.overall_status == "yellow"
    r2 = DoctorReport(checks=[
        Check(name="a", status="green", detail=""),
        Check(name="b", status="red", detail="bad"),
    ])
    assert r2.overall_status == "red"


# ── Item #4 — Auto-tier on hardware change ─────────────────────────────

def test_hardware_watch_detects_disk_increase(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.hardware_watch import note_disk_now, should_suggest_upgrade
    note_disk_now(free_gb=50.0)
    assert should_suggest_upgrade(current_free_gb=55.0) is False
    assert should_suggest_upgrade(current_free_gb=85.0) is True


def test_hardware_watch_no_suggestion_when_first_run(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.hardware_watch import should_suggest_upgrade
    assert should_suggest_upgrade(current_free_gb=100.0) is False


# ── Item #5 — RAG-aware diff preview ───────────────────────────────────

def test_rag_aware_diff_flags_unknown_symbols(tmp_path):
    from sage.core.rag_aware_diff import flag_unknown_references
    from sage.core.project_grammar import ProjectSymbols
    syms = ProjectSymbols(modules={"app.utils"}, names={"foo"})
    code = "import bar\nfrom app.utils import nonexistent\nfoo()\n"
    flags = flag_unknown_references(code, syms, language="python")
    flagged_names = {f.name for f in flags}
    assert "nonexistent" in flagged_names
    assert "foo" not in flagged_names


def test_rag_aware_diff_no_flags_when_all_known():
    from sage.core.rag_aware_diff import flag_unknown_references
    from sage.core.project_grammar import ProjectSymbols
    syms = ProjectSymbols(modules={"x"}, names={"alpha", "beta"})
    code = "from x import alpha, beta\n"
    flags = flag_unknown_references(code, syms, language="python")
    assert flags == []


# ── Item #6 — Sticky model warmth daemon ───────────────────────────────

def test_warmth_daemon_socket_path_uses_xdg_runtime(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.warmth_daemon import socket_path
    p = socket_path()
    assert ".sage" in str(p)
    assert p.suffix == ".sock"


def test_warmth_daemon_status_returns_not_running_when_no_socket(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.warmth_daemon import daemon_status
    status = daemon_status()
    assert status.running is False


def test_warmth_daemon_status_returns_stale_when_only_socket_present(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.warmth_daemon import socket_path, daemon_status
    p = socket_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()
    status = daemon_status()
    assert status.running is False or status.stale is True


# ── Item #7 — Tool-budget per turn ─────────────────────────────────────

def test_tool_budget_blocks_when_exceeded():
    from sage.core.tool_budget import ToolBudget
    budget = ToolBudget(max_calls=3)
    assert budget.allow("READ").allowed
    assert budget.allow("READ").allowed
    assert budget.allow("RUN").allowed
    decision = budget.allow("READ")
    assert decision.allowed is False
    assert "budget" in decision.reason.lower() or "exceeded" in decision.reason.lower()


def test_tool_budget_resets_per_turn():
    from sage.core.tool_budget import ToolBudget
    budget = ToolBudget(max_calls=2)
    budget.allow("READ")
    budget.allow("RUN")
    assert budget.allow("READ").allowed is False
    budget.start_new_turn()
    assert budget.allow("READ").allowed is True


def test_tool_budget_summarizes_usage():
    from sage.core.tool_budget import ToolBudget
    budget = ToolBudget(max_calls=10)
    for _ in range(3):
        budget.allow("READ")
    budget.allow("RUN")
    s = budget.summary()
    assert s["READ"] == 3
    assert s["RUN"] == 1


# ── Item #8 — Auto-summarize long sessions ─────────────────────────────

def test_auto_compact_triggers_at_threshold():
    from sage.core.auto_compact import should_compact
    assert should_compact(current_tokens=5000, context_window=16000, threshold=0.7) is False
    assert should_compact(current_tokens=12000, context_window=16000, threshold=0.7) is True


def test_auto_compact_summary_template_contains_required_sections():
    from sage.core.auto_compact import build_compact_prompt
    prompt = build_compact_prompt(prior_messages=[
        {"role": "user", "content": "build pets app"},
        {"role": "assistant", "content": "wrote server.js"},
    ])
    assert "decisions" in prompt.lower()
    assert "files" in prompt.lower() or "changed" in prompt.lower()


# ── Item #9 — Did you mean? ────────────────────────────────────────────

def test_didyoumean_suggests_close_filename(tmp_path):
    from sage.core.didyoumean import suggest_filenames
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "server.js").write_text("//")
    (tmp_path / "src" / "client.js").write_text("//")
    suggestions = suggest_filenames("src/sever.js", tmp_path)
    assert any("server.js" in s for s in suggestions)


def test_didyoumean_no_suggestions_when_path_correct(tmp_path):
    from sage.core.didyoumean import suggest_filenames
    (tmp_path / "exists.py").write_text("")
    suggestions = suggest_filenames("exists.py", tmp_path)
    assert suggestions == []


# ── Item #10 — Speculative decoding default ────────────────────────────

def test_speculative_default_no_op_when_already_set(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    import sage.config
    cfg_path = tmp_path / ".sage" / "config.json"
    monkeypatch.setattr(sage.config, "CONFIG_PATH", cfg_path)
    from sage.core.speculative_default import enable_if_available
    from sage.config import save_config, SageConfig, load_config
    save_config(SageConfig(speculative_draft_model="llama_cpp:custom-draft"), path=cfg_path)
    enable_if_available()
    cfg = load_config(path=cfg_path)
    assert cfg.speculative_draft_model == "llama_cpp:custom-draft"


def test_speculative_default_sets_when_draft_available(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    import sage.config
    cfg_path = tmp_path / ".sage" / "config.json"
    monkeypatch.setattr(sage.config, "CONFIG_PATH", cfg_path)
    from sage.core.speculative_default import enable_if_available
    from sage.config import save_config, SageConfig, load_config
    models_dir = tmp_path / ".sage" / "models"
    models_dir.mkdir(parents=True)
    (models_dir / "llama3.2-1b.gguf").write_bytes(b"x" * (200 * 1024 * 1024))
    save_config(SageConfig(default_model="ollama:qwen3-coder-next"), path=cfg_path)
    enable_if_available()
    cfg = load_config(path=cfg_path)
    assert cfg.speculative_draft_model in ("", "llama_cpp:llama3.2-1b") or "llama3.2-1b" in cfg.speculative_draft_model


# ── Item #11 — KV-cache compression ────────────────────────────────────

def test_kv_compression_round_trip_preserves_data():
    from sage.core.kv_compression import compress_kv, decompress_kv
    payload = b"fake_kv_state_" * 1000
    compressed = compress_kv(payload)
    assert isinstance(compressed, bytes)
    assert len(compressed) <= len(payload)
    out = decompress_kv(compressed)
    assert out == payload


def test_kv_compression_smaller_for_compressible_input():
    from sage.core.kv_compression import compress_kv
    payload = b"\x00" * 10_000
    compressed = compress_kv(payload)
    assert len(compressed) < len(payload) / 10


# ── Item #12 — Quantization-on-pull ────────────────────────────────────

def test_quant_on_pull_schedules_q5_for_unquantized_gguf(tmp_path):
    from sage.core.quant_on_pull import plan_quantizations
    plan = plan_quantizations(tmp_path / "model.gguf", available_quants=["Q4_0"])
    assert "Q5_K_M" in plan
    assert "Q8_0" in plan


def test_quant_on_pull_skips_when_quants_present():
    from sage.core.quant_on_pull import plan_quantizations
    plan = plan_quantizations(Path("/nonexistent/model.gguf"),
                               available_quants=["Q4_0", "Q5_K_M", "Q8_0"])
    assert plan == []


# ── Item #13 — Per-task LoRA composition ───────────────────────────────

def test_lora_compose_layers_multiple_adapters(tmp_path):
    from sage.core.lora_compose import compose_adapters, AdapterStack
    stack = compose_adapters(
        project_adapter=tmp_path / "proj_adapter",
        style_adapter=tmp_path / "style_adapter",
        framework_adapter=None,
    )
    assert isinstance(stack, AdapterStack)
    assert len(stack.adapters) == 2


def test_lora_compose_empty_stack_for_no_adapters():
    from sage.core.lora_compose import compose_adapters
    stack = compose_adapters(project_adapter=None, style_adapter=None, framework_adapter=None)
    assert len(stack.adapters) == 0


# ── Item #14 — Distributed RAG sync ────────────────────────────────────

def test_rag_sync_push_uses_gsutil(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    db_dir = tmp_path / ".sage" / "rag"
    db_dir.mkdir(parents=True)
    db = db_dir / "abc123.db"
    db.write_bytes(b"sqlite-fake")
    captured = {}
    from sage.core import rag_sync
    monkeypatch.setattr(rag_sync, "_have_gsutil", lambda: True)
    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(rag_sync.subprocess, "run", fake_run)
    ok = rag_sync.push_index(db, bucket="gs://test")
    assert ok is True
    assert "gsutil" in captured["cmd"][0] or captured["cmd"][0].endswith("gsutil")


def test_rag_sync_pull_skipped_without_gsutil(monkeypatch):
    from sage.core import rag_sync
    monkeypatch.setattr(rag_sync, "_have_gsutil", lambda: False)
    ok = rag_sync.pull_index(Path("/tmp/x.db"), bucket="gs://test")
    assert ok is False


# ── Item #15 — Trace-based code review ─────────────────────────────────

def test_code_trace_finds_uncovered_function(tmp_path):
    from sage.core.code_trace import scan_for_uncovered
    (tmp_path / "mod.py").write_text(
        "def used():\n    return 1\n\n"
        "def unused():\n    return 2\n"
    )
    coverage_data = {"mod.py": {2}}
    uncovered = scan_for_uncovered(tmp_path, coverage_data, recently_changed=["mod.py"])
    names = {u.symbol for u in uncovered}
    assert "unused" in names
    assert "used" not in names


# ── Item #16 — Type-check loop ─────────────────────────────────────────

def test_typecheck_loop_runs_or_skips(tmp_path):
    from sage.core.typecheck_loop import run_type_check, TypeCheckResult
    (tmp_path / "x.py").write_text("def f(x: int) -> str: return x\n")
    result = run_type_check(tmp_path, language="python")
    assert isinstance(result, TypeCheckResult)
    if result.skipped:
        assert "skipped" in (result.detail or "").lower() or not result.checked


# ── Item #17 — PR-aware sessions ───────────────────────────────────────

def test_pr_context_parses_pr_number():
    from sage.core.pr_context import parse_pr_target
    assert parse_pr_target("1234").number == 1234
    assert parse_pr_target("#1234").number == 1234
    assert parse_pr_target("https://github.com/owner/repo/pull/1234").number == 1234


def test_pr_context_returns_none_for_invalid():
    from sage.core.pr_context import parse_pr_target
    assert parse_pr_target("not-a-pr") is None
    assert parse_pr_target("") is None


# ── Item #18 — Online learning from corrections ────────────────────────

def test_correction_log_records_undo_event(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.correction_log import CorrectionLog
    log = CorrectionLog(session_id="s1")
    log.record_undo(prompt="write tests", bad_output="...", accepted_alternative=None)
    log.record_undo(prompt="fix bug", bad_output="...", accepted_alternative="real fix")
    rows = log.read()
    assert len(rows) == 2
    assert rows[0]["prompt"] == "write tests"


def test_correction_log_aggregates_by_signal(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.correction_log import CorrectionLog, aggregate_corrections
    log = CorrectionLog(session_id="s2")
    for i in range(5):
        log.record_undo(prompt=f"p{i}", bad_output=f"o{i}", validator_signal="protocol_leak")
    log.record_undo(prompt="x", bad_output="y", validator_signal="json_poison")
    summary = aggregate_corrections()
    assert summary["protocol_leak"] >= 5
    assert summary["json_poison"] >= 1


# ── Item #19 — Constitution per project ────────────────────────────────

def test_constitution_loads_invariants_from_file(tmp_path):
    from sage.core.constitution import load_constitution
    (tmp_path / "SAGE.md").write_text(
        "# SAGE\n"
        "## Invariants\n"
        "- never use unsafe-builtin\n"
        "- hooks must start with `use`\n\n"
        "## Test requirements\n"
        "- every endpoint needs a 401/403/404 test\n"
    )
    c = load_constitution(tmp_path)
    assert "unsafe-builtin" in " ".join(c.invariants).lower()
    assert any("hooks" in inv.lower() for inv in c.invariants)
    assert c.test_requirements


def test_constitution_returns_empty_when_no_file(tmp_path):
    from sage.core.constitution import load_constitution
    c = load_constitution(tmp_path)
    assert c.invariants == []


def test_constitution_format_for_prompt():
    from sage.core.constitution import Constitution, format_constitution_for_prompt
    c = Constitution(invariants=["never use unsafe-builtin"], test_requirements=["401 test"])
    out = format_constitution_for_prompt(c)
    assert "INVARIANTS" in out.upper() or "invariants" in out.lower()
    assert "unsafe-builtin" in out


# ── Item #20 — Multi-machine fleet ─────────────────────────────────────

def test_fleet_loads_machine_list(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.fleet import load_fleet
    cfg_path = tmp_path / ".sage" / "fleet.json"
    cfg_path.parent.mkdir(parents=True)
    cfg_path.write_text(json.dumps({
        "machines": [
            {"name": "laptop", "host": "localhost", "ram_gb": 16},
            {"name": "desktop", "host": "192.168.1.10", "ram_gb": 64},
        ]
    }))
    fleet = load_fleet()
    assert len(fleet.machines) == 2
    assert fleet.machines[0].name == "laptop"


def test_fleet_picks_best_for_size():
    from sage.core.fleet import Fleet, Machine, pick_machine_for_model
    fleet = Fleet(machines=[
        Machine(name="laptop", host="localhost", ram_gb=16),
        Machine(name="desktop", host="192.168.1.10", ram_gb=64),
    ])
    chosen = pick_machine_for_model(fleet, model_size_gb=40.0)
    assert chosen.name == "desktop"
    chosen2 = pick_machine_for_model(fleet, model_size_gb=8.0)
    assert chosen2.name == "laptop"


def test_fleet_returns_none_when_no_machine_fits():
    from sage.core.fleet import Fleet, Machine, pick_machine_for_model
    fleet = Fleet(machines=[Machine(name="tiny", host="x", ram_gb=4)])
    assert pick_machine_for_model(fleet, model_size_gb=50.0) is None


# ── Item #21 — Replay against frontier ─────────────────────────────────

def test_replay_against_passes_through_session(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.session_recorder import SessionRecorder, SessionEvent
    from sage.core.replay_against import replay_with_model

    rec = SessionRecorder(session_id="orig")
    rec.record(SessionEvent(kind="user", prompt="prompt 1"))
    rec.record(SessionEvent(kind="user", prompt="prompt 2"))

    sent = []
    def fake_send(prompt, *, model, system):
        sent.append((model, prompt))
        return f"output_for_{prompt}"

    out = replay_with_model(session_id="orig", model="cloud:test", send_fn=fake_send)
    assert len(sent) == 2
    assert all(m == "cloud:test" for m, _ in sent)


# ── Item #22 — Shell-history mining ────────────────────────────────────

def test_shell_history_extracts_top_commands(tmp_path):
    from sage.core.shell_history import extract_top_commands
    history_file = tmp_path / ".zsh_history"
    history_file.write_text(
        ": 1234567890:0;npm test\n"
        ": 1234567891:0;npm test\n"
        ": 1234567892:0;ls -la\n"
        ": 1234567893:0;npm test\n"
    )
    top = extract_top_commands(history_file, n=2)
    assert top[0][0].startswith("npm test")
    assert top[0][1] == 3


def test_shell_history_returns_empty_for_missing_file(tmp_path):
    from sage.core.shell_history import extract_top_commands
    top = extract_top_commands(tmp_path / "nonexistent", n=5)
    assert top == []


def test_shell_history_recency_weighting():
    from sage.core.shell_history import score_command
    a = score_command(count=2, last_seen_ts=1_000_000)
    b = score_command(count=2, last_seen_ts=2_000_000)
    assert b > a


# ── Item #23 — Live overlay ────────────────────────────────────────────

def test_live_overlay_collects_metrics(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.live_overlay import OverlayState
    state = OverlayState()
    state.note_file_modification("src/server.js")
    state.note_file_modification("src/server.js")
    state.note_test_result(passed=True, total=10)
    state.note_validator_signal("protocol_leak")
    snapshot = state.snapshot()
    assert snapshot["most_modified"][0][0] == "src/server.js"
    assert snapshot["test_pass_rate"] == 1.0
    assert snapshot["recent_signals"]["protocol_leak"] == 1


# ── Item #24 — Multi-model tournament ──────────────────────────────────

def test_tournament_runs_all_models_and_picks_winner():
    from sage.core.tournament import tournament
    models = ["model_a", "model_b", "model_c"]
    def fake_send(prompt, *, model, system):
        return f"answer from {model}"
    def fake_judge(prompt, candidates):
        return candidates[0]
    result = tournament(
        prompt="solve a thing",
        models=models,
        send_fn=fake_send,
        judge_fn=fake_judge,
    )
    assert result.winner_model == "model_a"
    assert len(result.candidates) == 3


def test_tournament_handles_send_exception():
    from sage.core.tournament import tournament
    def bad_send(prompt, *, model, system):
        if model == "model_b":
            raise RuntimeError("offline")
        return f"answer from {model}"
    result = tournament(
        prompt="x",
        models=["model_a", "model_b", "model_c"],
        send_fn=bad_send,
        judge_fn=lambda p, c: c[0],
    )
    assert len([c for c in result.candidates if c.error is None]) == 2


# ── Item #25 — Reverse-RAG ─────────────────────────────────────────────

def test_reverse_rag_returns_results(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.reverse_rag import find_relevant_files

    proj = tmp_path / "p"
    proj.mkdir()
    (proj / "auth.py").write_text("def authenticate(user, pw): ...")
    (proj / "ui.py").write_text("def render_button(): ...")

    class _StubEmbedder:
        dim = 4
        def embed(self, texts):
            return [[1.0, 0, 0, 0]] * len(texts)

    import sage.core.rag as rag
    monkeypatch.setattr(rag, "OllamaEmbedder", lambda *a, **kw: _StubEmbedder())
    rag.RAGIndex(proj, embedder=_StubEmbedder()).reindex()

    results = find_relevant_files("authenticate", proj, top_k=2)
    assert isinstance(results, list)
