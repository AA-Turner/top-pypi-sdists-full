"""One verified local schema selection with separate build and execution projections."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.projects.schema_requirement import SchemaRequirement


@dataclass(frozen=True)
class PinnedSchema(SchemaRequirement):
    """Retain the selected revision locally while exposing only schema requirements to generation."""

    dataset: str
    revision: str

    def selection(self) -> JsonDocument:
        """Serialize the tracked project lock entry used during submission."""
        return JsonDocument(
            {
                "dataset": self.dataset,
                "revision": self.revision,
                "schema_digest": self.schema.digest,
                "schema_file": self.schema_file,
            }
        )
