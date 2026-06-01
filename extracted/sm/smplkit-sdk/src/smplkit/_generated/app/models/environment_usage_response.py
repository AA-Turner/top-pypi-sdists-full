from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.environment_usage_resource import EnvironmentUsageResource


T = TypeVar("T", bound="EnvironmentUsageResponse")


@_attrs_define
class EnvironmentUsageResponse:
    """JSON:API single-resource response envelope for environment-usage counts.

    Attributes:
        data (EnvironmentUsageResource): JSON:API resource envelope for an environment-usage report. Example:
            {'attributes': {'config_overrides': 5, 'flag_env_defaults': 2, 'flag_rules': 3, 'logger_overrides': 1}, 'id':
            'production', 'type': 'environment_usage'}.
    """

    data: EnvironmentUsageResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_usage_resource import EnvironmentUsageResource

        d = dict(src_dict)
        data = EnvironmentUsageResource.from_dict(d.pop("data"))

        environment_usage_response = cls(
            data=data,
        )

        environment_usage_response.additional_properties = d
        return environment_usage_response

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
