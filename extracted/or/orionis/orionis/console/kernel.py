from orionis.console.contracts.kernel import IKernelCLI
from orionis.console.contracts.reactor import IReactor
from orionis.console.output.contracts.console import IConsole
from orionis.foundation.contracts.application import IApplication
from orionis.console.exceptions import CLIOrionisValueError
from orionis.services.log.contracts.log_service import ILogger

class KernelCLI(IKernelCLI):

    def __init__(
        self,
        app: IApplication
    ) -> None:
        """
        Initializes the KernelCLI instance with the provided application container.

        Parameters
        ----------
        app : IApplication
            The application container instance that provides access to services and dependencies.

        Returns
        -------
        None
            This constructor does not return a value. It initializes internal dependencies required for CLI operations.

        Raises
        ------
        CLIOrionisValueError
            If the provided `app` argument is not an instance of `IApplication`.
        """

        # Validate that the app is an instance of IApplication
        if not isinstance(app, IApplication):
            raise CLIOrionisValueError(
                f"Failed to initialize TestKernel: expected IApplication, got {type(app).__module__}.{type(app).__name__}."
            )

        # Retrieve and initialize the reactor instance from the application container.
        # The reactor is responsible for dispatching CLI commands.
        self.__reactor: IReactor = app.make('x-orionis.console.core.reactor', app)

        # Retrieve and initialize the console instance for command output and error handling.
        self.__console: IConsole = app.make('x-orionis.console.output.console')

        # Initialize the logger service for logging command execution details
        self.__logger: ILogger = app.make('x-orionis.services.log.log_service')

    def handle(self, args: list) -> None:
        """
        Processes and dispatches command line arguments to the appropriate command handler.

        Parameters
        ----------
        args : list
            The list of command line arguments, typically `sys.argv`.

        Returns
        -------
        None
            This method does not return a value. It may terminate the process or delegate execution to command handlers.

        Raises
        ------
        SystemExit
            If invalid arguments are provided or no command is specified, this method may terminate the process with an error message.
        """

        try:

            # Ensure the arguments are provided as a list
            if not isinstance(args, list):
                raise CLIOrionisValueError(
                    f"Failed to handle command line arguments: expected list, got {type(args).__module__}.{type(args).__name__}."
                )

            # If no arguments or only the script name is provided, show the default help command
            if not args or len(args) <= 1:
                return self.__reactor.call('help')

            # Remove the first argument (script name) to process only the command and its parameters
            args = args[1:]

            # If no command is provided after removing the script name, exit with an error
            if len(args) == 0:
                raise CLIOrionisValueError("No command provided to execute.")

            # If only the command is provided, call it without additional arguments
            if len(args) == 1:
                return self.__reactor.call(args[0])

            # If command and arguments are provided, call the command with its arguments
            return self.__reactor.call(args[0], args[1:])

        except SystemExit as e:

            # Log the SystemExit exception for debugging purposes
            self.__logger.error(f"SystemExit encountered: {str(e)}")

            # Handle SystemExit exceptions gracefully, allowing for clean exits with error messages
            self.__console.exitError(str(e))

        except Exception as e:

            # Log any unexpected exceptions that occur during command processing
            self.__logger.error(f"An unexpected error occurred while processing command: {str(e)}")

            # Handle any other exceptions that may occur during command processing
            self.__console.exitError(f"An unexpected error occurred: {str(e)}")