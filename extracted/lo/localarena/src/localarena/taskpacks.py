"""Versioned, content-addressed task packs and JSONL interoperability."""

from __future__ import annotations

import hashlib
import json
import math
import struct
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from .generation import (
    ChatMessage,
    _freeze_json_object,
    _thaw_json,
)
from .tasks import PromptTask, TextMatch, evaluator_from_config

TASK_PACK_SCHEMA_VERSION = 1
_PACK_FIELDS = {
    "$schema",
    "schema_version",
    "name",
    "version",
    "description",
    "license",
    "source",
    "tasks",
    "digest",
    "format",
}
_TASK_FIELDS = {
    "id",
    "prompt",
    "system",
    "messages",
    "evaluator",
    "metadata",
}
_SOURCE_FORMATS = {
    "localarena",
    "localarena-jsonl",
    "openai-evals-jsonl",
}


class _DuplicateJSONKeyError(ValueError):
    """Raised when textual JSON has an ambiguous object member."""


def _unique_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise _DuplicateJSONKeyError(
                f"JSON object contains duplicate key {key!r}"
            )
        output[key] = value
    return output


def _require_text(value: object, field_name: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field_name} must be a string")
    normalized = _unicode_scalar_text(value)
    if not normalized or all(
        _portable_whitespace(character)
        for character in normalized
    ):
        raise ValueError(f"{field_name} must not be empty or whitespace")
    return normalized


def _code_point_key(value: str) -> tuple[int, ...]:
    return tuple(ord(character) for character in value)


def _unicode_scalar_text(value: str) -> str:
    """Normalize escaped surrogate pairs and reject unpaired surrogates."""

    try:
        return value.encode("utf-16", "surrogatepass").decode("utf-16")
    except UnicodeDecodeError as error:
        raise ValueError(
            "task pack strings must not contain unpaired Unicode surrogates"
        ) from error


def _portable_whitespace(character: str) -> bool:
    """Use the union of Python and JavaScript trimming whitespace."""

    code_point = ord(character)
    return (
        0x0009 <= code_point <= 0x000D
        or 0x001C <= code_point <= 0x0020
        or code_point
        in {
            0x0085,
            0x00A0,
            0x1680,
            0x2028,
            0x2029,
            0x202F,
            0x205F,
            0x3000,
            0xFEFF,
        }
        or 0x2000 <= code_point <= 0x200A
    )


def _normalize_pack_json(value: object) -> object:
    """Return JSON data with portable Unicode scalar strings and keys."""

    if type(value) is str:
        return _unicode_scalar_text(value)
    if isinstance(value, list):
        return [_normalize_pack_json(item) for item in value]
    if isinstance(value, Mapping):
        output: dict[str, object] = {}
        for key, item in value.items():
            if type(key) is not str:
                raise TypeError("task pack object keys must be strings")
            normalized_key = _unicode_scalar_text(key)
            if normalized_key in output:
                raise ValueError(
                    "task pack object keys must be unique Unicode strings"
                )
            output[normalized_key] = _normalize_pack_json(item)
        return output
    return value


