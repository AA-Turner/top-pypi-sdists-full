class OrionisStdValueException(Exception):

    def __init__(self, msg: str):
        """
        Parameters
        ----------
        msg : str
            The error message that describes the reason for the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            The error message associated with this exception.
        """
        return str(self.args[0])
