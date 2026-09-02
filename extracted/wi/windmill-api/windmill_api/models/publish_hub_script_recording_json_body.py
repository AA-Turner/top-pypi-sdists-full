from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_hub_script_recording_json_body_recording import PublishHubScriptRecordingJsonBodyRecording


T = TypeVar("T", bound="PublishHubScriptRecordingJsonBody")


@_attrs_define
class PublishHubScriptRecordingJsonBody:
    """
    Attributes:
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
        recording (Union[Unset, PublishHubScriptRecordingJsonBodyRecording]):
    """

    project_slug: str
    recording: Union[Unset, "PublishHubScriptRecordingJsonBodyRecording"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_slug = self.project_slug
        recording: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recording, Unset):
            recording = self.recording.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_slug": project_slug,
            }
        )
        if recording is not UNSET:
            field_dict["recording"] = recording

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_hub_script_recording_json_body_recording import PublishHubScriptRecordingJsonBodyRecording

        d = src_dict.copy()
        project_slug = d.pop("project_slug")

        _recording = d.pop("recording", UNSET)
        recording: Union[Unset, PublishHubScriptRecordingJsonBodyRecording]
        if isinstance(_recording, Unset):
            recording = UNSET
        else:
            recording = PublishHubScriptRecordingJsonBodyRecording.from_dict(_recording)

        publish_hub_script_recording_json_body = cls(
            project_slug=project_slug,
            recording=recording,
        )

        publish_hub_script_recording_json_body.additional_properties = d
        return publish_hub_script_recording_json_body

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
