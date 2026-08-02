# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from typing import TYPE_CHECKING, Any

from geneva.cluster.builder import default_image

if TYPE_CHECKING:
    from typing import Self

    from .mgr import GenevaManifest


# =============================================================================
# Type-Safe Manifest Builders
#
# Pip and conda manifests are separate builders because Ray's runtime_env
# treats them as mutually exclusive options:
# https://docs.ray.io/en/latest/ray-core/handling-dependencies.html#using-conda-or-pip-packages
# =============================================================================


class _ManifestBuilderBase:
    """Base class with shared configuration for type-safe manifest builders.

    This mixin provides common methods for configuring manifest properties
    like version, images, py_modules, and site package options.
    """

    def __init__(self) -> None:
        self._name: str | None = None
        self._version: str | None = None
        self._py_modules: list[str] = []
        self._head_image: str | None = None
        self._worker_image: str | None = None
        self._upload_site_packages: bool = False
        self._delete_local_zips: bool = False
        self._local_zip_output_dir: str | None = None
        self._env_vars: dict[str, str] = {}

    def name(self, name: str) -> "Self":
        """Set the manifest name."""
        self._name = name
        return self  # type: ignore[return-value]

    def version(self, version: str) -> "Self":
        """Set the manifest version."""
        self._version = version
        return self  # type: ignore[return-value]

    def py_modules(self, modules: list[str]) -> "Self":
        """Set the Python modules for the runtime environment."""
        self._py_modules = modules.copy()
        return self  # type: ignore[return-value]

    def add_py_module(self, module: str) -> "Self":
        """Add a single Python module to the runtime environment."""
        self._py_modules.append(module)
        return self  # type: ignore[return-value]

    def head_image(self, head_image: str) -> "Self":
        """Set the container image for Ray head."""
        self._head_image = head_image
        return self  # type: ignore[return-value]

    def worker_image(self, worker_image: str) -> "Self":
        """Set the container image for Ray workers."""
        self._worker_image = worker_image
        return self  # type: ignore[return-value]

    def default_head_image(self) -> "Self":
        """Set the container image for Ray head to the platform default."""
        self._head_image = default_image()
        return self  # type: ignore[return-value]

    def default_worker_image(self) -> "Self":
        """Set the container image for Ray workers to the platform default."""
        self._worker_image = default_image()
        return self  # type: ignore[return-value]

    def upload_site_packages(self, upload: bool = True) -> "Self":
        """Set whether to upload site packages during packaging."""
        self._upload_site_packages = upload
        return self  # type: ignore[return-value]

    def delete_local_zips(self, delete: bool = True) -> "Self":
        """Set whether to delete local zip files after upload."""
        self._delete_local_zips = delete
        return self  # type: ignore[return-value]

    def local_zip_output_dir(self, output_dir: str) -> "Self":
        """Set the local directory for zip file output."""
        self._local_zip_output_dir = output_dir
        return self  # type: ignore[return-value]

    # Keys managed by Geneva internals that must not be overridden.
    _RESERVED_ENV_VARS = frozenset({"GENEVA_ZIPS", "PIP_EXTRA_INDEX_URL"})

    def _check_reserved_env_vars(self, keys: set[str]) -> None:
        conflicts = self._RESERVED_ENV_VARS & keys
        if conflicts:
            raise ValueError(
                f"env_vars cannot override Geneva internal keys: "
                f"{', '.join(sorted(conflicts))}"
            )

    def env_vars(self, env_vars: dict[str, str]) -> "Self":
        """Set environment variables for Ray workers via runtime_env.

        These override cluster-level env vars for Ray worker processes.
        """
        self._check_reserved_env_vars(set(env_vars.keys()))
        self._env_vars = env_vars.copy()
        return self  # type: ignore[return-value]

    def add_env_var(self, key: str, value: str) -> "Self":
        """Add a single environment variable for Ray workers."""
        self._check_reserved_env_vars({key})
        self._env_vars[key] = value
        return self  # type: ignore[return-value]

    def _build_manifest(
        self,
        pip: list[str] | None = None,
        requirements_path: str | None = None,
        conda: dict[str, Any] | None = None,
        conda_environment_path: str | None = None,
        pip_extra_index_urls: list[str] | None = None,
    ) -> "GenevaManifest":
        """Build the GenevaManifest with the configured settings."""
        if self._name is None:
            raise ValueError("Manifest name is required. Use .name() to set it.")

        from .mgr import GenevaManifest

        return GenevaManifest(
            name=self._name,
            version=self._version,
            pip=pip or [],
            requirements_path=requirements_path,
            conda=conda or {},
            conda_environment_path=conda_environment_path,
            py_modules=self._py_modules,
            head_image=self._head_image,
            worker_image=self._worker_image,
            skip_site_packages=not self._upload_site_packages,
            delete_local_zips=self._delete_local_zips,
            local_zip_output_dir=self._local_zip_output_dir,
            env_vars=self._env_vars,
            pip_extra_index_urls=pip_extra_index_urls or [],
        )


