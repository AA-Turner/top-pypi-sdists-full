"""Pure decoding and read-only snapshots for dispatch-state payloads."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

from agentic_devtools.cli.ci.canonical_dispatch_identity import CanonicalDispatchIdentity
from agentic_devtools.cli.ci.dispatch_state import _read_store, _validate_repo


@dataclass(frozen=True)
class DispatchStateEnvelope:
    """An immutable decoded envelope retaining both v2 record namespaces."""

    version: int | None
    records: Mapping[str, Mapping[str, Any]]
    canonical_records: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.version not in {None, 1, 2} or isinstance(self.version, bool):
            raise ValueError("dispatch state envelope version is invalid")
        if self.version != 2 and self.canonical_records:
            raise ValueError("canonical records require a v2 envelope")
        object.__setattr__(self, "records", self._freeze_mapping(self.records))
        object.__setattr__(self, "canonical_records", self._freeze_mapping(self.canonical_records))

    @classmethod
    def _freeze_json_value(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            if any(not isinstance(key, str) for key in value):
                raise ValueError("dispatch state values must use JSON object keys")
            return MappingProxyType({key: cls._freeze_json_value(item) for key, item in value.items()})
        if isinstance(value, (list, tuple)):
            return tuple(cls._freeze_json_value(item) for item in value)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        raise ValueError("dispatch state contains a non-JSON value")

    @classmethod
    def _freeze_mapping(cls, records: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Mapping[str, Any]]:
        if not isinstance(records, Mapping):
            raise ValueError("dispatch state records must be an object")
        return cls._freeze_json_value(records)

    @classmethod
    def _mutable_json_value(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {key: cls._mutable_json_value(item) for key, item in value.items()}
        if isinstance(value, tuple):
            return [cls._mutable_json_value(item) for item in value]
        return value

    def to_dict(self) -> dict[str, Any]:
        """Return a mutable JSON-compatible copy in the original envelope shape."""
        records = self._mutable_json_value(self.records)
        if self.version is None:
            return records
        envelope = {"version": self.version, "records": records}
        if self.version == 2:
            envelope["canonical_records"] = self._mutable_json_value(self.canonical_records)
        return envelope

    @classmethod
    def from_payload(cls, content: str) -> DispatchStateEnvelope:
        """Decode one complete payload while preserving its original envelope format."""

        def reject_constant(value: str) -> None:
            raise ValueError(f"dispatch state contains invalid JSON constant {value}")

        if not isinstance(content, str):
            raise ValueError("dispatch state content must be text")
        if not content.strip():
            raise ValueError("dispatch state file is blank")
        try:
            raw = json.loads(content, parse_constant=reject_constant)
        except json.JSONDecodeError as exc:
            raise ValueError("dispatch state is not valid JSON") from exc
        if not isinstance(raw, dict):
            raise ValueError("dispatch state records must be an object")
        if "version" not in raw and "records" not in raw:
            _read_store(content)
            return cls(None, raw)
        return cls._decode_versioned_payload(content, raw)

    @classmethod
    def _decode_versioned_payload(cls, content: str, raw: dict[str, Any]) -> DispatchStateEnvelope:
        version = raw.get("version")
        if isinstance(version, bool) or not isinstance(version, int):
            raise ValueError("dispatch state version is unsupported")
        if version == 1:
            if "canonical_records" in raw:
                raise ValueError("canonical records require a v2 envelope")
            _read_store(content)
            return cls(1, raw["records"])
        if version != 2:
            raise ValueError("dispatch state version is unsupported")
        return cls._decode_v2_payload(raw)

    @classmethod
    def _decode_v2_payload(cls, raw: dict[str, Any]) -> DispatchStateEnvelope:
        if set(raw) != {"version", "records", "canonical_records"}:
            raise ValueError("v2 dispatch state envelope has invalid properties")
        records = raw["records"]
        canonical_records = raw["canonical_records"]
        if not isinstance(records, dict) or not isinstance(canonical_records, dict):
            raise ValueError("v2 dispatch state records must be objects")

        legacy_content = json.dumps({"version": 1, "records": records})
        _read_store(legacy_content)
        validated_canonical_records = cls._validate_canonical_records(canonical_records)
        return cls(2, records, validated_canonical_records)

    @staticmethod
    def _validate_canonical_records(
        canonical_records: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        validated_records: dict[str, dict[str, Any]] = {}
        for key, raw_record in canonical_records.items():
            if not isinstance(raw_record, dict):
                raise ValueError("dispatch state contains an invalid canonical record")
            try:
                identity = CanonicalDispatchIdentity(
                    repo=raw_record["repo"],
                    pull_request_id=raw_record["pull_request_id"],
                    head_sha=raw_record["head_sha"],
                    review_id=raw_record["review_id"],
                    work_digest=raw_record["work_digest"],
                    ordinal=raw_record["ordinal"],
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError("dispatch state contains an invalid canonical record") from exc
            if key != identity.key:
                raise ValueError("dispatch state canonical record key does not match identity")
            validated_records[key] = raw_record
        return validated_records


@dataclass(frozen=True)
class DispatchStateSnapshot:
    """Filtered immutable records together with the complete decoded envelope."""

    records: Mapping[str, Mapping[str, Any]]
    canonical_records: Mapping[str, Mapping[str, Any]]
    envelope: DispatchStateEnvelope

    def __post_init__(self) -> None:
        object.__setattr__(self, "records", DispatchStateEnvelope._freeze_mapping(self.records))
        object.__setattr__(
            self,
            "canonical_records",
            DispatchStateEnvelope._freeze_mapping(self.canonical_records),
        )


def decode_dispatch_state_payload(content: str) -> DispatchStateEnvelope:
    """Validate and decode a flat, v1, or v2 dispatch-state payload without I/O."""
    return DispatchStateEnvelope.from_payload(content)


def read_dispatch_state_snapshot(
    path: Path,
    *,
    legacy_repo: str,
    canonical_repo: str,
    pull_request_id: int,
    head_sha: str,
) -> DispatchStateSnapshot:
    """Read one file and return independently filtered, immutable namespace snapshots."""
    legacy_repo = _validate_repo(legacy_repo)
    selector = CanonicalDispatchIdentity(
        repo=canonical_repo,
        pull_request_id=pull_request_id,
        head_sha=head_sha,
        review_id=0,
        work_digest="0" * 64,
        ordinal=1,
    )
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        envelope = DispatchStateEnvelope(None, {})
        return DispatchStateSnapshot({}, {}, envelope)
    envelope = decode_dispatch_state_payload(content)
    legacy_records = {
        key: record
        for key, record in envelope.records.items()
        if record["repo"] == legacy_repo and record["pull_request_id"] == pull_request_id and record["sha"] == head_sha
    }
    canonical_records = {
        key: record
        for key, record in envelope.canonical_records.items()
        if record["repo"] == selector.repo
        and record["pull_request_id"] == selector.pull_request_id
        and record["head_sha"] == selector.head_sha
    }
    return DispatchStateSnapshot(legacy_records, canonical_records, envelope)
