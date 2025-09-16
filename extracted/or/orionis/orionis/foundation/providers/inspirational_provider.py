from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.inspirational.contracts.inspire import IInspire
from orionis.services.inspirational.inspire import Inspire

class InspirationalProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the inspirational service as a transient binding in the application container.

        This method binds the `IInspire` interface to its concrete implementation `Inspire`
        as a transient service within the application's service container. Each time the
        service is requested, a new instance of `Inspire` will be provided. The service is
        also registered with a specific alias to facilitate convenient resolution and
        identification throughout the application.

        This registration enables dependency injection, allowing other components to
        receive an instance of `Inspire` whenever the `IInspire` contract is requested.

        Returns
        -------
        None
            This method does not return any value. It performs service registration as a side effect.
        """

        # Register the IInspire contract to the Inspire implementation as a transient service.
        # Each resolution from the container will provide a new instance.
        self.app.transient(IInspire, Inspire, alias="x-orionis.services.inspirational.contracts.inspire.IInspire")