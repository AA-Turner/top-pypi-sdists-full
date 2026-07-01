from typing import Union


class Omit:
    """
    Sentinel class for parameters that were not explicitly provided by the user.
    It is used to explicitly omit something from being sent in a request.
    """

    def __bool__(self) -> bool:
        return False


OMIT = Omit()
Omittable = Union[Omit, object]
