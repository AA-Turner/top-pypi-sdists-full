from orionis.container.facades.facade import Facade

class Inspire(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Retrieves the binding key used to resolve the 'inspire' service from the service container.

        This method provides the unique identifier string that the service container uses to locate
        and return the implementation associated with the 'inspire' service. It is typically used
        internally by the Facade base class to delegate calls to the appropriate service instance.

        Returns
        -------
        str
            The binding key "core.orionis.inspire" that identifies the 'inspire' service in the container.
        """

        return "core.orionis.inspire"
