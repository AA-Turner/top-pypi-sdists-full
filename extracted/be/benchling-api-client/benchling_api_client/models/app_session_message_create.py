from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.app_session_message_style import AppSessionMessageStyle
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppSessionMessageCreate")


@attr.s(auto_attribs=True, repr=False)
class AppSessionMessageCreate:
    """  """

    _content: str
    _style: Union[Unset, AppSessionMessageStyle] = AppSessionMessageStyle.NONE

    def __repr__(self):
        fields = []
        fields.append("content={}".format(repr(self._content)))
        fields.append("style={}".format(repr(self._style)))
        return "AppSessionMessageCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        content = self._content
        style: Union[Unset, int] = UNSET
        if not isinstance(self._style, Unset):
            style = self._style.value

        field_dict: Dict[str, Any] = {}
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

        app_session_message_create = cls(
            content=content,
            style=style,
        )

        return app_session_message_create

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
