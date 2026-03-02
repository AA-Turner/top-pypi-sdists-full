
from ._entity import Entity

class Service(Entity):
    """
    The Service object describes characteristics of a service, e.g. AWS EC2.
    """

    # Recommended:
    version: str | None = None # The version of the service.

    # Optional:
    labels: list[str] | None = None # The list of labels associated with the service.
    name: str | None = None # The name of the service.
    uid: str | None = None # The unique identifier of the service.
