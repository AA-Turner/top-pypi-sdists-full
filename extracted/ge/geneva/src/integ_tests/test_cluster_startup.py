# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import importlib
import logging
import site
import subprocess
import sys
from contextlib import AbstractContextManager, suppress
from pathlib import Path

import pytest
import ray

import geneva
from geneva.cluster import GenevaCluster, GenevaClusterType, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder, default_image
from geneva.cluster.mgr import (
    HeadGroupConfig,
    KubeRayConfig,
    WorkerGroupConfig,
)
from geneva.constants import DEFAULT_K8S_NS
from geneva.manifest import GenevaManifest
from geneva.runners.kuberay.client import KuberayClients
from geneva.runners.ray._mgr import _force_ray_cleanup, ray_cluster
from geneva.runners.ray.raycluster import (
    CPU_ONLY_NODE,
    RayCluster,
    _HeadGroupSpec,
    _WorkerGroupSpec,
)
from geneva.utils import dt_now_utc
from integ_tests.utils import ray_get_with_retry

logging.basicConfig(level=logging.INFO)
_LOG = logging.getLogger(__name__)

# Package/version used to verify manifest dependency resolution
_NUMPY_VERSION = "1.26.4"


@ray.remote
def _get_numpy_version() -> str:
    import numpy

    return numpy.__version__


@pytest.fixture
def reset_ray() -> None:
    # kill any lingering ray connections
    # in azure tests specifically, there may be a race condition that can
    # manifest as errors:
    # "ValueError: The client has already connected to the cluster
    # with allow_multiple=True. Please set allow_multiple=True to proceed"
    _force_ray_cleanup()


def test_kube_auth(
    geneva_test_bucket: str,
    k8s_config_method: K8sConfigMethod,
    k8s_cluster_name: str,
    region: str,
    reset_ray,
) -> None:
    geneva.connect(geneva_test_bucket)
    clients = KuberayClients(
        config_method=k8s_config_method,
        region=region,
        role_name="geneva-client-role",
        cluster_name=k8s_cluster_name,
    )
    clients.core_api.list_namespaced_pod(DEFAULT_K8S_NS)


def test_cluster_startup(
    head_node_selector: dict,
    worker_node_selector: dict,
    slug: str | None,
    geneva_test_bucket: str,
    k8s_config_method: K8sConfigMethod,
    k8s_cluster_name: str,
    region: str,
    default_manifest: GenevaManifest,
    reset_ray,
) -> None:
    geneva.connect(geneva_test_bucket)
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    with ray_cluster(
        name=cluster_name,
        manifest=default_manifest,
        namespace=DEFAULT_K8S_NS,
        head_group=_HeadGroupSpec(
            node_selector=head_node_selector,
            image=default_manifest.head_image,
        ),  # type: ignore[call-arg]
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="worker",
                min_replicas=1,
                node_selector=worker_node_selector,
                image=default_manifest.worker_image,
            )
        ],
        use_portforwarding=True,
        skip_site_packages=True,
        config_method=k8s_config_method,
        region=region,
        cluster_name=k8s_cluster_name,
    ):
        ray_get_with_retry(ray.remote(lambda: 1).remote())


@ray.remote
def _get_env_var(name: str) -> str:
    import os

    return os.environ.get(name, "")


@ray.remote
def _module_importable(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def test_ray_init_kwargs_env_var_on_worker(
    session_context: AbstractContextManager,
) -> None:
    """Ensure that values passed to KubeRayClusterBuilder.ray_init_kwargs(env_vars=...)
    do get passed through to Ray runtime_env and are available on workers.
    (here configured via standard_cluster fixture)"""
    value = ray_get_with_retry(_get_env_var.remote("GENEVA_WORKER_ENV_VAR"))
    assert value == "geneva_worker_env_var_value"


@pytest.mark.skip(
    "This test requires configmaps:create/delete RBAC permissions. "
    "We don't grant these permissions to client roles by default in "
    "managed environments"
)
def test_cluster_startup_config_map(
    cluster_from_config_map: RayCluster,
    slug: str | None,
    geneva_test_bucket: str,
    default_manifest: GenevaManifest,
) -> None:
    """Test cluster startup from a Kubernetes ConfigMap.

    This test takes ~10 minutes because it creates its own Ray cluster
    (not a shared session cluster):
    - Cluster startup: ~3-4 min (K8s pod scheduling, image pull, Ray init)
    - Test execution: ~1 min
    - Cluster teardown: ~1-2 min
    """
    geneva.connect(geneva_test_bucket)
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    with ray_cluster(ray_cluster=cluster_from_config_map, manifest=default_manifest):
        res = ray_get_with_retry(ray.remote(lambda: __import__("sys").version).remote())
        _LOG.info(f"***done {res=}")


def test_eks_token_refresh(
    geneva_test_bucket: str,
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    default_manifest: GenevaManifest,
    monkeypatch,
    reset_ray,
) -> None:
    geneva.connect(geneva_test_bucket)
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"
    monkeypatch.setattr(
        "geneva.eks.TOKEN_EXPIRATION_S",
        5,
    )
    img = default_image(arm=False)
    cluster = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region)
        .head_group(
            image=img,
            node_selector=head_node_selector,
            service_account=geneva_k8s_service_account,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .image(img)
            .node_selector(worker_node_selector)
            .service_account(geneva_k8s_service_account)
            .build()
        )
        .build()
    )

    try:
        with ray_cluster(
            ray_cluster=cluster.to_ray_cluster(), manifest=default_manifest
        ):
            res = ray_get_with_retry(
                ray.remote(lambda: __import__("sys").version).remote()
            )
            _LOG.info(f"***done {res=}")
    finally:
        monkeypatch.setattr(
            "geneva.eks.TOKEN_EXPIRATION_S",
            1800,
        )


