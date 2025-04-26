from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.lifecycle_activate_webhook_v0_type import LifecycleActivateWebhookV0Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="LifecycleActivateWebhookV0")


@attr.s(auto_attribs=True, repr=False)
class LifecycleActivateWebhookV0:
    """Sent when a user initiates app activation on a tenant.
    Please migrate to AppActivateRequestedWebhookV2."""

    _type: LifecycleActivateWebhookV0Type
    _deprecated: bool
    _excluded_properties: List[str]

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("excluded_properties={}".format(repr(self._excluded_properties)))
        return "LifecycleActivateWebhookV0({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        deprecated = self._deprecated
        excluded_properties = self._excluded_properties

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if excluded_properties is not UNSET:
            field_dict["excludedProperties"] = excluded_properties

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> LifecycleActivateWebhookV0Type:
            _type = d.pop("type")
            try:
                type = LifecycleActivateWebhookV0Type(_type)
            except ValueError:
                type = LifecycleActivateWebhookV0Type.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(LifecycleActivateWebhookV0Type, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        def get_excluded_properties() -> List[str]:
            excluded_properties = cast(List[str], d.pop("excludedProperties"))

            return excluded_properties

        try:
            excluded_properties = get_excluded_properties()
        except KeyError:
            if strict:
                raise
            excluded_properties = cast(List[str], UNSET)

        lifecycle_activate_webhook_v0 = cls(
            type=type,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
        )

        return lifecycle_activate_webhook_v0

    @property
    def type(self) -> LifecycleActivateWebhookV0Type:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: LifecycleActivateWebhookV0Type) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value

    @property
    def excluded_properties(self) -> List[str]:
        """These properties have been dropped from the payload due to size."""
        if isinstance(self._excluded_properties, Unset):
            raise NotPresentError(self, "excluded_properties")
        return self._excluded_properties

    @excluded_properties.setter
    def excluded_properties(self, value: List[str]) -> None:
        self._excluded_properties = value
