from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.core.unit_test import UnitTest

class TestingProvider(ServiceProvider):
    """
    TestingProvider
    ===============

    Registers the unit testing environment service in the application container.
    Provides a native unit testing framework for Orionis with features beyond common frameworks.

    Methods
    -------
    register()
        Registers the unit testing service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """

    def register(self) -> None:
        """
        Registers the unit testing service in the application container.

        Returns
        -------
        None
        """
        self.app.singleton(IUnitTest, UnitTest, alias="core.orionis.testing")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass