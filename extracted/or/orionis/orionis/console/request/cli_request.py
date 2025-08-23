from typing import List
from orionis.console.entities.request import CLIRequest as CLIRequestEntity
from orionis.console.exceptions.cli_orionis_value_error import CLIOrionisValueError

class CLIRequest:
    def __call__(self, args: List[str]) -> "CLIRequestEntity":
        """
        Processes command-line arguments and returns a CLIRequest instance.

        Parameters
        ----------
        args : List[str]
            The list of command-line arguments. The first argument is expected to be the script name.

        Returns
        -------
        CLIRequestEntity
            An instance representing the parsed command and its arguments.

        Raises
        ------
        CLIOrionisValueError
            If the provided arguments are not a list or if no command is provided.
        """
        if not isinstance(args, list):
            raise CLIOrionisValueError(
                f"Failed to handle command line arguments: expected list, got {type(args).__module__}.{type(args).__name__}."
            )

        if len(args) <= 1:
            raise CLIOrionisValueError("No command provided to execute.")

        # Remove the script name
        args = args[1:]

        if not args or not args[0]:
            raise CLIOrionisValueError("No command provided to execute.")

        return CLIRequestEntity(
            command=args[0],
            args=args[1:]
        )

# Export the CLIRequest Singleton
Request = CLIRequest()