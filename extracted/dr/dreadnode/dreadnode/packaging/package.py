from __future__ import annotations

import hashlib
import json
import tomllib
import typing as t
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from dreadnode.packaging.manifest import MANIFEST_TYPES, BaseManifest

if TYPE_CHECKING:
    from dreadnode.packaging.oci import OCIImage
    from dreadnode.storage.storage import Storage

PackageType = Literal["datasets", "models", "environments", "capabilities"]


class PackageInfo(BaseModel):
    """Serializable package metadata for listing and discovery."""

    name: str
    """Package name."""
    project_type: PackageType
    """Type of package."""
    version: str | None = None
    """Latest version available."""
    description: str | None = None
    """Package description."""
    org: str | None = None
    """Organization that owns the package."""
    is_local: bool = True
    """Whether this package is from local storage."""


CAS_TYPES = {"dataset", "model"}

ARTIFACT_EXTENSIONS = {
    ".parquet",
    ".csv",
    ".arrow",
    ".feather",
    ".jsonl",
    ".safetensors",
    ".pt",
    ".pth",
    ".onnx",
    ".bin",
    ".h5",
    ".pb",
    ".tar",
    ".gz",
    ".zip",
}


@dataclass
class BuildResult:
    success: bool
    image: OCIImage | None = None
    errors: list[str] = field(default_factory=list)


@dataclass
class PushResult:
    success: bool
    manifest_digest: str | None = None
    blobs_uploaded: int = 0
    blobs_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    package_name: str | None = None
    package_version: str | None = None
    package_type: PackageType | None = None


@dataclass
class PullResult:
    success: bool
    config: dict[str, t.Any] | None = None
    dest: Path | None = None
    version: str | None = None
    errors: list[str] = field(default_factory=list)


def _parse_oci_reference(ref: str) -> tuple[str, str]:
    """Parse a package reference into (name, tag).

    Supports formats:
        - capability://org/name       → ("org/name", "latest")
        - capability://org/name:1.0.0 → ("org/name", "1.0.0")
        - org/name                    → ("org/name", "latest")
        - org/name:1.0.0             → ("org/name", "1.0.0")

    Args:
        ref: Package reference.

    Returns:
        Tuple of (name, tag).
    """
    # Strip scheme if present
    if "://" in ref:
        scheme, ref = ref.split("://", 1)
        valid_schemes = {"dataset", "model", "environment", "capability"}
        if scheme not in valid_schemes:
            raise ValueError(
                f"Unknown package type: {scheme}. Valid types: {', '.join(sorted(valid_schemes))}"
            )

    # Split name:tag
    if ":" in ref:
        name, tag = ref.rsplit(":", 1)
        return name, tag

    return ref, "latest"


def _collect_artifacts(module_dir: Path) -> list[Path]:
    """Collect artifact files that should go to CAS."""
    return [
        p for p in module_dir.rglob("*") if p.is_file() and p.suffix.lower() in ARTIFACT_EXTENSIONS
    ]


def _resolve_local_capability_dir(
    package_name: str,
    config: dict[str, t.Any],
) -> str:
    """Return the flattened local directory name for a pulled capability."""

    capability_manifest = config.get("capability_manifest")
    if isinstance(capability_manifest, dict):
        manifest_name = capability_manifest.get("name")
        if isinstance(manifest_name, str) and manifest_name.strip():
            return manifest_name.strip()

    if "/" in package_name:
        return package_name.split("/", 1)[1]
    return package_name


_PLURAL_TO_SINGULAR: dict[str, str] = {
    "datasets": "dataset",
    "models": "model",
    "environments": "environment",
    "capabilities": "capability",
}


def _get_template_type(package_type: str) -> str:
    """Convert package type to template directory name (singular)."""
    return _PLURAL_TO_SINGULAR.get(package_type, package_type)


