from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.core.unit_test import UnitTest

class TestingProvider(ServiceProvider):
    """
    Provides and registers the unit testing environment service in the application container.

    This provider integrates a native unit testing framework for Orionis,
    enabling advanced testing features and registering the service as a singleton
    within the application's dependency injection container.

    Attributes
    ----------
    app : Application
        The application container instance where services are registered.
    """

    def register(self) -> None:
        """
        Register the unit testing service in the application container.

        Registers the IUnitTest interface to the UnitTest implementation as a singleton,
        with the alias "core.orionis.testing".

        Returns
        -------
        None
        """

        self.app.singleton(IUnitTest, UnitTest, alias="core.orionis.testing")

    def boot(self) -> None:
        """
        Perform post-registration initialization if required.

        This method is intended for any setup needed after service registration.
        Currently, no additional initialization is performed.

        Returns
        -------
        None
        """

        pass