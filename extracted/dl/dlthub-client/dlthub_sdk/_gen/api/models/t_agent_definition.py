from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TAgentDefinition")


@_attrs_define
class TAgentDefinition:
    """
    Attributes:
        engine_version (int):
        name (str):
        agent_file (str | Unset):
        description (str | Unset):
        instructions (str | Unset):
        model (str | Unset):
        rules (list[str] | Unset):
        skills (list[str] | Unset):
        tools (list[str] | Unset):
    """

    engine_version: int
    name: str
    agent_file: str | Unset = UNSET
    description: str | Unset = UNSET
    instructions: str | Unset = UNSET
    model: str | Unset = UNSET
    rules: list[str] | Unset = UNSET
    skills: list[str] | Unset = UNSET
    tools: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine_version = self.engine_version

        name = self.name

        agent_file = self.agent_file

        description = self.description

        instructions = self.instructions

        model = self.model

        rules: list[str] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules

        skills: list[str] | Unset = UNSET
        if not isinstance(self.skills, Unset):
            skills = self.skills

        tools: list[str] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engine_version": engine_version,
                "name": name,
            }
        )
        if agent_file is not UNSET:
            field_dict["agent_file"] = agent_file
        if description is not UNSET:
            field_dict["description"] = description
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if model is not UNSET:
            field_dict["model"] = model
        if rules is not UNSET:
            field_dict["rules"] = rules
        if skills is not UNSET:
            field_dict["skills"] = skills
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        engine_version = d.pop("engine_version")

        name = d.pop("name")

        agent_file = d.pop("agent_file", UNSET)

        description = d.pop("description", UNSET)

        instructions = d.pop("instructions", UNSET)

        model = d.pop("model", UNSET)

        rules = cast(list[str], d.pop("rules", UNSET))

        skills = cast(list[str], d.pop("skills", UNSET))

        tools = cast(list[str], d.pop("tools", UNSET))

        t_agent_definition = cls(
            engine_version=engine_version,
            name=name,
            agent_file=agent_file,
            description=description,
            instructions=instructions,
            model=model,
            rules=rules,
            skills=skills,
            tools=tools,
        )

        t_agent_definition.additional_properties = d
        return t_agent_definition

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
