import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetThresholdAlertResponse200")


@_attrs_define
class GetThresholdAlertResponse200:
    """
    Attributes:
        threshold_alert_amount (Union[Unset, float]):
        last_alert_sent (Union[Unset, datetime.datetime]):
    """

    threshold_alert_amount: Union[Unset, float] = UNSET
    last_alert_sent: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        threshold_alert_amount = self.threshold_alert_amount
        last_alert_sent: Union[Unset, str] = UNSET
        if not isinstance(self.last_alert_sent, Unset):
            last_alert_sent = self.last_alert_sent.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if threshold_alert_amount is not UNSET:
            field_dict["threshold_alert_amount"] = threshold_alert_amount
        if last_alert_sent is not UNSET:
            field_dict["last_alert_sent"] = last_alert_sent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        threshold_alert_amount = d.pop("threshold_alert_amount", UNSET)

        _last_alert_sent = d.pop("last_alert_sent", UNSET)
        last_alert_sent: Union[Unset, datetime.datetime]
        if isinstance(_last_alert_sent, Unset):
            last_alert_sent = UNSET
        else:
            last_alert_sent = isoparse(_last_alert_sent)

        get_threshold_alert_response_200 = cls(
            threshold_alert_amount=threshold_alert_amount,
            last_alert_sent=last_alert_sent,
        )

        get_threshold_alert_response_200.additional_properties = d
        return get_threshold_alert_response_200

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
