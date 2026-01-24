from __future__ import (
    annotations,
)

import re
from dataclasses import (
    dataclass,
    field,
)

from fa_purity import (
    Result,
    ResultE,
    cast_exception,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class GroupId:
    _private: _Private = field(repr=False, hash=False, compare=False)
    name: str

    @staticmethod
    def new(name: str) -> ResultE[GroupId]:
        _name = name.removeprefix("GROUP#")
        pattern = r"^[\w\s-]+$"
        if not re.match(pattern, _name):
            err = ValueError(rf"Group name is not `^[\w- ]+$` i.e. {_name}")
            return Result.failure(err, GroupId).alt(cast_exception)
        return Result.success(GroupId(_Private(), _name), Exception)


@dataclass(frozen=True)
class OrganizationId:
    _private: _Private = field(repr=False, hash=False, compare=False)
    name: str
    uuid: str

    @staticmethod
    def new(uuid: str, name: str) -> ResultE[OrganizationId]:
        _name = name.removeprefix("ORG#")
        _uuid = uuid.removeprefix("ORG#")
        if not _name.isalnum():
            err = ValueError(f"Org name is not alphanum i.e. {_name}")
            return Result.failure(err, OrganizationId).alt(cast_exception)
        uuidv4 = "^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$"
        if re.match(uuidv4, _uuid, re.IGNORECASE) is None:
            err = ValueError(f"Org id is not an UUIDv4 i.e. {_uuid}")
            return Result.failure(err, OrganizationId).alt(cast_exception)

        return Result.success(OrganizationId(_Private(), _name, _uuid), Exception)
