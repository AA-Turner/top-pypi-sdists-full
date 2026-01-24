from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from importlib.util import (
    find_spec,
)

from . import (
    _utils,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class FullPathModule:
    """Represents a full path module that exist."""

    _inner: _Private = field(repr=False, hash=False, compare=False)
    module: str

    @staticmethod
    def from_raw(raw: str) -> FullPathModule | Exception:
        try:
            module = find_spec(raw)
            if module is not None:
                return FullPathModule(_Private(), raw)
            return ModuleNotFoundError(raw)
        except ValueError as err:
            return err

    @classmethod
    def assert_module(cls, raw: str) -> FullPathModule:
        result = cls.from_raw(raw)
        return _utils.raise_or_value(result)

    @property
    def name(self) -> str:
        return self.module.split(".")[-1]

    @property
    def parent(self) -> FullPathModule | None:
        parent = ".".join(self.module.split(".")[:-1])
        result = self.from_raw(parent)
        if isinstance(result, Exception):
            return None
        return result

    def new_child(self, module: str) -> FullPathModule | None:
        joined = ".".join([self.module, module])
        result = self.from_raw(joined)
        if isinstance(result, Exception):
            return None
        return result

    def assert_child(self, module: str) -> FullPathModule | Exception:
        result = self.new_child(module)
        if result:
            return result
        return ModuleNotFoundError(f"Children of {self} i.e. {module}")

    def is_descendant_of(self, module: FullPathModule) -> bool:
        if self != module:
            return self.module.startswith(module.module)
        return False

    def __repr__(self) -> str:
        return self.module
