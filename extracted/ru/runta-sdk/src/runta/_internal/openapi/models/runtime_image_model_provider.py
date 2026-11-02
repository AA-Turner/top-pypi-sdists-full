from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.runtime_image_protocol_binding import RuntimeImageProtocolBinding
    from ..models.runtime_image_subscription_option import (
        RuntimeImageSubscriptionOption,
    )


T = TypeVar("T", bound="RuntimeImageModelProvider")


@_attrs_define
class RuntimeImageModelProvider:
    """
    Attributes:
        protocol_bindings (list[RuntimeImageProtocolBinding]): How each protocol this image speaks reaches a provider.
        subscription_options (list[RuntimeImageSubscriptionOption]): Subscription credentials Runta signs in to on the
            tenant's behalf. Empty when this image only accepts a credential the tenant supplies.
        allow_custom_base_url (bool): Whether this image's agent can be pointed at another endpoint.
        allow_runtime_sign_in (bool):
    """

    protocol_bindings: list[RuntimeImageProtocolBinding]
    subscription_options: list[RuntimeImageSubscriptionOption]
    allow_custom_base_url: bool
    allow_runtime_sign_in: bool

    def to_dict(self) -> dict[str, Any]:
        protocol_bindings = []
        for protocol_bindings_item_data in self.protocol_bindings:
            protocol_bindings_item = protocol_bindings_item_data.to_dict()
            protocol_bindings.append(protocol_bindings_item)

        subscription_options = []
        for subscription_options_item_data in self.subscription_options:
            subscription_options_item = subscription_options_item_data.to_dict()
            subscription_options.append(subscription_options_item)

        allow_custom_base_url = self.allow_custom_base_url

        allow_runtime_sign_in = self.allow_runtime_sign_in

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "protocol_bindings": protocol_bindings,
                "subscription_options": subscription_options,
                "allow_custom_base_url": allow_custom_base_url,
                "allow_runtime_sign_in": allow_runtime_sign_in,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.runtime_image_protocol_binding import RuntimeImageProtocolBinding
        from ..models.runtime_image_subscription_option import (
            RuntimeImageSubscriptionOption,
        )

        d = dict(src_dict)
        protocol_bindings = []
        _protocol_bindings = d.pop("protocol_bindings")
        for protocol_bindings_item_data in _protocol_bindings:
            protocol_bindings_item = RuntimeImageProtocolBinding.from_dict(
                protocol_bindings_item_data
            )

            protocol_bindings.append(protocol_bindings_item)

        subscription_options = []
        _subscription_options = d.pop("subscription_options")
        for subscription_options_item_data in _subscription_options:
            subscription_options_item = RuntimeImageSubscriptionOption.from_dict(
                subscription_options_item_data
            )

            subscription_options.append(subscription_options_item)

        allow_custom_base_url = d.pop("allow_custom_base_url")

        allow_runtime_sign_in = d.pop("allow_runtime_sign_in")

        runtime_image_model_provider = cls(
            protocol_bindings=protocol_bindings,
            subscription_options=subscription_options,
            allow_custom_base_url=allow_custom_base_url,
            allow_runtime_sign_in=allow_runtime_sign_in,
        )

        return runtime_image_model_provider
