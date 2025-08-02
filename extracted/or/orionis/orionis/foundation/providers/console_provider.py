from orionis.console.output.console import Console
from orionis.console.output.contracts.console import IConsole
from orionis.container.providers.service_provider import ServiceProvider

class ConsoleProvider(ServiceProvider):
    """
    ConsoleProvider
    ===============

    Registers the console output service in the application container.
    Provides access to various console output features, including information, warnings, errors, debug messages, tables, confirmations, and password prompts.

    Methods
    -------
    register()
        Registers the console service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """

    def register(self) -> None:
        """
        Registers the console service in the application container.

        Returns
        -------
        None
        """
        self.app.transient(IConsole, Console, alias="core.orionis.console")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass