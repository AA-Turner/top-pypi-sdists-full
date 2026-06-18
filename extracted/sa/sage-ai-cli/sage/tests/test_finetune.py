"""Unit and integration tests for finetune.py."""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
import pytest

from sage.training.finetune import (
    FinetuneConfig,
    FinetuneResult,
    Backend,
    _has_module,
    _is_apple_silicon,
    available_backends,
    _pick_backend,
    install_hint,
    _train_mlx,
    _train_peft,
    _train_unsloth,
    finetune,
)


# ==========================================
# UNIT TESTS
# ==========================================

def test_finetune_config_base_name():
    """Verify FinetuneConfig.base_name parses model strings correctly."""
    c1 = FinetuneConfig(base_model="provider:llama3:latest", corpus_path=Path("/tmp"))
    assert c1.base_name() == "llama3"

    c2 = FinetuneConfig(base_model="models/phi-3", corpus_path=Path("/tmp"))
    # Split tag replaces '/' with '_'
    assert c2.base_name() == "models_phi-3"


def test_has_module(monkeypatch):
    """Verify module presence detection using importlib spec finder."""
    import importlib.util
    original_find = importlib.util.find_spec
    
    def mock_find(name):
        if name in {"mlx", "unsloth"}:
            return importlib.machinery.ModuleSpec(name, None)
        return None

    monkeypatch.setattr(importlib.util, "find_spec", mock_find)
    assert _has_module("mlx") is True
    assert _has_module("unsloth") is True
    assert _has_module("transformers") is False


def test_is_apple_silicon(monkeypatch):
    """Verify Apple Silicon detection matches system platform and machine architecture."""
    import platform
    
    # 1. On macOS Apple Silicon
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "machine", lambda: "arm64")
    assert _is_apple_silicon() is True

    # 2. On macOS Intel
    monkeypatch.setattr(platform, "machine", lambda: "x86_64")
    assert _is_apple_silicon() is False

    # 3. On Linux/Windows
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "machine", lambda: "arm64")
    assert _is_apple_silicon() is False


def test_available_backends(monkeypatch):
    """Verify prioritisation order of usable fine-tuning backends."""
    import platform
    # Mock environment to be Apple Silicon, with mlx and peft installed
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "machine", lambda: "arm64")
    
    installed = {"mlx", "mlx_lm", "peft", "transformers"}
    monkeypatch.setattr("sage.training.finetune._has_module", lambda name: name in installed)
    
    backends = available_backends()
    assert Backend.MLX in backends
    assert Backend.PEFT in backends
    assert Backend.UNSLOTH not in backends
    assert backends[0] == Backend.MLX  # MLX preferred on Apple Silicon


def test_available_backends_unsloth(monkeypatch):
    """Verify detection of the Unsloth backend when installed."""
    import platform
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "machine", lambda: "x86_64")
    
    installed = {"unsloth"}
    monkeypatch.setattr("sage.training.finetune._has_module", lambda name: name in installed)
    
    backends = available_backends()
    assert Backend.UNSLOTH in backends



def test_pick_backend(monkeypatch):
    """Verify backend resolution handles manual requests and fallbacks."""
    # Mock available list
    monkeypatch.setattr("sage.training.finetune.available_backends", lambda: ["mlx", "peft"])

    # 1. Auto resolves to first option
    assert _pick_backend("auto") == "mlx"

    # 2. Explicit requested is available - return it
    assert _pick_backend("peft") == "peft"

    # 3. Explicit requested is not available - return None
    assert _pick_backend("unsloth") is None

    # 4. Nothing available
    monkeypatch.setattr("sage.training.finetune.available_backends", lambda: [])
    assert _pick_backend("auto") is None


def test_install_hint(monkeypatch):
    """Verify install CLI hints are context aware for system architectures."""
    # 1. macOS Apple Silicon
    monkeypatch.setattr("sage.training.finetune._is_apple_silicon", lambda: True)
    assert "mlx-lm" in install_hint()

    # 2. Linux / Intel
    monkeypatch.setattr("sage.training.finetune._is_apple_silicon", lambda: False)
    assert "unsloth" in install_hint()


