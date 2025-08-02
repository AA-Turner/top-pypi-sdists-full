from orionis.console.dumper.dump import Debug
from orionis.console.dumper.contracts.dump import IDebug
from orionis.container.providers.service_provider import ServiceProvider

class DumperProvider(ServiceProvider):
    """
    DumperProvider
    ==============

    Registers the debug message service in the application container.
    Provides access to debug message printing, error reporting, and other console diagnostics.

    Methods
    -------
    register()
        Registers the debug service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """

    def register(self) -> None:
        """
        Registers the debug service in the application container.

        Returns
        -------
        None
        """
        self.app.transient(IDebug, Debug, alias="core.orionis.dumper")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass