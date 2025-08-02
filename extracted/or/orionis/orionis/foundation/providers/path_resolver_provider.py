from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.paths.contracts.resolver import IResolver
from orionis.services.paths.resolver import Resolver

class PathResolverProvider(ServiceProvider):
    """
    PathResolverProvider
    ===================

    Registers the path resolution service in the application container.
    Provides compatibility with the file system for resolving paths.

    Methods
    -------
    register()
        Registers the path resolver service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """


    def register(self) -> None:
        """
        Registers the path resolver service in the application container.

        Returns
        -------
        None
        """
        self.app.transient(IResolver, Resolver, alias="core.orionis.path_resolver")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass