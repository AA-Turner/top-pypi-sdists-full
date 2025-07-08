from dataclasses import dataclass, field
from typing import Iterable, Literal, Optional

from slugify import slugify

from wbcore.metadata.configs.display.formatting import Formatting, FormattingRule


@dataclass
class Tooltip:
    key: str | None = None
    endpoint: str | None = None
    width: str | None = None
    height: str | None = None

    def __post_init__(self):
        if not self.key and not self.endpoint:
            raise ValueError("Either key or endpoint needs to be specified.")

    def serialize(self):
        tooltip = {}
        if self.key:
            tooltip["key"] = self.key

        if self.endpoint:
            tooltip["endpoint"] = self.endpoint

        if self.width:
            tooltip["width"] = self.width

        if self.height:
            tooltip["height"] = self.height

        return tooltip


@dataclass(unsafe_hash=True)
class Field:
    key: str | None
    label: str
    formatting_rules: Iterable[FormattingRule] = field(default_factory=list)
    width: int | None = None

    tooltip: Tooltip | None = None

    hide: bool | None = None
    pinned: str | None = None

    children: list["Field"] | None = None
    marry_children: bool | None = True
    show: Literal["open"] | Literal["closed"] | None = None
    open_by_default: bool | None = None

    lock_position: Literal["left"] | Literal["right"] | None = None
    movable: bool = True
    resizable: bool = True
    auto_size: bool = True
    menu: bool = True
    size_to_fit: bool = True

    def __post_init__(self):
        if not self.key and len(self.children) == 0:
            self.key = slugify(str(self.label))  # we cast to str explicitly in case label is in a translation wrapper

    def iterate_leaf_fields(self, aggregated_parent_label: str = ""):
        label = self.label
        if aggregated_parent_label:
            label = aggregated_parent_label + " " + label
        if self.children:
            for children in self.children:
                yield from children.iterate_leaf_fields(label)
        else:
            yield self.key, label

    def serialize(self, parent_identifier: str | None = None):
        identifier = parent_identifier + "_" + self.key if parent_identifier else self.key
        repr = {
            "identifier": identifier,
            "key": self.key,
            "label": self.label,
            "formatting_rules": [dict(rule) for rule in self.formatting_rules],
        }

        if self.width:
            repr["width"] = self.width

        if self.hide:
            repr["hide"] = self.hide

        if self.pinned and self.pinned in ["left", "right"]:
            repr["pinned"] = self.pinned

        if self.children:
            repr["children"] = [child.serialize(identifier) for child in self.children]
            repr["marry_children"] = self.marry_children is True  # Convert None into False

        if self.show:
            repr["show"] = self.show

        if self.open_by_default is not None:
            repr["open_by_default"] = self.open_by_default

        if not self.movable:
            repr["movable"] = self.movable

        if not self.resizable:
            repr["resizable"] = self.resizable

        if self.lock_position:
            repr["lock_position"] = self.lock_position

        if not self.auto_size:
            repr["auto_size"] = self.auto_size

        if not self.menu:
            repr["menu"] = self.menu

        if not self.size_to_fit:
            repr["size_to_fit"] = self.size_to_fit

        if self.tooltip:
            repr["tooltip"] = self.tooltip.serialize()
        return repr


@dataclass(unsafe_hash=True)
class LegendItem:
    icon: str
    label: str
    value: Optional[str | bool] = None

    def __iter__(self):
        yield "icon", self.icon
        yield "label", self.label

        if self.value is not None:
            yield "value", self.value


@dataclass(unsafe_hash=True)
class Legend:
    items: list[LegendItem]
    label: str | None = None
    key: str | None = None

    def __post_init__(self):
        if self.key:
            assert all(
                [item.value is not None for item in self.items]
            ), "If key is set, all items need to specify a value."

    def __iter__(self):
        if self.label:
            yield "label", self.label

        if self.key:
            yield "key", self.key

        yield "items", [dict(item) for item in self.items]


