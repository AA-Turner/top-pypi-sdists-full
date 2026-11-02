"""A captured dataset interface without a selected dataset or revision."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.projects.project_directory import ProjectDirectory
from labqoat.projects.project_names import ProjectNames
from labqoat.schemas.identity import Identity
from labqoat.schemas.schema_document import SchemaDocument


@dataclass(frozen=True)
class SchemaRequirement:
    """Own the exact schema identity captured by a local dataset selection."""

    alias: str
    schema_file: str
    schema: SchemaDocument

    @staticmethod
    def capture(project: ProjectDirectory, alias: str, value: JsonDocument) -> "SchemaRequirement":
        """Resolve closed local schema paths and verify their exact declared canonical identity."""
        ProjectNames.alias(alias)
        file = JsonDocument.expect_scalar(value["schema_file"], str)
        if not file.startswith("schemas/"):
            raise ValueError(f"/datasets/{alias}/schema_file: captured schemas must live in schemas/")
        schema = SchemaDocument.capture(
            JsonDocument.expect_dict(Identity.decode(project.path(file).read_text(encoding="utf-8")))
        )
        if schema.digest != value["schema_digest"]:
            raise ValueError(f"/datasets/{alias}/schema_digest: captured schema digest mismatch")
        return SchemaRequirement(alias, file, schema)
