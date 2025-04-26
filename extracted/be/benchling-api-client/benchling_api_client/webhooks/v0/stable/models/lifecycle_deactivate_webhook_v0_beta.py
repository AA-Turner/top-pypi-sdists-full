from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.lifecycle_deactivate_webhook_v0_beta_type import LifecycleDeactivateWebhookV0BetaType
from ..types import UNSET, Unset

T = TypeVar("T", bound="LifecycleDeactivateWebhookV0Beta")


@attr.s(auto_attribs=True, repr=False)
class LifecycleDeactivateWebhookV0Beta:
    """Sent when a user initiates app deactivation on a tenant.
    Please migrate to Shareable Apps. Reference: https://docs.benchling.com/changelog/sunset-app-lifecycle-management"""

    _type: LifecycleDeactivateWebhookV0BetaType
    _deprecated: bool
    _excluded_properties: List[str]

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        fields.append("excluded_properties={}".format(repr(self._excluded_properties)))
        return "LifecycleDeactivateWebhookV0Beta({})".format(", ".join(fields))

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

        def get_type() -> LifecycleDeactivateWebhookV0BetaType:
            _type = d.pop("type")
            try:
                type = LifecycleDeactivateWebhookV0BetaType(_type)
            except ValueError:
                type = LifecycleDeactivateWebhookV0BetaType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(LifecycleDeactivateWebhookV0BetaType, UNSET)

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

        lifecycle_deactivate_webhook_v0_beta = cls(
            type=type,
            deprecated=deprecated,
            excluded_properties=excluded_properties,
        )

        return lifecycle_deactivate_webhook_v0_beta

    @property
    def type(self) -> LifecycleDeactivateWebhookV0BetaType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: LifecycleDeactivateWebhookV0BetaType) -> None:
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
