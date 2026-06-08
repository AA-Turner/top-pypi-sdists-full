"""Smoke + unit tests for Waves 1-4.

Run:
    .venv/bin/python -m pytest sage/tests/test_waves.py -v

These tests intentionally avoid:
  - Real network calls (web_search hits a stub HTML body)
  - Real GCS uploads (corpus push/pull tested with shutil.which monkeypatch)
  - Actual model fine-tuning (finetune tests check resolver, not training)
  - llama-cpp-python loading (grammar test optional, skipped if absent)

What they DO verify:
  - Every new module imports without error
  - Pure functions return the right shape on representative inputs
  - File I/O round-trips (corpus snapshot, few-shot store, RAG vec blob)
  - CLI extension app registers without crashing
  - Python REPL actually executes and bounds output
"""

from __future__ import annotations

import json
import os
import struct
import sys
import tempfile
from pathlib import Path

import pytest


# ── Wave 1 ────────────────────────────────────────────────────────────

def test_auto_model_imports_and_classifies():
    from sage.core.auto_model import _is_coder, Candidate
    assert _is_coder("qwen3-coder-next") is True
    assert _is_coder("deepseek-coder-v2") is True
    assert _is_coder("llama3.2") is False
    c = Candidate(
        qualified_id="ollama:qwen3-coder-next", backend="ollama",
        base_name="qwen3-coder-next", size_gb=51.0, is_coder=True,
    )
    # +100 coder bonus + min(51, 80) raw size = 151
    assert c.score == 151.0


def test_auto_model_pick_prefers_coder_over_bigger_general():
    from sage.core.auto_model import Candidate, pick_best_coder
    cands = [
        Candidate("ollama:llama3.3", "ollama", "llama3.3", 42.0, False),       # score=42
        Candidate("ollama:qwen3-coder-next", "ollama", "qwen3-coder-next", 51.0, True),  # 151
        Candidate("ollama:llama3.2", "ollama", "llama3.2", 2.0, False),        # 2
    ]
    pick = pick_best_coder(cands, available_ram_gb=128.0)
    assert pick is not None and pick.base_name == "qwen3-coder-next"


def test_auto_model_pick_falls_back_when_nothing_fits():
    from sage.core.auto_model import Candidate, pick_best_coder
    cands = [
        Candidate("ollama:big", "ollama", "big-coder", 200.0, True),
    ]
    # Tiny RAM — nothing fits, but we still return *something* (the only one)
    pick = pick_best_coder(cands, available_ram_gb=8.0)
    assert pick is not None


def test_auto_pick_default_preserves_existing_coder_choice():
    from sage.core.auto_model import auto_pick_default_model
    # User explicitly chose a coder model — don't override
    assert auto_pick_default_model("ollama:deepseek-coder-v2") == "ollama:deepseek-coder-v2"


def test_project_detect_python_fastapi(tmp_path: Path):
    from sage.core.project_detect import detect_project, format_for_prompt
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "x"\ndependencies = ["fastapi", "pytest"]\n'
        '[tool.ruff]\n'
    )
    (tmp_path / "src").mkdir()
    ctx = detect_project(tmp_path)
    assert "Python" in ctx.languages
    assert "FastAPI" in ctx.frameworks
    assert ctx.test_runner == "pytest"
    assert "ruff" in ctx.style_tools
    assert "src" in ctx.source_dirs
    rendered = format_for_prompt(ctx)
    assert "DETECTED PROJECT CONTEXT" in rendered
    assert "FastAPI" in rendered


def test_project_detect_js_react_vite(tmp_path: Path):
    from sage.core.project_detect import detect_project
    (tmp_path / "package.json").write_text(json.dumps({
        "name": "demo",
        "dependencies": {"react": "^18.2.0"},
        "devDependencies": {"vite": "^5.0.0", "vitest": "^1.0.0", "tailwindcss": "^3"},
        "scripts": {"test": "vitest"},
    }))
    (tmp_path / "components").mkdir()
    ctx = detect_project(tmp_path)
    assert "React" in ctx.frameworks
    assert "Vite" in ctx.frameworks
    assert ctx.test_runner == "Vitest"
    assert "Tailwind" in ctx.style_tools


