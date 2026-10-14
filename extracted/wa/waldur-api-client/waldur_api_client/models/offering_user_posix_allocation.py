from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.posix_sharing_offering import PosixSharingOffering


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
        shared_with_offerings (list['PosixSharingOffering']):
    """

    namespace: str
    value: int
    pool_uuid: Union[None, str]
    scope: Union[None, str]
    scope_name: Union[None, str]
    shared_with_offerings: list["PosixSharingOffering"]
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

        shared_with_offerings = []
        for shared_with_offerings_item_data in self.shared_with_offerings:
            shared_with_offerings_item = shared_with_offerings_item_data.to_dict()
            shared_with_offerings.append(shared_with_offerings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace": namespace,
                "value": value,
                "pool_uuid": pool_uuid,
                "scope": scope,
                "scope_name": scope_name,
                "shared_with_offerings": shared_with_offerings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.posix_sharing_offering import PosixSharingOffering

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

        shared_with_offerings = []
        _shared_with_offerings = d.pop("shared_with_offerings")
        for shared_with_offerings_item_data in _shared_with_offerings:
            shared_with_offerings_item = PosixSharingOffering.from_dict(shared_with_offerings_item_data)

            shared_with_offerings.append(shared_with_offerings_item)

        offering_user_posix_allocation = cls(
            namespace=namespace,
            value=value,
            pool_uuid=pool_uuid,
            scope=scope,
            scope_name=scope_name,
            shared_with_offerings=shared_with_offerings,
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
