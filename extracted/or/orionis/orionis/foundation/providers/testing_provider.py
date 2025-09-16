from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.core.unit_test import UnitTest

class TestingProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers and configures the unit testing service within the application container.

        This method retrieves the application's testing configuration, creates an instance
        of the UnitTest service, and registers it as a singleton in the dependency injection
        container. The service is bound to the `IUnitTest` interface and is accessible via
        the alias `"x-orionis.test.contracts.unit_test.IUnitTest"`.

        The registration process includes:
            - Retrieving the testing configuration from the application settings.
            - Instantiating the UnitTest service with the retrieved configuration.
            - Registering the UnitTest service as a singleton in the container.
            - Binding the service to the `IUnitTest` interface and an alias for resolution.

        Returns
        -------
        None
            This method does not return any value. It performs side effects by
            registering and binding the testing service in the application container.
        """

        # Register the UnitTest service as a singleton in the application container.
        # The service is bound to the IUnitTest interface and can be resolved using the alias.
        self.app.singleton(IUnitTest, UnitTest, alias="x-orionis.test.contracts.unit_test.IUnitTest")