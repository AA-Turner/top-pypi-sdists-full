from orionis.container.facades.facade import Facade

class Log(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the binding key used to resolve the logger service from the service container.

        This method provides the unique identifier required by the service container to retrieve
        the logger component. It is used internally by the Facade base class to delegate calls
        to the appropriate service implementation.

        Returns
        -------
        str
            The binding key for the logger service in the service container, specifically
            "core.orionis.logger".
        """

        # Return the service container binding key for the logger component
        return "core.orionis.logger"