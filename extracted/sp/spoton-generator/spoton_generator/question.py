class Question:
    """Implementation of a question."""

    def __init__(self, text: str):
        """Initialisation of the class.

        Parameters
        ----------
        text: str
            content of the question
        """
        self.text: str = text

    def __str__(self):
        return f"<{self.__class__.__name__}> {self.text}"

    def __repr__(self):
        return self.text
