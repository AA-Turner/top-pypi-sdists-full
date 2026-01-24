r"""Contain functionalities to configure the records."""

from __future__ import annotations

__all__ = ["Config", "get_default_config", "get_max_size", "reset_max_size", "set_max_size"]


class Config:
    r"""Config class to configure the records.

    Example:
        ```pycon
        >>> from minrecord.config import Config
        >>> c = Config()
        >>> c.get_max_size()
        10
        >>> c.set_max_size(5)
        >>> c.get_max_size()
        5

        ```
    """

    DEFAULT_MAX_SIZE = 10

    def __init__(self) -> None:
        self._max_size = self.DEFAULT_MAX_SIZE

    def get_max_size(self) -> int:
        r"""Get the current default maximum size of values to track in
        each record.

        Returns:
            The current default maximum size of values to track in each
                record.

        Example:
            ```pycon
            >>> from minrecord.config import Config
            >>> c = Config()
            >>> c.get_max_size()
            10

            ```
        """
        return self._max_size

    def set_max_size(self, max_size: int) -> None:
        r"""Set the default maximum size of values to track in each
        record.

        This function does not change the maximum size of records that are
        already created. It only changes the maximum size of records that
        will be created after the call of this function.

        Args:
            max_size: The new default maximum size of values to track in
                each record. Must be a positive integer.

        Raises:
            ValueError: If max_size is not a positive integer.

        Example:
            ```pycon
            >>> from minrecord.config import Config
            >>> c = Config()
            >>> c.get_max_size()
            10
            >>> c.set_max_size(5)
            >>> c.get_max_size()
            5

            ```
        """
        if not isinstance(max_size, int) or max_size <= 0:
            msg = f"max_size must be a positive integer, got {max_size}"
            raise ValueError(msg)
        self._max_size = max_size

    def reset_max_size(self) -> None:
        r"""Reset max_size to its default value.

        Example:
            ```pycon
            >>> from minrecord.config import Config
            >>> c = Config()
            >>> c.set_max_size(5)
            >>> c.get_max_size()
            5
            >>> c.reset_max_size()
            >>> c.get_max_size()
            10

            ```
        """
        self._max_size = self.DEFAULT_MAX_SIZE


def get_default_config() -> Config:
    r"""Get the default global config instance.

    This function uses a singleton pattern to ensure the same config
    instance is returned on all calls. The config is created lazily on
    the first call and cached for subsequent calls.

    Returns:
        The singleton Config instance.

    Note:
        Since this returns a singleton, modifications to the config will
        persist across all calls and affect the entire application. To use
        an isolated config, create a new Config instance directly with
        ``Config()``.

    Example:
        ```pycon
        >>> from minrecord.config import get_default_config
        >>> c1 = get_default_config()
        >>> c1.get_max_size()
        10
        >>> c1.set_max_size(5)
        >>> # The change persists across calls
        >>> c2 = get_default_config()
        >>> c2.get_max_size()
        5
        >>> c1 is c2  # Same instance
        True
        >>> c1.reset_max_size()

        ```
    """
    if not hasattr(get_default_config, "_config"):
        config = Config()
        get_default_config._config = config
    return get_default_config._config


def get_max_size() -> int:
    r"""Get the current default maximum size of values to track in each
    record.

    Returns:
        The current default maximum size of values to track in each
            record.

    This value can be changed by using ``set_max_size``.

    Example:
        ```pycon
        >>> from minrecord.config import get_max_size
        >>> get_max_size()
        10

        ```
    """
    return get_default_config().get_max_size()


def set_max_size(max_size: int) -> None:
    r"""Set the default maximum size of values to track in each record.

    This function does not change the maximum size of records that are
    already created. It only changes the maximum size of records that
    will be created after the call of this function.

    Args:
        max_size: The new default maximum size of values to track in
            each record.

    Example:
        ```pycon
        >>> from minrecord.config import get_max_size, set_max_size
        >>> get_max_size()
        10
        >>> set_max_size(5)
        >>> get_max_size()
        5

        ```
    """
    get_default_config().set_max_size(max_size)


def reset_max_size() -> None:
    """Reset maximum size to its default value.

    Example:
        ```pycon
        >>> from minrecord.config import get_max_size, set_max_size, reset_max_size
        >>> set_max_size(5)
        >>> get_max_size()
        5
        >>> reset_max_size()
        >>> get_max_size()
        10

        ```
    """
    get_default_config().reset_max_size()
