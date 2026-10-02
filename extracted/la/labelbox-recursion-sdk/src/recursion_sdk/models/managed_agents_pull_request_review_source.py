from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_output_policy import ManagedAgentsOutputPolicy
  from ..models.managed_agents_pull_request_target import ManagedAgentsPullRequestTarget
  from ..models.managed_agents_trigger import ManagedAgentsTrigger





T = TypeVar("T", bound="ManagedAgentsPullRequestReviewSource")



@_attrs_define
class ManagedAgentsPullRequestReviewSource:
    """ The durable, non-secret input a pull request review session needs during preparation: the strategy, the connection
    that stages the checkout, the exact target, why it ran, and what it may publish. Credential material is resolved
    just in time and never stored here, in the session config, in workflow history, or in the transcript.

        Example:
            {'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'example', 'outputs': {'capture_patch': True,
                'publish_review': True}, 'target': {'base_sha': 'example', 'head_sha': 'example', 'number': 1, 'owner':
                'example', 'repository': 'example', 'repository_id': 1}, 'trigger': {'binding_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'delivery_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event':
                'example', 'mode': 'example'}}

        Attributes:
            connection_id (str): Organization-scoped integration connection (UUID) whose credentials stage the checkout.
                Only the id is stored; the token itself is minted just in time.
            kind (str): Repository automation strategy this session runs. pull_request_review is the only supported value.
            outputs (ManagedAgentsOutputPolicy): What one repository automation run is allowed to produce. It is snapshotted
                onto the session at start, so a later edit to the trigger binding cannot change what an already-running
                automation does. Example: {'capture_patch': True, 'publish_review': True}.
            target (ManagedAgentsPullRequestTarget): The exact, immutable identity of one GitHub pull request under
                automation: the repository, the number, and the two commits that bound the reviewed diff. Example: {'base_sha':
                'example', 'head_sha': 'example', 'number': 1, 'owner': 'example', 'repository': 'example', 'repository_id': 1}.
            trigger (ManagedAgentsTrigger): Why one repository automation ran. Webhook provenance is recorded without
                persisting the provider's raw payload; a manual run carries the mode alone and no provenance fields at all.
                Example: {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'delivery_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event': 'example', 'mode': 'example'}.
     """

    connection_id: str
    kind: str
    outputs: ManagedAgentsOutputPolicy
    target: ManagedAgentsPullRequestTarget
    trigger: ManagedAgentsTrigger
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_output_policy import ManagedAgentsOutputPolicy # noqa: PLC0415
        from ..models.managed_agents_pull_request_target import ManagedAgentsPullRequestTarget # noqa: PLC0415
        from ..models.managed_agents_trigger import ManagedAgentsTrigger # noqa: PLC0415
        connection_id = self.connection_id

        kind = self.kind

        outputs = self.outputs.to_dict()

        target = self.target.to_dict()

        trigger = self.trigger.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connection_id": connection_id,
            "kind": kind,
            "outputs": outputs,
            "target": target,
            "trigger": trigger,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_output_policy import ManagedAgentsOutputPolicy # noqa: PLC0415
        from ..models.managed_agents_pull_request_target import ManagedAgentsPullRequestTarget # noqa: PLC0415
        from ..models.managed_agents_trigger import ManagedAgentsTrigger # noqa: PLC0415
        d = dict(src_dict)
        connection_id = d.pop("connection_id")

        kind = d.pop("kind")

        outputs = ManagedAgentsOutputPolicy.from_dict(d.pop("outputs"))




        target = ManagedAgentsPullRequestTarget.from_dict(d.pop("target"))




        trigger = ManagedAgentsTrigger.from_dict(d.pop("trigger"))




        managed_agents_pull_request_review_source = cls(
            connection_id=connection_id,
            kind=kind,
            outputs=outputs,
            target=target,
            trigger=trigger,
        )


        managed_agents_pull_request_review_source.additional_properties = d
        return managed_agents_pull_request_review_source

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
