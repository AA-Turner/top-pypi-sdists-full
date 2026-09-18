from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowConversationMessageAttachmentsItem")


@_attrs_define
class FlowConversationMessageAttachmentsItem:
    """
    Attributes:
        input_ (str): The flow input that held the file
        s3 (str): The file's key in object storage
        storage (Union[Unset, str]): The secondary storage holding the file, absent for the primary one
        filename (Union[Unset, str]):
    """

    input_: str
    s3: str
    storage: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_ = self.input_
        s3 = self.s3
        storage = self.storage
        filename = self.filename

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
                "s3": s3,
            }
        )
        if storage is not UNSET:
            field_dict["storage"] = storage
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_ = d.pop("input")

        s3 = d.pop("s3")

        storage = d.pop("storage", UNSET)

        filename = d.pop("filename", UNSET)

        flow_conversation_message_attachments_item = cls(
            input_=input_,
            s3=s3,
            storage=storage,
            filename=filename,
        )

        flow_conversation_message_attachments_item.additional_properties = d
        return flow_conversation_message_attachments_item

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
