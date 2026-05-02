class Pattern:
    """Implementation of how a pattern will repeat in time."""

    def __init__(self, step: int, start: int, value: int):
        """Initialisation of the class.


        Parameters
        ----------
        step: int
            how often the patterns repeats
        start: int
            when the patterns starts
        value: int
            value to repeat
        """

        self.step: int = step
        self.start: int = start
        self.value: int = value

    def __repr__(self):
        return f"<{self.__class__.__name__}> step:{self.step}, start: {self.start}, value: {self.value}"

    def __str__(self):
        return f"step:{self.step}, start: {self.start}, value: {self.value}"

    @classmethod
    def load(cls, item: dict):
        """Create class instance from dictionnary.

        Parameters
        ----------
        item: dict
            input to create the instance from.
        """

        return Pattern(
            item.get("step", 0),
            item.get("start", 0),
            item.get("value", 0),
        )
