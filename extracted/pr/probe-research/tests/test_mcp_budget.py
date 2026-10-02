"""Reference counting and whole-text limits, without an MCP/framework stand-in."""

from __future__ import annotations

import builtins
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from probe.mcp import budget


@pytest.mark.parametrize("limit,byte_limit", [(512, 4096), (2000, 16000), (8000, 64000)])
def test_supported_budgets_have_exact_decimal_byte_limits(limit, byte_limit):
    configured = budget.Budget(limit)
    assert configured.token_limit == limit
    assert configured.byte_limit == byte_limit
    assert budget.Budget().token_limit == 2000


@pytest.mark.parametrize("value", [None, True, False, 0, -1, 511, 8001, 512.0, "512", object()])
def test_invalid_budget_is_rejected_without_coercion_or_echo(value):
    with pytest.raises(budget.InvalidBudget) as caught:
        budget.Budget(value)
    assert str(caught.value) == "token_budget must be an integer from 512 through 8000."


def test_compact_serialization_is_deterministic_and_preserves_json_content():
    value = {"z": [True, None, "é"], "a": 1}
    text = budget.serialize(value)
    assert text == '{"a":1,"z":[true,null,"é"]}'
    assert budget.serialize(dict(reversed(list(value.items())))) == text
    assert json.loads(text) == value
    assert budget.count_tokens(text) == 13
    assert budget.Budget().fits(value)


@pytest.mark.parametrize(
    "value",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
        b"bytes",
        (1, 2),
        {1: "integer key"},
        {"nested": {"bad": object()}},
        {"text": "\ud800"},
        {"\udfff": "bad key"},
    ],
)
def test_non_json_and_invalid_unicode_fail_closed(value):
    with pytest.raises(budget.SerializationError) as caught:
        budget.serialize(value)
    assert str(caught.value) == "Response must contain finite JSON values and valid Unicode."


def test_recursive_data_fails_but_reused_nonrecursive_values_survive():
    repeated = ["same"]
    assert budget.serialize([repeated, repeated]) == '[["same"],["same"]]'
    recursive = []
    recursive.append(recursive)
    with pytest.raises(budget.SerializationError):
        budget.serialize(recursive)


def test_unsupported_objects_are_not_stringified():
    class MustNotRender:
        def __str__(self):
            raise AssertionError("arbitrary __str__ was called")

        def __repr__(self):
            raise AssertionError("arbitrary __repr__ was called")

    with pytest.raises(budget.SerializationError):
        budget.serialize({"data": MustNotRender()})


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", 0),
        ("hello world", 2),
        ("こんにちは世界 🌍", 4),
        ("<|endoftext|><|endofprompt|>", 13),
        ("antidisestablishmentarianism", 6),
    ],
)
def test_frozen_reference_golden_counts(text, expected):
    # Captured independently with upstream 0.13.0's o200k_base configuration.
    assert budget.count_tokens(text) == expected


def test_the_token_limit_is_exact_not_a_character_estimate():
    configured = budget.Budget(512)
    exact = " x" * 512
    assert budget.count_tokens(exact) == 512
    assert configured.fits_text(exact)
    over = exact + " x"
    assert len(over.encode()) < configured.byte_limit
    assert not configured.fits_text(over)


def test_the_byte_limit_is_independent_and_counts_utf8():
    configured = budget.Budget(512)
    assert configured.fits_text(" " * 4096)
    over = " " * 4095 + "é"
    assert len(over) == 4096 and len(over.encode()) == 4097
    assert budget.count_tokens(over) < 512
    assert not configured.fits_text(over)


def test_fits_counts_the_complete_serialized_envelope():
    configured = budget.Budget(512)
    data = {"text": " x" * 500}
    assert configured.fits(data)
    envelope = {"data": data, "completeness": {"state": "partial"}, "next_cursor": "cursor " * 30}
    assert not configured.fits(envelope)


@pytest.mark.parametrize("text", [b"not text", None, "\ud800"])
def test_text_counters_reject_invalid_input(text):
    with pytest.raises(budget.SerializationError):
        budget.count_tokens(text)
    with pytest.raises(budget.SerializationError):
        budget.Budget().fits_text(text)


@pytest.mark.parametrize("broken", ["config", "vocabulary", "missing"])
def test_missing_or_corrupt_assets_raise_a_bounded_error(tmp_path, monkeypatch, broken):
    assets = tmp_path / "_tokenizer"
    assets.mkdir()
    real_assets = Path(budget.__file__).parent / "_tokenizer"
    (assets / "o200k_base.json").write_bytes(
        b"corrupt" if broken == "config" else (real_assets / "o200k_base.json").read_bytes()
    )
    if broken != "missing":
        (assets / "o200k_base.tiktoken").write_bytes(b"corrupt")
    monkeypatch.setattr(budget, "_encoding", None)
    monkeypatch.setattr(budget.resources, "files", lambda _: tmp_path)
    with pytest.raises(budget.TokenizerUnavailable) as caught:
        budget.count_tokens("hello world")
    assert str(caught.value) == "MCP tokenizer unavailable; verify packaged assets."
    assert budget._encoding is None


def test_missing_native_dependency_has_no_estimator_fallback(monkeypatch):
    original = builtins.__import__

    def without_tiktoken(name, *args, **kwargs):
        if name == "tiktoken":
            raise ModuleNotFoundError("unavailable")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(budget, "_encoding", None)
    monkeypatch.setattr(builtins, "__import__", without_tiktoken)
    with pytest.raises(budget.TokenizerUnavailable):
        budget.count_tokens("hello world")


def test_concurrent_first_calls_construct_only_one_encoding(monkeypatch):
    original_load = budget._load_encoding
    loads = []
    start = threading.Barrier(8)

    def counted_load():
        loads.append(True)
        return original_load()

    def count(_):
        start.wait(timeout=5)
        return budget.count_tokens("hello world")

    monkeypatch.setattr(budget, "_encoding", None)
    monkeypatch.setattr(budget, "_load_encoding", counted_load)
    with ThreadPoolExecutor(max_workers=8) as pool:
        assert list(pool.map(count, range(8))) == [2] * 8
    assert len(loads) == 1


def test_budget_module_and_sdk_import_without_site_packages_or_tokenizer(tmp_path):
    src = Path(__file__).resolve().parents[1] / "src"
    code = """
import importlib.util, sys
from pathlib import Path
import probe
import probe.sdk
# The existing probe.mcp package imports the service (and Pydantic). Load only
# the new module to prove it adds no dependency to lightweight CLI/SDK imports.
spec = importlib.util.spec_from_file_location('budget_under_test', Path(probe.__file__).parent / 'mcp' / 'budget.py')
budget = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = budget
spec.loader.exec_module(budget)
assert 'tiktoken' not in sys.modules
assert budget._encoding is None
assert budget.Budget().byte_limit == 16000
assert budget.serialize({'ok': True}) == '{"ok":true}'
"""
    result = subprocess.run(
        [sys.executable, "-S", "-c", code],
        cwd=tmp_path,
        env={"PATH": os.defpath, "PYTHONPATH": str(src), "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
