import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.policy_type_enum import PolicyTypeEnum
from ..models.rbac_policy_direction_enum import RbacPolicyDirectionEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NetworkRBACPolicy")


@_attrs_define
class NetworkRBACPolicy:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        network (Union[Unset, str]):
        network_name (Union[Unset, str]):
        source_tenant_uuid (Union[Unset, UUID]):
        source_tenant_name (Union[Unset, str]):
        target_tenant (Union[Unset, str]):
        target_tenant_name (Union[Unset, str]):
        target_label (Union[Unset, str]):
        direction (Union[Unset, RbacPolicyDirectionEnum]):
        backend_id (Union[Unset, str]):
        policy_type (Union[Unset, PolicyTypeEnum]):  Default: PolicyTypeEnum.ACCESS_AS_SHARED.
        created (Union[Unset, datetime.datetime]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    network: Union[Unset, str] = UNSET
    network_name: Union[Unset, str] = UNSET
    source_tenant_uuid: Union[Unset, UUID] = UNSET
    source_tenant_name: Union[Unset, str] = UNSET
    target_tenant: Union[Unset, str] = UNSET
    target_tenant_name: Union[Unset, str] = UNSET
    target_label: Union[Unset, str] = UNSET
    direction: Union[Unset, RbacPolicyDirectionEnum] = UNSET
    backend_id: Union[Unset, str] = UNSET
    policy_type: Union[Unset, PolicyTypeEnum] = PolicyTypeEnum.ACCESS_AS_SHARED
    created: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        network = self.network

        network_name = self.network_name

        source_tenant_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.source_tenant_uuid, Unset):
            source_tenant_uuid = str(self.source_tenant_uuid)

        source_tenant_name = self.source_tenant_name

        target_tenant = self.target_tenant

        target_tenant_name = self.target_tenant_name

        target_label = self.target_label

        direction: Union[Unset, str] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value

        backend_id = self.backend_id

        policy_type: Union[Unset, str] = UNSET
        if not isinstance(self.policy_type, Unset):
            policy_type = self.policy_type.value

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if network is not UNSET:
            field_dict["network"] = network
        if network_name is not UNSET:
            field_dict["network_name"] = network_name
        if source_tenant_uuid is not UNSET:
            field_dict["source_tenant_uuid"] = source_tenant_uuid
        if source_tenant_name is not UNSET:
            field_dict["source_tenant_name"] = source_tenant_name
        if target_tenant is not UNSET:
            field_dict["target_tenant"] = target_tenant
        if target_tenant_name is not UNSET:
            field_dict["target_tenant_name"] = target_tenant_name
        if target_label is not UNSET:
            field_dict["target_label"] = target_label
        if direction is not UNSET:
            field_dict["direction"] = direction
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if policy_type is not UNSET:
            field_dict["policy_type"] = policy_type
        if created is not UNSET:
            field_dict["created"] = created

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        network = d.pop("network", UNSET)

        network_name = d.pop("network_name", UNSET)

        _source_tenant_uuid = d.pop("source_tenant_uuid", UNSET)
        source_tenant_uuid: Union[Unset, UUID]
        if isinstance(_source_tenant_uuid, Unset):
            source_tenant_uuid = UNSET
        else:
            source_tenant_uuid = UUID(_source_tenant_uuid)

        source_tenant_name = d.pop("source_tenant_name", UNSET)

        target_tenant = d.pop("target_tenant", UNSET)

        target_tenant_name = d.pop("target_tenant_name", UNSET)

        target_label = d.pop("target_label", UNSET)

        _direction = d.pop("direction", UNSET)
        direction: Union[Unset, RbacPolicyDirectionEnum]
        if isinstance(_direction, Unset):
            direction = UNSET
        else:
            direction = RbacPolicyDirectionEnum(_direction)

        backend_id = d.pop("backend_id", UNSET)

        _policy_type = d.pop("policy_type", UNSET)
        policy_type: Union[Unset, PolicyTypeEnum]
        if isinstance(_policy_type, Unset):
            policy_type = UNSET
        else:
            policy_type = PolicyTypeEnum(_policy_type)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        network_rbac_policy = cls(
            url=url,
            uuid=uuid,
            network=network,
            network_name=network_name,
            source_tenant_uuid=source_tenant_uuid,
            source_tenant_name=source_tenant_name,
            target_tenant=target_tenant,
            target_tenant_name=target_tenant_name,
            target_label=target_label,
            direction=direction,
            backend_id=backend_id,
            policy_type=policy_type,
            created=created,
        )

        network_rbac_policy.additional_properties = d
        return network_rbac_policy

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
