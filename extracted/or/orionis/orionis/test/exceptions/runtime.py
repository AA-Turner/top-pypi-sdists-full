class OrionisTestRuntimeError(Exception):

    def __init__(self, msg: str):
        """
        Initialize the OrionisTestRuntimeError with a specific error message.

        Parameters
        ----------
        msg : str
            The error message describing the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Return the string representation of the exception.

        Returns
        -------
        str
            The error message provided during initialization.
        """
        return str(self.args[0])
