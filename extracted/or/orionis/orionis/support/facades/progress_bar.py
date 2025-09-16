from orionis.container.facades.facade import Facade

class ProgressBar(Facade):

    @classmethod
    def getFacadeAccessor(cls):
        """
        Returns the service container binding key for the progress bar component.

        This method provides the unique string identifier used by the service container
        to resolve and retrieve the progress bar implementation. The facade relies on
        this binding key to delegate static method calls to the underlying progress bar
        service.

        Returns
        -------
        str
            The string 'x-orionis.console.contracts.progress_bar.IProgressBar', which
            is the binding key used to obtain the progress bar service instance from
            the service container.
        """

        # Return the binding key for the progress bar service in the container
        return "x-orionis.console.contracts.progress_bar.IProgressBar"
