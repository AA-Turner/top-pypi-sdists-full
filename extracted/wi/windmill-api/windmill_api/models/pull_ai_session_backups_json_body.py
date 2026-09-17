from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pull_ai_session_backups_json_body_resume import PullAiSessionBackupsJsonBodyResume


T = TypeVar("T", bound="PullAiSessionBackupsJsonBody")


@_attrs_define
class PullAiSessionBackupsJsonBody:
    """
    Attributes:
        ids (List[str]):
        resume (Union[Unset, PullAiSessionBackupsJsonBodyResume]): where a pull of a session that did not fit one answer
            whole picks up; the rest of the session follows a pull naming that session alone with this as `resume`
    """

    ids: List[str]
    resume: Union[Unset, "PullAiSessionBackupsJsonBodyResume"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ids = self.ids

        resume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resume, Unset):
            resume = self.resume.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ids": ids,
            }
        )
        if resume is not UNSET:
            field_dict["resume"] = resume

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.pull_ai_session_backups_json_body_resume import PullAiSessionBackupsJsonBodyResume

        d = src_dict.copy()
        ids = cast(List[str], d.pop("ids"))

        _resume = d.pop("resume", UNSET)
        resume: Union[Unset, PullAiSessionBackupsJsonBodyResume]
        if isinstance(_resume, Unset):
            resume = UNSET
        else:
            resume = PullAiSessionBackupsJsonBodyResume.from_dict(_resume)

        pull_ai_session_backups_json_body = cls(
            ids=ids,
            resume=resume,
        )

        pull_ai_session_backups_json_body.additional_properties = d
        return pull_ai_session_backups_json_body

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
