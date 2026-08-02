# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import copy
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from geneva import DEFAULT_UPLOAD_DIR, connect
from geneva.cluster.builder import default_image
from geneva.manifest import GenevaManifest
from geneva.manifest.builder import (
    CondaManifestBuilder,
    PipManifestBuilder,
    SiteManifestBuilder,
)


@pytest.mark.slow
def test_manifest_upload_location_namespace(tmp_path: Path) -> None:
    """Test manifest zips uploaded to correct location for namespace connections."""
    import pyarrow.fs as pafs
    from lance_namespace import DescribeTableRequest

    # Create a directory namespace connection with a system namespace
    system_ns = "test_system"
    db_root = tmp_path / "db"
    db_root.mkdir()

    # Create zip output directory
    zip_dir = tmp_path / "zips"
    zip_dir.mkdir()

    geneva = connect(
        namespace_client_impl="dir",
        namespace_client_properties={"root": str(db_root)},
        system_namespace=[system_ns],
    )

    manifest_def = GenevaManifest(
        name="test-manifest",
        local_zip_output_dir=str(zip_dir),
        skip_site_packages=True,  # Skip to make test faster
        delete_local_zips=False,
        pip=["numpy"],
    )

    # Define the manifest (this should upload zips)
    geneva.define_manifest("test-manifest", manifest_def)

    # Verify the manifest was created and has zips
    manifests = geneva.list_manifests()
    assert len(manifests) == 1
    manifest = manifests[0]
    assert len(manifest.zips) > 0, "Expected manifest to have uploaded zips"

    # Get the manifest table location from namespace
    assert geneva.namespace_client() is not None
    from geneva.manifest.mgr import MANIFEST_TABLE_NAME

    table_id = [system_ns, MANIFEST_TABLE_NAME]
    response = geneva.namespace_client().describe_table(
        DescribeTableRequest(id=table_id)
    )
    manifest_table_location = response.location
    assert manifest_table_location is not None

    # Expected upload directory should be {manifest_table_location}/_geneva_uploads
    expected_upload_dir = f"{manifest_table_location.rstrip('/')}/{DEFAULT_UPLOAD_DIR}"

    # Verify that all uploaded zips are in the expected location
    for zip_path_list in manifest.zips:
        for zip_path in zip_path_list:
            # The zip path should start with the expected upload directory
            assert zip_path.startswith(expected_upload_dir), (
                f"Expected zip to be uploaded to {expected_upload_dir}, "
                f"but got {zip_path}"
            )

            # Verify the file actually exists at that location
            filesystem, path = pafs.FileSystem.from_uri(zip_path)
            file_info = filesystem.get_file_info(path)
            assert file_info.type == pafs.FileType.File, (
                f"Expected file to exist at {zip_path}"
            )


@pytest.mark.slow
def test_manifest_upload_location_local(tmp_path: Path) -> None:
    """Test manifest zips uploaded to correct location for local connections."""
    import pyarrow.fs as pafs
    from lance_namespace import DescribeTableRequest

    # Create a local connection
    db_path = tmp_path / "db"

    # Create zip output directory
    zip_dir = tmp_path / "zips"
    zip_dir.mkdir()

    geneva = connect(db_path)

    manifest_def = GenevaManifest(
        name="test-manifest",
        local_zip_output_dir=str(tmp_path / "zips"),
        skip_site_packages=True,  # Skip to make test faster
        delete_local_zips=False,
        pip=["numpy"],
    )

    # Define the manifest (this should upload zips)
    geneva.define_manifest("test-manifest", manifest_def)

    # Verify the manifest was created and has zips
    manifests = geneva.list_manifests()
    assert len(manifests) == 1
    manifest = manifests[0]
    assert len(manifest.zips) > 0, "Expected manifest to have uploaded zips"

    from geneva.manifest.mgr import MANIFEST_TABLE_NAME

    response = geneva.namespace_client().describe_table(
        DescribeTableRequest(id=["__system", MANIFEST_TABLE_NAME])
    )
    manifest_table_location = response.location
    assert manifest_table_location is not None

    expected_upload_dir = f"{manifest_table_location.rstrip('/')}/{DEFAULT_UPLOAD_DIR}"

    # Verify that all uploaded zips are in the expected location
    for zip_path_list in manifest.zips:
        for zip_path in zip_path_list:
            # The zip path should start with the expected upload directory
            assert zip_path.startswith(expected_upload_dir), (
                f"Expected zip to be uploaded to {expected_upload_dir}, "
                f"but got {zip_path}"
            )

            # Verify the file actually exists at that location
            filesystem, path = pafs.FileSystem.from_uri(zip_path)
            file_info = filesystem.get_file_info(path)
            assert file_info.type == pafs.FileType.File, (
                f"Expected file to exist at {zip_path}"
            )


