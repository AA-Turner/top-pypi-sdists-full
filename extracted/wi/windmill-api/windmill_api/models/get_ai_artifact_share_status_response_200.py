from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_ai_artifact_share_status_response_200_share import GetAiArtifactShareStatusResponse200Share


T = TypeVar("T", bound="GetAiArtifactShareStatusResponse200")


@_attrs_define
class GetAiArtifactShareStatusResponse200:
    """
    Attributes:
        retention_secs (int):
        share (Union[Unset, GetAiArtifactShareStatusResponse200Share]):
    """

    retention_secs: int
    share: Union[Unset, "GetAiArtifactShareStatusResponse200Share"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        retention_secs = self.retention_secs
        share: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.share, Unset):
            share = self.share.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "retention_secs": retention_secs,
            }
        )
        if share is not UNSET:
            field_dict["share"] = share

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_ai_artifact_share_status_response_200_share import GetAiArtifactShareStatusResponse200Share

        d = src_dict.copy()
        retention_secs = d.pop("retention_secs")

        _share = d.pop("share", UNSET)
        share: Union[Unset, GetAiArtifactShareStatusResponse200Share]
        if isinstance(_share, Unset):
            share = UNSET
        else:
            share = GetAiArtifactShareStatusResponse200Share.from_dict(_share)

        get_ai_artifact_share_status_response_200 = cls(
            retention_secs=retention_secs,
            share=share,
        )

        get_ai_artifact_share_status_response_200.additional_properties = d
        return get_ai_artifact_share_status_response_200

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
