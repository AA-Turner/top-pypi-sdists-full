import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.policy_type_enum import PolicyTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeprecatedNetworkRBACPolicy")


@_attrs_define
class DeprecatedNetworkRBACPolicy:
    """
    Attributes:
        url (str):
        uuid (UUID):
        network (str):
        network_name (str):
        target_tenant (str):
        target_tenant_name (str):
        backend_id (str):
        created (datetime.datetime):
        policy_type (Union[Unset, PolicyTypeEnum]):  Default: PolicyTypeEnum.ACCESS_AS_SHARED.
    """

    url: str
    uuid: UUID
    network: str
    network_name: str
    target_tenant: str
    target_tenant_name: str
    backend_id: str
    created: datetime.datetime
    policy_type: Union[Unset, PolicyTypeEnum] = PolicyTypeEnum.ACCESS_AS_SHARED
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        network = self.network

        network_name = self.network_name

        target_tenant = self.target_tenant

        target_tenant_name = self.target_tenant_name

        backend_id = self.backend_id

        created = self.created.isoformat()

        policy_type: Union[Unset, str] = UNSET
        if not isinstance(self.policy_type, Unset):
            policy_type = self.policy_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "network": network,
                "network_name": network_name,
                "target_tenant": target_tenant,
                "target_tenant_name": target_tenant_name,
                "backend_id": backend_id,
                "created": created,
            }
        )
        if policy_type is not UNSET:
            field_dict["policy_type"] = policy_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        network = d.pop("network")

        network_name = d.pop("network_name")

        target_tenant = d.pop("target_tenant")

        target_tenant_name = d.pop("target_tenant_name")

        backend_id = d.pop("backend_id")

        created = isoparse(d.pop("created"))

        _policy_type = d.pop("policy_type", UNSET)
        policy_type: Union[Unset, PolicyTypeEnum]
        if isinstance(_policy_type, Unset):
            policy_type = UNSET
        else:
            policy_type = PolicyTypeEnum(_policy_type)

        deprecated_network_rbac_policy = cls(
            url=url,
            uuid=uuid,
            network=network,
            network_name=network_name,
            target_tenant=target_tenant,
            target_tenant_name=target_tenant_name,
            backend_id=backend_id,
            created=created,
            policy_type=policy_type,
        )

        deprecated_network_rbac_policy.additional_properties = d
        return deprecated_network_rbac_policy

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