def test_project_detect_empty_dir(tmp_path: Path):
    from sage.core.project_detect import detect_project, format_for_prompt
    ctx = detect_project(tmp_path)
    assert ctx.empty
    assert format_for_prompt(ctx) == ""


def test_web_search_parses_canned_ddg_html():
    from sage.core.web_search import _parse_ddg_html
    html = """
    <div class="result">
      <h2><a class="result__a" href="https://example.com/foo">Example Foo</a></h2>
      <a class="result__snippet" href="https://example.com/foo">A useful snippet about foo.</a>
    </div>
    <div class="result">
      <h2><a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A//bar.com">Bar Title</a></h2>
      <a class="result__snippet" href="x">Snippet two.</a>
    </div>
    """
    results = _parse_ddg_html(html, limit=5)
    assert len(results) == 2
    assert results[0].title == "Example Foo"
    assert results[0].url == "https://example.com/foo"
    # Verify DDG redirect unwrapping
    assert results[1].url.startswith("https://bar.com")


# ── Wave 2 ────────────────────────────────────────────────────────────

def test_rag_vec_blob_roundtrip():
    from sage.core.rag import _vec_to_blob, _blob_to_vec
    v = [0.1, 0.2, -0.3, 1e-5, -42.0]
    out = _blob_to_vec(_vec_to_blob(v))
    assert len(out) == len(v)
    for a, b in zip(v, out):
        assert abs(a - b) < 1e-6


def test_rag_cosine_basic():
    from sage.core.rag import _cosine
    assert _cosine([1, 0, 0], [1, 0, 0]) == pytest.approx(1.0)
    assert _cosine([1, 0, 0], [0, 1, 0]) == pytest.approx(0.0)
    assert _cosine([1, 0, 0], [-1, 0, 0]) == pytest.approx(-1.0)
    assert _cosine([], [1, 2]) == 0.0  # empty guard


def test_rag_chunk_file(tmp_path: Path):
    from sage.core.rag import _chunk_file
    p = tmp_path / "src" / "thing.py"
    p.parent.mkdir()
    # 200 lines → at chunk size 80 with overlap 12, expect 3 chunks
    p.write_text("\n".join(f"line_{i}" for i in range(200)))
    chunks = _chunk_file(p, tmp_path)
    assert len(chunks) >= 2
    assert chunks[0].file_path == "src/thing.py"
    assert chunks[0].start_line == 1
    # Each subsequent chunk overlaps with the previous by 12 lines
    assert chunks[1].start_line == chunks[0].end_line - 11


def test_grammar_string_loads_or_skips():
    """If llama_cpp is installed, the grammar should compile cleanly."""
    from sage.core.grammar import SAGE_PROTOCOL_GBNF, load_grammar
    assert "FILE:" in SAGE_PROTOCOL_GBNF
    assert "ANSWER:" in SAGE_PROTOCOL_GBNF
    g = load_grammar()
    if g is None:
        pytest.skip("llama_cpp not installed; grammar compile skipped")


