from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_success_handler_json_body_type_0_extra_args import EditSuccessHandlerJsonBodyType0ExtraArgs


T = TypeVar("T", bound="EditSuccessHandlerJsonBodyType0")


@_attrs_define
class EditSuccessHandlerJsonBodyType0:
    """New grouped format for editing success handler

    Attributes:
        path (Union[Unset, str]): Path to the success handler script or flow
        extra_args (Union[Unset, EditSuccessHandlerJsonBodyType0ExtraArgs]): The arguments to pass to the script or flow
    """

    path: Union[Unset, str] = UNSET
    extra_args: Union[Unset, "EditSuccessHandlerJsonBodyType0ExtraArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_args, Unset):
            extra_args = self.extra_args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if extra_args is not UNSET:
            field_dict["extra_args"] = extra_args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_success_handler_json_body_type_0_extra_args import EditSuccessHandlerJsonBodyType0ExtraArgs

        d = src_dict.copy()
        path = d.pop("path", UNSET)

        _extra_args = d.pop("extra_args", UNSET)
        extra_args: Union[Unset, EditSuccessHandlerJsonBodyType0ExtraArgs]
        if isinstance(_extra_args, Unset):
            extra_args = UNSET
        else:
            extra_args = EditSuccessHandlerJsonBodyType0ExtraArgs.from_dict(_extra_args)

        edit_success_handler_json_body_type_0 = cls(
            path=path,
            extra_args=extra_args,
        )

        edit_success_handler_json_body_type_0.additional_properties = d
        return edit_success_handler_json_body_type_0

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