class Package:
    """A dreadnode component package."""

    def __init__(self, path: Path | None = None):
        """Load an existing package.

        Args:
            path: Project directory. Defaults to current directory.
        """
        self.project_dir = (path or Path.cwd()).resolve()
        self._load_info()

    def _load_info(self) -> None:
        """Load project info from pyproject.toml."""
        pyproject = self.project_dir / "pyproject.toml"
        if not pyproject.exists():
            raise FileNotFoundError(f"No pyproject.toml found in {self.project_dir}")

        with pyproject.open("rb") as f:
            config = tomllib.load(f)

        self.version = config["project"]["version"]
        self.description = config["project"].get("description", "")

        # Find dreadnode entry point
        entry_points = config.get("project", {}).get("entry-points", {})
        for group, eps in entry_points.items():
            if group.startswith("dreadnode."):
                self.entry_point_name = next(iter(eps.keys()))
                self.module_name = next(iter(eps.values()))
                self.package_type = _get_template_type(group.replace("dreadnode.", ""))
                self.org = self.entry_point_name.split(".")[0]
                self.name = (
                    self.entry_point_name.split(".", 1)[1]
                    if "." in self.entry_point_name
                    else self.entry_point_name
                )
                break
        else:
            raise ValueError("No dreadnode entry points found in pyproject.toml")

        self.module_dir = self.project_dir / "src" / self.module_name
        self.manifest_path = (
            None if self.package_type == "capability" else self.module_dir / "manifest.json"
        )

    @property
    def manifest(self) -> BaseManifest:
        """Load and return the manifest."""
        if self.manifest_path is None:
            raise ValueError(self._unsupported_capability_error())
        if not self.manifest_path.exists():
            raise FileNotFoundError("manifest.json not found")
        manifest_class = MANIFEST_TYPES[self.package_type]
        return manifest_class.model_validate_json(self.manifest_path.read_text())

    def _unsupported_capability_error(self) -> str:
        return (
            "Capability package projects are no longer built via Package. "
            "Use a capability directory with capability.yaml and "
            "Dreadnode.push_capability() or dreadnode capability push instead."
        )

    def build(self) -> BuildResult:
        """Build the package as an OCI image.

        For datasets/models, creates a manifest-only image (no layers — artifacts
        are referenced by digest and resolved from CAS/S3).

        For environments, packages the directory as a tar.gz layer.

        Returns:
            BuildResult with success status and OCI image.
        """
        from dreadnode.packaging.oci import build_directory_image, build_manifest_image

        result = BuildResult(success=False)

        if self.package_type == "capability":
            result.errors.append(self._unsupported_capability_error())
            return result

        oci_name = f"{self.org}/{self.name}"

        try:
            if self.package_type in CAS_TYPES:
                # Datasets/models: manifest-only image (artifacts in CAS/S3)
                manifest = self.manifest
                config = json.loads(manifest.model_dump_json())
                result.image = build_manifest_image(
                    config,
                    package_type=self.package_type,
                    name=oci_name,
                    version=self.version,
                )
            else:
                # Environments: directory as tar.gz layer
                manifest = self.manifest
                config = json.loads(manifest.model_dump_json())
                result.image = build_directory_image(
                    self.module_dir,
                    config,
                    package_type=self.package_type,
                    name=oci_name,
                    version=self.version,
                )

            result.success = True
        except Exception as e:
            result.errors.append(f"Build failed: {e}")

        return result

    def push(self, storage: Storage, *, skip_upload: bool = False) -> PushResult:
        """Build and push the package to the OCI registry.

        For datasets and models, uploads artifacts to CAS first, then pushes
        a manifest-only OCI image with artifact digest pointers.

        For environments, packages the directory as a tar.gz layer and pushes
        as a full OCI image.

        Args:
            storage: Storage instance for the org.
            skip_upload: Skip uploading to remote (local only).

        Returns:
            PushResult with status and details.
        """
        result = PushResult(success=False)

        if self.package_type == "capability":
            result.errors.append(self._unsupported_capability_error())
            return result

        if not self.module_dir.exists():
            result.errors.append(f"Module directory not found: {self.module_dir}")
            return result

        assert self.manifest_path is not None  # checked above: capability type already returned
        if not self.manifest_path.exists():
            result.errors.append("manifest.json not found")
            return result

        manifest = self.manifest

        # Handle CAS artifacts for datasets and models
        if self.package_type in CAS_TYPES:
            artifacts = _collect_artifacts(self.module_dir)

            if artifacts:
                # New artifacts in module_dir — hash and store them
                hashes = storage.hash_files(artifacts)

                files_to_upload: dict[Path, str] = {}
                for file_path in artifacts:
                    rel_path = str(file_path.relative_to(self.module_dir))
                    file_hash = hashes[file_path]
                    oid = f"sha256:{file_hash}"
                    manifest.artifacts[rel_path] = oid

                    if not storage.blob_exists(oid):
                        storage.store_blob(oid, file_path)

                    files_to_upload[file_path] = oid

                # Batch upload CAS blobs to remote
                if not skip_upload:
                    uploaded, skipped = storage.upload_blobs(files_to_upload)
                    result.blobs_uploaded += uploaded
                    result.blobs_skipped += skipped

                # Compute artifacts hash
                artifacts_json = json.dumps(manifest.artifacts, sort_keys=True)
                manifest.artifacts_hash = (
                    f"sha256:{hashlib.sha256(artifacts_json.encode()).hexdigest()}"
                )

                # Write updated manifest
                assert self.manifest_path is not None
                self.manifest_path.write_text(manifest.model_dump_json(indent=2))

                # Store manifest in local storage
                # Reverse the singular→plural mapping for storage
                _SINGULAR_TO_PLURAL: dict[str, str] = {v: k for k, v in _PLURAL_TO_SINGULAR.items()}  # noqa: N806
                plural_type = _SINGULAR_TO_PLURAL.get(self.package_type, f"{self.package_type}s")
                storage.store_manifest(
                    package_type=t.cast("PackageType", plural_type),
                    name=self.name,
                    version=self.version,
                    content=manifest.model_dump_json(indent=2),
                )

                # Remove artifacts from module (they're now in CAS)
                for file_path in artifacts:
                    file_path.unlink()
                    parent = file_path.parent
                    while parent != self.module_dir and not any(parent.iterdir()):
                        parent.rmdir()
                        parent = parent.parent

            elif manifest.artifacts:
                # Artifacts already in local CAS, just upload to remote
                if not skip_upload:
                    blobs_to_upload: dict[Path, str] = {}
                    for oid in manifest.artifacts.values():
                        blob_path = storage.blob_path(oid)
                        if blob_path.exists():
                            blobs_to_upload[blob_path] = oid

                    if blobs_to_upload:
                        uploaded, skipped = storage.upload_blobs(blobs_to_upload)
                        result.blobs_uploaded += uploaded
                        result.blobs_skipped += skipped

        # Build OCI image
        build_result = self.build()
        if not build_result.success:
            result.errors.extend(build_result.errors)
            return result

        result.package_name = f"{self.org}/{self.name}"
        result.package_version = self.version
        result.package_type = t.cast("PackageType", self.package_type)

        # Push OCI image to registry
        if not skip_upload and build_result.image is not None:
            try:
                client = storage.oci_client()
                oci_result = client.push(result.package_name, self.version, build_result.image)
                if not oci_result.success:
                    result.errors.extend(oci_result.errors)
                    return result
                result.manifest_digest = oci_result.manifest_digest
                result.blobs_uploaded += oci_result.blobs_pushed
                result.blobs_skipped += oci_result.blobs_existed
            except Exception as e:
                result.errors.append(f"OCI push failed: {e}")
                return result

        result.success = True
        return result

    @staticmethod
    def pull(
        *packages: str,
        upgrade: bool = False,
        _storage: Storage,
    ) -> PullResult:
        """Pull packages from the OCI registry.

        Packages can be specified using URI syntax:
            - capability://org/name - Pull a capability
            - dataset://org/name - Pull a dataset
            - model://org/name - Pull a model
            - environment://org/name - Pull an environment

        Or as plain names (org/name or org/name:version):
            - acme/my-cap - Pull latest
            - acme/my-cap:1.0.0 - Pull specific version

        Args:
            packages: Package names or URIs to pull.
            _storage: Storage instance for registry access.
            upgrade: Re-pull even if already present locally.

        Returns:
            PullResult with status.
        """
        result = PullResult(success=False)

        if not packages:
            result.errors.append("No packages specified")
            return result

        if not _storage.can_sync:
            result.errors.append("No API client configured — cannot access registry")
            return result

        try:
            client = _storage.oci_client()
        except Exception as e:
            result.errors.append(f"Failed to create OCI client: {e}")
            return result

        for pkg in packages:
            name, reference = _parse_oci_reference(pkg)
            try:
                manifest = client.pull_manifest(name, reference)
                annotations = manifest.get("annotations", {})
                package_type = annotations.get("io.dreadnode.type")
                version = annotations.get("io.dreadnode.version", reference)
                config_digest = manifest["config"]["digest"]
                config = json.loads(client.pull_blob(name, config_digest))

                if package_type in CAS_TYPES:
                    plural_type = t.cast("PackageType", f"{package_type}s")
                    dest = _storage.manifest_path(plural_type, name, version)
                    if not upgrade and dest.exists():
                        continue

                    _storage.store_manifest(
                        plural_type,
                        name,
                        version,
                        json.dumps(config, indent=2, sort_keys=True),
                    )
                    result.config = config
                    result.dest = dest
                    result.version = version
                    continue

                if package_type == "capability":
                    dest = _storage.capabilities_path / _resolve_local_capability_dir(
                        name,
                        config,
                    )
                elif package_type == "environment":
                    dest = _storage.package_path("environments", name, version)
                else:
                    dest = _storage.capabilities_path / name

                if not upgrade and dest.exists():
                    continue

                oci_result = client.pull(name, reference, dest)
                if not oci_result.success:
                    result.errors.extend(oci_result.errors)
                    return result

                result.config = oci_result.config
                result.dest = oci_result.dest
                result.version = version
            except Exception as e:
                result.errors.append(f"Pull failed: {e}")
                return result

        result.success = True
        return result