@pytest.mark.slow
def test_manifest_crud(tmp_path: Path) -> None:
    mock_uploader = MagicMock()
    mock_uploader.upload_dir = "/mock/upload/dir"
    mock_uploader._file_exists.return_value = False
    mock_uploader.upload.side_effect = lambda path: f"mock://{path.name}"

    geneva = connect(tmp_path)

    manifest_def = GenevaManifest(
        name="test-manifest-1",
        local_zip_output_dir=str(tmp_path),
        skip_site_packages=False,
        delete_local_zips=False,
        pip=["numpy", "pandas"],
        py_modules=["pyarrow"],
    )

    # upload and create
    geneva.define_manifest("test-manifest-1", manifest_def, uploader=mock_uploader)
    m = geneva.list_manifests()[0]
    _assert_manifest_eq(m.as_dict(), manifest_def.as_dict())

    upload_count = mock_uploader.upload.call_count
    assert upload_count >= 1, "files were not uploaded"

    # update - should update metadata and upload new artifacts
    manifest_def.skip_site_packages = True
    geneva.define_manifest("test-manifest-1", manifest_def, uploader=mock_uploader)
    manifests = geneva.list_manifests()
    assert len(manifests) == 1, "expected single manifest"
    m1 = manifests[0].as_dict()
    m2 = manifest_def.as_dict()
    assert m1["checksum"] != m2["checksum"], "checksum should change"
    _assert_manifest_eq(m1, m2)
    assert mock_uploader.upload.call_count >= upload_count, "files were not uploaded"

    # delete
    geneva.delete_manifest("test-manifest-1")
    assert geneva.list_manifests() == []


def _assert_manifest_eq(m1: dict, m2: dict) -> bool:
    m1 = copy.deepcopy(m1)
    m2 = copy.deepcopy(m2)
    # exclude transient fields from comparison
    for f in {"checksum", "zips"}:
        if f in m1:
            del m1[f]
        if f in m2:
            del m2[f]
    assert m1 == m2, "manifests should match"


def test_manifest_conda_passed_to_ray(monkeypatch: Any) -> None:
    """Test that conda dependencies from manifest are passed to Ray runtime_env."""
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Use a realistic conda structure with nested dependencies
    conda_deps = {
        "dependencies": [
            "python=3.8",
            "pip",
            {"pip": ["requests", "chess"]},
        ],
        "channels": ["conda-forge"],
    }

    manifest = CondaManifestBuilder.create("conda-manifest").conda(conda_deps).build()

    with ray_mgr_mod.ray_cluster(local=True, manifest=manifest):
        pass

    assert "kwargs" in ray_init_called
    runtime_env = ray_init_called["kwargs"]["runtime_env"]
    assert "conda" in runtime_env
    assert runtime_env["conda"] == conda_deps
    assert "pip" not in runtime_env


def test_manifest_requirements_path_not_passed_to_local_ray(
    monkeypatch: Any, tmp_path: Path
) -> None:
    """Local ray_cluster does not install requirements_path via pip — workers share
    the driver's environment. Worker env setup (env_vars) still happens."""
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    req_file = tmp_path / "requirements.txt"
    req_file.write_text("numpy>=1.0\npandas\n")
    req_path = str(req_file)

    manifest = (
        PipManifestBuilder.create("req-manifest").requirements_path(req_path).build()
    )

    with ray_mgr_mod.ray_cluster(local=True, manifest=manifest):
        pass

    assert "kwargs" in ray_init_called
    runtime_env = ray_init_called["kwargs"]["runtime_env"]
    # pip/conda not set for local mode — workers share the driver's environment
    assert "pip" not in runtime_env
    assert "conda" not in runtime_env
    # Worker env setup still happens: GENEVA_ZIPS tells workers where to find code
    assert "env_vars" in runtime_env
    assert "GENEVA_ZIPS" in runtime_env["env_vars"]
    assert "PIP_EXTRA_INDEX_URL" in runtime_env["env_vars"]


def test_manifest_conda_environment_path_passed_to_ray(
    monkeypatch: Any, tmp_path: Path
) -> None:
    """Test that conda_environment_path from manifest is passed to Ray runtime_env."""
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    env_file = tmp_path / "environment.yml"
    env_file.write_text(
        "name: test-env\n"
        "channels:\n"
        "  - conda-forge\n"
        "dependencies:\n"
        "  - python=3.10\n"
        "  - numpy\n"
    )
    env_path = str(env_file)

    manifest = (
        CondaManifestBuilder.create("conda-env-manifest")
        .conda_environment_path(env_path)
        .build()
    )

    with ray_mgr_mod.ray_cluster(local=True, manifest=manifest):
        pass

    assert "kwargs" in ray_init_called
    runtime_env = ray_init_called["kwargs"]["runtime_env"]
    assert "conda" in runtime_env
    assert runtime_env["conda"] == env_path
    assert "pip" not in runtime_env


