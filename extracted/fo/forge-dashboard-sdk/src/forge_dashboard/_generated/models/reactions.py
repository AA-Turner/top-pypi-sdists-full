from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.reaction import Reaction





T = TypeVar("T", bound="Reactions")



@_attrs_define
class Reactions:
    """ The two reactions the dialog shows, `+1` and `-1` on both forges.

        Attributes:
            thumbs_up (Reaction):
            thumbs_down (Reaction):
     """

    thumbs_up: Reaction
    thumbs_down: Reaction
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.reaction import Reaction # noqa: PLC0415
        thumbs_up = self.thumbs_up.to_dict()

        thumbs_down = self.thumbs_down.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "thumbsUp": thumbs_up,
            "thumbsDown": thumbs_down,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reaction import Reaction # noqa: PLC0415
        d = dict(src_dict)
        thumbs_up = Reaction.from_dict(d.pop("thumbsUp"))




        thumbs_down = Reaction.from_dict(d.pop("thumbsDown"))




        reactions = cls(
            thumbs_up=thumbs_up,
            thumbs_down=thumbs_down,
        )


        reactions.additional_properties = d
        return reactions

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
