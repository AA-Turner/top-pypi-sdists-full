from orionis.console.contracts.progress_bar import IProgressBar
from orionis.console.dynamic.progress_bar import ProgressBar
from orionis.container.providers.service_provider import ServiceProvider

class ProgressBarProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the progress bar service in the application container.

        This method binds the `IProgressBar` interface to its concrete implementation,
        `ProgressBar`, using transient lifetime management. The service is registered
        with a specific alias for easy identification and retrieval from the container.
        Transient lifetime ensures that a new instance of `ProgressBar` is created
        each time the `IProgressBar` interface is resolved.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It registers the service as a side effect
            on the application container.
        """

        # Register the ProgressBar implementation as a transient service for IProgressBar.
        # The alias allows for explicit retrieval from the container if needed.
        self.app.transient(IProgressBar, ProgressBar, alias="x-orionis.console.contracts.progress_bar.IProgressBar")