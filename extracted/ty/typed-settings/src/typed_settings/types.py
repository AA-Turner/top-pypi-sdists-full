"""
Internal data structures.
"""

import dataclasses
from collections.abc import Collection
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Literal,
    NamedTuple,
    NewType,
    Optional,
    Protocol,
    TypeVar,
    Union,
)

from ._compat import PY_310
from .constants import SECRET_REPR


if TYPE_CHECKING:
    from typing_extensions import TypeGuard

__all__ = [
    "AUTO",
    "ET",
    "SECRETS_TYPES",
    "SECRET_REPR",
    "ST",
    "CollectionChildOptions",
    "LoadedSettings",
    "LoadedValue",
    "LoaderMeta",
    "MergedSettings",
    "OptionDict",
    "OptionInfo",
    "OptionList",
    "OptionName",
    "OptionPath",
    "Secret",
    "SecretStr",
    "SettingsClass",
    "SettingsDict",
    "SettingsInstance",
    "T",
    "is_new_type",
]


#: A generic TypeVar
T = TypeVar("T")
#: A TypeVar for :class:`~enum.Enum` types
ET = TypeVar("ET", bound=Enum)  # Enum type
#: A TypeVar for settings instances
ST = TypeVar("ST")  # Type var for SettingsInstance

SettingsClass = type
SettingsInstance = Any
OptionName = str
OptionPath = str
SettingsDict = dict[OptionName, Union[Any, "SettingsDict"]]
"""
A dictionary with all loaded settings.

Values are not converted to their final type yet.
"""


class _Auto:
    """
    Sentinel class to indicate the lack of a value when ``None`` is ambiguous.

    ``_Auto`` is a singleton. There is only ever one of it.
    """

    _singleton = None

    def __new__(cls) -> "_Auto":
        if _Auto._singleton is None:
            _Auto._singleton = super().__new__(cls)
        return _Auto._singleton

    def __repr__(self) -> str:
        return "AUTO"


AUTO = _Auto()
"""
Sentinel to indicate the lack of a value when ``None`` is ambiguous.
"""


def _type2name(value: Union[str, Any]) -> str:
    """
    Return either *value* if it is a str or else its type name.
    """
    if isinstance(value, str):
        return value
    return type(value).__name__


@dataclasses.dataclass(frozen=True)
class OptionInfo:
    """
    Information about (possibly nested) option attributes.

    Each instance represents a single attribute of an apps's settings class.
    """

    #: The option's settings class.  This is either the root settings class or a nested
    #: one.
    parent_cls: type

    #: Dotted path to the option name relative to the root settings class.
    path: OptionPath

    #: The option's name (last component of :attr:`path`)
    name: str = dataclasses.field(init=False)

    #: The option's type
    cls: type

    #: the option's default value
    default: Any

    #: Whether or not the option has a default value.
    has_no_default: bool

    #: Whether or not the default value is a factory function.
    default_is_factory: bool

    #: Whether or not the option is a secret.
    is_secret: bool = False

    #: An optional explicit converter for the option value
    converter: Optional[Callable[[Any], Any]] = None

    #: Additional metadata.
    metadata: dict[Any, Any] = dataclasses.field(default_factory=dict)

    #: Options for child elements in case *cls* is a collection (sequence or mapping).
    collection_child_options: Optional["CollectionChildOptions"] = None

    @property
    def has_default(self) -> bool:
        """
        Opposite of :attr:`has_no_default`.
        """
        return not self.has_no_default

    def __post_init__(self) -> None:
        _prefix, _, name = self.path.rpartition(".")
        object.__setattr__(self, "name", name)


OptionList = tuple[OptionInfo, ...]
"""
A flat list of all available options, including those from nested settings.
"""


@dataclasses.dataclass(frozen=True)
class CollectionChildOptions:
    """
    *Options* for child elements of *collection*.
    """

    options: OptionList
    collection: Literal["mapping", "sequence"]


OptionDict = MappingProxyType[OptionPath, OptionInfo]
"""
A dict version of :class:`OptionList`.
"""


