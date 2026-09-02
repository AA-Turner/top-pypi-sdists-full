from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_eval_cases_response_200_cases_item_input_user_attachments_item import (
        ListEvalCasesResponse200CasesItemInputUserAttachmentsItem,
    )


T = TypeVar("T", bound="ListEvalCasesResponse200CasesItemInput")


@_attrs_define
class ListEvalCasesResponse200CasesItemInput:
    """The inputs a standalone run feeds the agent.

    Attributes:
        user_message (Union[Unset, str]):
        user_attachments (Union[Unset, List['ListEvalCasesResponse200CasesItemInputUserAttachmentsItem']]):
    """

    user_message: Union[Unset, str] = UNSET
    user_attachments: Union[Unset, List["ListEvalCasesResponse200CasesItemInputUserAttachmentsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_message = self.user_message
        user_attachments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.user_attachments, Unset):
            user_attachments = []
            for user_attachments_item_data in self.user_attachments:
                user_attachments_item = user_attachments_item_data.to_dict()

                user_attachments.append(user_attachments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user_message is not UNSET:
            field_dict["user_message"] = user_message
        if user_attachments is not UNSET:
            field_dict["user_attachments"] = user_attachments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_eval_cases_response_200_cases_item_input_user_attachments_item import (
            ListEvalCasesResponse200CasesItemInputUserAttachmentsItem,
        )

        d = src_dict.copy()
        user_message = d.pop("user_message", UNSET)

        user_attachments = []
        _user_attachments = d.pop("user_attachments", UNSET)
        for user_attachments_item_data in _user_attachments or []:
            user_attachments_item = ListEvalCasesResponse200CasesItemInputUserAttachmentsItem.from_dict(
                user_attachments_item_data
            )

            user_attachments.append(user_attachments_item)

        list_eval_cases_response_200_cases_item_input = cls(
            user_message=user_message,
            user_attachments=user_attachments,
        )

        list_eval_cases_response_200_cases_item_input.additional_properties = d
        return list_eval_cases_response_200_cases_item_input

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
