from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sign_s3_objects_json_body_s3_objects_item import SignS3ObjectsJsonBodyS3ObjectsItem


T = TypeVar("T", bound="SignS3ObjectsJsonBody")


@_attrs_define
class SignS3ObjectsJsonBody:
    """
    Attributes:
        s3_objects (List['SignS3ObjectsJsonBodyS3ObjectsItem']):
    """

    s3_objects: List["SignS3ObjectsJsonBodyS3ObjectsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        s3_objects = []
        for s3_objects_item_data in self.s3_objects:
            s3_objects_item = s3_objects_item_data.to_dict()

            s3_objects.append(s3_objects_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "s3_objects": s3_objects,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sign_s3_objects_json_body_s3_objects_item import SignS3ObjectsJsonBodyS3ObjectsItem

        d = src_dict.copy()
        s3_objects = []
        _s3_objects = d.pop("s3_objects")
        for s3_objects_item_data in _s3_objects:
            s3_objects_item = SignS3ObjectsJsonBodyS3ObjectsItem.from_dict(s3_objects_item_data)

            s3_objects.append(s3_objects_item)

        sign_s3_objects_json_body = cls(
            s3_objects=s3_objects,
        )

        sign_s3_objects_json_body.additional_properties = d
        return sign_s3_objects_json_body

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
