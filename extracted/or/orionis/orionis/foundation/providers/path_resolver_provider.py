from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.paths.contracts.resolver import IResolver
from orionis.services.paths.resolver import Resolver

class PathResolverProvider(ServiceProvider):
    """
    Registers the path resolution service in the application container.

    This provider binds the `IResolver` interface to the `Resolver` implementation,
    allowing the application to resolve file system paths through dependency injection.

    Attributes
    ----------
    app : Application
        The application container instance inherited from ServiceProvider.
    """

    def register(self) -> None:
        """
        Register the path resolver service in the application container.

        Binds the `IResolver` interface to the `Resolver` implementation as a transient
        service, with the alias "core.orionis.path_resolver".

        Returns
        -------
        None
        """

        self.app.transient(IResolver, Resolver, alias="core.orionis.path_resolver")

    def boot(self) -> None:
        """
        Perform post-registration initialization if needed.

        This method is a placeholder for any actions required after service registration.

        Returns
        -------
        None
        """

        pass