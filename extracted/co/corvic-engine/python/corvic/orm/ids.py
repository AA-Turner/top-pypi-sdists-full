"""Id containers for orm objects."""

from __future__ import annotations

import abc
from typing import Any, Generic, TypeVar

import sqlalchemy as sa
import sqlalchemy.types as sa_types
from typing_extensions import Self

import corvic.context
from corvic.orm.errors import InvalidORMIdentifierError
from corvic.result import Ok

ORMIdentifier = TypeVar("ORMIdentifier")


class BaseID(Generic[ORMIdentifier], abc.ABC):
    """Base class for all API object identifiers."""

    _value: str

    def __init__(self, value: str = ""):
        self._value = value

    @classmethod
    def from_str(cls, value: str):
        return cls(value)

    def to_json(self):
        return {"type": self.__class__.__name__, "value": self._value}

    def __str__(self):
        """Directly calling str() is the preferred method for converting to str."""
        return self._value

    def __repr__(self):
        return f"{type(self).__name__}({self._value})"

    def __bool__(self):
        """An ID is truthy if it's not empty."""
        return bool(self._value)

    def __eq__(self, other: object):
        """IDs are equal if they have the same specific type and their values match."""
        if isinstance(other, type(self)):
            return self._value == other._value
        return False

    def __hash__(self):
        """Hash value is exactly the hash of the string."""
        return hash(self._value)

    @abc.abstractmethod
    def to_db(self) -> Ok[ORMIdentifier] | InvalidORMIdentifierError:
        """Translate this identifier to its orm equivalent."""

    @classmethod
    @abc.abstractmethod
    def from_db(cls, orm_id: ORMIdentifier | None) -> Self:
        """Make an identifier from some orm identifier."""


class BaseIDFromInt(BaseID[int]):
    """Implementation of BaseID for the common case were orm ids are integers.

    Particularly when orm ids are selected from a sequence.
    """

    def to_db(self) -> Ok[int] | InvalidORMIdentifierError:
        if not self._value:
            return InvalidORMIdentifierError("id was empty")
        try:
            return Ok(int(self._value))
        except ValueError:
            return InvalidORMIdentifierError(
                "conversion to orm failed", id_value=self._value
            )

    def __lt__(self, other: BaseIDFromInt) -> bool:
        try:
            return int(self._value) < int(other._value)
        except ValueError:
            return self._value < other._value

    @classmethod
    def from_db(cls, orm_id: int | None):
        # Note that "0" is not a valid identifier in this scheme.
        # A feature rather than a bug since 0 is the same as
        # unspecified in protos, and database sequences for
        # generating sequential ids start at 1.
        return cls(str(orm_id or ""))


class BaseIDFromStr(BaseID[str]):
    """Implementation of BaseID for the case were orm ids are strings."""

    def to_db(self) -> Ok[str] | InvalidORMIdentifierError:
        if not self._value:
            return InvalidORMIdentifierError("id was empty")
        return Ok(self._value)

    @classmethod
    def from_db(cls, orm_id: str | None):
        return cls(orm_id or "")


class OrgID(BaseIDFromStr):
    """A unique identifier for an organization."""

    @property
    def is_super_user(self):
        return self._value == corvic.context.SUPERUSER_ORG_ID

    @property
    def is_nobody(self):
        return self._value == corvic.context.NOBODY_ORG_ID


class RoomID(BaseIDFromInt):
    """A unique identifier for a room."""


class ResourceID(BaseIDFromInt):
    """A unique identifier for a resource."""


class SourceID(BaseIDFromInt):
    """A unique identifier for a source."""


class FeatureViewID(BaseIDFromInt):
    """A unique identifier for a feature view."""


class FeatureViewSourceID(BaseIDFromInt):
    """A unique identifier for a source in a feature view."""


class SpaceID(BaseIDFromInt):
    """A unique identifier for a space."""


class SpaceRunID(BaseIDFromInt):
    """A unique identifier for a space run."""


class SpaceParametersID(BaseIDFromInt):
    """A unique identifier for a space parameters."""


class AgentID(BaseIDFromInt):
    """A unique identifier for a agent."""


class AgentMessageID(BaseIDFromInt):
    """A unique identifier for a agent message."""


class UserMessageID(BaseIDFromInt):
    """A unique identifier for a user message."""


class MessageEntryID(BaseIDFromInt):
    """A unique identifier for a message entry."""


_IntID = TypeVar("_IntID", bound=BaseIDFromInt)


class IntIDDecorator(sa.types.TypeDecorator[_IntID]):
    """Sqlalchemy type decorator for translating int backed id types."""

    # placeholder, overrode by load_dialect_impl
    impl = sa_types.TypeEngine[Any]
    cache_ok = True

    def __init__(self, instance: _IntID):
        super().__init__()
        self._instance = instance

    def load_dialect_impl(self, dialect: sa.Dialect) -> sa_types.TypeEngine[Any]:
        if dialect.name == "sqlite":
            return sa.INTEGER()
        return sa.BIGINT()

    def process_bind_param(
        self, value: _IntID | None, dialect: sa.Dialect
    ) -> int | None:
        if value is None:
            return None
        return value.to_db().unwrap_or_raise()

    def process_result_value(
        self, value: int | None, dialect: sa.Dialect
    ) -> _IntID | None:
        if value is None:
            return None
        return self._instance.from_db(value)


_StrID = TypeVar("_StrID", bound=BaseIDFromStr)


class StrIDDecorator(sa.types.TypeDecorator[_StrID]):
    """Sqlalchemy type decorator for translating string-backed id types."""

    impl = sa.String
    cache_ok = True

    def __init__(self, instance: _StrID):
        super().__init__()
        self._instance = instance

    def process_bind_param(
        self, value: _StrID | None, dialect: sa.Dialect
    ) -> str | None:
        if value is None:
            return None
        return value.to_db().unwrap_or_raise()

    def process_result_value(
        self, value: str | None, dialect: sa.Dialect
    ) -> _StrID | None:
        if value is None:
            return None
        return self._instance.from_db(value)
