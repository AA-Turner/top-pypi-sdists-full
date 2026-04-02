from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fetch_billing_export_response_data_item import FetchBillingExportResponseDataItem


T = TypeVar("T", bound="FetchBillingExportResponse")


@_attrs_define
class FetchBillingExportResponse:
    """
    Attributes:
        period_from (str):
        period_to (str):
        classification (str):
        row_count (int):
        data (list['FetchBillingExportResponseDataItem']):
    """

    period_from: str
    period_to: str
    classification: str
    row_count: int
    data: list["FetchBillingExportResponseDataItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_from = self.period_from

        period_to = self.period_to

        classification = self.classification

        row_count = self.row_count

        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_from": period_from,
                "period_to": period_to,
                "classification": classification,
                "row_count": row_count,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fetch_billing_export_response_data_item import FetchBillingExportResponseDataItem

        d = dict(src_dict)
        period_from = d.pop("period_from")

        period_to = d.pop("period_to")

        classification = d.pop("classification")

        row_count = d.pop("row_count")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = FetchBillingExportResponseDataItem.from_dict(data_item_data)

            data.append(data_item)

        fetch_billing_export_response = cls(
            period_from=period_from,
            period_to=period_to,
            classification=classification,
            row_count=row_count,
            data=data,
        )

        fetch_billing_export_response.additional_properties = d
        return fetch_billing_export_response

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
