"""Pins the shared Snapshot.list filter set across the SDK family.

Both SDKs accept {service_id, name, type, status, limit, offset}: `name` maps
to the API's `name` query param, while `service_id` filters the returned page
client-side — the list endpoint has no service_id query param.
"""

import inspect
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch

from koyeb.api.models.instance_snapshot_type import InstanceSnapshotType
from koyeb.sandbox.snapshot import Snapshot, SnapshotType


def _api_snapshot(idx, service_id=None):
    return SimpleNamespace(
        id=f"snap-{idx}",
        name=f"snapshot-{idx}",
        service_id=service_id or f"svc-{idx}",
        type=SimpleNamespace(value="INSTANCE_SNAPSHOT_TYPE_FILESYSTEM"),
        status=SimpleNamespace(value="INSTANCE_SNAPSHOT_STATUS_AVAILABLE"),
        created_at=datetime(2026, 9, 24, tzinfo=timezone.utc),
        available_at=None,
        deployment_id="dep-1",
        region=None,
        regional_deployment_id=None,
        organization_id="org-1",
        project_id=None,
        instance_id="inst-1",
        messages=[],
    )


class FakeInstanceSnapshotsApi:
    """Records list kwargs and returns a fixed page, like the generated client."""

    def __init__(self, snapshots):
        self.snapshots = snapshots
        self.calls = []

    def list_instance_snapshots(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(instance_snapshots=list(self.snapshots))


class TestSnapshotList(unittest.TestCase):
    def _list(self, api, **kwargs):
        with patch(
            "koyeb.sandbox.snapshot.get_api_clients",
            return_value=SimpleNamespace(instance_snapshots=api),
        ):
            return Snapshot.list(api_token="tok", **kwargs)

    def test_filters_map_to_the_api_query(self):
        api = FakeInstanceSnapshotsApi([_api_snapshot(1)])

        found = self._list(
            api,
            service_id="svc-1",
            name="snapshot-1",
            snapshot_type=SnapshotType.FULL,
            limit=10,
            offset=5,
        )

        # Shared parity set, pinned: every filter except service_id is
        # API-shaped; service_id never reaches the query.
        self.assertEqual(
            api.calls[0],
            {
                "limit": "10",
                "offset": "5",
                "name": "snapshot-1",
                "type": InstanceSnapshotType.INSTANCE_SNAPSHOT_TYPE_FULL,
            },
        )
        self.assertEqual([s.id for s in found], ["snap-1"])
        self.assertEqual(found[0].service_id, "svc-1")

    def test_service_id_filters_the_returned_page(self):
        api = FakeInstanceSnapshotsApi(
            [_api_snapshot(1, service_id="svc-1"), _api_snapshot(2, service_id="svc-2")]
        )

        found = self._list(api, service_id="svc-2")

        self.assertEqual([s.id for s in found], ["snap-2"])
        self.assertEqual(found[0].service_id, "svc-2")

    def test_shared_filter_set_matches_the_js_parity_set(self):
        # JS ListSnapshotsFilter: { type, status, name, service_id, limit, offset }
        # plus token/host plumbing — Python names `type` as `snapshot_type`.
        params = set(inspect.signature(Snapshot.list).parameters)
        self.assertEqual(
            params,
            {"service_id", "name", "snapshot_type", "status", "limit", "offset", "api_token", "host"},
        )


if __name__ == "__main__":
    unittest.main()
