from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.canvas_initialize_webhook_v2_type import CanvasInitializeWebhookV2Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanvasInitializeWebhookV2")


@attr.s(auto_attribs=True, repr=False)
class CanvasInitializeWebhookV2:
    """ Sent when a user initializes a canvas via trigger in the Benchling UI """

    _feature_id: str
    _resource_id: str
    _type: CanvasInitializeWebhookV2Type
    _user_id: str
    _deprecated: bool

    def __repr__(self):
        fields = []
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("user_id={}".format(repr(self._user_id)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        return "CanvasInitializeWebhookV2({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        feature_id = self._feature_id
        resource_id = self._resource_id
        type = self._type.value

        user_id = self._user_id
        deprecated = self._deprecated

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if type is not UNSET:
            field_dict["type"] = type
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_feature_id() -> str:
            feature_id = d.pop("featureId")
            return feature_id

        try:
            feature_id = get_feature_id()
        except KeyError:
            if strict:
                raise
            feature_id = cast(str, UNSET)

        def get_resource_id() -> str:
            resource_id = d.pop("resourceId")
            return resource_id

        try:
            resource_id = get_resource_id()
        except KeyError:
            if strict:
                raise
            resource_id = cast(str, UNSET)

        def get_type() -> CanvasInitializeWebhookV2Type:
            _type = d.pop("type")
            try:
                type = CanvasInitializeWebhookV2Type(_type)
            except ValueError:
                type = CanvasInitializeWebhookV2Type.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(CanvasInitializeWebhookV2Type, UNSET)

        def get_user_id() -> str:
            user_id = d.pop("userId")
            return user_id

        try:
            user_id = get_user_id()
        except KeyError:
            if strict:
                raise
            user_id = cast(str, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        canvas_initialize_webhook_v2 = cls(
            feature_id=feature_id,
            resource_id=resource_id,
            type=type,
            user_id=user_id,
            deprecated=deprecated,
        )

        return canvas_initialize_webhook_v2

    @property
    def feature_id(self) -> str:
        if isinstance(self._feature_id, Unset):
            raise NotPresentError(self, "feature_id")
        return self._feature_id

    @feature_id.setter
    def feature_id(self, value: str) -> None:
        self._feature_id = value

    @property
    def resource_id(self) -> str:
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @property
    def type(self) -> CanvasInitializeWebhookV2Type:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: CanvasInitializeWebhookV2Type) -> None:
        self._type = value

    @property
    def user_id(self) -> str:
        if isinstance(self._user_id, Unset):
            raise NotPresentError(self, "user_id")
        return self._user_id

    @user_id.setter
    def user_id(self, value: str) -> None:
        self._user_id = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value
