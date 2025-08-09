from orionis.container.facades.facade import Facade

class PathResolver(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the binding key for the path resolver service in the container.

        Returns
        -------
        str
            The unique string identifier for the path resolver service, used by the service container.
        """
        return "core.orionis.path_resolver"
