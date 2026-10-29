"""
Form Widgets
"""

__lazy_modules__ = ["collections.abc", "django.utils.safestring"]

from typing import TYPE_CHECKING, Any

from django import forms
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

if TYPE_CHECKING:
    from collections.abc import Iterable

    from django.utils.safestring import SafeString


class DataListWidget(forms.TextInput):
    """
    DataListWidget

    Draws an HTML5 datalist form field
    """

    def __init__(self, data_list: "Iterable[str]", name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._name = name
        self._list = data_list
        self.attrs.update({"list": f"list__{self._name}"})

    def render(
        self, name: str, value, attrs: dict[str, Any] | None = None, renderer=None
    ) -> "SafeString":
        """
        Render the DataList
        :param name:
        :type name:
        :param value:
        :type value:
        :param attrs:
        :type attrs:
        :param renderer:
        :type renderer:
        :return:
        :rtype:
        """

        text_html = super().render(name, value, attrs=attrs)
        options = format_html_join(
            '', '<option value="{}">',
            ((item,) for item in self._list)
        )
        data_list = format_html(
            '<datalist id="list__{}">{}</datalist>',
            self._name, options
        )

        return text_html + data_list
