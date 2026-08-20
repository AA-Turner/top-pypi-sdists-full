"""OCI Distribution client for Dreadnode packages.

Push/pull capabilities, datasets, models, and environments as OCI artifacts.
Uses httpx (already a dependency) — no external OCI library needed.

OCI image layout per package:
  - Config blob: JSON manifest (CapabilityManifest, DatasetManifest, etc.)
  - Layer(s): tar.gz of package directory, or individual CAS blobs

Custom media types:
  - application/vnd.dreadnode.config.v1+json   (config blob)
  - application/vnd.dreadnode.layer.v1.tar+gzip (directory archive)
  - application/vnd.dreadnode.blob.v1           (individual CAS blob)
"""

from __future__ import annotations

import gzip
import hashlib
import inspect
import io
import json
import os
import re
import tarfile
import typing as t
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self
from urllib.parse import urljoin

import httpx
import yaml
from loguru import logger

from dreadnode.core.exceptions import InsufficientCreditsError

if t.TYPE_CHECKING:
    from dreadnode.storage.storage import Storage

# -- Media Types ---------------------------------------------------------------

MEDIA_OCI_MANIFEST = "application/vnd.oci.image.manifest.v1+json"
MEDIA_CONFIG = "application/vnd.dreadnode.config.v1+json"
MEDIA_LAYER_TAR_GZ = "application/vnd.dreadnode.layer.v1.tar+gzip"
MEDIA_BLOB = "application/vnd.dreadnode.blob.v1"

# -- Annotation Keys ----------------------------------------------------------

ANN_TYPE = "io.dreadnode.type"
ANN_NAME = "io.dreadnode.name"
ANN_VERSION = "io.dreadnode.version"
ANN_PATH = "io.dreadnode.path"

# -- Excluded paths during build -----------------------------------------------

_DEFAULT_EXCLUDES = {".git", "__pycache__", ".DS_Store", "dist", ".venv", "node_modules"}
_EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


# ==============================================================================
# Data Types
# ==============================================================================


@dataclass
class Descriptor:
    """OCI content descriptor."""

    media_type: str
    digest: str
    size: int
    annotations: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, t.Any]:
        d: dict[str, t.Any] = {
            "mediaType": self.media_type,
            "digest": self.digest,
            "size": self.size,
        }
        if self.annotations:
            d["annotations"] = self.annotations
        return d


@dataclass
class OCIImage:
    """An OCI image ready for push."""

    config: Descriptor
    layers: list[Descriptor]
    annotations: dict[str, str]
    config_bytes: bytes
    layer_data: dict[str, bytes]  # digest -> bytes

    def manifest_dict(self) -> dict[str, t.Any]:
        return {
            "schemaVersion": 2,
            "mediaType": MEDIA_OCI_MANIFEST,
            "config": self.config.to_dict(),
            "layers": [layer.to_dict() for layer in self.layers],
            "annotations": self.annotations,
        }

    def manifest_bytes(self) -> bytes:
        return json.dumps(self.manifest_dict(), indent=2).encode()


@dataclass
class PushResult:
    success: bool
    manifest_digest: str | None = None
    blobs_pushed: int = 0
    blobs_existed: int = 0
    errors: list[str] = field(default_factory=list)


@dataclass
class PullResult:
    success: bool
    dest: Path | None = None
    config: dict[str, t.Any] | None = None
    errors: list[str] = field(default_factory=list)


# ==============================================================================
# Build
# ==============================================================================


def _sha256(data: bytes) -> str:
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def _descriptor(
    data: bytes, media_type: str, annotations: dict[str, str] | None = None
) -> Descriptor:
    return Descriptor(
        media_type=media_type,
        digest=_sha256(data),
        size=len(data),
        annotations=annotations or {},
    )


def _should_exclude(rel_parts: tuple[str, ...]) -> bool:
    """Check if a path should be excluded from the archive."""
    for part in rel_parts:
        if part in _DEFAULT_EXCLUDES:
            return True
    return any(rel_parts[-1].endswith(s) for s in _EXCLUDED_SUFFIXES) if rel_parts else False


