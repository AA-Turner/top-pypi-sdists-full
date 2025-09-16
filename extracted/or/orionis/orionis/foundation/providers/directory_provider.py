from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.file.contracts.directory import IDirectory
from orionis.services.file.directory import Directory

class DirectoryProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the directory service as a singleton within the application container.

        This method binds the `IDirectory` interface to its concrete implementation `Directory`
        as a singleton. The binding is associated with a specific alias, ensuring that only one
        instance of `Directory` is created and shared across the application's lifecycle. This
        promotes efficient resource usage and consistent behavior when accessing directory-related
        services.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs registration as a side effect.
        """

        # Bind the IDirectory interface to the Directory implementation as a singleton.
        # The alias ensures unique identification within the container.
        self.app.singleton(IDirectory, Directory, alias="x-orionis.services.file.contracts.directory.IDirectory")