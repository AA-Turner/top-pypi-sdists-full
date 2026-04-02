from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chat_request_mode_enum import ChatRequestModeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatRequestRequest")


@_attrs_define
class ChatRequestRequest:
    """
    Attributes:
        input_ (str): User input text for the chat model.
        thread_uuid (Union[None, UUID, Unset]): Existing thread UUID. If omitted, a new thread is created.
        mode (Union[ChatRequestModeEnum, None, Unset]): 'reload': replace the last assistant response. 'edit': edit a
            user message and re-stream. Omit for normal new-message behavior.
        edit_message_uuid (Union[None, UUID, Unset]): UUID of the user message to edit. Required when mode='edit'.
    """

    input_: str
    thread_uuid: Union[None, UUID, Unset] = UNSET
    mode: Union[ChatRequestModeEnum, None, Unset] = UNSET
    edit_message_uuid: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        thread_uuid: Union[None, Unset, str]
        if isinstance(self.thread_uuid, Unset):
            thread_uuid = UNSET
        elif isinstance(self.thread_uuid, UUID):
            thread_uuid = str(self.thread_uuid)
        else:
            thread_uuid = self.thread_uuid

        mode: Union[None, Unset, str]
        if isinstance(self.mode, Unset):
            mode = UNSET
        elif isinstance(self.mode, ChatRequestModeEnum):
            mode = self.mode.value
        else:
            mode = self.mode

        edit_message_uuid: Union[None, Unset, str]
        if isinstance(self.edit_message_uuid, Unset):
            edit_message_uuid = UNSET
        elif isinstance(self.edit_message_uuid, UUID):
            edit_message_uuid = str(self.edit_message_uuid)
        else:
            edit_message_uuid = self.edit_message_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
            }
        )
        if thread_uuid is not UNSET:
            field_dict["thread_uuid"] = thread_uuid
        if mode is not UNSET:
            field_dict["mode"] = mode
        if edit_message_uuid is not UNSET:
            field_dict["edit_message_uuid"] = edit_message_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_ = d.pop("input")

        def _parse_thread_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                thread_uuid_type_0 = UUID(data)

                return thread_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        thread_uuid = _parse_thread_uuid(d.pop("thread_uuid", UNSET))

        def _parse_mode(data: object) -> Union[ChatRequestModeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                mode_type_0 = ChatRequestModeEnum(data)

                return mode_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ChatRequestModeEnum, None, Unset], data)

        mode = _parse_mode(d.pop("mode", UNSET))

        def _parse_edit_message_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                edit_message_uuid_type_0 = UUID(data)

                return edit_message_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        edit_message_uuid = _parse_edit_message_uuid(d.pop("edit_message_uuid", UNSET))

        chat_request_request = cls(
            input_=input_,
            thread_uuid=thread_uuid,
            mode=mode,
            edit_message_uuid=edit_message_uuid,
        )

        chat_request_request.additional_properties = d
        return chat_request_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
