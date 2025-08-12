from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.log_service import LoggerService

class LoggerProvider(ServiceProvider):
    """
    Service provider for logging functionality within the Orionis framework.

    The LoggerProvider is responsible for registering and configuring the logging
    service implementation in the application's dependency injection container.
    It binds the concrete LoggerService to the ILoggerService interface, enabling
    application-wide access to structured logging capabilities.

    This provider handles the initialization of the logging service with the
    application's configuration and ensures proper registration under both the
    interface contract and an internal framework alias for service resolution.

    Attributes
    ----------
    app : Application
        The application container instance used for service registration and
        configuration retrieval. Inherited from the base ServiceProvider class.

    Notes
    -----
    This provider follows the two-phase initialization pattern:
    - register(): Performs service binding and container registration
    - boot(): Handles post-registration initialization and setup
    """

    def register(self) -> None:
        """
        Register the logging service in the application container.

        This method binds the `LoggerService` implementation to the `ILoggerService`
        contract within the application's dependency injection container. The service
        is initialized with the application's logging configuration and registered
        with a specific alias for internal framework identification.

        The registration enables application-wide access to logging functionality
        through the container's service resolution mechanism.

        Returns
        -------
        None
            This method does not return any value. It performs service registration
            as a side effect on the application container.
        """

        # Retrieve logging configuration from application config
        logging_config = self.app.config('logging')

        # Create LoggerService instance with the retrieved configuration
        logger_service = LoggerService(logging_config)

        # Register the service instance in the container with interface binding and alias
        self.app.instance(
            ILoggerService,                             # Interface contract
            logger_service,                             # Concrete implementation instance
            alias="x-orionis.services.log.log_service"  # Internal framework alias
        )

    def boot(self) -> None:
        """
        Perform post-registration initialization for the logging service.

        This method is called after all service providers have been registered
        and allows for any additional configuration, setup, or initialization
        logic that depends on other services being available in the container.

        Currently, this method serves as a placeholder and performs no operations,
        but it can be extended to include logging service initialization tasks
        such as setting up log handlers, configuring formatters, or establishing
        connections to external logging systems.

        Returns
        -------
        None
            This method does not return any value. It performs initialization
            operations as side effects during the application boot process.
        """

        pass