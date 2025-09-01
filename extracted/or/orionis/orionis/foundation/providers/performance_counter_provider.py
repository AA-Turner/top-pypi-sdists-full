from orionis.container.providers.service_provider import ServiceProvider
from orionis.support.performance.contracts.counter import IPerformanceCounter
from orionis.support.performance.counter import PerformanceCounter

class PerformanceCounterProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the performance counter service as a transient dependency in the application container.

        This method binds the `IPerformanceCounter` interface contract to the `PerformanceCounter`
        concrete implementation within the application's dependency injection container. The binding
        is configured with a transient lifetime, ensuring that each resolution of the service yields
        a new instance of `PerformanceCounter`. This approach is suitable for scenarios requiring
        independent timing or measurement operations across different parts of the application.

        Additionally, an alias `"x-orionis.support.performance.counter"` is assigned to this binding,
        allowing for alternative resolution or referencing of the service.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method performs service registration as a side effect and does not return any value.

        Notes
        -----
        - The transient lifetime ensures isolation between different consumers of the service.
        - The alias facilitates flexible service resolution by name.
        """

        # Register the IPerformanceCounter interface to the PerformanceCounter implementation
        # with a transient lifetime and assign an alias for alternative resolution.
        self.app.transient(IPerformanceCounter, PerformanceCounter, alias=f"x-{IPerformanceCounter.__module__}.{IPerformanceCounter.__name__}")

    def boot(self) -> None:
        """
        Performs initialization and configuration tasks for the performance counter provider during the application's bootstrapping phase.

        This method is automatically invoked when the provider is loaded by the application. It is intended for setting up or registering
        any performance counters or related resources required by the application. By default, this implementation does not perform any
        actions, but it can be extended in subclasses to include custom initialization logic as needed.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It executes initialization logic as a side effect.

        Notes
        -----
        - Override this method in subclasses to implement custom bootstrapping behavior for performance counters.
        - This method is part of the provider lifecycle and is called after service registration.
        """

        # No initialization logic is required by default.
        # Override this method in subclasses to perform custom setup.
        pass