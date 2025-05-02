import typing


def apply_if_or_value(
    maybe_value: typing.Optional[typing.Any],
    operation: typing.Callable[[typing.Any], typing.Any],
    fallback_value: typing.Any,
) -> typing.Any:
    """Attempt to apply operation to maybe_value, returning fallback_value if
    maybe_value is None.

    Almost a convenience composition of or_value over apply_if, except that it
    *will* return None and not fallback_value if invoking operation on
    maybe_value returns None.

    Parameters
    ----------
    maybe_value
        The value to test and feed to operation if it is not None.
    operation: callable object
        The operation to apply to maybe_value if it is not None.
    fallback_value
        The value to return if maybe_value is None.

    Returns
    -------
    result
        The result of invoking operation on maybe_value, or fallback_value.
    """

    if maybe_value is not None:
        return operation(maybe_value)
    else:
        return fallback_value
