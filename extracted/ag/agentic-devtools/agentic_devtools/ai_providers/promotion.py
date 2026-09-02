import hashlib
import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, cast

from ..file_locking import locked_file
from .errors import ProviderError
from .serialization import freeze_json, thaw_json

_CANONICAL_META_NAME = "meta-canonical.json"
_CANONICAL_BODY_NAME = "body-canonical.md"
_MANIFEST_NAME = "promotion-manifest.json"
_PROMOTED_META_TEMPLATE = "meta-promoted-r{round_id}.json"
_PROMOTED_BODY_TEMPLATE = "body-promoted-r{round_id}.md"
_MANIFEST_STATUSES = frozenset({"accepted", "rejected", "pending"})
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_MANIFEST_FIELDS = frozenset(
    {"round_id", "meta_path", "body_path", "meta_sha256", "body_sha256", "status", "verification_timestamp"}
)


@dataclass(frozen=True)
class PromotionManifest:
    round_id: int
    meta_path: str
    body_path: str
    meta_sha256: str
    body_sha256: str
    status: Literal["accepted", "rejected", "pending"]
    verification_timestamp: str


def compute_sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _compute_sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _write_temp_bytes(target: Path, content: bytes) -> Path:
    temp_path = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        temp_path.write_bytes(content)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path


def _replace_file(source: Path, target: Path) -> None:
    source.replace(target)


def _restore_file(target: Path, previous_content: bytes | None) -> None:
    if previous_content is None:
        target.unlink(missing_ok=True)
        return
    target.write_bytes(previous_content)


def _require_iso8601_timestamp(field_name: str, value: object) -> str:
    if not isinstance(value, str) or "T" not in value:
        raise ProviderError(
            f"{field_name} must be a valid ISO-8601 timestamp.",
            category="validation_error",
        )

    normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ProviderError(
            f"{field_name} must be a valid ISO-8601 timestamp.",
            category="validation_error",
        ) from exc
    return value


def _require_round_id(round_id: object) -> int:
    if isinstance(round_id, bool) or not isinstance(round_id, int):
        raise ProviderError("round_id must be a non-bool integer.", category="validation_error")
    return round_id


def _canonicalize_meta_content(meta_content: str) -> str:
    try:
        parsed = json.loads(meta_content)
    except json.JSONDecodeError as exc:
        raise ProviderError("meta_content must be valid JSON.", category="validation_error") from exc
    if not isinstance(parsed, dict):
        raise ProviderError("meta_content must decode to a JSON object.", category="validation_error")

    canonical = thaw_json(freeze_json(parsed))
    return json.dumps(canonical, indent=2, sort_keys=True)


def _publish_bytes_atomically(contents_by_target: dict[Path, bytes]) -> None:
    previous_contents = {target: target.read_bytes() if target.exists() else None for target in contents_by_target}
    staged_paths: list[tuple[Path, Path]] = []
    replaced_targets: list[Path] = []
    try:
        for target, content in contents_by_target.items():
            temp_path = _write_temp_bytes(target, content)
            staged_paths.append((target, temp_path))

        for target, temp_path in staged_paths:
            _replace_file(temp_path, target)
            replaced_targets.append(target)
    except Exception:
        for target in reversed(replaced_targets):
            _restore_file(target, previous_contents[target])
        raise
    finally:
        for _, temp_path in staged_paths:
            temp_path.unlink(missing_ok=True)


