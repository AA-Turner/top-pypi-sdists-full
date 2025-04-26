import json
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_app_raw_multipart_data_app import UpdateAppRawMultipartDataApp


T = TypeVar("T", bound="UpdateAppRawMultipartData")


@_attrs_define
class UpdateAppRawMultipartData:
    """
    Attributes:
        app (Union[Unset, UpdateAppRawMultipartDataApp]):
        js (Union[Unset, str]):
        css (Union[Unset, str]):
    """

    app: Union[Unset, "UpdateAppRawMultipartDataApp"] = UNSET
    js: Union[Unset, str] = UNSET
    css: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        app: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.app, Unset):
            app = self.app.to_dict()

        js = self.js
        css = self.css

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if app is not UNSET:
            field_dict["app"] = app
        if js is not UNSET:
            field_dict["js"] = js
        if css is not UNSET:
            field_dict["css"] = css

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        app: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.app, Unset):
            app = (None, json.dumps(self.app.to_dict()).encode(), "application/json")

        js = self.js if isinstance(self.js, Unset) else (None, str(self.js).encode(), "text/plain")
        css = self.css if isinstance(self.css, Unset) else (None, str(self.css).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update({})
        if app is not UNSET:
            field_dict["app"] = app
        if js is not UNSET:
            field_dict["js"] = js
        if css is not UNSET:
            field_dict["css"] = css

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_app_raw_multipart_data_app import UpdateAppRawMultipartDataApp

        d = src_dict.copy()
        _app = d.pop("app", UNSET)
        app: Union[Unset, UpdateAppRawMultipartDataApp]
        if isinstance(_app, Unset):
            app = UNSET
        else:
            app = UpdateAppRawMultipartDataApp.from_dict(_app)

        js = d.pop("js", UNSET)

        css = d.pop("css", UNSET)

        update_app_raw_multipart_data = cls(
            app=app,
            js=js,
            css=css,
        )

        update_app_raw_multipart_data.additional_properties = d
        return update_app_raw_multipart_data

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
