from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.posix_sharing_offering import PosixSharingOffering


T = TypeVar("T", bound="UserPosixIdentity")


@_attrs_define
class UserPosixIdentity:
    """
    Attributes:
        namespace (str):
        value (int):
        context (Union[None, str]):
        pool_uuid (Union[None, str]):
        pool_scope (Union[None, str]):
        offerings (list['PosixSharingOffering']):
        offering_name (Union[None, str]): Deprecated: the first entry of 'offerings'. The endpoint used to return one
            row per offering; read 'offerings' instead.
        offering_uuid (Union[None, str]): Deprecated: the first entry of 'offerings'. Read 'offerings' instead.
    """

    namespace: str
    value: int
    context: Union[None, str]
    pool_uuid: Union[None, str]
    pool_scope: Union[None, str]
    offerings: list["PosixSharingOffering"]
    offering_name: Union[None, str]
    offering_uuid: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        namespace = self.namespace

        value = self.value

        context: Union[None, str]
        context = self.context

        pool_uuid: Union[None, str]
        pool_uuid = self.pool_uuid

        pool_scope: Union[None, str]
        pool_scope = self.pool_scope

        offerings = []
        for offerings_item_data in self.offerings:
            offerings_item = offerings_item_data.to_dict()
            offerings.append(offerings_item)

        offering_name: Union[None, str]
        offering_name = self.offering_name

        offering_uuid: Union[None, str]
        offering_uuid = self.offering_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace": namespace,
                "value": value,
                "context": context,
                "pool_uuid": pool_uuid,
                "pool_scope": pool_scope,
                "offerings": offerings,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.posix_sharing_offering import PosixSharingOffering

        d = dict(src_dict)
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

        def _parse_pool_scope(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pool_scope = _parse_pool_scope(d.pop("pool_scope"))

        offerings = []
        _offerings = d.pop("offerings")
        for offerings_item_data in _offerings:
            offerings_item = PosixSharingOffering.from_dict(offerings_item_data)

            offerings.append(offerings_item)

        def _parse_offering_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_name = _parse_offering_name(d.pop("offering_name"))

        def _parse_offering_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_uuid = _parse_offering_uuid(d.pop("offering_uuid"))

        user_posix_identity = cls(
            namespace=namespace,
            value=value,
            context=context,
            pool_uuid=pool_uuid,
            pool_scope=pool_scope,
            offerings=offerings,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
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
