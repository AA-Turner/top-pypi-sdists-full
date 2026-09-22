from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AppDeployed")


@_attrs_define
class AppDeployed:
    """What a deploy of an existing app answers with. `version` is the one this call wrote, which is what an editor pins as
    the fork base of the draft it starts next: reading the head back afterwards cannot tell it from a deploy that landed
    beside it. A metadata-only update writes none and reports the head it kept.

        Attributes:
            path (str): Where the app now lives, which differs from the request path on a rename.
            version (int):
    """

    path: str
    version: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "version": version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        version = d.pop("version")

        app_deployed = cls(
            path=path,
            version=version,
        )

        app_deployed.additional_properties = d
        return app_deployed

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
