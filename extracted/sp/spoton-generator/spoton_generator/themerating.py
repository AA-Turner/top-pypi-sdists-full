from .factor import Factor


class ThemeRating:
    """Implementation of how a persona would react to a given theme."""

    def __init__(
        self,
        id: str,
        rate: float,
        average: float,
        possible_values: list[int],
        factors: list[Factor],
    ):
        """Initialisation of the class.

        Parameters
        ----------
        id: str
            theme to react to
        rate: float
            how often an answer is given
        average: float
            mean value of the answers
        possible_values: list of int
            list of values that can be used
        factors: list of Factors
            list of factors
        """

        self.id: str = id
        self.rate: float = rate
        self.average: float = average
        self.possible_values: list[int] = possible_values
        self.factors: list[Factor] = factors

    def __str__(self):
        return f"{self.__class__.__name__} '{self.theme}'"

    def __repr__(self):
        return f"<Rating for '{self.theme}' theme"

    @classmethod
    def load(cls, item: dict):
        """Create class instance from dictionnary.

        Parameters
        ----------
        item: dict
            input to create the instance from.
        """

        rating = ThemeRating(
            item.get("id", "0"),
            item.get("rate", 1),
            item.get("average", 0),
            item.get("possible_values", []),
            [Factor.load(pattern) for pattern in item.get("factors", [])],
        )

        return rating
