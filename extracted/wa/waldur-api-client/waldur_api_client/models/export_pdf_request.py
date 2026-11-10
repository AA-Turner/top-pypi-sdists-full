from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportPdfRequest")


@_attrs_define
class ExportPdfRequest:
    """
    Attributes:
        title (str):
        columns (Union[Unset, list[str]]): Header row of a table export.
        rows (Union[Unset, list[list[str]]]): Rows of a table export, each with one cell per column.
        image (Union[Unset, str]): Base64-encoded PNG of a chart export.
    """

    title: str
    columns: Union[Unset, list[str]] = UNSET
    rows: Union[Unset, list[list[str]]] = UNSET
    image: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        columns: Union[Unset, list[str]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = self.columns

        rows: Union[Unset, list[list[str]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data

                rows.append(rows_item)

        image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if rows is not UNSET:
            field_dict["rows"] = rows
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        columns = cast(list[str], d.pop("columns", UNSET))

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = cast(list[str], rows_item_data)

            rows.append(rows_item)

        image = d.pop("image", UNSET)

        export_pdf_request = cls(
            title=title,
            columns=columns,
            rows=rows,
            image=image,
        )

        export_pdf_request.additional_properties = d
        return export_pdf_request

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
