from orionis.container.facades.facade import Facade

class ProgressBar(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the binding key used to retrieve the progress bar service from the service container.

        This method provides the unique string identifier that the service container uses to resolve
        the progress bar component. It is typically used internally by the Facade system to access
        the underlying implementation.

        Returns
        -------
        str
            The binding key for the progress bar service in the service container, specifically
            "core.orionis.progress_bar".
        """

        # Return the service container binding key for the progress bar component
        return "core.orionis.progress_bar"