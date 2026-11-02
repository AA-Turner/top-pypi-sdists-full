from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pipeline_recording_body_recording import PipelineRecordingBodyRecording


T = TypeVar("T", bound="PipelineRecordingBody")


@_attrs_define
class PipelineRecordingBody:
    """
    Attributes:
        recording (Union[Unset, PipelineRecordingBodyRecording]):
    """

    recording: Union[Unset, "PipelineRecordingBodyRecording"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        recording: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recording, Unset):
            recording = self.recording.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if recording is not UNSET:
            field_dict["recording"] = recording

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pipeline_recording_body_recording import PipelineRecordingBodyRecording

        d = src_dict.copy()
        _recording = d.pop("recording", UNSET)
        recording: Union[Unset, PipelineRecordingBodyRecording]
        if isinstance(_recording, Unset):
            recording = UNSET
        else:
            recording = PipelineRecordingBodyRecording.from_dict(_recording)

        pipeline_recording_body = cls(
            recording=recording,
        )

        pipeline_recording_body.additional_properties = d
        return pipeline_recording_body

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
