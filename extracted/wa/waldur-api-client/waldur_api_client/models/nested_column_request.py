from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.widget_enum import WidgetEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedColumnRequest")


@_attrs_define
class NestedColumnRequest:
    """
    Attributes:
        index (int): Index allows to reorder columns.
        title (str): Title is rendered as column header.
        attribute (Union[Unset, str]): Resource attribute is rendered as table cell.
        widget (Union[BlankEnum, None, Unset, WidgetEnum]): Widget field allows to customise table cell rendering.
    """

    index: int
    title: str
    attribute: Union[Unset, str] = UNSET
    widget: Union[BlankEnum, None, Unset, WidgetEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        title = self.title

        attribute = self.attribute

        widget: Union[None, Unset, str]
        if isinstance(self.widget, Unset):
            widget = UNSET
        elif isinstance(self.widget, WidgetEnum):
            widget = self.widget.value
        elif isinstance(self.widget, BlankEnum):
            widget = self.widget.value
        else:
            widget = self.widget

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
                "title": title,
            }
        )
        if attribute is not UNSET:
            field_dict["attribute"] = attribute
        if widget is not UNSET:
            field_dict["widget"] = widget

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        index = d.pop("index")

        title = d.pop("title")

        attribute = d.pop("attribute", UNSET)

        def _parse_widget(data: object) -> Union[BlankEnum, None, Unset, WidgetEnum]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                widget_type_0 = WidgetEnum(data)

                return widget_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                widget_type_1 = BlankEnum(data)

                return widget_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, Unset, WidgetEnum], data)

        widget = _parse_widget(d.pop("widget", UNSET))

        nested_column_request = cls(
            index=index,
            title=title,
            attribute=attribute,
            widget=widget,
        )

        nested_column_request.additional_properties = d
        return nested_column_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
