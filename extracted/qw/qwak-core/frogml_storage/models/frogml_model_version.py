from frogml_storage.models.frogml_entity_version import FrogMLEntityVersion


class FrogMLModelVersion(FrogMLEntityVersion):
    """
    Represent metadata of an uploaded model version.

    Inherits:
        FrogMLEntityVersion: Base class for entity versions.
    """

    @classmethod
    def from_entity_version(
        cls, entity_version: FrogMLEntityVersion
    ) -> "FrogMLModelVersion":
        return cls(
            entity_name=entity_version.entity_name,
            version=entity_version.version,
            namespace=entity_version.namespace,
            entity_manifest=entity_version.entity_manifest,
        )
