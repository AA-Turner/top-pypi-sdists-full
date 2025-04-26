from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasWriteBase")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasWriteBase:
    """  """

    _data: Union[Unset, None, str] = UNSET
    _enabled: Union[Unset, bool] = UNSET
    _feature_id: Union[Unset, str] = UNSET
    _resource_id: Union[Unset, str] = UNSET
    _session_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("data={}".format(repr(self._data)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("feature_id={}".format(repr(self._feature_id)))
        fields.append("resource_id={}".format(repr(self._resource_id)))
        fields.append("session_id={}".format(repr(self._session_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppCanvasWriteBase({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        data = self._data
        enabled = self._enabled
        feature_id = self._feature_id
        resource_id = self._resource_id
        session_id = self._session_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if data is not UNSET:
            field_dict["data"] = data
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if feature_id is not UNSET:
            field_dict["featureId"] = feature_id
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_data() -> Union[Unset, None, str]:
            data = d.pop("data")
            return data

        try:
            data = get_data()
        except KeyError:
            if strict:
                raise
            data = cast(Union[Unset, None, str], UNSET)

        def get_enabled() -> Union[Unset, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, bool], UNSET)

        def get_feature_id() -> Union[Unset, str]:
            feature_id = d.pop("featureId")
            return feature_id

        try:
            feature_id = get_feature_id()
        except KeyError:
            if strict:
                raise
            feature_id = cast(Union[Unset, str], UNSET)

        def get_resource_id() -> Union[Unset, str]:
            resource_id = d.pop("resourceId")
            return resource_id

        try:
            resource_id = get_resource_id()
        except KeyError:
            if strict:
                raise
            resource_id = cast(Union[Unset, str], UNSET)

        def get_session_id() -> Union[Unset, None, str]:
            session_id = d.pop("sessionId")
            return session_id

        try:
            session_id = get_session_id()
        except KeyError:
            if strict:
                raise
            session_id = cast(Union[Unset, None, str], UNSET)

        app_canvas_write_base = cls(
            data=data,
            enabled=enabled,
            feature_id=feature_id,
            resource_id=resource_id,
            session_id=session_id,
        )

        app_canvas_write_base.additional_properties = d
        return app_canvas_write_base

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
    def data(self) -> Optional[str]:
        """Additional data to associate with the canvas. Can be useful for persisting data associated with the canvas but won't be rendered to the user. If specified, it must be valid JSON in string format less than 5kb in total."""
        if isinstance(self._data, Unset):
            raise NotPresentError(self, "data")
        return self._data

    @data.setter
    def data(self, value: Optional[str]) -> None:
        self._data = value

    @data.deleter
    def data(self) -> None:
        self._data = UNSET

    @property
    def enabled(self) -> bool:
        """Overall control for whether the canvas is interactable or not. If `false`, every block is disabled and will override the individual block's `enabled` property. If `true` or absent, the interactivity status will defer to the block's `enabled` property."""
        if isinstance(self._enabled, Unset):
            raise NotPresentError(self, "enabled")
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @enabled.deleter
    def enabled(self) -> None:
        self._enabled = UNSET

    @property
    def feature_id(self) -> str:
        """ Identifier of the feature defined in Benchling App Manifest this canvas corresponds to. """
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
    def resource_id(self) -> str:
        """ Identifier of the resource object to attach canvas to. """
        if isinstance(self._resource_id, Unset):
            raise NotPresentError(self, "resource_id")
        return self._resource_id

    @resource_id.setter
    def resource_id(self, value: str) -> None:
        self._resource_id = value

    @resource_id.deleter
    def resource_id(self) -> None:
        self._resource_id = UNSET

    @property
    def session_id(self) -> Optional[str]:
        """Identifier of a session. If specified, app status messages from the session will be reported in the canvas."""
        if isinstance(self._session_id, Unset):
            raise NotPresentError(self, "session_id")
        return self._session_id

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        self._session_id = value

    @session_id.deleter
    def session_id(self) -> None:
        self._session_id = UNSET
