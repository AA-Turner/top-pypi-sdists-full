from orionis.container.facades.facade import Facade

class PathResolver(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the service container binding key used to resolve the path resolver component.

        This method provides the unique string identifier that the service container uses
        to locate and retrieve the path resolver service. It is typically used internally
        by the facade mechanism to delegate calls to the appropriate underlying implementation.

        Returns
        -------
        str
            The string key "core.orionis.path_resolver" that identifies the path resolver
            service in the container.
        """

        # Return the binding key for the path resolver service in the container
        return "core.orionis.path_resolver"