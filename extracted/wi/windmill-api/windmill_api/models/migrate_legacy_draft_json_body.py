from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.migrate_legacy_draft_json_body_action import MigrateLegacyDraftJsonBodyAction

T = TypeVar("T", bound="MigrateLegacyDraftJsonBody")


@_attrs_define
class MigrateLegacyDraftJsonBody:
    """
    Attributes:
        action (MigrateLegacyDraftJsonBodyAction): delete the legacy draft, or take ownership of it.
    """

    action: MigrateLegacyDraftJsonBodyAction
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        action = self.action.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        action = MigrateLegacyDraftJsonBodyAction(d.pop("action"))

        migrate_legacy_draft_json_body = cls(
            action=action,
        )

        migrate_legacy_draft_json_body.additional_properties = d
        return migrate_legacy_draft_json_body

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
