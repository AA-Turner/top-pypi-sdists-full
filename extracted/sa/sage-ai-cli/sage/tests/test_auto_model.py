"""Unit and integration tests for auto_model.py."""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path
import pytest

from sage.core.auto_model import (
    Candidate,
    _is_coder,
    _available_ram_gb,
    _ollama_models,
    _llama_cpp_models,
    list_installed_models,
    pick_best_coder,
    auto_pick_default_model,
)


# ==========================================
# UNIT TESTS
# ==========================================

def test_candidate_score():
    """Verify Candidate scoring logic for coder and non-coder models."""
    c1 = Candidate("ollama:llama3", "ollama", "llama3", 4.5, is_coder=False)
    # Score for non-coder is size capped at 80
    assert c1.score == 4.5

    c2 = Candidate("ollama:deepseek-coder:6.7b", "ollama", "deepseek-coder", 4.0, is_coder=True)
    # Score for coder is size + 100
    assert c2.score == 104.0

    c3 = Candidate("llama_cpp:huge-model", "llama_cpp", "huge-model", 120.0, is_coder=False)
    # Size-gb capped at 80.0
    assert c3.score == 80.0


def test_is_coder():
    """Verify classification of models as coders by naming convention."""
    assert _is_coder("qwen2.5-coder") is True
    assert _is_coder("deepseek-coder-v2") is True
    assert _is_coder("starcoder2-3b") is True
    assert _is_coder("llama3-8b") is False
    assert _is_coder("phi3") is False


def test_available_ram_gb(monkeypatch):
    """Verify virtual memory detection fallback logic."""
    # Case A: psutil is available
    class MockVirtualMemory:
        def __init__(self):
            self.available = 16 * (1024 ** 3)
            
    class MockPsutil:
        @staticmethod
        def virtual_memory():
            return MockVirtualMemory()
            
    monkeypatch.setitem(sys.modules, "psutil", MockPsutil)
    assert _available_ram_gb() == 16.0

    # Case B: psutil fails/missing, sysctl fallback on Darwin/Mac
    monkeypatch.setitem(sys.modules, "psutil", None)
    
    class MockUname:
        sysname = "Darwin"
    monkeypatch.setattr(os, "uname", lambda: MockUname)

    def mock_run(cmd, **kwargs):
        class MockCompletedProcess:
            returncode = 0
            stdout = str(32 * (1024 ** 3))
        return MockCompletedProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert _available_ram_gb() == 32.0

    # Case C: all systems fail, defaults to 16.0
    def failing_run(*a, **kw):
        raise ValueError("mock error")
    monkeypatch.setattr(subprocess, "run", failing_run)
    assert _available_ram_gb() == 16.0


def test_ollama_models_mock_http(monkeypatch):
    """Verify parsing Ollama model response from API tags."""
    # Setup HTTP mock
    class MockResponse:
        status_code = 200
        def json(self):
            return {
                "models": [
                    {"name": "qwen2.5-coder:7b", "size": 4.7 * (1024 ** 3)},
                    {"name": "llama3:latest", "size": 4.8 * (1024 ** 3)},
                    # Malformed/unrelated item
                    None,
                    {"size": 1000}
                ]
            }

    class MockHttpx:
        @staticmethod
        def get(url, timeout):
            return MockResponse()

    monkeypatch.setitem(sys.modules, "httpx", MockHttpx)
    
    candidates = _ollama_models()
    assert len(candidates) == 2
    
    assert candidates[0].qualified_id == "ollama:qwen2.5-coder:7b"
    assert candidates[0].base_name == "qwen2.5-coder"
    assert candidates[0].is_coder is True
    assert abs(candidates[0].size_gb - 4.7) < 0.01

    assert candidates[1].qualified_id == "ollama:llama3:latest"
    assert candidates[1].is_coder is False


