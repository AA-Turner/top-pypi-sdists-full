from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pytest

from geneva.cluster import GenevaCluster
from geneva.manifest import GenevaManifest


class DummyClusterDef:
    def __init__(self, cluster_type: Any, use_portforwarding: bool = True) -> None:
        self.cluster_type = cluster_type
        self._use_portforwarding = use_portforwarding

    def as_dict(self) -> dict[str, Any]:
        return {"kuberay": {"use_portforwarding": self._use_portforwarding}}

    def to_ray_cluster(self) -> Any:
        # Return a dummy RayCluster object to capture on_exit attribute
        return type("RC", (), {})()


class DummyManifestDef:
    @property
    def head_image(self) -> str | None:
        return None

    @property
    def worker_image(self) -> str | None:
        return None


@pytest.fixture
def patch_dependencies(monkeypatch: Any) -> dict[str, Any]:
    # Patch ray_cluster and prevent real manager initialization
    import geneva.cluster.mgr as cluster_mgr_mod
    import geneva.manifest.mgr as manifest_mgr_mod
    import geneva.runners.ray._mgr as ray_mgr_mod

    called = {}

    @contextmanager
    def dummy_ray_cluster(**kwargs: Any) -> Generator[str, None, None]:
        called.update(kwargs)
        yield "ctx"

    # Patch ray_cluster in the module where it's defined
    monkeypatch.setattr(ray_mgr_mod, "ray_cluster", dummy_ray_cluster)
    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager,
        "__init__",
        lambda self, db, namespace=None: None,
    )
    monkeypatch.setattr(
        manifest_mgr_mod.ManifestConfigManager,
        "__init__",
        lambda self, db, table_name=None, namespace=None: None,
    )
    return called


def test_ray_cluster_local(monkeypatch: Any) -> None:
    # Import modules inside function to avoid import errors at module level
    import geneva.packager.autodetect as autodetect_mod
    import geneva.runners.ray._mgr as ray_mgr_mod

    # local=True should skip upload and call init_ray with empty zips
    called = {}

    @contextmanager
    def dummy_init_ray(*args: Any, **kwargs: Any) -> Generator[None, None, None]:
        called["init"] = kwargs.copy()
        yield

    @contextmanager
    def dummy_upload_local_env(
        *args: Any, **kwargs: Any
    ) -> Generator[list[list[str]], None, None]:
        called["upload"] = True
        yield [["dummy.zip"]]

    # Mock the functions in ray_mgr_mod where they are used
    monkeypatch.setattr(ray_mgr_mod, "init_ray", dummy_init_ray)
    monkeypatch.setattr(ray_mgr_mod, "upload_local_env", dummy_upload_local_env)
    monkeypatch.setattr(autodetect_mod, "upload_local_env", dummy_upload_local_env)

    # Also mock ray.init and ray.shutdown to prevent actual Ray operations
    monkeypatch.setattr("ray.init", lambda *args, **kwargs: None)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Mock base64 and json to prevent encoding operations
    monkeypatch.setattr("base64.b64encode", lambda x: b"mocked_base64")
    monkeypatch.setattr("json.dumps", lambda x: "mocked_json")

    # invoke local ray cluster
    with ray_mgr_mod.ray_cluster(local=True):
        pass
    # upload_local_env should not be called, init_ray zips should be empty
    assert "upload" not in called
    assert called["init"]["local"] is True
    assert called["init"]["zips"] == []


