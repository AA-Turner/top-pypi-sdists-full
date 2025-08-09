class OrionisEnvironmentValueError(Exception):

    def __init__(self, msg: str):
        """
        Initialize the OrionisEnvironmentValueError exception.

        Parameters
        ----------
        msg : str
            A descriptive error message explaining the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Return a formatted string describing the exception.

        Returns
        -------
        str
            The error message associated with the exception.
        """
        return str(self.args[0])
