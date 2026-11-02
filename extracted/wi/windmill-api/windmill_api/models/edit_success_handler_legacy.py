from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_success_handler_legacy_success_handler_extra_args import (
        EditSuccessHandlerLegacySuccessHandlerExtraArgs,
    )


T = TypeVar("T", bound="EditSuccessHandlerLegacy")


@_attrs_define
class EditSuccessHandlerLegacy:
    """Legacy flat format for editing success handler (deprecated, use new format)

    Attributes:
        success_handler (Union[Unset, str]): Path to the success handler script or flow
        success_handler_extra_args (Union[Unset, EditSuccessHandlerLegacySuccessHandlerExtraArgs]): The arguments to
            pass to the script or flow
    """

    success_handler: Union[Unset, str] = UNSET
    success_handler_extra_args: Union[Unset, "EditSuccessHandlerLegacySuccessHandlerExtraArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success_handler = self.success_handler
        success_handler_extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.success_handler_extra_args, Unset):
            success_handler_extra_args = self.success_handler_extra_args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if success_handler is not UNSET:
            field_dict["success_handler"] = success_handler
        if success_handler_extra_args is not UNSET:
            field_dict["success_handler_extra_args"] = success_handler_extra_args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_success_handler_legacy_success_handler_extra_args import (
            EditSuccessHandlerLegacySuccessHandlerExtraArgs,
        )

        d = src_dict.copy()
        success_handler = d.pop("success_handler", UNSET)

        _success_handler_extra_args = d.pop("success_handler_extra_args", UNSET)
        success_handler_extra_args: Union[Unset, EditSuccessHandlerLegacySuccessHandlerExtraArgs]
        if isinstance(_success_handler_extra_args, Unset):
            success_handler_extra_args = UNSET
        else:
            success_handler_extra_args = EditSuccessHandlerLegacySuccessHandlerExtraArgs.from_dict(
                _success_handler_extra_args
            )

        edit_success_handler_legacy = cls(
            success_handler=success_handler,
            success_handler_extra_args=success_handler_extra_args,
        )

        edit_success_handler_legacy.additional_properties = d
        return edit_success_handler_legacy

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
