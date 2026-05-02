from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_cloud_quotas_response_200_apps import GetCloudQuotasResponse200Apps
    from ..models.get_cloud_quotas_response_200_flows import GetCloudQuotasResponse200Flows
    from ..models.get_cloud_quotas_response_200_resources import GetCloudQuotasResponse200Resources
    from ..models.get_cloud_quotas_response_200_scripts import GetCloudQuotasResponse200Scripts
    from ..models.get_cloud_quotas_response_200_variables import GetCloudQuotasResponse200Variables


T = TypeVar("T", bound="GetCloudQuotasResponse200")


@_attrs_define
class GetCloudQuotasResponse200:
    """
    Attributes:
        scripts (GetCloudQuotasResponse200Scripts):
        flows (GetCloudQuotasResponse200Flows):
        apps (GetCloudQuotasResponse200Apps):
        variables (GetCloudQuotasResponse200Variables):
        resources (GetCloudQuotasResponse200Resources):
    """

    scripts: "GetCloudQuotasResponse200Scripts"
    flows: "GetCloudQuotasResponse200Flows"
    apps: "GetCloudQuotasResponse200Apps"
    variables: "GetCloudQuotasResponse200Variables"
    resources: "GetCloudQuotasResponse200Resources"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scripts = self.scripts.to_dict()

        flows = self.flows.to_dict()

        apps = self.apps.to_dict()

        variables = self.variables.to_dict()

        resources = self.resources.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scripts": scripts,
                "flows": flows,
                "apps": apps,
                "variables": variables,
                "resources": resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_cloud_quotas_response_200_apps import GetCloudQuotasResponse200Apps
        from ..models.get_cloud_quotas_response_200_flows import GetCloudQuotasResponse200Flows
        from ..models.get_cloud_quotas_response_200_resources import GetCloudQuotasResponse200Resources
        from ..models.get_cloud_quotas_response_200_scripts import GetCloudQuotasResponse200Scripts
        from ..models.get_cloud_quotas_response_200_variables import GetCloudQuotasResponse200Variables

        d = src_dict.copy()
        scripts = GetCloudQuotasResponse200Scripts.from_dict(d.pop("scripts"))

        flows = GetCloudQuotasResponse200Flows.from_dict(d.pop("flows"))

        apps = GetCloudQuotasResponse200Apps.from_dict(d.pop("apps"))

        variables = GetCloudQuotasResponse200Variables.from_dict(d.pop("variables"))

        resources = GetCloudQuotasResponse200Resources.from_dict(d.pop("resources"))

        get_cloud_quotas_response_200 = cls(
            scripts=scripts,
            flows=flows,
            apps=apps,
            variables=variables,
            resources=resources,
        )

        get_cloud_quotas_response_200.additional_properties = d
        return get_cloud_quotas_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
