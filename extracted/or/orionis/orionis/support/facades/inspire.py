from orionis.container.facades.facade import Facade
from orionis.services.inspirational.contracts.inspire import IInspire

class Inspire(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Get the registered name of the component.

        This method returns the service container binding key that identifies the
        inspirational service implementation. The facade system uses this accessor
        to resolve the underlying service instance from the IoC container when
        facade methods are called.

        Returns
        -------
        str
            The service container binding key 'x-orionis.services.inspirational.contracts.inspire.IInspire'
            used to resolve the inspirational service instance.
        """

        # Return the service container binding key for the inspirational service
        return f"x-{IInspire.__module__}.{IInspire.__name__}"