def test_cluster_startup_persisted_with_context(
    geneva_test_bucket: str,
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    reset_ray,
) -> None:
    db = geneva.connect(geneva_test_bucket)

    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"
    manifest_name = f"test-manifest-{slug}"

    tolerations = [
        {
            "key": "test_toleration",
            "operator": "Exists",
            "effect": "NoExecute",
        },
    ]
    img = default_image(arm=False)

    cluster_def = GenevaCluster(
        name=cluster_name,
        cluster_type=GenevaClusterType.KUBE_RAY,
        kuberay=KubeRayConfig(
            namespace=k8s_namespace,
            config_method=k8s_config_method,
            aws_region=region,
            aws_role_name="geneva-client-role",
            use_portforwarding=True,
            head_group=HeadGroupConfig(
                image=img,
                service_account=geneva_k8s_service_account,
                num_cpus=4,
                memory="8Gi",
                node_selector=head_node_selector,
                labels={"foo": "bar", "baz": "fu"},
                tolerations=tolerations,
            ),
            worker_groups=[
                WorkerGroupConfig(
                    image=img,
                    service_account=geneva_k8s_service_account,
                    num_cpus=4,
                    memory="8Gi",
                    node_selector=worker_node_selector,
                    labels={"foo": "bar"},
                    tolerations=tolerations,
                ),
                WorkerGroupConfig(
                    image=img,
                    service_account=geneva_k8s_service_account,
                    num_cpus=4,
                    memory="8Gi",
                    node_selector=worker_node_selector,
                    labels={"foo": "bar"},
                    tolerations=tolerations,
                ),
            ],
        ),
    )
    _LOG.info(f"{cluster_def=}")

    try:
        # persist the cluster definition
        db.define_cluster(cluster_name, cluster_def)

        clusters = db.list_clusters()
        _LOG.info(f"clusters: {clusters}")
        assert any(c.name == cluster_name for c in clusters), (
            f"couldn't find cluster {cluster_name}"
        )

        # load the cluster def and provision the ray cluster
        success = False
        with db.context(cluster=cluster_name):
            res = ray_get_with_retry(
                ray.remote(lambda: __import__("sys").version).remote()
            )
            _LOG.info(f"***done {res=}")
            success = True
        assert success, f"cluster {cluster_name} was not started successfully"

        # run with a custom manifest
        success = False
        db.define_manifest(
            manifest_name,
            GenevaManifest(
                manifest_name,
                head_image=img,
                worker_image=img,
                delete_local_zips=True,
                skip_site_packages=True,
                pip=["lancedb"],
                py_modules=["./"],
            ),
        )
        with db.context(cluster=cluster_name, manifest=manifest_name):
            res = ray_get_with_retry(
                ray.remote(lambda: __import__("sys").version).remote()
            )
            _LOG.info(f"***done {res=}")
            success = True

        assert success, f"cluster {cluster_name} was not started successfully"
    finally:
        db.delete_cluster(cluster_name)
        db.delete_manifest(manifest_name)


