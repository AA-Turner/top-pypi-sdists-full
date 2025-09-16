from orionis.container.facades.facade import Facade

class Log(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Retrieves the service container binding key for the logger service.

        This method returns the unique string identifier used by the service container
        to resolve and provide the logger service implementation. The returned key acts
        as a bridge between the facade and the actual logger service instance registered
        in the dependency injection container.

        Returns
        -------
        str
            The string identifier
            "x-orionis.services.log.contracts.log_service.ILogger"
            which is used to resolve the logger service instance from the service container.
        """

        # Return the unique binding key for the logger service in the container
        return f"x-orionis.services.log.contracts.log_service.ILogger"
