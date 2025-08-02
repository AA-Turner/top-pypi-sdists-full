class OrionisTestValueError(Exception):

    def __init__(self, msg: str):
        """
        Initializes the OrionisTestValueError with a descriptive error message.

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

        This method retrieves the error message provided during initialization
        and returns it as a string. It ensures that when the exception is
        converted to a string, the descriptive message is displayed.

        Returns
        -------
        str
            The descriptive error message associated with this exception.
        """

        # Return the error message stored in the first argument
        return str(self.args[0])