def test_ray_cluster_new_cluster(monkeypatch: Any) -> None:
    # Import modules inside function to avoid import errors at module level
    import geneva.packager.autodetect as autodetect_mod
    import geneva.runners.ray._mgr as ray_mgr_mod

    # non-local cluster: stub RayCluster and PortForward to capture addr and zips
    called = {}
    dummy_zips = [["a.zip", "b.zip"]]

    @contextmanager
    def dummy_upload_local_env(
        *args: Any, **kwargs: Any
    ) -> Generator[list[list[str]], None, None]:
        called["upload_opts"] = kwargs.copy()
        yield dummy_zips

    @contextmanager
    def dummy_init_ray(*args: Any, **kwargs: Any) -> Generator[None, None, None]:
        called["init"] = kwargs.copy()
        yield

    class DummyRC:
        def __init__(self, **kwargs: Any) -> None:
            called["rc_opts"] = kwargs.copy()
            self.ray_init_kwargs = None  # Mock the ray_init_kwargs attribute
            self.manifest = None  # Mock the manifest attribute
            self.on_exit = None  # Mock the on_exit attribute

        def __enter__(self) -> str:
            return "10.0.0.1"

        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            pass

    @contextmanager
    def dummy_pf(cluster: Any) -> Generator[Any, None, None]:
        class PF:
            local_port = "9999"

        yield PF()

    # Mock the functions and classes in ray_mgr_mod where they are used
    monkeypatch.setattr(ray_mgr_mod, "upload_local_env", dummy_upload_local_env)
    monkeypatch.setattr(ray_mgr_mod, "init_ray", dummy_init_ray)
    monkeypatch.setattr(ray_mgr_mod, "RayCluster", DummyRC)
    monkeypatch.setattr(
        ray_mgr_mod.PortForward, "to_head_node", classmethod(lambda cls, c: dummy_pf(c))
    )
    monkeypatch.setattr(
        ray_mgr_mod.PortForward, "to_ui", classmethod(lambda cls, c: dummy_pf(c))
    )
    monkeypatch.setattr(autodetect_mod, "upload_local_env", dummy_upload_local_env)

    # Also mock ray.init and ray.shutdown to prevent actual Ray operations
    monkeypatch.setattr("ray.init", lambda *args, **kwargs: None)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Mock base64 and json to prevent encoding operations
    monkeypatch.setattr("base64.b64encode", lambda x: b"mocked_base64")
    monkeypatch.setattr("json.dumps", lambda x: "mocked_json")

    with ray_mgr_mod.ray_cluster():
        pass
    # upload_local_env called with default flags
    assert "upload_opts" in called
    # init_ray should be called with computed addr and zips
    assert called["init"]["addr"] == "ray://localhost:9999"
    assert called["init"]["zips"] == dummy_zips


def test_cluster_not_found_error(
    tmp_path: Path, patch_dependencies: dict[str, Any], monkeypatch: Any
) -> None:
    import geneva.cluster.mgr as cluster_mgr_mod
    from geneva import connect

    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager, "load", lambda self, name: None
    )
    conn = connect(tmp_path)
    with (
        pytest.raises(Exception, match="cluster definition 'abc' not found"),
        conn.context(cluster="abc"),
    ):
        pass


def test_manifest_not_found_error(
    tmp_path: Path, patch_dependencies: dict[str, Any], monkeypatch: Any
) -> None:
    import geneva.cluster.mgr as cluster_mgr_mod
    import geneva.manifest.mgr as manifest_mgr_mod
    from geneva import connect
    from geneva.cluster import GenevaClusterType

    dummy_cluster = DummyClusterDef(GenevaClusterType.KUBE_RAY)
    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager, "load", lambda self, name: dummy_cluster
    )
    monkeypatch.setattr(
        manifest_mgr_mod.ManifestConfigManager, "load", lambda self, name: None
    )
    conn = connect(tmp_path)
    with (
        pytest.raises(Exception, match="manifest definition 'm' not found"),
        conn.context(cluster="c", manifest="m"),
    ):
        pass


def test_success_no_manifest(
    tmp_path: Path, patch_dependencies: dict[str, Any], monkeypatch: Any
) -> None:
    import geneva.cluster.mgr as cluster_mgr_mod
    import geneva.manifest.mgr as manifest_mgr_mod
    from geneva import connect
    from geneva.cluster import GenevaClusterType
    from geneva.db import Connection
    from geneva.runners.ray.raycluster import ExitMode

    # Prepare dummy cluster and ray cluster
    rc = type("RC", (), {})()
    dummy_cluster = DummyClusterDef(
        GenevaClusterType.KUBE_RAY, use_portforwarding=False
    )
    dummy_cluster.to_ray_cluster = lambda self=dummy_cluster: rc
    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager, "load", lambda self, name: dummy_cluster
    )
    monkeypatch.setattr(
        manifest_mgr_mod.ManifestConfigManager, "get_table", lambda self: object()
    )
    dummy_uploader = object()
    monkeypatch.setattr(
        Connection, "_default_manifest_uploader", lambda self: dummy_uploader
    )
    conn = connect(tmp_path)
    called = patch_dependencies
    with conn.context(cluster="c") as ctx:
        assert ctx == "ctx"
    # Default on_exit should be DELETE
    assert hasattr(rc, "on_exit")
    assert rc.on_exit == ExitMode.DELETE
    # Verify ray_cluster arguments
    assert called == {
        "extra_env": {
            "RAY_BACKEND_LOG_LEVEL": "info",
            "RAY_LOG_TO_DRIVER": "1",
            "RAY_ENABLE_RECORD_ACTOR_TASK_LOGGING": "0",
            "RAY_RUNTIME_ENV_LOG_TO_DRIVER_ENABLED": "true",
        },
        "log_to_driver": True,
        "logging_level": 20,
        "manifest": None,
        "ray_cluster": rc,
        "uploader": dummy_uploader,
        "use_portforwarding": False,
    }