def test_make_manifest_conda_none() -> None:
    """Test that _make_manifest handles conda=None from stored data."""
    from datetime import datetime, timezone

    from geneva.manifest.mgr import _make_manifest

    args = {
        "name": "test",
        "version": None,
        "pip": [],
        "py_modules": [],
        "head_image": None,
        "worker_image": None,
        "skip_site_packages": True,
        "delete_local_zips": False,
        "local_zip_output_dir": None,
        "zips": [[]],
        "checksum": None,
        "created_at": datetime.now(timezone.utc),
        "created_by": "test",
        "requirements_path": None,
        "conda": None,
        "conda_environment_path": None,
    }
    manifest = _make_manifest(args)
    assert manifest.conda == {}


# =============================================================================
# Type-Safe Builder Tests
# =============================================================================


class TestPipManifestBuilder:
    """Tests for PipManifestBuilder."""

    def test_no_conda_methods(self) -> None:
        """PipManifestBuilder should not have conda methods."""
        builder = PipManifestBuilder()
        assert not hasattr(builder, "conda")
        assert not hasattr(builder, "conda_environment_path")

    def test_has_pip_methods(self) -> None:
        """PipManifestBuilder should have pip methods."""
        builder = PipManifestBuilder()
        assert hasattr(builder, "pip")
        assert hasattr(builder, "add_pip")
        assert hasattr(builder, "requirements_path")

    def test_pip_packages(self) -> None:
        """Test setting pip packages."""
        manifest = PipManifestBuilder.create("test").pip(["numpy", "pandas"]).build()
        assert manifest.pip == ["numpy", "pandas"]
        assert manifest.conda == {}

    def test_add_pip(self) -> None:
        """Test adding pip packages incrementally."""
        manifest = (
            PipManifestBuilder.create("test").add_pip("numpy").add_pip("pandas").build()
        )
        assert manifest.pip == ["numpy", "pandas"]

    def test_requirements_path(self, tmp_path: Path) -> None:
        """Test using requirements.txt path."""
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("numpy\npandas\n")

        manifest = (
            PipManifestBuilder.create("test").requirements_path(str(req_file)).build()
        )
        assert manifest.requirements_path == str(req_file)
        assert manifest.pip == []

    def test_pip_and_requirements_mutually_exclusive(self) -> None:
        """Test that pip and requirements_path cannot both be set."""
        with pytest.raises(ValueError, match="Cannot set both pip and requirements"):
            PipManifestBuilder.create("test").pip(["numpy"]).requirements_path(
                "/path"
            ).build()

    def test_common_methods(self) -> None:
        """Test that common methods work."""
        manifest = (
            PipManifestBuilder.create("test")
            .version("1.0")
            .py_modules(["mymodule"])
            .head_image("custom:latest")
            .worker_image("worker:latest")
            .upload_site_packages(True)
            .pip(["numpy"])
            .build()
        )
        assert manifest.version == "1.0"
        assert manifest.py_modules == ["mymodule"]
        assert manifest.head_image == "custom:latest"
        assert manifest.worker_image == "worker:latest"
        assert manifest.skip_site_packages is False

    def test_requires_name(self) -> None:
        """Test that builder requires a name."""
        with pytest.raises(ValueError, match="Manifest name is required"):
            PipManifestBuilder().build()


class TestCondaManifestBuilder:
    """Tests for CondaManifestBuilder."""

    def test_no_pip_methods(self) -> None:
        """CondaManifestBuilder should not have pip methods."""
        builder = CondaManifestBuilder()
        assert not hasattr(builder, "pip")
        assert not hasattr(builder, "add_pip")
        assert not hasattr(builder, "requirements_path")

    def test_has_conda_methods(self) -> None:
        """CondaManifestBuilder should have conda methods."""
        builder = CondaManifestBuilder()
        assert hasattr(builder, "conda")
        assert hasattr(builder, "conda_environment_path")

    def test_conda_dependencies(self) -> None:
        """Test setting conda dependencies."""
        conda_deps = {"dependencies": ["python=3.10", "numpy"]}
        manifest = CondaManifestBuilder.create("test").conda(conda_deps).build()
        assert manifest.conda == conda_deps
        assert manifest.pip == []

    def test_conda_environment_path(self, tmp_path: Path) -> None:
        """Test using environment.yml path."""
        env_file = tmp_path / "environment.yml"
        env_file.write_text("name: test\ndependencies:\n  - numpy\n")

        manifest = (
            CondaManifestBuilder.create("test")
            .conda_environment_path(str(env_file))
            .build()
        )
        assert manifest.conda_environment_path == str(env_file)
        assert manifest.conda == {}

    def test_conda_and_path_mutually_exclusive(self) -> None:
        """Test that conda and conda_environment_path cannot both be set."""
        with pytest.raises(ValueError, match="Cannot set both conda and conda_env"):
            CondaManifestBuilder.create("test").conda(
                {"dependencies": ["numpy"]}
            ).conda_environment_path("/path").build()

    def test_common_methods(self) -> None:
        """Test that common methods work."""
        manifest = (
            CondaManifestBuilder.create("test")
            .version("2.0")
            .add_py_module("mymodule")
            .default_head_image()
            .upload_site_packages()
            .conda({"dependencies": ["numpy"]})
            .build()
        )
        assert manifest.version == "2.0"
        assert manifest.py_modules == ["mymodule"]
        assert manifest.head_image == default_image()
        assert manifest.skip_site_packages is False

    def test_requires_name(self) -> None:
        """Test that builder requires a name."""
        with pytest.raises(ValueError, match="Manifest name is required"):
            CondaManifestBuilder().build()


