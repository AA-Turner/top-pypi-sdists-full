from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.changelog_entry import ChangelogEntry
    from ..models.changelog_release_component_activity import ChangelogReleaseComponentActivity


T = TypeVar("T", bound="ChangelogRelease")


@_attrs_define
class ChangelogRelease:
    """
    Attributes:
        version (str):
        date (str):
        type_ (str):
        summary (str):
        entries (list['ChangelogEntry']):
        since_previous (Union[Unset, list['ChangelogEntry']]):
        component_activity (Union[Unset, ChangelogReleaseComponentActivity]):
    """

    version: str
    date: str
    type_: str
    summary: str
    entries: list["ChangelogEntry"]
    since_previous: Union[Unset, list["ChangelogEntry"]] = UNSET
    component_activity: Union[Unset, "ChangelogReleaseComponentActivity"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        version = self.version

        date = self.date

        type_ = self.type_

        summary = self.summary

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        since_previous: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.since_previous, Unset):
            since_previous = []
            for since_previous_item_data in self.since_previous:
                since_previous_item = since_previous_item_data.to_dict()
                since_previous.append(since_previous_item)

        component_activity: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.component_activity, Unset):
            component_activity = self.component_activity.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "date": date,
                "type": type_,
                "summary": summary,
                "entries": entries,
            }
        )
        if since_previous is not UNSET:
            field_dict["since_previous"] = since_previous
        if component_activity is not UNSET:
            field_dict["component_activity"] = component_activity

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.changelog_entry import ChangelogEntry
        from ..models.changelog_release_component_activity import ChangelogReleaseComponentActivity

        d = dict(src_dict)
        version = d.pop("version")

        date = d.pop("date")

        type_ = d.pop("type")

        summary = d.pop("summary")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = ChangelogEntry.from_dict(entries_item_data)

            entries.append(entries_item)

        since_previous = []
        _since_previous = d.pop("since_previous", UNSET)
        for since_previous_item_data in _since_previous or []:
            since_previous_item = ChangelogEntry.from_dict(since_previous_item_data)

            since_previous.append(since_previous_item)

        _component_activity = d.pop("component_activity", UNSET)
        component_activity: Union[Unset, ChangelogReleaseComponentActivity]
        if isinstance(_component_activity, Unset):
            component_activity = UNSET
        else:
            component_activity = ChangelogReleaseComponentActivity.from_dict(_component_activity)

        changelog_release = cls(
            version=version,
            date=date,
            type_=type_,
            summary=summary,
            entries=entries,
            since_previous=since_previous,
            component_activity=component_activity,
        )

        changelog_release.additional_properties = d
        return changelog_release

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
