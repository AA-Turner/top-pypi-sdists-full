from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_resource_api_key_update_request_limits_type_0 import (
        PatchedResourceApiKeyUpdateRequestLimitsType0,
    )
    from ..models.patched_resource_api_key_update_request_spending_limits_type_0 import (
        PatchedResourceApiKeyUpdateRequestSpendingLimitsType0,
    )


T = TypeVar("T", bound="PatchedResourceApiKeyUpdateRequest")


@_attrs_define
class PatchedResourceApiKeyUpdateRequest:
    """
    Attributes:
        description (Union[Unset, str]): A note telling the key apart from the resource's other keys, such as the
            environment that uses it. No command to the site agent carries it, so changing it alone issues none and needs no
            enable_api_key_provisioning. Everyone who can list the key reads it, the provider included.
        limits (Union['PatchedResourceApiKeyUpdateRequestLimitsType0', None, Unset]): Month limits per component type;
            zero or absent means no month limit. Replaces the month limits of spending_limits and keeps the other periods.
            Not together with spending_limits.
        spending_limits (Union['PatchedResourceApiKeyUpdateRequestSpendingLimitsType0', None, Unset]): Limits per
            component type and period, replacing the key's limits; a null amount clears that period's limit. Only where the
            offering's api_key_limits is not off. A period other than month must be offered on the component and needs the
            offering's api_key_daily_usage. A limit may not exceed the resource's spending limit for the same period.
        allowed_models (Union[Unset, list[str]]): Models the key may call: ["*"] for every model, an empty list for
            none. Absent, a new key gets none and an edited one keeps its list.
    """

    description: Union[Unset, str] = UNSET
    limits: Union["PatchedResourceApiKeyUpdateRequestLimitsType0", None, Unset] = UNSET
    spending_limits: Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0", None, Unset] = UNSET
    allowed_models: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.patched_resource_api_key_update_request_limits_type_0 import (
            PatchedResourceApiKeyUpdateRequestLimitsType0,
        )
        from ..models.patched_resource_api_key_update_request_spending_limits_type_0 import (
            PatchedResourceApiKeyUpdateRequestSpendingLimitsType0,
        )

        description = self.description

        limits: Union[None, Unset, dict[str, Any]]
        if isinstance(self.limits, Unset):
            limits = UNSET
        elif isinstance(self.limits, PatchedResourceApiKeyUpdateRequestLimitsType0):
            limits = self.limits.to_dict()
        else:
            limits = self.limits

        spending_limits: Union[None, Unset, dict[str, Any]]
        if isinstance(self.spending_limits, Unset):
            spending_limits = UNSET
        elif isinstance(self.spending_limits, PatchedResourceApiKeyUpdateRequestSpendingLimitsType0):
            spending_limits = self.spending_limits.to_dict()
        else:
            spending_limits = self.spending_limits

        allowed_models: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_models, Unset):
            allowed_models = self.allowed_models

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if limits is not UNSET:
            field_dict["limits"] = limits
        if spending_limits is not UNSET:
            field_dict["spending_limits"] = spending_limits
        if allowed_models is not UNSET:
            field_dict["allowed_models"] = allowed_models

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_resource_api_key_update_request_limits_type_0 import (
            PatchedResourceApiKeyUpdateRequestLimitsType0,
        )
        from ..models.patched_resource_api_key_update_request_spending_limits_type_0 import (
            PatchedResourceApiKeyUpdateRequestSpendingLimitsType0,
        )

        d = dict(src_dict)
        description = d.pop("description", UNSET)

        def _parse_limits(data: object) -> Union["PatchedResourceApiKeyUpdateRequestLimitsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                limits_type_0 = PatchedResourceApiKeyUpdateRequestLimitsType0.from_dict(data)

                return limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PatchedResourceApiKeyUpdateRequestLimitsType0", None, Unset], data)

        limits = _parse_limits(d.pop("limits", UNSET))

        def _parse_spending_limits(
            data: object,
        ) -> Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                spending_limits_type_0 = PatchedResourceApiKeyUpdateRequestSpendingLimitsType0.from_dict(data)

                return spending_limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PatchedResourceApiKeyUpdateRequestSpendingLimitsType0", None, Unset], data)

        spending_limits = _parse_spending_limits(d.pop("spending_limits", UNSET))

        allowed_models = cast(list[str], d.pop("allowed_models", UNSET))

        patched_resource_api_key_update_request = cls(
            description=description,
            limits=limits,
            spending_limits=spending_limits,
            allowed_models=allowed_models,
        )

        patched_resource_api_key_update_request.additional_properties = d
        return patched_resource_api_key_update_request

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
