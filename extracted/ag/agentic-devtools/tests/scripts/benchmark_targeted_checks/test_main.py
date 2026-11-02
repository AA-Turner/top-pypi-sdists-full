"""Tests for the targeted-check benchmark script wrapper."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch


def test_script_exposes_benchmark_entrypoint():
    script = Path(__file__).resolve().parents[3] / "scripts" / "benchmark_targeted_checks.py"
    spec = importlib.util.spec_from_file_location("benchmark_targeted_checks_script", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    with patch("agentic_devtools.cli.checks.benchmark.main", return_value=0) as mock_main:
        with patch("sys.path", ["sentinel"]):
            spec.loader.exec_module(module)
            assert sys.path[0] == str(script.parents[1])
            assert module.main() == 0
    mock_main.assert_called_once()
