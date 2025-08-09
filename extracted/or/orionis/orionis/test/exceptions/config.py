class OrionisTestConfigException(Exception):

    def __init__(self, msg: str):
        """
        Initialize the OrionisTestConfigException.

        Parameters
        ----------
        msg : str
            The error message describing the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Return the exception message as a string.

        Returns
        -------
        str
            The error message provided during initialization.
        """
        return str(self.args[0])
