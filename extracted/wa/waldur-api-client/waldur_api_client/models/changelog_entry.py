from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action import Action
    from ..models.changelog_entry_plugin_analysis import ChangelogEntryPluginAnalysis
    from ..models.changelog_entry_settings_analysis import ChangelogEntrySettingsAnalysis
    from ..models.impact import Impact
    from ..models.relevant_when import RelevantWhen
    from ..models.security_detail import SecurityDetail


T = TypeVar("T", bound="ChangelogEntry")


@_attrs_define
class ChangelogEntry:
    """
    Attributes:
        id (str):
        type_ (str):
        category (str):
        title (str):
        description (str):
        scope (str):
        component (list[str]):
        impact (Impact):
        highlight (Union[Unset, bool]):  Default: False.
        security (Union['SecurityDetail', None, Unset]):
        actions (Union[Unset, list['Action']]):
        relevant_when (Union[Unset, RelevantWhen]):
        relevant (Union[Unset, bool]):
        relevance_reasons (Union[Unset, list[str]]):
        affected_resources_count (Union[Unset, int]):
        affected_users_count (Union[Unset, int]):
        settings_analysis (Union[Unset, ChangelogEntrySettingsAnalysis]):
        plugin_analysis (Union[Unset, ChangelogEntryPluginAnalysis]):
    """

    id: str
    type_: str
    category: str
    title: str
    description: str
    scope: str
    component: list[str]
    impact: "Impact"
    highlight: Union[Unset, bool] = False
    security: Union["SecurityDetail", None, Unset] = UNSET
    actions: Union[Unset, list["Action"]] = UNSET
    relevant_when: Union[Unset, "RelevantWhen"] = UNSET
    relevant: Union[Unset, bool] = UNSET
    relevance_reasons: Union[Unset, list[str]] = UNSET
    affected_resources_count: Union[Unset, int] = UNSET
    affected_users_count: Union[Unset, int] = UNSET
    settings_analysis: Union[Unset, "ChangelogEntrySettingsAnalysis"] = UNSET
    plugin_analysis: Union[Unset, "ChangelogEntryPluginAnalysis"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.security_detail import SecurityDetail

        id = self.id

        type_ = self.type_

        category = self.category

        title = self.title

        description = self.description

        scope = self.scope

        component = self.component

        impact = self.impact.to_dict()

        highlight = self.highlight

        security: Union[None, Unset, dict[str, Any]]
        if isinstance(self.security, Unset):
            security = UNSET
        elif isinstance(self.security, SecurityDetail):
            security = self.security.to_dict()
        else:
            security = self.security

        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        relevant_when: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.relevant_when, Unset):
            relevant_when = self.relevant_when.to_dict()

        relevant = self.relevant

        relevance_reasons: Union[Unset, list[str]] = UNSET
        if not isinstance(self.relevance_reasons, Unset):
            relevance_reasons = self.relevance_reasons

        affected_resources_count = self.affected_resources_count

        affected_users_count = self.affected_users_count

        settings_analysis: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings_analysis, Unset):
            settings_analysis = self.settings_analysis.to_dict()

        plugin_analysis: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plugin_analysis, Unset):
            plugin_analysis = self.plugin_analysis.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "category": category,
                "title": title,
                "description": description,
                "scope": scope,
                "component": component,
                "impact": impact,
            }
        )
        if highlight is not UNSET:
            field_dict["highlight"] = highlight
        if security is not UNSET:
            field_dict["security"] = security
        if actions is not UNSET:
            field_dict["actions"] = actions
        if relevant_when is not UNSET:
            field_dict["relevant_when"] = relevant_when
        if relevant is not UNSET:
            field_dict["relevant"] = relevant
        if relevance_reasons is not UNSET:
            field_dict["relevance_reasons"] = relevance_reasons
        if affected_resources_count is not UNSET:
            field_dict["affected_resources_count"] = affected_resources_count
        if affected_users_count is not UNSET:
            field_dict["affected_users_count"] = affected_users_count
        if settings_analysis is not UNSET:
            field_dict["settings_analysis"] = settings_analysis
        if plugin_analysis is not UNSET:
            field_dict["plugin_analysis"] = plugin_analysis

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action import Action
        from ..models.changelog_entry_plugin_analysis import ChangelogEntryPluginAnalysis
        from ..models.changelog_entry_settings_analysis import ChangelogEntrySettingsAnalysis
        from ..models.impact import Impact
        from ..models.relevant_when import RelevantWhen
        from ..models.security_detail import SecurityDetail

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        category = d.pop("category")

        title = d.pop("title")

        description = d.pop("description")

        scope = d.pop("scope")

        component = cast(list[str], d.pop("component"))

        impact = Impact.from_dict(d.pop("impact"))

        highlight = d.pop("highlight", UNSET)

        def _parse_security(data: object) -> Union["SecurityDetail", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                security_type_1 = SecurityDetail.from_dict(data)

                return security_type_1
            except:  # noqa: E722
                pass
            return cast(Union["SecurityDetail", None, Unset], data)

        security = _parse_security(d.pop("security", UNSET))

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = Action.from_dict(actions_item_data)

            actions.append(actions_item)

        _relevant_when = d.pop("relevant_when", UNSET)
        relevant_when: Union[Unset, RelevantWhen]
        if isinstance(_relevant_when, Unset):
            relevant_when = UNSET
        else:
            relevant_when = RelevantWhen.from_dict(_relevant_when)

        relevant = d.pop("relevant", UNSET)

        relevance_reasons = cast(list[str], d.pop("relevance_reasons", UNSET))

        affected_resources_count = d.pop("affected_resources_count", UNSET)

        affected_users_count = d.pop("affected_users_count", UNSET)

        _settings_analysis = d.pop("settings_analysis", UNSET)
        settings_analysis: Union[Unset, ChangelogEntrySettingsAnalysis]
        if isinstance(_settings_analysis, Unset):
            settings_analysis = UNSET
        else:
            settings_analysis = ChangelogEntrySettingsAnalysis.from_dict(_settings_analysis)

        _plugin_analysis = d.pop("plugin_analysis", UNSET)
        plugin_analysis: Union[Unset, ChangelogEntryPluginAnalysis]
        if isinstance(_plugin_analysis, Unset):
            plugin_analysis = UNSET
        else:
            plugin_analysis = ChangelogEntryPluginAnalysis.from_dict(_plugin_analysis)

        changelog_entry = cls(
            id=id,
            type_=type_,
            category=category,
            title=title,
            description=description,
            scope=scope,
            component=component,
            impact=impact,
            highlight=highlight,
            security=security,
            actions=actions,
            relevant_when=relevant_when,
            relevant=relevant,
            relevance_reasons=relevance_reasons,
            affected_resources_count=affected_resources_count,
            affected_users_count=affected_users_count,
            settings_analysis=settings_analysis,
            plugin_analysis=plugin_analysis,
        )

        changelog_entry.additional_properties = d
        return changelog_entry

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
