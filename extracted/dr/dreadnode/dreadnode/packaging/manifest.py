from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field


class BaseManifest(BaseModel):
    """Base manifest with artifact tracking."""

    artifacts: dict[str, str] = Field(default_factory=dict)  # path -> oid
    artifacts_hash: str | None = None


class DatasetManifest(BaseManifest):
    """Dataset-specific manifest."""

    summary: str | None = None
    format: str = "parquet"
    data_schema: dict[str, str] = Field(default_factory=dict)
    row_count: int | None = None
    splits: dict[str, str] | None = None  # split_name -> artifact_path


class ModelManifest(BaseManifest):
    """Model-specific manifest."""

    summary: str | None = None
    framework: str = "safetensors"
    task: str | None = None
    architecture: str | None = None
    tags: list[str] | None = None
    license: str | None = None
    pretty_name: str | None = None
    language: list[str] | None = None
    task_categories: list[str] | None = None
    size_category: str | None = None
    description: str | None = None
    base_model: str | None = None
    metrics: dict[str, t.Any] | None = None
    dataset_refs: list[str] | None = None
    aliases: list[str] | None = None


class EnvironmentManifest(BaseManifest):
    """Environment-specific manifest."""


# ============================================================================
# Capability Manifest
# ============================================================================


class CapabilityManifest(BaseManifest):
    """Capability manifest stored in OCI config and on disk."""

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    schema_version: int = Field(default=1, alias="schema")
    name: str = ""
    version: str = ""
    description: str = ""
    agents: list[str] | None = None
    tools: list[str] | None = None
    hooks: list[str] | None = None
    skills: list[str] | None = None
    policies: list[str] | None = None
    workers: dict[str, t.Any] | None = None
    mcp: dict[str, t.Any] | None = None
    author: dict[str, str] | None = None
    license: str | None = None
    repository: str | None = None
    keywords: list[str] = Field(default_factory=list)
    dependencies: dict[str, t.Any] | None = None
    checks: list[dict[str, t.Any]] | None = None
    flags: dict[str, t.Any] | None = None
    # Structured item production config. Supported forms:
    # true/false for enable/disable, a registry identifier or list of identifiers,
    # or a mapping of optional local models as "module:PydanticClass". Dict forms may
    # also use reserved keys like enabled/values/custom. See dreadnode.items.config.
    outputs: bool | str | list[str] | dict[str, t.Any] | None = None
    # Deprecated aliases retained for historical capability manifests.
    produces: bool | str | list[str] | dict[str, t.Any] | None = None
    items: dict[str, t.Any] | None = None


# Mapping from singular type name to manifest class
MANIFEST_TYPES: dict[str, type[BaseManifest]] = {
    "dataset": DatasetManifest,
    "model": ModelManifest,
    "environment": EnvironmentManifest,
    "capability": CapabilityManifest,
}
