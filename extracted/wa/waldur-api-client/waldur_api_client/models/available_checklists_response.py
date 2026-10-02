from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.available_checklists_response_customer_checklist_type_0 import (
        AvailableChecklistsResponseCustomerChecklistType0,
    )
    from ..models.available_checklists_response_intent_checklist_type_0 import (
        AvailableChecklistsResponseIntentChecklistType0,
    )


T = TypeVar("T", bound="AvailableChecklistsResponse")


@_attrs_define
class AvailableChecklistsResponse:
    """
    Attributes:
        customer_checklist (Union['AvailableChecklistsResponseCustomerChecklistType0', None]):
        intent_checklist (Union['AvailableChecklistsResponseIntentChecklistType0', None]):
    """

    customer_checklist: Union["AvailableChecklistsResponseCustomerChecklistType0", None]
    intent_checklist: Union["AvailableChecklistsResponseIntentChecklistType0", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.available_checklists_response_customer_checklist_type_0 import (
            AvailableChecklistsResponseCustomerChecklistType0,
        )
        from ..models.available_checklists_response_intent_checklist_type_0 import (
            AvailableChecklistsResponseIntentChecklistType0,
        )

        customer_checklist: Union[None, dict[str, Any]]
        if isinstance(self.customer_checklist, AvailableChecklistsResponseCustomerChecklistType0):
            customer_checklist = self.customer_checklist.to_dict()
        else:
            customer_checklist = self.customer_checklist

        intent_checklist: Union[None, dict[str, Any]]
        if isinstance(self.intent_checklist, AvailableChecklistsResponseIntentChecklistType0):
            intent_checklist = self.intent_checklist.to_dict()
        else:
            intent_checklist = self.intent_checklist

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "customer_checklist": customer_checklist,
                "intent_checklist": intent_checklist,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.available_checklists_response_customer_checklist_type_0 import (
            AvailableChecklistsResponseCustomerChecklistType0,
        )
        from ..models.available_checklists_response_intent_checklist_type_0 import (
            AvailableChecklistsResponseIntentChecklistType0,
        )

        d = dict(src_dict)

        def _parse_customer_checklist(data: object) -> Union["AvailableChecklistsResponseCustomerChecklistType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                customer_checklist_type_0 = AvailableChecklistsResponseCustomerChecklistType0.from_dict(data)

                return customer_checklist_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AvailableChecklistsResponseCustomerChecklistType0", None], data)

        customer_checklist = _parse_customer_checklist(d.pop("customer_checklist"))

        def _parse_intent_checklist(data: object) -> Union["AvailableChecklistsResponseIntentChecklistType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                intent_checklist_type_0 = AvailableChecklistsResponseIntentChecklistType0.from_dict(data)

                return intent_checklist_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AvailableChecklistsResponseIntentChecklistType0", None], data)

        intent_checklist = _parse_intent_checklist(d.pop("intent_checklist"))

        available_checklists_response = cls(
            customer_checklist=customer_checklist,
            intent_checklist=intent_checklist,
        )

        available_checklists_response.additional_properties = d
        return available_checklists_response

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
