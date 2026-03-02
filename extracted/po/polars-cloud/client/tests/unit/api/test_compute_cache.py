from __future__ import annotations

import polars_cloud as pc
import pytest
from polars_cloud.context import cache


@pytest.mark.usefixtures("_mock_workspace_by_name_with_workspace_defaults")
def test_set_compute_context(workspace_name: str) -> None:
    assert cache.cached_context is None

    ctx = pc.ComputeContext(
        workspace=workspace_name, instance_type="g5.xlarge", cluster_size=4
    )
    pc.set_compute_context(ctx)

    assert cache.cached_context == ctx


@pytest.mark.usefixtures("_mock_workspace_by_name_with_workspace_defaults")
def test_set_compute_context_contextmanager(workspace_name: str) -> None:
    assert cache.cached_context is None

    ctx = pc.ComputeContext(
        workspace=workspace_name, instance_type="g5.xlarge", cluster_size=4
    )
    with pc.set_compute_context(ctx):
        assert cache.cached_context == ctx

    assert cache.cached_context is None

    with pc.set_compute_context(ctx):
        assert cache.cached_context == ctx

    assert cache.cached_context is None

    @pc.set_compute_context(ctx)
    def assert_function() -> None:
        assert cache.cached_context == ctx

    assert cache.cached_context is None

    assert_function()

    assert cache.cached_context is None


@pytest.mark.usefixtures("_mock_workspace_by_name_with_workspace_defaults")
def test_set_compute_context_contextmanager_reentrant(workspace_name: str) -> None:
    assert cache.cached_context is None
    ctx_outer = pc.ComputeContext(
        workspace=workspace_name, instance_type="t3.micro", cluster_size=1
    )
    ctx_inner = pc.ComputeContext(
        workspace=workspace_name, instance_type="t3.large", cluster_size=1
    )

    with pc.set_compute_context(ctx_outer):
        assert cache.cached_context == ctx_outer

        with pc.set_compute_context(ctx_inner):
            assert cache.cached_context == ctx_inner

        assert cache.cached_context == ctx_outer

    assert cache.cached_context is None