def _canonical_value(value: object) -> str:
    """Encode JSON data identically in Python and JavaScript.

    Numbers use their interoperable IEEE-754 representation. Length prefixes
    make the encoding unambiguous without relying on runtime-specific JSON
    number formatting.
    """

    if value is None:
        return "z"
    if type(value) is bool:
        return "b1" if value else "b0"
    if type(value) in (int, float):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("task pack values must contain only finite numbers")
        if type(value) is int and abs(value) > (1 << 53) - 1:
            raise ValueError(
                "task pack integers must be within the interoperable safe range"
            )
        # JSON has one zero value, but JavaScript preserves the sign when it
        # parses the spelling ``-0`` while Python parses it as integer zero.
        if number == 0:
            number = 0.0
        return f"n{struct.pack('>d', number).hex()}"
    if type(value) is str:
        normalized = _unicode_scalar_text(value)
        encoded = normalized.encode("utf-8")
        return f"s{len(encoded)}:{normalized}"
    if isinstance(value, list):
        return f"a{len(value)}:" + "".join(
            _canonical_value(item) for item in value
        )
    if isinstance(value, Mapping):
        if any(type(key) is not str for key in value):
            raise TypeError("task pack object keys must be strings")
        normalized_items = [
            (_unicode_scalar_text(key), item)
            for key, item in value.items()
        ]
        normalized_keys = [key for key, _ in normalized_items]
        if len(set(normalized_keys)) != len(normalized_keys):
            raise ValueError(
                "task pack object keys must be unique Unicode strings"
            )
        normalized_items.sort(key=lambda item: _code_point_key(item[0]))
        return f"o{len(normalized_items)}:" + "".join(
            _canonical_value(key) + _canonical_value(item)
            for key, item in normalized_items
        )
    raise TypeError(
        "task pack values must contain only JSON-compatible values"
    )


def task_pack_digest(value: Mapping[str, object]) -> str:
    """Return a cross-runtime SHA-256 identity for one pack manifest."""

    normalized = _normalize_pack_json(
        _thaw_json(
            _freeze_json_object(value, field_name="task pack")
        )
    )
    if not isinstance(normalized, dict):
        raise TypeError("task pack must be an object")
    payload = {
        key: item
        for key, item in normalized.items()
        if key not in {"$schema", "digest", "format"}
    }
    canonical = _canonical_value(payload).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


@dataclass(frozen=True, slots=True)
class TaskPack:
    """A validated task collection with explicit provenance and identity."""

    name: str
    version: str
    license: str
    tasks: tuple[PromptTask, ...]
    digest: str
    format: str
    description: str = ""
    source: Mapping[str, object] = field(default_factory=dict)
    _manifest: Mapping[str, object] = field(
        default_factory=dict,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _require_text(self.name, "name"))
        object.__setattr__(
            self,
            "version",
            _require_text(self.version, "version"),
        )
        object.__setattr__(
            self,
            "license",
            _require_text(self.license, "license"),
        )
        digest = _require_text(self.digest, "digest")
        if (
            not digest.startswith("sha256:")
            or len(digest) != 71
            or any(
                character not in "0123456789abcdef"
                for character in digest[7:]
            )
        ):
            raise ValueError("digest must be a sha256: value")
        object.__setattr__(self, "digest", digest)
        source_format = _require_text(self.format, "format")
        if source_format not in _SOURCE_FORMATS:
            raise ValueError("format is invalid")
        object.__setattr__(self, "format", source_format)
        if type(self.description) is not str:
            raise TypeError("description must be a string")
        description = _unicode_scalar_text(self.description)
        object.__setattr__(self, "description", description)
        supplied_tasks = tuple(self.tasks)
        if (
            not supplied_tasks
            or not all(
                isinstance(task, PromptTask)
                for task in supplied_tasks
            )
        ):
            raise ValueError("tasks must contain one or more PromptTask values")
        normalized_tasks: list[PromptTask] = []
        for index, task in enumerate(supplied_tasks):
            normalized_row = _normalize_pack_json(
                _task_manifest_row(task)
            )
            if not isinstance(normalized_row, Mapping):
                raise TypeError("task pack tasks must normalize to objects")
            normalized_tasks.append(
                _task_from_row(
                    normalized_row,
                    field_name=f"tasks[{index}]",
                )
            )
        tasks = tuple(normalized_tasks)
        ids = [task.id for task in tasks]
        if len(ids) != len(set(ids)):
            raise ValueError("task pack task ids must be unique")
        normalized_source = _normalize_pack_json(
            _thaw_json(
                _freeze_json_object(self.source, field_name="source")
            )
        )
        if not isinstance(normalized_source, dict):
            raise TypeError("source must be an object")
        frozen_source = _freeze_json_object(
            normalized_source,
            field_name="source",
        )
        object.__setattr__(self, "source", frozen_source)
        manifest = (
            _normalize_pack_json(
                _thaw_json(
                    _freeze_json_object(
                        self._manifest,
                        field_name="task pack manifest",
                    )
                )
            )
            if self._manifest
            else _manifest_from_tasks(
                name=self.name,
                version=self.version,
                license_name=self.license,
                description=self.description,
                source=self.source,
                tasks=tasks,
            )
        )
        if not isinstance(manifest, dict):
            raise TypeError("task pack manifest must be an object")
        identity = _task_pack_manifest_identity(manifest)
        expected_identity = {
            "name": self.name,
            "version": self.version,
            "license": self.license,
            "description": self.description,
            "source": _thaw_json(self.source),
            "tasks": [_task_manifest_row(task) for task in tasks],
        }
        if _canonical_value(identity) != _canonical_value(expected_identity):
            raise ValueError(
                "manifest does not match the task pack fields and tasks"
            )
        for field_name, expected in (
            ("digest", self.digest),
            ("format", self.format),
        ):
            declared = manifest.get(field_name)
            if declared is not None and declared != expected:
                raise ValueError(
                    f"manifest {field_name} does not match the task pack"
                )
        manifest["digest"] = self.digest
        manifest["format"] = self.format
        if task_pack_digest(manifest) != self.digest:
            raise ValueError("digest does not match the task pack manifest")
        tasks_with_provenance = tuple(
            _with_pack_provenance(
                task,
                name=self.name,
                version=self.version,
                license_name=self.license,
                digest=self.digest,
                source_format=self.format,
                description=self.description,
                source=self.source,
            )
            for task in tasks
        )
        object.__setattr__(self, "tasks", tasks_with_provenance)
        object.__setattr__(
            self,
            "_manifest",
            _freeze_json_object(manifest, field_name="task pack manifest"),
        )

    def to_dict(self) -> dict[str, object]:
        """Return a detached, parseable manifest including task content."""

        manifest = _thaw_json(self._manifest)
        if not isinstance(manifest, dict):
            raise TypeError("task pack manifest must be an object")
        return manifest


