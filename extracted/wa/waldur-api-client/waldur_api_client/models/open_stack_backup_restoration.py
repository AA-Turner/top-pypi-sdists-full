import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_nested_floating_ip import OpenStackNestedFloatingIP
    from ..models.open_stack_nested_port import OpenStackNestedPort
    from ..models.open_stack_nested_security_group import OpenStackNestedSecurityGroup


T = TypeVar("T", bound="OpenStackBackupRestoration")


@_attrs_define
class OpenStackBackupRestoration:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        instance (Union[Unset, str]): Instance that is being restored from the backup
        created (Union[Unset, datetime.datetime]):
        flavor (Union[Unset, str]): Flavor to be used for the restored instance. If not specified, original instance
            flavor will be used
        name (Union[Unset, str]): New instance name. Leave blank to use source instance name.
        floating_ips (Union[Unset, list['OpenStackNestedFloatingIP']]):
        security_groups (Union[Unset, list['OpenStackNestedSecurityGroup']]):
        ports (Union[Unset, list['OpenStackNestedPort']]):
    """

    uuid: Union[Unset, UUID] = UNSET
    instance: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    flavor: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    floating_ips: Union[Unset, list["OpenStackNestedFloatingIP"]] = UNSET
    security_groups: Union[Unset, list["OpenStackNestedSecurityGroup"]] = UNSET
    ports: Union[Unset, list["OpenStackNestedPort"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        instance = self.instance

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        flavor = self.flavor

        name = self.name

        floating_ips: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.floating_ips, Unset):
            floating_ips = []
            for floating_ips_item_data in self.floating_ips:
                floating_ips_item = floating_ips_item_data.to_dict()
                floating_ips.append(floating_ips_item)

        security_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.security_groups, Unset):
            security_groups = []
            for security_groups_item_data in self.security_groups:
                security_groups_item = security_groups_item_data.to_dict()
                security_groups.append(security_groups_item)

        ports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ports, Unset):
            ports = []
            for ports_item_data in self.ports:
                ports_item = ports_item_data.to_dict()
                ports.append(ports_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if instance is not UNSET:
            field_dict["instance"] = instance
        if created is not UNSET:
            field_dict["created"] = created
        if flavor is not UNSET:
            field_dict["flavor"] = flavor
        if name is not UNSET:
            field_dict["name"] = name
        if floating_ips is not UNSET:
            field_dict["floating_ips"] = floating_ips
        if security_groups is not UNSET:
            field_dict["security_groups"] = security_groups
        if ports is not UNSET:
            field_dict["ports"] = ports

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_nested_floating_ip import OpenStackNestedFloatingIP
        from ..models.open_stack_nested_port import OpenStackNestedPort
        from ..models.open_stack_nested_security_group import OpenStackNestedSecurityGroup

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        instance = d.pop("instance", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        flavor = d.pop("flavor", UNSET)

        name = d.pop("name", UNSET)

        floating_ips = []
        _floating_ips = d.pop("floating_ips", UNSET)
        for floating_ips_item_data in _floating_ips or []:
            floating_ips_item = OpenStackNestedFloatingIP.from_dict(floating_ips_item_data)

            floating_ips.append(floating_ips_item)

        security_groups = []
        _security_groups = d.pop("security_groups", UNSET)
        for security_groups_item_data in _security_groups or []:
            security_groups_item = OpenStackNestedSecurityGroup.from_dict(security_groups_item_data)

            security_groups.append(security_groups_item)

        ports = []
        _ports = d.pop("ports", UNSET)
        for ports_item_data in _ports or []:
            ports_item = OpenStackNestedPort.from_dict(ports_item_data)

            ports.append(ports_item)

        open_stack_backup_restoration = cls(
            uuid=uuid,
            instance=instance,
            created=created,
            flavor=flavor,
            name=name,
            floating_ips=floating_ips,
            security_groups=security_groups,
            ports=ports,
        )

        open_stack_backup_restoration.additional_properties = d
        return open_stack_backup_restoration

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
