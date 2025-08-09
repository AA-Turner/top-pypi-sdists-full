class OrionisEnvironmentValueException(Exception):

    def __init__(self, msg: str):
        """
        Initialize the OrionisEnvironmentValueException.

        Parameters
        ----------
        msg : str
            A descriptive error message that explains the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Return the string representation of the exception.

        Returns
        -------
        str
            The error message associated with the exception.
        """
        return str(self.args[0])
