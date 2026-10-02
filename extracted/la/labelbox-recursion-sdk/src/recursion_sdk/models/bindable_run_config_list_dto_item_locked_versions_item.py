from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="BindableRunConfigListDtoItemLockedVersionsItem")



@_attrs_define
class BindableRunConfigListDtoItemLockedVersionsItem:
    """ Compact locked-version row for bindable-catalog selectors — enough to render version choices without the full
    version payload.

        Attributes:
            id (UUID): Stable identifier of the locked run-config version.
            version_number (int): Monotonic version number within the owning run-config identity.
            locked_at (datetime.datetime): Timestamp when the version was locked (ISO-8601, UTC).
     """

    id: UUID
    version_number: int
    locked_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        version_number = self.version_number

        locked_at = self.locked_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "versionNumber": version_number,
            "lockedAt": locked_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        version_number = d.pop("versionNumber")

        locked_at = datetime.datetime.fromisoformat(d.pop("lockedAt"))




        bindable_run_config_list_dto_item_locked_versions_item = cls(
            id=id,
            version_number=version_number,
            locked_at=locked_at,
        )

        return bindable_run_config_list_dto_item_locked_versions_item

