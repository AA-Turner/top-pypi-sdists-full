class OrionisCoroutineException(Exception):

    def __init__(self, msg: str):
        """
        Initializes an OrionisCoroutineException with a descriptive error message.

        Parameters
        ----------
        msg : str
            Descriptive error message explaining the cause of the exception.
        """

        # Call the base Exception constructor with the provided message
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the exception message.

        Returns
        -------
        str
            The error message provided during exception initialization.
        """

        # Return the first argument passed to the Exception, which is the error message
        return str(self.args[0])
