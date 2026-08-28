# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Ray dashboard names: every task/actor row must carry its job history id."""

from hashlib import sha256
from unittest.mock import patch

import pyarrow as pa
import pytest

from geneva import udf
from geneva.checkpoint import CheckpointStore
from geneva.runners.ray.naming import job_tracker_name, ray_name


def test_full_name_carries_table_column_detail_and_job() -> None:
    name = ray_name(
        "applier.run",
        table="videos",
        column="embedding",
        job_id="8f1c4d02",
        detail="frag=12 off=4096",
    )
    assert name == "job=8f1c4d02 applier.run(videos.embedding) frag=12 off=4096"


def test_missing_fields_are_omitted() -> None:
    assert ray_name("backfill.driver") == "backfill.driver"
    assert ray_name("writer", job_id="j1") == "job=j1 writer"
    assert ray_name("writer", table="videos") == "writer(videos)"
    assert ray_name("writer", column="embedding") == "writer(embedding)"


def test_empty_fields_are_treated_as_missing() -> None:
    assert ray_name("writer", table="", column="   ", job_id=None) == "writer"


def test_component_falls_back_when_blank() -> None:
    assert ray_name("", table="videos") == "geneva(videos)"


def test_newlines_and_tabs_cannot_split_a_log_prefix() -> None:
    name = ray_name("applier", table="odd\nname", column="a\tb", job_id="j\n1")
    assert "\n" not in name
    assert "\t" not in name
    assert name == "job=j_1 applier(odd_name.a_b)"


def test_long_fields_are_truncated_and_marked() -> None:
    name = ray_name("applier", table="t" * 200, job_id="j" * 200)
    assert len(name) <= 200
    assert "~" in name


def test_job_id_is_not_shortened_for_a_real_uuid() -> None:
    job_id = "8f1c4d02-1111-2222-3333-444455556666"
    assert ray_name("backfill.driver", job_id=job_id).startswith(f"job={job_id}")


def test_the_length_cap_can_never_eat_the_job_id() -> None:
    """The job id leads, so an over-long scope trims itself, not the link."""
    job_id = "8f1c4d02-1111-2222-3333-444455556666"
    name = ray_name(
        "udtf.process_partition",
        table="t" * 48,
        column="c" * 48,
        detail="part=" + "v" * 91,
        job_id=job_id,
    )
    assert len(name) <= 200
    assert name.startswith(f"job={job_id} udtf.process_partition(")


def test_job_tracker_name_is_a_stable_lookup_handle() -> None:
    assert job_tracker_name("abc") == "jobtracker-abc"
    assert job_tracker_name("abc", prefix="jobtracker-udtf") == "jobtracker-udtf-abc"


def test_applier_actor_repr_links_to_the_job_row() -> None:
    """The dashboard's actor list must name the job, table and UDF."""
    from geneva.runners.ray.pipeline import ApplierActor

    class FakeBatchApplier:
        job_id = "8f1c4d02"

    class FakeApplier:
        batch_applier = FakeBatchApplier()

    actor = ApplierActor.__ray_metadata__.modified_class(
        applier=FakeApplier(),
        table_name="videos",
        column_name="embedding",
        job_id="8f1c4d02",
    )
    assert repr(actor) == "job=8f1c4d02 applier(videos.embedding)"

    # Falls back to the applier's own job id when the driver label is absent.
    unlabeled = ApplierActor.__ray_metadata__.modified_class(applier=FakeApplier())
    assert repr(unlabeled) == "job=8f1c4d02 applier"


def test_applier_actor_repr_survives_a_broken_applier() -> None:
    from geneva.runners.ray.pipeline import ApplierActor

    class ExplodingApplier:
        @property
        def batch_applier(self) -> object:
            raise RuntimeError("boom")

    actor = ApplierActor.__ray_metadata__.modified_class(applier=ExplodingApplier())
    assert repr(actor) == "applier"


def test_fragment_writer_repr_names_its_fragment_and_job() -> None:
    from geneva.runners.ray.writer import FragmentWriter

    writer_cls = FragmentWriter.__ray_metadata__.modified_class
    with patch.object(CheckpointStore, "from_uri", return_value=object()):
        writer = writer_cls(
            uri="memory://test",
            column_names=["embedding"],
            checkpoint_uri="memory:///",
            fragment_id=12,
            checkpoint_keys=None,
            job_id="8f1c4d02",
            table_name="videos",
        )
    assert repr(writer) == "job=8f1c4d02 writer(videos.embedding) frag=12"


