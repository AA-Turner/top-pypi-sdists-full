from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_session_backup_push_artifacts import AISessionBackupPushArtifacts
    from ..models.ai_session_backup_push_chats_item import AISessionBackupPushChatsItem
    from ..models.ai_session_backup_push_delete_images_item import AISessionBackupPushDeleteImagesItem
    from ..models.ai_session_backup_push_head import AISessionBackupPushHead
    from ..models.ai_session_backup_push_images_item import AISessionBackupPushImagesItem


T = TypeVar("T", bound="AISessionBackupPush")


@_attrs_define
class AISessionBackupPush:
    """
    Attributes:
        id (str):
        head (Union[Unset, AISessionBackupPushHead]):
        chats (Union[Unset, List['AISessionBackupPushChatsItem']]):
        images (Union[Unset, List['AISessionBackupPushImagesItem']]):
        artifacts (Union[Unset, AISessionBackupPushArtifacts]):
        delete_chats (Union[Unset, List[str]]):
        delete_images (Union[Unset, List['AISessionBackupPushDeleteImagesItem']]):
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
    head: Union[Unset, "AISessionBackupPushHead"] = UNSET
    chats: Union[Unset, List["AISessionBackupPushChatsItem"]] = UNSET
    images: Union[Unset, List["AISessionBackupPushImagesItem"]] = UNSET
    artifacts: Union[Unset, "AISessionBackupPushArtifacts"] = UNSET
    delete_chats: Union[Unset, List[str]] = UNSET
    delete_images: Union[Unset, List["AISessionBackupPushDeleteImagesItem"]] = UNSET
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
        from ..models.ai_session_backup_push_artifacts import AISessionBackupPushArtifacts
        from ..models.ai_session_backup_push_chats_item import AISessionBackupPushChatsItem
        from ..models.ai_session_backup_push_delete_images_item import AISessionBackupPushDeleteImagesItem
        from ..models.ai_session_backup_push_head import AISessionBackupPushHead
        from ..models.ai_session_backup_push_images_item import AISessionBackupPushImagesItem

        d = src_dict.copy()
        id = d.pop("id")

        _head = d.pop("head", UNSET)
        head: Union[Unset, AISessionBackupPushHead]
        if isinstance(_head, Unset):
            head = UNSET
        else:
            head = AISessionBackupPushHead.from_dict(_head)

        chats = []
        _chats = d.pop("chats", UNSET)
        for chats_item_data in _chats or []:
            chats_item = AISessionBackupPushChatsItem.from_dict(chats_item_data)

            chats.append(chats_item)

        images = []
        _images = d.pop("images", UNSET)
        for images_item_data in _images or []:
            images_item = AISessionBackupPushImagesItem.from_dict(images_item_data)

            images.append(images_item)

        _artifacts = d.pop("artifacts", UNSET)
        artifacts: Union[Unset, AISessionBackupPushArtifacts]
        if isinstance(_artifacts, Unset):
            artifacts = UNSET
        else:
            artifacts = AISessionBackupPushArtifacts.from_dict(_artifacts)

        delete_chats = cast(List[str], d.pop("delete_chats", UNSET))

        delete_images = []
        _delete_images = d.pop("delete_images", UNSET)
        for delete_images_item_data in _delete_images or []:
            delete_images_item = AISessionBackupPushDeleteImagesItem.from_dict(delete_images_item_data)

            delete_images.append(delete_images_item)

        partial = d.pop("partial", UNSET)

        whole = d.pop("whole", UNSET)

        push = d.pop("push", UNSET)

        opens = d.pop("opens", UNSET)

        epoch = d.pop("epoch", UNSET)

        ai_session_backup_push = cls(
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

        ai_session_backup_push.additional_properties = d
        return ai_session_backup_push

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
