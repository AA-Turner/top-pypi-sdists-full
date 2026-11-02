import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.list_shared_ui_response_200_sizes import ListSharedUiResponse200Sizes


T = TypeVar("T", bound="ListSharedUiResponse200")


@_attrs_define
class ListSharedUiResponse200:
    """
    Attributes:
        paths (List[str]):
        sizes (ListSharedUiResponse200Sizes):
        version (int):
        edited_at (datetime.datetime):
        edited_by (str):
    """

    paths: List[str]
    sizes: "ListSharedUiResponse200Sizes"
    version: int
    edited_at: datetime.datetime
    edited_by: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        paths = self.paths

        sizes = self.sizes.to_dict()

        version = self.version
        edited_at = self.edited_at.isoformat()

        edited_by = self.edited_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "paths": paths,
                "sizes": sizes,
                "version": version,
                "edited_at": edited_at,
                "edited_by": edited_by,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_shared_ui_response_200_sizes import ListSharedUiResponse200Sizes

        d = src_dict.copy()
        paths = cast(List[str], d.pop("paths"))

        sizes = ListSharedUiResponse200Sizes.from_dict(d.pop("sizes"))

        version = d.pop("version")

        edited_at = isoparse(d.pop("edited_at"))

        edited_by = d.pop("edited_by")

        list_shared_ui_response_200 = cls(
            paths=paths,
            sizes=sizes,
            version=version,
            edited_at=edited_at,
            edited_by=edited_by,
        )

        list_shared_ui_response_200.additional_properties = d
        return list_shared_ui_response_200

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
