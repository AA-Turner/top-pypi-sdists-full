from ._entity import Entity


class Feature(Entity):
    """
    The Feature object provides information about the software product feature that
    generated a specific event. It encompasses details related to the capabilities,
    components, user interface (UI) design, and performance upgrades associated with
    the feature.
    """

    # Recommended:
    version: str | None = None # The version of the feature.

    # Optional:
    name: str | None = None # The name of the feature.
    uid: str | None = None # The unique identifier of the feature.
