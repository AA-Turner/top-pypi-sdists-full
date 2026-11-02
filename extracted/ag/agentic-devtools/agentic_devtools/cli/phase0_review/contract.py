"""Versioned input-contract and integrity validation."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from agentic_devtools.cli.issue_template.type_resolver import slugify_type
from agentic_devtools.cli.phase0_review.config import (
    MAX_BODY_BYTES,
    MAX_COLLECTION_ITEMS,
    MAX_COLLECTION_MEMBER_CHARACTERS,
    MAX_ISSUE_MD_BYTES,
    MAX_JSON_DEPTH,
    MAX_PAYLOAD_BYTES,
    MAX_PROPERTIES,
    MAX_PROPERTY_KEY_CHARACTERS,
    MAX_PROPERTY_RENDERED_CHARACTERS,
    MAX_SNAPSHOT_BYTES,
    MAX_STRING_CHARACTERS,
    MAX_TEMPLATE_BYTES,
    MAX_TITLE_CHARACTERS,
    RESERVED_PROPERTY_NAMES,
    SCHEMA_VERSION,
    TRUNCATION_THRESHOLD_BYTES,
)
from agentic_devtools.cli.phase0_review.helpers import coerce_value, resolve_safe_path
from agentic_devtools.cli.phase0_review.report import Finding, malformed_input, missing_input

_ASCII_WHITESPACE = " \t\r\n\v\f"
_HEX = re.compile(r"^[0-9a-f]{64}$")
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$")
_SOURCE_REQUIRED = {
    "provider",
    "issue_id",
    "title",
    "status",
    "body",
    "url",
    "created_at",
    "updated_at",
    "labels",
    "dependencies",
    "constraints",
    "type",
    "truncated",
    "original_size",
}
_SOURCE_OPTIONAL = {"priority", "assignees", "milestone", "properties"}
_NONEMPTY_STRINGS = {"provider", "issue_id", "title", "status", "url", "type"}
_ARRAY_FIELDS = {"labels", "dependencies", "constraints", "assignees"}
_IDENTIFIER_SEGMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass
class ContractResult:
    """Loaded contract, validated artifact paths, and exhaustive input findings."""

    data: dict[str, Any] | None = None
    payload_bytes: bytes | None = None
    paths: dict[str, Path] = field(default_factory=dict)
    artifact_bytes: dict[str, bytes] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)


class _JSONObjectPairs(list[tuple[str, Any]]):
    """Marker type that preserves object pairs during decoding."""


def _json_member_path(parent: str, key: str) -> str:
    if _IDENTIFIER_SEGMENT.fullmatch(key):
        return f"{parent}.{key}"
    return f"{parent}[{json.dumps(key, ensure_ascii=False)}]"


def _materialize_json(value: Any, *, duplicates: list[str], path: str = "$") -> Any:
    if isinstance(value, _JSONObjectPairs):
        result: dict[str, Any] = {}
        for key, member in value:
            member_path = _json_member_path(path, key)
            if key in result:
                duplicates.append(member_path)
            result[key] = _materialize_json(member, duplicates=duplicates, path=member_path)
        return result
    if isinstance(value, list):
        return [
            _materialize_json(member, duplicates=duplicates, path=f"{path}[{index}]")
            for index, member in enumerate(value)
        ]
    return value


def _json_depth(value: Any) -> int:
    if isinstance(value, dict):
        return 1 + max((_json_depth(item) for item in value.values()), default=0)
    if isinstance(value, list):
        return 1 + max((_json_depth(item) for item in value), default=0)
    return 0


def load_contract(path: Path, *, label: str = "factual-review payload") -> ContractResult:
    """Read bounded UTF-8 JSON and detect duplicate members at every level."""
    result = ContractResult()
    try:
        raw = path.read_bytes()
    except OSError as exc:
        result.findings.append(missing_input(label, f"unreadable: {exc}"))
        return result
    result.payload_bytes = raw
    if len(raw) > MAX_PAYLOAD_BYTES:
        result.findings.append(
            malformed_input(
                f"{label} is at most {MAX_PAYLOAD_BYTES} bytes",
                f"found {len(raw)} bytes",
            )
        )
        return result
    duplicates: list[str] = []
    try:
        text = raw.decode("utf-8")
        data = json.loads(
            text,
            object_pairs_hook=_JSONObjectPairs,
            parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid constant {value}")),
        )
        data = _materialize_json(data, duplicates=duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        result.findings.append(malformed_input(f"{label} is valid UTF-8 JSON", str(exc)))
        return result
    for member_path in duplicates:
        result.findings.append(
            malformed_input(
                f"{label} has unique JSON member names",
                f"duplicate member {member_path}",
            )
        )
    if not isinstance(data, dict):
        result.findings.append(malformed_input(f"{label} is an object", f"found {type(data).__name__}"))
        return result
    result.data = data
    depth = _json_depth(data)
    if depth > MAX_JSON_DEPTH:
        result.findings.append(
            malformed_input(
                f"JSON nesting depth is at most {MAX_JSON_DEPTH}",
                f"found depth {depth}",
            )
        )
    return result


def _add_type(findings: list[Finding], field_name: str, expected: str, value: Any) -> None:
    findings.append(malformed_input(f"{field_name} is {expected}", f"found {type(value).__name__}"))


def _validate_string(
    findings: list[Finding],
    field_name: str,
    value: Any,
    *,
    nonempty: bool,
    maximum: int | None = None,
) -> bool:
    if not isinstance(value, str):
        _add_type(findings, field_name, "a string", value)
        return False
    if nonempty and not value.strip(_ASCII_WHITESPACE):
        findings.append(malformed_input(f"{field_name} is non-empty after trimming", "found empty value"))
    if maximum is not None and len(value) > maximum:
        findings.append(
            malformed_input(
                f"{field_name} is at most {maximum} characters",
                f"found {len(value)} characters",
            )
        )
    return True


def _validate_array(findings: list[Finding], field_name: str, value: Any) -> int:
    if not isinstance(value, list):
        _add_type(findings, field_name, "an array", value)
        return 0
    for index, member in enumerate(value):
        member_name = f"{field_name}[{index}]"
        if not isinstance(member, str):
            _add_type(findings, member_name, "a string", member)
        elif not member.strip(_ASCII_WHITESPACE):
            findings.append(malformed_input(f"{member_name} is non-empty after trimming", "found empty value"))
        elif len(member) > MAX_COLLECTION_MEMBER_CHARACTERS:
            findings.append(
                malformed_input(
                    f"{member_name} is at most 500 characters",
                    f"found {len(member)} characters",
                )
            )
    return len(value)


def _validate_properties(findings: list[Finding], source: dict[str, Any]) -> int:
    properties = source.get("properties")
    if properties is None and "properties" not in source:
        return 0
    if not isinstance(properties, dict):
        _add_type(findings, "source.properties", "an object", properties)
        return 0
    if len(properties) > MAX_PROPERTIES:
        findings.append(malformed_input("source.properties has at most 50 entries", f"found {len(properties)} entries"))
    item_count = 0
    for key, value in properties.items():
        field_name = f"source.properties.{key}"
        if len(key) > MAX_PROPERTY_KEY_CHARACTERS:
            findings.append(
                malformed_input(f"{field_name} key is at most 128 characters", f"found {len(key)} characters")
            )
        if key in RESERVED_PROPERTY_NAMES or key in source:
            findings.append(malformed_input(f"{field_name} does not collide with a reserved field", "name collision"))
        if isinstance(value, (dict, tuple)) or not isinstance(value, (str, int, float, bool, list, type(None))):
            findings.append(
                malformed_input(f"{field_name} is a supported scalar or scalar array", "unsupported value shape")
            )
            continue
        if isinstance(value, float) and not math.isfinite(value):
            findings.append(malformed_input(f"{field_name} is a finite number", f"found {value!r}"))
            continue
        if isinstance(value, list):
            item_count += len(value)
            if len(value) > MAX_COLLECTION_ITEMS:
                findings.append(malformed_input(f"{field_name} has at most 50 members", f"found {len(value)} members"))
            for index, member in enumerate(value):
                if member is None or isinstance(member, (dict, list)):
                    findings.append(
                        malformed_input(
                            f"{field_name}[{index}] is a non-null scalar",
                            f"found {type(member).__name__}",
                        )
                    )
                elif isinstance(member, str):
                    if not member.strip(_ASCII_WHITESPACE):
                        findings.append(
                            malformed_input(f"{field_name}[{index}] is non-empty after trimming", "found empty value")
                        )
                    if len(member) > MAX_COLLECTION_MEMBER_CHARACTERS:
                        findings.append(
                            malformed_input(
                                f"{field_name}[{index}] is at most 500 characters",
                                f"found {len(member)} characters",
                            )
                        )
                elif isinstance(member, float) and not math.isfinite(member):
                    findings.append(malformed_input(f"{field_name}[{index}] is finite", f"found {member!r}"))
                elif len(coerce_value(member)) > MAX_COLLECTION_MEMBER_CHARACTERS:
                    findings.append(
                        malformed_input(
                            f"{field_name}[{index}] renders to at most 500 characters",
                            f"found {len(coerce_value(member))} characters",
                        )
                    )
        rendered = coerce_value(value)
        if len(rendered) > MAX_PROPERTY_RENDERED_CHARACTERS:
            findings.append(
                malformed_input(
                    f"{field_name} renders to at most 1024 characters",
                    f"found {len(rendered)} characters",
                )
            )
    return item_count


def validate_schema(data: dict[str, Any]) -> list[Finding]:
    """Validate all discoverable FR-009a schema and bounded-input conditions."""
    findings: list[Finding] = []
    allowed_top = {"schema_version", "source", "issue_md", "template"}
    for name in sorted(data.keys() - allowed_top):
        findings.append(malformed_input("known top-level members only", f"unknown top-level member {name!r}"))
    for name in sorted(allowed_top - data.keys()):
        findings.append(malformed_input(f"required member {name!r}", "member is missing"))
    if "schema_version" in data and data["schema_version"] != SCHEMA_VERSION:
        findings.append(
            malformed_input(
                f"schema_version equals {SCHEMA_VERSION!r}",
                f"found {data['schema_version']!r}",
            )
        )
    source = data.get("source")
    if not isinstance(source, dict):
        _add_type(findings, "source", "an object", source)
        source = {}
    for name in sorted(source.keys() - (_SOURCE_REQUIRED | _SOURCE_OPTIONAL)):
        findings.append(malformed_input("known source members only", f"unknown source member {name!r}"))
    for name in sorted(_SOURCE_REQUIRED - source.keys()):
        findings.append(malformed_input(f"required member source.{name}", "member is missing"))

    string_fields = (
        _NONEMPTY_STRINGS | {"body", "created_at", "updated_at"} | ({"priority", "milestone"} & source.keys())
    )
    for name in sorted(string_fields):
        if name not in source:
            continue
        maximum = MAX_TITLE_CHARACTERS if name == "title" else MAX_STRING_CHARACTERS if name != "body" else None
        valid = _validate_string(
            findings,
            f"source.{name}",
            source[name],
            nonempty=name in _NONEMPTY_STRINGS,
            maximum=maximum,
        )
        if valid and name == "body" and len(source[name].encode("utf-8")) > MAX_BODY_BYTES:
            findings.append(
                malformed_input(
                    "source.body is at most 102400 UTF-8 bytes",
                    f"found {len(source[name].encode('utf-8'))} bytes",
                )
            )
    item_count = 0
    for name in sorted(_ARRAY_FIELDS):
        if name in source:
            item_count += _validate_array(findings, f"source.{name}", source[name])
    item_count += _validate_properties(findings, source)
    if item_count > MAX_COLLECTION_ITEMS:
        findings.append(
            malformed_input(
                "total collection item count is at most 50",
                f"found {item_count} items",
            )
        )

    if "truncated" in source and not isinstance(source["truncated"], bool):
        _add_type(findings, "source.truncated", "a boolean", source["truncated"])
    original_size = source.get("original_size")
    if not isinstance(original_size, int) or isinstance(original_size, bool) or original_size < 0:
        findings.append(malformed_input("source.original_size is a non-negative integer", f"found {original_size!r}"))
    body = source.get("body")
    truncated = source.get("truncated")
    if isinstance(body, str) and isinstance(original_size, int) and not isinstance(original_size, bool):
        body_size = len(body.encode("utf-8"))
        if truncated is False and original_size != body_size:
            findings.append(
                malformed_input(
                    "source.original_size equals source.body UTF-8 byte length when untruncated",
                    f"found original_size={original_size}, body_size={body_size}",
                )
            )
        if truncated is True:
            if original_size <= body_size:
                findings.append(
                    malformed_input(
                        "source.original_size exceeds truncated body size",
                        f"found original_size={original_size}, body_size={body_size}",
                    )
                )
            if original_size <= TRUNCATION_THRESHOLD_BYTES:
                findings.append(
                    malformed_input(
                        "source.original_size exceeds 102400 when truncated",
                        f"found {original_size}",
                    )
                )
    provider = source.get("provider")
    url = source.get("url")
    if isinstance(provider, str) and isinstance(url, str) and url:
        parsed = urlparse(url)
        if provider == "markdown":
            if Path(url).is_absolute() or parsed.scheme:
                findings.append(malformed_input("source.url is repository-relative for markdown", f"found {url!r}"))
        elif not parsed.scheme or not parsed.netloc:
            findings.append(malformed_input("source.url is an absolute URL", f"found {url!r}"))
    for name in ("created_at", "updated_at"):
        value = source.get(name)
        if isinstance(value, str) and value and not _TIMESTAMP.fullmatch(value):
            findings.append(malformed_input(f"source.{name} is ISO 8601 extended format", f"found {value!r}"))
        elif isinstance(value, str) and value:
            try:
                normalized = re.sub(r"([+-])(\d{2})(\d{2})$", r"\1\2:\3", value).replace("Z", "+00:00")
                datetime.fromisoformat(normalized)
            except ValueError:
                findings.append(malformed_input(f"source.{name} is a valid timestamp", f"found {value!r}"))
    source_type = source.get("type")
    if isinstance(source_type, str) and source_type and slugify_type(source_type) != source_type:
        findings.append(malformed_input("source.type is a normalized slug", f"found {source_type!r}"))

    issue_md = data.get("issue_md")
    template = data.get("template")
    if not isinstance(issue_md, dict):
        _add_type(findings, "issue_md", "an object", issue_md)
    else:
        for name in sorted(issue_md.keys() - {"path"}):
            findings.append(malformed_input("known issue_md members only", f"unknown issue_md member {name!r}"))
        if "path" not in issue_md:
            findings.append(malformed_input("required member issue_md.path", "member is missing"))
        elif _validate_string(
            findings, "issue_md.path", issue_md["path"], nonempty=True, maximum=MAX_STRING_CHARACTERS
        ):
            if not issue_md["path"].endswith("issue.md"):
                findings.append(malformed_input("issue_md.path ends in issue.md", f"found {issue_md['path']!r}"))
    if not isinstance(template, dict):
        _add_type(findings, "template", "an object", template)
    else:
        allowed_template = {"selected_path", "structure_snapshot_path"}
        for name in sorted(template.keys() - allowed_template):
            findings.append(malformed_input("known template members only", f"unknown template member {name!r}"))
        for name in allowed_template:
            if name not in template:
                findings.append(malformed_input(f"required member template.{name}", "member is missing"))
            else:
                _validate_string(
                    findings,
                    f"template.{name}",
                    template[name],
                    nonempty=True,
                    maximum=MAX_STRING_CHARACTERS,
                )
    return findings


def validate_paths(data: dict[str, Any], repo_root: Path) -> tuple[dict[str, Path], list[Finding]]:
    """Resolve contract artifact paths and validate regular files and bounds."""
    paths: dict[str, Path] = {}
    findings: list[Finding] = []
    specifications = (
        ("issue_md.path", data.get("issue_md"), "path", MAX_ISSUE_MD_BYTES),
        ("template.selected_path", data.get("template"), "selected_path", MAX_TEMPLATE_BYTES),
        (
            "template.structure_snapshot_path",
            data.get("template"),
            "structure_snapshot_path",
            MAX_SNAPSHOT_BYTES,
        ),
    )
    for label, container, member, maximum in specifications:
        if not isinstance(container, dict) or not isinstance(container.get(member), str):
            continue
        path, error = resolve_safe_path(container[member], repo_root, require_relative=True)
        if error:
            findings.append(malformed_input(f"{label} is a safe repository path", error))
            continue
        if path is None:
            findings.append(malformed_input(f"{label} is a safe repository path", "path was not resolved"))
            continue
        try:
            if not path.exists():
                findings.append(missing_input(label, "file does not exist"))
                continue
            if not path.is_file():
                findings.append(malformed_input(f"{label} resolves to a regular file", f"found {path}"))
                continue
            size = path.stat().st_size
        except OSError as exc:
            findings.append(missing_input(label, f"unreadable: {exc}"))
            continue
        if size > maximum:
            findings.append(malformed_input(f"{label} is at most {maximum} bytes", f"found {size} bytes"))
            continue
        paths[label] = path
    return paths, findings


def validate_integrity(
    integrity_path: Path,
    payload_bytes: bytes,
    artifact_bytes: Mapping[str, bytes] | None,
) -> list[Finding]:
    """Validate exact integrity schema and raw-byte SHA-256 digests."""
    findings: list[Finding] = []
    loaded = load_contract(integrity_path, label="integrity metadata")
    if loaded.data is None:
        return loaded.findings
    findings.extend(loaded.findings)
    data = loaded.data
    expected_members = {"payload_sha256", "selected_template_sha256", "snapshot_sha256"}
    for name in sorted(expected_members - data.keys()):
        findings.append(malformed_input(f"integrity member {name}", "member is missing"))
    for name in sorted(data.keys() - expected_members):
        findings.append(malformed_input("known integrity members only", f"unknown integrity member {name!r}"))
    for name in expected_members & data.keys():
        if not isinstance(data[name], str) or not _HEX.fullmatch(data[name]):
            findings.append(malformed_input(f"integrity {name} is lowercase 64-hex", f"found {data[name]!r}"))
    artifact_map = artifact_bytes if isinstance(artifact_bytes, Mapping) else {}
    actual_bytes = {
        "payload_sha256": payload_bytes,
        "selected_template_sha256": artifact_map.get("template.selected_path"),
        "snapshot_sha256": artifact_map.get("template.structure_snapshot_path"),
    }
    for name, raw in actual_bytes.items():
        expected = data.get(name)
        if raw is not None and isinstance(expected, str) and _HEX.fullmatch(expected):
            actual = hashlib.sha256(raw).hexdigest()
            if actual != expected:
                findings.append(malformed_input(f"integrity {name} matches raw bytes", f"found digest {actual}"))
    return findings
