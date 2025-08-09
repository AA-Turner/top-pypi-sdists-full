from orionis.container.facades.facade import Facade

class Dumper(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the service container binding key for the dumper component.

        Returns
        -------
        str
            The binding key "core.orionis.dumper" used to resolve the dumper service from the container.
        """
        return "core.orionis.dumper"
