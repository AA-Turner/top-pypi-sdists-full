from orionis.container.providers.service_provider import ServiceProvider
from orionis.support.performance.contracts.counter import IPerformanceCounter
from orionis.support.performance.counter import PerformanceCounter

class PerformanceCounterProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the performance counter service as a transient dependency in the application container.

        This method binds the `IPerformanceCounter` interface to the `PerformanceCounter` implementation
        within the application's dependency injection container. The binding uses a transient lifetime,
        ensuring that each resolution of the service provides a new instance of `PerformanceCounter`.
        This is useful for scenarios where independent timing or measurement operations are required
        across different parts of the application.

        An alias, `"x-orionis.support.performance.contracts.counter.IPerformanceCounter"`, is also
        assigned to this binding, enabling alternative resolution or referencing of the service by name.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs service registration as a side effect.

        Notes
        -----
        - The transient lifetime ensures that each consumer receives a separate instance of the service.
        - The alias allows for flexible service resolution by a specific name.
        """

        # Register the IPerformanceCounter interface to the PerformanceCounter implementation
        # with a transient lifetime. Each resolution yields a new instance.
        # Assign an alias for alternative resolution by name.
        self.app.transient(IPerformanceCounter, PerformanceCounter, alias="x-orionis.support.performance.contracts.counter.IPerformanceCounter")