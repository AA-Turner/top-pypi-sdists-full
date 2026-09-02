import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_by_path_response_200_draft import GetFlowByPathResponse200Draft
    from ..models.get_flow_by_path_response_200_other_drafts_users_item import (
        GetFlowByPathResponse200OtherDraftsUsersItem,
    )


T = TypeVar("T", bound="GetFlowByPathResponse200")


@_attrs_define
class GetFlowByPathResponse200:
    """
    Attributes:
        is_draft (bool):
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetFlowByPathResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetFlowByPathResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    is_draft: bool
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetFlowByPathResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetFlowByPathResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_draft = self.is_draft
        draft_saved_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_saved_at, Unset):
            draft_saved_at = self.draft_saved_at.isoformat()

        no_deployed = self.no_deployed
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        other_drafts_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.other_drafts_users, Unset):
            other_drafts_users = []
            for other_drafts_users_item_data in self.other_drafts_users:
                other_drafts_users_item = other_drafts_users_item_data.to_dict()

                other_drafts_users.append(other_drafts_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_draft": is_draft,
            }
        )
        if draft_saved_at is not UNSET:
            field_dict["draft_saved_at"] = draft_saved_at
        if no_deployed is not UNSET:
            field_dict["no_deployed"] = no_deployed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if other_drafts_users is not UNSET:
            field_dict["other_drafts_users"] = other_drafts_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_by_path_response_200_draft import GetFlowByPathResponse200Draft
        from ..models.get_flow_by_path_response_200_other_drafts_users_item import (
            GetFlowByPathResponse200OtherDraftsUsersItem,
        )

        d = src_dict.copy()
        is_draft = d.pop("is_draft")

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetFlowByPathResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetFlowByPathResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetFlowByPathResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_flow_by_path_response_200 = cls(
            is_draft=is_draft,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_flow_by_path_response_200.additional_properties = d
        return get_flow_by_path_response_200

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
