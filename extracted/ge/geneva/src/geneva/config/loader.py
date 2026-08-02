# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
# loader for config files

import abc
import bisect
import json
import os
from collections.abc import Callable
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar, cast

import attrs
import toml
import yaml
from typing_extensions import Self

from geneva.config.base import KV

# avoid circular import
if TYPE_CHECKING:
    from geneva.config import ConfigBase


class ConfigResolver(KV):
    @abc.abstractmethod
    def has_key(self, key: list[str]) -> bool:
        """
        If the current key path is valid in the resolver
        """


@attrs.define
class KVDictResolver(ConfigResolver):
    data: dict[str, str] = attrs.field(factory=dict)

    sorted_keys: list[str] = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.sorted_keys = sorted(self.data.keys())

    def __getitem__(self, key: list[str]) -> str:
        return self.data[".".join(key)]

    def __contains__(self, key: list[str]) -> bool:
        return ".".join(key) in self.data

    def has_key(self, key: list[str]) -> bool:
        flat_key = ".".join(key)
        i = bisect.bisect_left(self.sorted_keys, flat_key)
        if i >= len(self.sorted_keys):
            return False
        return self.sorted_keys[i].startswith(flat_key)


@attrs.define
class EnvVarResolver(ConfigResolver):
    """Resolve config values from environment variables.

    Uses '__' (double underscore) as separator between config section and field.
    For example, config section 'geneva_admission' with field 'check' becomes
    'GENEVA_ADMISSION__CHECK'.
    """

    def __getitem__(self, key: list[str]) -> str:
        env_key = "__".join(k.upper() for k in key)
        return os.environ[env_key]

    def __contains__(self, key: list[str]) -> bool:
        env_key = "__".join(k.upper() for k in key)
        return env_key in os.environ

    def has_key(self, key: list[str]) -> bool:
        env_prefix = "__".join(k.upper() for k in key)
        return any(k.startswith(env_prefix) for k in os.environ)


@attrs.define
class NestedDictResolver(ConfigResolver):
    data: dict = attrs.field(factory=dict)

    def __getitem__(self, key: list[str]) -> str:
        current = self.data
        for k in key:
            current = current[k]
        return cast("str", current)

    def __contains__(self, key: list[str]) -> bool:
        current = self.data
        for k in key:
            if k not in current:
                return False
            current = current[k]

        return isinstance(current, str)

    def has_key(self, key: list[str]) -> bool:
        current = self.data
        for k in key:
            if k not in current:
                return False
            current = current[k]
        return True


@attrs.define
class LasyLoader(ConfigResolver):
    loader_fn: Callable[[], ConfigResolver] = attrs.field()

    loader: ConfigResolver = attrs.field(init=False)

    def _load(self) -> None:
        if not hasattr(self, "loader"):
            self.loader = self.loader_fn()

    def __getitem__(self, key: list[str]) -> str:
        self._load()
        return self.loader[key]

    def __contains__(self, key: list[str]) -> bool:
        self._load()
        return key in self.loader

    def has_key(self, key: list[str]) -> bool:
        self._load()
        return self.loader.has_key(key)


@attrs.define
class ChainResolver(ConfigResolver):
    resolvers: list[ConfigResolver] = attrs.field(factory=list, converter=list)

    def __getitem__(self, key: list[str]) -> str:
        for resolver in self.resolvers:
            if key in resolver:
                return resolver[key]
        raise KeyError(key)

    def __contains__(self, key: list[str]) -> bool:
        return any(key in resolver for resolver in self.resolvers)

    def has_key(self, key: list[str]) -> bool:
        return any(resolver.has_key(key) for resolver in self.resolvers)

    def push_front(self, resolver: ConfigResolver) -> None:
        self.resolvers.insert(0, resolver)

    def push_back(self, resolver: ConfigResolver) -> None:
        self.resolvers.append(resolver)


_EMPTY_RESOLVER = NestedDictResolver(data={})


def chain(*resolvers: ConfigResolver) -> ChainResolver:
    return ChainResolver(resolvers=resolvers)


def from_file(file_path: Path) -> ConfigResolver:
    extension = file_path.name.split(".")[-1]
    parser = {
        "json": json.loads,
        "yaml": lambda x: yaml.full_load(StringIO(x)),
        "yml": lambda x: yaml.full_load(StringIO(x)),
        "toml": toml.loads,
    }

    def load() -> NestedDictResolver:
        with file_path.open() as f:
            return NestedDictResolver(data=parser[extension](f.read()))

    return LasyLoader(load)


def from_env() -> ConfigResolver:
    return EnvVarResolver()


def from_dict(data: dict) -> ConfigResolver:
    return NestedDictResolver(data=data)


def from_kv(data: dict[str, str]) -> ConfigResolver:
    return KVDictResolver(data=data)


def from_pyproject() -> ConfigResolver:
    path = Path(".").resolve().absolute()
    while path != Path("/"):
        if (path / "pyproject.toml").exists():
            with open(path / "pyproject.toml") as f:
                return from_dict(toml.loads(f.read()).get("geneva", {}))
        path = path.parent

    return _EMPTY_RESOLVER


# =============================================================================
# Type Converters for attrs fields
# =============================================================================
def str_to_bool(value: bool | str) -> bool:
    """Convert string to bool, handling common env var values.

    Use as a converter in attrs fields for ConfigBase subclasses:

        check: bool = attrs.field(default=True, converter=str_to_bool)

    Handles: "true", "false", "1", "0", "yes", "no", "" (empty = False)
    """
    if isinstance(value, bool):
        return value
    return str(value).lower() not in ("false", "0", "no", "")


T = TypeVar("T")

ConfigType = TypeVar("ConfigType", bound="ConfigBase")


@attrs.define
class ConfigLoader:
    resolver: ConfigResolver = attrs.field()

    key_chain: list[str] = attrs.field(factory=list)

    def __getitem__(self, key) -> Self | str:
        new_key = self.key_chain.copy() + [key]
        if new_key in self.resolver:
            return self.resolver[new_key]
        elif key in self:
            return ConfigLoader(self.resolver, new_key)  # type: ignore[return-value]
        else:
            raise KeyError(new_key)

    def get(self, key: str, default: T) -> Self | str | T:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: str) -> bool:
        return self.resolver.has_key(self.key_chain + [key])

    def load(self, cls: type[ConfigType]) -> ConfigType:
        return cls.from_loader(self)


def loader(resolver: ConfigResolver) -> ConfigLoader:
    return ConfigLoader(resolver=resolver, key_chain=[])
