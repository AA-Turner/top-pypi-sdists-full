from collections.abc import Callable


def cli_method(method: Callable) -> Callable:
    """
    Marks the provided method to be included in the automatically generated CLI of fitrequest.
    """
    method.cli_method = True
    return method