class LoaderMeta:
    """
    Meta data about the loader that loaded a set of option values.

    That data is used to improve error reporting and for converting loaded values to the
    target type.
    """

    def __init__(self, name: Union[str, Any], base_dir: Optional[Path] = None):
        self._name: str = _type2name(name)
        self._base_dir = base_dir or Path.cwd()

    def __str__(self) -> str:
        return f"{type(self).__name__}({self._name!r}, {self.base_dir!r})"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.base_dir == other.base_dir
        )

    @property
    def name(self) -> str:
        """
        The loader's name.  Can be a string or the loader class itself (it's class name
        is will then be used).
        """
        return self._name

    @property
    def base_dir(self) -> Path:
        """
        The loader's base directory.

        It is used to resolve relative paths in loaded option values in the proper
        context.

        For most loaders, this should be the *cwd* (which is also the default).  For
        file loaders, the parent directory of a loaded file might be a better
        alternative.
        """
        return self._base_dir


class LoadedValue(NamedTuple):
    """
    A container for a loaded option value and the meta data of the originating loader.
    """

    value: Any
    """
    The loaded option value.
    """

    loader_meta: LoaderMeta
    """
    Meta data of the loader that loaded the corresponding value.
    """


@dataclasses.dataclass(frozen=True)
class LoadedSettings:
    """
    A container for the settings loaded by a single loader, and the meta data of that
    loader.
    """

    settings: SettingsDict
    """
    The loaded settings values.
    """

    meta: LoaderMeta
    """
    Meta data of the loader that loaded the settings.
    """


MergedSettings = dict[OptionPath, LoadedValue]
"""
A dict that maps a dotted option path to a loaded option value.

The values may come from different loaders, so each option values stores the meta data
of it's loader.
"""


class SecretStr(str):
    """
    A subclass of :class:`str` that masks the output of :func:`repr()`.

    It is less secure than :class:`Secret` but is a drop-in replacement for normal
    strings.

    The main use case is avoiding accidental secrets leakage via tracebacks.
    It also helps to enforce secret usage via Typing.

    It does **not help** when you:

    - :func:`print()` it
    - :class:`str` it
    - Log it
    - Use it in an f-string (``f"{val}"``)

    .. versionadded:: 2.0.0
    """

    def __repr__(self) -> str:
        """
        Return a secret representation if a non-empty value is set, else a repr for an
        empty string.
        """
        return f"{SECRET_REPR!r}" if self else "''"


class Secret(Generic[T]):
    """
    A secret wrapper around any value.

    It makes it very hard to accidentally leak the secret, even when printing or logging
    it.

    You need to explicitly call :meth:`get_secret_value()` to get the wrapped value.
    Thus, it is no drop-in replacement for the wrapped data.

    See :class:`SecretStr` if you need a drop-in replacement for strings, even if it is
    not quite as safe.

    You can use :class:`bool` to get the boolean value of the wrapped secret.  Other
    protocol methods (e.g., for length or comparison operators) are not implemented.

    .. versionadded:: 2.0.0
    """

    def __init__(self, secret_value: T) -> None:
        self._is_collection = isinstance(secret_value, Collection)
        self._secret_value = secret_value

    def __bool__(self) -> bool:
        """
        Return the boolean representation of the stored secret.
        """
        return bool(self._secret_value)

    def __repr__(self) -> str:
        """
        Return a secret representation if a non-empty value is set, else a repr for an
        empty string.
        """
        r = repr(
            self._secret_value
            if not self._secret_value and self._is_collection
            else SECRET_REPR
        )
        return f"{self.__class__.__name__}({r})"

    def __str__(self) -> str:
        """
        Return a secret representation if a non-empty value is set, else an empty
        string.
        """
        return str(
            self._secret_value
            if not self._secret_value and self._is_collection
            else SECRET_REPR
        )

    def get_secret_value(self) -> T:
        """
        Return the wrapped secret value.
        """
        return self._secret_value


class SecretRepr:
    def __call__(self, v: Any) -> str:
        return repr(v if not v and isinstance(v, Collection) else SECRET_REPR)

    def __repr__(self) -> str:
        return "***"


class NewTypeLike(Protocol):
    __supertype__: type


def is_new_type(obj: Any) -> "TypeGuard[NewTypeLike]":
    """
    Return ``True`` if *obj* is a :class:`~typing.NewType`.
    """
    if PY_310:
        return isinstance(obj, NewType)
    else:
        return hasattr(obj, "__supertype__") and isinstance(obj.__supertype__, type)


SECRETS_TYPES = (Secret, SecretStr)
"""
Types that mask the repr of their values.
"""
