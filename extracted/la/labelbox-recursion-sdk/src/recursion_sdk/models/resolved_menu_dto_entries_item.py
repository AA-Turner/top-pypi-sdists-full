from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_menu_dto_entries_item_type import ResolvedMenuDtoEntriesItemType
from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ResolvedMenuDtoEntriesItem")



@_attrs_define
class ResolvedMenuDtoEntriesItem:
    """ One render-ready choice in a resolved menu.

        Attributes:
            entry_id (UUID): Stable run-config menu-entry identifier (UUID). One curated choice (a run-config version) on a
                slot menu.
            run_config_id (UUID): Stable run-config identifier (UUID). Versioned reusable solver / grader / QA / synthesizer
                config.
            run_config_version_id (UUID): Stable run-config-version identifier (UUID). Points at one specific version of a
                run config.
            name (str): Display name of the run config this entry points at.
            version_number (int): Version number of the offered version.
            type_ (ResolvedMenuDtoEntriesItemType): Identity-level discriminator for a run config. The agent-harness type
                follows the standard draft, verified, locked lifecycle where a passing probe is recommended but not required
                before locking; the snapshot type is lockable without a probe and bindable to roles once locked.
            is_default (bool): Whether this entry is included by default (starred). Multiple entries may be starred; in the
                Run dialog the starred set is pre-selected (flexible) or the mandatory set (locked).
            sort_order (int): Display order within the slot menu; lower values appear first.
            reachable (bool | Unset): Whether this version is currently reachable for the slot. Omitted or true for picker
                menus; false when an admin list includes a stale entry.
     """

    entry_id: UUID
    run_config_id: UUID
    run_config_version_id: UUID
    name: str
    version_number: int
    type_: ResolvedMenuDtoEntriesItemType
    is_default: bool
    sort_order: int
    reachable: bool | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        entry_id = str(self.entry_id)

        run_config_id = str(self.run_config_id)

        run_config_version_id = str(self.run_config_version_id)

        name = self.name

        version_number = self.version_number

        type_ = self.type_.value

        is_default = self.is_default

        sort_order = self.sort_order

        reachable = self.reachable


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "entryId": entry_id,
            "runConfigId": run_config_id,
            "runConfigVersionId": run_config_version_id,
            "name": name,
            "versionNumber": version_number,
            "type": type_,
            "isDefault": is_default,
            "sortOrder": sort_order,
        })
        if reachable is not UNSET:
            field_dict["reachable"] = reachable

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entry_id = UUID(d.pop("entryId"))




        run_config_id = UUID(d.pop("runConfigId"))




        run_config_version_id = UUID(d.pop("runConfigVersionId"))




        name = d.pop("name")

        version_number = d.pop("versionNumber")

        type_ = ResolvedMenuDtoEntriesItemType(d.pop("type"))




        is_default = d.pop("isDefault")

        sort_order = d.pop("sortOrder")

        reachable = d.pop("reachable", UNSET)

        resolved_menu_dto_entries_item = cls(
            entry_id=entry_id,
            run_config_id=run_config_id,
            run_config_version_id=run_config_version_id,
            name=name,
            version_number=version_number,
            type_=type_,
            is_default=is_default,
            sort_order=sort_order,
            reachable=reachable,
        )

        return resolved_menu_dto_entries_item

