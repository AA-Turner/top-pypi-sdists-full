from orionis.console.base.command import BaseCommand
from orionis.console.contracts.reactor import IReactor
from orionis.console.exceptions import CLIOrionisRuntimeError
from rich.console import Console
from rich.panel import Panel

class MakeListenerCommand(BaseCommand):
    """
    Este comando se encarga de crear los listener tando para CLI como para otro tipo de Eventos.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "make:listener"

    # Command description
    description: str = "Displays usage information, examples, and a list of available commands in the Orionis CLI."

    def handle(self) -> dict:
        """
        Displays usage information and a list of available commands for the Orionis CLI.

        Parameters
        ----------
        reactor : IReactor
            The reactor instance providing command metadata via the `info()` method.

        Returns
        -------
        dict
            A dictionary containing the list of available commands, each with its signature and description.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during help information generation or display.
        """
        try:

            # Solicitar el nombre del listener al usuario
            ans = self.choice(
                question="Tipo de Listener",
                choices=[
                    "Listener para eventos CLI",
                    "Listener para eventos de Schedule",
                ],
                default_index=0
            )

            print(ans)

        except Exception as e:

            # Raise a custom runtime error if any exception occurs
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
