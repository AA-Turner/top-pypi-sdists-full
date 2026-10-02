from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FetchBillingExportRequestRequest")


@_attrs_define
class FetchBillingExportRequestRequest:
    """
    Attributes:
        period_from (str): YYYY-MM format
        period_to (str): YYYY-MM format
        classification (Union[Unset, str]):
    """

    period_from: str
    period_to: str
    classification: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_from = self.period_from

        period_to = self.period_to

        classification = self.classification

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_from": period_from,
                "period_to": period_to,
            }
        )
        if classification is not UNSET:
            field_dict["classification"] = classification

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period_from = d.pop("period_from")

        period_to = d.pop("period_to")

        classification = d.pop("classification", UNSET)

        fetch_billing_export_request_request = cls(
            period_from=period_from,
            period_to=period_to,
            classification=classification,
        )

        fetch_billing_export_request_request.additional_properties = d
        return fetch_billing_export_request_request

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
