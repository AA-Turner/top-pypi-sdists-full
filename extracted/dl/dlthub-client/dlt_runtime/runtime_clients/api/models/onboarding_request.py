from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OnboardingRequest")


@_attrs_define
class OnboardingRequest:
    """
    Attributes:
        dataplane_id (None | str | Unset): Plane id from GET /dataplanes. Defaults to the first available plane.
        organization_name (None | str | Unset): Personal organization name. Defaults to 'Personal Workspaces'.
        workspace_name (None | str | Unset): Deprecated and ignored. Onboarding always creates exactly one workspace,
            the personal playground.
    """

    dataplane_id: None | str | Unset = UNSET
    organization_name: None | str | Unset = UNSET
    workspace_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataplane_id: None | str | Unset
        if isinstance(self.dataplane_id, Unset):
            dataplane_id = UNSET
        else:
            dataplane_id = self.dataplane_id

        organization_name: None | str | Unset
        if isinstance(self.organization_name, Unset):
            organization_name = UNSET
        else:
            organization_name = self.organization_name

        workspace_name: None | str | Unset
        if isinstance(self.workspace_name, Unset):
            workspace_name = UNSET
        else:
            workspace_name = self.workspace_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dataplane_id is not UNSET:
            field_dict["dataplane_id"] = dataplane_id
        if organization_name is not UNSET:
            field_dict["organization_name"] = organization_name
        if workspace_name is not UNSET:
            field_dict["workspace_name"] = workspace_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_dataplane_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataplane_id = _parse_dataplane_id(d.pop("dataplane_id", UNSET))

        def _parse_organization_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        organization_name = _parse_organization_name(d.pop("organization_name", UNSET))

        def _parse_workspace_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        workspace_name = _parse_workspace_name(d.pop("workspace_name", UNSET))

        onboarding_request = cls(
            dataplane_id=dataplane_id,
            organization_name=organization_name,
            workspace_name=workspace_name,
        )

        onboarding_request.additional_properties = d
        return onboarding_request

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
