from orionis.container.facades.facade import Facade

class Application(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Retrieve the service container binding key for the application component.

        This class method provides the unique string identifier (binding key) that is registered
        in the service container for the application interface. The facade uses this key to resolve
        and access the underlying application service implementation from the dependency injection container.

        Returns
        -------
        str
            The binding key "x-orionis.foundation.contracts.application.IApplication" used to resolve
            the application service from the service container.
        """

        # Return the predefined binding key for the application service
        return "x-orionis.foundation.contracts.application.IApplication"
