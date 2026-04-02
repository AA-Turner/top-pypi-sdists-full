from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExportComponentDataRequest")


@_attrs_define
class ExportComponentDataRequest:
    """
    Attributes:
        type_ (str):
        name (str):
        description (str):
        billing_type (str):
        measured_unit (str):
        unit_factor (Union[None, float]):
        limit_period (Union[None, str]):
        limit_amount (Union[None, int]):
        article_code (str):
        backend_id (str):
    """

    type_: str
    name: str
    description: str
    billing_type: str
    measured_unit: str
    unit_factor: Union[None, float]
    limit_period: Union[None, str]
    limit_amount: Union[None, int]
    article_code: str
    backend_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        name = self.name

        description = self.description

        billing_type = self.billing_type

        measured_unit = self.measured_unit

        unit_factor: Union[None, float]
        unit_factor = self.unit_factor

        limit_period: Union[None, str]
        limit_period = self.limit_period

        limit_amount: Union[None, int]
        limit_amount = self.limit_amount

        article_code = self.article_code

        backend_id = self.backend_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "name": name,
                "description": description,
                "billing_type": billing_type,
                "measured_unit": measured_unit,
                "unit_factor": unit_factor,
                "limit_period": limit_period,
                "limit_amount": limit_amount,
                "article_code": article_code,
                "backend_id": backend_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        name = d.pop("name")

        description = d.pop("description")

        billing_type = d.pop("billing_type")

        measured_unit = d.pop("measured_unit")

        def _parse_unit_factor(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        unit_factor = _parse_unit_factor(d.pop("unit_factor"))

        def _parse_limit_period(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        limit_period = _parse_limit_period(d.pop("limit_period"))

        def _parse_limit_amount(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        limit_amount = _parse_limit_amount(d.pop("limit_amount"))

        article_code = d.pop("article_code")

        backend_id = d.pop("backend_id")

        export_component_data_request = cls(
            type_=type_,
            name=name,
            description=description,
            billing_type=billing_type,
            measured_unit=measured_unit,
            unit_factor=unit_factor,
            limit_period=limit_period,
            limit_amount=limit_amount,
            article_code=article_code,
            backend_id=backend_id,
        )

        export_component_data_request.additional_properties = d
        return export_component_data_request

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
