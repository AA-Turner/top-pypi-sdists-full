r"""Contain torch-based data loaders and savers."""

from __future__ import annotations

__all__ = ["TorchLoader", "TorchSaver", "load_torch", "save_torch", "get_loader_mapping"]

from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

from coola.utils import check_torch, is_torch_available

from iden.io.base import BaseFileSaver, BaseLoader

if is_torch_available():
    import torch
else:  # pragma: no cover
    torch = Mock()

if TYPE_CHECKING:
    from pathlib import Path


class TorchLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data in a JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_torch, TorchLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pt")
    ...     save_torch({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = TorchLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __init__(self) -> None:
        check_torch()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, path: Path) -> Any:
        return torch.load(path)


class TorchSaver(BaseFileSaver[Any]):
    r"""Implement a file saver to save data with a JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import TorchSaver, TorchLoader
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pt")
    ...     TorchSaver().save({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = TorchLoader().load(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """

    def __init__(self) -> None:
        check_torch()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def _save_file(self, to_save: Any, path: Path) -> None:
        torch.save(to_save, path)


def load_torch(path: Path) -> Any:
    r"""Load the data from a given JSON file.

    Args:
        path: Specifies the path to the JSON file.

    Returns:
        The data from the JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.io import save_torch, load_torch
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pt")
    ...     save_torch({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_torch(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    return TorchLoader().load(path)


def save_torch(to_save: Any, path: Path, *, exist_ok: bool = False) -> None:
    r"""Save the given data in a JSON file.

    Args:
        to_save: Specifies the data to write in a JSON file.
        path: Specifies the path where to write the JSON file.
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
    >>> from iden.io import save_torch, load_torch
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     path = Path(tmpdir).joinpath("data.pt")
    ...     save_torch({"key1": [1, 2, 3], "key2": "abc"}, path)
    ...     data = load_torch(path)
    ...     data
    ...
    {'key1': [1, 2, 3], 'key2': 'abc'}

    ```
    """
    TorchSaver().save(to_save, path, exist_ok=exist_ok)


def get_loader_mapping() -> dict[str, BaseLoader]:
    r"""Get a default mapping between the file extensions and loaders.

    Returns:
        The mapping between the file extensions and loaders.

    Example usage:

    ```pycon
    >>> from iden.io.torch import get_loader_mapping
    >>> get_loader_mapping()
    {'pt': TorchLoader()}

    ```
    """
    if not is_torch_available():
        return {}
    return {"pt": TorchLoader()}
