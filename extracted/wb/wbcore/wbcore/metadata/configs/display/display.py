from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Optional

# Type Definitions
GridArea = list[list[str]]
SerializedField = dict[str, str | bool]
SerializedCardLayout = dict[str, str | SerializedField | list[SerializedField]]
SerializedTable = dict[str, str | bool]
SerializedChart = dict[str, str]
SerializedSection = list
SerializedLayout = dict[str, str | SerializedSection | SerializedTable]
SerializedItem = dict[str, str | dict[str, SerializedLayout]]


class DisplayType(Enum):
    FORM = "form"
    TABLE = "table"
    CHART = "chart"
    CALENDAR = "calendar"


class ItemType(Enum):
    PAGE = "page"
    TAB = "tab"


class InvalidOperatorError(Exception):
    pass


class Operator(Enum):
    S = "<"
    SE = "<="
    G = ">"
    GE = ">="
    E = "=="

    @classmethod
    def get_operator(cls, op: str) -> "Operator":
        operator_dict = {o.value: o for o in cls}
        try:
            return operator_dict[op]
        except KeyError as e:
            raise InvalidOperatorError(f"`{op}` is not a valid operator") from e


def fr(fractions: int) -> str:
    return f"{fractions}fr"


def px(pixels: int) -> str:
    return f"{pixels}px"


def pct(percent: float) -> str:
    return f"{percent}%"


def repeat(times: int, unit: str) -> str:
    return f"repeat({times}, {unit})"


def grid_definition(*units):
    return " ".join(units)


def layout_size(width: Optional[int] = None, operator: str | Operator = Operator.S) -> str:
    if width is None:
        return "default"

    if isinstance(operator, str):
        operator = Operator.get_operator(operator)

    return f"{operator.value}{width}"


@dataclass
class Table:
    key: str
    editable: bool = False

    def serialize(self) -> SerializedTable:
        return {
            "key": self.key,
            "editable": self.editable,
        }


@dataclass
class Chart:
    key: str

    def serialize(self) -> SerializedChart:
        return {"key": self.key}


@dataclass
class Layout:  # This has to be renamed to FormLayout
    grid_areas: GridArea
    grid_columns: Optional[str] = None
    grid_rows: Optional[str] = None
    sections: list = field(default_factory=list)
    tables: list[Table] = field(default_factory=list)
    charts: list[Chart] = field(default_factory=list)

    def serialize(self) -> SerializedLayout:
        serialized_layout = {
            "gridTemplateAreas": " ".join([f"'{' '.join(row)}'" for row in self.grid_areas]),
            "sections": self.sections,
            "tables": [table.serialize() for table in self.tables],
            "charts": [chart.serialize() for chart in self.charts],
        }

        if self.grid_columns:
            serialized_layout["gridTemplateColumns"] = self.grid_columns

        if self.grid_rows:
            serialized_layout["gridTemplateRows"] = self.grid_rows

        return serialized_layout


@dataclass
class Field:
    key: str
    show_label: bool = True
    label: str | None = None

    def serialize(self) -> SerializedField:
        serialized_field = {"key": self.key, "show_label": self.show_label}

        if self.label and self.show_label:
            serialized_field["label"] = self.label

        return serialized_field


# @dataclass
# class TableLayout:
#     def serialize(self) -> SerializedTableLayout:
#         pass


@dataclass
class CardLayout:
    title: Field
    fields: list[Field] = field(default_factory=list)

    color: str | None = None
    background_color: str | None = None
    image: str | None = None

    def serialize(self) -> SerializedCardLayout:
        serialized_layout = {"title": self.title.serialize(), "fields": [field.serialize() for field in self.fields]}

        if self.color:
            serialized_layout["color"] = self.color

        if self.background_color:
            serialized_layout["background_color"] = self.background_color

        if self.image:
            serialized_layout["image"] = self.image

        return serialized_layout


@dataclass
class Item:
    layouts: dict[str, Layout]
    title: str = ""

    def serialize(self) -> SerializedItem:
        return {"title": self.title, "layout": {key: layout.serialize() for key, layout in self.layouts.items()}}


@dataclass
class Display:
    display_type: DisplayType
    items: Iterable[Item]  # Consider to also be able to just a layout to make it redundant to use an Item here
    item_type: ItemType = ItemType.PAGE  # This can maybe also be nullable?

    def serialize(self) -> dict[str, str | list[SerializedItem]]:
        return {
            "display_type": self.display_type.value,
            "item_type": self.item_type.value,
            "items": [item.serialize() for item in self.items],
        }

    def __iter__(self):
        for item in self.items:
            yield item.serialize()


if __name__ == "__main__":
    # display = Display(
    #     display_type=DisplayType.FORM,
    #     items=[
    #         Item(
    #             title="First Page",
    #             layouts={
    #                 layout_size(): Layout(
    #                     grid_columns=repeat(6, fr(1)),
    #                     grid_areas=[["status", "status", "status", "title", "period", "period"]],
    #                 ),
    #                 layout_size(400): Layout(
    #                     grid_columns=repeat(3, fr(1)),
    #                     grid_areas=[["status", "status", "status"], ["title", "period", "period"]],
    #                 ),
    #             },
    #         )
    #     ],
    # )
    # display = Display(
    #     display_type=DisplayType.TABLE,
    #     items=[
    #         Item(
    #             layouts={
    #                 layout_size(): Layout(
    #                     grid_columns=repeat(4, fr(1)),
    #                     grid_areas=[
    #                         ["period", "status", "title", "other_field"],
    #                         ["period", "status", "title", "other_field1"],
    #                     ],
    #                 )
    #             }
    #         )
    #     ],
    # )
    # print(display.serialize())
    # print(list(display) == display.serialize())

    print(layout_size(500, Operator.E))  # noqa: T201
