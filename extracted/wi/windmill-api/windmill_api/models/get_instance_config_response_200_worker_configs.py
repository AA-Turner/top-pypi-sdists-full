from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_instance_config_response_200_worker_configs_additional_property import (
        GetInstanceConfigResponse200WorkerConfigsAdditionalProperty,
    )


T = TypeVar("T", bound="GetInstanceConfigResponse200WorkerConfigs")


@_attrs_define
class GetInstanceConfigResponse200WorkerConfigs:
    """Worker group configurations keyed by group name (e.g. "default", "gpu"). Each value contains worker_tags, init_bash,
    autoscaling, etc.

    """

    additional_properties: Dict[str, "GetInstanceConfigResponse200WorkerConfigsAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_instance_config_response_200_worker_configs_additional_property import (
            GetInstanceConfigResponse200WorkerConfigsAdditionalProperty,
        )

        d = src_dict.copy()
        get_instance_config_response_200_worker_configs = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetInstanceConfigResponse200WorkerConfigsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_instance_config_response_200_worker_configs.additional_properties = additional_properties
        return get_instance_config_response_200_worker_configs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetInstanceConfigResponse200WorkerConfigsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetInstanceConfigResponse200WorkerConfigsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
