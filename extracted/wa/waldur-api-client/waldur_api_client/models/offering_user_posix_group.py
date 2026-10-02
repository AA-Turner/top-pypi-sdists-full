from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingUserPosixGroup")


@_attrs_define
class OfferingUserPosixGroup:
    """
    Attributes:
        gid (int):
        offering_name (str):
        project_name (Union[None, str]):
        project_uuid (Union[None, str]):
        customer_name (Union[None, str]):
        customer_uuid (Union[None, str]):
        project_accessible (bool):
        pool_uuid (Union[None, str]):
    """

    gid: int
    offering_name: str
    project_name: Union[None, str]
    project_uuid: Union[None, str]
    customer_name: Union[None, str]
    customer_uuid: Union[None, str]
    project_accessible: bool
    pool_uuid: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gid = self.gid

        offering_name = self.offering_name

        project_name: Union[None, str]
        project_name = self.project_name

        project_uuid: Union[None, str]
        project_uuid = self.project_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        customer_uuid: Union[None, str]
        customer_uuid = self.customer_uuid

        project_accessible = self.project_accessible

        pool_uuid: Union[None, str]
        pool_uuid = self.pool_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gid": gid,
                "offering_name": offering_name,
                "project_name": project_name,
                "project_uuid": project_uuid,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "project_accessible": project_accessible,
                "pool_uuid": pool_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gid = d.pop("gid")

        offering_name = d.pop("offering_name")

        def _parse_project_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_name = _parse_project_name(d.pop("project_name"))

        def _parse_project_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        def _parse_customer_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        project_accessible = d.pop("project_accessible")

        def _parse_pool_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        pool_uuid = _parse_pool_uuid(d.pop("pool_uuid"))

        offering_user_posix_group = cls(
            gid=gid,
            offering_name=offering_name,
            project_name=project_name,
            project_uuid=project_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            project_accessible=project_accessible,
            pool_uuid=pool_uuid,
        )

        offering_user_posix_group.additional_properties = d
        return offering_user_posix_group

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