def build_directory_image(
    source_dir: Path,
    config: dict[str, t.Any],
    *,
    package_type: str,
    name: str,
    version: str,
) -> OCIImage:
    """Build an OCI image from a directory (capabilities, environments).

    The entire directory becomes a single tar.gz layer.
    The config dict becomes the OCI config blob.
    """
    source_dir = source_dir.resolve()

    # Create tar.gz of source directory (deterministic: zero timestamps and metadata)
    buf = io.BytesIO()
    gz = gzip.GzipFile(fileobj=buf, mode="wb", mtime=0)
    with tarfile.open(fileobj=gz, mode="w") as tar:
        for item in sorted(source_dir.rglob("*")):
            if not item.is_file():
                continue
            rel = item.relative_to(source_dir)
            if _should_exclude(rel.parts):
                continue
            info = tar.gettarinfo(item, arcname=str(rel))
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            with item.open("rb") as f:
                tar.addfile(info, f)
    gz.close()

    layer_bytes = buf.getvalue()

    annotations = {
        ANN_TYPE: package_type,
        ANN_NAME: name,
        ANN_VERSION: version,
    }

    config_bytes = json.dumps(config, indent=2, sort_keys=True).encode()
    config_desc = _descriptor(config_bytes, MEDIA_CONFIG)
    layer_desc = _descriptor(layer_bytes, MEDIA_LAYER_TAR_GZ)

    return OCIImage(
        config=config_desc,
        layers=[layer_desc],
        annotations=annotations,
        config_bytes=config_bytes,
        layer_data={layer_desc.digest: layer_bytes},
    )


def build_manifest_image(
    config: dict[str, t.Any],
    *,
    package_type: str,
    name: str,
    version: str,
) -> OCIImage:
    """Build an OCI image that is just a manifest/config (datasets, models).

    The OCI image contains only the metadata manifest as the config blob.
    No layers — actual artifact blobs (parquet, safetensors, etc.) live in
    S3/CAS and are referenced by digest in the manifest's ``artifacts`` dict.

    At pull time, the consumer reads the config to get artifact pointers,
    then resolves them from CAS/S3.
    """
    annotations = {
        ANN_TYPE: package_type,
        ANN_NAME: name,
        ANN_VERSION: version,
    }

    config_bytes = json.dumps(config, indent=2, sort_keys=True).encode()
    config_desc = _descriptor(config_bytes, MEDIA_CONFIG)

    return OCIImage(
        config=config_desc,
        layers=[],
        annotations=annotations,
        config_bytes=config_bytes,
        layer_data={},
    )


# ==============================================================================
# OCI Registry Client
# ==============================================================================


