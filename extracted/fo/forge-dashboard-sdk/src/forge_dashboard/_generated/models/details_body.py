from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.details_body_format import DetailsBodyFormat
from typing import cast

if TYPE_CHECKING:
  from ..models.reactions import Reactions





T = TypeVar("T", bound="DetailsBody")



@_attrs_define
class DetailsBody:
    """ A pull request's description, or the release notes of a release pull request.

        Attributes:
            text (str): The text as the forge stores it, cut at 20,000 characters. Markdown,
                not converted or sanitised: render it with raw HTML disabled.
            format_ (DetailsBodyFormat): How `text` is written. Only markdown today; a later format is additive.
            truncated (bool): True when `text` was cut at 20,000 characters.
            edited (bool): True when the forge says the text was edited after it was posted.
            reactions (Reactions): The two reactions the dialog shows, `+1` and `-1` on both forges.
     """

    text: str
    format_: DetailsBodyFormat
    truncated: bool
    edited: bool
    reactions: Reactions
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.reactions import Reactions # noqa: PLC0415
        text = self.text

        format_ = self.format_.value

        truncated = self.truncated

        edited = self.edited

        reactions = self.reactions.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "text": text,
            "format": format_,
            "truncated": truncated,
            "edited": edited,
            "reactions": reactions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reactions import Reactions # noqa: PLC0415
        d = dict(src_dict)
        text = d.pop("text")

        format_ = DetailsBodyFormat(d.pop("format"))




        truncated = d.pop("truncated")

        edited = d.pop("edited")

        reactions = Reactions.from_dict(d.pop("reactions"))




        details_body = cls(
            text=text,
            format_=format_,
            truncated=truncated,
            edited=edited,
            reactions=reactions,
        )


        details_body.additional_properties = d
        return details_body

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
