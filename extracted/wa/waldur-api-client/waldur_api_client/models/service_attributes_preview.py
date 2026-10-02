from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.service_attributes_preview_plugin_options import ServiceAttributesPreviewPluginOptions
    from ..models.service_attributes_preview_service_attributes import ServiceAttributesPreviewServiceAttributes


T = TypeVar("T", bound="ServiceAttributesPreview")


@_attrs_define
class ServiceAttributesPreview:
    """
    Attributes:
        service_attributes (ServiceAttributesPreviewServiceAttributes):
        plugin_options (ServiceAttributesPreviewPluginOptions):
    """

    service_attributes: "ServiceAttributesPreviewServiceAttributes"
    plugin_options: "ServiceAttributesPreviewPluginOptions"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service_attributes = self.service_attributes.to_dict()

        plugin_options = self.plugin_options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "service_attributes": service_attributes,
                "plugin_options": plugin_options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_attributes_preview_plugin_options import ServiceAttributesPreviewPluginOptions
        from ..models.service_attributes_preview_service_attributes import ServiceAttributesPreviewServiceAttributes

        d = dict(src_dict)
        service_attributes = ServiceAttributesPreviewServiceAttributes.from_dict(d.pop("service_attributes"))

        plugin_options = ServiceAttributesPreviewPluginOptions.from_dict(d.pop("plugin_options"))

        service_attributes_preview = cls(
            service_attributes=service_attributes,
            plugin_options=plugin_options,
        )

        service_attributes_preview.additional_properties = d
        return service_attributes_preview

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
