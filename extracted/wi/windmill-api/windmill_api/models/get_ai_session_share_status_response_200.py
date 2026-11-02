from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_ai_session_share_status_response_200_share import GetAiSessionShareStatusResponse200Share


T = TypeVar("T", bound="GetAiSessionShareStatusResponse200")


@_attrs_define
class GetAiSessionShareStatusResponse200:
    """
    Attributes:
        share (Union[Unset, GetAiSessionShareStatusResponse200Share]):
    """

    share: Union[Unset, "GetAiSessionShareStatusResponse200Share"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        share: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.share, Unset):
            share = self.share.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if share is not UNSET:
            field_dict["share"] = share

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_ai_session_share_status_response_200_share import GetAiSessionShareStatusResponse200Share

        d = src_dict.copy()
        _share = d.pop("share", UNSET)
        share: Union[Unset, GetAiSessionShareStatusResponse200Share]
        if isinstance(_share, Unset):
            share = UNSET
        else:
            share = GetAiSessionShareStatusResponse200Share.from_dict(_share)

        get_ai_session_share_status_response_200 = cls(
            share=share,
        )

        get_ai_session_share_status_response_200.additional_properties = d
        return get_ai_session_share_status_response_200

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
