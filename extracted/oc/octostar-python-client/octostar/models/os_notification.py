from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="OsNotification")


@attr.s(auto_attribs=True)
class OsNotification:
    """
    ### Attributes:
    * `channel (Union[Unset, str])`: None
    * `workspace_id (Union[Unset, str])`: None
    * `title (Union[Unset, str])`: None
    * `body (Union[Unset, str])`: None
    * `result_url (Union[Unset, str])`: None
    * `type (Union[Unset, str])`: None
    * `expires_at (Union[Unset, str])`: None
    """

    channel: Union[Unset, str] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    body: Union[Unset, str] = UNSET
    result_url: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    expires_at: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channel = self.channel
        workspace_id = self.workspace_id
        title = self.title
        body = self.body
        result_url = self.result_url
        type = self.type
        expires_at = self.expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channel is not UNSET:
            field_dict["channel"] = channel
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if title is not UNSET:
            field_dict["title"] = title
        if body is not UNSET:
            field_dict["body"] = body
        if result_url is not UNSET:
            field_dict["result_url"] = result_url
        if type is not UNSET:
            field_dict["type"] = type
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        channel = d.pop("channel", UNSET)

        workspace_id = d.pop("workspace_id", UNSET)

        title = d.pop("title", UNSET)

        body = d.pop("body", UNSET)

        result_url = d.pop("result_url", UNSET)

        type = d.pop("type", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        os_notification = cls(
            channel=channel,
            workspace_id=workspace_id,
            title=title,
            body=body,
            result_url=result_url,
            type=type,
            expires_at=expires_at,
        )

        os_notification.additional_properties = d
        return os_notification

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
