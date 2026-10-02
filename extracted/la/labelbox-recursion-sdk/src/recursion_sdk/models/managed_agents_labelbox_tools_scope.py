from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_labelbox_tools_scope_mode import ManagedAgentsLabelboxToolsScopeMode
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_labelbox_tools_audience import ManagedAgentsLabelboxToolsAudience





T = TypeVar("T", bound="ManagedAgentsLabelboxToolsScope")



@_attrs_define
class ManagedAgentsLabelboxToolsScope:
    """ Labelbox product-state authorization ceiling. The organization always equals the credential's owner. Projects mode
    permits one exact project set; organization mode permits organization-wide reads only from one exact Slack binding
    whose internal or Slack Connect classification is explicit.

        Example:
            {'mode': 'projects', 'organization_id': 'organization-id', 'project_ids': ['project-id']}

        Attributes:
            organization_id (str): Labelbox organization the projects belong to. Must equal the organization that owns the
                credential; filled in from it when omitted on write.
            audience (ManagedAgentsLabelboxToolsAudience | Unset): Exact Slack trigger binding authorized to use an
                organization-wide Labelbox product-state credential, with an explicit internal or Slack Connect classification.
                Example: {'binding_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind':
                'internal_slack_binding'}.
            mode (ManagedAgentsLabelboxToolsScopeMode | Unset): Scope mode. Omitted legacy values are canonicalized to
                projects.
            project_ids (list[str] | Unset): Projects-mode ceiling: exactly 1 to 100 project ids, each up to 128 characters
                of letters, digits, hyphen, or underscore. Forbidden in organization mode; validated as unique and sorted on
                write.
     """

    organization_id: str
    audience: ManagedAgentsLabelboxToolsAudience | Unset = UNSET
    mode: ManagedAgentsLabelboxToolsScopeMode | Unset = UNSET
    project_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_labelbox_tools_audience import ManagedAgentsLabelboxToolsAudience # noqa: PLC0415
        organization_id = self.organization_id

        audience: dict[str, Any] | Unset = UNSET
        if not isinstance(self.audience, Unset):
            audience = self.audience.to_dict()

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value


        project_ids: list[str] | Unset = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "organization_id": organization_id,
        })
        if audience is not UNSET:
            field_dict["audience"] = audience
        if mode is not UNSET:
            field_dict["mode"] = mode
        if project_ids is not UNSET:
            field_dict["project_ids"] = project_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_labelbox_tools_audience import ManagedAgentsLabelboxToolsAudience # noqa: PLC0415
        d = dict(src_dict)
        organization_id = d.pop("organization_id")

        _audience = d.pop("audience", UNSET)
        audience: ManagedAgentsLabelboxToolsAudience | Unset
        if isinstance(_audience,  Unset):
            audience = UNSET
        else:
            audience = ManagedAgentsLabelboxToolsAudience.from_dict(_audience)




        _mode = d.pop("mode", UNSET)
        mode: ManagedAgentsLabelboxToolsScopeMode | Unset
        if isinstance(_mode,  Unset):
            mode = UNSET
        else:
            mode = ManagedAgentsLabelboxToolsScopeMode(_mode)




        project_ids = cast(list[str], d.pop("project_ids", UNSET))


        managed_agents_labelbox_tools_scope = cls(
            organization_id=organization_id,
            audience=audience,
            mode=mode,
            project_ids=project_ids,
        )


        managed_agents_labelbox_tools_scope.additional_properties = d
        return managed_agents_labelbox_tools_scope

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
