from orionis.container.facades.facade import Facade

class Console(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the service container binding key for the console component.

        Returns
        -------
        str
            The binding key used to resolve the console service from the container.
        """
        return "core.orionis.console"
