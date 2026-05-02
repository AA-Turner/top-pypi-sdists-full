from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_error_handler_json_body_type_0_extra_args import EditErrorHandlerJsonBodyType0ExtraArgs


T = TypeVar("T", bound="EditErrorHandlerJsonBodyType0")


@_attrs_define
class EditErrorHandlerJsonBodyType0:
    """New grouped format for editing error handler

    Attributes:
        path (Union[Unset, str]): Path to the error handler script or flow
        extra_args (Union[Unset, EditErrorHandlerJsonBodyType0ExtraArgs]): The arguments to pass to the script or flow
        muted_on_cancel (Union[Unset, bool]):
        muted_on_user_path (Union[Unset, bool]):
    """

    path: Union[Unset, str] = UNSET
    extra_args: Union[Unset, "EditErrorHandlerJsonBodyType0ExtraArgs"] = UNSET
    muted_on_cancel: Union[Unset, bool] = False
    muted_on_user_path: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_args, Unset):
            extra_args = self.extra_args.to_dict()

        muted_on_cancel = self.muted_on_cancel
        muted_on_user_path = self.muted_on_user_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if extra_args is not UNSET:
            field_dict["extra_args"] = extra_args
        if muted_on_cancel is not UNSET:
            field_dict["muted_on_cancel"] = muted_on_cancel
        if muted_on_user_path is not UNSET:
            field_dict["muted_on_user_path"] = muted_on_user_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_error_handler_json_body_type_0_extra_args import EditErrorHandlerJsonBodyType0ExtraArgs

        d = src_dict.copy()
        path = d.pop("path", UNSET)

        _extra_args = d.pop("extra_args", UNSET)
        extra_args: Union[Unset, EditErrorHandlerJsonBodyType0ExtraArgs]
        if isinstance(_extra_args, Unset):
            extra_args = UNSET
        else:
            extra_args = EditErrorHandlerJsonBodyType0ExtraArgs.from_dict(_extra_args)

        muted_on_cancel = d.pop("muted_on_cancel", UNSET)

        muted_on_user_path = d.pop("muted_on_user_path", UNSET)

        edit_error_handler_json_body_type_0 = cls(
            path=path,
            extra_args=extra_args,
            muted_on_cancel=muted_on_cancel,
            muted_on_user_path=muted_on_user_path,
        )

        edit_error_handler_json_body_type_0.additional_properties = d
        return edit_error_handler_json_body_type_0

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
