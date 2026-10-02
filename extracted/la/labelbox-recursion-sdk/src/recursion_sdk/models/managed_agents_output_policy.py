from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsOutputPolicy")



@_attrs_define
class ManagedAgentsOutputPolicy:
    """ What one repository automation run is allowed to produce. It is snapshotted onto the session at start, so a later
    edit to the trigger binding cannot change what an already-running automation does.

        Example:
            {'capture_patch': True, 'publish_review': True}

        Attributes:
            capture_patch (bool): Whether the run captures the agent's final working-tree patch as a transcript artifact.
            publish_review (bool): Whether the run publishes its validated result to the pull request as a GitHub review.
     """

    capture_patch: bool
    publish_review: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        capture_patch = self.capture_patch

        publish_review = self.publish_review


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "capture_patch": capture_patch,
            "publish_review": publish_review,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        capture_patch = d.pop("capture_patch")

        publish_review = d.pop("publish_review")

        managed_agents_output_policy = cls(
            capture_patch=capture_patch,
            publish_review=publish_review,
        )


        managed_agents_output_policy.additional_properties = d
        return managed_agents_output_policy

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
