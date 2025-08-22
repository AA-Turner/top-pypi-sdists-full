from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.file.contracts.directory import IDirectory
from orionis.services.file.directory import Directory

class DirectoryProvider(ServiceProvider):
    """
    Service provider for registering the directory service in the application container.

    This provider binds the `IDirectory` interface to its concrete implementation (`Directory`)
    as a singleton. This ensures that a single shared instance of the directory service is
    available for dependency injection throughout the application.

    Attributes
    ----------
    app : Application
        The application container instance where services are registered.

    Methods
    -------
    register()
        Registers the directory service as a singleton in the application container.
    boot()
        Performs post-registration actions if necessary.
    """

    def register(self) -> None:
        """
        Register the directory service as a singleton in the application container.

        This method binds the `IDirectory` interface to the `Directory` implementation with
        a specific alias. Only one instance of `Directory` will be created and shared
        throughout the application's lifecycle.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Bind IDirectory to Directory as a singleton with a specific alias
        self.app.singleton(IDirectory, Directory, alias="x-orionis.services.file.contracts.directory")

    def boot(self) -> None:
        """
        Perform actions required after all providers have been registered.

        This method is called after the `register` phase. It can be used for additional
        initialization if needed. No additional boot logic is required for this provider.

        Returns
        -------
        None
            This method does not return any value.
        """
        # No additional boot logic required for this provider
        pass