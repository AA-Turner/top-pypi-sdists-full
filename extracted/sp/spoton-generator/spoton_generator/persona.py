from .themerating import ThemeRating


class Persona:
    """Implementation of a fictional target"""

    def __init__(self, name: str, description: str, ratings: list[ThemeRating]):
        """Initialisation of the class.

        Parameters
        ----------
        name: str
            name of the persona
        description: str
            what are the persona's main characteristics
        ratings: list of ThemeRating
            to what themes and hiw is the persona answering
        """

        self.name: str = name
        self.description: str = description
        self.ratings: list[ThemeRating] = ratings

    def __str__(self):
        text = f"{self.name}:  {self.description} (rating {len(self.ratings)} themes)"
        return text

    def __repr__(self):
        return f"<{self.__class__.__name__}> '{self.name}': {self.ratings}"

    @classmethod
    def load(cls, item: dict):
        """Create class instance from dictionnary.

        Parameters
        ----------
        item: dict
            input to create the instance from.
        """

        name: str = item.get("name", "default")
        description: str = item.get("description", "-")
        ratings_dict = item.get("ratings", [])

        ratings = [ThemeRating.load(rating) for rating in ratings_dict]

        return cls(name, description, ratings)
