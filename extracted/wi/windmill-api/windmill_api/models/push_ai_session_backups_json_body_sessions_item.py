from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.push_ai_session_backups_json_body_sessions_item_artifacts import (
        PushAiSessionBackupsJsonBodySessionsItemArtifacts,
    )
    from ..models.push_ai_session_backups_json_body_sessions_item_chats_item import (
        PushAiSessionBackupsJsonBodySessionsItemChatsItem,
    )
    from ..models.push_ai_session_backups_json_body_sessions_item_delete_images_item import (
        PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem,
    )
    from ..models.push_ai_session_backups_json_body_sessions_item_head import (
        PushAiSessionBackupsJsonBodySessionsItemHead,
    )
    from ..models.push_ai_session_backups_json_body_sessions_item_images_item import (
        PushAiSessionBackupsJsonBodySessionsItemImagesItem,
    )


T = TypeVar("T", bound="PushAiSessionBackupsJsonBodySessionsItem")


@_attrs_define
class PushAiSessionBackupsJsonBodySessionsItem:
    """
    Attributes:
        id (str):
        head (Union[Unset, PushAiSessionBackupsJsonBodySessionsItemHead]):
        chats (Union[Unset, List['PushAiSessionBackupsJsonBodySessionsItemChatsItem']]):
        images (Union[Unset, List['PushAiSessionBackupsJsonBodySessionsItemImagesItem']]):
        artifacts (Union[Unset, PushAiSessionBackupsJsonBodySessionsItemArtifacts]):
        delete_chats (Union[Unset, List[str]]):
        delete_images (Union[Unset, List['PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem']]):
        partial (Union[Unset, bool]): more parts of this session follow, in this push or a later one; the session is not
            listed on this one. Such a part names its push (`push`), or it is refused
        whole (Union[Unset, bool]): a part of a push of the session whole; the head is on the part that opens it, which
            replaces whatever the storage holds of the session, and every piece the browser has is on one of them. An
            incremental part instead rides on a session the storage lists and is refused with needs_whole when it lists none
        push (Union[Unset, str]): a push split over several parts names itself on each with a token the browser draws;
            the part that opens it unlists the session and the last part lists it again, and a later part is written only
            while that token is the one there (refused with needs_whole otherwise)
        opens (Union[Unset, bool]): this part opens the push named by `push`
        epoch (Union[Unset, int]): the session's move count (its record's `moves`), kept with the marker that lists the
            session; an incremental part rides on the marker of the same count
    """

    id: str
    head: Union[Unset, "PushAiSessionBackupsJsonBodySessionsItemHead"] = UNSET
    chats: Union[Unset, List["PushAiSessionBackupsJsonBodySessionsItemChatsItem"]] = UNSET
    images: Union[Unset, List["PushAiSessionBackupsJsonBodySessionsItemImagesItem"]] = UNSET
    artifacts: Union[Unset, "PushAiSessionBackupsJsonBodySessionsItemArtifacts"] = UNSET
    delete_chats: Union[Unset, List[str]] = UNSET
    delete_images: Union[Unset, List["PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem"]] = UNSET
    partial: Union[Unset, bool] = UNSET
    whole: Union[Unset, bool] = UNSET
    push: Union[Unset, str] = UNSET
    opens: Union[Unset, bool] = UNSET
    epoch: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        head: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.head, Unset):
            head = self.head.to_dict()

        chats: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.chats, Unset):
            chats = []
            for chats_item_data in self.chats:
                chats_item = chats_item_data.to_dict()

                chats.append(chats_item)

        images: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.images, Unset):
            images = []
            for images_item_data in self.images:
                images_item = images_item_data.to_dict()

                images.append(images_item)

        artifacts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = self.artifacts.to_dict()

        delete_chats: Union[Unset, List[str]] = UNSET
        if not isinstance(self.delete_chats, Unset):
            delete_chats = self.delete_chats

        delete_images: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.delete_images, Unset):
            delete_images = []
            for delete_images_item_data in self.delete_images:
                delete_images_item = delete_images_item_data.to_dict()

                delete_images.append(delete_images_item)

        partial = self.partial
        whole = self.whole
        push = self.push
        opens = self.opens
        epoch = self.epoch

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if head is not UNSET:
            field_dict["head"] = head
        if chats is not UNSET:
            field_dict["chats"] = chats
        if images is not UNSET:
            field_dict["images"] = images
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if delete_chats is not UNSET:
            field_dict["delete_chats"] = delete_chats
        if delete_images is not UNSET:
            field_dict["delete_images"] = delete_images
        if partial is not UNSET:
            field_dict["partial"] = partial
        if whole is not UNSET:
            field_dict["whole"] = whole
        if push is not UNSET:
            field_dict["push"] = push
        if opens is not UNSET:
            field_dict["opens"] = opens
        if epoch is not UNSET:
            field_dict["epoch"] = epoch

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.push_ai_session_backups_json_body_sessions_item_artifacts import (
            PushAiSessionBackupsJsonBodySessionsItemArtifacts,
        )
        from ..models.push_ai_session_backups_json_body_sessions_item_chats_item import (
            PushAiSessionBackupsJsonBodySessionsItemChatsItem,
        )
        from ..models.push_ai_session_backups_json_body_sessions_item_delete_images_item import (
            PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem,
        )
        from ..models.push_ai_session_backups_json_body_sessions_item_head import (
            PushAiSessionBackupsJsonBodySessionsItemHead,
        )
        from ..models.push_ai_session_backups_json_body_sessions_item_images_item import (
            PushAiSessionBackupsJsonBodySessionsItemImagesItem,
        )

        d = src_dict.copy()
        id = d.pop("id")

        _head = d.pop("head", UNSET)
        head: Union[Unset, PushAiSessionBackupsJsonBodySessionsItemHead]
        if isinstance(_head, Unset):
            head = UNSET
        else:
            head = PushAiSessionBackupsJsonBodySessionsItemHead.from_dict(_head)

        chats = []
        _chats = d.pop("chats", UNSET)
        for chats_item_data in _chats or []:
            chats_item = PushAiSessionBackupsJsonBodySessionsItemChatsItem.from_dict(chats_item_data)

            chats.append(chats_item)

        images = []
        _images = d.pop("images", UNSET)
        for images_item_data in _images or []:
            images_item = PushAiSessionBackupsJsonBodySessionsItemImagesItem.from_dict(images_item_data)

            images.append(images_item)

        _artifacts = d.pop("artifacts", UNSET)
        artifacts: Union[Unset, PushAiSessionBackupsJsonBodySessionsItemArtifacts]
        if isinstance(_artifacts, Unset):
            artifacts = UNSET
        else:
            artifacts = PushAiSessionBackupsJsonBodySessionsItemArtifacts.from_dict(_artifacts)

        delete_chats = cast(List[str], d.pop("delete_chats", UNSET))

        delete_images = []
        _delete_images = d.pop("delete_images", UNSET)
        for delete_images_item_data in _delete_images or []:
            delete_images_item = PushAiSessionBackupsJsonBodySessionsItemDeleteImagesItem.from_dict(
                delete_images_item_data
            )

            delete_images.append(delete_images_item)

        partial = d.pop("partial", UNSET)

        whole = d.pop("whole", UNSET)

        push = d.pop("push", UNSET)

        opens = d.pop("opens", UNSET)

        epoch = d.pop("epoch", UNSET)

        push_ai_session_backups_json_body_sessions_item = cls(
            id=id,
            head=head,
            chats=chats,
            images=images,
            artifacts=artifacts,
            delete_chats=delete_chats,
            delete_images=delete_images,
            partial=partial,
            whole=whole,
            push=push,
            opens=opens,
            epoch=epoch,
        )

        push_ai_session_backups_json_body_sessions_item.additional_properties = d
        return push_ai_session_backups_json_body_sessions_item

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
