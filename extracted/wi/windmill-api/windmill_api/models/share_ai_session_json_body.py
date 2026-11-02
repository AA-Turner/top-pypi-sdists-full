from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.share_ai_session_json_body_snapshot import ShareAiSessionJsonBodySnapshot


T = TypeVar("T", bound="ShareAiSessionJsonBody")


@_attrs_define
class ShareAiSessionJsonBody:
    """
    Attributes:
        session_id (str): the session's id in the author's browser
        name (str):
        message_count (int):
        snapshot (ShareAiSessionJsonBodySnapshot):
        is_public (Union[Unset, bool]): left as it is on an existing share when absent; a new share starts private
    """

    session_id: str
    name: str
    message_count: int
    snapshot: "ShareAiSessionJsonBodySnapshot"
    is_public: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        session_id = self.session_id
        name = self.name
        message_count = self.message_count
        snapshot = self.snapshot.to_dict()

        is_public = self.is_public

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "name": name,
                "message_count": message_count,
                "snapshot": snapshot,
            }
        )
        if is_public is not UNSET:
            field_dict["is_public"] = is_public

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.share_ai_session_json_body_snapshot import ShareAiSessionJsonBodySnapshot

        d = src_dict.copy()
        session_id = d.pop("session_id")

        name = d.pop("name")

        message_count = d.pop("message_count")

        snapshot = ShareAiSessionJsonBodySnapshot.from_dict(d.pop("snapshot"))

        is_public = d.pop("is_public", UNSET)

        share_ai_session_json_body = cls(
            session_id=session_id,
            name=name,
            message_count=message_count,
            snapshot=snapshot,
            is_public=is_public,
        )

        share_ai_session_json_body.additional_properties = d
        return share_ai_session_json_body

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