class OCIRegistryClient:
    """OCI Distribution v2 registry client.

    Supports push/pull of blobs and manifests via the standard
    OCI Distribution Specification endpoints.
    """

    def __init__(
        self,
        registry_url: str,
        *,
        auth: tuple[str, str] | None = None,
        token: str | None = None,
        timeout: float = 300.0,
    ) -> None:
        self._base_url = registry_url.rstrip("/")

        headers: dict[str, str] = {"User-Agent": "dreadnode-sdk/2.0"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        auth_param = httpx.BasicAuth(auth[0], auth[1]) if auth else None

        self._client = httpx.Client(
            base_url=self._base_url,
            headers=headers,
            auth=auth_param,
            timeout=timeout,
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    # -- Blob operations -------------------------------------------------------

    @staticmethod
    def _org_from_name(name: str) -> str:
        """Extract the org segment from an OCI repository name."""
        org, _, _ = name.partition("/")
        if not org:
            raise ValueError(f"Invalid OCI repository name: {name!r}")
        return org

    @staticmethod
    def _extract_response_detail(response: httpx.Response) -> str | None:
        try:
            payload = response.json()
        except (TypeError, ValueError):
            return None

        if not isinstance(payload, dict):
            return None

        detail = payload.get("detail")
        if detail is None:
            return None
        if isinstance(detail, str):
            return detail
        return str(detail)

    def _raise_insufficient_credits(
        self,
        response: httpx.Response,
        fallback_message: str,
    ) -> None:
        if response.status_code != 429:
            return

        detail = self._extract_response_detail(response)
        message = detail or fallback_message
        logger.warning(message)
        raise InsufficientCreditsError(message)

    def _raise_for_status(self, response: httpx.Response) -> None:
        """``raise_for_status`` that surfaces the API ``detail`` body on errors.

        httpx's bare ``raise_for_status`` drops the response body, so ingest
        validation rejections (e.g. a task-archive ``400``) arrived as an opaque
        ``Client error '400 Bad Request'``. Pull the ``detail`` through so the
        CLI tells the author *why* the upload was rejected.
        """
        if response.is_success:
            return
        detail = self._extract_response_detail(response)
        if detail is None:
            response.raise_for_status()
            return
        raise httpx.HTTPStatusError(
            f"{response.status_code} {response.reason_phrase}: {detail}",
            request=response.request,
            response=response,
        )

    def blob_exists(self, name: str, digest: str) -> bool:
        """HEAD /v2/<name>/blobs/<digest>"""
        org = self._org_from_name(name)
        resp = self._client.head(f"/api/v1/{org}/blobs/{digest}")
        return resp.status_code == 200

    def push_blob(self, name: str, data: bytes, digest: str) -> bool:
        """Push a blob via monolithic upload. Returns True if newly pushed, False if existed."""
        if self.blob_exists(name, digest):
            return False

        # Initiate upload
        resp = self._client.post(f"/api/v1/{name}/blobs/uploads/")
        self._raise_insufficient_credits(
            resp,
            "Insufficient credits for storage — purchase credits to continue",
        )
        self._raise_for_status(resp)

        location = resp.headers.get("Location", "")
        if not location:
            raise RuntimeError("Registry did not return upload location")

        # Resolve relative location
        if not location.startswith("http"):
            location = urljoin(f"{self._base_url.rstrip('/')}/", location)

        # Complete the upload with digest
        sep = "&" if "?" in location else "?"
        resp = self._client.put(
            f"{location}{sep}digest={digest}",
            content=data,
            headers={"Content-Type": "application/octet-stream"},
        )
        self._raise_insufficient_credits(
            resp,
            "Insufficient credits for storage — purchase credits to continue",
        )
        self._raise_for_status(resp)
        return True

    def pull_blob(self, name: str, digest: str) -> bytes:
        """GET /v2/<name>/blobs/<digest>"""
        org = self._org_from_name(name)
        resp = self._client.get(f"/api/v1/{org}/blobs/{digest}")
        resp.raise_for_status()
        return resp.content

    # -- Manifest operations ---------------------------------------------------

    def push_manifest(self, name: str, reference: str, manifest: bytes) -> str:
        """PUT /v2/<name>/manifests/<reference>. Returns the digest."""
        resp = self._client.put(
            f"/api/v1/{name}/manifests/{reference}",
            content=manifest,
            headers={"Content-Type": MEDIA_OCI_MANIFEST},
        )
        self._raise_insufficient_credits(
            resp,
            "Insufficient credits for storage — purchase credits to continue",
        )
        self._raise_for_status(resp)
        return resp.headers.get("Docker-Content-Digest", _sha256(manifest))

    def pull_manifest(self, name: str, reference: str) -> dict[str, t.Any]:
        """GET /v2/<name>/manifests/<reference>"""
        resp = self._client.get(
            f"/api/v1/{name}/manifests/{reference}",
            headers={"Accept": MEDIA_OCI_MANIFEST},
        )
        resp.raise_for_status()
        return resp.json()

    def list_tags(self, name: str) -> list[str]:
        """GET /v2/<name>/tags/list"""
        resp = self._client.get(f"/api/v1/{name}/tags/list")
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
        return resp.json().get("tags", [])

    # -- High-level push/pull --------------------------------------------------

    def push(self, name: str, tag: str, image: OCIImage) -> PushResult:
        """Push an OCI image (config + layers + manifest) to the registry."""
        result = PushResult(success=False)
        try:
            # Push config blob
            if self.push_blob(name, image.config_bytes, image.config.digest):
                result.blobs_pushed += 1
            else:
                result.blobs_existed += 1

            # Push layer blobs
            for layer in image.layers:
                data = image.layer_data[layer.digest]
                if self.push_blob(name, data, layer.digest):
                    result.blobs_pushed += 1
                else:
                    result.blobs_existed += 1

            # Push manifest
            manifest_bytes = image.manifest_bytes()
            digest = self.push_manifest(name, tag, manifest_bytes)

            result.success = True
            result.manifest_digest = digest
        except InsufficientCreditsError as exc:
            result.errors.append(str(exc))
            raise
        except (httpx.HTTPError, RuntimeError, ValueError) as exc:
            result.errors.append(str(exc))

        return result

    def pull(self, name: str, reference: str, dest: Path) -> PullResult:
        """Pull an OCI image and extract to dest."""
        result = PullResult(success=False)
        try:
            manifest = self.pull_manifest(name, reference)

            # Pull config
            config_digest = manifest["config"]["digest"]
            config_bytes = self.pull_blob(name, config_digest)
            result.config = json.loads(config_bytes)

            # Pull and extract layers
            dest.mkdir(parents=True, exist_ok=True)
            for layer in manifest.get("layers", []):
                layer_digest = layer["digest"]
                media_type = layer.get("mediaType", "")
                layer_bytes = self.pull_blob(name, layer_digest)

                if media_type == MEDIA_LAYER_TAR_GZ:
                    _safe_extract_tar(layer_bytes, dest)
                elif media_type == MEDIA_BLOB:
                    path_ann = layer.get("annotations", {}).get(ANN_PATH)
                    if path_ann:
                        file_dest = dest / path_ann
                        file_dest.parent.mkdir(parents=True, exist_ok=True)
                        file_dest.write_bytes(layer_bytes)

            result.success = True
            result.dest = dest
        except (
            httpx.HTTPError,
            json.JSONDecodeError,
            KeyError,
            OSError,
            RuntimeError,
            tarfile.TarError,
            ValueError,
        ) as exc:
            result.errors.append(str(exc))

        return result


# ==============================================================================
# Capability convenience functions
# ==============================================================================


def _resolve_produced_item_types(
    capability_root: Path, produces: dict[str, str] | None
) -> list[dict[str, t.Any]]:
    """Resolve `produces` refs ("module:Class") to JSON Schemas at build time.

    ``module`` is a path relative to the capability root (with or without the
    ``.py`` suffix). The referenced class must be a Pydantic ``BaseModel``; its
    ``.model_json_schema()`` is embedded in the package so the platform can
    validate items of this type without ever importing capability code.
    """
    import importlib.util
    import sys

    from pydantic import BaseModel

    resolved: list[dict[str, t.Any]] = []
    for type_name, ref in (produces or {}).items():
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", type_name) or type_name in {
            "finding",
            "asset",
        }:
            raise ValueError(
                f"produces item type identifier {type_name!r} must be lowercase snake_case, at most 64 characters, and not a built-in type"
            )
        module_ref, sep, class_name = ref.partition(":")
        if not sep or not class_name:
            raise ValueError(f"produces['{type_name}'] must be 'module:ClassName', got '{ref}'")
        rel = module_ref if module_ref.endswith(".py") else f"{module_ref}.py"
        file_path = (capability_root / rel).resolve()
        if not file_path.is_file():
            raise FileNotFoundError(f"produces['{type_name}'] references missing module: {rel}")

        mod_name = f"_dn_produces_{type_name}_{file_path.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module for produces['{type_name}']: {rel}")
        module = importlib.util.module_from_spec(spec)
        # Register in sys.modules before exec so a module using
        # `from __future__ import annotations` (PEP 563) can resolve its own
        # forward references when model_json_schema() builds the schema below.
        # An unregistered module has no importable namespace, so Pydantic's
        # deferred forward-ref resolution raises "not fully defined". Removed
        # afterwards so we do not pollute sys.modules during the build.
        sys.modules[mod_name] = module
        try:
            spec.loader.exec_module(module)

            cls = getattr(module, class_name, None)
            if not (isinstance(cls, type) and issubclass(cls, BaseModel)):
                raise TypeError(f"produces['{type_name}'] -> {ref} is not a Pydantic BaseModel")

            resolved.append(
                {
                    "name": type_name,
                    "model_path": ref,
                    "json_schema": cls.model_json_schema(),
                }
            )
        finally:
            sys.modules.pop(mod_name, None)
    return resolved


