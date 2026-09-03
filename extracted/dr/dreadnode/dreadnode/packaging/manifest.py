from __future__ import annotations

import typing as t
from string import Formatter

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SHELL_EXECUTABLE_NAMES = frozenset(
    {
        "ash",
        "bash",
        "csh",
        "cmd",
        "dash",
        "fish",
        "ksh",
        "ksh93",
        "mksh",
        "powershell",
        "pwsh",
        "sh",
        "tcsh",
        "zsh",
    }
)


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


class CommandWrapperManifest(BaseModel):
    """Explicit, non-shell command tool declaration."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(pattern=r"^[a-z][a-z0-9_]{0,63}$")
    description: str | None = None
    input_schema: dict[str, t.Any]
    executable: str = Field(min_length=1)
    version_probe: list[str] = Field(min_length=1)
    expected_version: str = Field(min_length=1)
    argv: list[str] = Field(min_length=1)
    timeout_seconds: float = Field(gt=0, le=3600)
    working_directory: t.Literal["capability", "workspace"]
    adapter_version: str = Field(pattern=r"^\d+\.\d+\.\d+$")

    @field_validator("input_schema")
    @classmethod
    def validate_input_schema(cls, value: dict[str, t.Any]) -> dict[str, t.Any]:
        try:
            Draft202012Validator.check_schema(value)
        except SchemaError as exc:
            raise ValueError(f"input_schema is not valid JSON Schema: {exc.message}") from exc
        if value.get("type") != "object":
            raise ValueError("input_schema must describe a JSON object")
        return value

    @field_validator("executable")
    @classmethod
    def validate_executable(cls, value: str) -> str:
        if any(character.isspace() for character in value) or any(
            character in value for character in ("\x00", "|", "&", ";", "<", ">", "`")
        ):
            raise ValueError("executable must be one program path, not a shell command")
        executable_name = value.replace("\\", "/").rsplit("/", 1)[-1].lower()
        if executable_name in SHELL_EXECUTABLE_NAMES:
            raise ValueError("shell executables are not supported")
        return value

    @field_validator("version_probe", "argv")
    @classmethod
    def validate_argv(cls, value: list[str]) -> list[str]:
        if any(not item or "\x00" in item for item in value):
            raise ValueError("argv entries must be non-empty strings without NUL bytes")
        return value

    @field_validator("expected_version")
    @classmethod
    def validate_expected_version(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("expected_version must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_argv_template(self) -> CommandWrapperManifest:
        properties = self.input_schema.get("properties", {})
        for argument in self.argv:
            try:
                fields = Formatter().parse(argument)
            except ValueError as exc:
                raise ValueError(f"argv contains an invalid template: {exc}") from exc
            for _, field_name, format_spec, conversion in fields:
                if field_name is None:
                    continue
                if field_name not in properties or format_spec or conversion:
                    raise ValueError("argv placeholders must be plain input_schema property names")
        return self


class CapabilityManifest(BaseManifest):
    """Capability manifest stored in OCI config and on disk."""

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    schema_version: int = Field(default=1, alias="schema")
    name: str = ""
    version: str = ""
    description: str = ""
    agents: list[str] | None = None
    tools: list[str] | None = None
    commands: list[CommandWrapperManifest] | None = None
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

    @model_validator(mode="after")
    def validate_command_names(self) -> CapabilityManifest:
        names = [command.name for command in self.commands or []]
        if len(names) != len(set(names)):
            raise ValueError("command wrapper names must be unique")
        return self


# Mapping from singular type name to manifest class
MANIFEST_TYPES: dict[str, type[BaseManifest]] = {
    "dataset": DatasetManifest,
    "model": ModelManifest,
    "environment": EnvironmentManifest,
    "capability": CapabilityManifest,
}
