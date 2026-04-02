from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.category_enum import CategoryEnum
from ..models.corrective_action_severity_enum import CorrectiveActionSeverityEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.corrective_action_metadata import CorrectiveActionMetadata
    from ..models.corrective_action_route_params import CorrectiveActionRouteParams


T = TypeVar("T", bound="CorrectiveAction")


@_attrs_define
class CorrectiveAction:
    """
    Attributes:
        label (str):
        category (CategoryEnum):
        severity (CorrectiveActionSeverityEnum):
        method (Union[Unset, str]):  Default: 'GET'.
        api_endpoint (Union[Unset, bool]):  Default: False.
        confirmation_required (Union[Unset, bool]):  Default: False.
        permissions_required (Union[Unset, list[str]]):
        metadata (Union[Unset, CorrectiveActionMetadata]):
        route_name (Union[None, Unset, str]):
        route_params (Union[Unset, CorrectiveActionRouteParams]):
    """

    label: str
    category: CategoryEnum
    severity: CorrectiveActionSeverityEnum
    method: Union[Unset, str] = "GET"
    api_endpoint: Union[Unset, bool] = False
    confirmation_required: Union[Unset, bool] = False
    permissions_required: Union[Unset, list[str]] = UNSET
    metadata: Union[Unset, "CorrectiveActionMetadata"] = UNSET
    route_name: Union[None, Unset, str] = UNSET
    route_params: Union[Unset, "CorrectiveActionRouteParams"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        category = self.category.value

        severity = self.severity.value

        method = self.method

        api_endpoint = self.api_endpoint

        confirmation_required = self.confirmation_required

        permissions_required: Union[Unset, list[str]] = UNSET
        if not isinstance(self.permissions_required, Unset):
            permissions_required = self.permissions_required

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        route_name: Union[None, Unset, str]
        if isinstance(self.route_name, Unset):
            route_name = UNSET
        else:
            route_name = self.route_name

        route_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.route_params, Unset):
            route_params = self.route_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "category": category,
                "severity": severity,
            }
        )
        if method is not UNSET:
            field_dict["method"] = method
        if api_endpoint is not UNSET:
            field_dict["api_endpoint"] = api_endpoint
        if confirmation_required is not UNSET:
            field_dict["confirmation_required"] = confirmation_required
        if permissions_required is not UNSET:
            field_dict["permissions_required"] = permissions_required
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if route_name is not UNSET:
            field_dict["route_name"] = route_name
        if route_params is not UNSET:
            field_dict["route_params"] = route_params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.corrective_action_metadata import CorrectiveActionMetadata
        from ..models.corrective_action_route_params import CorrectiveActionRouteParams

        d = dict(src_dict)
        label = d.pop("label")

        category = CategoryEnum(d.pop("category"))

        severity = CorrectiveActionSeverityEnum(d.pop("severity"))

        method = d.pop("method", UNSET)

        api_endpoint = d.pop("api_endpoint", UNSET)

        confirmation_required = d.pop("confirmation_required", UNSET)

        permissions_required = cast(list[str], d.pop("permissions_required", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, CorrectiveActionMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CorrectiveActionMetadata.from_dict(_metadata)

        def _parse_route_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        route_name = _parse_route_name(d.pop("route_name", UNSET))

        _route_params = d.pop("route_params", UNSET)
        route_params: Union[Unset, CorrectiveActionRouteParams]
        if isinstance(_route_params, Unset):
            route_params = UNSET
        else:
            route_params = CorrectiveActionRouteParams.from_dict(_route_params)

        corrective_action = cls(
            label=label,
            category=category,
            severity=severity,
            method=method,
            api_endpoint=api_endpoint,
            confirmation_required=confirmation_required,
            permissions_required=permissions_required,
            metadata=metadata,
            route_name=route_name,
            route_params=route_params,
        )

        corrective_action.additional_properties = d
        return corrective_action

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