class PipManifestBuilder(_ManifestBuilderBase):
    """Type-safe builder for pip-based manifests.

    This builder does NOT have conda methods - use CondaManifestBuilder for conda.

    Examples
    --------

        manifest = (
            PipManifestBuilder.create("my-manifest")
            .pip(["numpy", "pandas"])
            .build()
        )
    """

    def __init__(self) -> None:
        super().__init__()
        self._pip: list[str] = []
        self._requirements_path: str | None = None
        self._pip_extra_index_urls: list[str] = []

    def pip(self, packages: list[str]) -> "PipManifestBuilder":
        """Set the runtime pip packages list.

        Cannot be used with .requirements_path().
        """
        self._pip = packages.copy()
        return self

    def add_pip(self, package: str) -> "PipManifestBuilder":
        """Add a single pip package to the runtime environment."""
        self._pip.append(package)
        return self

    def requirements_path(self, path: str) -> "PipManifestBuilder":
        """Set the path to a requirements.txt file.

        Cannot be used with .pip().
        """
        self._requirements_path = path
        return self

    def add_extra_index_url(self, url: str) -> "PipManifestBuilder":
        """Add an extra pip index URL for Ray workers.

        These URLs are merged with Geneva's default indexes (fury.io)
        and set in PIP_EXTRA_INDEX_URL for worker processes.
        """
        self._pip_extra_index_urls.append(url)
        return self

    def build(self) -> "GenevaManifest":
        """Build the GenevaManifest with pip configuration."""
        if len(self._pip) > 0 and self._requirements_path is not None:
            raise ValueError("Cannot set both pip and requirements_path")

        return self._build_manifest(
            pip=self._pip,
            requirements_path=self._requirements_path,
            pip_extra_index_urls=self._pip_extra_index_urls,
        )

    @classmethod
    def create(cls, name: str) -> "PipManifestBuilder":
        """Create a new pip manifest builder with the given name."""
        return cls().name(name)


class CondaManifestBuilder(_ManifestBuilderBase):
    """Type-safe builder for conda-based manifests.

    This builder does NOT have pip methods - use PipManifestBuilder for pip.

    Examples
    --------

        manifest = (
            CondaManifestBuilder.create("my-manifest")
            .conda({"dependencies": ["python=3.10", "numpy"]})
            .build()
        )
    """

    def __init__(self) -> None:
        super().__init__()
        self._conda: dict[str, Any] = {}
        self._conda_environment_path: str | None = None

    def conda(self, dependencies: dict[str, Any]) -> "CondaManifestBuilder":
        """Set the conda dependencies for the runtime environment.

        Cannot be used with .conda_environment_path().
        """
        self._conda = dependencies.copy()
        return self

    def conda_environment_path(self, path: str) -> "CondaManifestBuilder":
        """Set the path to a conda environment.yml file.

        Cannot be used with .conda().
        """
        self._conda_environment_path = path
        return self

    def build(self) -> "GenevaManifest":
        """Build the GenevaManifest with conda configuration."""
        if len(self._conda) > 0 and self._conda_environment_path is not None:
            raise ValueError("Cannot set both conda and conda_environment_path")

        return self._build_manifest(
            conda=self._conda,
            conda_environment_path=self._conda_environment_path,
        )

    @classmethod
    def create(cls, name: str) -> "CondaManifestBuilder":
        """Create a new conda manifest builder with the given name."""
        return cls().name(name)


class SiteManifestBuilder(_ManifestBuilderBase):
    """Type-safe builder for site-packages manifests.

    This builder uploads local site-packages without external dependencies.
    It does NOT have pip or conda methods.

    upload_site_packages defaults to True for this builder.

    Examples
    --------

        manifest = SiteManifestBuilder.create("my-manifest").build()
    """

    def __init__(self) -> None:
        super().__init__()
        # Site manifest defaults to uploading site packages
        self._upload_site_packages = True

    def build(self) -> "GenevaManifest":
        """Build the GenevaManifest with site-packages configuration."""
        return self._build_manifest()

    @classmethod
    def create(cls, name: str) -> "SiteManifestBuilder":
        """Create a new site manifest builder with the given name."""
        return cls().name(name)
