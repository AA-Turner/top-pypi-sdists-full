from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.hpc_service_health import HpcServiceHealth


T = TypeVar("T", bound="HpcWorkspaceOverview")


@_attrs_define
class HpcWorkspaceOverview:
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
        username (Union[None, str]):
        home_directory (Union[None, str]):
        healthy (Union[None, bool]):
        services_health (Union[None, list['HpcServiceHealth']]):
        error (Union[None, str]):
        sign_in_provider (Union[None, str]): Identity provider to sign in through again to restore HPC access, when that
            is what 'error' asks for.
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
    username: Union[None, str]
    home_directory: Union[None, str]
    healthy: Union[None, bool]
    services_health: Union[None, list["HpcServiceHealth"]]
    error: Union[None, str]
    sign_in_provider: Union[None, str]
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

        username: Union[None, str]
        username = self.username

        home_directory: Union[None, str]
        home_directory = self.home_directory

        healthy: Union[None, bool]
        healthy = self.healthy

        services_health: Union[None, list[dict[str, Any]]]
        if isinstance(self.services_health, list):
            services_health = []
            for services_health_type_0_item_data in self.services_health:
                services_health_type_0_item = services_health_type_0_item_data.to_dict()
                services_health.append(services_health_type_0_item)

        else:
            services_health = self.services_health

        error: Union[None, str]
        error = self.error

        sign_in_provider: Union[None, str]
        sign_in_provider = self.sign_in_provider

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
                "username": username,
                "home_directory": home_directory,
                "healthy": healthy,
                "services_health": services_health,
                "error": error,
                "sign_in_provider": sign_in_provider,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hpc_service_health import HpcServiceHealth

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

        def _parse_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        username = _parse_username(d.pop("username"))

        def _parse_home_directory(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        home_directory = _parse_home_directory(d.pop("home_directory"))

        def _parse_healthy(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        healthy = _parse_healthy(d.pop("healthy"))

        def _parse_services_health(data: object) -> Union[None, list["HpcServiceHealth"]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                services_health_type_0 = []
                _services_health_type_0 = data
                for services_health_type_0_item_data in _services_health_type_0:
                    services_health_type_0_item = HpcServiceHealth.from_dict(services_health_type_0_item_data)

                    services_health_type_0.append(services_health_type_0_item)

                return services_health_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list["HpcServiceHealth"]], data)

        services_health = _parse_services_health(d.pop("services_health"))

        def _parse_error(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        error = _parse_error(d.pop("error"))

        def _parse_sign_in_provider(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sign_in_provider = _parse_sign_in_provider(d.pop("sign_in_provider"))

        hpc_workspace_overview = cls(
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
            username=username,
            home_directory=home_directory,
            healthy=healthy,
            services_health=services_health,
            error=error,
            sign_in_provider=sign_in_provider,
        )

        hpc_workspace_overview.additional_properties = d
        return hpc_workspace_overview

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