def test_job_tracker_repr_names_its_table_and_job() -> None:
    from geneva.runners.ray.jobtracker import _JobTracker
    from geneva.table import TableReference

    tracker = _JobTracker(
        job_id="8f1c4d02",
        table_ref=TableReference(
            table_id=["videos"], version=None, db_uri="memory://db"
        ),
        enable_saves=False,
    )
    assert repr(tracker) == "job=8f1c4d02 jobtracker(videos)"


def test_read_task_detail_scopes_a_task_to_its_fragment_range() -> None:
    from geneva.runners.ray.pipeline import _read_task_detail

    class FakeTask:
        def dest_frag_id(self) -> int:
            return 12

        def dest_offset(self) -> int:
            return 4096

    assert _read_task_detail(FakeTask()) == "frag=12 off=4096"
    assert _read_task_detail(object()) is None


def test_udtf_partition_detail_labels_both_partition_kinds() -> None:
    from geneva.table import _IndexPartitionInfo, _udtf_partition_detail

    index_info = _IndexPartitionInfo(
        partition_ordinal=3, index_name="idx", column="category"
    )
    assert _udtf_partition_detail((None, "prefix", index_info)) == "part=category#3"
    assert _udtf_partition_detail((None, "prefix", None)) is None
    assert _udtf_partition_detail(("bad",)) is None


def test_udtf_partition_detail_never_leaks_the_partition_value() -> None:
    """A column partition's predicate is raw source data: digest it, don't show it."""
    from geneva.table import _udtf_partition_detail

    predicate = "email = 'alice@example.com'"
    detail = _udtf_partition_detail(
        (predicate, "prefix", None), partition_column="email"
    )
    assert detail is not None
    assert "alice@example.com" not in detail
    assert detail == f"part=email#{sha256(predicate.encode()).hexdigest()[:8]}"

    # ...and nothing leaks through the assembled name either.
    name = ray_name(
        "udtf.process_partition",
        table="orders",
        column="expand",
        job_id="8f1c4d02-1111-2222-3333-444455556666",
        detail=detail,
    )
    assert "alice@example.com" not in name

    # Stable across calls, distinct across partitions.
    other = _udtf_partition_detail(
        ("email = 'bob@example.com'", "prefix", None), partition_column="email"
    )
    assert detail == _udtf_partition_detail(
        (predicate, "prefix", None), partition_column="email"
    )
    assert detail != other


@pytest.mark.ray
def test_backfill_names_reach_the_ray_state_api(db, local_ray_context) -> None:
    """End to end: a real backfill's dashboard rows carry its job history id."""
    from ray.util.state import list_actors, list_tasks

    @udf(data_type=pa.int32())
    def times_ten(a: int) -> int:  # noqa: ANN001
        return a * 10

    tbl = db.create_table("images", pa.Table.from_pydict({"a": list(range(8))}))
    tbl.add_columns({"embedding": times_ten})
    result = tbl.backfill("embedding")
    job_id = result.job_id

    task_names = [
        task.name for task in list_tasks(limit=2000, raise_on_missing_output=False)
    ]
    assert (
        ray_name("backfill.driver", table="images", column="embedding", job_id=job_id)
        in task_names
    )
    applier_tasks = [n for n in task_names if " applier.run(images." in n]
    assert applier_tasks, task_names
    assert all(n.startswith(f"job={job_id} ") for n in applier_tasks)
    assert all(" frag=" in n for n in applier_tasks)

    # repr_name is a detail column, and actors without a custom ``__repr__``
    # (Ray's own queue actor) report None.
    actor_reprs = [
        actor.repr_name
        for actor in list_actors(detail=True, limit=2000, raise_on_missing_output=False)
        if actor.repr_name
    ]
    assert any(r.startswith(f"job={job_id} applier(images.") for r in actor_reprs), (
        actor_reprs
    )
    assert any(
        r == ray_name("jobtracker", table="images", job_id=job_id) for r in actor_reprs
    ), actor_reprs
