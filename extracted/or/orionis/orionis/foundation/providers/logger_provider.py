from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.log_service import LoggerService

class LoggerProvider(ServiceProvider):
    """
    LoggerProvider
    ==============

    Registers the logging service in the application container.
    Provides a `LoggerService` instance for application-wide logging.

    Methods
    -------
    register()
        Registers the logging service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """

    def register(self) -> None:
        """
        Registers the logging service in the application container.

        Returns
        -------
        None
        """
        self.app.instance(ILoggerService, LoggerService(self.app.config('logging')), alias="core.orionis.logger")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass