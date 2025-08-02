class OrionisTestConfigException(Exception):

    def __init__(self, msg: str):
        """
        Initializes the OrionisTestConfigException with a descriptive error message.

        Parameters
        ----------
        msg : str
            Descriptive error message explaining the cause of the exception.
        """

        # Call the base Exception class constructor with the message
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the exception message.

        Returns
        -------
        str
            The error message provided during exception initialization.
        """

        # Return the first argument as the exception message
        return str(self.args[0])