class TestSiteManifestBuilder:
    """Tests for SiteManifestBuilder."""

    def test_no_pip_methods(self) -> None:
        """SiteManifestBuilder should not have pip methods."""
        builder = SiteManifestBuilder()
        assert not hasattr(builder, "pip")
        assert not hasattr(builder, "add_pip")
        assert not hasattr(builder, "requirements_path")

    def test_no_conda_methods(self) -> None:
        """SiteManifestBuilder should not have conda methods."""
        builder = SiteManifestBuilder()
        assert not hasattr(builder, "conda")
        assert not hasattr(builder, "conda_environment_path")

    def test_upload_site_packages_default_true(self) -> None:
        """SiteManifestBuilder should default to uploading site packages."""
        manifest = SiteManifestBuilder.create("test").build()
        assert manifest.skip_site_packages is False  # upload=True means skip=False

    def test_can_disable_site_packages(self) -> None:
        """Test that site packages can be disabled."""
        manifest = (
            SiteManifestBuilder.create("test").upload_site_packages(False).build()
        )
        assert manifest.skip_site_packages is True

    def test_no_external_deps(self) -> None:
        """Test that no external dependencies are set."""
        manifest = SiteManifestBuilder.create("test").build()
        assert manifest.pip == []
        assert manifest.conda == {}
        assert manifest.requirements_path is None
        assert manifest.conda_environment_path is None

    def test_common_methods(self) -> None:
        """Test that common methods work."""
        manifest = (
            SiteManifestBuilder.create("test")
            .version("3.0")
            .py_modules(["local_module"])
            .head_image("site:latest")
            .delete_local_zips(True)
            .build()
        )
        assert manifest.version == "3.0"
        assert manifest.py_modules == ["local_module"]
        assert manifest.head_image == "site:latest"
        assert manifest.delete_local_zips is True

    def test_requires_name(self) -> None:
        """Test that builder requires a name."""
        with pytest.raises(ValueError, match="Manifest name is required"):
            SiteManifestBuilder().build()


class TestGenevaManifestFactories:
    """Tests for GenevaManifest static factory methods."""

    def test_create_pip_factory(self) -> None:
        """GenevaManifest.create_pip() should return PipManifestBuilder."""
        builder = GenevaManifest.create_pip("test")
        assert isinstance(builder, PipManifestBuilder)
        manifest = builder.pip(["numpy"]).build()
        assert manifest.name == "test"
        assert manifest.pip == ["numpy"]

    def test_create_conda_factory(self) -> None:
        """GenevaManifest.create_conda() should return CondaManifestBuilder."""
        builder = GenevaManifest.create_conda("test")
        assert isinstance(builder, CondaManifestBuilder)
        manifest = builder.conda({"dependencies": ["numpy"]}).build()
        assert manifest.name == "test"
        assert manifest.conda == {"dependencies": ["numpy"]}

    def test_create_site_factory(self) -> None:
        """GenevaManifest.create_site() should return SiteManifestBuilder."""
        builder = GenevaManifest.create_site("test")
        assert isinstance(builder, SiteManifestBuilder)
        manifest = builder.build()
        assert manifest.name == "test"
        assert manifest.skip_site_packages is False  # upload enabled by default

    def test_full_workflow_pip(self) -> None:
        """Test complete workflow using pip factory."""
        manifest = (
            GenevaManifest.create_pip("my-pip-manifest")
            .version("1.0.0")
            .pip(["numpy", "pandas"])
            .add_py_module("mymodule")
            .head_image("custom:latest")
            .build()
        )

        assert manifest.name == "my-pip-manifest"
        assert manifest.version == "1.0.0"
        assert manifest.pip == ["numpy", "pandas"]
        assert manifest.py_modules == ["mymodule"]
        assert manifest.head_image == "custom:latest"
        assert manifest.conda == {}

    def test_full_workflow_conda(self) -> None:
        """Test complete workflow using conda factory."""
        conda_deps = {
            "channels": ["conda-forge"],
            "dependencies": ["python=3.10", "numpy", {"pip": ["requests"]}],
        }
        manifest = (
            GenevaManifest.create_conda("my-conda-manifest")
            .conda(conda_deps)
            .upload_site_packages(True)
            .build()
        )

        assert manifest.name == "my-conda-manifest"
        assert manifest.conda == conda_deps
        assert manifest.pip == []
        assert manifest.skip_site_packages is False


