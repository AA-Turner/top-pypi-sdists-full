import typing


def or_else(
    maybe_value: typing.Optional[typing.Any],
    fallback_callable: typing.Callable[[], typing.Any],
) -> typing.Any:
    """Return maybe_value if not None; otherwise, return the result of invoking
    fallback_callable.

    Parameters
    ----------
    maybe_value
        The value to test and return if it is not None.
    fallback_callable : callable object
        The nullary callable (takes no arguments) to return the result of if
        maybe_value is None.
    """

    if maybe_value is not None:
        return maybe_value
    else:
        return fallback_callable()
