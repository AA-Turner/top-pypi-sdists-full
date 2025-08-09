class OrionisTestValueError(Exception):

    def __init__(self, msg: str):
        """
        Initialize the OrionisTestValueError exception.

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
            The error message associated with this exception.
        """
        return str(self.args[0])
