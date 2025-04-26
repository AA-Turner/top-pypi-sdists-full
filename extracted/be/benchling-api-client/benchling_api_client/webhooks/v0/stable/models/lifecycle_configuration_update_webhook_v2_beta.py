from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.lifecycle_configuration_update_webhook_v2_beta_type import (
    LifecycleConfigurationUpdateWebhookV2BetaType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="LifecycleConfigurationUpdateWebhookV2Beta")


@attr.s(auto_attribs=True, repr=False)
class LifecycleConfigurationUpdateWebhookV2Beta:
    """ Sent when the configuration of a Benchling App is updated """

    _type: LifecycleConfigurationUpdateWebhookV2BetaType
    _deprecated: bool

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        return "LifecycleConfigurationUpdateWebhookV2Beta({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        deprecated = self._deprecated

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> LifecycleConfigurationUpdateWebhookV2BetaType:
            _type = d.pop("type")
            try:
                type = LifecycleConfigurationUpdateWebhookV2BetaType(_type)
            except ValueError:
                type = LifecycleConfigurationUpdateWebhookV2BetaType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(LifecycleConfigurationUpdateWebhookV2BetaType, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        lifecycle_configuration_update_webhook_v2_beta = cls(
            type=type,
            deprecated=deprecated,
        )

        return lifecycle_configuration_update_webhook_v2_beta

    @property
    def type(self) -> LifecycleConfigurationUpdateWebhookV2BetaType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: LifecycleConfigurationUpdateWebhookV2BetaType) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value
