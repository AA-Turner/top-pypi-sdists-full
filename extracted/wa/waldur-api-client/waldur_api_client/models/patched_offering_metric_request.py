from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_aggregation_enum import ProjectAggregationEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOfferingMetricRequest")


@_attrs_define
class PatchedOfferingMetricRequest:
    """
    Attributes:
        offering (Union[Unset, UUID]):
        definition (Union[Unset, UUID]):
        display_name (Union[Unset, str]): Empty shows the definition's name.
        project_aggregation (Union[Unset, ProjectAggregationEnum]):
    """

    offering: Union[Unset, UUID] = UNSET
    definition: Union[Unset, UUID] = UNSET
    display_name: Union[Unset, str] = UNSET
    project_aggregation: Union[Unset, ProjectAggregationEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering: Union[Unset, str] = UNSET
        if not isinstance(self.offering, Unset):
            offering = str(self.offering)

        definition: Union[Unset, str] = UNSET
        if not isinstance(self.definition, Unset):
            definition = str(self.definition)

        display_name = self.display_name

        project_aggregation: Union[Unset, str] = UNSET
        if not isinstance(self.project_aggregation, Unset):
            project_aggregation = self.project_aggregation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if offering is not UNSET:
            field_dict["offering"] = offering
        if definition is not UNSET:
            field_dict["definition"] = definition
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if project_aggregation is not UNSET:
            field_dict["project_aggregation"] = project_aggregation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _offering = d.pop("offering", UNSET)
        offering: Union[Unset, UUID]
        if isinstance(_offering, Unset):
            offering = UNSET
        else:
            offering = UUID(_offering)

        _definition = d.pop("definition", UNSET)
        definition: Union[Unset, UUID]
        if isinstance(_definition, Unset):
            definition = UNSET
        else:
            definition = UUID(_definition)

        display_name = d.pop("display_name", UNSET)

        _project_aggregation = d.pop("project_aggregation", UNSET)
        project_aggregation: Union[Unset, ProjectAggregationEnum]
        if isinstance(_project_aggregation, Unset):
            project_aggregation = UNSET
        else:
            project_aggregation = ProjectAggregationEnum(_project_aggregation)

        patched_offering_metric_request = cls(
            offering=offering,
            definition=definition,
            display_name=display_name,
            project_aggregation=project_aggregation,
        )

        patched_offering_metric_request.additional_properties = d
        return patched_offering_metric_request

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
