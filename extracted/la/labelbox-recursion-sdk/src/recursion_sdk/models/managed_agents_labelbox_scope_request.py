from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_labelbox_scope_request_mode import ManagedAgentsLabelboxScopeRequestMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_labelbox_audience_request import ManagedAgentsLabelboxAudienceRequest





T = TypeVar("T", bound="ManagedAgentsLabelboxScopeRequest")



@_attrs_define
class ManagedAgentsLabelboxScopeRequest:
    """ Labelbox product-state authorization ceiling. Projects mode permits one exact project set. Organization mode permits
    organization-wide access, optionally pinned to one exact Slack binding whose internal or Slack Connect
    classification is explicit. The organization always equals the credential's owner.

        Example:
            {'mode': 'projects', 'project_ids': ['project-id']}

        Attributes:
            audience (ManagedAgentsLabelboxAudienceRequest | Unset): Exact Slack trigger binding authorized to use an
                organization-wide Labelbox product-state credential, with an explicit internal or Slack Connect classification.
                Example: {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind':
                'internal_slack_binding'}.
            mode (ManagedAgentsLabelboxScopeRequestMode | Unset): Scope mode. Omit for the backward-compatible projects
                mode.
            organization_id (str | Unset): Labelbox organization the projects belong to. Optional: filled in from the
                organization that owns the credential, and rejected if it names any other.
            project_ids (list[str] | Unset): Projects mode requires exactly 1 to 100 project ids. Forbidden in organization
                mode.
     """

    audience: ManagedAgentsLabelboxAudienceRequest | Unset = UNSET
    mode: ManagedAgentsLabelboxScopeRequestMode | Unset = UNSET
    organization_id: str | Unset = UNSET
    project_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_labelbox_audience_request import ManagedAgentsLabelboxAudienceRequest # noqa: PLC0415
        audience: dict[str, Any] | Unset = UNSET
        if not isinstance(self.audience, Unset):
            audience = self.audience.to_dict()

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value


        organization_id = self.organization_id

        project_ids: list[str] | Unset = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if audience is not UNSET:
            field_dict["audience"] = audience
        if mode is not UNSET:
            field_dict["mode"] = mode
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if project_ids is not UNSET:
            field_dict["project_ids"] = project_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_labelbox_audience_request import ManagedAgentsLabelboxAudienceRequest # noqa: PLC0415
        d = dict(src_dict)
        _audience = d.pop("audience", UNSET)
        audience: ManagedAgentsLabelboxAudienceRequest | Unset
        if isinstance(_audience,  Unset):
            audience = UNSET
        else:
            audience = ManagedAgentsLabelboxAudienceRequest.from_dict(_audience)




        _mode = d.pop("mode", UNSET)
        mode: ManagedAgentsLabelboxScopeRequestMode | Unset
        if isinstance(_mode,  Unset):
            mode = UNSET
        else:
            mode = ManagedAgentsLabelboxScopeRequestMode(_mode)




        organization_id = d.pop("organization_id", UNSET)

        project_ids = cast(list[str], d.pop("project_ids", UNSET))


        managed_agents_labelbox_scope_request = cls(
            audience=audience,
            mode=mode,
            organization_id=organization_id,
            project_ids=project_ids,
        )


        managed_agents_labelbox_scope_request.additional_properties = d
        return managed_agents_labelbox_scope_request

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