def test_cluster_startup_from_builder(
    geneva_test_bucket: str,
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    default_manifest: GenevaManifest,
    session_manifest: str,
    reset_ray,
) -> None:
    geneva.connect(geneva_test_bucket)
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    img = default_image(arm=False)
    cluster = (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region)
        .head_group(
            image=img,
            node_selector=head_node_selector,
            service_account=geneva_k8s_service_account,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .image(img)
            .node_selector(worker_node_selector)
            .service_account(geneva_k8s_service_account)
            .build()
        )
        .build()
    )

    res = None
    with ray_cluster(ray_cluster=cluster.to_ray_cluster(), manifest=default_manifest):
        res = ray_get_with_retry(ray.remote(lambda: __import__("sys").version).remote())
        _LOG.info(f"{res=}")
    assert res, f"cluster {cluster_name} was not started successfully"


def test_cluster_startup_no_account(
    k8s_config_method: K8sConfigMethod,
    head_node_selector: dict,
    worker_node_selector: dict,
    slug: str | None,
    default_manifest: GenevaManifest,
    session_manifest: str,
    reset_ray,
) -> None:
    """
    Test the if we try to import geneva, which uses gcs for
    workspace packaging magic, errors when the service account
    doesn't have permission to access the gcs bucket.
    """

    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    with (
        pytest.raises(ValueError, match=r"Service account .* does not exist"),
        ray_cluster(
            name=cluster_name,
            manifest=default_manifest,
            namespace=DEFAULT_K8S_NS,
            config_method=k8s_config_method,
            use_portforwarding=True,
            skip_site_packages=True,
            head_group=_HeadGroupSpec(
                node_selector=head_node_selector,
                image=default_image(arm=False),
            ),  # type: ignore[call-arg]
            # allocate at least a single worker so the test runs faster
            # that we save time on waiting for the actor to start
            worker_groups=[
                _WorkerGroupSpec(  # type: ignore[call-arg]
                    name="worker",
                    min_replicas=1,
                    service_account="bogus-service-account",
                    node_selector=worker_node_selector,
                    image=default_image(arm=False),
                )
            ],
        ),
    ):
        ray.get(ray.remote(lambda: importlib.import_module("geneva")).remote())


@pytest.mark.skip("Need to create a service account with no permissions")
def test_cluster_startup_no_gcs_permission(
    k8s_config_method: K8sConfigMethod,
    head_node_selector: dict,
    worker_node_selector: dict,
    slug: str | None,
    reset_ray,
) -> None:
    """
    Test the if we try to import geneva, which uses gcs for
    workspace packaging magic, errors when the service account
    doesn't have permission to access the gcs bucket.
    """

    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    with (
        ray_cluster(
            name=cluster_name,
            namespace=DEFAULT_K8S_NS,
            config_method=k8s_config_method,
            use_portforwarding=True,
            skip_site_packages=True,
            # allocate at least a single worker so the test runs faster
            # that we save time on waiting for the actor to start
            head_group=_HeadGroupSpec(
                node_selector=head_node_selector,
                image=default_image(arm=False),
            ),  # type: ignore[call-arg]
            worker_groups=[
                _WorkerGroupSpec(  # type: ignore[call-arg]
                    name="worker",
                    min_replicas=1,
                    service_account="valid-no-perms-service-account",
                    node_selector=worker_node_selector,
                    image=default_image(arm=False),
                )
            ],
        ),
        pytest.raises(PermissionError, match="PERMISSION_DENIED"),
    ):
        ray.get(ray.remote(lambda: importlib.import_module("geneva")).remote())


def test_cluster_startup_can_import_geneva_and_lance(
    geneva_k8s_service_account: str,
    geneva_test_bucket: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_config_method: K8sConfigMethod,
    k8s_cluster_name: str,
    region: str,
    slug: str | None,
    session_manifest: str,
    reset_ray,
) -> None:
    from geneva.manifest.mgr import ManifestConfigManager

    # Connect to bucket and load manifest object
    db = geneva.connect(geneva_test_bucket)
    manifest_mgr = ManifestConfigManager(db)
    manifest_def = manifest_mgr.load(session_manifest)

    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    with ray_cluster(
        name=cluster_name,
        namespace=DEFAULT_K8S_NS,
        use_portforwarding=True,
        skip_site_packages=True,
        manifest=manifest_def,
        head_group=_HeadGroupSpec(  # type: ignore[call-arg]
            service_account=geneva_k8s_service_account,
            node_selector=head_node_selector,
            image=default_image(arm=False),
        ),
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="worker",
                min_replicas=1,
                service_account=geneva_k8s_service_account,
                node_selector=worker_node_selector,
                image=default_image(arm=False),
            )
        ],
        config_method=k8s_config_method,
        region=region,
        cluster_name=k8s_cluster_name,
    ):
        ray_get_with_retry(
            ray.remote(lambda: importlib.import_module("geneva")).remote()
        )
        ray_get_with_retry(
            ray.remote(lambda: importlib.import_module("lance")).remote()
        )