def test_train_mlx_success(monkeypatch, tmp_path):
    """Verify successful MLX training returns FinetuneResult."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", max_steps=10)
    
    class MockCompletedProcess:
        returncode = 0
        stdout = "iter 10: loss 0.12"
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: MockCompletedProcess())
    res = _train_mlx(cfg, tmp_path / "out")
    assert res.success is True
    assert res.backend == Backend.MLX
    assert res.adapter_dir == tmp_path / "out"
    assert res.steps_run == 10
    assert "iter 10" in res.meta.get("stdout_tail", "")


def test_train_mlx_failure(monkeypatch, tmp_path):
    """Verify MLX training process failures are handled and returned."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", max_steps=10)
    
    class MockCompletedProcess:
        returncode = 1
        stdout = ""
        stderr = "Out of memory"

    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: MockCompletedProcess())
    res = _train_mlx(cfg, tmp_path / "out")
    assert res.success is False
    assert "exit 1: Out of memory" in res.error


def test_train_mlx_timeout(monkeypatch, tmp_path):
    """Verify MLX subprocess timeouts are caught."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", max_steps=10)
    
    def failing_run(*a, **kw):
        raise subprocess.TimeoutExpired(cmd=a[0], timeout=3600)

    monkeypatch.setattr(subprocess, "run", failing_run)
    res = _train_mlx(cfg, tmp_path / "out")
    assert res.success is False
    assert "timed out" in res.error


def test_train_peft_exception(tmp_path):
    """Verify PEFT exceptions (e.g. missing dependencies) fail gracefully."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl")
    # PEFT backend requires transformers, which we expect to raise errors or run
    res = _train_peft(cfg, tmp_path / "out")
    assert res.success is False
    assert res.backend == Backend.PEFT
    assert res.adapter_dir is None
    assert res.error is not None


def test_train_unsloth_exception(tmp_path):
    """Verify Unsloth exceptions fail gracefully."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl")
    res = _train_unsloth(cfg, tmp_path / "out")
    assert res.success is False
    assert res.backend == Backend.UNSLOTH
    assert res.error is not None


# ==========================================
# INTEGRATION TESTS
# ==========================================

def test_integration_finetune_cache_hit(tmp_path, monkeypatch):
    """Verify finetune returns success instantly on adapter cache hits without training."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl")
    
    # Mock CorpusManager.corpus_hash
    monkeypatch.setattr("sage.training.corpus.CorpusManager.corpus_hash", lambda p: "cached-hash-123")
    
    # Mock AdapterCache resolution
    class MockAdapterCache:
        def __init__(self, bucket):
            pass
        def get_or_resolve(self, ref):
            return Path("/cached/adapter/path")

    monkeypatch.setattr("sage.training.finetune.AdapterCache", MockAdapterCache)

    # Execute
    res = finetune(cfg, bucket="gs://test-bucket")
    
    assert res.success is True
    assert res.backend == "cache"
    assert res.adapter_dir == Path("/cached/adapter/path")
    assert res.duration_s == 0.0
    assert res.meta.get("hit") == "cache"


