"""Unit and integration tests for lora_swap.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import pytest

from sage.core.lora_swap import LoraSwap, ResolvedAdapter
from sage.training.cache import AdapterRef


# ==========================================
# UNIT TESTS
# ==========================================

class DummyConfig:
    def __init__(self):
        self.gcs_corpus_bucket = "gs://mock-bucket"


def test_lora_swap_init(monkeypatch):
    """Verify initialization and load_config fallback behavior."""
    # Custom config
    cfg = DummyConfig()
    swap = LoraSwap(cfg)
    assert swap.cfg == cfg

    # Default config fallback
    monkeypatch.setattr("sage.config.load_config", lambda: cfg)
    swap_default = LoraSwap()
    assert swap_default.cfg == cfg


def test_lora_swap_ref_for_none():
    """Verify _ref_for returns None under various missing prerequisites."""
    swap = LoraSwap(DummyConfig())
    # 1. corpus_mgr is None
    swap.corpus_mgr = None
    assert swap._ref_for(Path("/tmp"), "phi-3:latest") is None


def test_lora_swap_ref_for_missing_latest_local(tmp_path):
    """Verify _ref_for returns None if the project has no latest_local snapshot."""
    swap = LoraSwap(DummyConfig())
    
    class MockProject:
        def __init__(self):
            self.latest_local = tmp_path / "nonexistent"

    class MockCorpusManager:
        def project(self, cwd):
            return MockProject()

    swap.corpus_mgr = MockCorpusManager()
    assert swap._ref_for(tmp_path, "phi-3:latest") is None


def test_lora_swap_ref_for_valid_project(tmp_path, monkeypatch):
    """Verify _ref_for returns the correct AdapterRef for a valid project."""
    swap = LoraSwap(DummyConfig())
    latest_file = tmp_path / "latest.jsonl"
    latest_file.write_text("dummy jsonl content", encoding="utf-8")

    class MockProject:
        def __init__(self):
            self.latest_local = latest_file

    class MockCorpusManager:
        def project(self, cwd):
            return MockProject()

    swap.corpus_mgr = MockCorpusManager()
    
    # 1. Base model split tests
    ref = swap._ref_for(tmp_path, "ollama:llama3:8b-instruct-q4")
    assert ref is not None
    assert ref.base_name == "llama3"
    assert ref.corpus_hash == "2be928ee23130020"

    ref2 = swap._ref_for(tmp_path, "ollama:phi-3:latest")
    assert ref2 is not None
    assert ref2.base_name == "phi-3"


def test_lora_swap_adapter_for_missing():
    """Verify adapter_for returns missing source if cache or ref is absent."""
    swap = LoraSwap(DummyConfig())
    
    # 1. ref is None
    swap.corpus_mgr = None
    resolved = swap.adapter_for(Path("/tmp"), base_model="llama3:latest")
    assert resolved.source == "missing"
    assert resolved.adapter_dir is None

    # 2. cache is None (with a valid ref mock)
    class MockRef:
        corpus_hash = "hash"
    
    swap._ref_for = lambda cwd, model: MockRef()
    swap.cache = None
    resolved2 = swap.adapter_for(Path("/tmp"), base_model="llama3:latest")
    assert resolved2.source == "missing"


def test_lora_swap_adapter_for_local_and_gcs():
    """Verify adapter_for sources from local cache first, then GCS pull, then fails to missing."""
    swap = LoraSwap(DummyConfig())
    
    class MockRef:
        corpus_hash = "abc123hash"
        def local_dir(self):
            return Path("/local/dir")

    swap._ref_for = lambda cwd, model: MockRef()

    # Mock Cache
    class MockCache:
        def __init__(self):
            self.local_exists = False
            self.pull_success = False

        def has_local(self, ref):
            return self.local_exists

        def pull(self, ref):
            return self.pull_success

    cache = MockCache()
    swap.cache = cache

    # Case A: adapter is already local
    cache.local_exists = True
    res = swap.adapter_for(Path("/tmp"), base_model="llama3")
    assert res.source == "local"
    assert res.adapter_dir == Path("/local/dir")

    # Case B: adapter is not local, but GCS pull succeeds
    cache.local_exists = False
    cache.pull_success = True
    res = swap.adapter_for(Path("/tmp"), base_model="llama3")
    assert res.source == "gcs"
    assert res.adapter_dir == Path("/local/dir")

    # Case C: adapter not local, GCS pull fails
    cache.pull_success = False
    res = swap.adapter_for(Path("/tmp"), base_model="llama3")
    assert res.source == "missing"
    assert res.adapter_dir is None


def test_lora_swap_schedule_training_noop():
    """Verify schedule_training_if_missing does not call subprocess if adapter is local or pulled."""
    swap = LoraSwap(DummyConfig())
    expected = ResolvedAdapter("llama3", "hash", Path("/dir"), "local")
    swap.adapter_for = lambda cwd, base_model: expected

    # If it is local, it should skip training and return directly
    resolved = swap.schedule_training_if_missing(Path("/tmp"), base_model="llama3")
    assert resolved == expected


def test_lora_swap_schedule_training_triggered(monkeypatch):
    """Verify schedule_training_if_missing runs finetuning subprocess when adapter is missing."""
    swap = LoraSwap(DummyConfig())
    expected = ResolvedAdapter("llama3", "hash", None, "missing")
    swap.adapter_for = lambda cwd, base_model: expected

    popen_called = []
    call_called = []

    class MockPopen:
        def __init__(self, cmd, **kwargs):
            popen_called.append(cmd)

    monkeypatch.setattr(subprocess, "Popen", MockPopen)
    monkeypatch.setattr(subprocess, "call", lambda cmd, **kw: call_called.append(cmd))

    # 1. Background execution
    resolved_bg = swap.schedule_training_if_missing(Path("/tmp"), base_model="llama3", in_background=True)
    assert resolved_bg == expected
    assert len(popen_called) == 1
    assert "finetune" in popen_called[0]
    assert "llama3" in popen_called[0]

    # 2. Foreground execution
    resolved_fg = swap.schedule_training_if_missing(Path("/tmp"), base_model="llama3", in_background=False)
    assert resolved_fg == expected
    assert len(call_called) == 1
    assert "finetune" in call_called[0]


# ==========================================
# INTEGRATION TESTS
# ==========================================

def test_integration_lora_swap_flow(tmp_path, monkeypatch):
    """Integration test validating LoraSwap resolving behavior with fake directory structure."""
    swap = LoraSwap(DummyConfig())
    
    # Setup mock project with a corpus file so that _ref_for succeeds
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    
    # Stub Project & Corpus Manager
    class MockProject:
        def __init__(self):
            self.latest_local = project_dir / "latest.jsonl"
            self.latest_local.write_text("content", encoding="utf-8")

    class MockCorpusManager:
        def project(self, cwd):
            return MockProject()
        
        @staticmethod
        def corpus_hash(path):
            return "int-hash-val"

    swap.corpus_mgr = MockCorpusManager()

    # Stub Cache
    class MockCache:
        def __init__(self):
            self.has_it = False

        def has_local(self, ref):
            return self.has_it

        def pull(self, ref):
            return False

    cache = MockCache()
    swap.cache = cache

    # Mock Subprocess Popen
    popen_cmds = []
    class MockPopen:
        def __init__(self, cmd, **kwargs):
            popen_cmds.append(cmd)

    monkeypatch.setattr(subprocess, "Popen", MockPopen)

    # 1. Run initially - should be missing, triggers background training
    res1 = swap.schedule_training_if_missing(project_dir, base_model="ollama:llama3:latest", in_background=True)
    assert res1.source == "missing"
    assert res1.adapter_dir is None
    assert len(popen_cmds) == 1
    assert "ollama:llama3:latest" in popen_cmds[0]

    # 2. Simulate training complete (cache now has local adapter)
    cache.has_it = True
    
    # 3. Call adapter_for again - should resolve to local successfully
    res2 = swap.adapter_for(project_dir, base_model="ollama:llama3:latest")
    assert res2.source == "local"
    assert res2.corpus_hash == "ed7002b439e9ac84"
    assert res2.adapter_dir is not None


def test_lora_swap_init_exception(monkeypatch):
    """Verify fallback when AdapterCache instantiation raises an exception."""
    def failing_init(*a, **kw):
        raise ValueError("mock init error")
    monkeypatch.setattr("sage.training.cache.AdapterCache", failing_init)
    swap = LoraSwap(DummyConfig())
    assert swap.cache is None
    assert swap.corpus_mgr is None


def test_lora_swap_schedule_training_popen_exception(monkeypatch):
    """Verify that schedule_training_if_missing handles Popen exceptions gracefully."""
    swap = LoraSwap(DummyConfig())
    expected = ResolvedAdapter("llama3", "hash", None, "missing")
    swap.adapter_for = lambda cwd, base_model: expected

    def failing_popen(*a, **kw):
        raise OSError("failed to start process")

    monkeypatch.setattr(subprocess, "Popen", failing_popen)

    resolved = swap.schedule_training_if_missing(Path("/tmp"), base_model="llama3", in_background=True)
    assert resolved == expected

