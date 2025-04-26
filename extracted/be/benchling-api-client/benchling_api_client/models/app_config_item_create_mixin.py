from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigItemCreateMixin")


@attr.s(auto_attribs=True, repr=False)
class AppConfigItemCreateMixin:
    """  """

    _app_id: str
    _path: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app_id={}".format(repr(self._app_id)))
        fields.append("path={}".format(repr(self._path)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppConfigItemCreateMixin({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_id = self._app_id
        path = self._path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_id is not UNSET:
            field_dict["appId"] = app_id
        if path is not UNSET:
            field_dict["path"] = path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_id() -> str:
            app_id = d.pop("appId")
            return app_id

        try:
            app_id = get_app_id()
        except KeyError:
            if strict:
                raise
            app_id = cast(str, UNSET)

        def get_path() -> List[str]:
            path = cast(List[str], d.pop("path"))

            return path

        try:
            path = get_path()
        except KeyError:
            if strict:
                raise
            path = cast(List[str], UNSET)

        app_config_item_create_mixin = cls(
            app_id=app_id,
            path=path,
        )

        app_config_item_create_mixin.additional_properties = d
        return app_config_item_create_mixin

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
        """ App id to which this config item belongs. """
        if isinstance(self._app_id, Unset):
            raise NotPresentError(self, "app_id")
        return self._app_id

    @app_id.setter
    def app_id(self, value: str) -> None:
        self._app_id = value

    @property
    def path(self) -> List[str]:
        """ Array-based representation of config item's location in the tree in order from top to bottom. """
        if isinstance(self._path, Unset):
            raise NotPresentError(self, "path")
        return self._path

    @path.setter
    def path(self, value: List[str]) -> None:
        self._path = value
