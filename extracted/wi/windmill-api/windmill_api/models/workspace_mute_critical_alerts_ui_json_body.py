from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceMuteCriticalAlertsUIJsonBody")


@_attrs_define
class WorkspaceMuteCriticalAlertsUIJsonBody:
    """
    Attributes:
        mute_critical_alerts (Union[Unset, bool]): Whether critical alerts should be muted. Example: True.
    """

    mute_critical_alerts: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mute_critical_alerts = self.mute_critical_alerts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mute_critical_alerts is not UNSET:
            field_dict["mute_critical_alerts"] = mute_critical_alerts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mute_critical_alerts = d.pop("mute_critical_alerts", UNSET)

        workspace_mute_critical_alerts_ui_json_body = cls(
            mute_critical_alerts=mute_critical_alerts,
        )

        workspace_mute_critical_alerts_ui_json_body.additional_properties = d
        return workspace_mute_critical_alerts_ui_json_body

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
