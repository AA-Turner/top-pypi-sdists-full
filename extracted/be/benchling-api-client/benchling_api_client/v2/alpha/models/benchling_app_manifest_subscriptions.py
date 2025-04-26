from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.delivery_method import DeliveryMethod
from ..models.message_subscription_webhook_v2_beta import MessageSubscriptionWebhookV2Beta
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppManifestSubscriptions")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppManifestSubscriptions:
    """Subscriptions allow an app to receive notifications when certain actions and changes occur in Benchling."""

    _delivery_method: DeliveryMethod
    _messages: List[MessageSubscriptionWebhookV2Beta]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("delivery_method={}".format(repr(self._delivery_method)))
        fields.append("messages={}".format(repr(self._messages)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BenchlingAppManifestSubscriptions({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        delivery_method = self._delivery_method.value

        messages = []
        for messages_item_data in self._messages:
            messages_item = messages_item_data.to_dict()

            messages.append(messages_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if delivery_method is not UNSET:
            field_dict["deliveryMethod"] = delivery_method
        if messages is not UNSET:
            field_dict["messages"] = messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_delivery_method() -> DeliveryMethod:
            _delivery_method = d.pop("deliveryMethod")
            try:
                delivery_method = DeliveryMethod(_delivery_method)
            except ValueError:
                delivery_method = DeliveryMethod.of_unknown(_delivery_method)

            return delivery_method

        try:
            delivery_method = get_delivery_method()
        except KeyError:
            if strict:
                raise
            delivery_method = cast(DeliveryMethod, UNSET)

        def get_messages() -> List[MessageSubscriptionWebhookV2Beta]:
            messages = []
            _messages = d.pop("messages")
            for messages_item_data in _messages:
                messages_item = MessageSubscriptionWebhookV2Beta.from_dict(messages_item_data, strict=False)

                messages.append(messages_item)

            return messages

        try:
            messages = get_messages()
        except KeyError:
            if strict:
                raise
            messages = cast(List[MessageSubscriptionWebhookV2Beta], UNSET)

        benchling_app_manifest_subscriptions = cls(
            delivery_method=delivery_method,
            messages=messages,
        )

        benchling_app_manifest_subscriptions.additional_properties = d
        return benchling_app_manifest_subscriptions

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def delivery_method(self) -> DeliveryMethod:
        """The delivery method for the subscriptions. Currently only webhook is supported."""
        if isinstance(self._delivery_method, Unset):
            raise NotPresentError(self, "delivery_method")
        return self._delivery_method

    @delivery_method.setter
    def delivery_method(self, value: DeliveryMethod) -> None:
        self._delivery_method = value

    @property
    def messages(self) -> List[MessageSubscriptionWebhookV2Beta]:
        if isinstance(self._messages, Unset):
            raise NotPresentError(self, "messages")
        return self._messages

    @messages.setter
    def messages(self, value: List[MessageSubscriptionWebhookV2Beta]) -> None:
        self._messages = value
