from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.share_ai_artifact_json_body_kind import ShareAiArtifactJsonBodyKind

T = TypeVar("T", bound="ShareAiArtifactJsonBody")


@_attrs_define
class ShareAiArtifactJsonBody:
    """
    Attributes:
        artifact_id (str): the artifact's id in the author's session
        name (str):
        kind (ShareAiArtifactJsonBodyKind):
        version (int):
        content (str):
    """

    artifact_id: str
    name: str
    kind: ShareAiArtifactJsonBodyKind
    version: int
    content: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        artifact_id = self.artifact_id
        name = self.name
        kind = self.kind.value

        version = self.version
        content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "artifact_id": artifact_id,
                "name": name,
                "kind": kind,
                "version": version,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        artifact_id = d.pop("artifact_id")

        name = d.pop("name")

        kind = ShareAiArtifactJsonBodyKind(d.pop("kind"))

        version = d.pop("version")

        content = d.pop("content")

        share_ai_artifact_json_body = cls(
            artifact_id=artifact_id,
            name=name,
            kind=kind,
            version=version,
            content=content,
        )

        share_ai_artifact_json_body.additional_properties = d
        return share_ai_artifact_json_body

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