def _parse_manifest(payload: object) -> PromotionManifest:
    if not isinstance(payload, dict):
        raise ProviderError("Promotion manifest must be a JSON object.", category="validation_error")

    unknown_fields = set(payload.keys()) - _MANIFEST_FIELDS
    if unknown_fields:
        raise ProviderError(
            f"Promotion manifest contains unknown fields: {', '.join(sorted(unknown_fields))}.",
            category="validation_error",
        )

    round_id = payload.get("round_id")
    if not isinstance(round_id, int) or isinstance(round_id, bool):
        raise ProviderError("round_id must be an integer.", category="validation_error")

    meta_path = payload.get("meta_path")
    body_path = payload.get("body_path")
    if meta_path != _CANONICAL_META_NAME or body_path != _CANONICAL_BODY_NAME:
        raise ProviderError(
            "Manifest must reference canonical filenames only.",
            category="validation_error",
        )

    meta_sha256 = payload.get("meta_sha256")
    if not isinstance(meta_sha256, str) or not _SHA256_PATTERN.fullmatch(meta_sha256):
        raise ProviderError(
            "meta_sha256 must be a 64-character lowercase hex digest.",
            category="validation_error",
        )

    body_sha256 = payload.get("body_sha256")
    if not isinstance(body_sha256, str) or not _SHA256_PATTERN.fullmatch(body_sha256):
        raise ProviderError(
            "body_sha256 must be a 64-character lowercase hex digest.",
            category="validation_error",
        )

    status = payload.get("status")
    if not isinstance(status, str) or status not in _MANIFEST_STATUSES:
        raise ProviderError(
            f"status must be one of: {', '.join(sorted(_MANIFEST_STATUSES))}.",
            category="validation_error",
        )

    verification_timestamp = _require_iso8601_timestamp(
        "verification_timestamp",
        payload.get("verification_timestamp"),
    )

    return PromotionManifest(
        round_id=round_id,
        meta_path=meta_path,
        body_path=body_path,
        meta_sha256=meta_sha256,
        body_sha256=body_sha256,
        status=cast(Literal["accepted", "rejected", "pending"], status),
        verification_timestamp=verification_timestamp,
    )


