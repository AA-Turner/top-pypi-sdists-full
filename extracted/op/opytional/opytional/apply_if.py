import typing


def apply_if(
    maybe_value: typing.Optional[typing.Any],
    operation: typing.Callable[[typing.Any], typing.Any],
) -> typing.Any:
    """Invoke operation on maybe_value if not None; otherwise, return None.

    Parameters
    ----------
    maybe_value
        The value to test and feed to operation if it is not None.
    operation: callable object
        The operation to apply to maybe_value if it is not None.

    Returns
    -------
    maybe_result
        The result of invoking operation on maybe_value, or None.
    """

    if maybe_value is not None:
        return operation(maybe_value)
    else:
        return None
