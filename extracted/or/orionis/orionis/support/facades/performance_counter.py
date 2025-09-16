from orionis.container.facades.facade import Facade

class PerformanceCounter(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the registered binding key for the performance counter service in the service container.

        This method provides the unique string identifier used by the service container to resolve
        and retrieve the implementation of the performance counter service. It acts as the connection
        point between the facade and the underlying service registration, ensuring that the correct
        service is accessed when requested through the facade.

        Returns
        -------
        str
            The binding key 'x-orionis.support.performance.contracts.counter.IPerformanceCounter'
            which identifies the performance counter service implementation in the service container.
        """

        # Return the unique binding key for the performance counter service
        return "x-orionis.support.performance.contracts.counter.IPerformanceCounter"