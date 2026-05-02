from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offboard_preview_owned_triggers import OffboardPreviewOwnedTriggers


T = TypeVar("T", bound="OffboardPreviewOwned")


@_attrs_define
class OffboardPreviewOwned:
    """Objects under u/{username}/ that will be reassigned

    Attributes:
        scripts (Union[Unset, List[str]]):
        flows (Union[Unset, List[str]]):
        apps (Union[Unset, List[str]]):
        resources (Union[Unset, List[str]]):
        variables (Union[Unset, List[str]]):
        schedules (Union[Unset, List[str]]):
        triggers (Union[Unset, OffboardPreviewOwnedTriggers]):
    """

    scripts: Union[Unset, List[str]] = UNSET
    flows: Union[Unset, List[str]] = UNSET
    apps: Union[Unset, List[str]] = UNSET
    resources: Union[Unset, List[str]] = UNSET
    variables: Union[Unset, List[str]] = UNSET
    schedules: Union[Unset, List[str]] = UNSET
    triggers: Union[Unset, "OffboardPreviewOwnedTriggers"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        scripts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scripts, Unset):
            scripts = self.scripts

        flows: Union[Unset, List[str]] = UNSET
        if not isinstance(self.flows, Unset):
            flows = self.flows

        apps: Union[Unset, List[str]] = UNSET
        if not isinstance(self.apps, Unset):
            apps = self.apps

        resources: Union[Unset, List[str]] = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources

        variables: Union[Unset, List[str]] = UNSET
        if not isinstance(self.variables, Unset):
            variables = self.variables

        schedules: Union[Unset, List[str]] = UNSET
        if not isinstance(self.schedules, Unset):
            schedules = self.schedules

        triggers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = self.triggers.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scripts is not UNSET:
            field_dict["scripts"] = scripts
        if flows is not UNSET:
            field_dict["flows"] = flows
        if apps is not UNSET:
            field_dict["apps"] = apps
        if resources is not UNSET:
            field_dict["resources"] = resources
        if variables is not UNSET:
            field_dict["variables"] = variables
        if schedules is not UNSET:
            field_dict["schedules"] = schedules
        if triggers is not UNSET:
            field_dict["triggers"] = triggers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.offboard_preview_owned_triggers import OffboardPreviewOwnedTriggers

        d = src_dict.copy()
        scripts = cast(List[str], d.pop("scripts", UNSET))

        flows = cast(List[str], d.pop("flows", UNSET))

        apps = cast(List[str], d.pop("apps", UNSET))

        resources = cast(List[str], d.pop("resources", UNSET))

        variables = cast(List[str], d.pop("variables", UNSET))

        schedules = cast(List[str], d.pop("schedules", UNSET))

        _triggers = d.pop("triggers", UNSET)
        triggers: Union[Unset, OffboardPreviewOwnedTriggers]
        if isinstance(_triggers, Unset):
            triggers = UNSET
        else:
            triggers = OffboardPreviewOwnedTriggers.from_dict(_triggers)

        offboard_preview_owned = cls(
            scripts=scripts,
            flows=flows,
            apps=apps,
            resources=resources,
            variables=variables,
            schedules=schedules,
            triggers=triggers,
        )

        offboard_preview_owned.additional_properties = d
        return offboard_preview_owned

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
