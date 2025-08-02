from orionis.container.facades.facade import Facade

class Dumper(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the binding key used to retrieve the dumper component from the service container.

        This method provides the unique string identifier that the service container uses to resolve
        and return the dumper service instance. It is typically used internally by the Facade base class
        to access the underlying implementation.

        Returns
        -------
        str
            The string "core.orionis.dumper", which is the service container binding key for the dumper component.
        """

        # Return the service container binding key for the dumper component
        return "core.orionis.dumper"