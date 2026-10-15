"""The task response carries metadata and target_device_id (a computer schedule's work is
metadata.device_op), so the web shows a just-created computer schedule without a second read."""

from __future__ import annotations

from matrx_scheduler.api import schemas


def test_task_response_keeps_metadata_and_target_device() -> None:
    row = {
        "id": "t", "user_id": "u", "kind": "device_op", "title": "Nightly", "queue": "default",
        "surfaces": ["desktop"], "enabled": True, "tags": [], "target_device_id": "dev-1",
        "metadata": {"device_op": {"op": "coding.start", "params": {"cwd": "/w"}}},
    }
    dumped = schemas.TaskResponse(**row).model_dump(mode="json")
    assert dumped["metadata"]["device_op"]["op"] == "coding.start"
    assert dumped["target_device_id"] == "dev-1"
    assert schemas.TaskResponse(**{k: v for k, v in row.items() if k != "metadata"}).metadata == {}
