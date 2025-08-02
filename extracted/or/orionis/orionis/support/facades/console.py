from orionis.container.facades.facade import Facade

class Console(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the service container binding key used to resolve the console component.

        This method provides the unique string identifier that the service container uses
        to locate and instantiate the console service. It is typically used internally
        by the Facade base class to delegate calls to the underlying implementation.

        Returns
        -------
        str
            The string key `"core.orionis.console"` that identifies the console service in the container.
        """

        # Return the binding key for the console service in the container
        return "core.orionis.console"