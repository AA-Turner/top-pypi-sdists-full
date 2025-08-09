from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.log_service import LoggerService

class LoggerProvider(ServiceProvider):
    """
    Provides and registers the logging service within the application container.

    This provider binds an implementation of `ILoggerService` to the application,
    making a `LoggerService` instance available for application-wide logging.

    Attributes
    ----------
    app : Application
        The application container instance where services are registered.
    """

    def register(self) -> None:
        """
        Register the logging service in the application container.

        This method binds the `LoggerService` implementation to the `ILoggerService`
        contract in the application container, using the application's logging configuration.

        Returns
        -------
        None
        """

        self.app.instance(ILoggerService, LoggerService(self.app.config('logging')), alias="core.orionis.logger")

    def boot(self) -> None:
        """
        Perform post-registration initialization for the logging service.

        This method is a placeholder for any additional setup required after
        the logging service has been registered.

        Returns
        -------
        None
        """

        pass