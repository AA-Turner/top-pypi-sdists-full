from dataclasses import dataclass, field
from typing import Generic, TypeAlias, TypeVar

from ...provider.loc_stack_filtering import LocStack
from ...type_tools.fwd_ref import FwdRef
from .schema_model import BaseJSONSchema

T = TypeVar("T")

JSONSchemaT = TypeVar("JSONSchemaT")


@dataclass(frozen=True)
class LocalRefSource(Generic[JSONSchemaT]):
    value: str | None
    json_schema: JSONSchemaT = field(hash=False)
    loc_stack: LocStack = field(repr=False)


@dataclass(frozen=True)
class RemoteRef:
    value: str


Boolable: TypeAlias = T | bool


@dataclass(repr=False)
class JSONSchema(
    BaseJSONSchema[
        LocalRefSource[FwdRef["JSONSchema"]] | RemoteRef,
        Boolable[FwdRef["JSONSchema"]],
    ],
):
    pass


@dataclass(repr=False)
class ResolvedJSONSchema(
    BaseJSONSchema[
        str,
        Boolable[FwdRef["ResolvedJSONSchema"]],
    ],
):
    pass

