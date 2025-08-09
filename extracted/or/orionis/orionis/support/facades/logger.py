from orionis.container.facades.facade import Facade

class Log(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the binding key for the logger service in the service container.

        Returns
        -------
        str
            The unique identifier used to resolve the logger service, specifically
            "core.orionis.logger".
        """
        return "core.orionis.logger"
