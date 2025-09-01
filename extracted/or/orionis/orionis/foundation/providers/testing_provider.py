from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.core.unit_test import UnitTest

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
        Register and configure the unit testing service in the application container.

        This method loads the testing configuration from the application, instantiates
        and configures a UnitTest service, and registers it as a singleton in the
        dependency injection container. The service is bound to the IUnitTest interface
        and is accessible via the alias "x-orionis.test.core.unit_test".

        The registration process includes:
            - Retrieving testing configuration from the application settings.
            - Instantiating the UnitTest service with the appropriate configuration.
            - Registering the UnitTest service as a singleton in the container.
            - Binding the service to the IUnitTest interface and alias.

        Returns
        -------
        None
            This method does not return any value. It performs side effects by
            registering and binding the testing service in the application container.
        """

        # Register the UnitTest service as a singleton in the application container.
        # The service is bound to the IUnitTest interface and can be resolved using the alias.
        self.app.singleton(IUnitTest, UnitTest, alias=f"x-{IUnitTest.__module__}.{IUnitTest.__name__}")

    def boot(self) -> None:
        """
        Finalize initialization for the testing provider after service registration.

        This method is called after the registration phase to allow for any additional
        setup required for the testing environment. In this implementation, no further
        actions are performed during the boot phase.

        Returns
        -------
        None
            This method does not return any value.
        """
        pass
