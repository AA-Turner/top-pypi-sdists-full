from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.app_deactivated_webhook_v2_type import AppDeactivatedWebhookV2Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppDeactivatedWebhookV2")


@attr.s(auto_attribs=True, repr=False)
class AppDeactivatedWebhookV2:
    """ Sent when a user initiates app deactivation on a tenant """

    _type: AppDeactivatedWebhookV2Type
    _deprecated: bool

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        return "AppDeactivatedWebhookV2({})".format(", ".join(fields))

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

        def get_type() -> AppDeactivatedWebhookV2Type:
            _type = d.pop("type")
            try:
                type = AppDeactivatedWebhookV2Type(_type)
            except ValueError:
                type = AppDeactivatedWebhookV2Type.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(AppDeactivatedWebhookV2Type, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        app_deactivated_webhook_v2 = cls(
            type=type,
            deprecated=deprecated,
        )

        return app_deactivated_webhook_v2

    @property
    def type(self) -> AppDeactivatedWebhookV2Type:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AppDeactivatedWebhookV2Type) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value
