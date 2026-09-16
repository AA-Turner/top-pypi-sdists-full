import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.share_ai_artifact_response_200_kind import ShareAiArtifactResponse200Kind

T = TypeVar("T", bound="ShareAiArtifactResponse200")


@_attrs_define
class ShareAiArtifactResponse200:
    """
    Attributes:
        id (str):
        name (str):
        kind (ShareAiArtifactResponse200Kind):
        version (int):
        created_by (str):
        shared_at (datetime.datetime):
        expires_at (datetime.datetime):
    """

    id: str
    name: str
    kind: ShareAiArtifactResponse200Kind
    version: int
    created_by: str
    shared_at: datetime.datetime
    expires_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        kind = self.kind.value

        version = self.version
        created_by = self.created_by
        shared_at = self.shared_at.isoformat()

        expires_at = self.expires_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "kind": kind,
                "version": version,
                "created_by": created_by,
                "shared_at": shared_at,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        kind = ShareAiArtifactResponse200Kind(d.pop("kind"))

        version = d.pop("version")

        created_by = d.pop("created_by")

        shared_at = isoparse(d.pop("shared_at"))

        expires_at = isoparse(d.pop("expires_at"))

        share_ai_artifact_response_200 = cls(
            id=id,
            name=name,
            kind=kind,
            version=version,
            created_by=created_by,
            shared_at=shared_at,
            expires_at=expires_at,
        )

        share_ai_artifact_response_200.additional_properties = d
        return share_ai_artifact_response_200

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