class DraftManager:
    """
    Manages round-local drafts and canonical pair promotion.
    """

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def get_meta_draft_path(self, round_id: int) -> Path:
        validated = _require_round_id(round_id)
        return self.output_dir / f"meta-draft-r{validated}.json"

    def get_body_draft_path(self, round_id: int) -> Path:
        validated = _require_round_id(round_id)
        return self.output_dir / f"body-draft-r{validated}.md"

    def get_canonical_meta_path(self) -> Path:
        return self.output_dir / _CANONICAL_META_NAME

    def get_canonical_body_path(self) -> Path:
        return self.output_dir / _CANONICAL_BODY_NAME

    def get_manifest_path(self) -> Path:
        return self.output_dir / _MANIFEST_NAME

    def _get_promoted_meta_path(self, round_id: int) -> Path:
        validated = _require_round_id(round_id)
        return self.output_dir / _PROMOTED_META_TEMPLATE.format(round_id=validated)

    def _get_promoted_body_path(self, round_id: int) -> Path:
        validated = _require_round_id(round_id)
        return self.output_dir / _PROMOTED_BODY_TEMPLATE.format(round_id=validated)

    def _publication_lock_path(self) -> Path:
        return self.output_dir / f"{_MANIFEST_NAME}.lock"

    def save_drafts(self, round_id: int, meta_content: str, body_content: str) -> None:
        with locked_file(self._publication_lock_path(), mode="a+", exclusive=True):
            self.output_dir.mkdir(parents=True, exist_ok=True)
            _publish_bytes_atomically(
                {
                    self.get_meta_draft_path(round_id): _canonicalize_meta_content(meta_content).encode("utf-8"),
                    self.get_body_draft_path(round_id): body_content.encode("utf-8"),
                }
            )

    def promote_drafts(self, round_id: int) -> PromotionManifest:
        """
        Promotes the round-local drafts to the canonical pair and retains
        round-bound copies for later verification.
        """
        with locked_file(self._publication_lock_path(), mode="a+", exclusive=True):
            meta_draft = self.get_meta_draft_path(round_id)
            body_draft = self.get_body_draft_path(round_id)

            if not meta_draft.exists() or not body_draft.exists():
                raise ProviderError(f"Drafts for round {round_id} do not exist.", category="validation_error")

            canonical_meta = self.get_canonical_meta_path()
            canonical_body = self.get_canonical_body_path()
            manifest_path = self.get_manifest_path()
            promoted_meta = self._get_promoted_meta_path(round_id)
            promoted_body = self._get_promoted_body_path(round_id)

            new_meta_bytes = meta_draft.read_bytes()
            new_body_bytes = body_draft.read_bytes()
            verification_timestamp = datetime.now(timezone.utc).isoformat()

            manifest = PromotionManifest(
                round_id=round_id,
                meta_path=canonical_meta.name,
                body_path=canonical_body.name,
                meta_sha256=_compute_sha256_bytes(new_meta_bytes),
                body_sha256=_compute_sha256_bytes(new_body_bytes),
                status="accepted",
                verification_timestamp=verification_timestamp,
            )

            manifest_content = json.dumps(
                {
                    "round_id": manifest.round_id,
                    "meta_path": manifest.meta_path,
                    "body_path": manifest.body_path,
                    "meta_sha256": manifest.meta_sha256,
                    "body_sha256": manifest.body_sha256,
                    "status": manifest.status,
                    "verification_timestamp": manifest.verification_timestamp,
                },
                indent=2,
            )

            if promoted_meta.exists() and compute_sha256(promoted_meta) != manifest.meta_sha256:
                raise ProviderError(
                    f"Round {round_id} promoted metadata does not match the current drafts.",
                    category="logic_error",
                )
            if promoted_body.exists() and compute_sha256(promoted_body) != manifest.body_sha256:
                raise ProviderError(
                    f"Round {round_id} promoted body does not match the current drafts.",
                    category="logic_error",
                )

            _publish_bytes_atomically(
                {
                    promoted_meta: new_meta_bytes,
                    promoted_body: new_body_bytes,
                    canonical_meta: new_meta_bytes,
                    canonical_body: new_body_bytes,
                    manifest_path: manifest_content.encode("utf-8"),
                }
            )

            return manifest

    def verify_canonical_pair(self) -> PromotionManifest:
        with locked_file(self._publication_lock_path(), mode="a+", exclusive=True):
            manifest_path = self.get_manifest_path()
            if not manifest_path.exists():
                raise ProviderError("Promotion manifest does not exist.", category="validation_error")

            try:
                manifest = _parse_manifest(json.loads(manifest_path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ProviderError(
                    "Promotion manifest must be a valid UTF-8 encoded JSON file.",
                    category="validation_error",
                ) from exc
            if manifest.status != "accepted":
                raise ProviderError(
                    "Promotion manifest status must be accepted.",
                    category="validation_error",
                )

            canonical_meta = self.output_dir / manifest.meta_path
            canonical_body = self.output_dir / manifest.body_path

            if not canonical_meta.exists() or not canonical_body.exists():
                raise ProviderError("Canonical files missing.", category="logic_error")

            current_meta_sha256 = compute_sha256(canonical_meta)
            current_body_sha256 = compute_sha256(canonical_body)

            if current_meta_sha256 != manifest.meta_sha256 or current_body_sha256 != manifest.body_sha256:
                raise ProviderError(
                    "Canonical files do not match manifest hashes (mixed-round or modified).",
                    category="logic_error",
                )

            promoted_meta = self._get_promoted_meta_path(manifest.round_id)
            promoted_body = self._get_promoted_body_path(manifest.round_id)
            if not promoted_meta.exists() or not promoted_body.exists():
                raise ProviderError(
                    f"Promoted round {manifest.round_id} files are missing.",
                    category="logic_error",
                )

            if (
                compute_sha256(promoted_meta) != current_meta_sha256
                or compute_sha256(promoted_body) != current_body_sha256
            ):
                raise ProviderError(
                    f"Canonical files do not match promoted round {manifest.round_id}.",
                    category="logic_error",
                )

            return manifest
