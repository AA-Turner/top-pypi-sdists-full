from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.changelog_flat_entry import ChangelogFlatEntry


T = TypeVar("T", bound="ChangelogEntryList")


@_attrs_define
class ChangelogEntryList:
    """
    Attributes:
        count (int):
        current_version (str):
        latest_version (str):
        versions_behind (int):
        results (list['ChangelogFlatEntry']):
    """

    count: int
    current_version: str
    latest_version: str
    versions_behind: int
    results: list["ChangelogFlatEntry"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        current_version = self.current_version

        latest_version = self.latest_version

        versions_behind = self.versions_behind

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "current_version": current_version,
                "latest_version": latest_version,
                "versions_behind": versions_behind,
                "results": results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.changelog_flat_entry import ChangelogFlatEntry

        d = dict(src_dict)
        count = d.pop("count")

        current_version = d.pop("current_version")

        latest_version = d.pop("latest_version")

        versions_behind = d.pop("versions_behind")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = ChangelogFlatEntry.from_dict(results_item_data)

            results.append(results_item)

        changelog_entry_list = cls(
            count=count,
            current_version=current_version,
            latest_version=latest_version,
            versions_behind=versions_behind,
            results=results,
        )

        changelog_entry_list.additional_properties = d
        return changelog_entry_list

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
