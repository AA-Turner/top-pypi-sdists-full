from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HpcWorkspace")


@_attrs_define
class HpcWorkspace:
    """
    Attributes:
        resource_uuid (UUID):
        resource_name (str):
        account (str):
        offering_uuid (UUID):
        offering_name (str):
        project_uuid (UUID):
        project_name (str):
        customer_name (str):
        system_name (str):
        state (str):
        firecrest_enabled (bool): Jobs can be submitted and canceled and files opened through FirecREST. Without it the
            workspace is read-only, from the cluster monitor.
        monitoring_enabled (bool): Jobs have per-run performance samples from the cluster monitor.
    """

    resource_uuid: UUID
    resource_name: str
    account: str
    offering_uuid: UUID
    offering_name: str
    project_uuid: UUID
    project_name: str
    customer_name: str
    system_name: str
    state: str
    firecrest_enabled: bool
    monitoring_enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        account = self.account

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_name = self.customer_name

        system_name = self.system_name

        state = self.state

        firecrest_enabled = self.firecrest_enabled

        monitoring_enabled = self.monitoring_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "account": account,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_name": customer_name,
                "system_name": system_name,
                "state": state,
                "firecrest_enabled": firecrest_enabled,
                "monitoring_enabled": monitoring_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        account = d.pop("account")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_name = d.pop("customer_name")

        system_name = d.pop("system_name")

        state = d.pop("state")

        firecrest_enabled = d.pop("firecrest_enabled")

        monitoring_enabled = d.pop("monitoring_enabled")

        hpc_workspace = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            account=account,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_name=customer_name,
            system_name=system_name,
            state=state,
            firecrest_enabled=firecrest_enabled,
            monitoring_enabled=monitoring_enabled,
        )

        hpc_workspace.additional_properties = d
        return hpc_workspace

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