def test_context_threads_azure_account_from_storage_options(
    tmp_path: Path, patch_dependencies: dict[str, Any], monkeypatch: Any
) -> None:
    import geneva.cluster.mgr as cluster_mgr_mod
    import geneva.manifest.mgr as manifest_mgr_mod
    from geneva import connect
    from geneva.cluster import GenevaClusterType
    from geneva.db import Connection

    rc = type("RC", (), {})()
    dummy_cluster = DummyClusterDef(
        GenevaClusterType.KUBE_RAY, use_portforwarding=False
    )
    dummy_cluster.to_ray_cluster = lambda self=dummy_cluster: rc
    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager, "load", lambda self, name: dummy_cluster
    )
    monkeypatch.setattr(
        manifest_mgr_mod.ManifestConfigManager, "get_table", lambda self: object()
    )
    monkeypatch.setattr(Connection, "_default_manifest_uploader", lambda self: object())
    conn = connect(
        tmp_path,
        storage_options={"account_name": "fromopts", "account_key": "secret"},
    )

    with conn.context(cluster="c"):
        pass

    assert patch_dependencies["extra_env"]["AZURE_STORAGE_ACCOUNT_NAME"] == "fromopts"


def test_success_with_manifest(
    tmp_path: Path, patch_dependencies: dict[str, Any], monkeypatch: Any
) -> None:
    import geneva.cluster.mgr as cluster_mgr_mod
    import geneva.manifest.mgr as manifest_mgr_mod
    from geneva import connect
    from geneva.cluster import GenevaClusterType
    from geneva.manifest.mgr import MANIFEST_TABLE_NAME
    from geneva.runners.ray.raycluster import ExitMode

    rc = type("RC", (), {})()
    dummy_cluster = DummyClusterDef(GenevaClusterType.KUBE_RAY, use_portforwarding=True)
    dummy_cluster.to_ray_cluster = lambda self=dummy_cluster: rc
    dummy_manifest = DummyManifestDef()
    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager, "load", lambda self, name: dummy_cluster
    )
    monkeypatch.setattr(
        manifest_mgr_mod.ManifestConfigManager,
        "load",
        lambda self, name: dummy_manifest,
    )
    conn = connect(tmp_path)
    called = patch_dependencies
    with conn.context(cluster="c", manifest="m", on_exit=ExitMode.RETAIN) as ctx:
        assert ctx == "ctx"
    assert rc.on_exit == ExitMode.RETAIN
    assert called == {
        "extra_env": {
            "RAY_BACKEND_LOG_LEVEL": "info",
            "RAY_LOG_TO_DRIVER": "1",
            "RAY_ENABLE_RECORD_ACTOR_TASK_LOGGING": "0",
            "RAY_RUNTIME_ENV_LOG_TO_DRIVER_ENABLED": "true",
        },
        "log_to_driver": True,
        "logging_level": 20,
        "manifest": dummy_manifest,
        "ray_cluster": rc,
        "use_portforwarding": True,
        "zip_namespace": {
            "impl": "dir",
            "properties": {
                "root": str(tmp_path),
                "manifest_enabled": "true",
            },
            "table_id": ["__system", MANIFEST_TABLE_NAME],
        },
    }


def test_manifest_image_override(
    tmp_path: Path, patch_dependencies: dict[str, Any], monkeypatch: Any
) -> None:
    import geneva.cluster.mgr as cluster_mgr_mod
    import geneva.manifest.mgr as manifest_mgr_mod
    from geneva import connect

    gc = GenevaCluster.create_kuberay("c").build()
    rc = gc.to_ray_cluster()
    manifest = (
        GenevaManifest.create_site("m")
        .head_image("head-image")
        .worker_image("worker-image")
        .build()
    )
    monkeypatch.setattr(
        cluster_mgr_mod.ClusterConfigManager, "load", lambda self, name: gc
    )
    monkeypatch.setattr(
        manifest_mgr_mod.ManifestConfigManager,
        "load",
        lambda self, name: manifest,
    )
    conn = connect(tmp_path)
    called = patch_dependencies
    with conn.context(cluster="c", manifest="m") as ctx:
        assert ctx == "ctx"

    # assert the cluster images are set to the manifest images
    rc.head_group.image = "head-image"
    for wg in rc.worker_groups:
        wg.image = "worker-image"
    assert called["ray_cluster"] == rc
