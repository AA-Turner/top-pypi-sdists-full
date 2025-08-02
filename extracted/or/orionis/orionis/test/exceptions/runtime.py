class OrionisTestRuntimeError(Exception):

    def __init__(self, msg: str):
        """
        Initializes the OrionisTestRuntimeError with a descriptive error message.

        Parameters
        ----------
        msg : str
            Descriptive error message explaining the cause of the exception.
        """

        # Call the base class constructor with the error message
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the exception.

        Returns
        -------
        str
            The error message provided during exception initialization.
        """

        # Return the error message stored in the first argument
        return str(self.args[0])
