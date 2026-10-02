from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_match_condition_request import ManagedAgentsWebhookMatchConditionRequest





T = TypeVar("T", bound="ManagedAgentsWebhookFilterRequest")



@_attrs_define
class ManagedAgentsWebhookFilterRequest:
    """ A conjunction of conditions that decides whether a webhook delivery starts or continues an automation conversation.

        Example:
            {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'},
                'value': 'example', 'values': ['example']}]}

        Attributes:
            all_ (list[ManagedAgentsWebhookMatchConditionRequest] | Unset): Conditions that must all match; an empty list
                matches every verified delivery.
     """

    all_: list[ManagedAgentsWebhookMatchConditionRequest] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_match_condition_request import ManagedAgentsWebhookMatchConditionRequest # noqa: PLC0415
        all_: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.all_, Unset):
            all_ = []
            for all_item_data in self.all_:
                all_item = all_item_data.to_dict()
                all_.append(all_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if all_ is not UNSET:
            field_dict["all"] = all_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_match_condition_request import ManagedAgentsWebhookMatchConditionRequest # noqa: PLC0415
        d = dict(src_dict)
        _all_ = d.pop("all", UNSET)
        all_: list[ManagedAgentsWebhookMatchConditionRequest] | Unset = UNSET
        if _all_ is not UNSET:
            all_ = []
            for all_item_data in _all_:
                all_item = ManagedAgentsWebhookMatchConditionRequest.from_dict(all_item_data)



                all_.append(all_item)


        managed_agents_webhook_filter_request = cls(
            all_=all_,
        )


        managed_agents_webhook_filter_request.additional_properties = d
        return managed_agents_webhook_filter_request

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