class TestCaptureLocalEnvironment:
    """Tests for ``Connection.capture_local_environment()``.

    The method is **eager**: it requires an open Connection and uploads
    the local environment synchronously, returning a fully-resolved
    :class:`GenevaManifest`.
    """

    @staticmethod
    def _stub_upload(monkeypatch: Any) -> dict[str, Any]:
        """Patch upload_local_env to return canned zip URIs and capture
        the kwargs it was called with."""
        captured_kwargs: dict[str, Any] = {}

        class _FakeCtx:
            def __enter__(self) -> list[list[str]]:
                return [
                    ["s3://upload/site_packages.zip"],
                    ["s3://upload/workspace.zip"],
                ]

            def __exit__(self, *_a: Any) -> None:
                return None

        def _fake_upload_local_env(**kwargs: Any) -> _FakeCtx:
            captured_kwargs.update(kwargs)
            return _FakeCtx()

        monkeypatch.setattr(
            "geneva.packager.autodetect.upload_local_env",
            _fake_upload_local_env,
        )
        return captured_kwargs

    @staticmethod
    def _stub_uploader(monkeypatch: Any) -> object:
        """Stub _build_capture_uploader to return a sentinel without
        touching real namespace / file-system infrastructure."""
        from geneva.manifest import mgr as mgr_mod
        from geneva.packager.uploader import Uploader

        sentinel = Uploader.__new__(Uploader)
        monkeypatch.setattr(mgr_mod, "_build_capture_uploader", lambda _conn: sentinel)
        return sentinel

    def test_eager_capture_populates_zips(
        self, tmp_path: Path, monkeypatch: Any
    ) -> None:
        """db.capture_local_environment() uploads zips synchronously and
        returns a manifest with ``zips`` populated."""
        captured_kwargs = self._stub_upload(monkeypatch)
        sentinel_uploader = self._stub_uploader(monkeypatch)

        db = connect(tmp_path)
        m = db.capture_local_environment("my-capture", skip_site_packages=True)

        assert isinstance(m, GenevaManifest)
        assert m.name == "my-capture"
        assert m.skip_site_packages is True
        assert m.zips == [
            ["s3://upload/site_packages.zip"],
            ["s3://upload/workspace.zip"],
        ]
        assert captured_kwargs["uploader"] is sentinel_uploader
        assert captured_kwargs["skip_site_packages"] is True
        assert m.checksum == m.compute_checksum()

    def test_auto_generated_name_when_omitted(
        self, tmp_path: Path, monkeypatch: Any
    ) -> None:
        self._stub_upload(monkeypatch)
        self._stub_uploader(monkeypatch)

        db = connect(tmp_path)
        m = db.capture_local_environment()
        assert m.name.startswith("capture-")
        assert len(m.name) > len("capture-")

    def test_each_call_returns_independent_manifest(
        self, tmp_path: Path, monkeypatch: Any
    ) -> None:
        """No caching — each call yields a fresh manifest with a unique
        auto-generated name."""
        self._stub_upload(monkeypatch)
        self._stub_uploader(monkeypatch)

        db = connect(tmp_path)
        a = db.capture_local_environment()
        b = db.capture_local_environment()
        assert a.name != b.name
        assert a is not b

    def test_raises_when_no_uploader_can_be_built(
        self, tmp_path: Path, monkeypatch: Any
    ) -> None:
        """When the connection can't vend an Uploader, the method
        surfaces a RuntimeError pointing at the alternatives."""
        from geneva.manifest import mgr as mgr_mod

        def _no_uploader(_conn: Any) -> Any:
            raise ValueError("uploader.upload_dir is not configured")

        monkeypatch.setattr(mgr_mod, "_build_capture_uploader", _no_uploader)

        db = connect(tmp_path)
        with pytest.raises(RuntimeError) as excinfo:
            db.capture_local_environment(skip_site_packages=True)
        assert "create_pip" in str(excinfo.value)

    def test_default_skip_site_packages_is_false(
        self, tmp_path: Path, monkeypatch: Any
    ) -> None:
        """Default capture is full (workspace + site-packages)."""
        captured_kwargs = self._stub_upload(monkeypatch)
        self._stub_uploader(monkeypatch)

        db = connect(tmp_path)
        m = db.capture_local_environment()
        assert m.skip_site_packages is False
        assert captured_kwargs["skip_site_packages"] is False