def _task_manifest_row(task: PromptTask) -> dict[str, object]:
    row = task.to_dict()
    metadata = row.get("metadata")
    if isinstance(metadata, dict):
        metadata.pop("localarena_task_pack", None)
    return row


def _manifest_from_tasks(
    *,
    name: str,
    version: str,
    license_name: str,
    description: str,
    source: Mapping[str, object],
    tasks: Sequence[PromptTask],
) -> dict[str, object]:
    return {
        "schema_version": TASK_PACK_SCHEMA_VERSION,
        "name": name,
        "version": version,
        "description": description,
        "license": license_name,
        "source": _thaw_json(source),
        "tasks": [_task_manifest_row(task) for task in tasks],
    }


def _chat_messages(value: object, field_name: str) -> tuple[ChatMessage, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field_name} must be a non-empty array")
    messages: list[ChatMessage] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise TypeError(f"{field_name}[{index}] must be an object")
        if set(item) != {"role", "content"}:
            raise ValueError(
                f"{field_name}[{index}] must contain exactly role and content"
            )
        messages.append(
            ChatMessage(
                role=item.get("role"),  # type: ignore[arg-type]
                content=item.get("content"),  # type: ignore[arg-type]
            )
        )
    return tuple(messages)


def _task_from_row(
    value: Mapping[str, object],
    *,
    field_name: str,
) -> PromptTask:
    extra = sorted(set(value) - _TASK_FIELDS)
    if extra:
        raise ValueError(
            f"{field_name} contains unsupported fields: {', '.join(extra)}"
        )
    task_id = _require_text(value.get("id"), f"{field_name}.id")
    evaluator = evaluator_from_config(value.get("evaluator"))  # type: ignore[arg-type]
    metadata = value.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise TypeError(f"{field_name}.metadata must be an object")
    if "messages" in value:
        messages = value.get("messages")
        if "prompt" in value or "system" in value:
            raise ValueError(
                f"{field_name} must use either messages or prompt/system"
            )
        return PromptTask(
            id=task_id,
            messages=_chat_messages(messages, f"{field_name}.messages"),
            evaluator=evaluator,
            metadata=metadata,
        )
    if "prompt" not in value:
        raise ValueError(f"{field_name} must contain prompt or messages")
    prompt = value.get("prompt")
    if type(prompt) is not str:
        raise TypeError(f"{field_name}.prompt must be a string")
    system = value.get("system")
    if system is not None and type(system) is not str:
        raise TypeError(f"{field_name}.system must be a string or null")
    return PromptTask.from_text(
        task_id,
        prompt,
        system=system,
        evaluator=evaluator,
        metadata=metadata,
    )


