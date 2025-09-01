from orionis.container.facades.facade import Facade
from orionis.console.contracts.progress_bar import IProgressBar

class ProgressBar(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Get the registered name of the component.

        This method returns the binding key that identifies the progress bar service
        within the service container. The facade uses this key to resolve the actual
        progress bar implementation when static methods are called.

        Returns
        -------
        str
            The service container binding key 'x-orionis.console.contracts.progress_bar.IProgressBar
            used to retrieve the progress bar service instance.
        """

        return f"x-{IProgressBar.__module__}.{IProgressBar.__name__}"
