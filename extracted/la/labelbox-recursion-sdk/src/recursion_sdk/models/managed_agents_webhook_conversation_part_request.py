from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest





T = TypeVar("T", bound="ManagedAgentsWebhookConversationPartRequest")



@_attrs_define
class ManagedAgentsWebhookConversationPartRequest:
    """ One component of a stable automation conversation key, with ordered fallback selectors.

        Example:
            {'selectors': [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}

        Attributes:
            selectors (list[ManagedAgentsWebhookValueSelectorRequest] | None | Unset): Fallback selectors checked in order;
                the first present value contributes this part of the conversation key.
     """

    selectors: list[ManagedAgentsWebhookValueSelectorRequest] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest # noqa: PLC0415
        selectors: list[dict[str, Any]] | None | Unset
        if isinstance(self.selectors, Unset):
            selectors = UNSET
        elif isinstance(self.selectors, list):
            selectors = []
            for selectors_type_0_item_data in self.selectors:
                selectors_type_0_item = selectors_type_0_item_data.to_dict()
                selectors.append(selectors_type_0_item)


        else:
            selectors = self.selectors


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if selectors is not UNSET:
            field_dict["selectors"] = selectors

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_value_selector_request import ManagedAgentsWebhookValueSelectorRequest # noqa: PLC0415
        d = dict(src_dict)
        def _parse_selectors(data: object) -> list[ManagedAgentsWebhookValueSelectorRequest] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                selectors_type_0 = []
                _selectors_type_0 = data
                for selectors_type_0_item_data in (_selectors_type_0):
                    selectors_type_0_item = ManagedAgentsWebhookValueSelectorRequest.from_dict(selectors_type_0_item_data)



                    selectors_type_0.append(selectors_type_0_item)

                return selectors_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsWebhookValueSelectorRequest] | None | Unset, data)

        selectors = _parse_selectors(d.pop("selectors", UNSET))


        managed_agents_webhook_conversation_part_request = cls(
            selectors=selectors,
        )


        managed_agents_webhook_conversation_part_request.additional_properties = d
        return managed_agents_webhook_conversation_part_request

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
