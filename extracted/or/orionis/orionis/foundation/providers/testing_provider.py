from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.core.unit_test import UnitTest
from orionis.foundation.config.testing.entities.testing import Testing
import os

class TestingProvider(ServiceProvider):
    """
    Provides comprehensive unit testing environment services for the Orionis framework.

    This service provider integrates a native unit testing framework into the Orionis
    application ecosystem, enabling advanced testing capabilities with configurable
    execution modes, parallel processing, and persistent result storage. The provider
    registers the testing service as a singleton within the application's dependency
    injection container, making it available throughout the application lifecycle.

    The TestingProvider handles the complete lifecycle of testing services, from
    initial configuration and test discovery to storage preparation and service
    registration. It supports various testing patterns, execution strategies, and
    reporting mechanisms to accommodate different testing scenarios and requirements.

    Attributes
    ----------
    app : Application
        The Orionis application container instance that manages service registration,
        configuration access, and dependency injection throughout the framework.

    Notes
    -----
    This provider follows the Orionis service provider pattern, implementing both
    register() and boot() methods to ensure proper service initialization and
    post-registration setup. The testing service is registered with the interface
    binding IUnitTest and can be resolved using the alias "x-orionis.test.core.unit_test".

    The provider requires a valid testing configuration section in the application
    configuration, which should include settings for verbosity, execution mode,
    worker configuration, and storage paths.
    """

    def register(self) -> None:
        """
        Register the unit testing service in the application container.

        This method creates and configures a UnitTest instance using the application's
        testing configuration, discovers test files based on specified patterns and paths,
        and registers the configured testing service as a singleton in the dependency
        injection container with the IUnitTest interface binding.

        The registration process includes:
        - Loading testing configuration from the application config
        - Creating and configuring a UnitTest instance with various settings
        - Discovering test files based on configuration parameters
        - Binding the service to the container with alias "x-orionis.test.core.unit_test"

        Returns
        -------
        None
            This method does not return any value. It performs side effects by
            registering the testing service in the application container.
        """

        # Load testing configuration from application config and create Testing instance
        config = Testing(**self.app.config('testing'))

        # Instantiate the UnitTest implementation with application reference
        unit_test = UnitTest(
            app=self.app
        )

        # Apply configuration settings to the UnitTest instance
        unit_test.configure(
            verbosity=config.verbosity,                 # Set output verbosity level
            execution_mode=config.execution_mode,       # Configure test execution mode
            max_workers=config.max_workers,             # Set maximum worker threads for parallel execution
            fail_fast=config.fail_fast,                 # Enable/disable fail-fast behavior
            print_result=config.print_result,           # Control result output printing
            throw_exception=config.throw_exception,     # Configure exception throwing behavior
            persistent=config.persistent,               # Enable/disable persistent test results
            persistent_driver=config.persistent_driver, # Set persistent storage driver
            web_report=config.web_report                # Enable/disable web-based reporting
        )

        # Discover and load test files based on configuration criteria
        unit_test.discoverTests(
            base_path=config.base_path,                 # Root directory for test discovery
            folder_path=config.folder_path,             # Specific folder path within base_path
            pattern=config.pattern,                     # File name pattern for test files
            test_name_pattern=config.test_name_pattern, # Pattern for test method names
            tags=config.tags                            # Tags to filter tests during discovery
        )

        # Register the configured UnitTest instance in the DI container
        # Binds IUnitTest interface to the UnitTest implementation as a singleton
        self.app.instance(IUnitTest, unit_test, alias="x-orionis.test.core.unit_test")

    def boot(self) -> None:
        """
        Perform post-registration initialization for the testing provider.

        This method is called after the service registration phase to handle any
        additional setup required for the testing environment. It ensures that
        the necessary storage directories for testing operations are created
        and available before test execution begins.

        The boot process includes:
        - Creating the testing storage directory if it doesn't exist
        - Setting appropriate permissions for the storage path
        - Preparing the filesystem structure for test artifacts

        Returns
        -------
        None
            This method does not return any value. It performs initialization
            side effects by creating required directories in the filesystem.
        """

        # Retrieve the configured storage path for testing artifacts and temporary files
        storage_path = self.app.path('storage_testing')

        # Check if the testing storage directory exists in the filesystem
        if not os.path.exists(storage_path):

            # Create the directory structure recursively, including parent directories
            # exist_ok=True prevents errors if directory is created by another process
            os.makedirs(storage_path, exist_ok=True)