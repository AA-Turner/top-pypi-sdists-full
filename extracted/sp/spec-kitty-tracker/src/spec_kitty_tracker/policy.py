from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class OwnershipMode(StrEnum):
    EXTERNAL_AUTHORITATIVE = "external_authoritative"
    SPLIT_OWNERSHIP = "split_ownership"
    SPEC_KITTY_AUTHORITATIVE = "spec_kitty_authoritative"


class FieldOwner(StrEnum):
    EXTERNAL = "external"
    LOCAL = "local"
    SHARED = "shared"


CORE_ISSUE_FIELDS: tuple[str, ...] = (
    "title",
    "body",
    "status",
    "issue_type",
    "priority",
    "assignees",
    "labels",
    "parent",
    "links",
    "custom_fields",
)


@dataclass(frozen=True, slots=True)
class OwnershipPolicy:
    mode: OwnershipMode
    split_field_owners: Mapping[str, FieldOwner] = field(default_factory=dict)
    default_split_owner: FieldOwner = FieldOwner.SHARED

    def owner_for(self, field_name: str) -> FieldOwner:
        if self.mode is OwnershipMode.EXTERNAL_AUTHORITATIVE:
            return FieldOwner.EXTERNAL
        if self.mode is OwnershipMode.SPEC_KITTY_AUTHORITATIVE:
            return FieldOwner.LOCAL
        return self.split_field_owners.get(field_name, self.default_split_owner)

    def local_can_write(self, field_name: str) -> bool:
        owner = self.owner_for(field_name)
        return owner in (FieldOwner.LOCAL, FieldOwner.SHARED)

    def external_can_write(self, field_name: str) -> bool:
        owner = self.owner_for(field_name)
        return owner in (FieldOwner.EXTERNAL, FieldOwner.SHARED)

    @classmethod
    def external_authoritative(cls) -> OwnershipPolicy:
        return cls(mode=OwnershipMode.EXTERNAL_AUTHORITATIVE)

    @classmethod
    def local_authoritative(cls) -> OwnershipPolicy:
        return cls(mode=OwnershipMode.SPEC_KITTY_AUTHORITATIVE)

    @classmethod
    def split(
        cls,
        *,
        field_owners: Mapping[str, FieldOwner],
        default_owner: FieldOwner = FieldOwner.SHARED,
    ) -> OwnershipPolicy:
        return cls(
            mode=OwnershipMode.SPLIT_OWNERSHIP,
            split_field_owners=dict(field_owners),
            default_split_owner=default_owner,
        )
