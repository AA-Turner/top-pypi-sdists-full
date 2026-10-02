from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_result import ManagedAgentsAutomationResult
  from ..models.managed_agents_pull_request_review_result import ManagedAgentsPullRequestReviewResult
  from ..models.managed_agents_pull_request_review_source import ManagedAgentsPullRequestReviewSource





T = TypeVar("T", bound="ManagedAgentsPullRequestReviewResultResponse")



@_attrs_define
class ManagedAgentsPullRequestReviewResultResponse:
    """ The completed review for one pull request review session. Available only after the session completes, and returned
    only once every claimed finding location has been rebound to the trusted exact-SHA diff manifest.

        Example:
            {'automation': {'patch': {'byte_size': 1, 'changed': True, 'event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'patch_sha256': 'example'}, 'publication': {'published': True, 'review_id': 1, 'url': 'https://example.com'}},
                'result': {'findings': [{'body': 'example', 'evidence': 'example', 'line': 1, 'path': 'example', 'severity':
                'example', 'side': 'example'}], 'summary': 'example', 'verdict': 'example'}, 'source': {'connection_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'example', 'outputs': {'capture_patch': True, 'publish_review':
                True}, 'target': {'base_sha': 'example', 'head_sha': 'example', 'number': 1, 'owner': 'example', 'repository':
                'example', 'repository_id': 1}, 'trigger': {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'delivery_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event': 'example', 'mode': 'example'}}}

        Attributes:
            automation (ManagedAgentsAutomationResult): The trusted side effects one repository automation performed after
                its result passed validation: the patch it captured and the review it published. A session that completed before
                output finalization existed reads back zero-valued, meaning neither happened. Example: {'patch': {'byte_size':
                1, 'changed': True, 'event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'patch_sha256': 'example'},
                'publication': {'published': True, 'review_id': 1, 'url': 'https://example.com'}}.
            result (ManagedAgentsPullRequestReviewResult): One agent's review of a pull request: a summary, a verdict, and
                the line-level findings. It is returned only after every claimed location has been rebound to the trusted exact-
                SHA diff manifest. Example: {'findings': [{'body': 'example', 'evidence': 'example', 'line': 1, 'path':
                'example', 'severity': 'example', 'side': 'example'}], 'summary': 'example', 'verdict': 'example'}.
            source (ManagedAgentsPullRequestReviewSource): The durable, non-secret input a pull request review session needs
                during preparation: the strategy, the connection that stages the checkout, the exact target, why it ran, and
                what it may publish. Credential material is resolved just in time and never stored here, in the session config,
                in workflow history, or in the transcript. Example: {'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'kind': 'example', 'outputs': {'capture_patch': True, 'publish_review': True}, 'target': {'base_sha': 'example',
                'head_sha': 'example', 'number': 1, 'owner': 'example', 'repository': 'example', 'repository_id': 1}, 'trigger':
                {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'delivery_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'event': 'example', 'mode': 'example'}}.
     """

    automation: ManagedAgentsAutomationResult
    result: ManagedAgentsPullRequestReviewResult
    source: ManagedAgentsPullRequestReviewSource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_result import ManagedAgentsAutomationResult # noqa: PLC0415
        from ..models.managed_agents_pull_request_review_result import ManagedAgentsPullRequestReviewResult # noqa: PLC0415
        from ..models.managed_agents_pull_request_review_source import ManagedAgentsPullRequestReviewSource # noqa: PLC0415
        automation = self.automation.to_dict()

        result = self.result.to_dict()

        source = self.source.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "automation": automation,
            "result": result,
            "source": source,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_result import ManagedAgentsAutomationResult # noqa: PLC0415
        from ..models.managed_agents_pull_request_review_result import ManagedAgentsPullRequestReviewResult # noqa: PLC0415
        from ..models.managed_agents_pull_request_review_source import ManagedAgentsPullRequestReviewSource # noqa: PLC0415
        d = dict(src_dict)
        automation = ManagedAgentsAutomationResult.from_dict(d.pop("automation"))




        result = ManagedAgentsPullRequestReviewResult.from_dict(d.pop("result"))




        source = ManagedAgentsPullRequestReviewSource.from_dict(d.pop("source"))




        managed_agents_pull_request_review_result_response = cls(
            automation=automation,
            result=result,
            source=source,
        )


        managed_agents_pull_request_review_result_response.additional_properties = d
        return managed_agents_pull_request_review_result_response

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
