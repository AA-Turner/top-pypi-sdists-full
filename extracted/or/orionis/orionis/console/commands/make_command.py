from pathlib import Path
import re
from typing import List
from orionis.console.args.argument import CLIArgument
from orionis.console.base.command import BaseCommand
from orionis.console.contracts.reactor import IReactor
from orionis.console.exceptions import CLIOrionisRuntimeError
from rich.console import Console
from rich.panel import Panel

from orionis.foundation.contracts.application import IApplication

class MakeCommand(BaseCommand):
    """
    Generates a new custom console command scaffold for the Orionis CLI.

    This command automates the creation of a Python file for a new CLI command, using a template stub.
    It ensures the generated command follows naming conventions and includes the specified signature.

    Attributes
    ----------
    timestamps : bool
        Indicates whether timestamps will be shown in the command output.
    signature : str
        The command signature.
    description : str
        The command description.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "make:command"

    # Command description
    description: str = "Creates a new custom console command for the Orionis CLI."

    async def options(self) -> List[CLIArgument]:
        """
        Defines the command-line options available for the `make:command` command.

        This method specifies the arguments that can be passed to the command when it is invoked
        from the CLI. It includes both required and optional arguments, each represented as a
        `CLIArgument` instance.

        Returns
        -------
        List[CLIArgument]
            A list of `CLIArgument` objects representing the available command-line options.
        """

        return [
            CLIArgument(
                flags=["name"],
                type=str,
                required=True,
                help="The filename where the new command will be created."
            ),
            CLIArgument(
                flags=["--signature", "-s"],
                type=str,
                required=False,
                help="The signature for the new command."
            ),
        ]

    def handle(self, app: IApplication) -> dict:
        """
        Handles the creation of a new custom console command file.

        This method processes the user-provided arguments, validates them, loads a command stub template,
        replaces placeholders with the appropriate values, and writes the resulting code to a new file
        in the commands directory. It also ensures that the file does not already exist and provides
        feedback to the user regarding the operation's success or failure.

        Parameters
        ----------
        app : IApplication
            The application instance used to resolve paths and interact with the application environment.

        Returns
        -------
        dict
            An empty dictionary. The method's primary purpose is side effects (file creation and user feedback).
        """

        try:

            # Retrieve the 'name' argument (required) and 'signature' argument (optional, with default)
            name: str = self.argument("name")
            signature: str = self.argument("signature", "custom:command")

            # Validate that the name argument is provided
            if not name:
                self.error("The 'name' argument is required.")

            # Validate that the file name starts with a lowercase letter and contains only lowercase letters, numbers, or underscores
            if not re.match(r'^[a-z][a-z0-9_]*$', name):
                self.error("The 'name' argument must start with a lowercase letter and contain only lowercase letters, numbers, and underscores (_).")

            # Validate the command signature: must start with a lowercase letter, can contain lowercase letters, numbers (not at the start), and the special characters ':' and '_'
            if not re.match(r'^[a-z][a-z0-9_:]*$', signature):
                self.error("The 'signature' argument must start with a lowercase letter and can only contain lowercase letters, numbers (not at the start), and the special characters ':' and '_'.")

            # Load the command stub template from the stubs directory
            stub_path = Path(__file__).parent.parent / "stubs" / "command.stub"
            with open(stub_path, "r", encoding="utf-8") as file:
                stub = file.read()

            # Generate the class name by capitalizing each word and appending 'Command'
            class_name = ''.join(word.capitalize() for word in name.split('_')) + "Command"
            # Replace placeholders in the stub with the actual class name and signature
            stub = stub.replace("{{class_name}}", class_name)
            stub = stub.replace("{{signature}}", signature)

            # Ensure the commands directory exists
            commands_dir = app.path('console') / "commands"
            commands_dir.mkdir(parents=True, exist_ok=True)
            file_path = commands_dir / f"{name}.py"

            # Check if the file already exists to prevent overwriting
            if file_path.exists():
                file_path = file_path.relative_to(app.path('root'))
                self.error(f"The file [{file_path}] already exists. Please choose another name.")
            else:
                # Write the generated command code to the new file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(stub)
                file_path = file_path.relative_to(app.path('root'))
                self.info(f"Console command [{file_path}] created successfully.")

        except Exception as e:

            # Catch any unexpected exceptions and raise a CLI-specific runtime error
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
