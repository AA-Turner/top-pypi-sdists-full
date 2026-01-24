from typing import (
    NoReturn,
)


def raise_exception(err: Exception) -> NoReturn:
    """Raise an error."""
    raise err


def cast_exception(err: Exception) -> Exception:
    """
    Cast an exception type.

    Useful for safe casting an `Exception` subclass into `Exception`.
    """
    return err
