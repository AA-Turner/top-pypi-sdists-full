import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sram_project_rule_field import SramProjectRuleField
from ..models.sram_project_rule_match import SramProjectRuleMatch
from ..models.sram_project_rule_source_kind import SramProjectRuleSourceKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="SramProjectRule")


@_attrs_define
class SramProjectRule:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        project_role (UUID):
        project_role_name (str):
        project_role_description (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        is_active (Union[Unset, bool]):
        source_kind (Union[Unset, SramProjectRuleSourceKind]):
        labels (Union[Unset, list[str]]):
        group_short_name_patterns (Union[Unset, list[str]]):
        project_field (Union[Unset, SramProjectRuleField]):
        project_match (Union[Unset, SramProjectRuleMatch]):
        project_pattern (Union[Unset, str]): Placeholders: {co_external_id}, {co_identifier}, {co_short_name},
            {org_short_name}, {group_short_name}.
    """

    url: str
    uuid: UUID
    name: str
    project_role: UUID
    project_role_name: str
    project_role_description: str
    created: datetime.datetime
    modified: datetime.datetime
    is_active: Union[Unset, bool] = UNSET
    source_kind: Union[Unset, SramProjectRuleSourceKind] = UNSET
    labels: Union[Unset, list[str]] = UNSET
    group_short_name_patterns: Union[Unset, list[str]] = UNSET
    project_field: Union[Unset, SramProjectRuleField] = UNSET
    project_match: Union[Unset, SramProjectRuleMatch] = UNSET
    project_pattern: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        project_role = str(self.project_role)

        project_role_name = self.project_role_name

        project_role_description = self.project_role_description

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        is_active = self.is_active

        source_kind: Union[Unset, str] = UNSET
        if not isinstance(self.source_kind, Unset):
            source_kind = self.source_kind.value

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        group_short_name_patterns: Union[Unset, list[str]] = UNSET
        if not isinstance(self.group_short_name_patterns, Unset):
            group_short_name_patterns = self.group_short_name_patterns

        project_field: Union[Unset, str] = UNSET
        if not isinstance(self.project_field, Unset):
            project_field = self.project_field.value

        project_match: Union[Unset, str] = UNSET
        if not isinstance(self.project_match, Unset):
            project_match = self.project_match.value

        project_pattern = self.project_pattern

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "project_role": project_role,
                "project_role_name": project_role_name,
                "project_role_description": project_role_description,
                "created": created,
                "modified": modified,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if source_kind is not UNSET:
            field_dict["source_kind"] = source_kind
        if labels is not UNSET:
            field_dict["labels"] = labels
        if group_short_name_patterns is not UNSET:
            field_dict["group_short_name_patterns"] = group_short_name_patterns
        if project_field is not UNSET:
            field_dict["project_field"] = project_field
        if project_match is not UNSET:
            field_dict["project_match"] = project_match
        if project_pattern is not UNSET:
            field_dict["project_pattern"] = project_pattern

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        project_role = UUID(d.pop("project_role"))

        project_role_name = d.pop("project_role_name")

        project_role_description = d.pop("project_role_description")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        is_active = d.pop("is_active", UNSET)

        _source_kind = d.pop("source_kind", UNSET)
        source_kind: Union[Unset, SramProjectRuleSourceKind]
        if isinstance(_source_kind, Unset):
            source_kind = UNSET
        else:
            source_kind = SramProjectRuleSourceKind(_source_kind)

        labels = cast(list[str], d.pop("labels", UNSET))

        group_short_name_patterns = cast(list[str], d.pop("group_short_name_patterns", UNSET))

        _project_field = d.pop("project_field", UNSET)
        project_field: Union[Unset, SramProjectRuleField]
        if isinstance(_project_field, Unset):
            project_field = UNSET
        else:
            project_field = SramProjectRuleField(_project_field)

        _project_match = d.pop("project_match", UNSET)
        project_match: Union[Unset, SramProjectRuleMatch]
        if isinstance(_project_match, Unset):
            project_match = UNSET
        else:
            project_match = SramProjectRuleMatch(_project_match)

        project_pattern = d.pop("project_pattern", UNSET)

        sram_project_rule = cls(
            url=url,
            uuid=uuid,
            name=name,
            project_role=project_role,
            project_role_name=project_role_name,
            project_role_description=project_role_description,
            created=created,
            modified=modified,
            is_active=is_active,
            source_kind=source_kind,
            labels=labels,
            group_short_name_patterns=group_short_name_patterns,
            project_field=project_field,
            project_match=project_match,
            project_pattern=project_pattern,
        )

        sram_project_rule.additional_properties = d
        return sram_project_rule

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