class TestManifestEnvVars:
    """Tests for env_vars support on manifest builders."""

    def test_env_vars_on_pip_builder(self) -> None:
        """Test setting env_vars via PipManifestBuilder."""
        manifest = (
            PipManifestBuilder.create("test")
            .pip(["numpy"])
            .env_vars({"MY_VAR": "value", "OTHER": "123"})
            .build()
        )
        assert manifest.env_vars == {"MY_VAR": "value", "OTHER": "123"}

    def test_env_vars_on_conda_builder(self) -> None:
        """Test setting env_vars via CondaManifestBuilder."""
        manifest = (
            CondaManifestBuilder.create("test")
            .conda({"dependencies": ["numpy"]})
            .env_vars({"API_KEY": "secret"})
            .build()
        )
        assert manifest.env_vars == {"API_KEY": "secret"}

    def test_env_vars_on_site_builder(self) -> None:
        """Test setting env_vars via SiteManifestBuilder."""
        manifest = SiteManifestBuilder.create("test").env_vars({"DEBUG": "1"}).build()
        assert manifest.env_vars == {"DEBUG": "1"}

    def test_add_env_var(self) -> None:
        """Test adding env vars incrementally."""
        manifest = (
            PipManifestBuilder.create("test")
            .pip(["numpy"])
            .add_env_var("VAR1", "a")
            .add_env_var("VAR2", "b")
            .build()
        )
        assert manifest.env_vars == {"VAR1": "a", "VAR2": "b"}

    def test_env_vars_default_empty(self) -> None:
        """Test that env_vars defaults to empty dict."""
        manifest = PipManifestBuilder.create("test").pip(["numpy"]).build()
        assert manifest.env_vars == {}

    def test_env_vars_factory_method(self) -> None:
        """Test env_vars via GenevaManifest.create_pip() factory."""
        manifest = (
            GenevaManifest.create_pip("test")
            .pip(["numpy"])
            .env_vars({"MODEL": "gpt-4"})
            .build()
        )
        assert manifest.env_vars == {"MODEL": "gpt-4"}

    def test_env_vars_does_not_mutate_input(self) -> None:
        """Test that env_vars makes a copy of the input dict."""
        original = {"KEY": "val"}
        builder = PipManifestBuilder.create("test").pip(["numpy"]).env_vars(original)
        original["KEY"] = "mutated"
        manifest = builder.build()
        assert manifest.env_vars == {"KEY": "val"}

    def test_env_vars_rejects_geneva_zips(self) -> None:
        """Test that GENEVA_ZIPS is rejected as a reserved key."""
        with pytest.raises(ValueError, match="Geneva internal keys.*GENEVA_ZIPS"):
            PipManifestBuilder.create("test").pip(["numpy"]).env_vars(
                {"GENEVA_ZIPS": "bad"}
            ).build()

    def test_env_vars_rejects_pip_extra_index_url(self) -> None:
        """Test that PIP_EXTRA_INDEX_URL is rejected as a reserved key."""
        with pytest.raises(
            ValueError, match="Geneva internal keys.*PIP_EXTRA_INDEX_URL"
        ):
            PipManifestBuilder.create("test").pip(["numpy"]).add_env_var(
                "PIP_EXTRA_INDEX_URL", "bad"
            ).build()

    def test_env_vars_allows_lance_log_override(self) -> None:
        """Test that LANCE_LOG can be overridden (has existing user-override logic)."""
        manifest = (
            PipManifestBuilder.create("test")
            .pip(["numpy"])
            .env_vars({"LANCE_LOG": "debug"})
            .build()
        )
        assert manifest.env_vars == {"LANCE_LOG": "debug"}


def test_make_manifest_env_vars_none() -> None:
    """Test that _make_manifest handles env_vars=None from stored data."""
    from datetime import datetime, timezone

    from geneva.manifest.mgr import _make_manifest

    args = {
        "name": "test",
        "version": None,
        "pip": [],
        "py_modules": [],
        "head_image": None,
        "worker_image": None,
        "skip_site_packages": True,
        "delete_local_zips": False,
        "local_zip_output_dir": None,
        "zips": [[]],
        "checksum": None,
        "created_at": datetime.now(timezone.utc),
        "created_by": "test",
        "requirements_path": None,
        "conda": "{}",
        "conda_environment_path": None,
        "env_vars": None,
    }
    manifest = _make_manifest(args)
    assert manifest.env_vars == {}


def test_make_manifest_env_vars_json_string() -> None:
    """Test that _make_manifest deserializes env_vars from JSON string."""
    from datetime import datetime, timezone

    from geneva.manifest.mgr import _make_manifest

    args = {
        "name": "test",
        "version": None,
        "pip": [],
        "py_modules": [],
        "head_image": None,
        "worker_image": None,
        "skip_site_packages": True,
        "delete_local_zips": False,
        "local_zip_output_dir": None,
        "zips": [[]],
        "checksum": None,
        "created_at": datetime.now(timezone.utc),
        "created_by": "test",
        "requirements_path": None,
        "conda": "{}",
        "conda_environment_path": None,
        "env_vars": '{"MY_VAR": "hello", "OTHER": "world"}',
    }
    manifest = _make_manifest(args)
    assert manifest.env_vars == {"MY_VAR": "hello", "OTHER": "world"}


