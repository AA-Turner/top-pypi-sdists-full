from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SkillResponseDto")



@_attrs_define
class SkillResponseDto:
    """ A Claude skill's markdown content plus its content-hash version.

        Example:
            {'name': 'recursion', 'version': '74093fc920beab757cae8154b37148dc8867d281db6e32609fcae5a6dd4aedf8', 'content':
                '---\\nname: recursion\\ndescription: Operate the Recursion Platform from the command line.\\nallowed-tools:
                Bash, Read, Write\\nskill-version: 74093fc920beab757cae8154b37148dc8867d281db6e32609fcae5a6dd4aedf8\\n---\\n\\n
                # Recursion\\n\\nOperate the Recursion Platform through its command-line interface.\\n'}

        Attributes:
            name (str): Skill name (filename stem), e.g. "recursion".
            version (str): Content hash (sha256 hex) of the authored skill markdown. Staleness is a plain string compare
                against this value.
            content (str): The full skill markdown, with a `skill-version:` line injected into its frontmatter so the
                downloaded file is self-describing.
     """

    name: str
    version: str
    content: str





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        content = self.content


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
            "version": version,
            "content": content,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        content = d.pop("content")

        skill_response_dto = cls(
            name=name,
            version=version,
            content=content,
        )

        return skill_response_dto

