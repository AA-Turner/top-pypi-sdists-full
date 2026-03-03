"""Tests for typed durable APIs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

import pytest
from pydantic import BaseModel, Field

from plato.worlds.durable import (
    DependencyMissing,
    DurableFile,
    DurableOutputs,
    DurablePath,
    FromArg,
    Requires,
    durable,
    load_durable_path,
)


class Inner(BaseModel):
    value: int
    name: str


class SimpleOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    results: Inner = Field(json_schema_extra={"json": "results.json"})


class FileOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    results: Inner = Field(json_schema_extra={"json": "results.json"})
    image: DurableFile = Field(json_schema_extra={"file": "output.png"})


class GlobOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}"
    results: Inner = Field(json_schema_extra={"json": "results.json"})
    steps: list[DurableFile] = Field(json_schema_extra={"glob": "step_*/annotated.png"})


class UpstreamOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/upstream"
    data: Inner = Field(json_schema_extra={"json": "data.json"})


class DownstreamOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/downstream"
    results: Inner = Field(json_schema_extra={"json": "results.json"})


class OtherOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/other"
    value: int = Field(json_schema_extra={"json": "value.json"})


class IterOutputs(DurableOutputs):
    DURABLE_PATH_TEMPLATE: ClassVar[str] = "{d}/iter_{step}"
    data: Inner = Field(json_schema_extra={"json": "data.json"})


class Cfg:
    def __init__(self, recordings: Path):
        self.recordings = recordings


def _write_upstream(path: Path, value: int = 10, name: str = "upstream") -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "data.json").write_text(json.dumps({"value": value, "name": name}))


class TestDurablePath:
    def test_extracts_template_roots(self) -> None:
        path = DurablePath(SimpleOutputs, "{config.recordings}/{session_id}/iter_{step_number}")
        assert set(path.required_vars) == {"config", "session_id", "step_number"}

    def test_resolve_missing_vars_raises(self, tmp_path: Path) -> None:
        path = DurablePath(SimpleOutputs, "{d}/{name}")
        with pytest.raises(TypeError, match="Missing durable path vars"):
            path.resolve(d=tmp_path)

    def test_load_helper(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 1, "name": "cached"}))
        out = load_durable_path(SimpleOutputs.durable_path(), d=tmp_path)
        assert out is not None
        assert out.results.value == 1


class TestCachedSync:
    def test_miss_runs_and_saves(self, tmp_path: Path) -> None:
        call_count = 0

        @durable(d=FromArg("d"))
        def process(d: Path) -> SimpleOutputs:
            nonlocal call_count
            call_count += 1
            return SimpleOutputs(results=Inner(value=42, name="test"))

        result = process(d=tmp_path)
        assert call_count == 1
        assert result.results.value == 42
        assert (tmp_path / "results.json").exists()

    def test_hit_loads_from_disk(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 99, "name": "cached"}))

        @durable(d=FromArg("d"))
        def process(d: Path) -> SimpleOutputs:
            raise AssertionError("should not be called")

        result = process(d=tmp_path)
        assert result.results.value == 99
        assert result.results.name == "cached"

    def test_validate_forces_rerun(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 0, "name": "stale"}))
        run_count = 0

        @durable(d=FromArg("d"), validate=lambda d: False)
        def process(d: Path) -> SimpleOutputs:
            nonlocal run_count
            run_count += 1
            return SimpleOutputs(results=Inner(value=run_count, name="fresh"))

        first = process(d=tmp_path)
        second = process(d=tmp_path)
        assert run_count == 2
        assert first.results.value == 1
        assert second.results.value == 2

    def test_file_field_must_exist(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 1, "name": "x"}))
        call_count = 0

        @durable(d=FromArg("d"))
        def process(d: Path) -> FileOutputs:
            nonlocal call_count
            call_count += 1
            (d / "output.png").write_bytes(b"PNG")
            return FileOutputs(results=Inner(value=1, name="x"), image=DurableFile(path=d / "output.png"))

        result = process(d=tmp_path)
        assert call_count == 1
        assert result.image.exists()

    def test_glob_field_cache_hit(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 1, "name": "x"}))
        for i in range(3):
            step_dir = tmp_path / f"step_{i}"
            step_dir.mkdir()
            (step_dir / "annotated.png").write_bytes(b"PNG")

        @durable(d=FromArg("d"))
        def process(d: Path) -> GlobOutputs:
            raise AssertionError("should not be called")

        result = process(d=tmp_path)
        assert len(result.steps) == 3


class TestCachedAsync:
    @pytest.mark.asyncio
    async def test_async_cache_hit(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 99, "name": "cached"}))

        @durable(d=FromArg("d"))
        async def process(d: Path) -> SimpleOutputs:
            raise AssertionError("should not be called")

        result = await process(d=tmp_path)
        assert result.results.value == 99

    @pytest.mark.asyncio
    async def test_async_validate_forces_rerun(self, tmp_path: Path) -> None:
        (tmp_path / "results.json").write_text(json.dumps({"value": 0, "name": "stale"}))
        run_count = 0

        @durable(d=FromArg("d"), validate=lambda d: False)
        async def process(d: Path) -> SimpleOutputs:
            nonlocal run_count
            run_count += 1
            return SimpleOutputs(results=Inner(value=run_count, name="fresh"))

        await process(d=tmp_path)
        await process(d=tmp_path)
        assert run_count == 2


class TestRequires:
    def test_dependency_injected_on_miss(self, tmp_path: Path) -> None:
        _write_upstream(tmp_path / "upstream")

        @durable(d=FromArg("d"))
        def process(
            d: Path,
            dep: UpstreamOutputs = Requires(d=FromArg("d")),
        ) -> DownstreamOutputs:
            return DownstreamOutputs(results=Inner(value=dep.data.value + 1, name="derived"))

        result = process(d=tmp_path)
        assert result.results.value == 11

    def test_dependency_missing_raises(self, tmp_path: Path) -> None:
        @durable(d=FromArg("d"))
        def process(
            d: Path,
            dep: UpstreamOutputs = Requires(d=FromArg("d")),
        ) -> DownstreamOutputs:
            raise AssertionError("should not be called")

        with pytest.raises(DependencyMissing):
            process(d=tmp_path)

    def test_optional_dependency_none_when_missing(self, tmp_path: Path) -> None:
        @durable(d=FromArg("d"))
        def process(
            d: Path,
            dep: UpstreamOutputs | None = Requires(optional=True, d=FromArg("d")),
        ) -> DownstreamOutputs:
            assert dep is None
            return DownstreamOutputs(results=Inner(value=0, name="no_dep"))

        result = process(d=tmp_path)
        assert result.results.value == 0

    def test_cache_hit_skips_dep_resolution(self, tmp_path: Path) -> None:
        downstream_dir = tmp_path / "downstream"
        downstream_dir.mkdir(parents=True, exist_ok=True)
        (downstream_dir / "results.json").write_text(json.dumps({"value": 99, "name": "cached"}))

        @durable(d=FromArg("d"))
        def process(
            d: Path,
            dep: UpstreamOutputs = Requires(d=FromArg("d")),
        ) -> DownstreamOutputs:
            raise AssertionError("should not be called")

        result = process(d=tmp_path)
        assert result.results.value == 99

    def test_fromarg_dotted_access(self, tmp_path: Path) -> None:
        _write_upstream(tmp_path / "upstream", value=7)

        @durable(d=FromArg("d"))
        def process(
            cfg: Cfg,
            d: Path,
            dep: UpstreamOutputs = Requires(d=FromArg("cfg.recordings")),
        ) -> DownstreamOutputs:
            return DownstreamOutputs(results=Inner(value=dep.data.value, name="ok"))

        result = process(cfg=Cfg(tmp_path), d=tmp_path)
        assert result.results.value == 7

    def test_fromarg_expression(self, tmp_path: Path) -> None:
        _write_upstream(tmp_path / "iter_2", value=7)

        @durable(d=FromArg("d"), step=FromArg("step_number"))
        def process(
            d: Path,
            step_number: int,
            dep: IterOutputs = Requires(d=FromArg("d"), step=FromArg("step_number - 1")),
        ) -> IterOutputs:
            return IterOutputs(data=Inner(value=dep.data.value + 1, name="expr_ok"))

        result = process(d=tmp_path, step_number=3)
        assert result.data.value == 8


class TestTypeErrors:
    def test_durable_requires_explicit_bindings(self) -> None:
        with pytest.raises(TypeError, match="missing bindings"):

            @durable
            def process(d: Path) -> SimpleOutputs:
                return SimpleOutputs(results=Inner(value=1, name="x"))

    def test_requires_rejects_unknown_binding_key(self) -> None:
        with pytest.raises(TypeError, match="unknown vars"):

            @durable(d=FromArg("d"))
            def process(d: Path, dep: UpstreamOutputs = Requires(bad=FromArg("d"))) -> DownstreamOutputs:
                return DownstreamOutputs(results=Inner(value=1, name="x"))

    def test_requires_rejects_non_basemodel_dep_type(self) -> None:
        with pytest.raises(TypeError, match="not a BaseModel"):

            @durable(d=FromArg("d"))
            def process(d: Path, dep: dict = Requires(d=FromArg("d"))) -> DownstreamOutputs:
                return DownstreamOutputs(results=Inner(value=1, name="x"))

    def test_requires_rejects_untyped_dep(self) -> None:
        with pytest.raises(TypeError, match="no type annotation"):

            @durable(d=FromArg("d"))
            def process(d: Path, dep=Requires(d=FromArg("d"))) -> DownstreamOutputs:
                return DownstreamOutputs(results=Inner(value=1, name="x"))

    def test_durable_rejects_non_basemodel_return(self) -> None:
        with pytest.raises(TypeError):

            @durable(d=FromArg("d"))
            def process(d: Path) -> dict:
                return {}

    def test_durable_rejects_explicit_path_argument(self) -> None:
        with pytest.raises(TypeError, match="does not accept a path"):

            @durable(OtherOutputs.durable_path())
            def process(d: Path) -> SimpleOutputs:
                return SimpleOutputs(results=Inner(value=1, name="x"))

    def test_fromarg_expression_rejects_calls(self, tmp_path: Path) -> None:
        @durable(d=FromArg("d"))
        def process(
            d: Path,
            dep: UpstreamOutputs = Requires(d=FromArg("str(d)")),
        ) -> DownstreamOutputs:
            return DownstreamOutputs(results=Inner(value=1, name="x"))

        with pytest.raises(TypeError, match="do not allow function calls"):
            process(d=tmp_path)