def test_cluster_startup_skip_site(
    geneva_k8s_service_account: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_config_method: K8sConfigMethod,
    k8s_cluster_name: str,
    region: str,
    slug: str | None,
    default_manifest: GenevaManifest,
    session_manifest: str,
    reset_ray,
) -> None:
    """Test that skip_site_packages=True prevents local site-package files from
    being shipped to ray workers."""
    module_name = "_geneva_integ_test_skip_site_canary"
    site_packages_dir = Path(site.getsitepackages()[0])
    dummy_file = site_packages_dir / f"{module_name}.py"
    dummy_file.write_text("VALUE = 42\n")
    importlib.invalidate_caches()

    try:
        assert importlib.import_module(module_name).VALUE == 42

        cluster_name = "geneva-integ-test"
        cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

        with ray_cluster(
            name=cluster_name,
            namespace=DEFAULT_K8S_NS,
            use_portforwarding=True,
            head_group=_HeadGroupSpec(  # type: ignore[call-arg]
                service_account=geneva_k8s_service_account,
                node_selector=head_node_selector,
                image=default_image(arm=False),
            ),
            worker_groups=[
                _WorkerGroupSpec(  # type: ignore[call-arg]
                    name="worker",
                    min_replicas=1,
                    service_account=geneva_k8s_service_account,
                    node_selector=worker_node_selector,
                    image=default_image(arm=False),
                )
            ],
            skip_site_packages=True,
            config_method=k8s_config_method,
            region=region,
            cluster_name=k8s_cluster_name,
            manifest=default_manifest,
        ):
            assert not ray_get_with_retry(_module_importable.remote(module_name))
    finally:
        dummy_file.unlink(missing_ok=True)
        sys.modules.pop(module_name, None)
        importlib.invalidate_caches()


# GPU test routing: this test provisions GPU worker nodes and requires
# nvidia-smi.  It is excluded from GCP/AWS CI (where GPU node spin-up
# contention causes flaky timeouts) and runs only on Azure, which has
# always-on GPU nodes.  See GEN-439 for the full cross-cloud strategy.
@pytest.mark.gpu
def test_cluster_startup_cpu_only_tag_with_cpu_gpu_workers(
    geneva_k8s_service_account: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_config_method: K8sConfigMethod,
    k8s_cluster_name: str,
    region: str,
    slug: str | None,
    default_manifest: GenevaManifest,
    session_context,
    reset_ray,
) -> None:
    """
    Test that if we force a CPU only task, it runs only on a CPU worker.

    If we request a GPU worker, it can run GPU worker, if we don't request a GPU worker
    without the cpu-only tag, it can be scheduled to runs on either a CPU or GPU worker.

    Oftentimes GPU workers fail to provision so we let the test pass in this case.
    """

    cluster_name = "cluster-startup-cpu-only-tag"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    with ray_cluster(
        name=cluster_name,
        namespace=DEFAULT_K8S_NS,
        use_portforwarding=True,
        skip_site_packages=True,
        manifest=default_manifest,
        head_group=_HeadGroupSpec(  # type: ignore[call-arg]
            service_account=geneva_k8s_service_account,
            node_selector=head_node_selector,
            image=default_image(arm=False),
        ),
        # allocate both GPU and CPU workers
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="cpu",
                min_replicas=0,
                service_account=geneva_k8s_service_account,
                node_selector=worker_node_selector,
                image=default_image(arm=False),
            ),
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="gpu",
                min_replicas=1,
                service_account=geneva_k8s_service_account,
                num_gpus=1,
                node_selector={"geneva.lancedb.com/ray-worker-gpu": "true"},
                image=default_image(arm=False, gpu=True),
            ),
        ],
        config_method=k8s_config_method,
        region=region,
        cluster_name=k8s_cluster_name,
    ):
        try:
            ray.get(
                ray.remote(num_gpus=1)(
                    lambda: subprocess.run("nvidia-smi", check=True)
                ).remote(),
                timeout=300,
            )
        except ray.exceptions.GetTimeoutError as e:
            _LOG.info(e)
            pytest.skip(
                "Skipping test due to Ray cluster startup failure "
                "(likely cannot provision GPU node)"
            )

        # running a CPU only task but we have a GPU worker
        # should schedule on the GPU worker but may schedule on CPU
        with suppress(ray.exceptions.RayTaskError, ray.exceptions.GetTimeoutError):
            ray_get_with_retry(
                ray.remote(lambda: subprocess.run("nvidia-smi", check=True)).remote()
            )

        # running a CPU only task + force it to run on CPU
        # should only schedule on the CPU worker and should always raise exception
        with pytest.raises(
            ray.exceptions.RayTaskError,
            match="No such file or directory: 'nvidia-smi'",
        ):
            ray.get(
                ray.remote(resources={CPU_ONLY_NODE: 1})(
                    lambda: subprocess.run("nvidia-smi", check=True)
                ).remote()
            )


