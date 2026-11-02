from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_variable_expiration_handler_extra_args import (
        GetSettingsResponse200VariableExpirationHandlerExtraArgs,
    )


T = TypeVar("T", bound="GetSettingsResponse200VariableExpirationHandler")


@_attrs_define
class GetSettingsResponse200VariableExpirationHandler:
    """Workspace variable expiration handler configuration

    Attributes:
        path (Union[Unset, str]):
        extra_args (Union[Unset, GetSettingsResponse200VariableExpirationHandlerExtraArgs]): The arguments to pass to
            the script or flow
        muted_on_user_path (Union[Unset, bool]):
        notify_before_secs (Union[Unset, int]):
        remind_every_secs (Union[Unset, int]):
    """

    path: Union[Unset, str] = UNSET
    extra_args: Union[Unset, "GetSettingsResponse200VariableExpirationHandlerExtraArgs"] = UNSET
    muted_on_user_path: Union[Unset, bool] = UNSET
    notify_before_secs: Union[Unset, int] = UNSET
    remind_every_secs: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_args, Unset):
            extra_args = self.extra_args.to_dict()

        muted_on_user_path = self.muted_on_user_path
        notify_before_secs = self.notify_before_secs
        remind_every_secs = self.remind_every_secs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if extra_args is not UNSET:
            field_dict["extra_args"] = extra_args
        if muted_on_user_path is not UNSET:
            field_dict["muted_on_user_path"] = muted_on_user_path
        if notify_before_secs is not UNSET:
            field_dict["notify_before_secs"] = notify_before_secs
        if remind_every_secs is not UNSET:
            field_dict["remind_every_secs"] = remind_every_secs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_variable_expiration_handler_extra_args import (
            GetSettingsResponse200VariableExpirationHandlerExtraArgs,
        )

        d = src_dict.copy()
        path = d.pop("path", UNSET)

        _extra_args = d.pop("extra_args", UNSET)
        extra_args: Union[Unset, GetSettingsResponse200VariableExpirationHandlerExtraArgs]
        if isinstance(_extra_args, Unset):
            extra_args = UNSET
        else:
            extra_args = GetSettingsResponse200VariableExpirationHandlerExtraArgs.from_dict(_extra_args)

        muted_on_user_path = d.pop("muted_on_user_path", UNSET)

        notify_before_secs = d.pop("notify_before_secs", UNSET)

        remind_every_secs = d.pop("remind_every_secs", UNSET)

        get_settings_response_200_variable_expiration_handler = cls(
            path=path,
            extra_args=extra_args,
            muted_on_user_path=muted_on_user_path,
            notify_before_secs=notify_before_secs,
            remind_every_secs=remind_every_secs,
        )

        get_settings_response_200_variable_expiration_handler.additional_properties = d
        return get_settings_response_200_variable_expiration_handler

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
