from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.interactive_script_type import InteractiveScriptType
from ..models.script_type import ScriptType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateScriptRequest")


@_attrs_define
class CreateScriptRequest:
    """
    Attributes:
        description (str): The description of the script
        entry_point (str): The entry point of the script. Will usually be the path to a python file in the uploaded
            tarball
        name (str): The name of the script
        script_type (ScriptType): The type of the script. Use 'batch' for batch pipelines and 'interactive' for
            notebooks
        interactive_script_type (Union[InteractiveScriptType, None, Unset]): The type of interactive script. Use
            'marimo' for marimo notebook, 'mcp' for MCPs and 'streamlit' for streamlit reports.
        profile (Union[None, Unset, str]): The name of the profile to use for the script
        schedule (Union[None, Unset, str]): The schedule of the script. Use 'cron' format for cron jobs
    """

    description: str
    entry_point: str
    name: str
    script_type: ScriptType
    interactive_script_type: Union[InteractiveScriptType, None, Unset] = UNSET
    profile: Union[None, Unset, str] = UNSET
    schedule: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        entry_point = self.entry_point

        name = self.name

        script_type = self.script_type.value

        interactive_script_type: Union[None, Unset, str]
        if isinstance(self.interactive_script_type, Unset):
            interactive_script_type = UNSET
        elif isinstance(self.interactive_script_type, InteractiveScriptType):
            interactive_script_type = self.interactive_script_type.value
        else:
            interactive_script_type = self.interactive_script_type

        profile: Union[None, Unset, str]
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        schedule: Union[None, Unset, str]
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        else:
            schedule = self.schedule

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "entry_point": entry_point,
                "name": name,
                "script_type": script_type,
            }
        )
        if interactive_script_type is not UNSET:
            field_dict["interactive_script_type"] = interactive_script_type
        if profile is not UNSET:
            field_dict["profile"] = profile
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        entry_point = d.pop("entry_point")

        name = d.pop("name")

        script_type = ScriptType(d.pop("script_type"))

        def _parse_interactive_script_type(
            data: object,
        ) -> Union[InteractiveScriptType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                interactive_script_type_type_0 = InteractiveScriptType(data)

                return interactive_script_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[InteractiveScriptType, None, Unset], data)

        interactive_script_type = _parse_interactive_script_type(
            d.pop("interactive_script_type", UNSET)
        )

        def _parse_profile(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile = _parse_profile(d.pop("profile", UNSET))

        def _parse_schedule(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        create_script_request = cls(
            description=description,
            entry_point=entry_point,
            name=name,
            script_type=script_type,
            interactive_script_type=interactive_script_type,
            profile=profile,
            schedule=schedule,
        )

        create_script_request.additional_properties = d
        return create_script_request

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
