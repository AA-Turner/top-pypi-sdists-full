
from .data_classification import DataClassification

from ._entity import Entity


class Resource(Entity, DataClassification):
    """
    The Resource object contains attributes that provide information about a
    particular resource. It serves as a base object, offering attributes that help
    identify and classify the resource effectively.
    """

    # Optional:
    data: dict | None = None # Additional data describing the resource.
    labels: list[str] | None = None # The list of labels/tags associated to a resource.
    name: str | None = None # The name of the resource.
    type: str | None = None # The resource type as defined by the event source.
    uid: str | None = None # The unique identifier of the resource.
