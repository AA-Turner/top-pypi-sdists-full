from orionis.console.dynamic.contracts.progress_bar import IProgressBar
from orionis.console.dynamic.progress_bar import ProgressBar
from orionis.container.providers.service_provider import ServiceProvider

class ProgressBarProvider(ServiceProvider):
    """
    Service provider for registering the dynamic progress bar.

    This provider registers the `IProgressBar` interface with the `ProgressBar`
    implementation in the application container, allowing for dependency injection
    and usage of a console-based progress bar for visual feedback during operations.
    """

    def register(self) -> None:
        """
        Register the progress bar service in the application container.

        Registers the `IProgressBar` interface to resolve to the `ProgressBar`
        implementation, with the alias "core.orionis.progress_bar".

        Returns
        -------
        None
        """

        self.app.transient(IProgressBar, ProgressBar, alias="core.orionis.progress_bar")

    def boot(self) -> None:
        """
        Perform post-registration initialization.

        This method is called after all providers have been registered. No additional
        initialization is required for the progress bar service.

        Returns
        -------
        None
        """

        pass