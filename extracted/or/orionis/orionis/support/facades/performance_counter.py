from orionis.container.facades.facade import Facade
from orionis.support.performance.contracts.counter import IPerformanceCounter

class PerformanceCounter(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Get the registered name of the component in the service container.

        This method provides the binding key that the service container uses to
        resolve the workers service implementation. It serves as the bridge between
        the facade and the underlying service registration.

        Returns
        -------
        str
            The service container binding key 'x-orionis.support.performance.contracts.counter.IPerformanceCounter
            that identifies the workers service implementation.
        """

        return f"x-{IPerformanceCounter.__module__}.{IPerformanceCounter.__name__}"