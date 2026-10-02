from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UserPosixIdentity")


@_attrs_define
class UserPosixIdentity:
    """
    Attributes:
        offering_name (str):
        offering_uuid (str):
        namespace (str):
        value (int):
        context (Union[None, str]):
        pool_uuid (Union[None, str]):
    """

    offering_name: str
    offering_uuid: str
    namespace: str
    value: int
    context: Union[None, str]
    pool_uuid: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_name = self.offering_name

        offering_uuid = self.offering_uuid

        namespace = self.namespace

        value = self.value

        context: Union[None, str]
        context = self.context

        pool_uuid: Union[None, str]
        pool_uuid = self.pool_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "namespace": namespace,
                "value": value,
                "context": context,
                "pool_uuid": pool_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_name = d.pop("offering_name")

        offering_uuid = d.pop("offering_uuid")

        namespace = d.pop("namespace")

        value = d.pop("value")

        def _parse_context(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        context = _parse_context(d.pop("context"))

        def _parse_pool_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pool_uuid = _parse_pool_uuid(d.pop("pool_uuid"))

        user_posix_identity = cls(
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            namespace=namespace,
            value=value,
            context=context,
            pool_uuid=pool_uuid,
        )

        user_posix_identity.additional_properties = d
        return user_posix_identity

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
