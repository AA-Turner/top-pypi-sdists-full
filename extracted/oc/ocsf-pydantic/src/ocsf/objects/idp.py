from ._entity import Entity


class IdentityProvider(Entity):
    """
    The Identity Provider object contains detailed information about a provider
    responsible for creating, maintaining, and managing identity information while
    offering authentication services to applications. An Identity Provider (IdP)
    serves as a trusted authority that verifies the identity of users and issues
    authentication tokens or assertions to enable secure access to applications or
    services.
    """

    # Optional:
    name: str | None = None # The name of the identity provider.
    uid: str | None = None # The unique identifier of the identity provider.
