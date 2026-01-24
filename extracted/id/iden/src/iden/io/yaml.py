r"""Contain YAML-based data loaders and savers."""

from __future__ import annotations

__all__ = ["YamlLoader", "YamlSaver", "load_yaml", "save_yaml"]

from pathlib import Path
from typing import Any, TypeVar

from iden.io.base import BaseFileSaver, BaseLoader
from iden.utils.imports import check_yaml, is_yaml_available

if is_yaml_available():
    import yaml
else:  # pragma: no cover
    from iden.utils.fallback.yaml import yaml


T = TypeVar("T")


class YamlLoader(BaseLoader[T]):
    r"""Implement a data loader to load data in a YAML file.

    Example:
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

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def load(self, path: Path) -> T:
        with Path.open(path, mode="rb") as file:
            return yaml.safe_load(file)


class YamlSaver(BaseFileSaver[T]):
    r"""Implement a file saver to save data with a YAML file.

    Example:
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

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:  # noqa: ARG002
        return type(other) is type(self)

    def _save_file(self, to_save: T, path: Path) -> None:
        with Path.open(path, mode="w") as file:
            yaml.dump(to_save, file, Dumper=yaml.Dumper)


def load_yaml(path: Path) -> Any:
    r"""Load the data from a given YAML file.

    Args:
        path: The path to the YAML file.

    Returns:
        The data from the YAML file.

    Example:
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
        to_save: The data to write in a YAML file.
        path: The path where to write the YAML file.
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
