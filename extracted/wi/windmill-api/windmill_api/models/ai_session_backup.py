from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_session_backup_artifacts import AISessionBackupArtifacts
    from ..models.ai_session_backup_chats_item import AISessionBackupChatsItem
    from ..models.ai_session_backup_head import AISessionBackupHead
    from ..models.ai_session_backup_images_item import AISessionBackupImagesItem
    from ..models.ai_session_backup_next import AISessionBackupNext


T = TypeVar("T", bound="AISessionBackup")


@_attrs_define
class AISessionBackup:
    """
    Attributes:
        id (str):
        head (AISessionBackupHead):
        chats (List['AISessionBackupChatsItem']):
        images (List['AISessionBackupImagesItem']):
        listing (str): a fingerprint of the session's listing; pages of one session whose fingerprints differ do not
            belong together
        artifacts (Union[Unset, AISessionBackupArtifacts]):
        next_ (Union[Unset, AISessionBackupNext]): where a pull of a session that did not fit one answer whole picks up;
            the rest of the session follows a pull naming that session alone with this as `resume`
        moved (Union[Unset, bool]): the backup kept changing while this page was read, so it may mix two versions; the
            browser starts the session over
    """

    id: str
    head: "AISessionBackupHead"
    chats: List["AISessionBackupChatsItem"]
    images: List["AISessionBackupImagesItem"]
    listing: str
    artifacts: Union[Unset, "AISessionBackupArtifacts"] = UNSET
    next_: Union[Unset, "AISessionBackupNext"] = UNSET
    moved: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        head = self.head.to_dict()

        chats = []
        for chats_item_data in self.chats:
            chats_item = chats_item_data.to_dict()

            chats.append(chats_item)

        images = []
        for images_item_data in self.images:
            images_item = images_item_data.to_dict()

            images.append(images_item)

        listing = self.listing
        artifacts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = self.artifacts.to_dict()

        next_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.next_, Unset):
            next_ = self.next_.to_dict()

        moved = self.moved

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "head": head,
                "chats": chats,
                "images": images,
                "listing": listing,
            }
        )
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if next_ is not UNSET:
            field_dict["next"] = next_
        if moved is not UNSET:
            field_dict["moved"] = moved

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_session_backup_artifacts import AISessionBackupArtifacts
        from ..models.ai_session_backup_chats_item import AISessionBackupChatsItem
        from ..models.ai_session_backup_head import AISessionBackupHead
        from ..models.ai_session_backup_images_item import AISessionBackupImagesItem
        from ..models.ai_session_backup_next import AISessionBackupNext

        d = src_dict.copy()
        id = d.pop("id")

        head = AISessionBackupHead.from_dict(d.pop("head"))

        chats = []
        _chats = d.pop("chats")
        for chats_item_data in _chats:
            chats_item = AISessionBackupChatsItem.from_dict(chats_item_data)

            chats.append(chats_item)

        images = []
        _images = d.pop("images")
        for images_item_data in _images:
            images_item = AISessionBackupImagesItem.from_dict(images_item_data)

            images.append(images_item)

        listing = d.pop("listing")

        _artifacts = d.pop("artifacts", UNSET)
        artifacts: Union[Unset, AISessionBackupArtifacts]
        if isinstance(_artifacts, Unset):
            artifacts = UNSET
        else:
            artifacts = AISessionBackupArtifacts.from_dict(_artifacts)

        _next_ = d.pop("next", UNSET)
        next_: Union[Unset, AISessionBackupNext]
        if isinstance(_next_, Unset):
            next_ = UNSET
        else:
            next_ = AISessionBackupNext.from_dict(_next_)

        moved = d.pop("moved", UNSET)

        ai_session_backup = cls(
            id=id,
            head=head,
            chats=chats,
            images=images,
            listing=listing,
            artifacts=artifacts,
            next_=next_,
            moved=moved,
        )

        ai_session_backup.additional_properties = d
        return ai_session_backup

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