def build_capability(source_dir: Path, *, name: str | None = None) -> OCIImage:
    """Build an OCI image from a capability directory.

    Resolves capability.yaml into a full manifest, then packages
    the directory as a tar.gz layer with the manifest as config.
    """
    import asyncio

    from dreadnode.capabilities.loader import load_capability

    cap = asyncio.run(load_capability(source_dir))
    skill_paths: list[str] = []
    for skill_root in sorted(cap.skills_paths or []):
        if skill_root.is_dir():
            for entry in sorted(skill_root.iterdir()):
                if not entry.is_dir():
                    continue
                if not (entry / "SKILL.md").exists():
                    continue
                skill_paths.append(str(entry.relative_to(cap.path)))
        elif skill_root.name.upper() == "SKILL.MD":
            skill_paths.append(str(skill_root.parent.relative_to(cap.path)))

    manifest_dict = json.loads(cap.manifest.model_dump_json())
    declared_output_fields = cap.manifest.model_fields_set & {"outputs", "produces", "items"}
    if "outputs" not in declared_output_fields and declared_output_fields:
        from dreadnode.items.config import parse_item_produces_config

        output_config = parse_item_produces_config(cap.manifest)
        if not output_config.enabled:
            manifest_dict["outputs"] = False
        elif (
            output_config.builtin_types == {"finding", "asset"}
            and not output_config.registry_types
            and not output_config.custom_types
        ):
            manifest_dict["outputs"] = True
        elif not output_config.custom_types:
            manifest_dict["outputs"] = sorted(
                output_config.builtin_types | output_config.registry_types
            )
        else:
            manifest_dict["outputs"] = dict(output_config.custom_types)
            selected_identifiers = output_config.builtin_types | output_config.registry_types
            if selected_identifiers:
                manifest_dict["outputs"]["values"] = sorted(selected_identifiers)
    elif "outputs" not in declared_output_fields:
        manifest_dict.pop("outputs", None)
    manifest_dict.pop("produces", None)
    manifest_dict.pop("items", None)
    capability_root = cap.path.resolve()

    # Build raw (pre-interpolated) server config lookup for display metadata.
    # Merges .mcp.json files and inline servers, same order as the loader.
    _raw_server_configs: dict[str, dict[str, t.Any]] = {}
    _mcp_section = manifest_dict.get("mcp")
    if isinstance(_mcp_section, dict):
        for _rel in _mcp_section.get("files", []):
            _p = source_dir / _rel
            if _p.exists():
                _data = json.loads(_p.read_text())
                _raw_server_configs.update(_data.get("mcpServers", {}))
        _raw_server_configs.update(_mcp_section.get("servers", {}))
    elif _mcp_section is None:
        for _fn in (".mcp.json", "mcp.json"):
            _p = source_dir / _fn
            if _p.exists():
                _data = json.loads(_p.read_text())
                _raw_server_configs.update(_data.get("mcpServers", {}))

    def _tool_source_path(tool: t.Any) -> str | None:
        source_target = getattr(tool.fn, "func", tool.fn)
        source_file = inspect.getsourcefile(source_target)
        if source_file is None:
            return None
        try:
            return str(Path(source_file).resolve().relative_to(capability_root))
        except ValueError:
            return None

    # Resolve optional local `outputs` Pydantic classes → JSON Schemas at BUILD
    # time. Identifier-only platform types need no capability-local model.
    from dreadnode.items.config import custom_item_type_refs

    item_types_list = _resolve_produced_item_types(
        capability_root,
        custom_item_type_refs(cap.manifest),
    )

    config_dict: dict[str, t.Any] = {
        "capability_manifest": manifest_dict,
        "item_types": item_types_list,
        "agents": [
            {
                "name": agent.name,
                "description": agent.description,
                "model": agent.model,
            }
            for agent in cap.agents
        ],
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "path": _tool_source_path(tool),
            }
            for tool in cap.tools
        ],
        "skills": skill_paths,
        "mcp_servers": [
            {
                "name": server.name,
                "transport": server.transport,
                "description": _raw_server_configs.get(server.name, {}).get("description"),
                # Use raw (pre-interpolated) values so absolute build paths
                # don't leak into the stored config.
                **(
                    {"command": raw_cmd}
                    if (raw_cmd := _raw_server_configs.get(server.name, {}).get("command"))
                    else {}
                ),
                **(
                    {"args": raw_args}
                    if (raw_args := _raw_server_configs.get(server.name, {}).get("args"))
                    else {}
                ),
                **(
                    {"url": raw_url}
                    if (raw_url := _raw_server_configs.get(server.name, {}).get("url"))
                    else {}
                ),
                **(
                    {"env": raw_env}
                    if (raw_env := _raw_server_configs.get(server.name, {}).get("env"))
                    else {}
                ),
                **(
                    {"headers": raw_hdrs}
                    if (raw_hdrs := _raw_server_configs.get(server.name, {}).get("headers"))
                    else {}
                ),
            }
            for server in cap.mcp_server_defs
        ],
        "workers": [
            {
                "name": name_,
                "kind": "subprocess" if (raw or {}).get("command") else "inprocess",
                # Use raw (pre-interpolated) values so absolute build paths
                # don't leak into the stored config.
                **({"path": raw_path} if (raw_path := (raw or {}).get("path")) else {}),
                **({"command": raw_cmd} if (raw_cmd := (raw or {}).get("command")) else {}),
                **({"args": raw_args} if (raw_args := (raw or {}).get("args")) else {}),
                **({"env": raw_env} if (raw_env := (raw or {}).get("env")) else {}),
                **({"when": raw_when} if (raw_when := (raw or {}).get("when")) else {}),
            }
            for name_, raw in (manifest_dict.get("workers") or {}).items()
        ],
    }
    resolved_name = name or cap.name
    version = cap.version

    return build_directory_image(
        source_dir,
        config_dict,
        package_type="capability",
        name=resolved_name,
        version=version,
    )


