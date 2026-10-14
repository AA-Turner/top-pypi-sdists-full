from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_api_key_create_request_limits_type_0 import ResourceApiKeyCreateRequestLimitsType0


T = TypeVar("T", bound="ResourceApiKeyCreateRequest")


@_attrs_define
class ResourceApiKeyCreateRequest:
    """
    Attributes:
        resource (UUID):
        user (Union[None, UUID, Unset]): Assignee. When set, only this user can reveal the key.
        limits (Union['ResourceApiKeyCreateRequestLimitsType0', None, Unset]): Limits per component type; zero or absent
            means no limit.
        allowed_models (Union[None, Unset, list[str]]): Models the key may call; empty or absent allows every model.
    """

    resource: UUID
    user: Union[None, UUID, Unset] = UNSET
    limits: Union["ResourceApiKeyCreateRequestLimitsType0", None, Unset] = UNSET
    allowed_models: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_api_key_create_request_limits_type_0 import ResourceApiKeyCreateRequestLimitsType0

        resource = str(self.resource)

        user: Union[None, Unset, str]
        if isinstance(self.user, Unset):
            user = UNSET
        elif isinstance(self.user, UUID):
            user = str(self.user)
        else:
            user = self.user

        limits: Union[None, Unset, dict[str, Any]]
        if isinstance(self.limits, Unset):
            limits = UNSET
        elif isinstance(self.limits, ResourceApiKeyCreateRequestLimitsType0):
            limits = self.limits.to_dict()
        else:
            limits = self.limits

        allowed_models: Union[None, Unset, list[str]]
        if isinstance(self.allowed_models, Unset):
            allowed_models = UNSET
        elif isinstance(self.allowed_models, list):
            allowed_models = self.allowed_models

        else:
            allowed_models = self.allowed_models

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource": resource,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user
        if limits is not UNSET:
            field_dict["limits"] = limits
        if allowed_models is not UNSET:
            field_dict["allowed_models"] = allowed_models

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_api_key_create_request_limits_type_0 import ResourceApiKeyCreateRequestLimitsType0

        d = dict(src_dict)
        resource = UUID(d.pop("resource"))

        def _parse_user(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_type_0 = UUID(data)

                return user_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        user = _parse_user(d.pop("user", UNSET))

        def _parse_limits(data: object) -> Union["ResourceApiKeyCreateRequestLimitsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                limits_type_0 = ResourceApiKeyCreateRequestLimitsType0.from_dict(data)

                return limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceApiKeyCreateRequestLimitsType0", None, Unset], data)

        limits = _parse_limits(d.pop("limits", UNSET))

        def _parse_allowed_models(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_models_type_0 = cast(list[str], data)

                return allowed_models_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        allowed_models = _parse_allowed_models(d.pop("allowed_models", UNSET))

        resource_api_key_create_request = cls(
            resource=resource,
            user=user,
            limits=limits,
            allowed_models=allowed_models,
        )

        resource_api_key_create_request.additional_properties = d
        return resource_api_key_create_request

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
