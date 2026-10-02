from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RmqClientProperties")


@_attrs_define
class RmqClientProperties:
    """
    Attributes:
        product (Union[None, str]): Client product name (e.g., 'pika', 'amqp-client')
        version (Union[None, str]): Client library version
        platform (Union[None, str]): Client platform (e.g., 'Python 3.12')
    """

    product: Union[None, str]
    version: Union[None, str]
    platform: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        product: Union[None, str]
        product = self.product

        version: Union[None, str]
        version = self.version

        platform: Union[None, str]
        platform = self.platform

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "product": product,
                "version": version,
                "platform": platform,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_product(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        product = _parse_product(d.pop("product"))

        def _parse_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        version = _parse_version(d.pop("version"))

        def _parse_platform(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        platform = _parse_platform(d.pop("platform"))

        rmq_client_properties = cls(
            product=product,
            version=version,
            platform=platform,
        )

        rmq_client_properties.additional_properties = d
        return rmq_client_properties

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
