from orionis.container.facades.facade import Facade

class Directory(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the binding key used by the service container to resolve the directory service.

        This method provides the unique identifier (binding key) that the service container uses
        to locate and instantiate the implementation of the directory service. It acts as a bridge
        between the facade and the underlying service registration, ensuring that the correct
        service is retrieved when requested.

        Returns
        -------
        str
            The binding key for the directory service implementation:
            'x-orionis.services.file.contracts.directory.IDirectory'.
        """

        # Return the unique binding key for the directory service in the container
        return "x-orionis.services.file.contracts.directory.IDirectory"