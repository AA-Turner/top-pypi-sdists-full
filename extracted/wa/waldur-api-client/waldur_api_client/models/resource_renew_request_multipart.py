import json
from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

if TYPE_CHECKING:
    from ..models.resource_renew_request_multipart_limits import ResourceRenewRequestMultipartLimits


T = TypeVar("T", bound="ResourceRenewRequestMultipart")


@_attrs_define
class ResourceRenewRequestMultipart:
    """
    Attributes:
        extension_months (int): Number of months to extend the subscription by.
        limits (Union[Unset, ResourceRenewRequestMultipartLimits]): Optional new limits for the resource. Supports
            upgrades only.
        request_comment (Union[Unset, str]): Optional comment for the renewal request.
        attachment (Union[Unset, File]): Optional PDF attachment for the renewal request.
    """

    extension_months: int
    limits: Union[Unset, "ResourceRenewRequestMultipartLimits"] = UNSET
    request_comment: Union[Unset, str] = UNSET
    attachment: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        extension_months = self.extension_months

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        request_comment = self.request_comment

        attachment: Union[Unset, types.FileTypes] = UNSET
        if not isinstance(self.attachment, Unset):
            attachment = self.attachment.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "extension_months": extension_months,
            }
        )
        if limits is not UNSET:
            field_dict["limits"] = limits
        if request_comment is not UNSET:
            field_dict["request_comment"] = request_comment
        if attachment is not UNSET:
            field_dict["attachment"] = attachment

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("extension_months", (None, str(self.extension_months).encode(), "text/plain")))

        if not isinstance(self.limits, Unset):
            files.append(("limits", (None, json.dumps(self.limits.to_dict()).encode(), "application/json")))

        if not isinstance(self.request_comment, Unset):
            files.append(("request_comment", (None, str(self.request_comment).encode(), "text/plain")))

        if not isinstance(self.attachment, Unset):
            files.append(("attachment", self.attachment.to_tuple()))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_renew_request_multipart_limits import ResourceRenewRequestMultipartLimits

        d = dict(src_dict)
        extension_months = d.pop("extension_months")

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, ResourceRenewRequestMultipartLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = ResourceRenewRequestMultipartLimits.from_dict(_limits)

        request_comment = d.pop("request_comment", UNSET)

        _attachment = d.pop("attachment", UNSET)
        attachment: Union[Unset, File]
        if isinstance(_attachment, Unset):
            attachment = UNSET
        else:
            attachment = File(payload=BytesIO(_attachment))

        resource_renew_request_multipart = cls(
            extension_months=extension_months,
            limits=limits,
            request_comment=request_comment,
            attachment=attachment,
        )

        resource_renew_request_multipart.additional_properties = d
        return resource_renew_request_multipart

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
