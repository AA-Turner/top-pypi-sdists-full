import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_by_path_with_draft_response_200_draft import GetFlowByPathWithDraftResponse200Draft


T = TypeVar("T", bound="GetFlowByPathWithDraftResponse200")


@_attrs_define
class GetFlowByPathWithDraftResponse200:
    """
    Attributes:
        draft (Union[Unset, GetFlowByPathWithDraftResponse200Draft]):
        draft_created_at (Union[Unset, datetime.datetime]): Timestamp at which the most recent DB draft was created.
            Used by the frontend's UserDraft staleness check.
    """

    draft: Union[Unset, "GetFlowByPathWithDraftResponse200Draft"] = UNSET
    draft_created_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        draft_created_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_created_at, Unset):
            draft_created_at = self.draft_created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if draft is not UNSET:
            field_dict["draft"] = draft
        if draft_created_at is not UNSET:
            field_dict["draft_created_at"] = draft_created_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_by_path_with_draft_response_200_draft import GetFlowByPathWithDraftResponse200Draft

        d = src_dict.copy()
        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetFlowByPathWithDraftResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetFlowByPathWithDraftResponse200Draft.from_dict(_draft)

        _draft_created_at = d.pop("draft_created_at", UNSET)
        draft_created_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_created_at, Unset):
            draft_created_at = UNSET
        else:
            draft_created_at = isoparse(_draft_created_at)

        get_flow_by_path_with_draft_response_200 = cls(
            draft=draft,
            draft_created_at=draft_created_at,
        )

        get_flow_by_path_with_draft_response_200.additional_properties = d
        return get_flow_by_path_with_draft_response_200

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
