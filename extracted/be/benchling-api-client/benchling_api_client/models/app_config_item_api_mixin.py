import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.app_config_item_api_mixin_app import AppConfigItemApiMixinApp
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigItemApiMixin")


@attr.s(auto_attribs=True, repr=False)
class AppConfigItemApiMixin:
    """  """

    _api_url: Union[Unset, str] = UNSET
    _app: Union[Unset, AppConfigItemApiMixinApp] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _path: Union[Unset, List[str]] = UNSET
    _type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("api_url={}".format(repr(self._api_url)))
        fields.append("app={}".format(repr(self._app)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("path={}".format(repr(self._path)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppConfigItemApiMixin({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        api_url = self._api_url
        app: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._app, Unset):
            app = self._app.to_dict()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        path: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._path, Unset):
            path = self._path

        type = self._type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if app is not UNSET:
            field_dict["app"] = app
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if path is not UNSET:
            field_dict["path"] = path
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_api_url() -> Union[Unset, str]:
            api_url = d.pop("apiURL")
            return api_url

        try:
            api_url = get_api_url()
        except KeyError:
            if strict:
                raise
            api_url = cast(Union[Unset, str], UNSET)

        def get_app() -> Union[Unset, AppConfigItemApiMixinApp]:
            app: Union[Unset, Union[Unset, AppConfigItemApiMixinApp]] = UNSET
            _app = d.pop("app")

            if not isinstance(_app, Unset):
                app = AppConfigItemApiMixinApp.from_dict(_app)

            return app

        try:
            app = get_app()
        except KeyError:
            if strict:
                raise
            app = cast(Union[Unset, AppConfigItemApiMixinApp], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_path() -> Union[Unset, List[str]]:
            path = cast(List[str], d.pop("path"))

            return path

        try:
            path = get_path()
        except KeyError:
            if strict:
                raise
            path = cast(Union[Unset, List[str]], UNSET)

        def get_type() -> Union[Unset, str]:
            type = d.pop("type")
            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, str], UNSET)

        app_config_item_api_mixin = cls(
            api_url=api_url,
            app=app,
            created_at=created_at,
            id=id,
            modified_at=modified_at,
            path=path,
            type=type,
        )

        app_config_item_api_mixin.additional_properties = d
        return app_config_item_api_mixin

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
    def api_url(self) -> str:
        if isinstance(self._api_url, Unset):
            raise NotPresentError(self, "api_url")
        return self._api_url

    @api_url.setter
    def api_url(self, value: str) -> None:
        self._api_url = value

    @api_url.deleter
    def api_url(self) -> None:
        self._api_url = UNSET

    @property
    def app(self) -> AppConfigItemApiMixinApp:
        if isinstance(self._app, Unset):
            raise NotPresentError(self, "app")
        return self._app

    @app.setter
    def app(self, value: AppConfigItemApiMixinApp) -> None:
        self._app = value

    @app.deleter
    def app(self) -> None:
        self._app = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ DateTime the app config item was created """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        """ DateTime the app config item was last modified """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def path(self) -> List[str]:
        """ Array-based representation of config item's location in the tree in order from top to bottom. """
        if isinstance(self._path, Unset):
            raise NotPresentError(self, "path")
        return self._path

    @path.setter
    def path(self, value: List[str]) -> None:
        self._path = value

    @path.deleter
    def path(self) -> None:
        self._path = UNSET

    @property
    def type(self) -> str:
        """ Type of the app config item """
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
