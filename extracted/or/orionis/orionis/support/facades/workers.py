from orionis.container.facades.facade import Facade

class Workers(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the service container binding key for the workers component.

        This method provides the unique string identifier used by the service container
        to resolve the workers service. It is typically used internally by the Facade
        mechanism to access the underlying implementation.

        Returns
        -------
        str
            The string key "core.orionis.workers" that identifies the workers service
            in the service container.
        """

        # Return the binding key for the workers service in the container
        return "core.orionis.workers"