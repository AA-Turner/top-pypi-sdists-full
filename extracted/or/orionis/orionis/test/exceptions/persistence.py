class OrionisTestPersistenceError(Exception):

    def __init__(self, msg: str):
        """
        Initializes the OrionisTestPersistenceError with a descriptive error message.

        Parameters
        ----------
        msg : str
            A descriptive error message that explains the cause of the exception.
        """

        # Call the base Exception class constructor with the message
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the exception message.

        Returns
        -------
        str
            The error message provided when the exception was raised.
        """

        # Return the first argument passed to the exception as a string
        return str(self.args[0])
