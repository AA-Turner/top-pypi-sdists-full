from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SiteAgentConfigGenerationRequest")


@_attrs_define
class SiteAgentConfigGenerationRequest:
    """
    Attributes:
        offering_uuids (list[UUID]): List of SLURM offering UUIDs to include in configuration
        include_policy_settings (Union[Unset, bool]): Include SLURM periodic usage policy settings in configuration
            Default: True.
        waldur_api_url (Union[Unset, str]): Waldur API URL (defaults to current server URL)
        timezone (Union[Unset, str]): Timezone for the site agent Default: 'UTC'.
    """

    offering_uuids: list[UUID]
    include_policy_settings: Union[Unset, bool] = True
    waldur_api_url: Union[Unset, str] = UNSET
    timezone: Union[Unset, str] = "UTC"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuids = []
        for offering_uuids_item_data in self.offering_uuids:
            offering_uuids_item = str(offering_uuids_item_data)
            offering_uuids.append(offering_uuids_item)

        include_policy_settings = self.include_policy_settings

        waldur_api_url = self.waldur_api_url

        timezone = self.timezone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuids": offering_uuids,
            }
        )
        if include_policy_settings is not UNSET:
            field_dict["include_policy_settings"] = include_policy_settings
        if waldur_api_url is not UNSET:
            field_dict["waldur_api_url"] = waldur_api_url
        if timezone is not UNSET:
            field_dict["timezone"] = timezone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuids = []
        _offering_uuids = d.pop("offering_uuids")
        for offering_uuids_item_data in _offering_uuids:
            offering_uuids_item = UUID(offering_uuids_item_data)

            offering_uuids.append(offering_uuids_item)

        include_policy_settings = d.pop("include_policy_settings", UNSET)

        waldur_api_url = d.pop("waldur_api_url", UNSET)

        timezone = d.pop("timezone", UNSET)

        site_agent_config_generation_request = cls(
            offering_uuids=offering_uuids,
            include_policy_settings=include_policy_settings,
            waldur_api_url=waldur_api_url,
            timezone=timezone,
        )

        site_agent_config_generation_request.additional_properties = d
        return site_agent_config_generation_request

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
