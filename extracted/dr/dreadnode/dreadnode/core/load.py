"""Unified resource loading via URI schemes."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Literal, overload

if TYPE_CHECKING:
    from dreadnode.agents import Agent
    from dreadnode.app.config import Profile
    from dreadnode.datasets import Dataset, LocalDataset
    from dreadnode.models import LocalModel, Model
    from dreadnode.storage.storage import Storage


# URI pattern: scheme://path or just path (scheme can include hyphens)
URI_PATTERN = re.compile(r"^(?P<scheme>[a-z][a-z0-9-]*)://(?P<path>.+)$")


@overload
def load(
    uri: str,
    *,
    type: Literal["dataset"],
    storage: Storage | None = None,
    **kwargs: Any,
) -> Dataset | LocalDataset: ...


@overload
def load(
    uri: str,
    *,
    type: Literal["agent"],
    **kwargs: Any,
) -> Agent: ...


@overload
def load(
    uri: str,
    *,
    type: Literal["model"],
    storage: Storage | None = None,
    **kwargs: Any,
) -> Model | LocalModel: ...


@overload
def load(
    uri: str,
    *,
    type: None = None,
    storage: Storage | None = None,
    **kwargs: Any,
) -> Dataset | LocalDataset | Agent | Model | LocalModel | Any: ...


def load(
    uri: str,
    *,
    type: Literal["dataset", "agent", "model"] | None = None,
    storage: Storage | None = None,
    profile: Profile | None = None,
    **kwargs: Any,
) -> Any:
    """Load a resource by URI.

    Supports multiple URI schemes for loading different resource types:

    - `dataset://name` - Load a published dataset artifact
    - `dataset://name@version` - Load specific version
    - `model://name` - Load a published model artifact
    - `hf://path` - Load dataset from HuggingFace Hub
    - `hf-model://path` - Load model from HuggingFace Hub
    - `agent://name` - Load a published agent package
    - Plain path without scheme - Treated as HuggingFace dataset path

    Args:
        uri: Resource URI (e.g., "dataset://my-data", "hf://squad").
        type: Explicit type hint (optional, inferred from scheme).
        storage: Storage instance for local resources.
        profile: Active profile with API credentials.
        **kwargs: Additional arguments passed to the loader.

    Returns:
        The loaded resource (Dataset, LocalDataset, Model, LocalModel, Agent, etc.)

    Example:
        >>> import dreadnode as dn
        >>>
        >>> # Load a published dataset package
        >>> ds = dn.load("dataset://my-org/sentiment-data")
        >>>
        >>> # Load dataset from HuggingFace Hub
        >>> ds = dn.load("hf://squad", split="train[:100]")
        >>>
        >>> # Load model from HuggingFace Hub
        >>> model = dn.load("hf-model://bert-base-uncased")
        >>>
        >>> # Load a published model package
        >>> model = dn.load("model://my-org/classifier")
        >>>
        >>> # Load an agent package
        >>> agent = dn.load("agent://my-org/agent")
        >>>
        >>> # Plain path defaults to HuggingFace dataset
        >>> ds = dn.load("imdb", split="train")
    """
    match = URI_PATTERN.match(uri)

    if match:
        scheme = match.group("scheme")
        path = match.group("path")
    else:
        # No scheme - default based on type hint or assume HuggingFace
        scheme = type or "hf"
        path = uri

    # Parse version from path (e.g., "name@1.0.0")
    version = None
    if "@" in path:
        path, version = path.rsplit("@", 1)

    # Dispatch to appropriate loader
    if scheme == "dataset":
        return _load_dataset_package(path, version=version, profile=profile, storage=storage)
    if scheme == "hf":
        return _load_hf_dataset(path, storage=storage, **kwargs)
    if scheme == "model":
        return _load_model_package(path, version=version, profile=profile, storage=storage)
    if scheme in ("hf-model", "huggingface-model"):
        return _load_hf_model(path, storage=storage, **kwargs)
    if scheme == "agent":
        return _load_agent_package(path, version=version, **kwargs)
    raise ValueError(f"Unknown URI scheme: {scheme}")


def _load_dataset_package(
    name: str,
    version: str | None = None,
    profile: Profile | None = None,
    storage: Storage | None = None,
) -> Dataset:
    """Load a published dataset artifact from local storage.

    Raises:
        KeyError: If the dataset manifest is not available locally.
    """
    from dreadnode.datasets.dataset import Dataset

    if "/" in name:
        org, pkg_name = name.split("/", 1)
    else:
        if profile is None:
            raise RuntimeError(
                "No organization specified and no active profile. "
                "Either use 'org/package-name' format or call dn.configure() first."
            )
        org = profile.organization
        pkg_name = name

    manifest_name = f"{org}/{pkg_name}"

    try:
        return Dataset(manifest_name, storage=storage, version=version)
    except FileNotFoundError:
        version_hint = f"@{version}" if version else ""
        raise KeyError(
            f"Dataset artifact '{name}' is not available locally. "
            f"Install it first with: dn.pull_package(['dataset://{org}/{pkg_name}{version_hint}'])"
        ) from None


def _load_hf_dataset(
    path: str,
    storage: Storage | None = None,
    name: str | None = None,
    **kwargs: Any,
) -> LocalDataset:
    """Load a dataset from HuggingFace Hub."""
    from dreadnode.datasets.local import load_dataset

    return load_dataset(path, storage=storage, dataset_name=name, **kwargs)


def _load_agent_package(
    name: str,
    version: str | None = None,
    **kwargs: Any,
) -> Agent:
    """Load a published agent package.

    The package must be installed first using dn.pull_package().

    Raises:
        KeyError: If the package is not installed.
    """
    from dreadnode.agents.loader import AgentPackage

    # Parse org/name for error message
    if "/" in name:
        org, pkg_name = name.split("/", 1)
    else:
        org, pkg_name = name.split(".", 1) if "." in name else (None, name)

    try:
        pkg = AgentPackage(name)
        return pkg.load(**kwargs)
    except KeyError:
        version_hint = f"@{version}" if version else ""
        if org:
            raise KeyError(
                f"Agent package '{name}' is not installed. "
                f"Install it first with: dn.pull_package(['agent://{org}/{pkg_name}{version_hint}'])"
            ) from None
        raise KeyError(
            f"Agent package '{name}' is not installed. "
            f"Install it first with: dn.pull_package(['agent://<org>/{pkg_name}{version_hint}'])"
        ) from None


def _load_model_package(
    name: str,
    version: str | None = None,
    profile: Profile | None = None,
    storage: Storage | None = None,
) -> Model:
    """Load a published model artifact from local storage.

    Raises:
        KeyError: If the model manifest is not available locally.
    """
    from dreadnode.models.model import Model

    if "/" in name:
        org, pkg_name = name.split("/", 1)
    else:
        if profile is None:
            raise RuntimeError(
                "No organization specified and no active profile. "
                "Either use 'org/package-name' format or call dn.configure() first."
            )
        org = profile.organization
        pkg_name = name

    manifest_name = f"{org}/{pkg_name}"

    try:
        return Model(manifest_name, storage=storage, version=version)
    except FileNotFoundError:
        version_hint = f"@{version}" if version else ""
        raise KeyError(
            f"Model artifact '{name}' is not available locally. "
            f"Install it first with: dn.pull_package(['model://{org}/{pkg_name}{version_hint}'])"
        ) from None


def _load_hf_model(
    path: str,
    storage: Storage | None = None,
    name: str | None = None,
    **kwargs: Any,
) -> LocalModel:
    """Load a model from HuggingFace Hub."""
    from dreadnode.models.local import load_model

    return load_model(path, storage=storage, model_name=name, **kwargs)
