"""Search keys for RFC-402 (V1 input path).

Extraction runs on the worker because abraxas cannot read encrypted payloads. Validation
runs at definition time so a bad path fails at startup, not mid-execution. Extracted values
are stored UNENCRYPTED to be searchable.
"""

from __future__ import annotations

import collections.abc
import inspect
from datetime import date
from enum import Enum
from types import NoneType, UnionType
from typing import Any, Sequence, Union, get_args, get_origin

import structlog
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from mistralai.workflows.core.config.config import (
    MAX_SEARCH_KEY_CHARS,
    MAX_SEARCH_KEY_VALUE_CHARS,
    MAX_SEARCH_KEYS,
)
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

logger = structlog.get_logger(__name__)

# str/bytes are Collections too, but are valid scalar leaves.
_SCALAR_COLLECTION_TYPES = (str, bytes, bytearray)


def _unwrap_optional(annotation: Any) -> Any:
    if get_origin(annotation) in (Union, UnionType):
        members = [arg for arg in get_args(annotation) if arg is not NoneType]
        if len(members) == 1:
            return members[0]
    return annotation


def _is_basemodel(annotation: Any) -> bool:
    return inspect.isclass(annotation) and issubclass(annotation, BaseModel)


def _is_container(annotation: Any) -> bool:
    # Catch concrete (list, dict, ...) and abstract (Sequence, Mapping, Set) collections alike,
    # so define-time validation stays in lockstep with extract_search_key_metadata, which skips
    # these at runtime. Without this, e.g. Sequence[str] passes validation but yields no metadata.
    origin = get_origin(annotation)
    candidate = origin if origin is not None else annotation
    if not inspect.isclass(candidate):
        return False
    if issubclass(candidate, _SCALAR_COLLECTION_TYPES):
        return False
    return issubclass(candidate, collections.abc.Collection)


def _leaf_members(annotation: Any) -> list[Any]:
    if get_origin(annotation) in (Union, UnionType):
        return [arg for arg in get_args(annotation) if arg is not NoneType]
    return [annotation]


def _has_alias(field: FieldInfo) -> bool:
    """True if the field is keyed by anything other than its field name on the wire."""
    for attr in (field.alias, field.validation_alias, field.serialization_alias):
        if isinstance(attr, str) and attr:
            return True
    return False


def validate_search_key_paths(
    input_model: type[BaseModel],
    search_keys: Sequence[str],
    workflow_name: str | None = None,
) -> None:
    """Collect every invalid path and raise once so a typo fails at import/startup, not mid-execution."""
    if len(search_keys) > MAX_SEARCH_KEYS:
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message=f"A workflow may declare at most {MAX_SEARCH_KEYS} search_keys, got {len(search_keys)}.",
        )

    errors: dict[str, list[str]] = {}
    seen: set[str] = set()
    for path in search_keys:
        path_errors: list[str] = []
        if path in seen:
            path_errors.append("duplicate search key")
        else:
            seen.add(path)
        if ":" in path:
            path_errors.append("must not contain ':'")
        if not path or path != path.strip():
            path_errors.append("must not be empty or padded with whitespace")
        if len(path) > MAX_SEARCH_KEY_CHARS:
            path_errors.append(f"must be at most {MAX_SEARCH_KEY_CHARS} characters")
        segments = path.split(".")
        if any(not segment for segment in segments):
            path_errors.append("has an empty path segment")

        # Skip traversal when lexical errors already make the path meaningless.
        if not path_errors:
            current: type[BaseModel] = input_model
            for index, segment in enumerate(segments):
                field = current.model_fields.get(segment)
                if field is None:
                    path_errors.append(f"{segment!r} is not a field of {current.__name__}")
                    break
                if _has_alias(field):
                    path_errors.append(f"{segment!r} uses a Pydantic alias; aliased fields are not allowed")
                    break
                field_type = _unwrap_optional(field.annotation)
                if index == len(segments) - 1:
                    if any(_is_basemodel(member) or _is_container(member) for member in _leaf_members(field_type)):
                        path_errors.append(
                            "leaf must be a scalar value (or a union of scalars), not a model, list or dict"
                        )
                elif not _is_basemodel(field_type):
                    path_errors.append(f"{segment!r} must be a nested model to traverse into it")
                    break
                else:
                    current = field_type

        if path_errors:
            errors[path] = path_errors

    if errors:
        header = (
            f"At least one invalid search key in definition of workflow `{workflow_name}`:"
            if workflow_name
            else "At least one invalid search key in workflow definition:"
        )
        lines = [header]
        for path, path_errors in errors.items():
            lines.append(f"- `{path}`:")
            for reason in path_errors:
                lines.append(f"  - {reason}")
        raise WorkflowsException(
            code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
            message="\n".join(lines),
        )


def _cap_value(path: str, value: str) -> str:
    """Truncate over-long values. Slicing a str never splits a code point."""
    if len(value) <= MAX_SEARCH_KEY_VALUE_CHARS:
        return value
    logger.warning(
        "Search key value exceeded length cap; truncating",
        search_key=path,
        original_chars=len(value),
        max_chars=MAX_SEARCH_KEY_VALUE_CHARS,
    )
    return value[:MAX_SEARCH_KEY_VALUE_CHARS]


def _coerce_leaf(value: Any) -> str:
    """Enum -> .value, bool -> lowercase, date/datetime -> ISO 8601, everything else -> str."""
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, bool):
        return str(value).lower()
    # str(datetime) uses a space separator; ISO keeps stored values sortable and uniform.
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def extract_search_key_metadata(params: Any, search_keys: Sequence[str]) -> dict[str, str]:
    """Non-raising: metadata must never fail the workflow. Deterministic result, so sandbox-safe."""
    if not search_keys:
        return {}
    if isinstance(params, BaseModel):
        params = params.model_dump()
    if not isinstance(params, dict):
        return {}

    metadata: dict[str, str] = {}
    for path in search_keys:
        try:
            current: Any = params
            for segment in path.split("."):
                if isinstance(current, dict):
                    current = current.get(segment)
                else:
                    current = None
                if current is None:
                    break
            if current is not None and not isinstance(current, (dict, list, tuple, set, frozenset)):
                metadata[path] = _cap_value(path, _coerce_leaf(current))
        except Exception as exc:
            logger.debug(
                "Search key extraction failed for path; skipping",
                search_key=path,
                **extract_error_context(exc),
            )
            continue
    return metadata
