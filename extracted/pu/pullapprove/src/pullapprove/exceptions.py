class LargeScaleChangeException(Exception):
    """
    Can be raised to indicate this is a large-scale change,
    often triggered by a diff so large the platform complains about it.
    """

    def __init__(self) -> None:
        super().__init__("Large scale change detected")
