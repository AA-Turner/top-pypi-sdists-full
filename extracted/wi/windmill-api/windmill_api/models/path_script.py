from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.path_script_type import PathScriptType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.path_script_input_transforms import PathScriptInputTransforms


T = TypeVar("T", bound="PathScript")


@_attrs_define
class PathScript:
    """
    Attributes:
        input_transforms (PathScriptInputTransforms):
        path (str):
        type (PathScriptType):
        hash_ (Union[Unset, str]):
        tag_override (Union[Unset, str]):
        is_trigger (Union[Unset, bool]):
    """

    input_transforms: "PathScriptInputTransforms"
    path: str
    type: PathScriptType
    hash_: Union[Unset, str] = UNSET
    tag_override: Union[Unset, str] = UNSET
    is_trigger: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        path = self.path
        type = self.type.value

        hash_ = self.hash_
        tag_override = self.tag_override
        is_trigger = self.is_trigger

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "path": path,
                "type": type,
            }
        )
        if hash_ is not UNSET:
            field_dict["hash"] = hash_
        if tag_override is not UNSET:
            field_dict["tag_override"] = tag_override
        if is_trigger is not UNSET:
            field_dict["is_trigger"] = is_trigger

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.path_script_input_transforms import PathScriptInputTransforms

        d = src_dict.copy()
        input_transforms = PathScriptInputTransforms.from_dict(d.pop("input_transforms"))

        path = d.pop("path")

        type = PathScriptType(d.pop("type"))

        hash_ = d.pop("hash", UNSET)

        tag_override = d.pop("tag_override", UNSET)

        is_trigger = d.pop("is_trigger", UNSET)

        path_script = cls(
            input_transforms=input_transforms,
            path=path,
            type=type,
            hash_=hash_,
            tag_override=tag_override,
            is_trigger=is_trigger,
        )

        path_script.additional_properties = d
        return path_script

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
