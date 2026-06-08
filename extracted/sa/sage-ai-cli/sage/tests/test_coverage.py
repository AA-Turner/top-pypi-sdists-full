"""Deep coverage tests for every authored module.

Goal: push every module I wrote (Waves 1-5 + Tiers A-C) above ~85%
line+branch coverage by mocking the external boundaries (httpx,
subprocess/gsutil, huggingface datasets, tree-sitter, watchdog,
llama_cpp's LlamaGrammar, sqlite_vec, sentence-transformers).

Run:
    .venv/bin/python -m pytest sage/tests/test_coverage.py -v --no-cov
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import types
from pathlib import Path

import pytest


# ════════════════════════════════════════════════════════════════════════
# training/cache.py — full mock coverage
# ════════════════════════════════════════════════════════════════════════

def _make_run(returncode: int = 0, stdout: str = "", stderr: str = ""):
    def _run(cmd, capture_output=True, text=True, timeout=15, **kw):
        return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)
    return _run


def test_adapter_cache_has_local_and_pull_and_push(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import cache as c
    cache = c.AdapterCache(bucket="gs://test")
    ref = c.AdapterRef("base", "hash1")

    # has_local: false initially, then true after we drop a file
    assert cache.has_local(ref) is False
    ref.local_dir().mkdir(parents=True, exist_ok=True)
    (ref.local_dir() / "adapter.safetensors").write_bytes(b"x")
    assert cache.has_local(ref) is True

    # has_remote: mock subprocess returncode 0 → True, 1 → False
    monkeypatch.setattr(c.subprocess, "run", _make_run(0))
    assert cache.has_remote(ref) is True
    monkeypatch.setattr(c.subprocess, "run", _make_run(1))
    assert cache.has_remote(ref) is False

    # has_remote: gsutil missing
    def _missing(*a, **kw):
        raise FileNotFoundError("gsutil")
    monkeypatch.setattr(c.subprocess, "run", _missing)
    assert cache.has_remote(ref) is False


def test_adapter_cache_pull_handles_subprocess_outcomes(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import cache as c
    cache = c.AdapterCache(bucket="gs://test")
    ref = c.AdapterRef("base", "hash2")

    # pull when has_remote = False → False
    monkeypatch.setattr(c.AdapterCache, "has_remote", lambda self, r: False)
    assert cache.pull(ref) is False

    # pull when has_remote = True and subprocess succeeds → True
    monkeypatch.setattr(c.AdapterCache, "has_remote", lambda self, r: True)
    monkeypatch.setattr(c.subprocess, "run", _make_run(0))
    assert cache.pull(ref) is True

    # pull subprocess timeout
    def _timeout(*a, **kw):
        raise subprocess.TimeoutExpired("gsutil", 60)
    monkeypatch.setattr(c.subprocess, "run", _timeout)
    assert cache.pull(ref) is False


def test_adapter_cache_push_writes_meta_and_uploads(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import cache as c
    cache = c.AdapterCache(bucket="gs://test")
    ref = c.AdapterRef("base", "hash3")

    # No adapter file → push returns False
    meta = c.AdapterMeta(base_name="base", corpus_hash="hash3", steps=10,
                         created_ts=time.time(), train_seconds=1.0, backend="mlx")
    assert cache.push(ref, meta) is False

    # Drop adapter file, mock successful subprocess
    ref.local_dir().mkdir(parents=True, exist_ok=True)
    (ref.local_dir() / "adapter.safetensors").write_bytes(b"x")
    monkeypatch.setattr(c.subprocess, "run", _make_run(0))
    assert cache.push(ref, meta) is True
    # meta.json got written
    assert (ref.local_dir() / "meta.json").exists()


def test_adapter_cache_get_or_resolve_paths(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import cache as c
    cache = c.AdapterCache(bucket="gs://test")
    ref = c.AdapterRef("base", "hash4")

    # No local, no remote → None
    monkeypatch.setattr(c.AdapterCache, "has_remote", lambda self, r: False)
    assert cache.get_or_resolve(ref) is None

    # Local hit
    ref.local_dir().mkdir(parents=True, exist_ok=True)
    (ref.local_dir() / "adapter.safetensors").write_bytes(b"x")
    assert cache.get_or_resolve(ref) == ref.local_dir()


# ════════════════════════════════════════════════════════════════════════
# training/finetune.py — backend selection + cache hit + error paths
# ════════════════════════════════════════════════════════════════════════

def test_finetune_uses_cache_when_hit(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import finetune as f
    from sage.training.cache import AdapterCache, AdapterRef

    corpus = tmp_path / "c.jsonl"
    corpus.write_text('{"id":"x"}\n')
    cfg = f.FinetuneConfig(base_model="ollama:fake", corpus_path=corpus)

    # Force cache hit — get_or_resolve returns a path
    monkeypatch.setattr(AdapterCache, "get_or_resolve",
                        lambda self, ref: tmp_path / "adapter")
    result = f.finetune(cfg)
    assert result.success is True
    assert result.backend == "cache"
    assert result.meta["hit"] == "cache"


def test_finetune_cache_only_fails_on_miss(tmp_path):
    from sage.training import finetune as f
    corpus = tmp_path / "c.jsonl"
    corpus.write_text('{"id":"x"}\n')
    cfg = f.FinetuneConfig(base_model="ollama:fake", corpus_path=corpus)
    result = f.finetune(cfg, cache_only=True)
    assert result.success is False
    assert "not in cache" in (result.error or "")


def test_finetune_install_hint_apple_silicon(monkeypatch):
    from sage.training import finetune as f
    monkeypatch.setattr(f, "_is_apple_silicon", lambda: True)
    hint = f.install_hint()
    assert "mlx" in hint.lower()


def test_finetune_install_hint_other(monkeypatch):
    from sage.training import finetune as f
    monkeypatch.setattr(f, "_is_apple_silicon", lambda: False)
    hint = f.install_hint()
    assert "unsloth" in hint.lower() or "transformers" in hint.lower()


def test_finetune_pick_backend_returns_first_available(monkeypatch):
    from sage.training import finetune as f
    monkeypatch.setattr(f, "available_backends", lambda: ["mlx"])
    assert f._pick_backend("auto") == "mlx"
    monkeypatch.setattr(f, "available_backends", lambda: [])
    assert f._pick_backend("auto") is None
    # explicit request honored only when available
    monkeypatch.setattr(f, "available_backends", lambda: ["peft"])
    assert f._pick_backend("peft") == "peft"
    assert f._pick_backend("mlx") is None


def test_finetune_train_mlx_subprocess_failure(tmp_path, monkeypatch):
    from sage.training import finetune as f
    corpus = tmp_path / "c.jsonl"
    corpus.write_text('{}\n')
    cfg = f.FinetuneConfig(base_model="ollama:fake", corpus_path=corpus)

    class _Proc:
        returncode = 1
        stdout = ""
        stderr = "model load failed"
    monkeypatch.setattr(f.subprocess, "run", lambda *a, **kw: _Proc())
    result = f._train_mlx(cfg, tmp_path / "out")
    assert result.success is False
    assert "exit 1" in (result.error or "")


def test_finetune_train_mlx_subprocess_success(tmp_path, monkeypatch):
    from sage.training import finetune as f
    corpus = tmp_path / "c.jsonl"
    corpus.write_text('{}\n')
    cfg = f.FinetuneConfig(base_model="ollama:fake", corpus_path=corpus)

    class _Proc:
        returncode = 0
        stdout = "training done"
        stderr = ""
    monkeypatch.setattr(f.subprocess, "run", lambda *a, **kw: _Proc())
    result = f._train_mlx(cfg, tmp_path / "out")
    assert result.success is True
    assert result.backend == "mlx"


def test_finetune_train_mlx_timeout(tmp_path, monkeypatch):
    from sage.training import finetune as f
    corpus = tmp_path / "c.jsonl"
    corpus.write_text('{}\n')
    cfg = f.FinetuneConfig(base_model="ollama:fake", corpus_path=corpus)
    def _t(*a, **kw):
        raise subprocess.TimeoutExpired("mlx", 3600)
    monkeypatch.setattr(f.subprocess, "run", _t)
    result = f._train_mlx(cfg, tmp_path / "out")
    assert result.success is False
    assert "timed out" in (result.error or "").lower()


def test_finetune_full_flow_with_train_success(tmp_path, monkeypatch):
    """End-to-end: cache miss → train (mocked) → push to cache."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import finetune as f
    from sage.training.cache import AdapterCache

    corpus = tmp_path / "c.jsonl"
    corpus.write_text('{"id":"abc"}\n')
    cfg = f.FinetuneConfig(base_model="ollama:fake", corpus_path=corpus, backend="mlx")

    monkeypatch.setattr(AdapterCache, "get_or_resolve", lambda self, ref: None)
    monkeypatch.setattr(AdapterCache, "push", lambda self, ref, meta: True)
    monkeypatch.setattr(f, "_pick_backend", lambda r: "mlx")

    def _fake_mlx(cfg_, out_dir):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "adapter.safetensors").write_bytes(b"x")
        return f.FinetuneResult(success=True, backend="mlx", adapter_dir=out_dir,
                                duration_s=0.1, steps_run=10)
    monkeypatch.setattr(f, "_train_mlx", _fake_mlx)
    result = f.finetune(cfg)
    assert result.success is True
    assert result.meta.get("pushed_to_gcs") is True


