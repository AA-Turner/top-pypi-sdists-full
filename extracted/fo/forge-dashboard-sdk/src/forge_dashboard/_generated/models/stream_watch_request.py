from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.check_subject import CheckSubject





T = TypeVar("T", bound="StreamWatchRequest")



@_attrs_define
class StreamWatchRequest:
    """ 
        Attributes:
            stream_id (str): The `sid` the stream was opened with.
            subjects (list[CheckSubject]):
            refresh (bool | Unset): List every subject again, including the ones already watched.
                A client sends it after an action that changes the jobs.
     """

    stream_id: str
    subjects: list[CheckSubject]
    refresh: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.check_subject import CheckSubject # noqa: PLC0415
        stream_id = self.stream_id

        subjects = []
        for subjects_item_data in self.subjects:
            subjects_item = subjects_item_data.to_dict()
            subjects.append(subjects_item)



        refresh = self.refresh


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "streamId": stream_id,
            "subjects": subjects,
        })
        if refresh is not UNSET:
            field_dict["refresh"] = refresh

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_subject import CheckSubject # noqa: PLC0415
        d = dict(src_dict)
        stream_id = d.pop("streamId")

        subjects = []
        _subjects = d.pop("subjects")
        for subjects_item_data in (_subjects):
            subjects_item = CheckSubject.from_dict(subjects_item_data)



            subjects.append(subjects_item)


        refresh = d.pop("refresh", UNSET)

        stream_watch_request = cls(
            stream_id=stream_id,
            subjects=subjects,
            refresh=refresh,
        )


        stream_watch_request.additional_properties = d
        return stream_watch_request

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
