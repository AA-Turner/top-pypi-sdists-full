class ReflectionValueError(Exception):

    def __init__(self, msg: str):
        """
        Parameters
        ----------
        msg : str
            Descriptive error message explaining the cause of the exception.
        """
        super().__init__(msg)

    def __str__(self) -> str:
        """
        Returns
        -------
        str
            Formatted string describing the exception.
        """
        return str(self.args[0])