# ════════════════════════════════════════════════════════════════════════
# training/datasets.py — mock huggingface datasets + gsutil
# ════════════════════════════════════════════════════════════════════════

def test_datasets_is_mirrored_uses_gsutil_ls(monkeypatch):
    from sage.training import datasets as d
    monkeypatch.setattr(d, "_have_gsutil", lambda: True)
    monkeypatch.setattr(d, "_gcs_exists", lambda uri: True)
    mirror = d.DatasetMirror()
    assert mirror.is_mirrored(d.DATASETS[0]) is True

    monkeypatch.setattr(d, "_have_gsutil", lambda: False)
    assert mirror.is_mirrored(d.DATASETS[0]) is False


def test_datasets_fetch_and_normalize_writes_jsonl(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import datasets as d

    # Fake the huggingface datasets module
    fake_rows = [
        {"instruction": "q1", "input": "i1", "output": "a1"},
        {"instruction": "q2", "input": "", "output": "a2"},
        {"instruction": "", "input": "", "output": "skip-empty"},
    ]
    def _load_dataset(repo, split, streaming, trust_remote_code):
        return iter(fake_rows)
    fake_mod = types.SimpleNamespace(load_dataset=_load_dataset)
    monkeypatch.setitem(sys.modules, "datasets", fake_mod)

    mirror = d.DatasetMirror()
    ds = d.DATASETS[0]
    out = mirror.fetch_and_normalize(ds)
    assert out.exists()
    lines = [l for l in out.read_text().splitlines() if l.strip()]
    assert len(lines) == 2  # the empty one is filtered


def test_datasets_fetch_errors_without_hf(monkeypatch):
    from sage.training import datasets as d
    monkeypatch.setattr(d, "_have_datasets_lib", lambda: False)
    with pytest.raises(RuntimeError, match="datasets"):
        d.DatasetMirror().fetch_and_normalize(d.DATASETS[0])


def test_datasets_push_and_pull(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import datasets as d
    mirror = d.DatasetMirror()
    ds = d.DATASETS[0]

    # push when normalized.jsonl missing → False
    assert mirror.push(ds) is False

    # Create normalized.jsonl + mock gsutil success
    local = mirror.local_dir(ds)
    (local / "normalized.jsonl").write_text('{"x":1}\n')
    (local / "SOURCE.txt").write_text("info\n")
    monkeypatch.setattr(d, "_have_gsutil", lambda: True)
    monkeypatch.setattr(d, "_gcs_cp", lambda src, dst: True)
    assert mirror.push(ds) is True

    # pull existing local file just returns it
    assert mirror.pull(ds) is not None


def test_datasets_pull_downloads_when_missing_locally(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import datasets as d
    mirror = d.DatasetMirror()
    ds = d.DATASETS[0]
    monkeypatch.setattr(d, "_have_gsutil", lambda: True)

    def fake_cp(src, dst):
        Path(dst).write_text('{"x":1}\n')
        return True
    monkeypatch.setattr(d, "_gcs_cp", fake_cp)
    out = mirror.pull(ds)
    assert out is not None and out.exists()


def test_datasets_mirror_all_skips_existing_and_filters_languages(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import datasets as d
    mirror = d.DatasetMirror()

    # Pretend everything is already mirrored
    monkeypatch.setattr(d.DatasetMirror, "is_mirrored", lambda self, ds: True)
    report = mirror.mirror_all()
    assert report["mirrored"] == []
    assert len(report["skipped"]) == len(d.DATASETS)

    # Language filter
    monkeypatch.setattr(d.DatasetMirror, "is_mirrored", lambda self, ds: False)
    monkeypatch.setattr(d.DatasetMirror, "fetch_and_normalize", lambda self, ds: Path("/tmp/x"))
    monkeypatch.setattr(d.DatasetMirror, "push", lambda self, ds: True)
    report = mirror.mirror_all(languages=["python"])
    # multilang datasets always pass; language-restricted ones must include python
    expected = [ds.name for ds in d.DATASETS
                if "multilang" in ds.languages or "python" in ds.languages]
    assert sorted(report["mirrored"]) == sorted(expected)


def test_datasets_mirror_all_records_failures(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.training import datasets as d
    mirror = d.DatasetMirror()
    monkeypatch.setattr(d.DatasetMirror, "is_mirrored", lambda self, ds: False)
    def _boom(self, ds):
        raise RuntimeError("api dead")
    monkeypatch.setattr(d.DatasetMirror, "fetch_and_normalize", _boom)
    report = mirror.mirror_all((d.DATASETS[0],))
    assert report["failed"][0][0] == d.DATASETS[0].name


# ════════════════════════════════════════════════════════════════════════
# scripts/requantize.py — full coverage
# ════════════════════════════════════════════════════════════════════════

def test_requantize_find_binary_returns_none_when_absent(monkeypatch):
    from sage.scripts import requantize as r
    monkeypatch.setattr("shutil.which", lambda name: None)
    monkeypatch.setitem(sys.modules, "llama_cpp", None)
    assert r.find_quantize_binary() is None


def test_requantize_find_binary_returns_path_when_on_path(monkeypatch):
    from sage.scripts import requantize as r
    monkeypatch.setattr("shutil.which", lambda name: "/usr/local/bin/" + name)
    assert r.find_quantize_binary() == "/usr/local/bin/llama-quantize"


def test_requantize_calls_subprocess_with_args(tmp_path, monkeypatch):
    from sage.scripts import requantize as r
    captured = {}
    def fake_call(cmd):
        captured["cmd"] = cmd
        return 0
    monkeypatch.setattr(r, "find_quantize_binary", lambda: "/bin/llama-quantize")
    monkeypatch.setattr(r.subprocess, "call", fake_call)
    src = tmp_path / "in.gguf"
    src.write_bytes(b"GGUF")
    rc = r.requantize(src, tmp_path / "out.gguf", quant="Q5_K_M")
    assert rc == 0
    assert "Q5_K_M" in captured["cmd"]
    assert str(src) in captured["cmd"]


def test_requantize_main_with_replace(tmp_path, monkeypatch, capsys):
    from sage.scripts import requantize as r
    src = tmp_path / "model.gguf"
    src.write_bytes(b"GGUF" + b"\x00" * 20)
    monkeypatch.setattr(r, "requantize", lambda i, o, quant: (
        Path(o).write_bytes(b"new"), 0)[1])
    rc = r.main([str(src)])  # default: replace original
    assert rc == 0
    # Original got replaced (file content changed)
    assert src.read_bytes() == b"new"


def test_requantize_main_keep_original(tmp_path, monkeypatch):
    from sage.scripts import requantize as r
    src = tmp_path / "model.gguf"
    src.write_bytes(b"original")
    monkeypatch.setattr(r, "requantize", lambda i, o, quant: (
        Path(o).write_bytes(b"new"), 0)[1])
    rc = r.main([str(src), "--keep-original"])
    assert rc == 0
    assert src.read_bytes() == b"original"


# ════════════════════════════════════════════════════════════════════════
# scripts/build_llama_cpp_optimized.py — Linux + Windows branches
# ════════════════════════════════════════════════════════════════════════

def test_build_picks_linux_blas_when_no_nvidia(monkeypatch):
    from sage.scripts import build_llama_cpp_optimized as b
    monkeypatch.setattr(b.platform, "system", lambda: "Linux")
    monkeypatch.setattr(b.platform, "machine", lambda: "x86_64")
    def _no_nvidia(*a, **kw):
        raise FileNotFoundError("nvidia-smi")
    monkeypatch.setattr(b.subprocess, "run", _no_nvidia)
    flags = b.pick_cmake_flags()
    assert "-DGGML_NATIVE=ON" in flags
    assert "-DGGML_BLAS=ON" in flags


def test_build_picks_windows_native(monkeypatch):
    from sage.scripts import build_llama_cpp_optimized as b
    monkeypatch.setattr(b.platform, "system", lambda: "Windows")
    monkeypatch.setattr(b.platform, "machine", lambda: "AMD64")
    flags = b.pick_cmake_flags()
    assert "-DGGML_NATIVE=ON" in flags


def test_build_picks_intel_mac_native(monkeypatch):
    from sage.scripts import build_llama_cpp_optimized as b
    monkeypatch.setattr(b.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(b.platform, "machine", lambda: "x86_64")
    flags = b.pick_cmake_flags()
    assert flags == ["-DGGML_NATIVE=ON"]


# ════════════════════════════════════════════════════════════════════════
# scripts/vllm_serve.py — all branches
# ════════════════════════════════════════════════════════════════════════

def test_vllm_main_runs_when_all_deps_present(monkeypatch):
    from sage.scripts import vllm_serve as v
    monkeypatch.setattr(v, "have_cuda", lambda: True)
    monkeypatch.setattr(v, "have_vllm", lambda: True)
    monkeypatch.setattr(v.subprocess, "call", lambda cmd: 0)
    rc = v.main(["--model", "x"])
    assert rc == 0


def test_vllm_main_nonzero_when_no_vllm(monkeypatch):
    from sage.scripts import vllm_serve as v
    monkeypatch.setattr(v, "have_cuda", lambda: True)
    monkeypatch.setattr(v, "have_vllm", lambda: False)
    rc = v.main(["--model", "x"])
    assert rc != 0


def test_vllm_have_helpers_dont_crash():
    from sage.scripts import vllm_serve as v
    assert isinstance(v.have_cuda(), bool)
    assert isinstance(v.have_vllm(), bool)


# ════════════════════════════════════════════════════════════════════════
# core/rag.py — sqlite-vec mock + reindex stale-files + format
# ════════════════════════════════════════════════════════════════════════

class _StubEmbedder:
    dim = 4
    def embed(self, texts):
        return [[float(len(t)), float(ord(t[0]) if t else 0), 1.0, 0.0] for t in texts]


def test_rag_format_chunks_for_prompt_truncates(tmp_path):
    from sage.core.rag import Chunk, format_chunks_for_prompt
    chunks = [Chunk(file_path=f"f{i}.py", start_line=1, end_line=10,
                    text="x" * 2000, score=0.9 - 0.01 * i) for i in range(10)]
    out = format_chunks_for_prompt(chunks, max_chars=3000)
    assert "RETRIEVED CONTEXT" in out
    # Should have stopped before all 10 fit
    included = sum(1 for c in chunks if c.file_path in out)
    assert 0 < included < len(chunks)


def test_rag_format_chunks_empty_returns_empty():
    from sage.core.rag import format_chunks_for_prompt
    assert format_chunks_for_prompt([]) == ""


def test_rag_reindex_drops_stale_files(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.rag import RAGIndex
    proj = tmp_path / "p"
    proj.mkdir()
    a = proj / "a.py"
    b = proj / "b.py"
    a.write_text("def a(): pass")
    b.write_text("def b(): pass")
    idx = RAGIndex(proj, embedder=_StubEmbedder())
    idx.reindex()
    # Delete b.py and reindex — stale entry must be removed
    b.unlink()
    idx.reindex()
    cur = idx._conn.execute("SELECT path FROM files").fetchall()
    paths = {r[0] for r in cur}
    assert "a.py" in paths
    assert "b.py" not in paths


def test_rag_query_handles_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.rag import RAGIndex
    idx = RAGIndex(tmp_path, embedder=_StubEmbedder())
    assert idx.query("") == []
    assert idx.query("   ") == []


def test_rag_query_returns_empty_when_embedder_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.rag import RAGIndex

    class _Boom:
        dim = 4
        def embed(self, texts): raise RuntimeError("offline")
    idx = RAGIndex(tmp_path, embedder=_Boom())
    assert idx.query("anything") == []


def test_rag_ollama_embedder_handles_empty_text(monkeypatch):
    from sage.core.rag import OllamaEmbedder
    e = OllamaEmbedder()

    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"embedding": [0.1] * 768}

    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def post(self, *a, **kw): return _Resp()
    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    out = e.embed(["", "real text"])
    assert out[0] == [0.0] * 768


def test_rag_ollama_embedder_errors_without_httpx(monkeypatch):
    from sage.core.rag import OllamaEmbedder
    e = OllamaEmbedder()
    monkeypatch.setitem(sys.modules, "httpx", None)
    # Force ImportError by removing the cached module name
    if "httpx" in sys.modules:
        del sys.modules["httpx"]
    monkeypatch.setattr("builtins.__import__", lambda name, *a, **kw: (
        (_ for _ in ()).throw(ImportError("no httpx")) if name == "httpx"
        else __import__(name, *a, **kw)
    ))
    with pytest.raises(RuntimeError):
        e.embed(["x"])


# ════════════════════════════════════════════════════════════════════════
# core/auto_model.py — RAM probe + edge cases
# ════════════════════════════════════════════════════════════════════════

def test_auto_model_available_ram_with_psutil(monkeypatch):
    from sage.core import auto_model
    fake_psutil = types.SimpleNamespace(
        virtual_memory=lambda: types.SimpleNamespace(available=8 * (1024 ** 3))
    )
    monkeypatch.setitem(sys.modules, "psutil", fake_psutil)
    assert auto_model._available_ram_gb() == 8.0


def test_auto_model_pick_best_when_no_candidates():
    from sage.core.auto_model import pick_best_coder
    assert pick_best_coder([]) is None


def test_auto_model_auto_pick_falls_back_to_default_when_nothing():
    from sage.core.auto_model import auto_pick_default_model
    # With empty installed list, should return the default fallback string
    import sage.core.auto_model as a
    original = a.list_installed_models
    a.list_installed_models = lambda: []
    try:
        out = auto_pick_default_model("")
        assert "llama3.2" in out  # fallback
    finally:
        a.list_installed_models = original


def test_auto_model_llama_cpp_skips_unsupported_arch(tmp_path, monkeypatch):
    """Confirm _llama_cpp_models still includes any non-empty .gguf (arch check happens at load)."""
    from sage.core.auto_model import _llama_cpp_models
    (tmp_path / "okmodel.gguf").write_bytes(b"x" * (200 * 1024 * 1024))
    out = _llama_cpp_models(tmp_path)
    assert any(c.base_name == "okmodel" for c in out)


# ════════════════════════════════════════════════════════════════════════
# core/web_search.py — empty queries + import errors + redirect chains
# ════════════════════════════════════════════════════════════════════════

def test_web_search_empty_query_returns_empty():
    from sage.core.web_search import WebSearchTool
    assert WebSearchTool().search("") == []
    assert WebSearchTool().search("   ") == []


def test_web_search_no_httpx_returns_empty(monkeypatch):
    from sage.core import web_search
    if "httpx" in sys.modules:
        monkeypatch.delitem(sys.modules, "httpx", raising=False)
    monkeypatch.setattr("builtins.__import__", lambda name, *a, **kw: (
        (_ for _ in ()).throw(ImportError("no httpx")) if name == "httpx"
        else __import__(name, *a, **kw)
    ))
    assert web_search.WebSearchTool().search("anything") == []


def test_web_search_500_returns_empty(monkeypatch):
    from sage.core import web_search
    class _Resp:
        status_code = 500
        text = ""
    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def post(self, *a, **kw): return _Resp()
    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    assert web_search.WebSearchTool().search("query") == []


def test_web_search_unwrap_redirect_handles_no_uddg():
    from sage.core.web_search import _unwrap_ddg_redirect
    assert _unwrap_ddg_redirect("https://normal.com/x") == "https://normal.com/x"
    # DDG redirect without uddg param → returned as-is
    assert "duckduckgo.com" in _unwrap_ddg_redirect("https://duckduckgo.com/l/?nohuddg=1")


# ════════════════════════════════════════════════════════════════════════
# core/grammar.py — load_grammar exception branch
# ════════════════════════════════════════════════════════════════════════

def test_grammar_load_returns_none_when_llama_cpp_missing(monkeypatch):
    from sage.core import grammar
    monkeypatch.setitem(sys.modules, "llama_cpp", None)
    if "llama_cpp" in sys.modules:
        del sys.modules["llama_cpp"]
    monkeypatch.setattr("builtins.__import__", lambda name, *a, **kw: (
        (_ for _ in ()).throw(ImportError("no llama_cpp")) if name == "llama_cpp"
        else __import__(name, *a, **kw)
    ))
    assert grammar.load_grammar() is None


def test_grammar_load_returns_none_when_llama_grammar_raises(monkeypatch):
    from sage.core import grammar

    class _Bad:
        @staticmethod
        def from_string(s):
            raise ValueError("invalid GBNF")

    fake = types.SimpleNamespace(LlamaGrammar=_Bad)
    monkeypatch.setitem(sys.modules, "llama_cpp", fake)
    assert grammar.load_grammar() is None


# ════════════════════════════════════════════════════════════════════════
# core/internet.py — fetch error path + docs_for empty
# ════════════════════════════════════════════════════════════════════════

def test_internet_fetch_returns_error_page_on_failure(monkeypatch):
    from sage.core.internet import Internet
    from sage.core.tools import ToolResult, ToolStatus, ToolType
    inet = Internet()
    monkeypatch.setattr(inet._fetcher, "fetch", lambda url, timeout=10:
                        ToolResult(tool_type=ToolType.WEB_FETCH,
                                   status=ToolStatus.ERROR, error="DNS"))
    page = inet.fetch("https://nonexistent.example.com/")
    assert not page.ok
    assert "DNS" in (page.error or "")


def test_internet_docs_for_returns_none_when_no_results(monkeypatch):
    from sage.core.internet import Internet
    inet = Internet()
    monkeypatch.setattr(inet, "search", lambda q, limit=5: [])
    assert inet.docs_for("anything") is None


# ════════════════════════════════════════════════════════════════════════
# core/lora_swap.py — schedule_training paths
# ════════════════════════════════════════════════════════════════════════

def test_lora_swap_schedules_training_in_background(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.lora_swap import LoraSwap

    swap = LoraSwap(cfg=SageConfig())
    captured = {}
    class _Pop:
        def __init__(self, cmd, **kw):
            captured["cmd"] = cmd
            captured["kw"] = kw
    monkeypatch.setattr("subprocess.Popen", _Pop)
    resolved = swap.schedule_training_if_missing(
        tmp_path / "noproj", base_model="ollama:fake")
    assert resolved.source == "missing"
    assert captured["cmd"][0].endswith("python") or "python" in captured["cmd"][0]
    assert "finetune" in captured["cmd"]


def test_lora_swap_returns_existing_when_already_resolved(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.lora_swap import LoraSwap, ResolvedAdapter
    swap = LoraSwap(cfg=SageConfig())
    monkeypatch.setattr(swap, "adapter_for", lambda cwd, base_model:
                        ResolvedAdapter(base_model=base_model, corpus_hash="h",
                                        adapter_dir=tmp_path, source="local"))
    resolved = swap.schedule_training_if_missing(tmp_path, base_model="ollama:x")
    assert resolved.source == "local"


# ════════════════════════════════════════════════════════════════════════
# core/auto_verify.py — Rust/Go/Make/tox + run failures
# ════════════════════════════════════════════════════════════════════════

def test_auto_verify_infers_cargo(tmp_path, monkeypatch):
    from sage.core.auto_verify import infer_test_command
    (tmp_path / "Cargo.toml").write_text("[package]\nname='x'")
    monkeypatch.setattr("shutil.which", lambda c: "/bin/" + c if c == "cargo" else None)
    cmd = infer_test_command(tmp_path)
    assert cmd is not None and cmd[0] == "cargo"


def test_auto_verify_infers_go(tmp_path, monkeypatch):
    from sage.core.auto_verify import infer_test_command
    (tmp_path / "go.mod").write_text("module x")
    monkeypatch.setattr("shutil.which", lambda c: "/bin/" + c if c == "go" else None)
    cmd = infer_test_command(tmp_path)
    assert cmd is not None and cmd[0] == "go"


def test_auto_verify_infers_make(tmp_path, monkeypatch):
    from sage.core.auto_verify import infer_test_command
    (tmp_path / "Makefile").write_text("test:\n\techo ok")
    monkeypatch.setattr("shutil.which", lambda c: "/bin/" + c if c == "make" else None)
    cmd = infer_test_command(tmp_path)
    assert cmd is not None and cmd[0] == "make"


def test_auto_verify_run_handles_filenotfound(tmp_path, monkeypatch):
    from sage.core import auto_verify
    monkeypatch.setattr(auto_verify, "infer_test_command",
                        lambda cwd: ["/no/such/binary/here"])
    def _fnf(*a, **kw):
        raise FileNotFoundError("no such command")
    monkeypatch.setattr(auto_verify.subprocess, "run", _fnf)
    out = auto_verify.ProjectVerifier(tmp_path).run()
    assert out.ok is False
    assert "no such command" in out.stderr_tail


def test_auto_verify_run_handles_timeout(tmp_path, monkeypatch):
    from sage.core import auto_verify
    monkeypatch.setattr(auto_verify, "infer_test_command", lambda cwd: ["pytest"])
    def _t(*a, **kw):
        raise subprocess.TimeoutExpired("pytest", 90)
    monkeypatch.setattr(auto_verify.subprocess, "run", _t)
    out = auto_verify.ProjectVerifier(tmp_path).run()
    assert out.ok is False
    assert "TIMEOUT" in out.stderr_tail


def test_auto_verify_loop_returns_immediately_if_first_passes(tmp_path, monkeypatch):
    from sage.core.auto_verify import ProjectVerifier, VerifyOutcome
    v = ProjectVerifier(tmp_path)
    monkeypatch.setattr(v, "run", lambda: VerifyOutcome(
        ok=True, command="x", stdout_tail="ok", stderr_tail="", duration_s=0.0))
    final, history = v.loop(regenerate_fn=lambda m: None, max_iterations=5)
    assert final.ok is True
    assert len(history) == 1


# ════════════════════════════════════════════════════════════════════════
# core/federated_few_shot.py — push success + corrupt JSON
# ════════════════════════════════════════════════════════════════════════

def test_federated_push_success_and_local_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.federated_few_shot import FederatedFewShot
    fed = FederatedFewShot(tmp_path / "p", cfg=SageConfig())
    monkeypatch.setattr("sage.core.federated_few_shot._have_gsutil", lambda: True)

    # No local file → push False
    assert fed.push() is False

    # Local exists → push True
    fed.local.record_accept("p1", "r1")
    monkeypatch.setattr("sage.core.federated_few_shot.subprocess.run",
                        _make_run(0))
    assert fed.push() is True


def test_federated_pull_handles_corrupt_remote_json(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.config import SageConfig
    from sage.core.federated_few_shot import FederatedFewShot
    fed = FederatedFewShot(tmp_path / "p", cfg=SageConfig())
    monkeypatch.setattr("sage.core.federated_few_shot._have_gsutil", lambda: True)

    def fake_run(cmd, **kw):
        # cmd = ["gsutil", "-q", "cp", src, dst]
        Path(cmd[4]).write_text("not json {{{")
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")
    monkeypatch.setattr("sage.core.federated_few_shot.subprocess.run", fake_run)
    assert fed.pull_and_merge() == 0


# ════════════════════════════════════════════════════════════════════════
# core/search_provider.py — DDG fallback + SearXNG mocked
# ════════════════════════════════════════════════════════════════════════

def test_searxng_backend_parses_results(monkeypatch):
    from sage.core import search_provider as sp
    class _Resp:
        status_code = 200
        def json(self): return {"results": [
            {"title": "T1", "url": "https://t1", "content": "snip1"},
            {"title": "T2", "url": "https://t2", "content": "snip2"},
        ]}
    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get(self, *a, **kw): return _Resp()
    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    s = sp.SearXNGBackend(base_url="http://localhost:8888")
    results = s.search("anything", limit=2)
    assert len(results) == 2
    assert results[0].title == "T1"


def test_searxng_handles_500(monkeypatch):
    from sage.core import search_provider as sp
    class _Resp:
        status_code = 500
        def json(self): return {}
    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get(self, *a, **kw): return _Resp()
    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    s = sp.SearXNGBackend(base_url="http://localhost:8888")
    assert s.search("x") == []


def test_brave_handles_500(monkeypatch):
    from sage.core import search_provider as sp
    class _Resp:
        status_code = 500
        def json(self): return {}
    class _Client:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def get(self, *a, **kw): return _Resp()
    monkeypatch.setitem(sys.modules, "httpx", types.SimpleNamespace(Client=_Client))
    assert sp.BraveBackend(api_key="x").search("query") == []


# ════════════════════════════════════════════════════════════════════════
# core/ast_chunker.py — language coverage + tree_sitter unavailable
# ════════════════════════════════════════════════════════════════════════

def test_ast_chunker_dispatches_javascript(tmp_path):
    from sage.core.ast_chunker import chunk_ast
    p = tmp_path / "x.js"
    p.write_text("export function alpha() {}\n")
    chunks = chunk_ast(p, root=tmp_path)
    assert any("alpha" in c.symbol for c in chunks)


def test_ast_chunker_dispatches_typescript(tmp_path):
    from sage.core.ast_chunker import chunk_ast
    p = tmp_path / "x.ts"
    p.write_text("export class Beta {}\n")
    chunks = chunk_ast(p, root=tmp_path)
    assert any("Beta" in c.symbol for c in chunks)


def test_ast_chunker_with_tree_sitter_returns_none_when_missing(monkeypatch):
    from sage.core import ast_chunker
    monkeypatch.setattr(ast_chunker, "_have_tree_sitter", lambda: False)
    assert ast_chunker.chunk_with_tree_sitter("def f(): pass", "python", "x.py") is None


# ════════════════════════════════════════════════════════════════════════
# core/python_repl.py — empty + cwd + env stripping
# ════════════════════════════════════════════════════════════════════════

def test_python_repl_empty_code_returns_ok():
    from sage.core.python_repl import PythonRepl
    out = PythonRepl().run("")
    assert out.ok is True
    assert out.stdout == ""


def test_python_repl_strips_proxy_env_when_network_disallowed(tmp_path, monkeypatch):
    monkeypatch.setenv("HTTPS_PROXY", "http://forbidden")
    from sage.core.python_repl import PythonRepl
    out = PythonRepl(timeout_s=3).run(
        "import os; print(os.environ.get('HTTPS_PROXY', 'unset'))",
    )
    assert "unset" in out.stdout


def test_python_repl_uses_provided_cwd(tmp_path):
    from sage.core.python_repl import PythonRepl
    target = tmp_path / "scratch"
    target.mkdir()
    out = PythonRepl(timeout_s=3).run("import os; print(os.getcwd())", cwd=str(target))
    # On macOS, /var paths get aliased to /private/var — accept either
    assert str(target) in out.stdout or out.stdout.strip().endswith(target.name)


def test_python_repl_captures_stderr():
    from sage.core.python_repl import PythonRepl
    out = PythonRepl().run("import sys; sys.stderr.write('err'); sys.exit(2)")
    assert "err" in out.stderr
    assert out.exit_code == 2


# ════════════════════════════════════════════════════════════════════════
# core/route.py — long-context + attached-files difficulty hint
# ════════════════════════════════════════════════════════════════════════

def test_route_long_context_promotes_to_hard():
    from sage.core.route import _classify_difficulty, Difficulty
    out = _classify_difficulty("write hello", has_long_context=True, has_attached_files=False)
    assert out == Difficulty.HARD


def test_route_normalize_strips_latest_tag_only():
    from sage.core.route import _normalize_id
    assert _normalize_id("ollama:foo:latest") == "ollama:foo"
    assert _normalize_id("ollama:foo") == "ollama:foo"
    assert _normalize_id("llama_cpp:bar") == "llama_cpp:bar"


# ════════════════════════════════════════════════════════════════════════
# core/verifier.py — best_of_n early returns + critic exception
# ════════════════════════════════════════════════════════════════════════

def test_verifier_zero_samples_clamps_to_one():
    from sage.core.verifier import best_of_n
    result = best_of_n(task="t", generator=lambda temp: "x", n_samples=0)
    assert len(result.all_candidates) == 1


def test_verifier_critic_exception_falls_back_to_lengths():
    from sage.core.verifier import best_of_n

    def bad_critic(prompt: str) -> str:
        raise RuntimeError("model down")

    result = best_of_n(
        task="t",
        generator=lambda temp: "short" if temp < 0.5 else "much longer answer here",
        n_samples=2, validator=lambda out: (True, ""),
        critic=bad_critic,
    )
    # validator path picks the longest among valid → "much longer answer here"
    assert "much longer" in result.winner.output


def test_verifier_generator_exception_yields_empty_candidate():
    from sage.core.verifier import best_of_n

    def bad_gen(temp):
        raise RuntimeError("offline")
    result = best_of_n(task="t", generator=bad_gen, n_samples=2)
    assert all(c.output == "" for c in result.all_candidates)


# ════════════════════════════════════════════════════════════════════════
# core/keep_alive.py — already 90%; backfill remaining branches
# ════════════════════════════════════════════════════════════════════════

def test_keep_alive_no_httpx_returns_false(monkeypatch):
    from sage.core import keep_alive
    if "httpx" in sys.modules:
        monkeypatch.delitem(sys.modules, "httpx", raising=False)
    monkeypatch.setattr("builtins.__import__", lambda name, *a, **kw: (
        (_ for _ in ()).throw(ImportError("no httpx")) if name == "httpx"
        else __import__(name, *a, **kw)
    ))
    assert keep_alive.prewarm("model") is False


# ════════════════════════════════════════════════════════════════════════
# core/prefix_cache.py — corrupt index recovery
# ════════════════════════════════════════════════════════════════════════

def test_prefix_cache_recovers_from_corrupt_index(tmp_path):
    from sage.core.prefix_cache import PrefixCache
    (tmp_path / "_index.json").write_text("not json {{{")
    # Should not raise; should reset to empty
    cache = PrefixCache(root=tmp_path)
    assert cache.stats()["entries"] == 0


# ════════════════════════════════════════════════════════════════════════
# core/few_shot.py — corrupt store + truncation
# ════════════════════════════════════════════════════════════════════════

def test_few_shot_ignores_corrupt_store(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core.few_shot import FewShotStore
    proj = tmp_path / "p"
    proj.mkdir()
    store = FewShotStore(proj)
    # Corrupt the file behind its back
    store.path.write_text("nope nope")
    store2 = FewShotStore(proj)
    assert store2._examples == []


def test_few_shot_record_truncates_long_payloads(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    from sage.core import few_shot
    monkeypatch.setattr(few_shot, "_MAX_PROMPT_CHARS", 50)
    monkeypatch.setattr(few_shot, "_MAX_RESPONSE_CHARS", 50)
    store = few_shot.FewShotStore(tmp_path / "p")
    store.record_accept("x" * 200, "y" * 200)
    saved = store._examples[0]
    assert len(saved.prompt) <= 50
    assert len(saved.response) <= 50


# ════════════════════════════════════════════════════════════════════════
# core/distill.py — log error path + missing distill dir
# ════════════════════════════════════════════════════════════════════════

def test_distill_events_returns_empty_for_missing_file(tmp_path):
    from sage.core.distill import DistillLogger
    log = DistillLogger(session_id="ghost", root=tmp_path)
    log.path.unlink(missing_ok=True)
    assert log.events() == []


def test_distill_events_skips_corrupt_lines(tmp_path):
    from sage.core.distill import DistillLogger
    log = DistillLogger(session_id="s", root=tmp_path)
    log.path.write_text(
        '{"user_prompt":"q","final_response":"a","used_tools":[],'
        '"used_rag":false,"pipeline_phases":[],"project_hash":"","ts":1.0}\n'
        'CORRUPT LINE\n'
        '{"missing_required":1}\n'
    )
    events = log.events()
    assert len(events) == 1
