from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_hub_integration_meta_response_200_derived_style import GetHubIntegrationMetaResponse200DerivedStyle

if TYPE_CHECKING:
    from ..models.get_hub_integration_meta_response_200_derived_api_hosts_item import (
        GetHubIntegrationMetaResponse200DerivedApiHostsItem,
    )
    from ..models.get_hub_integration_meta_response_200_derived_languages import (
        GetHubIntegrationMetaResponse200DerivedLanguages,
    )
    from ..models.get_hub_integration_meta_response_200_derived_script_counts import (
        GetHubIntegrationMetaResponse200DerivedScriptCounts,
    )
    from ..models.get_hub_integration_meta_response_200_derived_top_scripts_item import (
        GetHubIntegrationMetaResponse200DerivedTopScriptsItem,
    )


T = TypeVar("T", bound="GetHubIntegrationMetaResponse200Derived")


@_attrs_define
class GetHubIntegrationMetaResponse200Derived:
    """facts computed from the integration's shipped scripts

    Attributes:
        api_hosts (List['GetHubIntegrationMetaResponse200DerivedApiHostsItem']):
        style (GetHubIntegrationMetaResponse200DerivedStyle):
        languages (GetHubIntegrationMetaResponse200DerivedLanguages):
        script_counts (GetHubIntegrationMetaResponse200DerivedScriptCounts):
        top_scripts (List['GetHubIntegrationMetaResponse200DerivedTopScriptsItem']):
    """

    api_hosts: List["GetHubIntegrationMetaResponse200DerivedApiHostsItem"]
    style: GetHubIntegrationMetaResponse200DerivedStyle
    languages: "GetHubIntegrationMetaResponse200DerivedLanguages"
    script_counts: "GetHubIntegrationMetaResponse200DerivedScriptCounts"
    top_scripts: List["GetHubIntegrationMetaResponse200DerivedTopScriptsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        api_hosts = []
        for api_hosts_item_data in self.api_hosts:
            api_hosts_item = api_hosts_item_data.to_dict()

            api_hosts.append(api_hosts_item)

        style = self.style.value

        languages = self.languages.to_dict()

        script_counts = self.script_counts.to_dict()

        top_scripts = []
        for top_scripts_item_data in self.top_scripts:
            top_scripts_item = top_scripts_item_data.to_dict()

            top_scripts.append(top_scripts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_hosts": api_hosts,
                "style": style,
                "languages": languages,
                "script_counts": script_counts,
                "top_scripts": top_scripts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_hub_integration_meta_response_200_derived_api_hosts_item import (
            GetHubIntegrationMetaResponse200DerivedApiHostsItem,
        )
        from ..models.get_hub_integration_meta_response_200_derived_languages import (
            GetHubIntegrationMetaResponse200DerivedLanguages,
        )
        from ..models.get_hub_integration_meta_response_200_derived_script_counts import (
            GetHubIntegrationMetaResponse200DerivedScriptCounts,
        )
        from ..models.get_hub_integration_meta_response_200_derived_top_scripts_item import (
            GetHubIntegrationMetaResponse200DerivedTopScriptsItem,
        )

        d = src_dict.copy()
        api_hosts = []
        _api_hosts = d.pop("api_hosts")
        for api_hosts_item_data in _api_hosts:
            api_hosts_item = GetHubIntegrationMetaResponse200DerivedApiHostsItem.from_dict(api_hosts_item_data)

            api_hosts.append(api_hosts_item)

        style = GetHubIntegrationMetaResponse200DerivedStyle(d.pop("style"))

        languages = GetHubIntegrationMetaResponse200DerivedLanguages.from_dict(d.pop("languages"))

        script_counts = GetHubIntegrationMetaResponse200DerivedScriptCounts.from_dict(d.pop("script_counts"))

        top_scripts = []
        _top_scripts = d.pop("top_scripts")
        for top_scripts_item_data in _top_scripts:
            top_scripts_item = GetHubIntegrationMetaResponse200DerivedTopScriptsItem.from_dict(top_scripts_item_data)

            top_scripts.append(top_scripts_item)

        get_hub_integration_meta_response_200_derived = cls(
            api_hosts=api_hosts,
            style=style,
            languages=languages,
            script_counts=script_counts,
            top_scripts=top_scripts,
        )

        get_hub_integration_meta_response_200_derived.additional_properties = d
        return get_hub_integration_meta_response_200_derived

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
