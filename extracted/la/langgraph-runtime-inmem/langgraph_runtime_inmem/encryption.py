"""Structural JSON encryption owned by the Python in-memory runtime.

Unlike Postgres persistence, this remains here while local persistence is
Python-owned.
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping

    from langgraph_api.encryption.aes_json import AesEncryptionInstance
    from langgraph_api.encryption.custom import JsonEncryptionWrapper, ModelType

NESTED_ENCRYPTED_SUBFIELDS: dict[tuple[str, str], tuple[str, ...]] = {
    ("run", "kwargs"): ("input", "config", "context", "command"),
    ("run", "config"): ("configurable", "metadata"),
    ("cron", "payload"): ("metadata", "context", "input", "config"),
    ("cron", "config"): ("configurable", "metadata"),
    ("assistant", "config"): ("configurable",),
    ("thread", "config"): ("configurable",),
}

ENCRYPTION_FIELDS: dict[str, tuple[str, ...]] = {
    "thread": ("metadata", "config", "values", "interrupts", "error"),
    "run": ("metadata", "kwargs"),
    "assistant": ("metadata", "config", "context"),
    "cron": ("metadata", "payload"),
    "store": ("value",),
}

NEVER_ENCRYPT_FIELDS = frozenset(
    {
        "thread_id",
        "run_id",
        "assistant_id",
        "graph_id",
        "checkpoint_id",
        "task_id",
        "__pregel_checkpointer",
        "__pregel_resuming",
        "__pregel_durability",
        "__pregel_stream",
        "__pregel_task_id",
        "__pregel_checkpoint_ns",
        "__after_seconds__",
        "__request_start_time_ms__",
        "__encryption_context__",
        "__blob_encryption_context__",
        "langgraph_version",
        "langgraph_api_version",
        "langgraph_plan",
        "langgraph_host",
        "langgraph_api_url",
        "langgraph_request_id",
        "langgraph_auth_user_id",
        "langgraph_auth_permissions",
    }
)

NEVER_ENCRYPT_PATHS = frozenset(
    {
        "run.kwargs.config.recursion_limit",
        "run.kwargs.config.max_concurrency",
        "run.kwargs.temporary",
        "run.kwargs.config.configurable.ttl",
        "checkpoint.metadata.source",
        "checkpoint.metadata.step",
        "checkpoint.metadata.parents",
        "checkpoint.metadata.run_attempt",
        "checkpoint.metadata.counters_since_delta_snapshot",
    }
)


def should_skip_encryption(key: str, path: str) -> bool:
    return key in NEVER_ENCRYPT_FIELDS or f"{path}.{key}" in NEVER_ENCRYPT_PATHS


def extract_blob_encryption_context(
    data: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Return checkpoint blob context carried by an encrypted resource."""
    if data is None:
        return None

    from langgraph_api.encryption.shared import (  # noqa: PLC0415
        BLOB_ENCRYPTION_CONTEXT_KEY,
        ENCRYPTION_CONTEXT_KEY,
    )

    return data.get(BLOB_ENCRYPTION_CONTEXT_KEY) or data.get(ENCRYPTION_CONTEXT_KEY)


def encryption_fields(model_type: ModelType) -> list[str]:
    """Return fields structurally encrypted by the local runtime."""
    return list(ENCRYPTION_FIELDS[model_type])


async def _decrypt_field(
    obj: dict[str, Any],
    field_name: str,
    encryption_instance: JsonEncryptionWrapper | AesEncryptionInstance | None,
    model_type: ModelType,
) -> tuple[str, Any]:
    from langgraph_api.encryption.middleware import (  # noqa: PLC0415
        decrypt_json_if_needed,
    )

    if not obj.get(field_name):
        return field_name, obj.get(field_name)

    decrypted = await decrypt_json_if_needed(
        obj[field_name], encryption_instance, model_type, field=field_name
    )
    nested_fields = NESTED_ENCRYPTED_SUBFIELDS.get((model_type, field_name), ())
    if decrypted is not None:
        results = await asyncio.gather(
            *(
                _decrypt_field(decrypted, name, encryption_instance, model_type)
                for name in nested_fields
                if isinstance(decrypted.get(name), dict)
            )
        )
        for name, value in results:
            decrypted[name] = value
    return field_name, decrypted


async def decrypt_fields(
    obj: dict[str, Any],
    model_type: ModelType,
    fields: list[str],
    encryption_instance: JsonEncryptionWrapper | AesEncryptionInstance | None,
) -> None:
    """Decrypt configured fields, including local-runtime nested structure."""
    results = await asyncio.gather(
        *(
            _decrypt_field(obj, name, encryption_instance, model_type)
            for name in fields
            if name in obj
        )
    )
    for name, value in results:
        obj[name] = value


async def _encrypt_field(
    data: Mapping[str, Any],
    field_name: str,
    encryption_instance: JsonEncryptionWrapper | AesEncryptionInstance | None,
    model_type: ModelType,
    path: str | None = None,
) -> tuple[str, Any]:
    from langgraph_api.encryption.middleware import (  # noqa: PLC0415
        encrypt_json_if_needed,
    )

    if field_name not in data or data[field_name] is None:
        return field_name, data.get(field_name)

    field_data = data[field_name]
    if model_type == "thread" and field_name == "values":
        from langgraph_api.serde import json_dumpb, json_loads  # noqa: PLC0415

        field_data = json_loads(json_dumpb(field_data))
    current_path = f"{path}.{field_name}" if path else f"{model_type}.{field_name}"
    nested_fields = NESTED_ENCRYPTED_SUBFIELDS.get((model_type, field_name), ())
    extracted: dict[str, Any] = {}
    if nested_fields:
        if not isinstance(field_data, dict):
            raise TypeError(
                f"'{field_name}' must be a dict for encryption, "
                f"got {type(field_data).__name__}"
            )
        for name in nested_fields:
            value = field_data.get(name)
            if isinstance(value, dict) and value:
                extracted[name] = value
        if extracted:
            field_data = {k: v for k, v in field_data.items() if k not in extracted}

    encrypted = await encrypt_json_if_needed(
        field_data,
        encryption_instance,
        model_type,
        field=field_name,
        path=current_path,
        should_skip=should_skip_encryption,
    )
    if extracted and isinstance(encrypted, dict):
        results = await asyncio.gather(
            *(
                _encrypt_field(
                    {name: value}, name, encryption_instance, model_type, current_path
                )
                for name, value in extracted.items()
            )
        )
        for name, value in results:
            encrypted[name] = value
            marker = value.get("__encryption_context__")
            if (
                "__encryption_context__" not in encrypted
                and isinstance(marker, dict)
                and marker.get("__langgraph_encryption_type__") == "aes"
            ):
                encrypted["__encryption_context__"] = marker
    return field_name, encrypted


async def encrypt_fields(
    data: Mapping[str, Any],
    model_type: ModelType,
    fields: list[str],
    encryption_instance: JsonEncryptionWrapper | AesEncryptionInstance | None,
) -> dict[str, Any]:
    """Encrypt configured fields, preserving local-runtime nested structure."""
    result = dict(data)
    encrypted_fields = await asyncio.gather(
        *(
            _encrypt_field(data, name, encryption_instance, model_type)
            for name in fields
            if name in data
        )
    )
    for name, value in encrypted_fields:
        result[name] = value
    return result
