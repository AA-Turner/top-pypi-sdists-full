from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.core.unit_test import UnitTest
from orionis.foundation.config.testing.entities.testing import Testing
import os

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

        # Create a Testing configuration instance from the application config
        config = Testing(**self.app.config('testing'))

        # Create a UnitTest instance
        unit_test = UnitTest(
            app=self.app
        )

        # Configure the UnitTest instance with settings from the Testing configuration
        unit_test.configure(
            verbosity=config.verbosity,
            execution_mode=config.execution_mode,
            max_workers=config.max_workers,
            fail_fast=config.fail_fast,
            print_result=config.print_result,
            throw_exception=config.throw_exception,
            persistent=config.persistent,
            persistent_driver=config.persistent_driver,
            web_report=config.web_report
        )

        # Discover tests based on the configuration
        unit_test.discoverTests(
            base_path=config.base_path,
            folder_path=config.folder_path,
            pattern=config.pattern,
            test_name_pattern=config.test_name_pattern,
            tags=config.tags
        )

        # Register the UnitTest instance in the application container
        self.app.instance(IUnitTest, unit_test, alias="core.orionis.testing")

    def boot(self) -> None:
        """
        Perform post-registration initialization if required.

        This method is intended for any setup needed after service registration.
        Currently, no additional initialization is performed.

        Returns
        -------
        None
        """

        # Ensure directory for testing storage exists
        storage_path = self.app.path('storage_testing')
        if not os.path.exists(storage_path):
            os.makedirs(storage_path, exist_ok=True)