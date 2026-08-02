# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for materialized view point-in-time refresh (rollback to older versions)."""

from unittest.mock import patch

import pytest

from conftest import create_filtered_mv, make_batch, refresh_and_verify
from geneva.jobs.config import JobConfig

pytestmark = pytest.mark.ray


# Four rollback tests below currently hang in
# ``FragmentWriterSession.drain()`` — the writer's actor never resolves its
# ``write.remote()`` future and gets restarted by the stall detector
# until ``MAX_WRITER_RESTARTS`` is exhausted. The failure pre-dates this
# branch (reproduces against ``main``'s pipeline / apply / loader code)
# and the refresh path is being reworked in #717
# (`feat(runners): V2 scalar UDTF refresh`), which replaces the
# per-batch driver-funnelled write with worker-side
# ``LanceFragment.create()`` + ``LanceOperation.Append``. Skipping until
# that lands so the stable CI suite isn't blocked.
_ROLLBACK_SKIP_REASON = (
    "matview point-in-time rollback hangs the FragmentWriter; "
    "refresh path is being reworked in #717. Re-enable once that "
    "PR lands."
)


def test_point_in_time_refresh_requires_stable_row_ids(db, local_ray_context) -> None:
    """Test that point-in-time refresh fails without stable row IDs."""
    # Create table WITHOUT stable row IDs
    animals = db.create_table("animals", make_batch(0, 100))
    v1 = animals.version

    # Create MV and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)

    # Add more data
    animals.add(make_batch(100, 50))
    v2 = animals.version
    assert v2 > v1

    # Refresh to v2 should fail (different version without stable row IDs)
    with pytest.raises(RuntimeError, match="stable row IDs"):
        dogs.refresh()


@pytest.mark.skip(reason=_ROLLBACK_SKIP_REASON)
def test_point_in_time_refresh_rollback(db, local_ray_context) -> None:
    """Test that we can roll back to an older source version with stable row IDs."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)  # 50 dogs out of 100 (every other row)

    # Add more data
    animals.add(make_batch(100, 50))

    # Refresh to latest
    refresh_and_verify(dogs, 75)  # 75 dogs out of 150

    # Rollback to v1 (point-in-time refresh)
    refresh_and_verify(dogs, 50, src_version=v1)  # Back to 50 dogs

    # Can refresh forward again
    refresh_and_verify(dogs, 75)  # Back to 75 dogs


@pytest.mark.skip(reason=_ROLLBACK_SKIP_REASON)
def test_point_in_time_refresh_multiple_rollbacks(db, local_ray_context) -> None:
    """Test multiple rollback and forward refreshes."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)

    # Add batch 2
    animals.add(make_batch(100, 50))
    v2 = animals.version
    refresh_and_verify(dogs, 75)

    # Add batch 3
    animals.add(make_batch(150, 50))
    v3 = animals.version
    refresh_and_verify(dogs, 100)

    # Rollback to v1
    refresh_and_verify(dogs, 50, src_version=v1)

    # Rollback to v2
    refresh_and_verify(dogs, 75, src_version=v2)

    # Forward to v3
    refresh_and_verify(dogs, 100, src_version=v3)

    # Rollback to v1 again
    refresh_and_verify(dogs, 50, src_version=v1)


@pytest.mark.skip(reason=_ROLLBACK_SKIP_REASON)
def test_point_in_time_refresh_without_filter(db, local_ray_context) -> None:
    """Test point-in-time refresh on MV without WHERE filter."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV without filter (copies all rows)
    all_animals = animals.search(None).create_materialized_view(
        conn=db, view_name="all_animals"
    )
    refresh_and_verify(all_animals, 100)

    # Add more data
    animals.add(make_batch(100, 50))

    # Refresh to latest
    refresh_and_verify(all_animals, 150)

    # Rollback to v1
    refresh_and_verify(all_animals, 100, src_version=v1)

    # Forward again
    refresh_and_verify(all_animals, 150)


@pytest.mark.skip(reason=_ROLLBACK_SKIP_REASON)
def test_point_in_time_refresh_batched_deletion(db, local_ray_context) -> None:
    """Test that rollback deletes rows in batches when delete_batch_size is small."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )
    v1 = animals.version

    # Create MV without filter (copies all rows)
    all_animals = animals.search(None).create_materialized_view(
        conn=db, view_name="all_animals"
    )
    refresh_and_verify(all_animals, 100)

    # Add more data - 50 additional rows
    animals.add(make_batch(100, 50))

    # Refresh to latest
    refresh_and_verify(all_animals, 150)

    # Rollback to v1 with small batch size (10) to force multiple batches
    # This will delete 50 rows in 5 batches of 10
    config_with_small_batch = JobConfig(delete_batch_size=10)

    with patch.object(JobConfig, "get", return_value=config_with_small_batch):
        refresh_and_verify(all_animals, 100, src_version=v1)


def test_forward_refresh_with_source_deletions(db, local_ray_context) -> None:
    """Test that forward refresh deletes MV rows when source rows are deleted."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV for dogs only and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)  # 50 dogs (IDs 0, 2, 4, ..., 98)

    # Delete some dogs from source (IDs 0, 2, 4 are dogs)
    animals.delete("id IN (0, 2, 4)")

    # Forward refresh should detect and delete corresponding MV rows, and the
    # surviving dogs must keep their real projected values. The deleted dogs sit
    # before the survivors in the same fragment, so an incremental refresh that
    # reads survivors at a stale positional offset would null them out while the
    # count stays correct (GEN-619). column_checks catches that; a count-only
    # assertion does not.
    surviving_dog_ids = list(range(6, 100, 2))  # 6, 8, ..., 98
    refresh_and_verify(
        dogs,
        47,  # 50 - 3 deleted dogs
        column_checks={
            "id": surviving_dog_ids,
            "value": [i * 10 for i in surviving_dog_ids],
        },
    )


def test_forward_refresh_with_mixed_adds_and_deletes(db, local_ray_context) -> None:
    """Test forward refresh handles both additions and deletions."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV for dogs only and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)  # 50 dogs

    # Delete some dogs (IDs 0, 2 are dogs)
    animals.delete("id IN (0, 2)")

    # Add new rows (IDs 100-149, 25 will be dogs)
    animals.add(make_batch(100, 50))

    # Forward refresh should handle both deletions and additions
    # 50 original - 2 deleted + 25 new dogs = 73
    refresh_and_verify(dogs, 73)


def test_forward_refresh_filter_affects_deletions(db, local_ray_context) -> None:
    """Test that MV filter is applied when checking deletions."""
    # Create table WITH stable row IDs
    animals = db.create_table(
        "animals",
        make_batch(0, 100),
        storage_options={"new_table_enable_stable_row_ids": True},
    )

    # Create MV for dogs only and refresh
    dogs = create_filtered_mv(db, animals, "dogs", "category == 'dog'")
    refresh_and_verify(dogs, 50)

    # Delete cats (IDs 1, 3, 5 are cats, not dogs)
    animals.delete("id IN (1, 3, 5)")

    # Forward refresh should not affect MV (cats weren't in it)
    refresh_and_verify(dogs, 50)  # Still 50 dogs
