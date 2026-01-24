r"""Define the public interface to load data."""

from __future__ import annotations

__all__ = ["get_default_loader_registry", "load", "register_loaders"]

from typing import TYPE_CHECKING, Any

from coola.utils.imports import is_torch_available

from iden.io.joblib import JoblibLoader
from iden.io.json import JsonLoader
from iden.io.pickle import PickleLoader
from iden.io.registry import LoaderRegistry
from iden.io.text import TextLoader
from iden.io.torch import TorchLoader
from iden.io.yaml import YamlLoader
from iden.utils.imports import is_joblib_available, is_yaml_available

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from iden.io import BaseLoader


def load(path: Path, registry: LoaderRegistry | None = None) -> Any:
    r"""Load the data from the given path.

    Args:
        path: The path with the data to load.
        registry: Registry to load data. If ``None``, uses the default
            global registry.

    Returns:
        The data

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json, load
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("data.json")
        ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
        ...     data = load(path)
        ...     data
        ...
        {'key1': [1, 2, 3], 'key2': 'abc'}

        ```
    """
    if registry is None:
        registry = get_default_loader_registry()
    return registry.load(path)


def register_loaders(mapping: Mapping[str, BaseLoader[Any]], exist_ok: bool = False) -> None:
    r"""Register custom loaders to the default global registry.

    This allows users to add support for custom file extensions without
    modifying global state directly.

    Args:
        mapping: Dictionary mapping file extensions to loader instances
        exist_ok: If ``False``, raises error if any extension is already
            registered. Defaults to ``False``.

    Example:
        ```pycon
        >>> from iden.io import register_loaders, TextLoader
        >>> register_loaders({"longtext": TextLoader()})

        ```
    """
    get_default_loader_registry().register_many(mapping, exist_ok=exist_ok)


def get_default_loader_registry() -> LoaderRegistry:
    r"""Get or create the default global registry.

    Returns:
        A LoaderRegistry instance with default loaders registered for
        common file formats (json, pkl, pickle, txt, yaml, yml, and
        optionally joblib and pt if their dependencies are available).

    Notes:
        The singleton pattern means modifications to the returned registry
        affect all future calls to this function. An isolated registry can
        be created by instantiating a new LoaderRegistry directly.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io import save_json, get_default_loader_registry
        >>> registry = get_default_loader_registry()
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = Path(tmpdir).joinpath("data.json")
        ...     save_json({"key1": [1, 2, 3], "key2": "abc"}, path)
        ...     data = registry.load(path)
        ...     data
        ...
        {'key1': [1, 2, 3], 'key2': 'abc'}

        ```
    """
    if not hasattr(get_default_loader_registry, "_registry"):
        registry = LoaderRegistry()
        _register_default_loaders(registry)
        get_default_loader_registry._registry = registry
    return get_default_loader_registry._registry


def _register_default_loaders(registry: LoaderRegistry) -> None:
    r"""Register default loaders for common file formats.

    Args:
        registry: The registry to populate with default loaders

    Notes:
        This function is called internally by get_default_loader_registry() and should
        not typically be called directly by users.
    """
    pickle_loader = PickleLoader()

    loaders: dict[str, BaseLoader[Any]] = {
        "json": JsonLoader(),
        "pkl": pickle_loader,
        "pickle": pickle_loader,
        "txt": TextLoader(),
    }
    if is_joblib_available():
        loaders["joblib"] = JoblibLoader()
    if is_torch_available():
        loaders["pt"] = TorchLoader()
    if is_yaml_available():
        yaml_loader = YamlLoader()
        loaders["yaml"] = yaml_loader
        loaders["yml"] = yaml_loader
    registry.register_many(loaders)
