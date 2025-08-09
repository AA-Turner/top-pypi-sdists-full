from orionis.console.dumper.dump import Debug
from orionis.console.dumper.contracts.dump import IDebug
from orionis.container.providers.service_provider import ServiceProvider

class DumperProvider(ServiceProvider):
    """
    Service provider for registering the debug message service.

    This provider registers the debug service in the application container,
    enabling debug message printing, error reporting, and console diagnostics.

    Attributes
    ----------
    app : Application
        The application container instance where services are registered.

    Methods
    -------
    register()
        Register the debug service in the application container.
    boot()
        Perform post-registration initialization if required.
    """

    def register(self) -> None:
        """
        Register the debug service in the application container.

        Registers the `IDebug` interface with the `Debug` implementation
        as a transient service, using the alias "core.orionis.dumper".

        Returns
        -------
        None
        """

        self.app.transient(IDebug, Debug, alias="core.orionis.dumper")

    def boot(self) -> None:
        """
        Perform post-registration initialization if required.

        This method is a placeholder for any initialization logic that
        should occur after the service has been registered.

        Returns
        -------
        None
        """

        pass