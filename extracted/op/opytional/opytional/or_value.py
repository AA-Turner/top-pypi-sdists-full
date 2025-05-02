import typing


def or_value(
    maybe_value: typing.Optional[typing.Any],
    fallback_value: typing.Any,
) -> typing.Any:
    """Return maybe_value if not None; otherwise, return fallback_value.

    Parameters
    ----------
    maybe_value
        The value to test and return if it is not None.
    fallback_value
        The value to return if maybe_value is None.
    """

    if maybe_value is not None:
        return maybe_value
    else:
        return fallback_value
