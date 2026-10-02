from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingUserPosixAllocation")


@_attrs_define
class OfferingUserPosixAllocation:
    """
    Attributes:
        namespace (str):
        value (int):
        pool_uuid (Union[None, str]):
        scope (Union[None, str]):
        scope_name (Union[None, str]):
    """

    namespace: str
    value: int
    pool_uuid: Union[None, str]
    scope: Union[None, str]
    scope_name: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        namespace = self.namespace

        value = self.value

        pool_uuid: Union[None, str]
        pool_uuid = self.pool_uuid

        scope: Union[None, str]
        scope = self.scope

        scope_name: Union[None, str]
        scope_name = self.scope_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace": namespace,
                "value": value,
                "pool_uuid": pool_uuid,
                "scope": scope,
                "scope_name": scope_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        namespace = d.pop("namespace")

        value = d.pop("value")

        def _parse_pool_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pool_uuid = _parse_pool_uuid(d.pop("pool_uuid"))

        def _parse_scope(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope = _parse_scope(d.pop("scope"))

        def _parse_scope_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_name = _parse_scope_name(d.pop("scope_name"))

        offering_user_posix_allocation = cls(
            namespace=namespace,
            value=value,
            pool_uuid=pool_uuid,
            scope=scope,
            scope_name=scope_name,
        )

        offering_user_posix_allocation.additional_properties = d
        return offering_user_posix_allocation

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
