from typing import Iterable


def ensure_known(target: str, value: str, known: Iterable) -> None:
    """
    Validate whether the a target argument is known and supported. The
    ``target`` is only used to provide a friendlier message to the user.
    The given ``value`` is checked against ``known`` and ``supported``.

    :param target: name of the target, as known to the end-user.
    :param value: value of the target key.
    :param known: known possible values for the target.

    Raises:
          :class:`ValueError`: if given value is not in ``known``.
    """
    if value not in known:
        raise ValueError(f'{target}={value} must be one of {known}')
