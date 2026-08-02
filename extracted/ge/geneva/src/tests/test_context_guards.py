# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for LocalRayContext guards and local cluster context.

These tests are in a separate file because they have specific requirements
about context state that conflict with module-scoped fixtures.
"""

import importlib
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import ray

from geneva import connect
from geneva._context import get_current_context
from geneva.cluster import GenevaCluster
from geneva.db import Connection
from geneva.runners.ray.raycluster import RayCluster

pytestmark = pytest.mark.slow


def test_nested_local_ray_context_rejected(tmp_path: Path) -> None:
    """Test that nested local_ray_context raises RuntimeError."""
    db = connect(tmp_path)
    # Enter first context, then try to enter a second (should fail)
    with (
        Connection.local_ray_context(),
        pytest.raises(RuntimeError, match="Cannot enter local_ray_context"),
        db.local_ray_context(),
    ):
        pass


def test_local_context_rejected_when_remote_ray(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """Test that local_ray_context raises error when Ray is connected to remote."""
    db = connect(tmp_path)

    # Mock Ray as initialized and connected to a remote cluster
    monkeypatch.setattr("ray.is_initialized", lambda: True)
    monkeypatch.setattr("ray.util.client.ray.is_connected", lambda: True)

    with (
        pytest.raises(RuntimeError, match="connected to a remote cluster"),
        db.local_ray_context(),
    ):
        pass


def test_raycluster_enter_clears_context_on_apply_failure() -> None:
    """If RayCluster.apply() raises during __enter__, the context must be cleared.

    Reproduces the bug where a TimeoutError in apply() left a stale context
    because __exit__ is never called when __enter__ raises.
    """
    cluster = MagicMock(spec=RayCluster)
    cluster.apply = MagicMock(side_effect=TimeoutError("timed out"))

    assert get_current_context() is None

    with (
        patch.object(RayCluster, "__enter__", RayCluster.__enter__),
        patch.object(RayCluster, "__exit__", RayCluster.__exit__),
        pytest.raises(TimeoutError, match="timed out"),
    ):
        RayCluster.__enter__(cluster)

    # Context must be cleared even though __exit__ was never called
    assert get_current_context() is None


def test_context_local(tmp_path: Path) -> None:
    """Test that LOCAL_RAY cluster type invokes ray_cluster with local=True."""
    ray.shutdown()
    db = connect(tmp_path)

    cluster_name = "local-ray-cluster"
    gc = GenevaCluster.create_local(cluster_name).build()
    db.define_cluster(cluster_name, gc)

    # LOCAL_RAY should invoke ray_cluster with local=True
    with db.context(cluster=cluster_name):
        ray.get(ray.remote(lambda: importlib.import_module("geneva")).remote())
