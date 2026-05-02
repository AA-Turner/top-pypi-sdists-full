from .question import Question


class Theme:
    """Implementation of a theme containing questions."""

    def __init__(self, name: str):
        """Initialisation of the class.

        Parameters
        ----------
        name: str
            name of the theme
        """

        self.name: str = name
        self.questions: Question = []

    def __str__(self):
        return f"<Theme> '{self.name}': {len(self.questions)} questions"

    def __repr__(self):
        return self.__str__()
