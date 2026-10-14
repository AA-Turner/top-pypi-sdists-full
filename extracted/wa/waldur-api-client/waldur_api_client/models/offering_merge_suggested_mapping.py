from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_suggested_mapping_component_mapping import (
        OfferingMergeSuggestedMappingComponentMapping,
    )
    from ..models.offering_merge_suggested_mapping_plan_mapping import OfferingMergeSuggestedMappingPlanMapping
    from ..models.offering_merge_unmatched_component import OfferingMergeUnmatchedComponent
    from ..models.offering_merge_unmatched_plan import OfferingMergeUnmatchedPlan


T = TypeVar("T", bound="OfferingMergeSuggestedMapping")


@_attrs_define
class OfferingMergeSuggestedMapping:
    """
    Attributes:
        plan_mapping (OfferingMergeSuggestedMappingPlanMapping): Source plan UUID to the target plan with the same name.
        component_mapping (OfferingMergeSuggestedMappingComponentMapping): Per source offering UUID: source component
            type to the target component of the same type, else the same name.
        unmatched_plans (list['OfferingMergeUnmatchedPlan']):
        unmatched_components (list['OfferingMergeUnmatchedComponent']):
    """

    plan_mapping: "OfferingMergeSuggestedMappingPlanMapping"
    component_mapping: "OfferingMergeSuggestedMappingComponentMapping"
    unmatched_plans: list["OfferingMergeUnmatchedPlan"]
    unmatched_components: list["OfferingMergeUnmatchedComponent"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan_mapping = self.plan_mapping.to_dict()

        component_mapping = self.component_mapping.to_dict()

        unmatched_plans = []
        for unmatched_plans_item_data in self.unmatched_plans:
            unmatched_plans_item = unmatched_plans_item_data.to_dict()
            unmatched_plans.append(unmatched_plans_item)

        unmatched_components = []
        for unmatched_components_item_data in self.unmatched_components:
            unmatched_components_item = unmatched_components_item_data.to_dict()
            unmatched_components.append(unmatched_components_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "plan_mapping": plan_mapping,
                "component_mapping": component_mapping,
                "unmatched_plans": unmatched_plans,
                "unmatched_components": unmatched_components,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_suggested_mapping_component_mapping import (
            OfferingMergeSuggestedMappingComponentMapping,
        )
        from ..models.offering_merge_suggested_mapping_plan_mapping import OfferingMergeSuggestedMappingPlanMapping
        from ..models.offering_merge_unmatched_component import OfferingMergeUnmatchedComponent
        from ..models.offering_merge_unmatched_plan import OfferingMergeUnmatchedPlan

        d = dict(src_dict)
        plan_mapping = OfferingMergeSuggestedMappingPlanMapping.from_dict(d.pop("plan_mapping"))

        component_mapping = OfferingMergeSuggestedMappingComponentMapping.from_dict(d.pop("component_mapping"))

        unmatched_plans = []
        _unmatched_plans = d.pop("unmatched_plans")
        for unmatched_plans_item_data in _unmatched_plans:
            unmatched_plans_item = OfferingMergeUnmatchedPlan.from_dict(unmatched_plans_item_data)

            unmatched_plans.append(unmatched_plans_item)

        unmatched_components = []
        _unmatched_components = d.pop("unmatched_components")
        for unmatched_components_item_data in _unmatched_components:
            unmatched_components_item = OfferingMergeUnmatchedComponent.from_dict(unmatched_components_item_data)

            unmatched_components.append(unmatched_components_item)

        offering_merge_suggested_mapping = cls(
            plan_mapping=plan_mapping,
            component_mapping=component_mapping,
            unmatched_plans=unmatched_plans,
            unmatched_components=unmatched_components,
        )

        offering_merge_suggested_mapping.additional_properties = d
        return offering_merge_suggested_mapping

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
