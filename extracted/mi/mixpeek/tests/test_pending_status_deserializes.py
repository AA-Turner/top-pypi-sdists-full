"""A manifest apply result with status pending deserializes.

The server added `pending` (with `pending_reason`) to the manifest apply and
plan result for a taxonomy promoted from a cluster run, and
the Python SDK raised on that row until its generated enum caught up. These
tests read the generated models as a client does, so a regeneration that drops
the value, or a server value the SDK never learns, fails here.
"""

from mixpeek.models.cluster_execution_result import ClusterExecutionResult
from mixpeek.models.resource_result import ResourceResult
from mixpeek.models.resource_result_status import ResourceResultStatus


def test_the_enum_has_pending():
    assert ResourceResultStatus("pending") is ResourceResultStatus.PENDING


def test_an_apply_row_with_status_pending_deserializes():
    row = ResourceResult.from_dict(
        {
            "resource_type": "taxonomy",
            "name": "scene-themes",
            "status": "pending",
            "pending_reason": "waits for the source cluster run to complete",
        }
    )
    assert row.status == ResourceResultStatus.PENDING
    assert row.pending_reason == "waits for the source cluster run to complete"


def test_a_cluster_run_with_status_pending_deserializes():
    run = ClusterExecutionResult.from_dict(
        {
            "run_id": "run_1",
            "cluster_id": "clust_1",
            "status": "pending",
            "num_clusters": 0,
            "num_points": 0,
            "created_at": "2026-10-22T00:00:00Z",
        }
    )
    assert run.status == "pending"
