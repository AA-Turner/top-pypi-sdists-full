from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_error_handler_json_body_type_1_error_handler_extra_args import (
        EditErrorHandlerJsonBodyType1ErrorHandlerExtraArgs,
    )


T = TypeVar("T", bound="EditErrorHandlerJsonBodyType1")


@_attrs_define
class EditErrorHandlerJsonBodyType1:
    """Legacy flat format for editing error handler (deprecated, use new format)

    Attributes:
        error_handler (Union[Unset, str]): Path to the error handler script or flow
        error_handler_extra_args (Union[Unset, EditErrorHandlerJsonBodyType1ErrorHandlerExtraArgs]): The arguments to
            pass to the script or flow
        error_handler_muted_on_cancel (Union[Unset, bool]):
    """

    error_handler: Union[Unset, str] = UNSET
    error_handler_extra_args: Union[Unset, "EditErrorHandlerJsonBodyType1ErrorHandlerExtraArgs"] = UNSET
    error_handler_muted_on_cancel: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error_handler = self.error_handler
        error_handler_extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_extra_args, Unset):
            error_handler_extra_args = self.error_handler_extra_args.to_dict()

        error_handler_muted_on_cancel = self.error_handler_muted_on_cancel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_handler is not UNSET:
            field_dict["error_handler"] = error_handler
        if error_handler_extra_args is not UNSET:
            field_dict["error_handler_extra_args"] = error_handler_extra_args
        if error_handler_muted_on_cancel is not UNSET:
            field_dict["error_handler_muted_on_cancel"] = error_handler_muted_on_cancel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_error_handler_json_body_type_1_error_handler_extra_args import (
            EditErrorHandlerJsonBodyType1ErrorHandlerExtraArgs,
        )

        d = src_dict.copy()
        error_handler = d.pop("error_handler", UNSET)

        _error_handler_extra_args = d.pop("error_handler_extra_args", UNSET)
        error_handler_extra_args: Union[Unset, EditErrorHandlerJsonBodyType1ErrorHandlerExtraArgs]
        if isinstance(_error_handler_extra_args, Unset):
            error_handler_extra_args = UNSET
        else:
            error_handler_extra_args = EditErrorHandlerJsonBodyType1ErrorHandlerExtraArgs.from_dict(
                _error_handler_extra_args
            )

        error_handler_muted_on_cancel = d.pop("error_handler_muted_on_cancel", UNSET)

        edit_error_handler_json_body_type_1 = cls(
            error_handler=error_handler,
            error_handler_extra_args=error_handler_extra_args,
            error_handler_muted_on_cancel=error_handler_muted_on_cancel,
        )

        edit_error_handler_json_body_type_1.additional_properties = d
        return edit_error_handler_json_body_type_1

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
