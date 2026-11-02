from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FreeTierInfo")


@_attrs_define
class FreeTierInfo:
    """Read-only. Present when the workspace has no AI provider of its own and is running on Windmill's free tier. Ignored
    on write.

        Attributes:
            exhausted (bool): The one-time grant is spent; no provider is served and the user must add their own API key.
            used_ratio (float): Fraction of the grant consumed, 0 to 1.
    """

    exhausted: bool
    used_ratio: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        exhausted = self.exhausted
        used_ratio = self.used_ratio

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exhausted": exhausted,
                "used_ratio": used_ratio,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        exhausted = d.pop("exhausted")

        used_ratio = d.pop("used_ratio")

        free_tier_info = cls(
            exhausted=exhausted,
            used_ratio=used_ratio,
        )

        free_tier_info.additional_properties = d
        return free_tier_info

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
