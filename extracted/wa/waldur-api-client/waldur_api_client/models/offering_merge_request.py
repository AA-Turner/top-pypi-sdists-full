from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invoice_policy_enum import InvoicePolicyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offering_merge_request_attribute_key_mapping import OfferingMergeRequestAttributeKeyMapping
    from ..models.offering_merge_request_component_mapping import OfferingMergeRequestComponentMapping
    from ..models.offering_merge_request_plan_mapping import OfferingMergeRequestPlanMapping


T = TypeVar("T", bound="OfferingMergeRequest")


@_attrs_define
class OfferingMergeRequest:
    """
    Attributes:
        sources (list[UUID]): Offerings whose resources and history move to the target.
        target (UUID):
        plan_mapping (Union[Unset, OfferingMergeRequestPlanMapping]): Source plan UUID to target plan UUID.
        component_mapping (Union[Unset, OfferingMergeRequestComponentMapping]): Per source offering UUID: source
            component type to target component type.
        attribute_key_mapping (Union[Unset, OfferingMergeRequestAttributeKeyMapping]): Order and resource answer key
            renames: old key to new key.
        invoice_policy (Union[Unset, InvoicePolicyEnum]):
    """

    sources: list[UUID]
    target: UUID
    plan_mapping: Union[Unset, "OfferingMergeRequestPlanMapping"] = UNSET
    component_mapping: Union[Unset, "OfferingMergeRequestComponentMapping"] = UNSET
    attribute_key_mapping: Union[Unset, "OfferingMergeRequestAttributeKeyMapping"] = UNSET
    invoice_policy: Union[Unset, InvoicePolicyEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sources = []
        for sources_item_data in self.sources:
            sources_item = str(sources_item_data)
            sources.append(sources_item)

        target = str(self.target)

        plan_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan_mapping, Unset):
            plan_mapping = self.plan_mapping.to_dict()

        component_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.component_mapping, Unset):
            component_mapping = self.component_mapping.to_dict()

        attribute_key_mapping: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attribute_key_mapping, Unset):
            attribute_key_mapping = self.attribute_key_mapping.to_dict()

        invoice_policy: Union[Unset, str] = UNSET
        if not isinstance(self.invoice_policy, Unset):
            invoice_policy = self.invoice_policy.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sources": sources,
                "target": target,
            }
        )
        if plan_mapping is not UNSET:
            field_dict["plan_mapping"] = plan_mapping
        if component_mapping is not UNSET:
            field_dict["component_mapping"] = component_mapping
        if attribute_key_mapping is not UNSET:
            field_dict["attribute_key_mapping"] = attribute_key_mapping
        if invoice_policy is not UNSET:
            field_dict["invoice_policy"] = invoice_policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_request_attribute_key_mapping import OfferingMergeRequestAttributeKeyMapping
        from ..models.offering_merge_request_component_mapping import OfferingMergeRequestComponentMapping
        from ..models.offering_merge_request_plan_mapping import OfferingMergeRequestPlanMapping

        d = dict(src_dict)
        sources = []
        _sources = d.pop("sources")
        for sources_item_data in _sources:
            sources_item = UUID(sources_item_data)

            sources.append(sources_item)

        target = UUID(d.pop("target"))

        _plan_mapping = d.pop("plan_mapping", UNSET)
        plan_mapping: Union[Unset, OfferingMergeRequestPlanMapping]
        if isinstance(_plan_mapping, Unset):
            plan_mapping = UNSET
        else:
            plan_mapping = OfferingMergeRequestPlanMapping.from_dict(_plan_mapping)

        _component_mapping = d.pop("component_mapping", UNSET)
        component_mapping: Union[Unset, OfferingMergeRequestComponentMapping]
        if isinstance(_component_mapping, Unset):
            component_mapping = UNSET
        else:
            component_mapping = OfferingMergeRequestComponentMapping.from_dict(_component_mapping)

        _attribute_key_mapping = d.pop("attribute_key_mapping", UNSET)
        attribute_key_mapping: Union[Unset, OfferingMergeRequestAttributeKeyMapping]
        if isinstance(_attribute_key_mapping, Unset):
            attribute_key_mapping = UNSET
        else:
            attribute_key_mapping = OfferingMergeRequestAttributeKeyMapping.from_dict(_attribute_key_mapping)

        _invoice_policy = d.pop("invoice_policy", UNSET)
        invoice_policy: Union[Unset, InvoicePolicyEnum]
        if isinstance(_invoice_policy, Unset):
            invoice_policy = UNSET
        else:
            invoice_policy = InvoicePolicyEnum(_invoice_policy)

        offering_merge_request = cls(
            sources=sources,
            target=target,
            plan_mapping=plan_mapping,
            component_mapping=component_mapping,
            attribute_key_mapping=attribute_key_mapping,
            invoice_policy=invoice_policy,
        )

        offering_merge_request.additional_properties = d
        return offering_merge_request

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
