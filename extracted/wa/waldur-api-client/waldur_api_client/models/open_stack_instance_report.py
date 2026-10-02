import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="OpenStackInstanceReport")


@_attrs_define
class OpenStackInstanceReport:
    """
    Attributes:
        uuid (UUID): Instance UUID
        name (str): Instance name
        created (datetime.datetime): Creation timestamp
        cores (int): Number of vCPUs
        ram (int): RAM in MiB
        disk (int): Root disk in MiB
        flavor_name (str): Flavor name
        flavor_disk (int): Flavor disk in MiB
        image_name (str): Image name
        hypervisor_hostname (str): Hypervisor hostname
        runtime_state (str): Runtime state (e.g. ACTIVE, SHUTOFF)
        state (str): Provisioning state
        availability_zone_name (Union[None, str]): Availability zone name
        start_time (Union[None, datetime.datetime]): Last start time of the VM
        service_settings_uuid (UUID): Cluster UUID
        service_settings_name (str): Cluster name
        tenant_uuid (UUID): Tenant UUID
        tenant_name (str): Tenant name
        project_uuid (UUID): Project UUID
        project_name (str): Project name
        customer_uuid (UUID): Customer UUID
        customer_name (str): Customer name
        customer_abbreviation (str): Customer abbreviation
        volume_count (int): Number of attached volumes
        total_volume_size_mb (int): Total attached volume size in MiB
        floating_ip_count (int): Number of floating IPs
        port_count (int): Number of ports
        internal_ips (list[str]): List of internal IP addresses
        external_ips (list[str]): List of external IP addresses
    """

    uuid: UUID
    name: str
    created: datetime.datetime
    cores: int
    ram: int
    disk: int
    flavor_name: str
    flavor_disk: int
    image_name: str
    hypervisor_hostname: str
    runtime_state: str
    state: str
    availability_zone_name: Union[None, str]
    start_time: Union[None, datetime.datetime]
    service_settings_uuid: UUID
    service_settings_name: str
    tenant_uuid: UUID
    tenant_name: str
    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    customer_abbreviation: str
    volume_count: int
    total_volume_size_mb: int
    floating_ip_count: int
    port_count: int
    internal_ips: list[str]
    external_ips: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        cores = self.cores

        ram = self.ram

        disk = self.disk

        flavor_name = self.flavor_name

        flavor_disk = self.flavor_disk

        image_name = self.image_name

        hypervisor_hostname = self.hypervisor_hostname

        runtime_state = self.runtime_state

        state = self.state

        availability_zone_name: Union[None, str]
        availability_zone_name = self.availability_zone_name

        start_time: Union[None, str]
        if isinstance(self.start_time, datetime.datetime):
            start_time = self.start_time.isoformat()
        else:
            start_time = self.start_time

        service_settings_uuid = str(self.service_settings_uuid)

        service_settings_name = self.service_settings_name

        tenant_uuid = str(self.tenant_uuid)

        tenant_name = self.tenant_name

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_abbreviation = self.customer_abbreviation

        volume_count = self.volume_count

        total_volume_size_mb = self.total_volume_size_mb

        floating_ip_count = self.floating_ip_count

        port_count = self.port_count

        internal_ips = self.internal_ips

        external_ips = self.external_ips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "created": created,
                "cores": cores,
                "ram": ram,
                "disk": disk,
                "flavor_name": flavor_name,
                "flavor_disk": flavor_disk,
                "image_name": image_name,
                "hypervisor_hostname": hypervisor_hostname,
                "runtime_state": runtime_state,
                "state": state,
                "availability_zone_name": availability_zone_name,
                "start_time": start_time,
                "service_settings_uuid": service_settings_uuid,
                "service_settings_name": service_settings_name,
                "tenant_uuid": tenant_uuid,
                "tenant_name": tenant_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "customer_abbreviation": customer_abbreviation,
                "volume_count": volume_count,
                "total_volume_size_mb": total_volume_size_mb,
                "floating_ip_count": floating_ip_count,
                "port_count": port_count,
                "internal_ips": internal_ips,
                "external_ips": external_ips,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        cores = d.pop("cores")

        ram = d.pop("ram")

        disk = d.pop("disk")

        flavor_name = d.pop("flavor_name")

        flavor_disk = d.pop("flavor_disk")

        image_name = d.pop("image_name")

        hypervisor_hostname = d.pop("hypervisor_hostname")

        runtime_state = d.pop("runtime_state")

        state = d.pop("state")

        def _parse_availability_zone_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        availability_zone_name = _parse_availability_zone_name(d.pop("availability_zone_name"))

        def _parse_start_time(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_time_type_0 = isoparse(data)

                return start_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        start_time = _parse_start_time(d.pop("start_time"))

        service_settings_uuid = UUID(d.pop("service_settings_uuid"))

        service_settings_name = d.pop("service_settings_name")

        tenant_uuid = UUID(d.pop("tenant_uuid"))

        tenant_name = d.pop("tenant_name")

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        customer_abbreviation = d.pop("customer_abbreviation")

        volume_count = d.pop("volume_count")

        total_volume_size_mb = d.pop("total_volume_size_mb")

        floating_ip_count = d.pop("floating_ip_count")

        port_count = d.pop("port_count")

        internal_ips = cast(list[str], d.pop("internal_ips"))

        external_ips = cast(list[str], d.pop("external_ips"))

        open_stack_instance_report = cls(
            uuid=uuid,
            name=name,
            created=created,
            cores=cores,
            ram=ram,
            disk=disk,
            flavor_name=flavor_name,
            flavor_disk=flavor_disk,
            image_name=image_name,
            hypervisor_hostname=hypervisor_hostname,
            runtime_state=runtime_state,
            state=state,
            availability_zone_name=availability_zone_name,
            start_time=start_time,
            service_settings_uuid=service_settings_uuid,
            service_settings_name=service_settings_name,
            tenant_uuid=tenant_uuid,
            tenant_name=tenant_name,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_abbreviation=customer_abbreviation,
            volume_count=volume_count,
            total_volume_size_mb=total_volume_size_mb,
            floating_ip_count=floating_ip_count,
            port_count=port_count,
            internal_ips=internal_ips,
            external_ips=external_ips,
        )

        open_stack_instance_report.additional_properties = d
        return open_stack_instance_report

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
