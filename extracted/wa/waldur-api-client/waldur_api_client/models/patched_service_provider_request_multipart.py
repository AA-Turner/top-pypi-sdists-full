from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PatchedServiceProviderRequestMultipart")


@_attrs_define
class PatchedServiceProviderRequestMultipart:
    """
    Attributes:
        description (Union[Unset, str]):
        enable_notifications (Union[Unset, bool]):
        image (Union[File, None, Unset]):
        allowed_domains (Union[Unset, Any]): List of allowed domains for offering endpoints. Only staff can modify this
            field.
    """

    description: Union[Unset, str] = UNSET
    enable_notifications: Union[Unset, bool] = UNSET
    image: Union[File, None, Unset] = UNSET
    allowed_domains: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        enable_notifications = self.enable_notifications

        image: Union[None, Unset, types.FileTypes]
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, File):
            image = self.image.to_tuple()

        else:
            image = self.image

        allowed_domains = self.allowed_domains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if enable_notifications is not UNSET:
            field_dict["enable_notifications"] = enable_notifications
        if image is not UNSET:
            field_dict["image"] = image
        if allowed_domains is not UNSET:
            field_dict["allowed_domains"] = allowed_domains

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.description, Unset):
            files.append(("description", (None, str(self.description).encode(), "text/plain")))

        if not isinstance(self.enable_notifications, Unset):
            files.append(("enable_notifications", (None, str(self.enable_notifications).encode(), "text/plain")))

        if not isinstance(self.image, Unset):
            if isinstance(self.image, File):
                files.append(("image", self.image.to_tuple()))
            else:
                files.append(("image", (None, str(self.image).encode(), "text/plain")))

        if not isinstance(self.allowed_domains, Unset):
            files.append(("allowed_domains", (None, str(self.allowed_domains).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        enable_notifications = d.pop("enable_notifications", UNSET)

        def _parse_image(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                image_type_0 = File(payload=BytesIO(data))

                return image_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        image = _parse_image(d.pop("image", UNSET))

        allowed_domains = d.pop("allowed_domains", UNSET)

        patched_service_provider_request_multipart = cls(
            description=description,
            enable_notifications=enable_notifications,
            image=image,
            allowed_domains=allowed_domains,
        )

        patched_service_provider_request_multipart.additional_properties = d
        return patched_service_provider_request_multipart

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
