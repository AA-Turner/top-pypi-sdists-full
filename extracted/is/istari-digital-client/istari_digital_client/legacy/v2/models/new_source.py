import dataclasses


@dataclasses.dataclass
class NewSource:
    """
    Represents a reference to a source revision when creating a new model or artifact.

    This includes the revision's unique identifier and an optional relationship
    identifier that describes how the source relates to the new entity (e.g., "input", "dependency").
    """

    revision_id: str
    relationship_identifier: str | None = None
