from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.service_settings_state_enum import ServiceSettingsStateEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.service_settings_options import ServiceSettingsOptions


T = TypeVar("T", bound="ServiceSettings")


@_attrs_define
class ServiceSettings:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        type_ (Union[Unset, str]):
        state (Union[Unset, ServiceSettingsStateEnum]):
        error_message (Union[Unset, str]):
        shared (Union[Unset, bool]): Anybody can use it
        customer (Union[None, Unset, str]):
        customer_name (Union[None, Unset, str]):
        customer_native_name (Union[Unset, str]):
        terms_of_services (Union[Unset, str]):
        scope (Union[None, Unset, str]):
        scope_uuid (Union[Unset, UUID]):
        options (Union[Unset, ServiceSettingsOptions]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    state: Union[Unset, ServiceSettingsStateEnum] = UNSET
    error_message: Union[Unset, str] = UNSET
    shared: Union[Unset, bool] = UNSET
    customer: Union[None, Unset, str] = UNSET
    customer_name: Union[None, Unset, str] = UNSET
    customer_native_name: Union[Unset, str] = UNSET
    terms_of_services: Union[Unset, str] = UNSET
    scope: Union[None, Unset, str] = UNSET
    scope_uuid: Union[Unset, UUID] = UNSET
    options: Union[Unset, "ServiceSettingsOptions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        type_ = self.type_

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        error_message = self.error_message

        shared = self.shared

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        customer_name: Union[None, Unset, str]
        if isinstance(self.customer_name, Unset):
            customer_name = UNSET
        else:
            customer_name = self.customer_name

        customer_native_name = self.customer_native_name

        terms_of_services = self.terms_of_services

        scope: Union[None, Unset, str]
        if isinstance(self.scope, Unset):
            scope = UNSET
        else:
            scope = self.scope

        scope_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.scope_uuid, Unset):
            scope_uuid = str(self.scope_uuid)

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if state is not UNSET:
            field_dict["state"] = state
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if shared is not UNSET:
            field_dict["shared"] = shared
        if customer is not UNSET:
            field_dict["customer"] = customer
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_native_name is not UNSET:
            field_dict["customer_native_name"] = customer_native_name
        if terms_of_services is not UNSET:
            field_dict["terms_of_services"] = terms_of_services
        if scope is not UNSET:
            field_dict["scope"] = scope
        if scope_uuid is not UNSET:
            field_dict["scope_uuid"] = scope_uuid
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.service_settings_options import ServiceSettingsOptions

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, ServiceSettingsStateEnum]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = ServiceSettingsStateEnum(_state)

        error_message = d.pop("error_message", UNSET)

        shared = d.pop("shared", UNSET)

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        def _parse_customer_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name", UNSET))

        customer_native_name = d.pop("customer_native_name", UNSET)

        terms_of_services = d.pop("terms_of_services", UNSET)

        def _parse_scope(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scope = _parse_scope(d.pop("scope", UNSET))

        _scope_uuid = d.pop("scope_uuid", UNSET)
        scope_uuid: Union[Unset, UUID]
        if isinstance(_scope_uuid, Unset):
            scope_uuid = UNSET
        else:
            scope_uuid = UUID(_scope_uuid)

        _options = d.pop("options", UNSET)
        options: Union[Unset, ServiceSettingsOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = ServiceSettingsOptions.from_dict(_options)

        service_settings = cls(
            url=url,
            uuid=uuid,
            name=name,
            type_=type_,
            state=state,
            error_message=error_message,
            shared=shared,
            customer=customer,
            customer_name=customer_name,
            customer_native_name=customer_native_name,
            terms_of_services=terms_of_services,
            scope=scope,
            scope_uuid=scope_uuid,
            options=options,
        )

        service_settings.additional_properties = d
        return service_settings

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
