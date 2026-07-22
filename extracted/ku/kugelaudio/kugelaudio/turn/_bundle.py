"""Model acquisition and integrity verification for local turn detection."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ._schema import BundleManifest, TurnModelConfig, VariantIndex, load_schema
from .errors import TurnBundleError, TurnDependencyError, TurnModelDownloadError

DEFAULT_REPO_ID = "kugelaudio/turn-detection"
DEFAULT_REVISION = "941a8e7667ae55d9d145cec8ad9412d8150f421b"
MANIFEST_FILENAME = "manifest.json"


@dataclass(frozen=True, slots=True)
class VerifiedBundle:
    """A local bundle whose complete manifest has passed verification."""

    path: Path
    manifest: BundleManifest
    config: TurnModelConfig


@dataclass(frozen=True, slots=True)
class DownloadedBundle:
    """Verified model plus the metadata needed by the endpoint policy."""

    bundle: VerifiedBundle
    policy_path: Path
    variant_path: str
    revision: str


def sha256_file(path: Path, *, chunk_bytes: int = 8 * 1024 * 1024) -> str:
    """Calculate SHA-256 without loading a model weight file into memory."""
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            while chunk := handle.read(chunk_bytes):
                digest.update(chunk)
    except OSError as exc:
        raise TurnBundleError(f"cannot read bundle file {path}: {exc}") from exc
    return digest.hexdigest()


def verify_bundle(bundle_dir: str | Path) -> VerifiedBundle:
    """Reject missing, corrupt, or incompatible model bundles."""
    root = Path(bundle_dir)
    manifest = load_schema(root / MANIFEST_FILENAME, BundleManifest)
    for item in manifest.files:
        path = root / item.path
        if not path.is_file():
            raise TurnBundleError(f"bundle file is missing: {path}")
        actual_size = path.stat().st_size
        if actual_size != item.size_bytes:
            raise TurnBundleError(
                f"bundle size mismatch for {item.path}: {actual_size} != {item.size_bytes}"
            )
        actual_sha = sha256_file(path)
        if actual_sha != item.sha256:
            raise TurnBundleError(
                f"bundle checksum mismatch for {item.path}: {actual_sha} != {item.sha256}"
            )
    config = load_schema(root / "config.json", TurnModelConfig)
    if config.whisper_input_frames != manifest.input_feature_frames:
        raise TurnBundleError(
            "config/manifest frame mismatch: "
            f"{config.whisper_input_frames} != {manifest.input_feature_frames}"
        )
    return VerifiedBundle(path=root, manifest=manifest, config=config)


def download_bundle(
    *,
    repo_id: str = DEFAULT_REPO_ID,
    variant: str = "recommended",
    revision: str = DEFAULT_REVISION,
    token: str | bool | None = None,
    cache_dir: str | Path | None = None,
    local_files_only: bool = False,
) -> DownloadedBundle:
    """Download only the selected variant, then verify every declared file."""
    try:
        from huggingface_hub import hf_hub_download, snapshot_download
        from huggingface_hub.errors import (
            HfHubHTTPError,
            LocalEntryNotFoundError,
            RepositoryNotFoundError,
            RevisionNotFoundError,
        )
    except ImportError as exc:
        raise TurnDependencyError(
            'Turn detection needs optional dependencies; install "kugelaudio[turn-detection]".'
        ) from exc

    cache = str(cache_dir) if cache_dir is not None else None
    try:
        index_path = Path(
            hf_hub_download(
                repo_id,
                "variants.json",
                repo_type="model",
                revision=revision,
                token=token,
                cache_dir=cache,
                local_files_only=local_files_only,
            )
        )
        index = load_schema(index_path, VariantIndex)
        selected = index.resolve(variant)
        snapshot_path = Path(
            snapshot_download(
                repo_id,
                repo_type="model",
                revision=revision,
                token=token,
                cache_dir=cache,
                local_files_only=local_files_only,
                allow_patterns=[f"{selected.path}/**", "policy.json"],
            )
        )
    except (
        HfHubHTTPError,
        LocalEntryNotFoundError,
        RepositoryNotFoundError,
        RevisionNotFoundError,
        OSError,
        ValueError,
    ) as exc:
        raise TurnModelDownloadError(
            f"cannot acquire {repo_id}@{revision} variant {variant!r}: {exc}"
        ) from exc

    policy_path = snapshot_path / "policy.json"
    if not policy_path.is_file():
        raise TurnBundleError(
            f"downloaded snapshot is missing policy metadata: {policy_path}"
        )
    return DownloadedBundle(
        bundle=verify_bundle(snapshot_path / selected.path),
        policy_path=policy_path,
        variant_path=selected.path,
        revision=revision,
    )
