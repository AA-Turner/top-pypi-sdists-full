from orionis.console.contracts.progress_bar import IProgressBar
from orionis.console.dynamic.progress_bar import ProgressBar
from orionis.container.providers.service_provider import ServiceProvider

class ProgressBarProvider(ServiceProvider):
    """
    Service provider for dynamic progress bar functionality.

    This provider is responsible for registering the dynamic progress bar service
    within the application's dependency injection container. It binds the IProgressBar
    interface to its concrete ProgressBar implementation, enabling the creation of
    visual progress indicators for long-running operations in console applications.

    The provider follows the transient lifetime pattern, ensuring that each request
    for a progress bar service creates a new, independent instance. This approach
    prevents state conflicts when multiple progress bars are used simultaneously
    across different parts of the application.

    Parameters
    ----------
    None
        This class does not accept initialization parameters beyond those
        inherited from the base ServiceProvider class.

    Returns
    -------
    None
        Service providers do not return values as they are used for
        registration and configuration purposes only.

    Notes
    -----
    The progress bar service is registered with the alias 'x-orionis.console.dynamic.progress_bar'
    to enable specific identification and retrieval from the container when needed.
    This provider requires the orionis container framework to be properly initialized
    before registration can occur.
    """

    def register(self) -> None:
        """
        Register the progress bar service in the application container.

        This method binds the IProgressBar interface to the ProgressBar concrete
        implementation using transient lifetime management. The service is registered
        with a specific alias for identification and retrieval within the container.

        The transient lifetime ensures that a new instance of ProgressBar is created
        each time the IProgressBar interface is resolved from the container.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs service registration
            as a side effect on the application container.
        """

        self.app.transient(IProgressBar, ProgressBar, alias=f"x-{IProgressBar.__module__}.{IProgressBar.__name__}")

    def boot(self) -> None:
        """
        Perform post-registration initialization for the progress bar provider.

        This method is called after all service providers have been registered
        in the application container. It provides an opportunity to perform
        any additional setup or configuration that depends on other services
        being available. For the progress bar provider, no additional
        initialization steps are required as the service is fully configured
        during registration.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It serves as a lifecycle
            hook for post-registration initialization.
        """

        pass