def test_ollama_models_http_error(monkeypatch):
    """Verify _ollama_models catches exceptions and errors gracefully."""
    class MockHttpxError:
        @staticmethod
        def get(url, timeout):
            raise ConnectionError("Connection refused")
            
    monkeypatch.setitem(sys.modules, "httpx", MockHttpxError)
    assert _ollama_models() == []


def test_llama_cpp_models_filtering(tmp_path):
    """Verify _llama_cpp_models checks gguf extensions and filters small files."""
    # Prepare mock files
    (tmp_path / "small.gguf").write_text("a" * 1000)  # 1KB - under 0.05GB limit
    
    large_file = tmp_path / "qwen-coder.gguf"
    large_file.write_text("a" * 100)
    # Force mock filesystem size calculation using monkeypatch
    original_stat = Path.stat
    def mock_stat(self):
        class MockStat:
            st_size = int(4.5 * (1024 ** 3)) # 4.5 GB
        if self.name == "qwen-coder.gguf":
            return MockStat()
        return original_stat(self)

    import unittest.mock as mock
    with mock.patch.object(Path, "stat", mock_stat):
        candidates = _llama_cpp_models(tmp_path)
        
    assert len(candidates) == 1
    assert candidates[0].qualified_id == "llama_cpp:qwen-coder"
    assert candidates[0].is_coder is True
    assert abs(candidates[0].size_gb - 4.5) < 0.01


def test_pick_best_coder():
    """Verify that picking logic scores correctly and handles RAM limit caps."""
    candidates = [
        Candidate("ollama:llama3", "ollama", "llama3", 4.0, is_coder=False),
        Candidate("llama_cpp:qwen-coder-32b", "llama_cpp", "qwen-coder-32b", 32.0, is_coder=True),
        Candidate("llama_cpp:qwen-coder-7b", "llama_cpp", "qwen-coder-7b", 7.0, is_coder=True),
    ]

    # Case A: Plenty of RAM (64GB). Large coder should fit and get chosen.
    best = pick_best_coder(candidates, available_ram_gb=64.0)
    assert best is not None
    assert best.qualified_id == "llama_cpp:qwen-coder-32b"

    # Case B: Limited RAM (16GB). Capping limit = 16 * 1.5 = 24GB.
    # The 32B model is too large, so we pick the 7B coder.
    best_limited = pick_best_coder(candidates, available_ram_gb=16.0)
    assert best_limited is not None
    assert best_limited.qualified_id == "llama_cpp:qwen-coder-7b"

    # Case C: Empty candidates
    assert pick_best_coder([], available_ram_gb=16.0) is None


def test_auto_pick_default_model(monkeypatch):
    """Verify auto_pick resolves default models, preserving existing coder configurations."""
    # Case A: Current default is already a coder - keep it
    assert auto_pick_default_model("ollama:qwen2.5-coder") == "ollama:qwen2.5-coder"
    assert auto_pick_default_model("llama_cpp:deepseek-coder:6.7b") == "llama_cpp:deepseek-coder:6.7b"

    # Case B: Current default is not a coder, list is empty - fallbacks
    monkeypatch.setattr("sage.core.auto_model.list_installed_models", lambda *a: [])
    assert auto_pick_default_model("ollama:llama3") == "ollama:llama3"
    assert auto_pick_default_model("") == "llama_cpp:llama3.2-3b"

    # Case C: Current default not coder, list has options - picks best coder
    candidates = [
        Candidate("ollama:qwen-coder", "ollama", "qwen-coder", 4.0, is_coder=True)
    ]
    monkeypatch.setattr("sage.core.auto_model.list_installed_models", lambda *a: candidates)
    monkeypatch.setattr("sage.core.auto_model._available_ram_gb", lambda: 16.0)
    assert auto_pick_default_model("ollama:llama3") == "ollama:qwen-coder"


# ==========================================
# INTEGRATION TESTS
# ==========================================

