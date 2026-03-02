from ._entity import Entity

class ManagedEntity(Entity):
    """
    The Managed Entity object describes the type and version of an entity, such as a
    policy or configuration.
    """

    # Recommended:
    type: str | None = None # The managed entity type. For example: `policy`,
                            # `user`, `organizational unit`, `device`.
    version: str | None = None # The version of the managed entity. For example: `1.2.3`.

    # Optional:
    data: dict | None = None # The managed entity content as a JSON object.
    name: str | None = None # The name of the managed entity.
    uid: str | None = None # The identifier of the managed entity.
