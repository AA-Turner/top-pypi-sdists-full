# mypy: disable-error-code="attr-defined,return-value,no-untyped-def"
from __future__ import annotations

import polars_cloud as pc
import pytest
from polars_cloud.exceptions import ComputeClusterMisspecified


@pytest.mark.usefixtures("_mock_workspace_by_name_with_workspace_defaults")
def test_compute(workspace_name) -> None:
    ctx = pc.ComputeContext(
        instance_type="g5.xlarge",
        # big_instance_type="g5.xlarge",
        cluster_size=4,
        workspace=workspace_name,
    )

    assert ctx.workspace.name == workspace_name
    assert ctx.instance_type == "g5.xlarge"
    # assert ctx.big_instance_type == "g5.xlarge"
    assert ctx.cluster_size == 4


@pytest.mark.usefixtures("_mock_workspace_by_name_with_workspace_defaults")
def test_compute_with_architectures(workspace_name) -> None:
    ctx = pc.ComputeContext(
        cpus=8,
        memory=8,
        cpu_architectures=["arm64"],
        cluster_size=1,
        workspace=workspace_name,
    )
    assert ctx.cpu_architectures == ["arm64"]


@pytest.mark.usefixtures("_mock_workspace_by_name")
def test_compute_overspecified(workspace_name) -> None:
    with pytest.raises(ComputeClusterMisspecified, match="cannot specify both"):
        pc.ComputeContext(workspace=workspace_name, instance_type="g5.xlarge", memory=8)


@pytest.mark.usefixtures("_mock_workspace_by_name")
def test_compute_overspecified_architectures(workspace_name) -> None:
    with pytest.raises(ComputeClusterMisspecified, match="cannot specify both"):
        pc.ComputeContext(
            workspace=workspace_name,
            instance_type="g5.xlarge",
            cpu_architectures=["x86_64"],
        )


@pytest.mark.usefixtures("_mock_workspace_by_name")
def test_compute_misspecified_memory_only(workspace_name) -> None:
    with pytest.raises(ComputeClusterMisspecified, match="`cpus` is required"):
        pc.ComputeContext(workspace=workspace_name, memory=8)


@pytest.mark.usefixtures("_mock_workspace_by_name")
def test_compute_misspecified_cpu_only(workspace_name) -> None:
    with pytest.raises(ComputeClusterMisspecified, match="`memory` is required"):
        pc.ComputeContext(workspace=workspace_name, cpus=8)


@pytest.mark.usefixtures("_mock_workspace_by_name", "_mock_no_default_cluster_settings")
def test_compute_incomplete(workspace_name) -> None:
    with pytest.raises(ComputeClusterMisspecified, match="Compute specification"):
        pc.ComputeContext(workspace=workspace_name)


# @pytest.mark.usefixtures("_mock_workspace_by_name")
# def test_compute_overspecified_big_instance_multiplier(workspace_name) -> None:
#     with pytest.raises(ComputeClusterMisspecified, match="cannot specify both"):
#         pc.ComputeContext(
#             workspace=workspace_name,
#             instance_type="g5.xlarge",
#             big_instance_multiplier=8,
#         )


# @pytest.mark.usefixtures("_mock_workspace_by_name")
# def test_compute_overspecified_big_instance_type(workspace_name) -> None:
#     with pytest.raises(ComputeClusterMisspecified, match="cannot specify both"):
#         pc.ComputeContext(
#             workspace=workspace_name, memory=4, cpus=4, big_instance_type="g5.xlarge"
#         )


@pytest.mark.usefixtures(
    "_mock_workspace_by_default", "_mock_default_cluster_settings_instance_type"
)
def test_compute_default(instance_type, workspace_name) -> None:
    ctx = pc.ComputeContext()
    assert ctx.workspace.name == workspace_name
    assert ctx.instance_type == instance_type


@pytest.mark.usefixtures("_mock_workspace_by_name", "_mock_defaults_failure")
def test_compute_cluster_avoid_loading_defaults(workspace_name) -> None:
    ctx = pc.ComputeContext(
        workspace=workspace_name,
        instance_type="t3.micro",
        storage=16,
        cluster_size=1,
    )
    assert ctx.instance_type == "t3.micro"
    assert ctx.storage == 16
    assert ctx.cluster_size == 1
