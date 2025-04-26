from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.canvas_interaction_webhook_v2_type import CanvasInteractionWebhookV2Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanvasInteractionWebhookV2")


@attr.s(auto_attribs=True, repr=False)
class CanvasInteractionWebhookV2:
    """ Sent when a user interacts with an app canvas via button press """

    _button_id: str
    _canvas_id: str
    _feature_id: str
    _type: CanvasInteractionWebhookV2Type
    _user_id: str
    _deprecated: bool

    def __repr__(self):
        fields = []
        fields.append("button_id={}".format(repr(self._button_id)))
        fields.append("canvas_id={}".format(repr(self._canvas_id)))
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("user_id={}".format(repr(self._user_id)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        return "CanvasInteractionWebhookV2({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        button_id = self._button_id
        canvas_id = self._canvas_id
        feature_id = self._feature_id
        type = self._type.value

        user_id = self._user_id
        deprecated = self._deprecated

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if button_id is not UNSET:
            field_dict["buttonId"] = button_id
        if canvas_id is not UNSET:
            field_dict["canvasId"] = canvas_id
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
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

        def get_button_id() -> str:
            button_id = d.pop("buttonId")
            return button_id

        try:
            button_id = get_button_id()
        except KeyError:
            if strict:
                raise
            button_id = cast(str, UNSET)

        def get_canvas_id() -> str:
            canvas_id = d.pop("canvasId")
            return canvas_id

        try:
            canvas_id = get_canvas_id()
        except KeyError:
            if strict:
                raise
            canvas_id = cast(str, UNSET)

        def get_feature_id() -> str:
            feature_id = d.pop("featureId")
            return feature_id

        try:
            feature_id = get_feature_id()
        except KeyError:
            if strict:
                raise
            feature_id = cast(str, UNSET)

        def get_type() -> CanvasInteractionWebhookV2Type:
            _type = d.pop("type")
            try:
                type = CanvasInteractionWebhookV2Type(_type)
            except ValueError:
                type = CanvasInteractionWebhookV2Type.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(CanvasInteractionWebhookV2Type, UNSET)

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

        canvas_interaction_webhook_v2 = cls(
            button_id=button_id,
            canvas_id=canvas_id,
            feature_id=feature_id,
            type=type,
            user_id=user_id,
            deprecated=deprecated,
        )

        return canvas_interaction_webhook_v2

    @property
    def button_id(self) -> str:
        if isinstance(self._button_id, Unset):
            raise NotPresentError(self, "button_id")
        return self._button_id

    @button_id.setter
    def button_id(self, value: str) -> None:
        self._button_id = value

    @property
    def canvas_id(self) -> str:
        if isinstance(self._canvas_id, Unset):
            raise NotPresentError(self, "canvas_id")
        return self._canvas_id

    @canvas_id.setter
    def canvas_id(self, value: str) -> None:
        self._canvas_id = value

    @property
    def feature_id(self) -> str:
        if isinstance(self._feature_id, Unset):
            raise NotPresentError(self, "feature_id")
        return self._feature_id

    @feature_id.setter
    def feature_id(self, value: str) -> None:
        self._feature_id = value

    @property
    def type(self) -> CanvasInteractionWebhookV2Type:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: CanvasInteractionWebhookV2Type) -> None:
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