def test_integration_auto_model_selection_flow(tmp_path, monkeypatch):
    """Integration test validating list_installed_models and pick_best_coder on mock workspace."""
    # Stub Ollama tags endpoint to return a coder model
    class MockOllamaResponse:
        status_code = 200
        def json(self):
            return {
                "models": [
                    {"name": "deepseek-coder:6.7b", "size": int(4.0 * (1024 ** 3))}
                ]
            }
    
    class MockHttpx:
        @staticmethod
        def get(url, timeout):
            return MockOllamaResponse()

    monkeypatch.setitem(sys.modules, "httpx", MockHttpx)

    # Prepare mock llama_cpp local models directory with GGUF files
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    
    # 1. Non-coder model
    (models_dir / "llama3.gguf").write_text("non-coder content")
    # 2. Coder model
    (models_dir / "codellama-7b.gguf").write_text("coder content")

    # Mock Path stat sizes
    original_stat = Path.stat
    def mock_stat(self):
        class MockStat:
            st_size = int(6.5 * (1024 ** 3)) # 6.5 GB
        if self.suffix == ".gguf":
            return MockStat()
        return original_stat(self)

    # Mock RAM to 16GB
    monkeypatch.setattr("sage.core.auto_model._available_ram_gb", lambda: 16.0)

    import unittest.mock as mock
    with mock.patch.object(Path, "stat", mock_stat):
        # Scan and verify lists
        candidates = list_installed_models(models_dir)
        assert len(candidates) == 3 # 1 ollama + 2 llama_cpp
        
        # Verify best coder selection (Deepseek Coder or CodeLlama)
        best = pick_best_coder(candidates)
        assert best is not None
        assert best.is_coder is True
        assert best.qualified_id in {"ollama:deepseek-coder:6.7b", "llama_cpp:codellama-7b"}


def test_ollama_models_non_200_status(monkeypatch):
    """Verify _ollama_models returns empty list if status code is not 200."""
    class MockResponse:
        status_code = 500
        def json(self):
            return {}

    class MockHttpx:
        @staticmethod
        def get(url, timeout):
            return MockResponse()

    monkeypatch.setitem(sys.modules, "httpx", MockHttpx)
    assert _ollama_models() == []


def test_llama_cpp_models_nonexistent_dir():
    """Verify _llama_cpp_models returns empty list if directory is missing."""
    assert _llama_cpp_models(Path("/nonexistent/path/here/12345")) == []


def test_llama_cpp_models_stat_os_error(tmp_path):
    """Verify _llama_cpp_models ignores files that raise OSError during stat."""
    (tmp_path / "broken.gguf").write_text("dummy")
    
    original_stat = Path.stat
    def mock_stat(self):
        if self.name == "broken.gguf":
            raise OSError("Permission denied")
        return original_stat(self)

    import unittest.mock as mock
    with mock.patch.object(Path, "stat", mock_stat):
        assert _llama_cpp_models(tmp_path) == []


def test_list_installed_models_default_path(tmp_path, monkeypatch):
    """Verify list_installed_models defaults to ~/.sage/models if none provided."""
    # Mock Path.home to return tmp_path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    
    # Mock httpx to return nothing so we don't query Ollama
    class MockHttpx:
        @staticmethod
        def get(url, timeout):
            raise Exception("no ollama")
    monkeypatch.setitem(sys.modules, "httpx", MockHttpx)
    
    # Create the default models directory and add a model file
    default_dir = tmp_path / ".sage" / "models"
    default_dir.mkdir(parents=True, exist_ok=True)
    (default_dir / "test.gguf").write_text("model content")
    
    original_stat = Path.stat
    def mock_stat(self):
        class MockStat:
            st_size = int(1.0 * (1024 ** 3)) # 1 GB
        if self.name == "test.gguf":
            return MockStat()
        return original_stat(self)
        
    import unittest.mock as mock
    with mock.patch.object(Path, "stat", mock_stat):
        candidates = list_installed_models()
        assert len(candidates) == 1
        assert candidates[0].base_name == "test"

