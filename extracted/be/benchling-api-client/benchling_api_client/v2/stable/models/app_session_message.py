from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_session_message_style import AppSessionMessageStyle
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppSessionMessage")


@attr.s(auto_attribs=True, repr=False)
class AppSessionMessage:
    """  """

    _content: str
    _style: Union[Unset, AppSessionMessageStyle] = AppSessionMessageStyle.NONE
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("content={}".format(repr(self._content)))
        fields.append("style={}".format(repr(self._style)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppSessionMessage({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        content = self._content
        style: Union[Unset, int] = UNSET
        if not isinstance(self._style, Unset):
            style = self._style.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if content is not UNSET:
            field_dict["content"] = content
        if style is not UNSET:
            field_dict["style"] = style

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_content() -> str:
            content = d.pop("content")
            return content

        try:
            content = get_content()
        except KeyError:
            if strict:
                raise
            content = cast(str, UNSET)

        def get_style() -> Union[Unset, AppSessionMessageStyle]:
            style = UNSET
            _style = d.pop("style")
            if _style is not None and _style is not UNSET:
                try:
                    style = AppSessionMessageStyle(_style)
                except ValueError:
                    style = AppSessionMessageStyle.of_unknown(_style)

            return style

        try:
            style = get_style()
        except KeyError:
            if strict:
                raise
            style = cast(Union[Unset, AppSessionMessageStyle], UNSET)

        app_session_message = cls(
            content=content,
            style=style,
        )

        app_session_message.additional_properties = d
        return app_session_message

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
    def content(self) -> str:
        """ A message string, to be rendered as plain text with Benchling chips. References to Benchling items (up to 10 per msg) will be rendered as chips in the Benchling UX. A valid reference is a Benchling API id, prefixed with "id:" and contained by braces. For example: "{id:ent_a0SApq3}." """
        if isinstance(self._content, Unset):
            raise NotPresentError(self, "content")
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        self._content = value

    @property
    def style(self) -> AppSessionMessageStyle:
        if isinstance(self._style, Unset):
            raise NotPresentError(self, "style")
        return self._style

    @style.setter
    def style(self, value: AppSessionMessageStyle) -> None:
        self._style = value

    @style.deleter
    def style(self) -> None:
        self._style = UNSET
