from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_gateway_model import ManagedAgentsGatewayModel





T = TypeVar("T", bound="ManagedAgentsGatewayModelListResponse")



@_attrs_define
class ManagedAgentsGatewayModelListResponse:
    """ Response body of GET /v1/models. Unlike the other catalogs this one is not read from this service's own storage: it
    is fetched from the deployment-wide model gateway and cached briefly, so a successful response can be slightly
    stale, and the operation returns 503 rather than an empty list when the gateway is unconfigured or unreachable with
    no cache.

        Example:
            {'items': [{'contextWindow': 1, 'displayName': 'example', 'family': 'example', 'maxOutputTokens': 1, 'modelId':
                'example', 'supportedReasoningEfforts': ['example'], 'supportsImageInput': True}]}

        Attributes:
            items (list[ManagedAgentsGatewayModel]): Models the deployment's gateway currently offers. Always an array and
                never null.
     """

    items: list[ManagedAgentsGatewayModel]





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_gateway_model import ManagedAgentsGatewayModel # noqa: PLC0415
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "items": items,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_gateway_model import ManagedAgentsGatewayModel # noqa: PLC0415
        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in (_items):
            items_item = ManagedAgentsGatewayModel.from_dict(items_item_data)



            items.append(items_item)


        managed_agents_gateway_model_list_response = cls(
            items=items,
        )

        return managed_agents_gateway_model_list_response

