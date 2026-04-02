from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_customer_usage_policy_component_request import NestedCustomerUsagePolicyComponentRequest


T = TypeVar("T", bound="PatchedCustomerComponentUsagePolicyRequest")


@_attrs_define
class PatchedCustomerComponentUsagePolicyRequest:
    """
    Attributes:
        scope (Union[Unset, str]):
        actions (Union[Unset, str]):
        options (Union[Unset, Any]): Fields for saving actions extra data. Keys are name of actions.
        component_limits_set (Union[Unset, list['NestedCustomerUsagePolicyComponentRequest']]):
    """

    scope: Union[Unset, str] = UNSET
    actions: Union[Unset, str] = UNSET
    options: Union[Unset, Any] = UNSET
    component_limits_set: Union[Unset, list["NestedCustomerUsagePolicyComponentRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope = self.scope

        actions = self.actions

        options = self.options

        component_limits_set: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.component_limits_set, Unset):
            component_limits_set = []
            for component_limits_set_item_data in self.component_limits_set:
                component_limits_set_item = component_limits_set_item_data.to_dict()
                component_limits_set.append(component_limits_set_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scope is not UNSET:
            field_dict["scope"] = scope
        if actions is not UNSET:
            field_dict["actions"] = actions
        if options is not UNSET:
            field_dict["options"] = options
        if component_limits_set is not UNSET:
            field_dict["component_limits_set"] = component_limits_set

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_customer_usage_policy_component_request import NestedCustomerUsagePolicyComponentRequest

        d = dict(src_dict)
        scope = d.pop("scope", UNSET)

        actions = d.pop("actions", UNSET)

        options = d.pop("options", UNSET)

        component_limits_set = []
        _component_limits_set = d.pop("component_limits_set", UNSET)
        for component_limits_set_item_data in _component_limits_set or []:
            component_limits_set_item = NestedCustomerUsagePolicyComponentRequest.from_dict(
                component_limits_set_item_data
            )

            component_limits_set.append(component_limits_set_item)

        patched_customer_component_usage_policy_request = cls(
            scope=scope,
            actions=actions,
            options=options,
            component_limits_set=component_limits_set,
        )

        patched_customer_component_usage_policy_request.additional_properties = d
        return patched_customer_component_usage_policy_request

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
