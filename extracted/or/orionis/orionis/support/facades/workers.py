from orionis.container.facades.facade import Facade

class Workers(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the binding key for the workers service in the service container.

        Returns
        -------
        str
            The identifier string for the workers service, used by the service container
            to resolve the corresponding implementation.
        """

        return "core.orionis.workers"
