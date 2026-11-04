# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""The cloud identity requirement on a RayCluster's service account.

A cloud identity annotation only grants anything when the pod's identity is what
authorises access to object storage. On a cluster with no cloud IAM provider the
annotation is meaningless, and requiring it rejects a service account that works.
``require_cloud_identity=False`` opts out; the RBAC access review is unaffected.
"""

import kubernetes.client as kc
import pytest

from geneva.runners.ray.raycluster import (
    _CLOUD_IDENTITY_ANNOTATIONS,
    _ValidationVisitor,
)


class _FakeServiceAccountMixin:
    def __init__(self, name: str = "test-sa") -> None:
        self.service_account = name


class _FakeCoreApi:
    """Returns a service account carrying exactly the annotations given."""

    def __init__(self, annotations: dict | None) -> None:
        self._annotations = annotations

    def read_namespaced_service_account(
        self, name: str, namespace: str
    ) -> kc.V1ServiceAccount:
        return kc.V1ServiceAccount(
            metadata=kc.V1ObjectMeta(name=name, annotations=self._annotations)
        )


class _NoAccessReviewVisitor(_ValidationVisitor):
    """Isolates the cloud identity gate from the RBAC access review."""

    def _check_sa_access(self, sa) -> None:  # noqa: ANN001
        return None


def _visitor(annotations: dict | None, *, require: bool) -> _NoAccessReviewVisitor:
    visitor = _NoAccessReviewVisitor()
    visitor.core_api = _FakeCoreApi(annotations)
    visitor.namespace = "geneva"
    visitor.cluster_name = "test-cluster"
    visitor.require_cloud_identity = require
    return visitor


@pytest.mark.parametrize("annotation", sorted(_CLOUD_IDENTITY_ANNOTATIONS))
def test_any_single_cloud_annotation_passes(annotation: str) -> None:
    visitor = _visitor({annotation: "some-identity"}, require=True)
    visitor.visit_service_account(_FakeServiceAccountMixin())


@pytest.mark.parametrize("annotations", [None, {}, {"unrelated": "value"}])
def test_missing_cloud_annotation_is_rejected_by_default(annotations) -> None:
    visitor = _visitor(annotations, require=True)
    with pytest.raises(
        ValueError, match="cloud service account|annotations"
    ) as excinfo:
        visitor.visit_service_account(_FakeServiceAccountMixin())
    # the error names the way out, so the user is not left guessing
    assert "require_cloud_identity=False" in str(excinfo.value)


@pytest.mark.parametrize("annotations", [None, {}, {"unrelated": "value"}])
def test_opt_out_accepts_a_service_account_without_cloud_identity(annotations) -> None:
    visitor = _visitor(annotations, require=False)
    visitor.visit_service_account(_FakeServiceAccountMixin())


def test_opt_out_still_requires_the_service_account_to_exist() -> None:
    class _Missing404:
        def read_namespaced_service_account(
            self, name: str, namespace: str
        ) -> kc.V1ServiceAccount:
            raise kc.exceptions.ApiException(status=404, reason="Not Found")

    visitor = _NoAccessReviewVisitor()
    visitor.core_api = _Missing404()
    visitor.namespace = "geneva"
    visitor.require_cloud_identity = False
    with pytest.raises(ValueError, match="does not exist"):
        visitor.visit_service_account(_FakeServiceAccountMixin("absent-sa"))


def test_no_service_account_skips_validation_entirely() -> None:
    visitor = _visitor(None, require=True)
    visitor.visit_service_account(_FakeServiceAccountMixin(None))


def test_rbac_access_review_still_runs_when_cloud_identity_is_skipped() -> None:
    """The autoscaler genuinely needs pod/raycluster permissions, so opting out
    of the cloud identity check must NOT weaken the access review."""
    called = {"n": 0}

    class _RecordingVisitor(_ValidationVisitor):
        def _check_sa_access(self, sa) -> None:  # noqa: ANN001
            called["n"] += 1

    visitor = _RecordingVisitor()
    visitor.core_api = _FakeCoreApi({})
    visitor.namespace = "geneva"
    visitor.require_cloud_identity = False
    visitor.visit_service_account(_FakeServiceAccountMixin())
    assert called["n"] == 1


# ---------------------------------------------------------------------------
# Plumbing: the flag has to survive the documented path,
# KubeRayClusterBuilder -> KubeRayConfig -> define_cluster() -> to_ray_cluster().
# A flag only reachable on RayCluster is useless to anyone using db.context().
# ---------------------------------------------------------------------------

import json  # noqa: E402

from geneva.cluster.builder import KubeRayClusterBuilder  # noqa: E402
from geneva.cluster.mgr import GenevaCluster  # noqa: E402


def _cluster(require: bool | None) -> GenevaCluster:
    builder = (
        GenevaCluster.create_kuberay("plumbing")
        .namespace("geneva")
        .head_group(cpus=2, memory="4Gi")
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker().name("cpu").cpus(1).memory("2Gi").build()
        )
    )
    if require is not None:
        builder = builder.require_cloud_identity(require)
    return builder.build()


def test_builder_defaults_to_requiring_cloud_identity() -> None:
    assert _cluster(None).kuberay.require_cloud_identity is True


@pytest.mark.parametrize("require", [True, False])
def test_flag_reaches_the_raycluster(require: bool) -> None:
    cluster = _cluster(require)
    assert cluster.kuberay.require_cloud_identity is require
    assert cluster.to_ray_cluster().require_cloud_identity is require


@pytest.mark.parametrize("require", [True, False])
def test_flag_survives_serialisation(require: bool) -> None:
    """define_cluster() persists the config as JSON and db.context() structures
    it back, so the flag must round-trip."""
    cluster = _cluster(require)
    persisted = json.loads(json.dumps(cluster.as_dict()["kuberay"], default=str))
    assert persisted["require_cloud_identity"] is require