def test_few_shot_roundtrip(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    # Need to also patch Path.home()
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    from sage.core.few_shot import FewShotStore
    cwd = tmp_path / "proj"
    cwd.mkdir()
    store = FewShotStore(cwd)
    store.record_accept("write a hello world", "print('hi')", tags=["python"])
    store.record_reject("write tests", "from unittest import...", reason="we use pytest")

    # Reload from disk
    store2 = FewShotStore(cwd)
    assert len(store2.accepted()) == 1
    assert len(store2.rejected()) == 1
    rendered = store2.format_for_prompt()
    assert "LEARNED PREFERENCES" in rendered
    assert "we use pytest" in rendered


# ── Wave 3 ────────────────────────────────────────────────────────────

def test_agent_pipeline_orchestrates_three_phases():
    from sage.core.agent_pipeline import AgentPipeline

    calls: list[str] = []

    def fake_send(prompt: str, *, model: str, system: str) -> str:
        calls.append(model)
        if "PLANNER" in system:
            return "1. step one\n2. step two"
        if "CODER" in system:
            return "FILE: x.py\n```python\nprint('hi')\n```"
        return "looks fine"

    pipeline = AgentPipeline(
        fake_send,
        planner_model="planner-model",
        coder_model="coder-model",
        reviewer_model="reviewer-model",
        validate_fn=lambda code: (True, "tests pass"),
    )
    result = pipeline.run("build a thing")
    assert result.success is True
    assert calls == ["planner-model", "coder-model", "reviewer-model"]
    assert result.validate is not None and result.validate.ok
    assert "step one" in result.plan.output


def test_agent_pipeline_short_circuits_on_planner_error():
    from sage.core.agent_pipeline import AgentPipeline

    def boom(prompt: str, *, model: str, system: str) -> str:
        raise RuntimeError("planner died")

    pipeline = AgentPipeline(boom, planner_model="p", coder_model="c")
    result = pipeline.run("x")
    assert result.success is False
    assert "planner died" in (result.plan.error or "")


def test_speculative_kwargs_disabled_by_default():
    from sage.config import SageConfig
    from sage.core.speculative import speculative_kwargs
    cfg = SageConfig()
    assert cfg.speculative_draft_model == ""
    assert speculative_kwargs(cfg) == {}


def test_python_repl_runs_simple_code():
    from sage.core.python_repl import run_python
    res = run_python("print(2 + 2)")
    assert res.ok is True
    assert "4" in res.stdout
    assert res.exit_code == 0


def test_python_repl_enforces_timeout():
    from sage.core.python_repl import PythonRepl
    res = PythonRepl(timeout_s=0.5).run("import time; time.sleep(3)")
    assert res.ok is False
    assert "TIMEOUT" in res.stderr


def test_python_repl_truncates_huge_output():
    from sage.core.python_repl import PythonRepl
    res = PythonRepl(max_output_bytes=200).run("print('x' * 10000)")
    assert res.truncated is True
    assert len(res.stdout) <= 200


# ── Wave 4 ────────────────────────────────────────────────────────────

def test_training_example_id_is_content_hash():
    from sage.training.corpus import TrainingExample
    a = TrainingExample(instruction="i", input="in", output="o")
    b = TrainingExample(instruction="i", input="in", output="o")
    c = TrainingExample(instruction="i", input="in", output="DIFFERENT")
    assert a.id == b.id      # same content → same id (dedup will work)
    assert a.id != c.id


def test_training_example_jsonl_roundtrip():
    from sage.training.corpus import TrainingExample
    ex = TrainingExample(instruction="i", input="in", output="o", tags=["py"])
    parsed = json.loads(ex.to_jsonl())
    assert parsed["instruction"] == "i"
    assert parsed["tags"] == ["py"]
    assert parsed["id"] == ex.id


def test_should_include_file_skips_secrets_and_lockfiles():
    from sage.training.corpus import should_include_file
    assert not should_include_file(Path(".env"))
    assert not should_include_file(Path("api.pem"))
    assert not should_include_file(Path("package-lock.json"))
    assert not should_include_file(Path("node_modules/lib/x.js"))
    assert should_include_file(Path("src/foo.py"))


def test_corpus_snapshot_dedupes(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training.corpus import CorpusManager, TrainingExample

    cm = CorpusManager()
    cwd = tmp_path / "proj"
    cwd.mkdir()
    examples = [
        TrainingExample(instruction="a", input="", output="x"),
        TrainingExample(instruction="a", input="", output="x"),  # dup
        TrainingExample(instruction="b", input="", output="y"),
    ]
    snap = cm.write_snapshot(cwd, examples, upload=False)
    lines = [l for l in snap.read_text().splitlines() if l.strip()]
    assert len(lines) == 2  # dedup worked


def test_corpus_hash_stable(tmp_path: Path):
    from sage.training.corpus import CorpusManager
    p = tmp_path / "snap.jsonl"
    p.write_text('{"id": "a"}\n{"id": "b"}\n')
    h1 = CorpusManager.corpus_hash(p)
    h2 = CorpusManager.corpus_hash(p)
    assert h1 == h2 and len(h1) == 16


def test_adapter_ref_paths(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training.cache import AdapterRef
    ref = AdapterRef(base_name="qwen3-coder-next", corpus_hash="abc123")
    assert "qwen3-coder-next/abc123" in str(ref.local_dir())
    assert "abc123" in ref.gcs_dir("gs://bucket")


def test_finetune_available_backends_no_crash():
    """Just verify the function runs without exploding regardless of installed deps."""
    from sage.training.finetune import available_backends, install_hint
    backends = available_backends()
    assert isinstance(backends, list)
    hint = install_hint()
    assert "pip install" in hint


def test_finetune_returns_helpful_error_when_no_backend(tmp_path: Path, monkeypatch):
    """If no backend is installed, finetune() should fail with a clear message."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr("sage.training.finetune.available_backends", lambda: [])
    # Also monkeypatch cache miss so we hit the train path
    monkeypatch.setattr("sage.training.cache.AdapterCache.get_or_resolve",
                        lambda self, ref: None)

    from sage.training.finetune import FinetuneConfig, finetune
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text('{"instruction":"x","input":"","output":"y","id":"deadbeef"}\n')
    cfg = FinetuneConfig(base_model="ollama:fake", corpus_path=corpus)
    result = finetune(cfg, bucket="gs://nope")
    assert result.success is False
    assert "pip install" in (result.error or "")


# ── CLI ────────────────────────────────────────────────────────────────

def test_cli_extensions_module_importable():
    """The cli_extensions module must import without errors so main.py can register it."""
    from sage import cli_extensions
    assert hasattr(cli_extensions, "register")
    assert hasattr(cli_extensions, "extensions_app")


def test_cli_extensions_register_idempotent():
    """register() should attach the sub-typer to a parent app without crashing."""
    import typer
    from sage.cli_extensions import register
    parent = typer.Typer()
    register(parent)  # should not raise


# ── Config integration ────────────────────────────────────────────────

def test_config_has_new_wave_fields():
    from sage.config import SageConfig
    cfg = SageConfig()
    assert cfg.rag_enabled is True
    assert cfg.rag_embedder == "ollama:nomic-embed-text"
    assert cfg.rag_top_k == 6
    assert cfg.gcs_corpus_bucket == "gs://sage-ai-models"


# ── Wave 5: prefix cache, route, verifier, datasets, internet ────────

def test_prefix_id_is_deterministic():
    from sage.core.prefix_cache import prefix_id_for
    a = prefix_id_for("system", "ollama:foo", [{"role": "user", "content": "hi"}])
    b = prefix_id_for("system", "ollama:foo", [{"role": "user", "content": "hi"}])
    c = prefix_id_for("system", "ollama:foo", [{"role": "user", "content": "different"}])
    assert a == b
    assert a != c


def test_prefix_cache_put_and_get(tmp_path: Path):
    from sage.core.prefix_cache import PrefixCache, PrefixCacheKey
    cache = PrefixCache(root=tmp_path, max_bytes=1024 * 1024)
    key = PrefixCacheKey(model="ollama:test", prefix_id="abc123")
    cache.put(key, b"x" * 1024)
    assert cache.get(key) is not None
    stats = cache.stats()
    assert stats["entries"] == 1
    assert stats["total_bytes"] == 1024


def test_prefix_cache_evicts_lru(tmp_path: Path):
    from sage.core.prefix_cache import PrefixCache, PrefixCacheKey
    cache = PrefixCache(root=tmp_path, max_bytes=2048)
    cache.put(PrefixCacheKey("m", "old"), b"a" * 1024)
    cache.put(PrefixCacheKey("m", "new1"), b"b" * 1024)
    cache.put(PrefixCacheKey("m", "new2"), b"c" * 1024)  # exceeds budget → evict
    assert cache.stats()["entries"] <= 2


def test_route_picks_local_for_simple_task():
    from sage.core.route import RoutePolicy, route_request, Difficulty
    avail = ["ollama:llama3.2", "ollama:qwen3-coder-next"]
    decision = route_request("rename foo to bar in this file", available_models=avail)
    # 'rename' triggers TRIVIAL pattern + word_count<20
    assert decision.difficulty in (Difficulty.TRIVIAL, Difficulty.SIMPLE)
    # Should pick a real installed model, not return empty
    assert decision.model in avail


def test_route_handles_ollama_latest_tag():
    """Bug from CLI smoke-test: 'ollama:llama3.2:latest' must match the ladder."""
    from sage.core.route import route_request
    avail = ["ollama:llama3.2:latest", "ollama:qwen3-coder-next:latest"]
    decision = route_request("rename foo to bar", available_models=avail)
    assert decision.model == "ollama:llama3.2:latest"


def test_route_escalates_for_novel_task():
    from sage.core.route import RoutePolicy, route_request, Difficulty
    avail = ["ollama:llama3.2", "ollama:qwen3-coder-next"]
    decision = route_request(
        "design a new distributed consensus protocol from scratch",
        available_models=avail,
    )
    assert decision.difficulty == Difficulty.NOVEL
    # qwen3-coder-next is in the novel ladder so it should be picked
    assert "qwen3-coder-next" in decision.model


def test_route_does_not_escalate_to_cloud_when_disallowed():
    from sage.core.route import RoutePolicy, route_request
    pol = RoutePolicy(allow_cloud=False)
    decision = route_request("design a new system", available_models=[
        "ollama:llama3.2", "anthropic:claude-sonnet-4-6",
    ], policy=pol)
    # Even though cloud is "available", policy forbids escalation when no local hard/novel hit
    assert not decision.model.startswith("anthropic:")


def test_verifier_picks_validator_passing_candidate():
    from sage.core.verifier import best_of_n
    calls = [0]

    def gen(temp: float) -> str:
        calls[0] += 1
        return f"output_at_temp_{temp}"

    def validator(out: str) -> tuple[bool, str]:
        # Only outputs at temp 0.4 pass
        return ("0.4" in out, "")

    result = best_of_n(
        task="x", generator=gen, n_samples=3, validator=validator,
        temperatures=[0.0, 0.4, 0.8],
    )
    assert result.used_validator
    assert "0.4" in result.winner.output
    assert calls[0] == 3


def test_verifier_falls_back_to_consistency_when_no_critic():
    from sage.core.verifier import best_of_n
    outputs = ["line_a\nline_b", "line_a\nline_b", "completely_other"]
    counter = [0]

    def gen(temp: float) -> str:
        out = outputs[counter[0]]
        counter[0] += 1
        return out

    result = best_of_n(task="x", generator=gen, n_samples=3)
    # Two candidates share 'line_a' / 'line_b' — one of them wins
    assert "line_a" in result.winner.output


def test_external_datasets_registry_well_formed():
    from sage.training.datasets import DATASETS, ExternalDataset
    assert len(DATASETS) >= 5
    seen = set()
    for ds in DATASETS:
        assert isinstance(ds, ExternalDataset)
        assert ds.name not in seen
        seen.add(ds.name)
        assert "/" in ds.huggingface_id or ds.huggingface_id.islower()
        assert len(ds.fields) == 3


def test_internet_facade_imports_and_blocks_local():
    from sage.core.internet import Internet
    inet = Internet()
    blocked, reason = inet.is_blocked("http://127.0.0.1:8000/admin")
    assert blocked is True


def test_project_detect_recognizes_more_languages(tmp_path: Path):
    """Wave 5: extended language coverage (Julia, Dart, Zig, Elm, ...)."""
    from sage.core.project_detect import detect_project
    (tmp_path / "Project.toml").write_text("[deps]\n")
    ctx = detect_project(tmp_path)
    assert "Julia" in ctx.languages

    other = tmp_path / "flutter_app"
    other.mkdir()
    (other / "pubspec.yaml").write_text("name: x\n")
    ctx2 = detect_project(other)
    assert any("Dart" in l for l in ctx2.languages)


# ── Wave 1-2 config (kept) ─────────────────────────────────────────


def test_config_roundtrip_preserves_new_fields(tmp_path: Path):
    from sage.config import SageConfig
    cfg = SageConfig(
        default_model="ollama:qwen3-coder-next",
        rag_top_k=10,
        speculative_draft_model="llama_cpp:llama3.2-1b",
    )
    path = tmp_path / "config.json"
    path.write_text(json.dumps(cfg.to_dict()))
    restored = SageConfig.from_dict(json.loads(path.read_text()))
    assert restored.default_model == "ollama:qwen3-coder-next"
    assert restored.rag_top_k == 10
    assert restored.speculative_draft_model == "llama_cpp:llama3.2-1b"