@dataclass(unsafe_hash=True, kw_only=True)
class BaseTreeGroupLevelOption:
    lookup: str = "_group_key"
    filter_key: str = "group_keys"
    filter_whitelist: list[str] = field(default_factory=list)
    filter_blacklist: list[str] = field(default_factory=list)
    clear_filter: bool = (
        False
        # Set to True if preselected filters other than required ones need to be cleared out before fetching the tree group
    )
    filter_depth: int | None = 1  # None would actually return all group keys concatenated.

    def __iter__(self):
        yield "lookup", self.lookup
        yield "filter_key", self.filter_key
        yield "filter_whitelist", self.filter_whitelist
        yield "filter_blacklist", self.filter_blacklist
        yield "clear_filter", self.clear_filter
        yield "filter_depth", self.filter_depth


@dataclass(unsafe_hash=True, kw_only=True)
class TreeGroupLevelOption(BaseTreeGroupLevelOption):
    list_endpoint: str
    reorder_endpoint: str | None = None
    reparent_endpoint: str | None = None
    parent_field: str = "parent"
    ordering_field: str = "order"

    def __iter__(self):
        yield from super().__iter__()
        endpoints = {"list": self.list_endpoint}
        if self.reorder_endpoint:
            endpoints["reorder"] = self.reorder_endpoint

        if self.reparent_endpoint:
            endpoints["reparent"] = self.reparent_endpoint

        yield "endpoints", endpoints

        yield "parent_field", self.parent_field
        yield "ordering_field", self.ordering_field


@dataclass(unsafe_hash=True)
class ListDisplay:
    fields: list[Field | None]
    legends: list[Legend] = field(default_factory=list)
    formatting: list[Formatting] = field(default_factory=list)
    editable: bool = True
    hide_control_bar: bool = False

    ordering_field: str = "order"
    condensed: bool = False

    auto_height: bool = False

    tree: bool = False
    tree_group_parent_pointer: str | None = (
        None  # if specified, the display assumes the whole tree data is given in the initial request and that it can be grouped by the given group key
    )
    tree_group_key: str = "_group_key"  # The field the `tree_group_parent_pointer` points to

    tree_group_field: str | None = None
    tree_group_open_level: int = 0
    tree_group_field_sortable: bool = False

    tree_group_level_options: list[TreeGroupLevelOption] = field(default_factory=list)

    @property
    def flatten_fields(self) -> tuple[str, str]:
        if self.fields:  # fields can be None
            for f in filter(lambda o: o, self.fields):  # field can be None
                yield from f.iterate_leaf_fields()

    def __iter__(self):
        yield "editable", self.editable
        yield "fields", [field.serialize() for field in self.fields if field]
        yield "legends", [dict(legend) for legend in self.legends if legend]
        yield "formatting", [dict(formatting) for formatting in self.formatting if formatting]
        yield "hide_control_bar", self.hide_control_bar
        yield "ordering_field", self.ordering_field

        yield "auto_height", self.auto_height

        if self.condensed:
            yield "condensed", self.condensed

        if self.tree:
            yield "tree", self.tree
            tree_group = {
                "field": (self.tree_group_field if self.tree_group_field else self.fields[0].key),
                "open_level": self.tree_group_open_level,
                "field_sortable": self.tree_group_field_sortable,
                "group_key": self.tree_group_key,
                "parent_pointer": self.tree_group_parent_pointer,
            }
            tree_group["level_options"] = [dict(level_option) for level_option in self.tree_group_level_options]
            yield "tree_group", tree_group


@dataclass(unsafe_hash=True)
class Calendar:
    title: str
    period: str
    all_day: bool
    color: str
    icon: str
    entities: list
    endpoint: str

    def __iter__(self):
        yield (
            "calendar",
            {
                "title": self.title,
                "period": self.period,
                "all_day": self.all_day,
                "color": self.color,
                "icon": self.icon,
                "entities": self.entities,
                "endpoint": self.endpoint,
            },
        )
