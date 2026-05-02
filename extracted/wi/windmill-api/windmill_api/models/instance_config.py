from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.instance_config_global_settings import InstanceConfigGlobalSettings
    from ..models.instance_config_worker_configs import InstanceConfigWorkerConfigs


T = TypeVar("T", bound="InstanceConfig")


@_attrs_define
class InstanceConfig:
    """Unified instance configuration combining global settings and worker group configs

    Attributes:
        global_settings (Union[Unset, InstanceConfigGlobalSettings]): Global settings keyed by setting name. Known
            fields include base_url, license_key, retention_period_secs, smtp_settings, otel, etc. Unknown fields are
            preserved as-is.
        worker_configs (Union[Unset, InstanceConfigWorkerConfigs]): Worker group configurations keyed by group name
            (e.g. "default", "gpu"). Each value contains worker_tags, init_bash, autoscaling, etc.
    """

    global_settings: Union[Unset, "InstanceConfigGlobalSettings"] = UNSET
    worker_configs: Union[Unset, "InstanceConfigWorkerConfigs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        global_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.global_settings, Unset):
            global_settings = self.global_settings.to_dict()

        worker_configs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.worker_configs, Unset):
            worker_configs = self.worker_configs.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if global_settings is not UNSET:
            field_dict["global_settings"] = global_settings
        if worker_configs is not UNSET:
            field_dict["worker_configs"] = worker_configs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.instance_config_global_settings import InstanceConfigGlobalSettings
        from ..models.instance_config_worker_configs import InstanceConfigWorkerConfigs

        d = src_dict.copy()
        _global_settings = d.pop("global_settings", UNSET)
        global_settings: Union[Unset, InstanceConfigGlobalSettings]
        if isinstance(_global_settings, Unset):
            global_settings = UNSET
        else:
            global_settings = InstanceConfigGlobalSettings.from_dict(_global_settings)

        _worker_configs = d.pop("worker_configs", UNSET)
        worker_configs: Union[Unset, InstanceConfigWorkerConfigs]
        if isinstance(_worker_configs, Unset):
            worker_configs = UNSET
        else:
            worker_configs = InstanceConfigWorkerConfigs.from_dict(_worker_configs)

        instance_config = cls(
            global_settings=global_settings,
            worker_configs=worker_configs,
        )

        instance_config.additional_properties = d
        return instance_config

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
