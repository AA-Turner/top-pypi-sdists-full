"""Shared pytest fixtures."""

from __future__ import annotations

from typing import Any

import pytest

TEST_BASE_URL = "https://hogland.test"


@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Strip real HOG_* env, then set test defaults under monkeypatch.

    Using ``monkeypatch.setenv`` instead of ``os.environ.setdefault`` so
    pytest's teardown restores the original env. ``setdefault`` would
    leak the test values past the test boundary.
    """
    for var in ("HOG_TOKEN", "HOG_HOST", "HOG_CONFIG"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("HOG_TOKEN", "test-token")
    monkeypatch.setenv("HOG_HOST", TEST_BASE_URL)


@pytest.fixture
def box_view_json() -> dict[str, Any]:
    """A minimal valid BoxView JSON, shared across sync + async tests."""
    return {
        "id": "hb-fixture",
        "spec": {
            "cpus": 1,
            "memory_mib": 1024,
            "disk_gib": 10,
            "disk_class": "mirrored",
            "disk_mbps": 0,
            "disk_iops": 0,
            "net_mbps": 0,
        },
        "status": "running",
        "created_at": "2026-05-19T10:00:00Z",
        "updated_at": "2026-05-19T10:00:01Z",
    }
