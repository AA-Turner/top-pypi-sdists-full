"""
Auto-generated typed classes for ConfigMeta classes.

This module provides IDE-friendly typed interfaces for all configuration classes.
The reason we auto-generate this file is because we want to provide a bridge between what is the ConfigMeta classes and the typed programmatic interface.
The CoreConfig class is setup in a way that if any additionally params are missed out from being auto-generated then it will not affect the core functionality of the programmatic API.
The new parameters will just not show up in IDE autocompletions.
It is fine if this file is not regularly updated by running the script in the .pre-commit-config.app-changes.yaml
but it is recommended that this file not be deleted or manually edited.

"""

from typing import Optional, List, Dict, Any
from .unified_config import CoreConfig

import sys
from typing import TYPE_CHECKING

# on 3.8+ use the stdlib TypedDict;
# in TYPE_CHECKING blocks mypy/pyright still pick it up on older Pythons
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    if TYPE_CHECKING:
        # for the benefit of type-checkers
        from typing import TypedDict  # noqa: F401
    # runtime no-op TypedDict shim
    class _TypedDictMeta(type):
        def __new__(cls, name, bases, namespace, total=True):
            # ignore total at runtime
            return super().__new__(cls, name, bases, namespace)

    class TypedDict(dict, metaclass=_TypedDictMeta):
        # Runtime stand-in for typing.TypedDict on <3.8.
        pass


class ResourceConfigDict(TypedDict, total=False):
    cpu: Optional[str]
    memory: Optional[str]
    gpu: Optional[str]
    disk: Optional[str]


class AuthConfigDict(TypedDict, total=False):
    type: Optional[str]
    public: Optional[bool]


class ReplicaConfigDict(TypedDict, total=False):
    fixed: Optional[int]
    min: Optional[int]
    max: Optional[int]


class DependencyConfigDict(TypedDict, total=False):
    from_requirements_file: Optional[str]
    from_pyproject_toml: Optional[str]
    python: Optional[str]
    pypi: Optional[dict]
    conda: Optional[dict]


class PackageConfigDict(TypedDict, total=False):
    src_path: Optional[str]
    suffixes: Optional[list]


class TypedCoreConfig:
    def __init__(
        self,
        name: Optional[str] = None,
        port: Optional[int] = None,
        description: Optional[str] = None,
        app_type: Optional[str] = None,
        image: Optional[str] = None,
        tags: Optional[list] = None,
        secrets: Optional[list] = None,
        compute_pools: Optional[list] = None,
        environment: Optional[dict] = None,
        commands: Optional[list] = None,
        resources: Optional[ResourceConfigDict] = None,
        auth: Optional[AuthConfigDict] = None,
        replicas: Optional[ReplicaConfigDict] = None,
        dependencies: Optional[DependencyConfigDict] = None,
        package: Optional[PackageConfigDict] = None,
        no_deps: Optional[bool] = None,
        force_upgrade: Optional[bool] = None,
        persistence: Optional[str] = None,
        project: Optional[str] = None,
        branch: Optional[str] = None,
        models: Optional[list] = None,
        data: Optional[list] = None,
        **kwargs
    ) -> None:
        self._kwargs = {
            "name": name,
            "port": port,
            "description": description,
            "app_type": app_type,
            "image": image,
            "tags": tags,
            "secrets": secrets,
            "compute_pools": compute_pools,
            "environment": environment,
            "commands": commands,
            "resources": resources,
            "auth": auth,
            "replicas": replicas,
            "dependencies": dependencies,
            "package": package,
            "no_deps": no_deps,
            "force_upgrade": force_upgrade,
            "persistence": persistence,
            "project": project,
            "branch": branch,
            "models": models,
            "data": data,
        }
        # Add any additional kwargs
        self._kwargs.update(kwargs)
        # Remove None values
        self._kwargs = {k: v for k, v in self._kwargs.items() if v is not None}
        self._config_class = CoreConfig
        self._config = self.create_config()

    def create_config(self) -> CoreConfig:
        return CoreConfig.from_dict(self._kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return self._config.to_dict()
