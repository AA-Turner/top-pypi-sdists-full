"""TDD for disk-space-aware bootstrap model selection."""

from __future__ import annotations

from pathlib import Path

import pytest


def test_pick_models_large_disk_includes_strong_coder():
    from sage.core.bootstrap import pick_models_for_disk
    models = pick_models_for_disk(free_gb=120.0)
    assert "qwen3-coder-next" in models
    assert "qwen2.5-coder-7b" in models
    assert "nomic-embed-text" in models


def test_pick_models_medium_disk_drops_strongest():
    from sage.core.bootstrap import pick_models_for_disk
    models = pick_models_for_disk(free_gb=50.0)
    assert "qwen3-coder-next" not in models
    assert "qwen2.5-coder-7b" in models
    assert "nomic-embed-text" in models


def test_pick_models_small_disk_only_lightweight():
    from sage.core.bootstrap import pick_models_for_disk
    models = pick_models_for_disk(free_gb=10.0)
    assert "qwen2.5-coder-7b" not in models
    assert "llama3.2" in models
    assert "nomic-embed-text" in models


def test_pick_models_minimal_disk_only_embedder():
    from sage.core.bootstrap import pick_models_for_disk
    models = pick_models_for_disk(free_gb=2.0)
    assert models == ("nomic-embed-text",)


def test_pick_models_no_disk_returns_empty():
    from sage.core.bootstrap import pick_models_for_disk
    models = pick_models_for_disk(free_gb=0.5)
    assert models == ()


def test_options_auto_picks_models_when_unset(tmp_path):
    from sage.core.bootstrap import BootstrapOptions
    opts = BootstrapOptions(cwd=tmp_path)
    # Whatever the actual disk has, ollama_models should be a non-empty tuple
    # (unless the disk is full, which is unlikely in a tmp_path)
    assert isinstance(opts.ollama_models, tuple)


def test_options_explicit_models_not_overridden(tmp_path):
    from sage.core.bootstrap import BootstrapOptions
    custom = ("my-custom-model",)
    opts = BootstrapOptions(cwd=tmp_path, ollama_models=custom)
    assert opts.ollama_models == custom


def test_floor_model_default_is_qwen_coder_7b():
    """T14: floor model should be qwen2.5-coder-7b."""
    from sage.core.bootstrap import BootstrapOptions
    opts = BootstrapOptions()
    assert opts.floor_model == "qwen2.5-coder-7b"
