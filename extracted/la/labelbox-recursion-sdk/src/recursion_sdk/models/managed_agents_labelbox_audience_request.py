from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_labelbox_audience_request_kind import ManagedAgentsLabelboxAudienceRequestKind






T = TypeVar("T", bound="ManagedAgentsLabelboxAudienceRequest")



@_attrs_define
class ManagedAgentsLabelboxAudienceRequest:
    """ Exact Slack trigger binding authorized to use an organization-wide Labelbox product-state credential, with an
    explicit internal or Slack Connect classification.

        Example:
            {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'internal_slack_binding'}

        Attributes:
            binding_id (str): Exact Slack trigger binding id authorized to use the credential.
            channel_id (str): Exact Slack channel id used by the binding. The signed webhook receipt's sharing
                classification must match kind.
            connection_id (str): Exact Slack integration connection id used by the binding.
            kind (ManagedAgentsLabelboxAudienceRequestKind): Optional restriction of organization-wide Labelbox access to
                one exact binding whose internal or Slack Connect classification is explicit.
     """

    binding_id: str
    channel_id: str
    connection_id: str
    kind: ManagedAgentsLabelboxAudienceRequestKind
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        binding_id = self.binding_id

        channel_id = self.channel_id

        connection_id = self.connection_id

        kind = self.kind.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "binding_id": binding_id,
            "channel_id": channel_id,
            "connection_id": connection_id,
            "kind": kind,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        binding_id = d.pop("binding_id")

        channel_id = d.pop("channel_id")

        connection_id = d.pop("connection_id")

        kind = ManagedAgentsLabelboxAudienceRequestKind(d.pop("kind"))




        managed_agents_labelbox_audience_request = cls(
            binding_id=binding_id,
            channel_id=channel_id,
            connection_id=connection_id,
            kind=kind,
        )


        managed_agents_labelbox_audience_request.additional_properties = d
        return managed_agents_labelbox_audience_request

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