def _cluster_for_manifest_tests(
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
) -> GenevaCluster:
    """Build a cluster for manifest resolution tests (same pattern as
    test_cluster_startup_from_builder)."""
    cluster_name = "geneva-integ-test"
    cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"
    img = default_image(arm=False)
    return (
        GenevaCluster.create_kuberay(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region)
        .head_group(
            image=img,
            node_selector=head_node_selector,
            service_account=geneva_k8s_service_account,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .image(img)
            .node_selector(worker_node_selector)
            .service_account(geneva_k8s_service_account)
            .build()
        )
        .build()
    )


def test_manifest_requirements_path(
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    tmp_path,
    reset_ray,
) -> None:
    """Verify manifest with requirements_path resolves and installs on workers."""
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text(f"numpy=={_NUMPY_VERSION}\n")

    manifest = (
        GenevaManifest.create_pip("manifest-req-path")
        # Integ tests assume x86 cluster (see integ_tests/conftest default_manifest)
        .head_image(default_image(arm=False))
        .worker_image(default_image(arm=False))
        .requirements_path(str(requirements_file))
        .build()
    )

    cluster = _cluster_for_manifest_tests(
        slug,
        geneva_k8s_service_account,
        k8s_namespace,
        head_node_selector,
        worker_node_selector,
        region,
        k8s_config_method,
    )
    with ray_cluster(
        ray_cluster=cluster.to_ray_cluster(),
        manifest=manifest,
    ):
        version = ray_get_with_retry(_get_numpy_version.remote())
        assert version == _NUMPY_VERSION, (
            f"expected numpy=={_NUMPY_VERSION}, got {version}"
        )


def test_manifest_conda(
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    reset_ray,
) -> None:
    """Verify manifest with conda dependencies resolves and installs on workers."""
    manifest = (
        GenevaManifest.create_conda("manifest-conda")
        # Integ tests assume x86 cluster
        .head_image(default_image(arm=False))
        .worker_image(default_image(arm=False))
        .conda({"dependencies": ["pip", {"pip": [f"numpy=={_NUMPY_VERSION}"]}]})
        .build()
    )

    cluster = _cluster_for_manifest_tests(
        slug,
        geneva_k8s_service_account,
        k8s_namespace,
        head_node_selector,
        worker_node_selector,
        region,
        k8s_config_method,
    )
    with ray_cluster(
        ray_cluster=cluster.to_ray_cluster(),
        manifest=manifest,
    ):
        version = ray_get_with_retry(_get_numpy_version.remote())
        assert version == _NUMPY_VERSION, (
            f"expected numpy=={_NUMPY_VERSION}, got {version}"
        )


@pytest.mark.skip(
    reason=(
        "covered by manifest/runtime_env unit tests; keep one remote conda smoke "
        "via test_manifest_conda"
    )
)
def test_manifest_conda_environment_path(
    slug: str | None,
    geneva_k8s_service_account: str,
    k8s_namespace: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    region: str,
    k8s_config_method: K8sConfigMethod,
    tmp_path,
    reset_ray,
) -> None:
    """Verify manifest with conda_environment_path resolves and installs on workers."""
    env_yml = tmp_path / "environment.yml"
    env_yml.write_text(
        f"""name: test-env
dependencies:
  - pip
  - pip:
    - numpy=={_NUMPY_VERSION}
"""
    )

    manifest = (
        GenevaManifest.create_conda("manifest-conda-env")
        # Integ tests assume x86 cluster
        .head_image(default_image(arm=False))
        .worker_image(default_image(arm=False))
        .conda_environment_path(str(env_yml))
        .build()
    )

    cluster = _cluster_for_manifest_tests(
        slug,
        geneva_k8s_service_account,
        k8s_namespace,
        head_node_selector,
        worker_node_selector,
        region,
        k8s_config_method,
    )
    with ray_cluster(
        ray_cluster=cluster.to_ray_cluster(),
        manifest=manifest,
    ):
        version = ray_get_with_retry(_get_numpy_version.remote())
        assert version == _NUMPY_VERSION, (
            f"expected numpy=={_NUMPY_VERSION}, got {version}"
        )