def build_dataset(
    source_dir: Path,
    storage: Storage,
    *,
    name: str | None = None,
) -> OCIImage:
    """Build a manifest-only OCI image from a dataset source directory."""
    from dreadnode.datasets.local import LocalDataset

    dataset = LocalDataset.from_dir(source_dir, storage)
    return build_manifest_image(
        json.loads(dataset.manifest.model_dump_json()),
        package_type="dataset",
        name=name or dataset.name,
        version=dataset.version,
    )


def build_model(
    source_dir: Path,
    storage: Storage,
    *,
    name: str | None = None,
) -> OCIImage:
    """Build a manifest-only OCI image from a model source directory."""
    from dreadnode.models.local import LocalModel

    model = LocalModel.from_dir(source_dir, storage)
    return build_manifest_image(
        json.loads(model.manifest.model_dump_json()),
        package_type="model",
        name=name or model.name,
        version=model.version,
    )


def _load_task_config(source_dir: Path) -> dict[str, t.Any]:
    """Load and validate task.yaml from a task/environment directory."""
    task_yaml_path = source_dir / "task.yaml"
    if not task_yaml_path.is_file():
        raise FileNotFoundError(f"task.yaml not found in {source_dir}")

    task_config = yaml.safe_load(task_yaml_path.read_text())
    if not isinstance(task_config, dict):
        raise TypeError("task.yaml must contain a YAML mapping")
    return task_config


