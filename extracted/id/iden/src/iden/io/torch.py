r"""Contain torch-based data loaders and savers."""

from __future__ import annotations

__all__ = ["TorchLoader", "TorchSaver", "get_loader_mapping", "load_torch", "save_torch"]

from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

from coola import objects_are_equal
from coola.utils import check_torch, is_torch_available
from coola.utils.format import repr_mapping_line

from iden.io.base import BaseFileSaver, BaseLoader

if is_torch_available():
    import torch
else:  # pragma: no cover
    torch = Mock()

if TYPE_CHECKING:
    from pathlib import Path


class TorchLoader(BaseLoader[Any]):
    r"""Implement a data loader to load data in a PyTorch file.

    Args:
        **kwargs: Additional arguments passed to ``torch.load``.

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

    def __init__(self, **kwargs: Any) -> None:
        check_torch()
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({repr_mapping_line(self._kwargs)})"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(self._kwargs, other._kwargs, equal_nan=equal_nan)

    def load(self, path: Path) -> Any:
        return torch.load(path, **self._kwargs)


class TorchSaver(BaseFileSaver[Any]):
    r"""Implement a file saver to save data with a PyTorch file.

    Args:
        **kwargs: Additional arguments passed to ``torch.save``.

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

    def __init__(self, **kwargs: Any) -> None:
        check_torch()
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({repr_mapping_line(self._kwargs)})"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(self._kwargs, other._kwargs, equal_nan=equal_nan)

    def _save_file(self, to_save: Any, path: Path) -> None:
        torch.save(to_save, path, **self._kwargs)


def load_torch(path: Path, **kwargs: Any) -> Any:
    r"""Load the data from a given PyTorch file.

    Args:
        path: The path to the PyTorch file.
        **kwargs: Additional arguments passed to ``torch.load``.

    Returns:
        The data from the PyTorch file.

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
    return TorchLoader(**kwargs).load(path)


def save_torch(to_save: Any, path: Path, *, exist_ok: bool = False, **kwargs: Any) -> None:
    r"""Save the given data in a PyTorch file.

    Args:
        to_save: The data to write in a PyTorch file.
        path: The path where to write the PyTorch file.
        exist_ok: If ``exist_ok`` is ``False`` (the default),
            ``FileExistsError`` is raised if the target file
            already exists. If ``exist_ok`` is ``True``,
            ``FileExistsError`` will not be raised unless the
            given path already exists in the file system and is
            not a file.
        **kwargs: Additional arguments passed to ``torch.save``.

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
    TorchSaver(**kwargs).save(to_save, path, exist_ok=exist_ok)


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
