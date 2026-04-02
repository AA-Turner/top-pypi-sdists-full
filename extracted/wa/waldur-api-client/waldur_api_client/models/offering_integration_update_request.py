from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merged_plugin_options_request import MergedPluginOptionsRequest
    from ..models.merged_secret_options_request import MergedSecretOptionsRequest


T = TypeVar("T", bound="OfferingIntegrationUpdateRequest")


@_attrs_define
class OfferingIntegrationUpdateRequest:
    """
    Attributes:
        secret_options (Union[Unset, MergedSecretOptionsRequest]):
        plugin_options (Union[Unset, MergedPluginOptionsRequest]):
        service_attributes (Union[Unset, Any]):
        backend_id (Union[Unset, str]):
    """

    secret_options: Union[Unset, "MergedSecretOptionsRequest"] = UNSET
    plugin_options: Union[Unset, "MergedPluginOptionsRequest"] = UNSET
    service_attributes: Union[Unset, Any] = UNSET
    backend_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        secret_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_options, Unset):
            secret_options = self.secret_options.to_dict()

        plugin_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plugin_options, Unset):
            plugin_options = self.plugin_options.to_dict()

        service_attributes = self.service_attributes

        backend_id = self.backend_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if secret_options is not UNSET:
            field_dict["secret_options"] = secret_options
        if plugin_options is not UNSET:
            field_dict["plugin_options"] = plugin_options
        if service_attributes is not UNSET:
            field_dict["service_attributes"] = service_attributes
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merged_plugin_options_request import MergedPluginOptionsRequest
        from ..models.merged_secret_options_request import MergedSecretOptionsRequest

        d = dict(src_dict)
        _secret_options = d.pop("secret_options", UNSET)
        secret_options: Union[Unset, MergedSecretOptionsRequest]
        if isinstance(_secret_options, Unset):
            secret_options = UNSET
        else:
            secret_options = MergedSecretOptionsRequest.from_dict(_secret_options)

        _plugin_options = d.pop("plugin_options", UNSET)
        plugin_options: Union[Unset, MergedPluginOptionsRequest]
        if isinstance(_plugin_options, Unset):
            plugin_options = UNSET
        else:
            plugin_options = MergedPluginOptionsRequest.from_dict(_plugin_options)

        service_attributes = d.pop("service_attributes", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        offering_integration_update_request = cls(
            secret_options=secret_options,
            plugin_options=plugin_options,
            service_attributes=service_attributes,
            backend_id=backend_id,
        )

        offering_integration_update_request.additional_properties = d
        return offering_integration_update_request

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
