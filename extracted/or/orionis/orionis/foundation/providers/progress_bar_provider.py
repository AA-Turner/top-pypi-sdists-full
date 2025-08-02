from orionis.console.dynamic.contracts.progress_bar import IProgressBar
from orionis.console.dynamic.progress_bar import ProgressBar
from orionis.container.providers.service_provider import ServiceProvider

class ProgressBarProvider(ServiceProvider):
    """
    ProgressBarProvider
    ===================

    Registers the dynamic progress bar service in the application container.
    Provides a console progress bar for visual feedback during operations.

    Methods
    -------
    register()
        Registers the progress bar service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """

    def register(self) -> None:
        """
        Registers the progress bar service in the application container.

        Returns
        -------
        None
        """
        self.app.transient(IProgressBar, ProgressBar, alias="core.orionis.progress_bar")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass