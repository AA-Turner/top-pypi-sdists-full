# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Per-job ``num_cpus``/``num_gpus``/``memory`` overrides on ``backfill()``.

An override must reach both the actor's Ray reservation and the admission
check, and must leave the UDF, its checkpoint identity, and callers that
omit it unchanged.
"""

import contextlib
import inspect
import json
import logging
import math
from unittest.mock import MagicMock, patch

import pyarrow as pa
import pytest

import geneva
from geneva.apply.task import BackfillUDFTask
from geneva.runners.ray.admission import calculate_job_resources
from geneva.runners.ray.memory_budget import resolve_default_actor_memory
from geneva.transformer import UDF

_GIB = 1 << 30


@geneva.udf(data_type=pa.int64(), num_cpus=1.0, memory=2 * _GIB)
def _plus_one(a: int) -> int:
    return a + 1


@geneva.udf(data_type=pa.int64(), num_cpus=2.0, num_gpus=1.0, memory=4 * _GIB)
def _gpu_plus_one(a: int) -> int:
    return a + 1


def _task(udf: UDF = _plus_one, **overrides) -> BackfillUDFTask:  # noqa: ANN003
    return BackfillUDFTask(udfs={"b": udf}, **overrides)


class _StopError(Exception):
    """Raised by dispatch spies so the test never reaches Ray."""


class TestTaskOverrides:
    """``setup_actor`` reads the task, so the override has to land there."""

    def test_declaration_is_used_when_nothing_is_overridden(self) -> None:
        task = _task(_gpu_plus_one)
        assert task.num_cpus() == 2.0
        assert task.num_gpus() == 1.0
        assert task.memory() == 4 * _GIB
        assert task.is_cuda()

    def test_each_override_replaces_only_its_field(self) -> None:
        task = _task(_gpu_plus_one, override_num_cpus=4.0)
        assert (task.num_cpus(), task.num_gpus(), task.memory()) == (4.0, 1.0, 4 * _GIB)

        task = _task(_gpu_plus_one, override_num_gpus=0.25)
        assert (task.num_cpus(), task.num_gpus(), task.memory()) == (
            2.0,
            0.25,
            4 * _GIB,
        )

        task = _task(_gpu_plus_one, override_memory=8 * _GIB)
        assert (task.num_cpus(), task.num_gpus(), task.memory()) == (2.0, 1.0, 8 * _GIB)

    def test_zero_gpus_overrides_a_gpu_udf(self) -> None:
        task = _task(_gpu_plus_one, override_num_gpus=0.0)
        assert task.num_gpus() == 0.0
        assert not task.is_cuda()

    def test_an_override_counts_as_a_declaration(self) -> None:
        """So it displaces the floor an unset UDF would otherwise reserve."""
        undeclared = UDF(func=lambda a: a, name="b", data_type=pa.int64())
        assert undeclared.memory is None

        floor = resolve_default_actor_memory()
        assert _task(undeclared).resolve_memory(floor) == floor
        assert _task(undeclared, override_memory=3 * _GIB).resolve_memory(floor) == (
            3 * _GIB
        )

    def test_zero_memory_asks_for_unreserved_scheduling(self) -> None:
        """``memory=0`` is a request, not an absent value -- as on ``@udf``."""
        task = _task(override_memory=0)
        assert task.memory() == 0
        assert task.resolve_memory(resolve_default_actor_memory()) == 0


class TestCheckpointIdentity:
    """Resources are scheduling bookkeeping; they must not fork checkpoints."""

    _KEY = {
        "dataset_uri": "s3://bucket/videos",
        "start": 0,
        "end": 64,
        "frag_id": 3,
        "where": "duration_us < 120000000",
        "src_files_hash": "abc123",
    }

    def test_overrides_leave_checkpoint_keys_unchanged(self) -> None:
        plain = _task(_gpu_plus_one)
        tuned = _task(
            _gpu_plus_one,
            override_num_cpus=8.0,
            override_num_gpus=0.25,
            override_memory=12 * _GIB,
        )
        assert plain.checkpoint_key(**self._KEY) == tuned.checkpoint_key(**self._KEY)
        prefix_args = {
            k: v for k, v in self._KEY.items() if k not in ("start", "end", "frag_id")
        }
        assert plain.checkpoint_prefix(**prefix_args) == tuned.checkpoint_prefix(
            **prefix_args
        )

    def test_a_version_change_still_forks_them(self) -> None:
        """Contrast: processing-logic identity does move the key."""
        reversioned = UDF(
            func=_gpu_plus_one.func,
            name=_gpu_plus_one.name,
            data_type=pa.int64(),
            version="v2",
        )
        assert _task(_gpu_plus_one).checkpoint_key(**self._KEY) != _task(
            reversioned
        ).checkpoint_key(**self._KEY)


def _udf_stub(*, num_cpus: float, num_gpus: float | None, memory: int | None) -> UDF:
    udf = MagicMock(spec=UDF)
    udf.num_cpus = num_cpus
    udf.num_gpus = num_gpus
    udf.memory = memory
    udf.has_preprocess.return_value = False
    return udf


class TestAdmissionPricesTheOverride:
    """Admission and the actor have to name the same number."""

    def test_all_three_overrides_are_priced(self) -> None:
        priced = calculate_job_resources(
            _udf_stub(num_cpus=1.0, num_gpus=None, memory=2 * _GIB),
            concurrency=4,
            num_cpus_override=4.0,
            num_gpus_override=0.5,
            memory_override=8 * _GIB,
        )
        assert priced.udf_cpus == 4.0
        assert priced.applier_cpus == 16.0
        assert priced.udf_gpus == 0.5
        assert priced.applier_gpus == 2.0
        assert priced.udf_memory == 8 * _GIB
        assert priced.applier_memory == 4 * 8 * _GIB

    def test_zero_gpus_unprices_a_gpu_udf(self) -> None:
        udf = _udf_stub(num_cpus=2.0, num_gpus=1.0, memory=4 * _GIB)
        assert calculate_job_resources(udf, concurrency=2).applier_gpus == 2.0
        assert (
            calculate_job_resources(
                udf, concurrency=2, num_gpus_override=0.0
            ).applier_gpus
            == 0.0
        )

    def test_a_memory_override_displaces_the_floor(self) -> None:
        udf = _udf_stub(num_cpus=1.0, num_gpus=None, memory=None)
        floor = resolve_default_actor_memory()
        assert (
            calculate_job_resources(
                udf, concurrency=1, default_memory_bytes=floor
            ).udf_memory
            == floor
        )
        assert (
            calculate_job_resources(
                udf, concurrency=1, default_memory_bytes=floor, memory_override=0
            ).udf_memory
            == 0
        )

    def test_intra_applier_concurrency_still_scales_the_override(self) -> None:
        priced = calculate_job_resources(
            _udf_stub(num_cpus=1.0, num_gpus=None, memory=None),
            concurrency=2,
            intra_applier_concurrency=3,
            num_cpus_override=2.0,
            memory_override=_GIB,
        )
        assert priced.udf_cpus == 6.0
        assert priced.udf_memory == 3 * _GIB


def _sparse_options(udf: UDF, **overrides) -> dict:  # noqa: ANN003
    """What the sparse actor factory hands Ray for ``udf``."""
    from geneva.runners.ray import sparse_pipeline as sparse_mod

    with patch.object(sparse_mod, "cpu_only_pool_resources", lambda: {"cpu-only": 1}):
        return sparse_mod._sparse_actor_options(udf, **overrides)


class TestSparseActorOptions:
    """Override, else declaration; no multipliers, no floor."""

    def test_declaration_is_used_when_nothing_is_overridden(self) -> None:
        assert _sparse_options(_gpu_plus_one) == {
            "num_cpus": 2.0,
            "num_gpus": 1.0,
            "memory": 4 * _GIB,
        }

    def test_each_override_replaces_only_its_field(self) -> None:
        base = {"num_cpus": 2.0, "num_gpus": 1.0, "memory": 4 * _GIB}
        assert _sparse_options(_gpu_plus_one, num_cpus=0.5) == {
            **base,
            "num_cpus": 0.5,
        }
        assert _sparse_options(_gpu_plus_one, num_gpus=0.25) == {
            **base,
            "num_gpus": 0.25,
        }
        assert _sparse_options(_gpu_plus_one, memory=_GIB) == {**base, "memory": _GIB}

    def test_a_fractional_declaration_is_reserved_as_declared(self) -> None:
        quarter = geneva.udf(data_type=pa.int64(), num_cpus=0.25)(lambda a: a)
        assert _sparse_options(quarter) == {"num_cpus": 0.25}

    def test_a_fractional_override_is_reserved_as_given(self) -> None:
        assert _sparse_options(_gpu_plus_one, num_cpus=0.5)["num_cpus"] == 0.5

    def test_a_zero_or_missing_cpu_declaration_reserves_one(self) -> None:
        for declared in (0.0, None):
            stub = _udf_stub(num_cpus=declared, num_gpus=None, memory=None)  # type: ignore[arg-type]
            assert _sparse_options(stub) == {"num_cpus": 1.0}

    def test_zero_gpus_drops_the_gpu_request(self) -> None:
        assert "num_gpus" not in _sparse_options(_gpu_plus_one, num_gpus=0)

    def test_zero_gpus_reaches_the_cpu_only_pool(self) -> None:
        options = _sparse_options(_gpu_plus_one, num_gpus=0, use_cpu_only_pool=True)
        assert options["resources"] == {"cpu-only": 1}
        assert "num_gpus" not in options

    def test_a_gpu_request_wins_over_the_cpu_only_pool(self, caplog) -> None:  # noqa: ANN001
        with caplog.at_level(
            logging.WARNING, logger="geneva.runners.ray.sparse_pipeline"
        ):
            options = _sparse_options(_gpu_plus_one, use_cpu_only_pool=True)
        assert options["num_gpus"] == 1.0
        assert "resources" not in options
        assert "use_cpu_only_pool=True is ignored" in caplog.text

    def test_fractional_gpus_need_no_hardware_to_be_requested(self) -> None:
        assert _sparse_options(_plus_one, num_gpus=0.5)["num_gpus"] == 0.5

    def test_zero_memory_asks_for_unreserved_scheduling(self) -> None:
        assert _sparse_options(_gpu_plus_one, memory=0)["memory"] == 0

    def test_undeclared_memory_reserves_nothing(self) -> None:
        stub = _udf_stub(num_cpus=1.0, num_gpus=0.0, memory=None)
        assert "memory" not in _sparse_options(stub)

    def test_the_udf_is_never_mutated(self) -> None:
        before = (_gpu_plus_one.num_cpus, _gpu_plus_one.num_gpus, _gpu_plus_one.memory)
        _sparse_options(_gpu_plus_one, num_cpus=8, num_gpus=0, memory=0)
        assert (
            _gpu_plus_one.num_cpus,
            _gpu_plus_one.num_gpus,
            _gpu_plus_one.memory,
        ) == before


class TestSparseAdmission:
    """Admission prices what a sparse actor reserves, and nothing it does not."""

    def test_sparse_jobs_carry_no_fragment_writer_overhead(self) -> None:
        from geneva.runners.ray.admission import _get_resource_config

        rc = _get_resource_config()
        udf = _udf_stub(num_cpus=2.0, num_gpus=0.0, memory=_GIB)
        sparse = calculate_job_resources(
            udf, concurrency=4, fragment_writers=False, num_cpus_override=0.5
        )
        ordinary = calculate_job_resources(udf, concurrency=4, num_cpus_override=0.5)

        assert sparse.udf_cpus == 0.5
        assert sparse.applier_cpus == 2.0
        assert sparse.applier_memory == 4 * _GIB
        assert sparse.overhead_cpus == rc.jobtracker_num_cpus
        assert sparse.overhead_memory == rc.jobtracker_memory
        assert ordinary.overhead_cpus == (
            rc.jobtracker_num_cpus + 4 * rc.fragment_writer_num_cpus
        )
        assert ordinary.overhead_memory == (
            rc.jobtracker_memory + 4 * rc.fragment_writer_memory
        )

    @pytest.mark.parametrize(
        ("udf", "overrides"),
        [
            pytest.param(
                _udf_stub(num_cpus=0.0, num_gpus=None, memory=None), {}, id="zero-cpu"
            ),
            pytest.param(
                _udf_stub(num_cpus=0.25, num_gpus=0.0, memory=None),
                {},
                id="fractional-declaration",
            ),
            pytest.param(_gpu_plus_one, {"num_cpus": 0.5}, id="fractional-override"),
            pytest.param(_gpu_plus_one, {"num_gpus": 0}, id="gpu-to-zero"),
            pytest.param(_plus_one, {"memory": 0}, id="memory-to-zero"),
            pytest.param(
                _udf_stub(num_cpus=1.0, num_gpus=0.0, memory=None),
                {"num_gpus": 0.5, "memory": _GIB},
                id="gpu-and-memory-override",
            ),
        ],
    )
    def test_actor_options_admission_and_metadata_agree(
        self,
        udf: UDF,
        overrides: dict,
    ) -> None:
        """The three places that name a sparse reservation name one number."""
        from geneva.table import _backfill_resource_metadata

        options = _sparse_options(udf, **overrides)
        priced = calculate_job_resources(
            udf,
            concurrency=1,
            intra_applier_concurrency=1,
            enable_gpu_pipelining=False,
            default_memory_bytes=0,
            fragment_writers=False,
            num_cpus_override=overrides.get("num_cpus"),
            num_gpus_override=overrides.get("num_gpus"),
            memory_override=overrides.get("memory"),
        )
        metadata = _backfill_resource_metadata(
            udf,
            num_cpus=overrides.get("num_cpus"),
            num_gpus=overrides.get("num_gpus"),
            memory=overrides.get("memory"),
            default_memory_bytes=0,
            cpu_thread_count=1,
            intra_applier_concurrency=1,
            include_multipliers=False,
        )

        # An absent option is an unreserved resource.
        actor = (
            options["num_cpus"],
            options.get("num_gpus", 0.0),
            options.get("memory", 0),
        )
        assert actor == (priced.udf_cpus, priced.udf_gpus, priced.udf_memory)
        expected = metadata["expected_actor_reservation"]
        assert actor == (
            expected["num_cpus"],
            expected["num_gpus"],
            expected["memory"],
        )


def _actor_options(task: BackfillUDFTask, **job_kwargs) -> dict:  # noqa: ANN003
    """What ``setup_actor`` hands Ray for ``task`` -- the end of the line."""
    from geneva.jobs.config import JobConfig
    from geneva.runners.ray import pipeline as pipeline_mod

    job = pipeline_mod.ColumnAddPipelineJob(
        map_task=task,
        checkpoint_store=MagicMock(),
        error_store=MagicMock(),
        config=JobConfig.get(),
        dst=MagicMock(),
        input_plan=iter([]),
        job_id="job",
        **job_kwargs,
    )

    captured: dict = {}

    class _FakeActor:
        @staticmethod
        def options(**kwargs):  # noqa: ANN003, ANN205
            captured.update(kwargs)
            return _FakeActor

    with (
        patch.object(pipeline_mod, "ApplierActor", _FakeActor),
        patch.object(pipeline_mod, "cpu_only_pool_resources", lambda: {"cpu-only": 1}),
    ):
        job.setup_actor()
    return captured


class TestActorReservation:
    def test_omitting_overrides_reserves_the_declaration(self) -> None:
        declared = _actor_options(_task(_gpu_plus_one))
        assert declared["num_cpus"] == 2.0
        assert declared["num_gpus"] == 1.0
        assert declared["memory"] == 4 * _GIB

    def test_overrides_reach_ray_with_the_scheduling_multipliers(self) -> None:
        options = _actor_options(
            _task(
                override_num_cpus=0.5, override_num_gpus=0.25, override_memory=2 * _GIB
            ),
            intra_applier_concurrency=3,
        )
        assert options["num_cpus"] == 1.5
        assert options["num_gpus"] == 0.25
        assert options["memory"] == 6 * _GIB

    def test_a_zero_memory_override_reserves_nothing(self) -> None:
        assert _actor_options(_task(override_memory=0))["memory"] == 0

    def test_zero_gpus_reaches_the_cpu_only_pool(self, caplog) -> None:  # noqa: ANN001
        """A GPU UDF pinned to CPU nodes by the override alone."""
        with caplog.at_level(logging.WARNING):
            options = _actor_options(
                _task(_gpu_plus_one, override_num_gpus=0), use_cpu_only_pool=True
            )
        assert "num_gpus" not in options
        assert options["resources"] == {"cpu-only": 1}
        assert "use_cpu_only_pool=True is ignored" not in caplog.text

    def test_admission_matches_the_actor(self) -> None:
        """The two paths resolve the same overrides through different code."""
        overrides = {"num_cpus": 0.5, "num_gpus": 0.25, "memory": 2 * _GIB}
        options = _actor_options(
            _task(
                _gpu_plus_one,
                override_num_cpus=overrides["num_cpus"],
                override_num_gpus=overrides["num_gpus"],
                override_memory=overrides["memory"],
            ),
            intra_applier_concurrency=3,
        )
        priced = calculate_job_resources(
            _gpu_plus_one,
            concurrency=1,
            intra_applier_concurrency=3,
            num_cpus_override=overrides["num_cpus"],
            num_gpus_override=overrides["num_gpus"],
            memory_override=overrides["memory"],
        )
        assert (options["num_cpus"], options["num_gpus"], options["memory"]) == (
            priced.udf_cpus,
            priced.udf_gpus,
            priced.udf_memory,
        )


@contextlib.contextmanager
def _spied_dispatch():  # noqa: ANN202
    """Stub admission and dispatch; yield what each received."""
    import geneva.runners.ray.admission as admission_mod
    import geneva.runners.ray.pipeline as pipeline_mod

    seen: dict = {"admission": None, "dispatch": None}

    def _spy_admission(_udf, **kwargs) -> None:  # noqa: ANN001, ANN003
        seen["admission"] = kwargs

    def _spy_dispatch(*_args, **kwargs):  # noqa: ANN002, ANN003, ANN202
        seen["dispatch"] = kwargs
        raise _StopError

    with (
        patch.object(admission_mod, "validate_admission", _spy_admission),
        patch.object(pipeline_mod, "dispatch_run_ray_add_column", _spy_dispatch),
        contextlib.suppress(_StopError),
    ):
        yield seen


class TestBackfillApi:
    """What ``backfill()`` accepts, and what it forwards."""

    @pytest.fixture
    def tbl(self, tmp_path):  # noqa: ANN001, ANN201
        db = geneva.connect(str(tmp_path))
        t = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
        t.add_columns({"b": _plus_one, "c": _gpu_plus_one})
        return t

    def test_admission_and_dispatch_see_every_override(self, tbl) -> None:  # noqa: ANN001
        with _spied_dispatch() as seen:
            tbl.backfill_async("b", num_cpus=4, num_gpus=0.5, memory=8 * _GIB)

        assert seen["admission"]["num_cpus_override"] == 4.0
        assert seen["admission"]["num_gpus_override"] == 0.5
        assert seen["admission"]["memory_override"] == 8 * _GIB
        assert seen["dispatch"]["num_cpus"] == 4.0
        assert seen["dispatch"]["num_gpus"] == 0.5
        assert seen["dispatch"]["memory"] == 8 * _GIB

    def test_omitting_them_changes_nothing(self, tbl) -> None:  # noqa: ANN001
        with _spied_dispatch() as seen:
            tbl.backfill_async("b")

        assert seen["dispatch"]["num_cpus"] is None
        assert seen["dispatch"]["num_gpus"] is None
        assert seen["dispatch"]["memory"] is None
        assert seen["admission"]["num_cpus_override"] is None
        assert seen["admission"]["num_gpus_override"] is None
        assert seen["admission"]["memory_override"] is None

    def test_the_sync_entry_forwards_them(self, tbl) -> None:  # noqa: ANN001
        with _spied_dispatch() as seen:
            tbl.backfill("b", num_cpus=0.25, num_gpus=0, memory=0)
        assert seen["dispatch"]["num_cpus"] == 0.25
        assert seen["dispatch"]["num_gpus"] == 0.0
        assert seen["dispatch"]["memory"] == 0

    @pytest.mark.parametrize(
        ("kwargs", "exc"),
        [
            ({"num_cpus": 0}, ValueError),
            ({"num_cpus": -1}, ValueError),
            ({"num_cpus": math.nan}, ValueError),
            ({"num_gpus": -0.5}, ValueError),
            ({"num_gpus": math.inf}, ValueError),
            ({"memory": -1}, ValueError),
            ({"num_cpus": "4"}, TypeError),
            ({"num_gpus": "1"}, TypeError),
            ({"memory": 1.5}, TypeError),
            ({"num_cpus": True}, TypeError),
            ({"num_gpus": True}, TypeError),
            ({"memory": True}, TypeError),
        ],
    )
    def test_bad_values_are_rejected(self, tbl, kwargs, exc) -> None:  # noqa: ANN001
        with pytest.raises(exc):
            tbl.backfill_async("b", **kwargs)
        with pytest.raises(exc):
            tbl.backfill("b", **kwargs)

    def test_fractions_and_zeros_are_accepted(self) -> None:
        from geneva.table import _normalize_backfill_resources

        assert _normalize_backfill_resources(4, None, None) == (4.0, None, None)
        assert _normalize_backfill_resources(0.25, 0.5, 0) == (0.25, 0.5, 0)
        assert _normalize_backfill_resources(None, 0, None) == (None, 0.0, None)
        assert _normalize_backfill_resources(None, None, None) == (None, None, None)

    def test_gpus_conflict_with_the_cpu_only_pool(self, tbl) -> None:  # noqa: ANN001
        with pytest.raises(ValueError, match="use_cpu_only_pool"):
            tbl.backfill_async("b", num_gpus=1, use_cpu_only_pool=True)
        # Zero GPUs *is* how a GPU UDF gets onto the CPU-only pool.
        with _spied_dispatch() as seen:
            tbl.backfill_async("c", num_gpus=0, use_cpu_only_pool=True)
        assert seen["dispatch"]["num_gpus"] == 0.0

    @pytest.mark.parametrize(
        "override", [{"num_cpus": 2}, {"num_gpus": 0}, {"memory": _GIB}]
    )
    def test_sparse_mode_forwards_overrides(
        self,
        tbl,  # noqa: ANN001
        override: dict,
    ) -> None:
        with _spied_dispatch() as seen:
            tbl.backfill_async(
                "b", where="a > 0", update_mode="sparse_rows", **override
            )
        (name, value), *_ = override.items()
        assert seen["admission"][f"{name}_override"] == value
        assert seen["dispatch"][name] == value
        assert seen["dispatch"]["update_mode"] == "sparse_rows"

    def test_sparse_mode_without_overrides_still_dispatches(self, tbl) -> None:  # noqa: ANN001
        with _spied_dispatch() as seen:
            tbl.backfill_async("b", where="a > 0", update_mode="sparse_rows")
        assert seen["dispatch"]["update_mode"] == "sparse_rows"
        assert seen["dispatch"]["num_cpus"] is None

    def test_sparse_mode_prices_one_range_per_actor(self, tbl) -> None:  # noqa: ANN001
        """Admission sees no multipliers, no writer overhead and no floor."""
        with _spied_dispatch() as seen:
            tbl.backfill_async(
                "b",
                where="a > 0",
                update_mode="sparse_rows",
                intra_applier_concurrency=4,
                memory=_GIB,
            )
        admission = seen["admission"]
        assert admission["intra_applier_concurrency"] == 1
        assert admission["enable_gpu_pipelining"] is False
        assert admission["fragment_writers"] is False
        assert admission["default_memory_bytes"] == 0
        assert admission["memory_override"] == _GIB

        with _spied_dispatch() as seen:
            tbl.backfill_async("b", intra_applier_concurrency=4)
        assert seen["admission"]["intra_applier_concurrency"] == 4
        assert seen["admission"]["fragment_writers"] is True

    def test_sparse_mode_keeps_validation(self, tbl, caplog) -> None:  # noqa: ANN001
        with pytest.raises(ValueError, match="num_cpus must be greater than 0"):
            tbl.backfill_async(
                "b", where="a > 0", update_mode="sparse_rows", num_cpus=0
            )
        with pytest.raises(ValueError, match="use_cpu_only_pool"):
            tbl.backfill_async(
                "c",
                where="a > 0",
                update_mode="sparse_rows",
                num_gpus=1,
                use_cpu_only_pool=True,
            )
        with (
            caplog.at_level(logging.WARNING, logger="geneva.table"),
            _spied_dispatch() as seen,
        ):
            tbl.backfill_async(
                "c", where="a > 0", update_mode="sparse_rows", num_gpus=0
            )
        assert "drops the GPU reservation" in caplog.text
        assert seen["dispatch"]["num_gpus"] == 0.0

    def test_dropping_a_gpu_declaration_to_zero_warns(self, tbl, caplog) -> None:  # noqa: ANN001
        with caplog.at_level(logging.WARNING, logger="geneva.table"):
            with _spied_dispatch():
                tbl.backfill_async("c", num_gpus=0)
            assert "drops the GPU reservation" in caplog.text
            caplog.clear()
            with _spied_dispatch():
                tbl.backfill_async("c", num_gpus=0.25)
            assert "drops the GPU reservation" not in caplog.text

    def test_the_udf_is_never_mutated(self, tbl) -> None:  # noqa: ANN001
        from geneva.runners.ray.pipeline import fetch_udf

        caller_owned = geneva.udf(data_type=pa.int64(), num_cpus=1.0, memory=_GIB)(
            lambda a: a + 2
        )
        before = (caller_owned.num_cpus, caller_owned.num_gpus, caller_owned.memory)
        version = caller_owned.version

        with _spied_dispatch():
            tbl.backfill_async(
                "b", udf=caller_owned, num_cpus=8, num_gpus=0.5, memory=16 * _GIB
            )
        with _spied_dispatch():
            tbl.backfill_async("c", num_cpus=8, num_gpus=0.5, memory=16 * _GIB)

        assert (
            caller_owned.num_cpus,
            caller_owned.num_gpus,
            caller_owned.memory,
        ) == before
        assert caller_owned.version == version
        registered = tbl._conn._packager.unmarshal(fetch_udf(tbl, "c"))
        assert (registered.num_cpus, registered.num_gpus, registered.memory) == (
            2.0,
            1.0,
            4 * _GIB,
        )


class TestJobMetadata:
    """The job record says what was asked for and what Ray was asked for."""

    def test_dispatch_receives_the_resolved_reservation(self, tmp_path) -> None:  # noqa: ANN001
        db = geneva.connect(str(tmp_path))
        tbl = db.create_table("t", pa.table({"a": pa.array([1], type=pa.int64())}))
        tbl.add_columns({"b": _plus_one})

        with _spied_dispatch() as seen:
            tbl.backfill_async(
                "b", num_cpus=0.5, memory=8 * _GIB, intra_applier_concurrency=2
            )
        metadata = seen["dispatch"]["resource_metadata"]
        assert metadata["resource_overrides"] == {
            "num_cpus": 0.5,
            "num_gpus": None,
            "memory": 8 * _GIB,
        }
        assert metadata["resolved_base_resources"] == {
            "num_cpus": 0.5,
            "num_gpus": 0.0,
            "memory": 8 * _GIB,
        }
        assert metadata["reservation_multipliers"] == {
            "cpu_thread_count": 2,
            "intra_applier_concurrency": 2,
        }
        assert metadata["expected_actor_reservation"] == {
            "num_cpus": 1.0,
            "num_gpus": 0.0,
            "memory": 16 * _GIB,
        }

    def test_no_overrides_records_the_declaration(self, tmp_path) -> None:  # noqa: ANN001
        db = geneva.connect(str(tmp_path))
        tbl = db.create_table("t", pa.table({"a": pa.array([1], type=pa.int64())}))
        tbl.add_columns({"c": _gpu_plus_one})

        with _spied_dispatch() as seen:
            tbl.backfill_async("c")
        metadata = seen["dispatch"]["resource_metadata"]
        assert all(v is None for v in metadata["resource_overrides"].values())
        assert metadata["resolved_base_resources"] == {
            "num_cpus": 2.0,
            "num_gpus": 1.0,
            "memory": 4 * _GIB,
        }
        assert metadata["expected_actor_reservation"]["num_gpus"] == 1.0

    def test_sparse_mode_records_an_unmultiplied_reservation(self, tmp_path) -> None:  # noqa: ANN001
        """Sparse actors reserve the base figures; there are no multipliers."""
        db = geneva.connect(str(tmp_path))
        tbl = db.create_table("t", pa.table({"a": pa.array([1], type=pa.int64())}))
        tbl.add_columns({"c": _gpu_plus_one})

        with _spied_dispatch() as seen:
            tbl.backfill_async(
                "c",
                where="a > 0",
                update_mode="sparse_rows",
                intra_applier_concurrency=3,
                num_cpus=0.5,
            )
        metadata = seen["dispatch"]["resource_metadata"]
        assert set(metadata) == {
            "resource_overrides",
            "resolved_base_resources",
            "expected_actor_reservation",
        }
        assert metadata["resolved_base_resources"] == {
            "num_cpus": 0.5,
            "num_gpus": 1.0,
            "memory": 4 * _GIB,
        }
        assert metadata["expected_actor_reservation"] == {
            "num_cpus": 0.5,
            "num_gpus": 1.0,
            "memory": 4 * _GIB,
        }

    def test_sparse_metadata_applies_the_actor_coercions(self) -> None:
        """The record says what the actor asks for, not the raw declaration."""
        from geneva.table import _backfill_resource_metadata

        metadata = _backfill_resource_metadata(
            _udf_stub(num_cpus=0.0, num_gpus=None, memory=None),
            num_cpus=None,
            num_gpus=None,
            memory=None,
            default_memory_bytes=0,
            cpu_thread_count=1,
            intra_applier_concurrency=1,
            include_multipliers=False,
        )
        assert "reservation_multipliers" not in metadata
        assert metadata["resolved_base_resources"] == {
            "num_cpus": 0.0,
            "num_gpus": None,
            "memory": 0,
        }
        assert metadata["expected_actor_reservation"] == {
            "num_cpus": 1.0,
            "num_gpus": 0.0,
            "memory": 0,
        }

    def test_without_a_udf_only_the_request_is_recorded(self) -> None:
        from geneva.table import _backfill_resource_metadata

        metadata = _backfill_resource_metadata(
            None,
            num_cpus=2.0,
            num_gpus=None,
            memory=None,
            default_memory_bytes=0,
            cpu_thread_count=1,
            intra_applier_concurrency=1,
        )
        assert set(metadata) == {"resource_overrides"}

    def test_the_job_record_round_trips_it(self, tmp_path) -> None:  # noqa: ANN001
        from geneva.jobs.jobs import JobStateManager
        from geneva.table import _backfill_resource_metadata

        metadata = _backfill_resource_metadata(
            _plus_one,
            num_cpus=0.5,
            num_gpus=None,
            memory=None,
            default_memory_bytes=0,
            cpu_thread_count=1,
            intra_applier_concurrency=1,
        )
        db = geneva.connect(str(tmp_path))
        jsm = JobStateManager(genevadb=db, jobs_table_name="test_jobs_resources")
        record = jsm.launch("t", "b", **metadata)
        config = json.loads(record.config)
        assert config["resource_overrides"]["num_cpus"] == 0.5
        assert config["resolved_base_resources"]["memory"] == 2 * _GIB
        assert config["expected_actor_reservation"]["num_cpus"] == 0.5


class TestRemoteConnections:
    """Remote (``db://``) dispatch must refuse, not forward or drop."""

    @staticmethod
    def _remote_table(monkeypatch):  # noqa: ANN001, ANN205
        from geneva.table import Table

        captured: dict = {}

        class _Conn:
            def use_remote_dispatch(self) -> bool:
                return True

        table = object.__new__(Table)
        object.__setattr__(table, "_conn", _Conn())
        monkeypatch.setattr(Table, "_canonical_backfill_output_column", lambda _s, c: c)
        monkeypatch.setattr(Table, "_validate_update_mode", lambda *_a, **_k: None)

        def _fake_v2(_self, col_name, **kwargs):  # noqa: ANN001, ANN003, ANN202
            captured.update(kwargs)
            captured["col_name"] = col_name
            return "dispatched"

        monkeypatch.setattr(Table, "_backfill_async_v2", _fake_v2)
        return table, captured

    @pytest.mark.parametrize(
        "override", [{"num_cpus": 2}, {"num_gpus": 0}, {"memory": 0}]
    )
    def test_overrides_are_rejected(self, monkeypatch, override: dict) -> None:  # noqa: ANN001
        from geneva.table import Table

        table, captured = self._remote_table(monkeypatch)
        with pytest.raises(NotImplementedError, match="remote connections"):
            Table.backfill_async(table, "b", **override)
        assert captured == {}

    def test_without_overrides_the_request_is_unchanged(self, monkeypatch) -> None:  # noqa: ANN001
        from geneva.table import Table

        table, captured = self._remote_table(monkeypatch)
        assert Table.backfill_async(table, "b", concurrency=3) == "dispatched"
        assert captured["concurrency"] == 3
        assert not {"num_cpus", "num_gpus", "memory"} & set(captured)


class TestDriverForwarding:
    """The Ray driver hands the sparse pipeline what the client resolved."""

    def test_the_sparse_branch_forwards_reservations(
        self,
        tmp_path,  # noqa: ANN001
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        from geneva.runners.ray import sparse_pipeline as sparse_mod
        from geneva.runners.ray.pipeline import run_ray_add_column_remote
        from geneva.runners.sparse_update import SparseUpdateResult

        db = geneva.connect(str(tmp_path))
        tbl = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
        tbl.add_columns({"b": _plus_one})

        seen: dict = {}

        def _fake_sparse(table_ref, udf, where, output_column, **kwargs):  # noqa: ANN001, ANN003, ANN202
            seen.update(kwargs, where=where, output_column=output_column, udf=udf)
            return SparseUpdateResult(
                base_version=1,
                committed_version=2,
                rows_total=2,
                rows_matched=1,
                rows_written=1,
                fragments_total=1,
                fragments_touched=1,
                fragment_equiv_rows=2,
            )

        # The branch imports it lazily, so the module attribute is what runs.
        monkeypatch.setattr(sparse_mod, "run_ray_sparse_update", _fake_sparse)
        # No job_id and no job_tracker: nothing to record, so no Ray needed.
        payload = run_ray_add_column_remote._function(
            tbl.get_reference(),
            "b",
            update_mode="sparse_rows",
            where="a > 1",
            num_cpus=0.5,
            num_gpus=0,
            memory=_GIB,
            use_cpu_only_pool=True,
        )

        assert seen["num_cpus"] == 0.5
        assert seen["num_gpus"] == 0
        assert seen["memory"] == _GIB
        assert seen["use_cpu_only_pool"] is True
        assert seen["where"] == "a > 1"
        assert seen["output_column"] == "b"
        assert seen["udf"].name == _plus_one.name
        assert payload["rows_processed"] == 1
        assert payload["rows_skipped"] == 1


class TestSignatures:
    """A knob that reaches only half the pipeline is worse than none."""

    def test_every_pipeline_hop_carries_all_three(self) -> None:
        from geneva.runners.ray.pipeline import (
            dispatch_run_ray_add_column,
            run_ray_add_column,
            run_ray_add_column_remote,
        )
        from geneva.runners.ray.sparse_pipeline import run_ray_sparse_update

        for hop in (
            dispatch_run_ray_add_column,
            run_ray_add_column,
            run_ray_add_column_remote._function,
            run_ray_sparse_update,
        ):
            params = inspect.signature(hop).parameters
            for name in ("num_cpus", "num_gpus", "memory"):
                assert name in params, (hop.__name__, name)
        assert (
            "use_cpu_only_pool" in inspect.signature(run_ray_sparse_update).parameters
        )

    def test_metadata_stops_at_dispatch(self) -> None:
        """Forwarding it would be a TypeError inside the Ray task."""
        from geneva.runners.ray.pipeline import (
            dispatch_run_ray_add_column,
            run_ray_add_column,
            run_ray_add_column_remote,
        )

        assert (
            "resource_metadata"
            in inspect.signature(dispatch_run_ray_add_column).parameters
        )
        for hop in (run_ray_add_column, run_ray_add_column_remote._function):
            assert "resource_metadata" not in inspect.signature(hop).parameters


@geneva.udf(data_type=pa.string(), num_cpus=2.0, memory=_GIB)
def _assigned_resources(a: int) -> str:
    """Report what Ray actually granted the actor running this row."""
    import ray

    return json.dumps(ray.get_runtime_context().get_assigned_resources())


@pytest.mark.ray
class TestTwoPassBackfill:
    """One registered UDF, two filtered passes over one column, each with its
    own reservation, on real Ray."""

    def test_each_pass_runs_under_its_own_reservation(
        self,
        db,  # noqa: ANN001
        local_ray_context,  # noqa: ANN001
    ) -> None:
        tbl = db.create_table(
            "videos", pa.table({"a": pa.array(range(8), type=pa.int64())})
        )
        tbl.add_columns({"res": _assigned_resources})

        # Both passes differ from the UDF's declaration (2 CPUs, 1 GiB).
        tbl.backfill(
            "res",
            where="res IS NULL AND a % 2 = 0",
            concurrency=1,
            num_cpus=0.5,
            memory=256 * 2**20,
        )
        tbl.backfill(
            "res",
            where="res IS NULL AND a % 2 = 1",
            concurrency=1,
            num_cpus=1,
            memory=0,
        )
        tbl.checkout_latest()

        rows = tbl.to_arrow().to_pylist()
        assert len(rows) == 8
        assert all(row["res"] is not None for row in rows)
        for row in rows:
            granted = json.loads(row["res"])
            if row["a"] % 2 == 0:
                assert granted["CPU"] == 0.5
                assert granted["memory"] == 256 * 2**20
            else:
                assert granted["CPU"] == 1.0
                assert "memory" not in granted

    def test_an_ordinary_pass_then_a_sparse_pass_each_under_its_own_reservation(
        self,
        db,  # noqa: ANN001
        local_ray_context,  # noqa: ANN001
    ) -> None:
        """One ordinary pass, then one sparse pass, each under its own
        reservation; nothing lost or duplicated."""
        tbl = db.create_table(
            "videos", pa.table({"a": pa.array(range(8), type=pa.int64())})
        )
        tbl.add_columns({"res": _assigned_resources})

        # Both passes differ from the UDF's declaration (2 CPUs, 1 GiB).
        tbl.backfill(
            "res",
            where="res IS NULL AND a < 4",
            concurrency=1,
            num_cpus=0.5,
            memory=256 * 2**20,
        )
        tbl.checkout_latest()
        first = {
            row["a"]: row["res"]
            for row in tbl.to_arrow().to_pylist()
            if row["res"] is not None
        }
        assert set(first) == set(range(4))

        tbl.backfill(
            "res",
            where="res IS NULL AND a >= 4",
            update_mode="sparse_rows",
            concurrency=1,
            num_cpus=1,
            memory=128 * 2**20,
        )
        tbl.checkout_latest()

        rows = tbl.to_arrow().to_pylist()
        assert sorted(row["a"] for row in rows) == list(range(8))
        by_id = {row["a"]: row["res"] for row in rows}
        assert all(res is not None for res in by_id.values())
        assert {a: by_id[a] for a in first} == first
        for a, res in by_id.items():
            granted = json.loads(res)
            if a < 4:
                assert granted["CPU"] == 0.5
                assert granted["memory"] == 256 * 2**20
            else:
                assert granted["CPU"] == 1.0
                assert granted["memory"] == 128 * 2**20