def test_manifest_env_vars_passed_to_ray(monkeypatch: Any) -> None:
    """Test that env_vars from manifest are passed through to ray.init runtime_env."""
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    manifest = (
        PipManifestBuilder.create("test")
        .pip(["numpy"])
        .env_vars({"MY_VAR": "hello", "DEBUG": "1"})
        .build()
    )

    with ray_mgr_mod.ray_cluster(local=True, manifest=manifest):
        pass

    assert "kwargs" in ray_init_called
    runtime_env = ray_init_called["kwargs"]["runtime_env"]
    env_vars = runtime_env["env_vars"]

    assert env_vars["MY_VAR"] == "hello"
    assert env_vars["DEBUG"] == "1"
    # Geneva defaults should also be present
    assert "GENEVA_ZIPS" in env_vars


def test_manifest_env_vars_overridden_by_extra_env(monkeypatch: Any) -> None:
    """Test that caller extra_env takes precedence over manifest env_vars."""
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    manifest = (
        PipManifestBuilder.create("test")
        .pip(["numpy"])
        .env_vars({"SHARED_KEY": "from_manifest", "MANIFEST_ONLY": "yes"})
        .build()
    )

    extra_env = {"SHARED_KEY": "from_caller", "CALLER_ONLY": "yes"}

    with ray_mgr_mod.ray_cluster(local=True, manifest=manifest, extra_env=extra_env):
        pass

    assert "kwargs" in ray_init_called
    env_vars = ray_init_called["kwargs"]["runtime_env"]["env_vars"]

    # Caller extra_env wins on conflict
    assert env_vars["SHARED_KEY"] == "from_caller"
    # Both unique keys are present
    assert env_vars["MANIFEST_ONLY"] == "yes"
    assert env_vars["CALLER_ONLY"] == "yes"


def test_azure_storage_account_passed_via_extra_env_when_no_env_var(
    monkeypatch: Any,
) -> None:
    """Customer's no-env-var scenario: account_name lives only in
    Connection.storage_options. The caller (Connection._cluster_context_for_def)
    surfaces it into extra_env, and _mgr.py preserves it in workers'
    runtime_env. Regression guard for the propagation hole where _mgr.py
    only consulted env vars, so a credentials-via-storage_options setup
    silently lost the worker-side env-var backstop.
    """
    import geneva.runners.ray._mgr as ray_mgr_mod

    # Scrub env so any silent fallback fails loudly.
    for k in ("AZURE_STORAGE_ACCOUNT_NAME", "AZURE_STORAGE_ACCOUNT"):
        monkeypatch.delenv(k, raising=False)

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    with ray_mgr_mod.ray_cluster(
        local=True,
        extra_env={"AZURE_STORAGE_ACCOUNT_NAME": "fromopts"},
    ):
        pass

    env_vars = ray_init_called["kwargs"]["runtime_env"]["env_vars"]
    assert env_vars["AZURE_STORAGE_ACCOUNT_NAME"] == "fromopts"


# ---------------------------------------------------------------------------
# pip_extra_index_urls
# ---------------------------------------------------------------------------


def test_pip_extra_index_urls_builder() -> None:
    """PipManifestBuilder.add_extra_index_url stores URLs on the manifest."""
    manifest = (
        PipManifestBuilder.create("test")
        .pip(["numpy"])
        .add_extra_index_url("https://example.com/simple/")
        .add_extra_index_url("https://other.com/simple/")
        .build()
    )
    assert manifest.pip_extra_index_urls == [
        "https://example.com/simple/",
        "https://other.com/simple/",
    ]


def test_pip_extra_index_urls_default_empty() -> None:
    """Manifest without add_extra_index_url has empty list."""
    manifest = PipManifestBuilder.create("test").pip(["numpy"]).build()
    assert manifest.pip_extra_index_urls == []


def test_pip_extra_index_urls_json_roundtrip() -> None:
    """pip_extra_index_urls survives to_json/from_json."""
    from geneva.manifest.mgr import GenevaManifest

    manifest = (
        PipManifestBuilder.create("test")
        .pip(["numpy"])
        .add_extra_index_url("https://example.com/simple/")
        .build()
    )
    payload = manifest.to_json()
    restored = GenevaManifest.from_json(payload)
    assert restored.pip_extra_index_urls == ["https://example.com/simple/"]


def test_make_manifest_pip_extra_index_urls_none() -> None:
    """_make_manifest handles pip_extra_index_urls=None from stored data."""
    from datetime import datetime, timezone

    from geneva.manifest.mgr import _make_manifest

    args = {
        "name": "test",
        "version": None,
        "pip": [],
        "py_modules": [],
        "head_image": None,
        "worker_image": None,
        "skip_site_packages": True,
        "delete_local_zips": False,
        "local_zip_output_dir": None,
        "zips": [[]],
        "checksum": None,
        "created_at": datetime.now(timezone.utc),
        "created_by": "test",
        "requirements_path": None,
        "conda": "{}",
        "conda_environment_path": None,
        "env_vars": "{}",
        "pip_extra_index_urls": None,
    }
    manifest = _make_manifest(args)
    assert manifest.pip_extra_index_urls == []


