from orionis.console.output.console import Console
from orionis.console.output.contracts.console import IConsole
from orionis.container.providers.service_provider import ServiceProvider

class ConsoleProvider(ServiceProvider):
    """
    Provides and registers the console output service within the application container.

    This provider binds the console output interface to its concrete implementation,
    enabling access to various console output features such as information, warnings,
    errors, debug messages, tables, confirmations, and password prompts.
    """

    def register(self) -> None:
        """
        Register the console output service in the application container.

        Binds the IConsole interface to the Console implementation as a transient service,
        with the alias "core.orionis.console".

        Returns
        -------
        None
        """

        self.app.transient(IConsole, Console, alias="core.orionis.console")

    def boot(self) -> None:
        """
        Perform post-registration initialization for the console provider.

        This method is a placeholder for any additional setup required after
        registration. Currently, it does not perform any actions.

        Returns
        -------
        None
        """

        pass
