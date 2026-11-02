"""Offline loading of exact pinned dataset schemas for local dataset views."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.manifests import Manifest
from labqoat.projects.pinned_schema import PinnedSchema
from labqoat.projects.project_directory import ProjectDirectory
from labqoat.projects.schema_requirement import SchemaRequirement


@dataclass(frozen=True)
class ProjectSchemas:
    """Never fetch a moving schema or silently accept local captured-schema drift."""

    pins: tuple[PinnedSchema, ...]

    @classmethod
    def read(cls, project: ProjectDirectory) -> "ProjectSchemas":
        """Read the versioned JSON project lock, or an empty selection before the first pin."""
        path = project.path("labqoat.lock")
        lock = (
            Manifest.decode("project_lock", path.read_text(encoding="utf-8"))
            if path.exists()
            else Manifest.capture("project_lock", {"lock_version": 1, "datasets": {}})
        )
        datasets = JsonDocument.expect_dict(lock.document["datasets"])
        return cls(
            tuple(cls._pin(project, alias, JsonDocument.expect_dict(datasets[alias])) for alias in sorted(datasets))
        )

    @staticmethod
    def _pin(project: ProjectDirectory, alias: str, selection: JsonDocument) -> PinnedSchema:
        """Validate a closed local path and canonical digest before exposing a schema to generation."""
        requirement = SchemaRequirement.capture(project, alias, selection)
        return PinnedSchema(
            alias=alias,
            schema_file=requirement.schema_file,
            schema=requirement.schema,
            dataset=JsonDocument.expect_scalar(selection["dataset"], str),
            revision=JsonDocument.expect_scalar(selection["revision"], str),
        )