def test_integration_finetune_cache_only_miss(tmp_path, monkeypatch):
    """Verify finetune cache_only mode fails immediately on cache misses."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl")
    monkeypatch.setattr("sage.training.corpus.CorpusManager.corpus_hash", lambda p: "cached-hash-123")
    
    class MockAdapterCache:
        def __init__(self, bucket): pass
        def get_or_resolve(self, ref): return None

    monkeypatch.setattr("sage.training.finetune.AdapterCache", MockAdapterCache)

    res = finetune(cfg, bucket="gs://test-bucket", cache_only=True)
    assert res.success is False
    assert res.backend == "cache"
    assert "not in cache" in res.error


def test_integration_finetune_run_mlx_backend(tmp_path, monkeypatch):
    """Verify complete fine-tuning pipeline flow when cache misses and MLX is executed."""
    # Write dummy corpus
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text("dummy", encoding="utf-8")
    
    cfg = FinetuneConfig("ollama:phi3", corpus, backend="mlx")
    monkeypatch.setattr("sage.training.corpus.CorpusManager.corpus_hash", lambda p: "new-hash-456")
    
    # Mock cache misses
    class MockAdapterCache:
        def __init__(self, bucket):
            self.pushed_ref = None
            self.pushed_meta = None

        def get_or_resolve(self, ref):
            return None

        def push(self, ref, meta):
            self.pushed_ref = ref
            self.pushed_meta = meta

    cache_instance = MockAdapterCache("bucket")
    monkeypatch.setattr("sage.training.finetune.AdapterCache", lambda *a, **kw: cache_instance)

    # Mock MLX backend as available
    monkeypatch.setattr("sage.training.finetune._pick_backend", lambda req: Backend.MLX)

    # Mock successful MLX training run
    class MockCompletedProcess:
        returncode = 0
        stdout = "iter 200: loss 0.05"
        stderr = ""

    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: MockCompletedProcess())

    # Run fine-tuning
    res = finetune(cfg, bucket="gs://test-bucket")

    # Assert success and verification
    assert res.success is True
    assert res.backend == Backend.MLX
    assert res.steps_run == 200
    
    # Assert cache upload was triggered
    assert cache_instance.pushed_ref is not None
    assert cache_instance.pushed_ref.base_name == "phi3"
    assert cache_instance.pushed_ref.corpus_hash == "new-hash-456"
    assert cache_instance.pushed_meta.backend == Backend.MLX
    assert res.meta.get("pushed_to_gcs") is True


def test_train_mlx_generic_exception(monkeypatch, tmp_path):
    """Verify generic exception in MLX training handles gracefully."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", max_steps=10)
    def failing_run(*a, **kw):
        raise OSError("Permission denied")
    monkeypatch.setattr(subprocess, "run", failing_run)
    res = _train_mlx(cfg, tmp_path / "out")
    assert res.success is False
    assert "OSError" in res.error


def test_train_peft_mock_success(monkeypatch, tmp_path):
    """Verify PEFT success path runs cleanly with mock HF modules."""
    # Write dummy corpus
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text('{"instruction": "x", "input": "y", "output": "z"}', encoding="utf-8")
    cfg = FinetuneConfig("ollama:phi3", corpus)

    # Setup mock imports
    class MockTorch:
        class cuda:
            @staticmethod
            def is_available(): return False
        float16 = "float16"

    class MockTokenizer:
        pad_token = None
        eos_token = "eos"
        def __call__(self, text, **kwargs): return {"input_ids": [1, 2, 3]}
        def save_pretrained(self, path): Path(path).mkdir(parents=True, exist_ok=True)

    class MockModel:
        def save_pretrained(self, path): Path(path).mkdir(parents=True, exist_ok=True)

    class MockLoraConfig:
        def __init__(self, **kwargs): pass

    class MockTaskType:
        CAUSAL_LM = "causal_lm"

    class MockDataset:
        column_names = ["instruction", "input", "output"]
        def map(self, func, remove_columns=None):
            # Simulate processing items
            func({"instruction": "x", "input": "y", "output": "z"})
            return self

    class MockTrainer:
        def __init__(self, **kwargs): pass
        def train(self): pass

    class MockTrainingArguments:
        def __init__(self, **kwargs): pass

    monkeypatch.setitem(sys.modules, "torch", MockTorch)
    monkeypatch.setitem(sys.modules, "datasets", type("ds", (), {"load_dataset": lambda *a, **kw: MockDataset()}))
    monkeypatch.setitem(sys.modules, "peft", type("peft", (), {"LoraConfig": MockLoraConfig, "get_peft_model": lambda m, c: m, "TaskType": MockTaskType}))
    
    transformers = type("tf", (), {
        "AutoModelForCausalLM": type("am", (), {"from_pretrained": lambda *a, **kw: MockModel()}),
        "AutoTokenizer": type("at", (), {"from_pretrained": lambda *a, **kw: MockTokenizer()}),
        "DataCollatorForLanguageModeling": lambda tokenizer, mlm: None,
        "Trainer": MockTrainer,
        "TrainingArguments": MockTrainingArguments,
    })
    monkeypatch.setitem(sys.modules, "transformers", transformers)

    res = _train_peft(cfg, tmp_path / "out")
    assert res.success is True
    assert res.backend == Backend.PEFT
    assert res.adapter_dir == tmp_path / "out"


