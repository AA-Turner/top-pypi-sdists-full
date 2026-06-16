import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateDraftJsonBody")


@_attrs_define
class UpdateDraftJsonBody:
    """
    Attributes:
        value (Union[Unset, Any]): Draft content to save. `null` (or omitted) signals a delete — the row is removed
            under the same conflict rules.
        last_sync (Union[Unset, datetime.datetime]): Server timestamp of the client's last known sync for this draft.
            Omit on first save.
        force (Union[Unset, bool]): Skip the conflict check and overwrite the server copy.
        legacy (Union[Unset, bool]): Delete-only. Target the legacy workspace-level row (email NULL) instead of the
            current user's row. Used to discard a legacy draft from the review page.
    """

    value: Union[Unset, Any] = UNSET
    last_sync: Union[Unset, datetime.datetime] = UNSET
    force: Union[Unset, bool] = UNSET
    legacy: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        last_sync: Union[Unset, str] = UNSET
        if not isinstance(self.last_sync, Unset):
            last_sync = self.last_sync.isoformat()

        force = self.force
        legacy = self.legacy

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if last_sync is not UNSET:
            field_dict["last_sync"] = last_sync
        if force is not UNSET:
            field_dict["force"] = force
        if legacy is not UNSET:
            field_dict["legacy"] = legacy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        _last_sync = d.pop("last_sync", UNSET)
        last_sync: Union[Unset, datetime.datetime]
        if isinstance(_last_sync, Unset):
            last_sync = UNSET
        else:
            last_sync = isoparse(_last_sync)

        force = d.pop("force", UNSET)

        legacy = d.pop("legacy", UNSET)

        update_draft_json_body = cls(
            value=value,
            last_sync=last_sync,
            force=force,
            legacy=legacy,
        )

        update_draft_json_body.additional_properties = d
        return update_draft_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
