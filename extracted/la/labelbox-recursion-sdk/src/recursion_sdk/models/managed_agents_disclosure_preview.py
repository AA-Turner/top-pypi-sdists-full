from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_disclosure_entry import ManagedAgentsDisclosureEntry





T = TypeVar("T", bound="ManagedAgentsDisclosurePreview")



@_attrs_define
class ManagedAgentsDisclosurePreview:
    """ What a set of skill attachments costs the model's prompt on every turn, and which skills the budget has reduced to a
    bare name. A skill listed without its description is still activatable but is unlikely to be chosen, because the
    description is the only signal the model has for choosing it.

        Example:
            {'budget_chars': 1, 'entries': [{'description_included': True, 'name': 'example-name'}], 'used_chars': 1,
                'warnings': ['example']}

        Attributes:
            budget_chars (int): Characters of prompt this session's model allows tier-1 skill disclosure to spend each turn.
            entries (list[ManagedAgentsDisclosureEntry] | None): Every attached skill in disclosure order, and whether the
                model is told what it is for.
            used_chars (int): Characters the rendered catalog actually occupies. Measured from the same pass that produces
                the prompt, not estimated.
            warnings (list[str] | None): What resolving and rendering this set cost: unresolvable references, truncated
                descriptions, and skills reduced to a name.
     """

    budget_chars: int
    entries: list[ManagedAgentsDisclosureEntry] | None
    used_chars: int
    warnings: list[str] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_disclosure_entry import ManagedAgentsDisclosureEntry # noqa: PLC0415
        budget_chars = self.budget_chars

        entries: list[dict[str, Any]] | None
        if isinstance(self.entries, list):
            entries = []
            for entries_type_0_item_data in self.entries:
                entries_type_0_item = entries_type_0_item_data.to_dict()
                entries.append(entries_type_0_item)


        else:
            entries = self.entries

        used_chars = self.used_chars

        warnings: list[str] | None
        if isinstance(self.warnings, list):
            warnings = self.warnings


        else:
            warnings = self.warnings


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "budget_chars": budget_chars,
            "entries": entries,
            "used_chars": used_chars,
            "warnings": warnings,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_disclosure_entry import ManagedAgentsDisclosureEntry # noqa: PLC0415
        d = dict(src_dict)
        budget_chars = d.pop("budget_chars")

        def _parse_entries(data: object) -> list[ManagedAgentsDisclosureEntry] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entries_type_0 = []
                _entries_type_0 = data
                for entries_type_0_item_data in (_entries_type_0):
                    entries_type_0_item = ManagedAgentsDisclosureEntry.from_dict(entries_type_0_item_data)



                    entries_type_0.append(entries_type_0_item)

                return entries_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsDisclosureEntry] | None, data)

        entries = _parse_entries(d.pop("entries"))


        used_chars = d.pop("used_chars")

        def _parse_warnings(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                warnings_type_0 = cast(list[str], data)

                return warnings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        warnings = _parse_warnings(d.pop("warnings"))


        managed_agents_disclosure_preview = cls(
            budget_chars=budget_chars,
            entries=entries,
            used_chars=used_chars,
            warnings=warnings,
        )


        managed_agents_disclosure_preview.additional_properties = d
        return managed_agents_disclosure_preview

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
