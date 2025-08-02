from orionis.console.contracts.kernel import IKernelCLI
from orionis.foundation.contracts.application import IApplication
from orionis.console.exceptions import CLIOrionisValueError

class KernelCLI(IKernelCLI):

    def __init__(
        self,
        app: IApplication
    ) -> None:

        # Validate that the app is an instance of IApplication
        if not isinstance(app, IApplication):
            raise CLIOrionisValueError(
                f"Failed to initialize TestKernel: expected IApplication, got {type(app).__module__}.{type(app).__name__}."
            )

    def handle(self, args: list) -> None:
        """
        Handle the command line arguments.

        :param args: List of command line arguments (e.g., sys.argv).
        """
        # This method should be implemented in subclasses
        print(args)