from ._entity import Entity


class Organization(Entity):
    """
    The Organization object describes characteristics of an organization or company
    and its division if any.
    """

    # Recommended:
    ou_name: str | None = None

    # Optional:
    name: str | None = None # The name of the organization. For example, Widget, Inc.
    ou_uid: str | None = None
    uid: str | None = None # The unique identifier of the organization. For example, its Active
                           # Directory or AWS Org ID.