def test_pip_extra_index_urls_merged_in_ray_init(monkeypatch) -> None:
    """Manifest pip_extra_index_urls are merged with default indexes in init_ray."""
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    def fake_ray_init(**kwargs) -> None:
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr(ray_mgr_mod.ray, "init", fake_ray_init)
    monkeypatch.setattr(ray_mgr_mod.ray, "is_initialized", lambda: False)
    monkeypatch.setattr(
        ray_mgr_mod.ray.util.client,  # type: ignore[attr-defined]
        "num_connected_contexts",
        lambda: 0,
    )

    manifest = (
        PipManifestBuilder.create("test")
        .pip(["numpy"])
        .add_extra_index_url("https://custom.example.com/simple/")
        .build()
    )

    with ray_mgr_mod.ray_cluster(local=True, manifest=manifest):
        pass

    assert "kwargs" in ray_init_called
    pip_url = ray_init_called["kwargs"]["runtime_env"]["env_vars"][
        "PIP_EXTRA_INDEX_URL"
    ]
    assert "https://pypi.fury.io/lancedb/" in pip_url
    assert "https://custom.example.com/simple/" in pip_url


class TestUploaderStorageOptionsFallback:
    """Verify Uploader passes credentials to open_lance_dataset under both
    Phalanx vending modes.

    Regression guard for the customer-reported Azure bug where Phalanx did
    not vend storage_options in its describe_table response and the
    Uploader silently passed storage_options=None to open_lance_dataset,
    causing 'no Azure account name in URI' to surface from Rust.

    The fix: when vended_storage_options is None, fall back to
    self.storage_options (which db.define_manifest threads through from
    Connection._storage_options).
    """

    def _build_uploader(
        self,
        *,
        vended_storage_options: dict[str, str] | None,
        connection_storage_options: dict[str, str] | None,
    ) -> MagicMock:
        """Construct an Uploader with mocked namespace + describe_table.

        Returns the mock ``open_lance_dataset`` so callers can assert on
        what storage_options reached the open.
        """
        from geneva.db import NamespaceConfig
        from geneva.packager.uploader import Uploader

        # Mock namespace_client whose describe_table vends a controlled
        # location and storage_options.
        mock_response = MagicMock()
        mock_response.location = "az://mycontainer/path/manifest.lance"
        mock_response.storage_options = vended_storage_options

        mock_ns_client = MagicMock()
        mock_ns_client.describe_table.return_value = mock_response

        ns_config = NamespaceConfig(
            namespace_client_impl="rest",
            namespace_client_properties={"uri": "https://phalanx.example.com"},
        )

        with (
            patch.object(
                NamespaceConfig,
                "connect_namespace_client",
                return_value=mock_ns_client,
            ),
            patch("geneva.db.open_lance_dataset") as mock_open,
        ):
            mock_ds = MagicMock()
            mock_ds.new_file_session.return_value = MagicMock()
            mock_open.return_value = mock_ds

            Uploader(
                namespace_config=ns_config,
                table_id=["_geneva_manifests"],
                storage_options=connection_storage_options,
            )

            return mock_open

    def test_falls_back_to_connection_storage_options_when_phalanx_does_not_vend(
        self,
    ) -> None:
        """The customer bug: Phalanx returns no storage_options, but the
        Connection had them set. Uploader must use the Connection's options.
        """
        connection_opts = {
            "account_name": "myaccount",
            "azure_storage_account_name": "myaccount",
        }
        mock_open = self._build_uploader(
            vended_storage_options=None,
            connection_storage_options=connection_opts,
        )

        assert mock_open.called
        passed_opts = mock_open.call_args.kwargs["storage_options"]
        assert passed_opts == connection_opts

    def test_vended_options_take_precedence_over_connection_options(self) -> None:
        """When Phalanx vends short-lived STS credentials, they win — the
        connection's static credentials must not override them.
        """
        vended_opts = {"account_name": "vended", "sas_token": "short-lived-sas"}
        connection_opts = {"account_name": "client", "account_key": "client-key"}
        mock_open = self._build_uploader(
            vended_storage_options=vended_opts,
            connection_storage_options=connection_opts,
        )

        assert mock_open.called
        passed_opts = mock_open.call_args.kwargs["storage_options"]
        assert passed_opts == vended_opts

    def test_none_when_neither_phalanx_nor_connection_provides_options(self) -> None:
        """If both sources are empty, pass None — caller is expected to
        rely on env vars / instance metadata. The runtime warning in
        open_lance_dataset will surface the issue if it's actually wrong.
        """
        mock_open = self._build_uploader(
            vended_storage_options=None,
            connection_storage_options=None,
        )

        assert mock_open.called
        assert mock_open.call_args.kwargs["storage_options"] is None
