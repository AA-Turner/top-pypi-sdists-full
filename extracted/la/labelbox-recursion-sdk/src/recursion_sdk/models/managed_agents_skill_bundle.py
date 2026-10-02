from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_skill_bundle_entry import ManagedAgentsSkillBundleEntry





T = TypeVar("T", bound="ManagedAgentsSkillBundle")



@_attrs_define
class ManagedAgentsSkillBundle:
    """ The files bundled with one skill version, stored as a single canonical archive and extracted into the session
    sandbox so the agent can read references and run scripts.

        Example:
            {'bytes': 1, 'entries': [{'bytes': 1, 'mode': 1, 'path': 'example', 'sha256': 'example'}], 'sha256': 'example'}

        Attributes:
            bytes_ (int): Compressed size of the archive in bytes, which is what mounting this skill into a session costs to
                transfer.
            sha256 (str): SHA-256 of the canonical archive, which is also its content address. Two uploads of identical
                files share one stored object.
            entries (list[ManagedAgentsSkillBundleEntry] | Unset): Every file in the bundle, sorted by path.
     """

    bytes_: int
    sha256: str
    entries: list[ManagedAgentsSkillBundleEntry] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_skill_bundle_entry import ManagedAgentsSkillBundleEntry # noqa: PLC0415
        bytes_ = self.bytes_

        sha256 = self.sha256

        entries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()
                entries.append(entries_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bytes": bytes_,
            "sha256": sha256,
        })
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_skill_bundle_entry import ManagedAgentsSkillBundleEntry # noqa: PLC0415
        d = dict(src_dict)
        bytes_ = d.pop("bytes")

        sha256 = d.pop("sha256")

        _entries = d.pop("entries", UNSET)
        entries: list[ManagedAgentsSkillBundleEntry] | Unset = UNSET
        if _entries is not UNSET:
            entries = []
            for entries_item_data in _entries:
                entries_item = ManagedAgentsSkillBundleEntry.from_dict(entries_item_data)



                entries.append(entries_item)


        managed_agents_skill_bundle = cls(
            bytes_=bytes_,
            sha256=sha256,
            entries=entries,
        )


        managed_agents_skill_bundle.additional_properties = d
        return managed_agents_skill_bundle

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
