from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_stack_nested_floating_ip_request import OpenStackNestedFloatingIPRequest
    from ..models.open_stack_nested_port_request import OpenStackNestedPortRequest


T = TypeVar("T", bound="OpenStackBackupRestorationRequest")


@_attrs_define
class OpenStackBackupRestorationRequest:
    """
    Attributes:
        flavor (str): Flavor to be used for the restored instance. If not specified, original instance flavor will be
            used
        floating_ips (list['OpenStackNestedFloatingIPRequest']):
        ports (list['OpenStackNestedPortRequest']):
        name (Union[Unset, str]): New instance name. Leave blank to use source instance name.
    """

    flavor: str
    floating_ips: list["OpenStackNestedFloatingIPRequest"]
    ports: list["OpenStackNestedPortRequest"]
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flavor = self.flavor

        floating_ips = []
        for floating_ips_item_data in self.floating_ips:
            floating_ips_item = floating_ips_item_data.to_dict()
            floating_ips.append(floating_ips_item)

        ports = []
        for ports_item_data in self.ports:
            ports_item = ports_item_data.to_dict()
            ports.append(ports_item)

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flavor": flavor,
                "floating_ips": floating_ips,
                "ports": ports,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.open_stack_nested_floating_ip_request import OpenStackNestedFloatingIPRequest
        from ..models.open_stack_nested_port_request import OpenStackNestedPortRequest

        d = dict(src_dict)
        flavor = d.pop("flavor")

        floating_ips = []
        _floating_ips = d.pop("floating_ips")
        for floating_ips_item_data in _floating_ips:
            floating_ips_item = OpenStackNestedFloatingIPRequest.from_dict(floating_ips_item_data)

            floating_ips.append(floating_ips_item)

        ports = []
        _ports = d.pop("ports")
        for ports_item_data in _ports:
            ports_item = OpenStackNestedPortRequest.from_dict(ports_item_data)

            ports.append(ports_item)

        name = d.pop("name", UNSET)

        open_stack_backup_restoration_request = cls(
            flavor=flavor,
            floating_ips=floating_ips,
            ports=ports,
            name=name,
        )

        open_stack_backup_restoration_request.additional_properties = d
        return open_stack_backup_restoration_request

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
