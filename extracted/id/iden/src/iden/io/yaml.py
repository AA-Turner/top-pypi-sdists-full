r"""Contain YAML-based data loaders and savers."""

from __future__ import annotations

__all__ = ["YamlLoader", "YamlSaver", "load_yaml", "save_yaml", "get_loader_mapping"]

from pathlib import Path
from typing import Any, TypeVar
from unittest.mock import Mock

from iden.io.base import BaseFileSaver, BaseLoader
from iden.utils.imports import check_yaml, is_yaml_available

if is_yaml_available():
    import yaml
else:  # pragma: no cover
    yaml = Mock()


T = TypeVar("T")


class YamlLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data in a YAML file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_yaml, YamlLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.yaml")
    ...     save_yaml({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = YamlLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __init__(self) -> None:
        check_yaml()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, path: Path) -> Any:
        with Path.open(path, mode="rb") as file:
            return yaml.safe_load(file)


class YamlSaver(BaseFileSaver[Any]):
    r"""Implement a file saver to save data with a YAML file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import YamlSaver, YamlLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.yaml")
    ...     YamlSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = YamlLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __init__(self) -> None:
        check_yaml()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def _save_file(self, to_save: Any, path: Path) -> None:
        with Path.open(path, mode="w") as file:
            yaml.dump(to_save, file, Dumper=yaml.Dumper)


def load_yaml(path: Path) -> Any:
    r"""Load the data from a given YAML file.

    Args:
        path: Specifies the path to the YAML file.

    Returns:
        The data from the YAML file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import load_yaml, save_yaml
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.yaml")
    ...     save_yaml({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_yaml(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    return YamlLoader().load(path)


def save_yaml(to_save: Any, path: Path, *, exist_ok: bool = False) -> None:
    r"""Save the given data in a YAML file.

    Args:
        to_save: Specifies the data to write in a YAML file.
        path: Specifies the path where to write the YAML file.
        exist_ok: If ``exist_ok`` is ``False`` (the default),
            ``FileExistsError`` is raised if the target file
            already exists. If ``exist_ok`` is ``True``,
            ``FileExistsError`` will not be raised unless the
            given path already exists in the file system and is
            not a file.

    Raises:
        FileExistsError: if the file already exists.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import load_yaml, save_yaml
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.yaml")
    ...     save_yaml({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_yaml(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    YamlSaver().save(to_save, path, exist_ok=exist_ok)


def get_loader_mapping() -> dict[str, BaseLoader]:
    r"""Get a default mapping between the file extensions and loaders.

    Returns:
        The mapping between the file extensions and loaders.

    Example usage:

    ```pycon
    >>> from iden.io.yaml import get_loader_mapping
    >>> get_loader_mapping()
    {'yaml': YamlLoader(), 'yml': YamlLoader()}

    ```
    """
    if not is_yaml_available():
        return {}
    loader = YamlLoader()
    return {"yaml": loader, "yml": loader}
