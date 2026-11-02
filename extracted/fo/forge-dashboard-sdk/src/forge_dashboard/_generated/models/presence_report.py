from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PresenceReport")



@_attrs_define
class PresenceReport:
    """ 
        Attributes:
            viewer_id (str): Names one browser tab, chosen by the page when it loads. Not a
                user id and not stored beyond the tab's heartbeats.
            visible (bool): True while the tab is visible and has had input recently. False
                once it is hidden or the person has stopped using it.
     """

    viewer_id: str
    visible: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        viewer_id = self.viewer_id

        visible = self.visible


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "viewerId": viewer_id,
            "visible": visible,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        viewer_id = d.pop("viewerId")

        visible = d.pop("visible")

        presence_report = cls(
            viewer_id=viewer_id,
            visible=visible,
        )


        presence_report.additional_properties = d
        return presence_report

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
