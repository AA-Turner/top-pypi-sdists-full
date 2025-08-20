from orionis.container.facades.facade import Facade

class Application(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the registered service container binding key for the console component.

        This method returns the specific binding key that is used to resolve the
        console output service from the dependency injection container. The facade
        pattern uses this key to locate and instantiate the underlying console
        service implementation.

        Returns
        -------
        str
            The string identifier 'x-orionis.services.log.log_service' used as the
            binding key to resolve the console service from the service container.
        """

        # Return the predefined binding key for the console output service
        return "x-orionis.services.log.log_service"