def test_train_unsloth_mock_success(monkeypatch, tmp_path):
    """Verify Unsloth success path runs cleanly with mock unsloth modules."""
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text('{"instruction": "x", "input": "y", "output": "z"}', encoding="utf-8")
    cfg = FinetuneConfig("ollama:phi3", corpus)

    class MockModel:
        def save_pretrained(self, path): Path(path).mkdir(parents=True, exist_ok=True)

    class MockTokenizer:
        def save_pretrained(self, path): Path(path).mkdir(parents=True, exist_ok=True)

    class MockFastLanguageModel:
        @staticmethod
        def from_pretrained(**kwargs):
            return MockModel(), MockTokenizer()
        @staticmethod
        def get_peft_model(model, **kwargs):
            return model

    class MockSFTTrainer:
        def __init__(self, **kwargs): pass
        def train(self): pass

    class MockTrainingArguments:
        def __init__(self, **kwargs): pass

    monkeypatch.setitem(sys.modules, "datasets", type("ds", (), {"load_dataset": lambda *a, **kw: "mock_dataset"}))
    monkeypatch.setitem(sys.modules, "unsloth", type("unsloth", (), {"FastLanguageModel": MockFastLanguageModel}))
    monkeypatch.setitem(sys.modules, "trl", type("trl", (), {"SFTTrainer": MockSFTTrainer}))
    monkeypatch.setitem(sys.modules, "transformers", type("tf", (), {"TrainingArguments": MockTrainingArguments}))

    res = _train_unsloth(cfg, tmp_path / "out")
    assert res.success is True
    assert res.backend == Backend.UNSLOTH
    assert res.adapter_dir == tmp_path / "out"


def test_finetune_no_backend_available(monkeypatch, tmp_path):
    """Verify finetune returns fail result if no backend fits requested config."""
    cfg = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", backend="auto")
    
    # Mock cache miss
    class MockAdapterCache:
        def __init__(self, bucket): pass
        def get_or_resolve(self, ref): return None
    monkeypatch.setattr("sage.training.finetune.AdapterCache", MockAdapterCache)
    monkeypatch.setattr("sage.training.corpus.CorpusManager.corpus_hash", lambda p: "new-hash")

    # Mock no backends available
    monkeypatch.setattr("sage.training.finetune._pick_backend", lambda req: None)

    res = finetune(cfg, bucket="gs://bucket")
    assert res.success is False
    assert res.backend == "none"
    assert "No fine-tuning backend installed" in res.error


def test_integration_finetune_unsloth_and_peft_routing(monkeypatch, tmp_path):
    """Verify finetune public entry point successfully routes and processes Unsloth and PEFT backends."""
    # Mock cache misses
    class MockAdapterCache:
        def __init__(self, bucket): pass
        def get_or_resolve(self, ref): return None
        def push(self, ref, meta): pass
    monkeypatch.setattr("sage.training.finetune.AdapterCache", MockAdapterCache)
    monkeypatch.setattr("sage.training.corpus.CorpusManager.corpus_hash", lambda p: "new-hash")

    # Mock out_dir
    out_dir = tmp_path / "out"

    # Verify Unsloth routing
    cfg_unsloth = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", backend="unsloth", output_dir=out_dir)
    monkeypatch.setattr("sage.training.finetune._pick_backend", lambda req: Backend.UNSLOTH)
    
    # Mock the actual train_unsloth call to return mock success
    monkeypatch.setattr("sage.training.finetune._train_unsloth", lambda cfg, path: FinetuneResult(True, Backend.UNSLOTH, path, 1.0))
    res_u = finetune(cfg_unsloth)
    assert res_u.success is True
    assert res_u.backend == Backend.UNSLOTH

    # Verify PEFT routing
    cfg_peft = FinetuneConfig("ollama:phi3", tmp_path / "corpus.jsonl", backend="peft", output_dir=out_dir)
    monkeypatch.setattr("sage.training.finetune._pick_backend", lambda req: Backend.PEFT)
    
    # Mock the actual train_peft call to return mock success
    monkeypatch.setattr("sage.training.finetune._train_peft", lambda cfg, path: FinetuneResult(True, Backend.PEFT, path, 1.0))
    res_p = finetune(cfg_peft)
    assert res_p.success is True
    assert res_p.backend == Backend.PEFT

