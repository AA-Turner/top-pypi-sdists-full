class OrionisTestPersistenceError(Exception):

    def __init__(self, msg: str):
        """
        Initialize the OrionisTestPersistenceError with an error message.

        Parameters
        ----------
        msg : str
            The error message describing the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Return the string representation of the exception message.

        Returns
        -------
        str
            The error message associated with the exception.
        """
        return str(self.args[0])
