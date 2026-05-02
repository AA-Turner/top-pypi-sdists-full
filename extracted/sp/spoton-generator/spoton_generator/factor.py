from .pattern import Pattern


class Factor:
    """Implementation of a theme factor."""

    def __init__(
        self,
        id: str,
        rate: float,
        patterns: list[Pattern],
    ):
        """Initialisation of the class.

        Parameters
        ----------
        id: int
            name of the factor
        rate: float
            how often an answer is given
        patterns: list of Patterns
            list of time repeating patterns
        """

        self.id: str = id
        self.rate: float = rate
        self.patterns: list[Pattern] = patterns

    def __str__(self):
        return f"{self.__class__.__name__} '{self.name}'"

    def __repr__(self):
        return f"<Factor {id}"

    @classmethod
    def load(cls, item: dict):
        """Create class instance from dictionnary.

        Parameters
        ----------
        item: dict
            input to create the instance from.
        """

        factor = Factor(
            item.get("id", "0.0"),
            item.get("rate", 1),
            [Pattern.load(pattern) for pattern in item.get("patterns", [])],
        )

        return factor
