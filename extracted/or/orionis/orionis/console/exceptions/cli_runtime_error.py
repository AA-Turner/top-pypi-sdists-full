class CLIOrionisRuntimeError(RuntimeError):
    """
    Custom exception raised when there is a runtime issue with Orionis processing.

    Parameters
    ----------
    message : str
        The response message associated with the exception.

    Attributes
    ----------
    message : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, message: str):
        """
        Initializes the CLIOrionisRuntimeError with the given response message.

        Parameters
        ----------
        message : str
            The response message associated with the exception.
        """
        super().__init__(message)

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"CLIOrionisRuntimeError: {self.args[0]}"