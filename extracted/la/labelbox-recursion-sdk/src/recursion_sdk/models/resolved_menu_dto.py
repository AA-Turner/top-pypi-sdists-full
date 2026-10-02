from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.resolved_menu_dto_selection_mode import ResolvedMenuDtoSelectionMode
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.resolved_menu_dto_entries_item import ResolvedMenuDtoEntriesItem
  from ..models.resolved_menu_dto_properties_effective_selection_platform_default import ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault
  from ..models.resolved_menu_dto_properties_effective_selection_versioned import ResolvedMenuDtoPropertiesEffectiveSelectionVersioned
  from ..models.resolved_menu_dto_slot import ResolvedMenuDtoSlot





T = TypeVar("T", bound="ResolvedMenuDto")



@_attrs_define
class ResolvedMenuDto:
    """ The curated, reachability-filtered menu for one slot — the picker pre-selects the starred set per selectionMode.

        Example:
            {'slot': {'environmentId': '784e2386-e297-4f9d-a886-838422383b65', 'role': 'solver'}, 'entries': [{'entryId':
                '11111111-1111-4111-8111-111111111111', 'runConfigId': '22222222-2222-4222-8222-222222222222',
                'runConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'name': 'claude-sonnet-baseline', 'versionNumber':
                1, 'type': 'agent-harness', 'isDefault': True, 'sortOrder': 0, 'reachable': True}], 'defaultEntryId':
                '11111111-1111-4111-8111-111111111111', 'selectionMode': 'flexible'}

        Attributes:
            slot (ResolvedMenuDtoSlot): An environment + role binding point for a curated run-config menu.
            entries (list[ResolvedMenuDtoEntriesItem]): Reachable entries for the slot, sorted by sortOrder then creation.
            default_entry_id (None | UUID): The first starred entry to pre-select, or the first reachable entry as a
                fallback when all starred entries are unreachable, or null when the slot has no reachable entries.
            selection_mode (ResolvedMenuDtoSelectionMode): How the starred set governs a run: flexible pre-checks the
                starred set but lets a labeler pick a subset or other offered entries; locked forces exactly the starred set
                with no deviation.
            effective_selection (ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault |
                ResolvedMenuDtoPropertiesEffectiveSelectionVersioned | Unset): Identity that would resolve at launch when no
                explicit menu version is submitted.
     """

    slot: ResolvedMenuDtoSlot
    entries: list[ResolvedMenuDtoEntriesItem]
    default_entry_id: None | UUID
    selection_mode: ResolvedMenuDtoSelectionMode
    effective_selection: ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault | ResolvedMenuDtoPropertiesEffectiveSelectionVersioned | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.resolved_menu_dto_entries_item import ResolvedMenuDtoEntriesItem # noqa: PLC0415
        from ..models.resolved_menu_dto_properties_effective_selection_platform_default import ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault # noqa: PLC0415
        from ..models.resolved_menu_dto_properties_effective_selection_versioned import ResolvedMenuDtoPropertiesEffectiveSelectionVersioned # noqa: PLC0415
        from ..models.resolved_menu_dto_slot import ResolvedMenuDtoSlot # noqa: PLC0415
        slot = self.slot.to_dict()

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)



        default_entry_id: None | str
        if isinstance(self.default_entry_id, UUID):
            default_entry_id = str(self.default_entry_id)
        else:
            default_entry_id = self.default_entry_id

        selection_mode = self.selection_mode.value

        effective_selection: dict[str, Any] | Unset
        if isinstance(self.effective_selection, Unset):
            effective_selection = UNSET
        elif isinstance(self.effective_selection, ResolvedMenuDtoPropertiesEffectiveSelectionVersioned):
            effective_selection = self.effective_selection.to_dict()
        else:
            effective_selection = self.effective_selection.to_dict()



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "slot": slot,
            "entries": entries,
            "defaultEntryId": default_entry_id,
            "selectionMode": selection_mode,
        })
        if effective_selection is not UNSET:
            field_dict["effectiveSelection"] = effective_selection

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_menu_dto_entries_item import ResolvedMenuDtoEntriesItem # noqa: PLC0415
        from ..models.resolved_menu_dto_properties_effective_selection_platform_default import ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault # noqa: PLC0415
        from ..models.resolved_menu_dto_properties_effective_selection_versioned import ResolvedMenuDtoPropertiesEffectiveSelectionVersioned # noqa: PLC0415
        from ..models.resolved_menu_dto_slot import ResolvedMenuDtoSlot # noqa: PLC0415
        d = dict(src_dict)
        slot = ResolvedMenuDtoSlot.from_dict(d.pop("slot"))




        entries = []
        _entries = d.pop("entries")
        for entries_item_data in (_entries):
            entries_item = ResolvedMenuDtoEntriesItem.from_dict(entries_item_data)



            entries.append(entries_item)


        def _parse_default_entry_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                default_entry_id_type_0 = UUID(data)



                return default_entry_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        default_entry_id = _parse_default_entry_id(d.pop("defaultEntryId"))


        selection_mode = ResolvedMenuDtoSelectionMode(d.pop("selectionMode"))




        def _parse_effective_selection(data: object) -> ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault | ResolvedMenuDtoPropertiesEffectiveSelectionVersioned | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                effective_selection_type_0 = ResolvedMenuDtoPropertiesEffectiveSelectionVersioned.from_dict(data)



                return effective_selection_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            effective_selection_type_1 = ResolvedMenuDtoPropertiesEffectiveSelectionPlatformDefault.from_dict(data)



            return effective_selection_type_1

        effective_selection = _parse_effective_selection(d.pop("effectiveSelection", UNSET))


        resolved_menu_dto = cls(
            slot=slot,
            entries=entries,
            default_entry_id=default_entry_id,
            selection_mode=selection_mode,
            effective_selection=effective_selection,
        )

        return resolved_menu_dto

