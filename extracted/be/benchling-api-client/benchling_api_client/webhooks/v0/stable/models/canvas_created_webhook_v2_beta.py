from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.canvas_created_webhook_v2_beta_type import CanvasCreatedWebhookV2BetaType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CanvasCreatedWebhookV2Beta")


@attr.s(auto_attribs=True, repr=False)
class CanvasCreatedWebhookV2Beta:
    """ Sent when a new canvas is created """

    _canvas_id: str
    _feature_id: str
    _type: CanvasCreatedWebhookV2BetaType
    _deprecated: bool

    def __repr__(self):
        fields = []
        fields.append("canvas_id={}".format(repr(self._canvas_id)))
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("deprecated={}".format(repr(self._deprecated)))
        return "CanvasCreatedWebhookV2Beta({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        canvas_id = self._canvas_id
        feature_id = self._feature_id
        type = self._type.value

        deprecated = self._deprecated

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if canvas_id is not UNSET:
            field_dict["canvasId"] = canvas_id
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if type is not UNSET:
            field_dict["type"] = type
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

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

        def get_type() -> CanvasCreatedWebhookV2BetaType:
            _type = d.pop("type")
            try:
                type = CanvasCreatedWebhookV2BetaType(_type)
            except ValueError:
                type = CanvasCreatedWebhookV2BetaType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(CanvasCreatedWebhookV2BetaType, UNSET)

        def get_deprecated() -> bool:
            deprecated = d.pop("deprecated")
            return deprecated

        try:
            deprecated = get_deprecated()
        except KeyError:
            if strict:
                raise
            deprecated = cast(bool, UNSET)

        canvas_created_webhook_v2_beta = cls(
            canvas_id=canvas_id,
            feature_id=feature_id,
            type=type,
            deprecated=deprecated,
        )

        return canvas_created_webhook_v2_beta

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
    def type(self) -> CanvasCreatedWebhookV2BetaType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: CanvasCreatedWebhookV2BetaType) -> None:
        self._type = value

    @property
    def deprecated(self) -> bool:
        if isinstance(self._deprecated, Unset):
            raise NotPresentError(self, "deprecated")
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        self._deprecated = value
