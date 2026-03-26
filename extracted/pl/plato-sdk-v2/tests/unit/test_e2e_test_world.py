"""Unit tests for the e2e test runner (plato.worlds.testing)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from plato.worlds.testing import _import_file, run_e2e_tests


class _FakeConfig:
    def __init__(self, test_dir: str, test_filter: str = ""):
        self.e2e_test_dir = test_dir
        self.e2e_test_filter = test_filter


class _FakeWorld:
    def __init__(self, test_dir: str, test_filter: str = ""):
        self.config = _FakeConfig(test_dir, test_filter)
        self.logger = MagicMock()


class _FakeTracer:
    """Minimal tracer stub that produces no-op spans."""

    def start_as_current_span(self, name: str):
        return _FakeSpan()


class _FakeSpan:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def set_status(self, *args):
        pass

    def record_exception(self, *args):
        pass


@pytest.fixture
def test_dir(tmp_path: Path) -> Path:
    d = tmp_path / "tests"
    d.mkdir()
    return d


class TestImportFile:
    def test_imports_valid_module(self, test_dir: Path) -> None:
        (test_dir / "test_sample.py").write_text("def test_a(world): pass\n")
        module = _import_file(test_dir / "test_sample.py")
        assert module is not None
        assert hasattr(module, "test_a")

    def test_returns_none_for_syntax_error(self, test_dir: Path) -> None:
        (test_dir / "test_bad.py").write_text("def test_a(world\n")
        assert _import_file(test_dir / "test_bad.py") is None

    def test_returns_none_for_missing_file(self, tmp_path: Path) -> None:
        assert _import_file(tmp_path / "nonexistent.py") is None


class TestRunE2ETests:
    @pytest.mark.asyncio
    async def test_runs_passing_tests(self, test_dir: Path) -> None:
        (test_dir / "test_ok.py").write_text(
            "def test_one(world): assert True\ndef test_two(world): assert 1 + 1 == 2\n"
        )
        world = _FakeWorld(str(test_dir))
        await run_e2e_tests(world, _FakeTracer())  # no error = all passed

    @pytest.mark.asyncio
    async def test_async_tests_work(self, test_dir: Path) -> None:
        (test_dir / "test_async.py").write_text("import asyncio\nasync def test_await(world): await asyncio.sleep(0)\n")
        world = _FakeWorld(str(test_dir))
        await run_e2e_tests(world, _FakeTracer())

    @pytest.mark.asyncio
    async def test_failing_test_raises(self, test_dir: Path) -> None:
        (test_dir / "test_fail.py").write_text("def test_bad(world): assert False\n")
        world = _FakeWorld(str(test_dir))
        with pytest.raises(RuntimeError, match="1 failed"):
            await run_e2e_tests(world, _FakeTracer())

    @pytest.mark.asyncio
    async def test_import_error_counted(self, test_dir: Path) -> None:
        (test_dir / "test_broken.py").write_text("import nonexistent_xyz\n")
        world = _FakeWorld(str(test_dir))
        with pytest.raises(RuntimeError, match="1 errors"):
            await run_e2e_tests(world, _FakeTracer())

    @pytest.mark.asyncio
    async def test_no_test_dir_raises(self) -> None:
        world = _FakeWorld("/nonexistent")
        with pytest.raises(RuntimeError, match="not found"):
            await run_e2e_tests(world, _FakeTracer())

    @pytest.mark.asyncio
    async def test_empty_dir_raises(self, test_dir: Path) -> None:
        world = _FakeWorld(str(test_dir))
        with pytest.raises(RuntimeError, match="No test_"):
            await run_e2e_tests(world, _FakeTracer())

    @pytest.mark.asyncio
    async def test_filter_selects_tests(self, test_dir: Path) -> None:
        (test_dir / "test_mixed.py").write_text("def test_alpha(world): pass\ndef test_beta(world): assert False\n")
        world = _FakeWorld(str(test_dir), test_filter="alpha")
        await run_e2e_tests(world, _FakeTracer())  # beta filtered out, no error

    @pytest.mark.asyncio
    async def test_non_test_functions_ignored(self, test_dir: Path) -> None:
        (test_dir / "test_helpers.py").write_text("def helper(world): assert False\ndef test_real(world): pass\n")
        world = _FakeWorld(str(test_dir))
        await run_e2e_tests(world, _FakeTracer())