def _task_pack_manifest_identity(
    manifest: Mapping[str, object],
) -> dict[str, object]:
    extra = sorted(set(manifest) - _PACK_FIELDS)
    if extra:
        raise ValueError(
            f"task pack manifest contains unsupported fields: "
            f"{', '.join(extra)}"
        )
    if (
        type(manifest.get("schema_version")) is not int
        or manifest.get("schema_version") != TASK_PACK_SCHEMA_VERSION
    ):
        raise ValueError("task pack manifest schema_version must be 1")
    schema_uri = manifest.get("$schema")
    if schema_uri is not None:
        _require_text(schema_uri, "task pack manifest $schema")
    name = _require_text(manifest.get("name"), "task pack manifest name")
    version = _require_text(
        manifest.get("version"),
        "task pack manifest version",
    )
    license_name = _require_text(
        manifest.get("license"),
        "task pack manifest license",
    )
    description = manifest.get("description", "")
    if type(description) is not str:
        raise TypeError("task pack manifest description must be a string")
    source = manifest.get("source", {})
    if not isinstance(source, Mapping):
        raise TypeError("task pack manifest source must be an object")
    rows = manifest.get("tasks")
    if not isinstance(rows, list) or not rows:
        raise ValueError(
            "task pack manifest tasks must be a non-empty array"
        )
    if not all(isinstance(row, Mapping) for row in rows):
        raise TypeError(
            "task pack manifest tasks must contain only objects"
        )
    normalized_tasks: list[dict[str, object]] = []
    for index, row in enumerate(rows):
        metadata = row.get("metadata")
        if (
            isinstance(metadata, Mapping)
            and "localarena_task_pack" in metadata
        ):
            raise ValueError(
                "task pack manifest metadata uses reserved "
                "localarena_task_pack"
            )
        normalized_tasks.append(
            _task_manifest_row(
                _task_from_row(
                    row,
                    field_name=f"manifest.tasks[{index}]",
                )
            )
        )
    return {
        "name": name,
        "version": version,
        "license": license_name,
        "description": description,
        "source": _thaw_json(source),
        "tasks": normalized_tasks,
    }


def _openai_eval_task(
    value: Mapping[str, object],
    *,
    line_number: int,
) -> PromptTask:
    if "input" not in value or "ideal" not in value:
        raise ValueError(
            f"line {line_number} must contain both input and ideal"
        )
    task_id_value = value.get("id", f"line-{line_number}")
    task_id = _require_text(task_id_value, f"line {line_number}.id")
    ideal = value.get("ideal")
    if type(ideal) is str:
        expected = (ideal,)
    elif (
        isinstance(ideal, Sequence)
        and not isinstance(ideal, (str, bytes, bytearray))
        and ideal
        and all(type(item) is str for item in ideal)
    ):
        expected = tuple(ideal)
    else:
        raise TypeError(
            f"line {line_number}.ideal must be a string or non-empty string array"
        )
    metadata = value.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise TypeError(f"line {line_number}.metadata must be an object")
    evaluator = TextMatch(expected, mode="begin")
    input_value = value.get("input")
    if type(input_value) is str:
        return PromptTask.from_text(
            task_id,
            input_value,
            evaluator=evaluator,
            metadata=metadata,
        )
    return PromptTask(
        id=task_id,
        messages=_chat_messages(input_value, f"line {line_number}.input"),
        evaluator=evaluator,
        metadata=metadata,
    )