def _build_task_like_image(
    source_dir: Path,
    *,
    package_type: t.Literal["environment", "task"],
    name: str | None = None,
    version: str = "1.0.0",
) -> OCIImage:
    """Build a directory-backed OCI image from task.yaml metadata."""
    task_config = _load_task_config(source_dir)
    resolved_name = name or source_dir.name
    return build_directory_image(
        source_dir,
        task_config,
        package_type=package_type,
        name=resolved_name,
        version=version,
    )


def build_environment(
    source_dir: Path,
    *,
    name: str | None = None,
    version: str = "1.0.0",
) -> OCIImage:
    """Build an OCI image from an environment directory described by task.yaml."""
    return _build_task_like_image(
        source_dir,
        package_type="environment",
        name=name,
        version=version,
    )


def build_task(
    source_dir: Path,
    *,
    name: str | None = None,
    version: str = "1.0.0",
) -> OCIImage:
    """Build an OCI image from a task directory.

    The task.yaml content becomes the OCI config blob and the task directory
    is packaged as a single tar.gz layer.
    """
    return _build_task_like_image(
        source_dir,
        package_type="task",
        name=name,
        version=version,
    )


# ==============================================================================
# Safety
# ==============================================================================


def _safe_extract_tar(data: bytes, dest: Path) -> None:
    """Extract a tar.gz archive with path traversal protection."""
    dest = dest.resolve()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for member in tar.getmembers():
            member_path = (dest / member.name).resolve()
            if not str(member_path).startswith(str(dest) + os.sep) and member_path != dest:
                raise ValueError(f"Path traversal detected in archive: {member.name}")
            if member.issym() or member.islnk():
                raise ValueError(f"Symlinks not allowed in archive: {member.name}")
        tar.extractall(dest, filter="data")
