from orionis.container.facades.facade import Facade

class Log(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the registered name of the component.

        This method returns the service container binding key that identifies
        the logger service implementation. It serves as the bridge between the
        facade and the actual service instance registered in the container.

        Returns
        -------
        str
            The service container binding key "x-orionis.services.log.log_service"
            used to resolve the logger service instance from the dependency
            injection container.
        """

        # Return the service container binding key for the logger service
        return "x-orionis.services.log.log_service"
