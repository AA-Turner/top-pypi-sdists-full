from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_canvas_note_part_type import AppCanvasNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasNotePart")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasNotePart:
    """  """

    _app_id: Union[Unset, str] = UNSET
    _canvas_id: Union[Unset, str] = UNSET
    _feature_id: Union[Unset, str] = UNSET
    _type: Union[Unset, AppCanvasNotePartType] = UNSET
    _indentation: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app_id={}".format(repr(self._app_id)))
        fields.append("canvas_id={}".format(repr(self._canvas_id)))
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("indentation={}".format(repr(self._indentation)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvasNotePart({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_id = self._app_id
        canvas_id = self._canvas_id
        feature_id = self._feature_id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        indentation = self._indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_id is not UNSET:
            field_dict["appId"] = app_id
        if canvas_id is not UNSET:
            field_dict["canvasId"] = canvas_id
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_id() -> Union[Unset, str]:
            app_id = d.pop("appId")
            return app_id

        try:
            app_id = get_app_id()
        except KeyError:
            if strict:
                raise
            app_id = cast(Union[Unset, str], UNSET)

        def get_canvas_id() -> Union[Unset, str]:
            canvas_id = d.pop("canvasId")
            return canvas_id

        try:
            canvas_id = get_canvas_id()
        except KeyError:
            if strict:
                raise
            canvas_id = cast(Union[Unset, str], UNSET)

        def get_feature_id() -> Union[Unset, str]:
            feature_id = d.pop("featureId")
            return feature_id

        try:
            feature_id = get_feature_id()
        except KeyError:
            if strict:
                raise
            feature_id = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, AppCanvasNotePartType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = AppCanvasNotePartType(_type)
                except ValueError:
                    type = AppCanvasNotePartType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, AppCanvasNotePartType], UNSET)

        def get_indentation() -> Union[Unset, int]:
            indentation = d.pop("indentation")
            return indentation

        try:
            indentation = get_indentation()
        except KeyError:
            if strict:
                raise
            indentation = cast(Union[Unset, int], UNSET)

        app_canvas_note_part = cls(
            app_id=app_id,
            canvas_id=canvas_id,
            feature_id=feature_id,
            type=type,
            indentation=indentation,
        )

        app_canvas_note_part.additional_properties = d
        return app_canvas_note_part

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
    def app_id(self) -> str:
        """ The API identifier for the Benchling App. """
        if isinstance(self._app_id, Unset):
            raise NotPresentError(self, "app_id")
        return self._app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        self._app_id = value

    @app_id.deleter
    def app_id(self) -> None:
        self._app_id = UNSET

    @property
    def canvas_id(self) -> str:
        """ The API identifier for this Analysis Chart. """
        if isinstance(self._canvas_id, Unset):
            raise NotPresentError(self, "canvas_id")
        return self._canvas_id

    @canvas_id.setter
    def canvas_id(self, value: str) -> None:
        self._canvas_id = value

    @canvas_id.deleter
    def canvas_id(self) -> None:
        self._canvas_id = UNSET

    @property
    def feature_id(self) -> str:
        """ The developer ID assigned to the feature of this App Canvas. """
        if isinstance(self._feature_id, Unset):
            raise NotPresentError(self, "feature_id")
        return self._feature_id

    @feature_id.setter
    def feature_id(self, value: str) -> None:
        self._feature_id = value

    @feature_id.deleter
    def feature_id(self) -> None:
        self._feature_id = UNSET

    @property
    def type(self) -> AppCanvasNotePartType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AppCanvasNotePartType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def indentation(self) -> int:
        """All notes have an indentation level - the default is 0 for no indent. For lists, indentation gives notes hierarchy - a bulleted list with children is modeled as one note part with indentation 1 followed by note parts with indentation 2, for example."""
        if isinstance(self._indentation, Unset):
            raise NotPresentError(self, "indentation")
        return self._indentation

    @indentation.setter
    def indentation(self, value: int) -> None:
        self._indentation = value

    @indentation.deleter
    def indentation(self) -> None:
        self._indentation = UNSET
