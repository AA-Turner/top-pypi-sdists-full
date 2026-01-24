r"""Contain the base class to implement a data loader or saver
object."""

from __future__ import annotations

__all__ = [
    "BaseFileSaver",
    "BaseLoader",
    "BaseSaver",
    "is_loader_config",
    "is_saver_config",
    "setup_loader",
    "setup_saver",
]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from coola.equality.testers import EqualityTester
from objectory import AbstractFactory
from objectory.utils import is_object_config

from iden.io.utils import generate_unique_tmp_path
from iden.utils.comparator import ObjectEqualityComparator

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T")

logger: logging.Logger = logging.getLogger(__name__)


class BaseLoader(ABC, Generic[T], metaclass=AbstractFactory):
    r"""Define the base class to implement a data loader.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json, JsonLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("data.json")
        ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
        ...     data = JsonLoader().load(path)
        ...     data
        ...
        {'key1': [1, 2, 3], 'key2': 'abc'}

        ```
    """

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two objects are equal or not.

        Args:
            other: The object to compare with.
            equal_nan: If ``True``, then two ``NaN``s will be
                considered equal.

        Returns:
            ``True`` if the two objects are equal, otherwise ``False``.

        Example:
            ```pycon
            >>> from iden.io import JsonLoader, YamlLoader
            >>> JsonLoader().equal(JsonLoader())
            True
            >>> JsonLoader().equal(YamlLoader())
            False

            ```
        """

    @abstractmethod
    def load(self, path: Path) -> T:
        r"""Load the data from the given path.

        Args:
            path: The path with the data to load.

        Returns:
            The data

        Example:
            ```pycon
            >>> import tempfile
            >>> from pathlib import Path
            >>> from iden.io import save_json, JsonLoader
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            ...     path = Path(tmpdir).joinpath("data.json")
            ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
            ...     data = JsonLoader().load(path)
            ...     data
            ...
            {'key1': [1, 2, 3], 'key2': 'abc'}

            ```
        """


class BaseSaver(ABC, Generic[T], metaclass=AbstractFactory):
    r"""Define the base class to implement a data saver.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import JsonSaver, JsonLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("data.json")
        ...     JsonSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
        ...     data = JsonLoader().load(path)
        ...     data
        ...
        {'key1': [1, 2, 3], 'key2': 'abc'}

        ```
    """

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two objects are equal or not.

        Args:
            other: The object to compare with.
            equal_nan: If ``True``, then two ``NaN``s will be
                considered equal.

        Returns:
            ``True`` if the two objects are equal, otherwise ``False``.

        Example:
            ```pycon
            >>> from iden.io import JsonSaver, YamlSaver
            >>> JsonSaver().equal(JsonSaver())
            True
            >>> JsonSaver().equal(YamlSaver())
            False

            ```
        """

    @abstractmethod
    def save(self, to_save: T, path: Path, *, exist_ok: bool = False) -> None:
        r"""Save the data into the given path.

        Args:
            to_save: The data to save. The data should be compatible
                with the saving engine.
            path: The path where to save the data.
            exist_ok: If ``exist_ok`` is ``False`` (the default),
                an exception is raised if the target path already
                exists.

        Example:
            ```pycon
            >>> import tempfile
            >>> from pathlib import Path
            >>> from iden.io import JsonSaver, JsonLoader
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            ...     path = Path(tmpdir).joinpath("data.json")
            ...     JsonSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
            ...     data = JsonLoader().load(path)
            ...     data
            ...
            {'key1': [1, 2, 3], 'key2': 'abc'}

            ```
        """


class BaseFileSaver(BaseSaver[T]):
    r"""Define the base class to implement a file saver.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import JsonSaver, JsonLoader
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("data.json")
        ...     JsonSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
        ...     data = JsonLoader().load(path)
        ...     data
        ...
        {'key1': [1, 2, 3], 'key2': 'abc'}

        ```
    """

    def save(self, to_save: T, path: Path, *, exist_ok: bool = False) -> None:
        r"""Save the data into the given path.

        Args:
            to_save: The data to save. The data should be compatible
                with the saving engine.
            path: The path where to save the data.
            exist_ok: If ``exist_ok`` is ``False`` (the default),
                ``FileExistsError`` is raised if the target file
                already exists. If ``exist_ok`` is ``True``,
                ``FileExistsError`` will not be raised unless the
                given path already exists in the file system and is
                not a file.

        Raises:
            FileExistsError: if the file already exists.

        Example:
            ```pycon
            >>> import tempfile
            >>> from pathlib import Path
            >>> from iden.io import JsonSaver, JsonLoader
            >>> with tempfile.TemporaryDirectory() as tmpdir:
            ...     path = Path(tmpdir).joinpath("data.json")
            ...     JsonSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
            ...     data = JsonLoader().load(path)
            ...     data
            ...
            {'key1': [1, 2, 3], 'key2': 'abc'}

            ```
        """
        if path.is_dir():
            msg = f"path ({path}) is a directory"
            raise IsADirectoryError(msg)
        if path.is_file() and not exist_ok:
            msg = f"path ({path}) already exists. Use `exist_ok=True` to overwrite the file"
            raise FileExistsError(msg)
        path.parent.mkdir(exist_ok=True, parents=True)

        # Save to tmp, then commit by moving the file in case the job gets
        # interrupted while writing the file
        tmp_path = generate_unique_tmp_path(path)
        self._save_file(to_save, tmp_path)
        tmp_path.rename(path)

    @abstractmethod
    def _save_file(self, to_save: T, path: Path) -> None:
        r"""Save the data into the given file.

        Args:
            to_save: The data to save. The data should be compatible
                with the saving engine.
            path: The path where to save the data.
        """


def is_loader_config(config: dict[Any, Any]) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseLoader``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseLoader`` object.

    Example:
        ```pycon
        >>> from iden.io import is_loader_config
        >>> is_loader_config({"_target_": "iden.io.JsonLoader"})
        True

        ```
    """
    return is_object_config(config, BaseLoader)


