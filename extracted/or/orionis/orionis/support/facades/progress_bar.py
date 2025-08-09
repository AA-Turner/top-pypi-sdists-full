from orionis.container.facades.facade import Facade

class ProgressBar(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the binding key for the progress bar service.

        Returns
        -------
        str
            The unique identifier used to retrieve the progress bar service from the service container.
        """
        return "core.orionis.progress_bar"
