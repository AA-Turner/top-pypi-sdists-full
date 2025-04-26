from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.message_type_webhook_v2_beta import MessageTypeWebhookV2Beta
from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageSubscriptionWebhookV2Beta")


@attr.s(auto_attribs=True, repr=False)
class MessageSubscriptionWebhookV2Beta:
    """  """

    _type: MessageTypeWebhookV2Beta
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "MessageSubscriptionWebhookV2Beta({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> MessageTypeWebhookV2Beta:
            _type = d.pop("type")
            try:
                type = MessageTypeWebhookV2Beta(_type)
            except ValueError:
                type = MessageTypeWebhookV2Beta.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(MessageTypeWebhookV2Beta, UNSET)

        message_subscription_webhook_v2_beta = cls(
            type=type,
        )

        message_subscription_webhook_v2_beta.additional_properties = d
        return message_subscription_webhook_v2_beta

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
    def type(self) -> MessageTypeWebhookV2Beta:
        """ The event that the app is subscribed to. """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: MessageTypeWebhookV2Beta) -> None:
        self._type = value
