from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_session import AppSession
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppSessionsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class AppSessionsPaginatedList:
    """  """

    _app_sessions: Union[Unset, List[AppSession]] = UNSET
    _next_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app_sessions={}".format(repr(self._app_sessions)))
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppSessionsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_sessions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._app_sessions, Unset):
            app_sessions = []
            for app_sessions_item_data in self._app_sessions:
                app_sessions_item = app_sessions_item_data.to_dict()

                app_sessions.append(app_sessions_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_sessions is not UNSET:
            field_dict["appSessions"] = app_sessions
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_sessions() -> Union[Unset, List[AppSession]]:
            app_sessions = []
            _app_sessions = d.pop("appSessions")
            for app_sessions_item_data in _app_sessions or []:
                app_sessions_item = AppSession.from_dict(app_sessions_item_data, strict=False)

                app_sessions.append(app_sessions_item)

            return app_sessions

        try:
            app_sessions = get_app_sessions()
        except KeyError:
            if strict:
                raise
            app_sessions = cast(Union[Unset, List[AppSession]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        app_sessions_paginated_list = cls(
            app_sessions=app_sessions,
            next_token=next_token,
        )

        app_sessions_paginated_list.additional_properties = d
        return app_sessions_paginated_list

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
    def app_sessions(self) -> List[AppSession]:
        if isinstance(self._app_sessions, Unset):
            raise NotPresentError(self, "app_sessions")
        return self._app_sessions

    @app_sessions.setter
    def app_sessions(self, value: List[AppSession]) -> None:
        self._app_sessions = value

    @app_sessions.deleter
    def app_sessions(self) -> None:
        self._app_sessions = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
