from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.log.contracts.log_service import ILogger
from orionis.services.log.log_service import Logger

class LoggerProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the Logger service implementation in the application container.

        This method binds the `Logger` class to the `ILogger` contract within the application's
        dependency injection container. It retrieves the logging configuration from the application,
        creates a `Logger` instance using this configuration, and registers it with an alias for
        internal framework identification. This setup allows the logging service to be resolved
        and used throughout the application via the container.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs service registration
            as a side effect on the application container.
        """

        # Retrieve the logging configuration from the application
        logging_config = self.app.config('logging')

        # Instantiate the Logger with the retrieved configuration
        logger_instance = Logger(logging_config)

        # Register the Logger instance in the application container,
        # binding it to the ILogger contract and assigning an alias
        self.app.instance(ILogger, logger_instance, alias="x-orionis.services.log.contracts.log_service.ILogger")