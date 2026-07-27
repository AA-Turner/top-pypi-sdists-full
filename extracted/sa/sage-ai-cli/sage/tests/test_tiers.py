"""Tests for Tier A/B/C modules + backfill for previously thin Wave 1-5 coverage.

Run:
    .venv/bin/python -m pytest sage/tests/test_tiers.py -v --no-cov

Conventions:
  - Network mocked via httpx.MockTransport or monkeypatched callables
  - GCS mocked by stubbing _have_gsutil / subprocess
  - Subprocess for build/requantize tested via dry-run paths
  - Heavy ML deps (mlx, transformers, peft) NOT installed; we test the
    decision logic, not the actual training
"""

from __future__ import annotations

import json
import os
import struct
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path

import pytest


# ────────────────────────────────────────────────────────────────────────
# TIER A
# ────────────────────────────────────────────────────────────────────────

# ── build_llama_cpp_optimized ─────────────────────────────────────────

def test_build_picks_apple_silicon_flags(monkeypatch):
    from sage.scripts import build_llama_cpp_optimized as b
    monkeypatch.setattr(b.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(b.platform, "machine", lambda: "arm64")
    flags = b.pick_cmake_flags()
    assert "-DGGML_METAL=ON" in flags
    assert "-DGGML_NATIVE=ON" in flags
    assert "-DGGML_ACCELERATE=ON" in flags


def test_build_picks_linux_cuda_when_nvidia_smi_present(monkeypatch):
    from sage.scripts import build_llama_cpp_optimized as b
    monkeypatch.setattr(b.platform, "system", lambda: "Linux")
    monkeypatch.setattr(b.platform, "machine", lambda: "x86_64")
    class _R:
        returncode = 0
    monkeypatch.setattr(b.subprocess, "run", lambda *a, **kw: _R())
    flags = b.pick_cmake_flags()
    assert "-DGGML_CUDA=ON" in flags


def test_build_force_flags_override_detection(monkeypatch):
    from sage.scripts import build_llama_cpp_optimized as b
    assert b.pick_cmake_flags(force_cpu=True) == ["-DGGML_NATIVE=ON"]
    assert "-DGGML_CUDA=ON" in b.pick_cmake_flags(force_cuda=True)


def test_build_command_constructs_pip_install():
    from sage.scripts import build_llama_cpp_optimized as b
    cmd, env = b.build_command(["-DGGML_NATIVE=ON"])
    assert "pip" in cmd
    assert "llama-cpp-python" in cmd
    assert env["CMAKE_ARGS"] == "-DGGML_NATIVE=ON"
    assert env["FORCE_CMAKE"] == "1"


def test_build_dry_run_returns_zero(monkeypatch, capsys):
    from sage.scripts import build_llama_cpp_optimized as b
    monkeypatch.setattr(b.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(b.platform, "machine", lambda: "arm64")
    rc = b.main(["--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "CMAKE_ARGS=" in out


# ── requantize ────────────────────────────────────────────────────────

def test_requantize_rejects_unknown_quant():
    from sage.scripts import requantize as r
    with pytest.raises(ValueError):
        r.requantize(Path("/tmp/x"), Path("/tmp/y"), quant="Q99_BOGUS")


def test_requantize_dry_run(monkeypatch, tmp_path, capsys):
    from sage.scripts import requantize as r
    src = tmp_path / "model.gguf"
    src.write_bytes(b"GGUF" + b"\x00" * 20)
    rc = r.main([str(src), "--dry-run", "--quant", "Q5_K_M"])
    assert rc == 0
    assert "Would" in capsys.readouterr().out


def test_requantize_main_errors_on_missing_input(tmp_path, capsys):
    from sage.scripts import requantize as r
    rc = r.main([str(tmp_path / "missing.gguf"), "--dry-run"])
    assert rc == 1


def test_requantize_valid_quants_includes_q5_k_m():
    from sage.scripts.requantize import VALID_QUANTS
    assert "Q5_K_M" in VALID_QUANTS
    assert "Q4_0" in VALID_QUANTS


# ── keep_alive ────────────────────────────────────────────────────────

def test_keep_alive_kwargs_adds_duration():
    from sage.core.keep_alive import keep_alive_kwargs, DEFAULT_KEEP_ALIVE
    out = keep_alive_kwargs({"model": "x"})
    assert out["model"] == "x"
    assert out["keep_alive"] == DEFAULT_KEEP_ALIVE
    custom = keep_alive_kwargs({}, duration="2h")
    assert custom["keep_alive"] == "2h"


def test_keep_alive_prewarm_returns_false_on_network_error(monkeypatch):
    from sage.core import keep_alive

    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def post(self, *a, **kw):
            raise RuntimeError("connection refused")

    fake_httpx = types.SimpleNamespace(Client=_Client)
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    assert keep_alive.prewarm("anymodel") is False


def test_keep_alive_prewarm_returns_true_on_200(monkeypatch):
    from sage.core import keep_alive

    class _Resp:
        status_code = 200

    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def post(self, *a, **kw): return _Resp()

    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    assert keep_alive.prewarm("anymodel") is True


# ── code_embedder ─────────────────────────────────────────────────────

def test_code_embedder_registry_has_known_entries():
    from sage.core.code_embedder import CodeEmbedderRegistry
    assert "nomic-embed-text" in CodeEmbedderRegistry
    assert "bge-code-v1" in CodeEmbedderRegistry
    assert "unixcoder-base" in CodeEmbedderRegistry


def test_make_embedder_default_returns_ollama():
    from sage.core.code_embedder import make_embedder
    from sage.core.rag import OllamaEmbedder
    emb = make_embedder()
    assert isinstance(emb, OllamaEmbedder)
    assert emb.dim == 768


def test_make_embedder_unknown_falls_back_to_ollama():
    from sage.core.code_embedder import make_embedder
    from sage.core.rag import OllamaEmbedder
    emb = make_embedder("totally-made-up-name")
    assert isinstance(emb, OllamaEmbedder)


def test_make_embedder_huggingface_errors_without_dep(monkeypatch):
    from sage.core.code_embedder import make_embedder
    emb = make_embedder("unixcoder-base")
    # Lazy-loaded; embed() should raise the install hint
    monkeypatch.setitem(sys.modules, "sentence_transformers", None)
    with pytest.raises(RuntimeError, match="sentence-transformers"):
        emb.embed(["hi"])


# ── llama_cpp provider wiring (Wave 5 hooks) ──────────────────────────

def test_llama_cpp_speculative_kwargs_empty_when_unset(tmp_path, monkeypatch):
    from sage.config import SageConfig
    from sage.providers.llama_cpp import LlamaCppProvider
    cfg = SageConfig()  # speculative_draft_model = ""
    p = LlamaCppProvider(cfg)
    assert p._maybe_speculative_kwargs() == {}


def test_llama_cpp_prefix_cache_skipped_when_no_model_loaded():
    from sage.config import SageConfig
    from sage.providers.llama_cpp import LlamaCppProvider
    p = LlamaCppProvider(SageConfig())
    assert p._try_load_prefix_cache("noname", "system prompt") is False
    p._save_prefix_cache("noname", "system prompt")  # no-op, must not raise


# ────────────────────────────────────────────────────────────────────────
# TIER B
# ────────────────────────────────────────────────────────────────────────

# ── ast_chunker ───────────────────────────────────────────────────────

def test_ast_chunker_python_regex_splits_functions(tmp_path):
    from sage.core.ast_chunker import chunk_python_regex
    text = (
        "import os\n"
        "\n"
        "def foo():\n"
        "    return 1\n"
        "\n"
        "def bar(x):\n"
        "    return x + 1\n"
        "\n"
        "class Baz:\n"
        "    pass\n"
    )
    chunks = chunk_python_regex(text, "x.py")
    names = [c.symbol for c in chunks]
    assert any("foo" in n for n in names)
    assert any("bar" in n for n in names)
    assert any("Baz" in n for n in names)


def test_ast_chunker_jsts_regex_splits_exports():
    from sage.core.ast_chunker import chunk_jsts_regex
    text = (
        "export function alpha() {}\n"
        "\n"
        "export class Beta {}\n"
        "\n"
        "export const gamma = () => {}\n"
    )
    chunks = chunk_jsts_regex(text, "x.ts")
    names = [c.symbol for c in chunks]
    assert any("alpha" in n for n in names)
    assert any("Beta" in n for n in names)
    assert any("gamma" in n for n in names)


def test_ast_chunker_dispatches_by_suffix(tmp_path):
    from sage.core.ast_chunker import chunk_ast
    p = tmp_path / "src" / "thing.py"
    p.parent.mkdir()
    p.write_text("def hello():\n    return 1\n")
    chunks = chunk_ast(p, root=tmp_path)
    assert chunks
    assert chunks[0].file_path == "src/thing.py"


def test_ast_chunker_unknown_extension_returns_linewise(tmp_path):
    from sage.core.ast_chunker import chunk_ast
    p = tmp_path / "weird.xyz"
    p.write_text("just some text\nmore text\n")
    chunks = chunk_ast(p, root=tmp_path)
    assert len(chunks) == 1
    assert chunks[0].symbol == "block:0"


def test_ast_chunker_empty_file_returns_empty(tmp_path):
    from sage.core.ast_chunker import chunk_ast
    p = tmp_path / "empty.py"
    p.write_text("")
    assert chunk_ast(p, root=tmp_path) == []


def test_ast_chunker_available_backend_is_string():
    from sage.core.ast_chunker import available_backend
    assert available_backend() in {"tree-sitter", "regex"}


# ── rag_watcher ───────────────────────────────────────────────────────

def test_rag_watcher_polling_calls_on_change(tmp_path, monkeypatch):
    """Drive _watch_with_polling for one iteration via monkeypatched sleep."""
    from sage.core import rag_watcher
    cwd = tmp_path
    (cwd / "a.py").write_text("def a(): pass")

    calls: list = []
    iterations = [0]

    def fake_sleep(s):
        iterations[0] += 1
        if iterations[0] >= 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(rag_watcher.time, "sleep", fake_sleep)
    rag_watcher._watch_with_polling(cwd, interval=0.01,
                                    on_change=lambda p: calls.append(p))
    assert calls  # at least one change registered (the initial scan)


def test_rag_watcher_main_force_polling_returns_zero(tmp_path, monkeypatch):
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    from sage.core import rag_watcher
    monkeypatch.setattr(rag_watcher.time, "sleep",
                        lambda s: (_ for _ in ()).throw(KeyboardInterrupt))
    rc = rag_watcher.main(["--cwd", str(tmp_path), "--force-polling", "--interval", "0.01"])
    assert rc == 0


# ── distill ───────────────────────────────────────────────────────────

def test_distill_logger_writes_and_reads(tmp_path):
    from sage.core.distill import DistillLogger, DistillEvent
    log = DistillLogger(session_id="abc", root=tmp_path)
    log.log(DistillEvent(user_prompt="q1", final_response="a1", used_tools=["rag"]))
    log.log(DistillEvent(user_prompt="q2", final_response="a2", used_tools=[]))
    events = log.events()
    assert len(events) == 2
    assert events[0].user_prompt == "q1"


def test_distill_compile_filters_to_tool_augmented(tmp_path):
    from sage.core.distill import DistillLogger, DistillEvent, compile_into_corpus
    log = DistillLogger(session_id="s1", root=tmp_path)
    log.log(DistillEvent(user_prompt="q_no_tools", final_response="a", used_tools=[]))
    log.log(DistillEvent(user_prompt="q_with_tools", final_response="a2",
                         used_tools=["rag", "web_search"]))
    out = compile_into_corpus(distill_root=tmp_path,
                              output=tmp_path / "compiled.jsonl",
                              only_tool_augmented=True)
    lines = [l for l in out.read_text().splitlines() if l.strip()]
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert obj["instruction"] == "q_with_tools"


def test_distill_compile_includes_all_when_filter_off(tmp_path):
    from sage.core.distill import DistillLogger, DistillEvent, compile_into_corpus
    log = DistillLogger(session_id="s2", root=tmp_path)
    log.log(DistillEvent(user_prompt="q", final_response="a", used_tools=[]))
    out = compile_into_corpus(distill_root=tmp_path,
                              output=tmp_path / "c.jsonl",
                              only_tool_augmented=False)
    assert out.read_text().strip()


# ── vllm_serve ────────────────────────────────────────────────────────

def test_vllm_launch_command_includes_model_and_port():
    from sage.scripts.vllm_serve import launch_command
    cmd = launch_command("Qwen/Qwen2.5-Coder-7B", port=9001)
    assert "--model" in cmd
    assert "Qwen/Qwen2.5-Coder-7B" in cmd
    assert "--port" in cmd
    assert "9001" in cmd


def test_vllm_main_dry_run_zero_when_deps_missing(monkeypatch, capsys):
    from sage.scripts import vllm_serve as v
    monkeypatch.setattr(v, "have_cuda", lambda: False)
    monkeypatch.setattr(v, "have_vllm", lambda: False)
    rc = v.main(["--model", "x", "--dry-run"])
    assert rc == 0
    out = capsys.readouterr()
    assert "Launch:" in out.out


def test_vllm_main_nonzero_when_no_cuda_and_not_dry_run(monkeypatch):
    from sage.scripts import vllm_serve as v
    monkeypatch.setattr(v, "have_cuda", lambda: False)
    monkeypatch.setattr(v, "have_vllm", lambda: True)
    rc = v.main(["--model", "x"])
    assert rc != 0


# ────────────────────────────────────────────────────────────────────────
# TIER C
# ────────────────────────────────────────────────────────────────────────

# ── lora_swap ─────────────────────────────────────────────────────────

def test_lora_swap_returns_missing_when_no_corpus(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.lora_swap import LoraSwap
    swap = LoraSwap(cfg=SageConfig())
    resolved = swap.adapter_for(tmp_path / "proj", base_model="ollama:foo")
    assert resolved.source == "missing"
    assert resolved.adapter_dir is None


def test_lora_swap_returns_local_when_cache_hit(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.lora_swap import LoraSwap
    from sage.training.corpus import CorpusManager, TrainingExample

    cwd = tmp_path / "proj"
    cwd.mkdir()
    cm = CorpusManager()
    snap = cm.write_snapshot(cwd, [TrainingExample(instruction="i", input="", output="o")],
                             upload=False)
    # Pre-place a fake local adapter
    swap = LoraSwap(cfg=SageConfig())
    ref = swap._ref_for(cwd, "ollama:fakebase")
    ref.local_dir().mkdir(parents=True, exist_ok=True)
    (ref.local_dir() / "adapter.safetensors").write_bytes(b"ok")

    resolved = swap.adapter_for(cwd, base_model="ollama:fakebase")
    assert resolved.source == "local"
    assert resolved.adapter_dir is not None


# ── moe_pipeline ──────────────────────────────────────────────────────

def test_moe_pipeline_full_flow():
    from sage.core.moe_pipeline import MoEPipeline, Specialist
    calls: list[tuple[str, str]] = []

    def send(prompt, *, model, system):
        calls.append((model, system[:20]))
        if "AVAILABLE SPECIALISTS" in prompt:
            return "coder, reviewer"
        if "SPECIALIST OUTPUTS" in prompt:
            return "FINAL SYNTHESIS"
        if "CODER" in system.upper():
            return "code goes here"
        if "REVIEWER" in system.upper():
            return "looks good"
        return "?"

    pipeline = MoEPipeline(
        send,
        planner=Specialist(name="planner", model="planner-m", system_prompt="PLANNER"),
        specialists={
            "coder":    Specialist(name="coder",    model="coder-m",    system_prompt="CODER",    description="writes code"),
            "reviewer": Specialist(name="reviewer", model="reviewer-m", system_prompt="REVIEWER", description="reviews code"),
        },
        max_specialists=3,
    )
    result = pipeline.run("build a thing")
    assert result.success
    assert result.plan == ["coder", "reviewer"]
    assert result.final == "FINAL SYNTHESIS"
    # planner should have been consulted twice (planning + synthesis)
    planner_calls = [c for c in calls if c[0] == "planner-m"]
    assert len(planner_calls) == 2


def test_moe_pipeline_aborts_when_planner_picks_nothing():
    from sage.core.moe_pipeline import MoEPipeline, Specialist
    pipeline = MoEPipeline(
        lambda *a, **kw: "garbage,not,a,specialist",
        planner=Specialist(name="p", model="p-m", system_prompt="P"),
        specialists={"coder": Specialist("coder", "m", "C", "writes")},
    )
    result = pipeline.run("hi")
    assert result.success is False
    assert result.plan == []


# ── project_grammar ───────────────────────────────────────────────────

def test_project_grammar_extracts_python_symbols(tmp_path):
    from sage.core.project_grammar import extract_project_symbols
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("")
    (tmp_path / "pkg" / "mod.py").write_text(
        "def public_one():\n    pass\n\n"
        "class PublicTwo:\n    pass\n\n"
        "def _private():\n    pass\n"
    )
    syms = extract_project_symbols(tmp_path)
    assert "public_one" in syms.names
    assert "PublicTwo" in syms.names
    assert "_private" not in syms.names


def test_project_grammar_extracts_js_exports(tmp_path):
    from sage.core.project_grammar import extract_project_symbols
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "x.ts").write_text(
        "export function alpha() {}\n"
        "export class Beta {}\n"
        "export const gamma = () => {}\n"
    )
    syms = extract_project_symbols(tmp_path)
    assert "alpha" in syms.names
    assert "Beta" in syms.names
    assert "gamma" in syms.names


def test_project_grammar_build_includes_real_symbols():
    from sage.core.project_grammar import ProjectSymbols, build_import_grammar
    syms = ProjectSymbols(modules={"app.utils"}, names={"foo", "Bar"})
    g = build_import_grammar(syms)
    assert '"app.utils"' in g
    assert '"foo"' in g
    assert '"Bar"' in g
    assert "from " in g
    assert "import " in g


def test_project_grammar_handles_empty_symbols():
    from sage.core.project_grammar import ProjectSymbols, build_import_grammar
    g = build_import_grammar(ProjectSymbols())
    # Should not crash; placeholder produces a syntactically valid grammar
    assert "_no_symbols_" in g


# ── auto_verify ───────────────────────────────────────────────────────

def test_auto_verify_infers_pytest_for_python_project(tmp_path, monkeypatch):
    from sage.core.auto_verify import infer_test_command
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    monkeypatch.setattr("shutil.which", lambda c: "/usr/bin/" + c)
    cmd = infer_test_command(tmp_path)
    assert cmd is not None and cmd[0] == "pytest"


def test_auto_verify_infers_npm_for_js_project(tmp_path, monkeypatch):
    from sage.core.auto_verify import infer_test_command
    (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
    monkeypatch.setattr("shutil.which", lambda c: "/usr/bin/" + c if c == "npm" else None)
    cmd = infer_test_command(tmp_path)
    assert cmd is not None and cmd[0] == "npm"


def test_auto_verify_returns_none_for_empty_project(tmp_path):
    from sage.core.auto_verify import infer_test_command
    assert infer_test_command(tmp_path) is None


def test_auto_verify_run_skips_when_no_command(tmp_path):
    from sage.core.auto_verify import ProjectVerifier
    out = ProjectVerifier(tmp_path).run()
    assert out.ok is True
    assert out.skipped_reason


def test_auto_verify_loop_iterates_on_failure(tmp_path, monkeypatch):
    from sage.core.auto_verify import ProjectVerifier, VerifyOutcome
    v = ProjectVerifier(tmp_path)
    iterations = [0]
    outcomes = [
        VerifyOutcome(ok=False, command="x", stdout_tail="", stderr_tail="bad", duration_s=0.0),
        VerifyOutcome(ok=False, command="x", stdout_tail="", stderr_tail="still bad", duration_s=0.0),
        VerifyOutcome(ok=True, command="x", stdout_tail="ok", stderr_tail="", duration_s=0.0),
    ]
    monkeypatch.setattr(v, "run", lambda: outcomes[iterations[0]])

    def regen(_msg):
        iterations[0] += 1

    final, history = v.loop(regenerate_fn=regen, max_iterations=3)
    assert final.ok is True
    assert len(history) == 3


# ── federated_few_shot ───────────────────────────────────────────────

def test_federated_few_shot_pull_noop_when_no_gsutil(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("sage.core.federated_few_shot._have_gsutil", lambda: False)
    from sage.config import SageConfig
    from sage.core.federated_few_shot import FederatedFewShot
    fed = FederatedFewShot(tmp_path / "proj", cfg=SageConfig())
    assert fed.pull_and_merge() == 0
    assert fed.push() is False


def test_federated_few_shot_merge_dedups(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.federated_few_shot import FederatedFewShot
    from sage.core.few_shot import FewShotExample

    cwd = tmp_path / "proj"
    cwd.mkdir()
    fed = FederatedFewShot(cwd, cfg=SageConfig())
    fed.local.record_accept("p1", "r1")
    fed.local.record_accept("p2", "r2")

    # Construct a "remote" payload with one duplicate + one new
    remote = {
        "examples": [
            {"timestamp": time.time(), "prompt": "p1", "response": "r1",
             "accepted": True, "tags": []},
            {"timestamp": time.time(), "prompt": "p3", "response": "r3",
             "accepted": True, "tags": []},
        ]
    }
    monkeypatch.setattr("sage.core.federated_few_shot._have_gsutil", lambda: True)

    # Stub subprocess.run so the gsutil cp "downloads" our payload.
    # gsutil cp <src> <dst>: cmd = ["gsutil", "-q", "cp", src, dst] → dst is cmd[4]
    import sage.core.federated_few_shot as ff
    def fake_run(cmd, capture_output=True, text=True, timeout=60):
        Path(cmd[4]).write_text(json.dumps(remote))
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    monkeypatch.setattr(ff.subprocess, "run", fake_run)

    added = fed.pull_and_merge()
    assert added == 1
    prompts = [e.prompt for e in fed.local._examples]
    assert "p3" in prompts


# ── search_provider ─────────────────────────────────────────────────

def test_make_provider_returns_correct_backend():
    from sage.core.search_provider import (
        make_provider, DuckDuckGoBackend, BraveBackend, SearXNGBackend,
    )
    assert isinstance(make_provider("duckduckgo"), DuckDuckGoBackend)
    assert isinstance(make_provider("brave"), BraveBackend)
    assert isinstance(make_provider("searxng"), SearXNGBackend)
    # Unknown → DDG fallback
    assert isinstance(make_provider("nope"), DuckDuckGoBackend)


def test_brave_backend_returns_empty_without_key(monkeypatch):
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    from sage.core.search_provider import BraveBackend
    b = BraveBackend()
    assert b.search("anything") == []


def test_searxng_backend_returns_empty_without_url(monkeypatch):
    monkeypatch.delenv("SAGE_SEARXNG_URL", raising=False)
    from sage.core.search_provider import SearXNGBackend
    s = SearXNGBackend()
    assert s.search("anything") == []


def test_brave_backend_parses_response(monkeypatch):
    from sage.core import search_provider
    class _Resp:
        status_code = 200
        def json(self): return {
            "web": {"results": [
                {"title": "T1", "url": "https://t1", "description": "d1"},
                {"title": "T2", "url": "https://t2", "description": "d2"},
            ]}
        }
    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get(self, *a, **kw): return _Resp()
    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    b = search_provider.BraveBackend(api_key="fake")
    results = b.search("anything", limit=2)
    assert len(results) == 2
    assert results[0].title == "T1"


# ────────────────────────────────────────────────────────────────────────
# BACKFILL: previously low-coverage Wave 1-5 modules
# ────────────────────────────────────────────────────────────────────────

# ── auto_model: Ollama probe + filesystem scan ───────────────────────

def test_auto_model_ollama_models_returns_empty_on_network_error(monkeypatch):
    from sage.core import auto_model
    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def post(self, *a, **kw): raise RuntimeError("nope")
    fake_httpx = types.SimpleNamespace(
        get=lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("nope"))
    )
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    assert auto_model._ollama_models() == []


def test_auto_model_ollama_models_parses_tags(monkeypatch):
    from sage.core import auto_model
    payload = {"models": [
        {"name": "qwen3-coder-next:latest", "size": 51 * 1024 ** 3},
        {"name": "llama3.2:latest", "size": 2 * 1024 ** 3},
    ]}
    class _Resp:
        status_code = 200
        def json(self): return payload
    fake_httpx = types.SimpleNamespace(get=lambda *a, **kw: _Resp())
    monkeypatch.setitem(sys.modules, "httpx", fake_httpx)
    out = auto_model._ollama_models()
    assert len(out) == 2
    assert out[0].is_coder is True
    assert out[1].is_coder is False


def test_auto_model_llama_cpp_models_scans_dir(tmp_path):
    from sage.core.auto_model import _llama_cpp_models
    (tmp_path / "qwen2.5-coder-3b.gguf").write_bytes(b"x" * (200 * 1024 * 1024))
    (tmp_path / "tiny.gguf").write_bytes(b"x" * 100)  # too small, skipped
    out = _llama_cpp_models(tmp_path)
    names = [c.base_name for c in out]
    assert "qwen2.5-coder-3b" in names
    assert "tiny" not in names


# ── speculative: path resolution ─────────────────────────────────────

def test_speculative_resolve_returns_none_when_unset():
    from sage.config import SageConfig
    from sage.core.speculative import resolve_draft_model_path
    assert resolve_draft_model_path(SageConfig()) is None


def test_speculative_resolve_finds_disk_file(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.speculative import resolve_draft_model_path
    models = tmp_path / ".sage" / "models"
    models.mkdir(parents=True)
    (models / "draft1b.gguf").write_bytes(b"x" * 100)
    cfg = SageConfig(speculative_draft_model="llama_cpp:draft1b")
    p = resolve_draft_model_path(cfg)
    assert p is not None and p.name == "draft1b.gguf"


def test_speculative_resolve_returns_none_for_non_llama_provider():
    from sage.config import SageConfig
    from sage.core.speculative import resolve_draft_model_path
    cfg = SageConfig(speculative_draft_model="ollama:foo")
    assert resolve_draft_model_path(cfg) is None


# ── corpus: harvest_from_filesystem ─────────────────────────────────

def test_corpus_harvest_yields_examples_and_skips_excluded(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training.corpus import CorpusManager

    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / ".env").write_text("SECRET=1")          # must skip
    (proj / "main.py").write_text("def m(): pass")  # must include
    (proj / "node_modules").mkdir()
    (proj / "node_modules" / "lib.js").write_text("// don't include")
    cm = CorpusManager()
    examples = list(cm.harvest_from_filesystem(proj, max_files=10))
    paths = {e.source["path"] for e in examples}
    assert "main.py" in paths
    assert ".env" not in paths
    assert all("node_modules" not in p for p in paths)


# ── rag: end-to-end with stub embedder ──────────────────────────────

class _StubEmbedder:
    """Deterministic embedder for tests — no network."""
    dim = 4
    def embed(self, texts):
        # Tiny embedding: 4 floats based on length and first char
        out = []
        for t in texts:
            first = ord(t[0]) if t else 0
            out.append([float(len(t)), float(first), 1.0, 0.0])
        return out


def test_rag_index_reindex_and_query(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.rag import RAGIndex
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "a.py").write_text("def hello():\n    return 1\n")
    (proj / "b.py").write_text("def goodbye():\n    return 2\n")

    index = RAGIndex(proj, embedder=_StubEmbedder())
    stats = index.reindex()
    assert stats["chunks_added"] >= 2

    chunks = index.query("hello", top_k=3)
    assert chunks
    assert all(c.text for c in chunks)


def test_rag_index_skips_unchanged_files(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.rag import RAGIndex
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "x.py").write_text("def x(): pass")
    index = RAGIndex(proj, embedder=_StubEmbedder())
    s1 = index.reindex()
    s2 = index.reindex()  # mtimes unchanged → no new chunks
    assert s2["chunks_added"] == 0
    assert s1["files_seen"] == s2["files_seen"]


# ── internet: search_and_summarize / docs_for ───────────────────────

def test_internet_search_and_summarize_handles_no_results(monkeypatch):
    from sage.core.internet import Internet
    inet = Internet()
    monkeypatch.setattr(inet, "search", lambda q, limit=5: [])
    assert inet.search_and_summarize("anything") == ""


def test_internet_search_and_summarize_concatenates_pages(monkeypatch):
    from sage.core.internet import Internet, FetchedPage
    from sage.core.web_search import SearchResult
    inet = Internet()
    monkeypatch.setattr(inet, "search", lambda q, limit=5: [
        SearchResult(title="T1", url="https://t1", snippet="s1"),
        SearchResult(title="T2", url="https://t2", snippet="s2"),
    ])
    monkeypatch.setattr(
        inet, "fetch",
        lambda url: FetchedPage(url=url, title="T", text=f"content for {url}"),
    )
    out = inet.search_and_summarize("query", k=2)
    assert "https://t1" in out
    assert "https://t2" in out
    assert "content for" in out


def test_internet_docs_for_prefers_docs_subdomain(monkeypatch):
    from sage.core.internet import Internet, FetchedPage
    from sage.core.web_search import SearchResult
    inet = Internet()
    monkeypatch.setattr(inet, "search", lambda q, limit=5: [
        SearchResult(title="SO", url="https://stackoverflow.com/q/1", snippet=""),
        SearchResult(title="Docs", url="https://docs.example.com/api", snippet=""),
    ])
    fetched = []
    def _fetch(url):
        fetched.append(url)
        return FetchedPage(url=url, title="T", text="...")
    monkeypatch.setattr(inet, "fetch", _fetch)
    page = inet.docs_for("example")
    assert page is not None
    assert fetched[0] == "https://docs.example.com/api"


# ── verifier: edge cases ─────────────────────────────────────────────

def test_verifier_temperature_spread_default():
    from sage.core.verifier import _spread_temperatures
    assert _spread_temperatures(1) == [0.2]
    assert _spread_temperatures(2) == [0.2, 0.7]
    assert _spread_temperatures(3) == [0.0, 0.4, 0.8]
    assert len(_spread_temperatures(5)) == 5


def test_verifier_critic_score_parsing():
    from sage.core.verifier import _parse_critic_scores
    reply = "0: 9 best\n1: 7.5 ok\n2: 3 bad\nignored garbage"
    scores = _parse_critic_scores(reply, n=3)
    assert scores == [9.0, 7.5, 3.0]


def test_verifier_critic_handles_malformed_lines():
    from sage.core.verifier import _parse_critic_scores
    reply = "garbage\n0:notanumber\n1: 5\n"
    scores = _parse_critic_scores(reply, n=2)
    assert scores[1] == 5.0


# ── prefix_cache: stats and eviction ordering ────────────────────────

def test_prefix_cache_stats_reports_root_and_counts(tmp_path):
    from sage.core.prefix_cache import PrefixCache, PrefixCacheKey
    cache = PrefixCache(root=tmp_path)
    cache.put(PrefixCacheKey("m", "a"), b"x" * 100)
    stats = cache.stats()
    assert stats["entries"] == 1
    assert stats["root"] == str(tmp_path)
    assert stats["total_bytes"] == 100


def test_prefix_cache_get_returns_none_when_file_missing(tmp_path):
    from sage.core.prefix_cache import PrefixCache, PrefixCacheKey
    cache = PrefixCache(root=tmp_path)
    key = PrefixCacheKey("m", "a")
    cache.put(key, b"x")
    # Externally delete the file but leave the index entry
    (tmp_path / key.filename()).unlink()
    assert cache.get(key) is None


# ── route: edge cases ───────────────────────────────────────────────

def test_route_returns_empty_when_no_models_at_all():
    from sage.core.route import route_request
    decision = route_request("anything", available_models=[])
    assert decision.model == ""


def test_route_difficulty_classification_word_count_threshold():
    from sage.core.route import _classify_difficulty, Difficulty
    # 200+ words → NOVEL regardless of pattern
    long = " ".join(["word"] * 250)
    assert _classify_difficulty(long, has_long_context=False, has_attached_files=False) == Difficulty.NOVEL


# ── few_shot: trim behaviour ────────────────────────────────────────

def test_few_shot_trims_to_max_examples(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core import few_shot
    monkeypatch.setattr(few_shot, "_MAX_EXAMPLES", 4)
    store = few_shot.FewShotStore(tmp_path / "proj")
    for i in range(10):
        store.record_accept(f"p{i}", f"r{i}")
    # Reload
    store2 = few_shot.FewShotStore(tmp_path / "proj")
    assert len(store2._examples) <= 4
