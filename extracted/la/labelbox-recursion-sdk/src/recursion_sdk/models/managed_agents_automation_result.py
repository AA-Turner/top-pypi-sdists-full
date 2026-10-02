from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_patch_artifact import ManagedAgentsPatchArtifact
  from ..models.managed_agents_publication import ManagedAgentsPublication





T = TypeVar("T", bound="ManagedAgentsAutomationResult")



@_attrs_define
class ManagedAgentsAutomationResult:
    """ The trusted side effects one repository automation performed after its result passed validation: the patch it
    captured and the review it published. A session that completed before output finalization existed reads back zero-
    valued, meaning neither happened.

        Example:
            {'patch': {'byte_size': 1, 'changed': True, 'event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'patch_sha256':
                'example'}, 'publication': {'published': True, 'review_id': 1, 'url': 'https://example.com'}}

        Attributes:
            patch (ManagedAgentsPatchArtifact): Metadata for the working-tree patch captured from a repository automation.
                Only the digest and size are recorded on the result; the patch body itself is a transcript artifact event
                addressed by event_id. Example: {'byte_size': 1, 'changed': True, 'event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'patch_sha256': 'example'}.
            publication (ManagedAgentsPublication): The GitHub-side outcome of one repository automation. Publication is
                idempotent: a retry finds the review this session already posted and returns it rather than duplicating
                comments. Example: {'published': True, 'review_id': 1, 'url': 'https://example.com'}.
     """

    patch: ManagedAgentsPatchArtifact
    publication: ManagedAgentsPublication
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_patch_artifact import ManagedAgentsPatchArtifact # noqa: PLC0415
        from ..models.managed_agents_publication import ManagedAgentsPublication # noqa: PLC0415
        patch = self.patch.to_dict()

        publication = self.publication.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "patch": patch,
            "publication": publication,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_patch_artifact import ManagedAgentsPatchArtifact # noqa: PLC0415
        from ..models.managed_agents_publication import ManagedAgentsPublication # noqa: PLC0415
        d = dict(src_dict)
        patch = ManagedAgentsPatchArtifact.from_dict(d.pop("patch"))




        publication = ManagedAgentsPublication.from_dict(d.pop("publication"))




        managed_agents_automation_result = cls(
            patch=patch,
            publication=publication,
        )


        managed_agents_automation_result.additional_properties = d
        return managed_agents_automation_result

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
