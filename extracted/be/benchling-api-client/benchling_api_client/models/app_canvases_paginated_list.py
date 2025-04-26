from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_canvas import AppCanvas
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppCanvasesPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class AppCanvasesPaginatedList:
    """  """

    _app_canvases: Union[Unset, List[AppCanvas]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("app_canvases={}".format(repr(self._app_canvases)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "AppCanvasesPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_canvases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._app_canvases, Unset):
            app_canvases = []
            for app_canvases_item_data in self._app_canvases:
                app_canvases_item = app_canvases_item_data.to_dict()

                app_canvases.append(app_canvases_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_canvases is not UNSET:
            field_dict["appCanvases"] = app_canvases
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_canvases() -> Union[Unset, List[AppCanvas]]:
            app_canvases = []
            _app_canvases = d.pop("appCanvases")
            for app_canvases_item_data in _app_canvases or []:
                app_canvases_item = AppCanvas.from_dict(app_canvases_item_data, strict=False)

                app_canvases.append(app_canvases_item)

            return app_canvases

        try:
            app_canvases = get_app_canvases()
        except KeyError:
            if strict:
                raise
            app_canvases = cast(Union[Unset, List[AppCanvas]], UNSET)

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        app_canvases_paginated_list = cls(
            app_canvases=app_canvases,
            next_token=next_token,
        )

        return app_canvases_paginated_list

    @property
    def app_canvases(self) -> List[AppCanvas]:
        if isinstance(self._app_canvases, Unset):
            raise NotPresentError(self, "app_canvases")
        return self._app_canvases

    @app_canvases.setter
    def app_canvases(self, value: List[AppCanvas]) -> None:
        self._app_canvases = value

    @app_canvases.deleter
    def app_canvases(self) -> None:
        self._app_canvases = UNSET

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