def is_saver_config(config: dict[Any, Any]) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseSaver``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration for a
            ``BaseSaver`` object.

    Example:
        ```pycon
        >>> from iden.io import is_saver_config
        >>> is_saver_config({"_target_": "iden.io.JsonSaver"})
        True

        ```
    """
    return is_object_config(config, BaseSaver)


def setup_loader(loader: BaseLoader[T] | dict[Any, Any]) -> BaseLoader[T]:
    r"""Set up a data loader.

    The data loader is instantiated from its configuration by using the
    ``BaseLoader`` factory function.

    Args:
        loader: The data loader or its configuration.

    Returns:
        The instantiated data loader.

    Example:
        ```pycon
        >>> from iden.io import setup_loader
        >>> loader = setup_loader({"_target_": "iden.io.JsonLoader"})
        >>> loader
        JsonLoader()

        ```
    """
    if isinstance(loader, dict):
        logger.debug("Initializing a data loader from its configuration...")
        loader = BaseLoader.factory(**loader)
    if not isinstance(loader, BaseLoader):
        logger.warning(f"data loader is not a BaseLoader (received: {type(loader)})")
    return loader


def setup_saver(saver: BaseSaver[T] | dict[Any, Any]) -> BaseSaver[T]:
    r"""Set up a data saver.

    The data saver is instantiated from its configuration by using the
    ``BaseSaver`` factory function.

    Args:
        saver: The data saver or its configuration.

    Returns:
        The instantiated data saver.

    Example:
        ```pycon
        >>> from iden.io import setup_saver
        >>> saver = setup_saver({"_target_": "iden.io.JsonSaver"})
        >>> saver
        JsonSaver()

        ```
    """
    if isinstance(saver, dict):
        logger.debug("Initializing a data saver from its configuration...")
        saver = BaseSaver.factory(**saver)
    if not isinstance(saver, BaseSaver):
        logger.warning(f"data saver is not a BaseSaver (received: {type(saver)})")
    return saver


if not EqualityTester.has_comparator(BaseLoader):  # pragma: no cover
    EqualityTester.add_comparator(BaseLoader, ObjectEqualityComparator())
if not EqualityTester.has_comparator(BaseSaver):  # pragma: no cover
    EqualityTester.add_comparator(BaseSaver, ObjectEqualityComparator())
