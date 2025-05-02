import typing


def apply_if_or_else(
    maybe_value: typing.Optional[typing.Any],
    operation: typing.Callable[[typing.Any], typing.Any],
    fallback_callable: typing.Callable[[], typing.Any],
) -> typing.Any:
    """Attempt to apply operation to maybe_value, returning the result of
    invoking fallback_callable if maybe_value is None.

    Almost a convenience composition of or_else over apply_if, except that it
    *will* return None and not the result of fallback_callable if invoking
    operation on maybe_value returns None.

    Parameters
    ----------
    maybe_value
        The value to test and feed to operation if it is not None.
    operation: callable object
        The operation to apply to maybe_value if it is not None.
    fallback_callable : callable object
        The nullary callable (takes no arguments) to return the result of if
        maybe_value is None.

    Returns
    -------
    result
        The result of invoking operation on maybe_value, or the result of
        invoking fallback_callable.
    """

    if maybe_value is not None:
        return operation(maybe_value)
    else:
        return fallback_callable()