def _with_pack_provenance(
    task: PromptTask,
    *,
    name: str,
    version: str,
    license_name: str,
    digest: str,
    source_format: str,
    description: str,
    source: Mapping[str, object],
) -> PromptTask:
    metadata = _thaw_json(task.metadata)
    if not isinstance(metadata, dict):
        raise TypeError("task metadata must be an object")
    if "localarena_task_pack" in metadata:
        raise ValueError(
            f"task {task.id!r} metadata uses reserved localarena_task_pack"
        )
    metadata["localarena_task_pack"] = {
        "name": name,
        "version": version,
        "license": license_name,
        "digest": digest,
        "format": source_format,
        "description": description,
        "source": _thaw_json(source),
    }
    return PromptTask(
        id=task.id,
        messages=task.messages,
        evaluator=task.evaluator,
        metadata=metadata,
    )


def parse_task_pack(
    value: str | Mapping[str, object],
    *,
    format: str = "auto",
    name: str = "Imported task pack",
    version: str = "unversioned",
    license: str = "unspecified",
) -> TaskPack:
    """Parse a native manifest, native JSONL rows, or Evals-style JSONL.

    ``format`` may be ``auto``, ``localarena``, ``localarena-jsonl``, or
    ``openai-evals-jsonl``.
    """

    valid_formats = {
        "auto",
        "localarena",
        "localarena-jsonl",
        "openai-evals-jsonl",
    }
    if format not in valid_formats:
        raise ValueError(
            f"format must be one of {', '.join(sorted(valid_formats))}"
        )

    parsed: object = value
    if isinstance(value, str) and format in {"auto", "localarena"}:
        try:
            candidate = json.loads(
                value,
                object_pairs_hook=_unique_json_object,
            )
        except json.JSONDecodeError:
            candidate = None
        if isinstance(candidate, Mapping):
            parsed = candidate
            if format == "auto":
                format = "localarena"

    if isinstance(parsed, Mapping):
        parsed = _normalize_pack_json(
            _thaw_json(
                _freeze_json_object(parsed, field_name="task pack")
            )
        )
        if not isinstance(parsed, dict):
            raise TypeError("task pack must be an object")
        if format not in {"auto", "localarena"}:
            raise ValueError(f"{format} requires JSONL text")
        extra = sorted(set(parsed) - _PACK_FIELDS)
        if extra:
            raise ValueError(
                f"task pack contains unsupported fields: {', '.join(extra)}"
            )
        schema_version = parsed.get("schema_version")
        if (
            type(schema_version) is not int
            or schema_version != TASK_PACK_SCHEMA_VERSION
        ):
            raise ValueError(
                "task pack schema_version must be 1"
            )
        schema_uri = parsed.get("$schema")
        if schema_uri is not None:
            _require_text(schema_uri, "task pack $schema")
        pack_name = _require_text(parsed.get("name"), "task pack name")
        pack_version = _require_text(
            parsed.get("version"),
            "task pack version",
        )
        pack_license = _require_text(
            parsed.get("license"),
            "task pack license",
        )
        description = parsed.get("description", "")
        if type(description) is not str:
            raise TypeError("task pack description must be a string")
        source = parsed.get("source", {})
        if not isinstance(source, Mapping):
            raise TypeError("task pack source must be an object")
        declared_digest = parsed.get("digest")
        if declared_digest is not None:
            if (
                type(declared_digest) is not str
                or not declared_digest.startswith("sha256:")
                or len(declared_digest) != 71
                or any(
                    character not in "0123456789abcdef"
                    for character in declared_digest[7:]
                )
            ):
                raise ValueError(
                    "task pack digest must be a sha256: value"
                )
        declared_format = parsed.get("format")
        if declared_format is not None and declared_format not in _SOURCE_FORMATS:
            raise ValueError("task pack format is invalid")
        rows = parsed.get("tasks")
        if not isinstance(rows, list) or not rows:
            raise ValueError("task pack tasks must be a non-empty array")
        if not all(isinstance(row, Mapping) for row in rows):
            raise TypeError("task pack tasks must contain only objects")
        digest = task_pack_digest(parsed)
        if declared_digest is not None and declared_digest != digest:
            raise ValueError(
                "task pack digest does not match its manifest"
            )
        tasks = tuple(
            _task_from_row(row, field_name=f"tasks[{index}]")
            for index, row in enumerate(rows)
        )
        source_format = declared_format or "localarena"
        manifest = _thaw_json(
            _freeze_json_object(parsed, field_name="task pack")
        )
        if not isinstance(manifest, dict):
            raise TypeError("task pack must be an object")
        manifest["digest"] = digest
        manifest["format"] = source_format
    else:
        if not isinstance(value, str):
            raise TypeError("task pack must be a JSON object or JSONL string")
        rows = []
        for line_number, line in enumerate(value.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(
                    line,
                    object_pairs_hook=_unique_json_object,
                )
            except _DuplicateJSONKeyError as error:
                raise ValueError(
                    f"line {line_number} has ambiguous JSON: {error}"
                ) from error
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"line {line_number} is not valid JSON: {error.msg}"
                ) from error
            if not isinstance(row, Mapping):
                raise TypeError(f"line {line_number} must be a JSON object")
            normalized_row = _normalize_pack_json(row)
            if not isinstance(normalized_row, dict):
                raise TypeError(f"line {line_number} must be a JSON object")
            rows.append((line_number, normalized_row))
        if not rows:
            raise ValueError("task pack JSONL must contain at least one row")
        if format == "auto":
            format = (
                "openai-evals-jsonl"
                if all("input" in row and "ideal" in row for _, row in rows)
                else "localarena-jsonl"
            )
        if format == "localarena":
            raise ValueError("localarena format requires a JSON object")
        pack_name = _require_text(name, "name")
        pack_version = _require_text(version, "version")
        pack_license = _require_text(license, "license")
        description = ""
        source = {}
        if format == "openai-evals-jsonl":
            tasks = tuple(
                _openai_eval_task(row, line_number=line_number)
                for line_number, row in rows
            )
        elif format == "localarena-jsonl":
            tasks = tuple(
                _task_from_row(row, field_name=f"line {line_number}")
                for line_number, row in rows
            )
        else:
            raise ValueError(f"unsupported task pack format: {format}")
        source_format = format
        manifest = _manifest_from_tasks(
            name=pack_name,
            version=pack_version,
            license_name=pack_license,
            description=description,
            source=source,
            tasks=tasks,
        )
        digest = task_pack_digest(manifest)
        manifest["digest"] = digest
        manifest["format"] = source_format

    ids = [task.id for task in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("task pack task ids must be unique")
    return TaskPack(
        name=pack_name,
        version=pack_version,
        license=pack_license,
        tasks=tasks,
        digest=digest,
        format=source_format,
        description=description,
        source=source,
        _manifest=manifest,
    )


def load_task_pack(
    path: str | Path,
    *,
    format: str = "auto",
    name: str | None = None,
    version: str = "unversioned",
    license: str = "unspecified",
) -> TaskPack:
    """Load a task pack from disk without executing downloaded code."""

    source_path = Path(path)
    return parse_task_pack(
        source_path.read_text(encoding="utf-8"),
        format=format,
        name=name or source_path.stem,
        version=version,
        license=license,
    )
