"""Declarative widget primitives for Python DSL pages.

Each widget serializes to a JSON dict via ``to_dict()``. The frontend
``<WidgetRenderer>`` component recursively renders the tree.
"""

from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from .constants import Column as ColumnDef

if TYPE_CHECKING:
    from .db import CollectionRef

ChartType = Literal["line", "bar", "pie", "scatter", "area"]
"""Supported chart visualisation types."""

MetricFormat = Literal["number", "currency", "percent"]
"""Display format for a ``Metric`` widget's value."""


class _Widget:
    _type: str = ""

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


class Page(_Widget):
    _type = "page"

    def __init__(self, children: list[_Widget]) -> None:
        self.children = children

    def to_dict(self) -> dict[str, Any]:
        return {"type": self._type, "children": [c.to_dict() for c in self.children]}


class Row(_Widget):
    _type = "row"

    def __init__(
        self,
        children: list[_Widget],
        *,
        columns: list[str | int | float] | None = None,
        min_widths: list[int | str] | int | str | None = None,
        gap: int | str | None = None,
        fill: bool = False,
        align: Literal["start", "center", "end", "stretch"] | None = None,
    ) -> None:
        self.children = children
        self.columns = columns
        self.min_widths = min_widths
        self.gap = gap
        self.fill = fill
        self.align = align

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "children": [c.to_dict() for c in self.children]}
        if self.columns is not None:
            d["columns"] = list(self.columns)
        if self.min_widths is not None:
            d["min_widths"] = (
                list(self.min_widths) if isinstance(self.min_widths, list) else self.min_widths
            )
        if self.gap is not None:
            d["gap"] = self.gap
        if self.fill:
            d["fill"] = True
        if self.align is not None:
            d["align"] = self.align
        return d


class Column(_Widget):
    _type = "column"

    def __init__(
        self,
        children: list[_Widget],
        *,
        width: int | str | None = None,
        flex: int | float | str | None = None,
        rows: list[str | int | float] | None = None,
        gap: int | str | None = None,
        fill: bool = False,
    ) -> None:
        self.children = children
        self.width = width
        self.flex = flex
        self.rows = rows
        self.gap = gap
        self.fill = fill

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "children": [c.to_dict() for c in self.children]}
        if self.width is not None:
            d["width"] = self.width
        if self.flex is not None:
            d["flex"] = self.flex
        if self.rows is not None:
            d["rows"] = list(self.rows)
        if self.gap is not None:
            d["gap"] = self.gap
        if self.fill:
            d["fill"] = True
        return d


class Card(_Widget):
    """Section container with a title row and stacked rows.

    By default renders **borderless** — the section sits directly on the
    page, with hairlines between rows for clean list-view separation.
    Pass ``bordered=True`` to wrap the section in a bordered card with
    background fill and rounded corners.

    Args:
        title: Section heading rendered above the body.
        icon: Optional Lucide icon name (kebab-case, e.g. ``"database"``)
            shown next to the title.
        children: Widgets stacked inside the card body.
        bordered: When ``True``, renders traditional card chrome
            (border + bg + radius). Default ``False``.
    """

    _type = "card"

    def __init__(
        self,
        title: str | None = None,
        children: list[_Widget] | None = None,
        *,
        icon: str | None = None,
        bordered: bool = False,
    ) -> None:
        self.title = title
        self.icon = icon
        self.bordered = bordered
        self.children = children or []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.title is not None:
            d["title"] = self.title
        if self.icon is not None:
            d["icon"] = self.icon
        if self.bordered:
            d["bordered"] = True
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


class Metric(_Widget):
    """Single KPI / stat card.

    Provide a static ``value`` directly, or bind to a collection with
    ``data`` + ``field`` to compute the metric from stored data.

    Args:
        label: Display label shown above the value.
        data: Name of a collection to pull data from.
        field: Column in the collection to aggregate.
        value: Static value to display (used when ``data`` is ``None``).
        format: Display format — ``"number"``, ``"currency"``, or
            ``"percent"``.
    """

    _type = "metric"

    def __init__(
        self,
        label: str,
        *,
        data: str | None = None,
        field: str | None = None,
        value: Any = None,
        format: MetricFormat | None = None,
    ) -> None:
        self.label = label
        self.data = data
        self.field = field
        self.value = value
        self.format = format

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "label": self.label}
        if self.data is not None:
            d["data"] = self.data
        if self.field is not None:
            d["field"] = self.field
        if self.value is not None:
            d["value"] = self.value
        if self.format is not None:
            d["format"] = self.format
        return d


class Table(_Widget):
    """Data table backed by a collection or inline rows.

    Pass a ``CollectionRef`` (from ``self.db.collection``) to bind the table
    to a stored collection — column order, sort, filter, and pagination
    settings are inherited from the collection declaration.  Alternatively
    pass ``rows`` for a static inline table.

    Args:
        collection: Collection name (``str``) or a ``CollectionRef``.
            When a ``CollectionRef`` is used, column/sort/filter/paginate
            defaults are pulled from its declaration automatically.
        data: Named data source (alternative to ``collection``).
        rows: Inline list of ``{"col": value}`` dicts.
        columns: Column names to display (and their order).
        label: Optional display label used when the table appears in a
            ``TableBrowser``. The collection remains the data source.
        scope: Scope for dynamic collection metadata when ``collection`` is a string.
        sortable: Enable column sorting in the UI.
        filterable: Show a filter bar above the table.
        paginate: Rows per page (``0`` disables pagination).
        editable: Allow inline row cell edits for collection-backed tables.
        reorderable: Allow users to persist collection column ordering.
    """

    _type = "table"

    def __init__(
        self,
        collection: str | CollectionRef | None = None,
        *,
        data: str | None = None,
        rows: list[dict[str, Any]] | None = None,
        columns: list[str | ColumnDef] | None = None,
        label: str | None = None,
        scope: Literal["app", "user", "owner", "session"] | None = None,
        sortable: bool = False,
        filterable: bool = False,
        paginate: int = 0,
        editable: bool = False,
        reorderable: bool = False,
    ) -> None:
        from .db import CollectionRef as _Ref

        self._typed_columns: list[ColumnDef] | None = None
        if isinstance(collection, _Ref):
            decl = collection._decl
            self.collection = collection.name
            scope = scope or decl.scope
            if columns is None and decl.columns:
                self._typed_columns = list(decl.columns)
                columns = [c.key for c in decl.columns]
            if not sortable and decl.sortable:
                sortable = decl.sortable
            if not filterable and decl.filterable:
                filterable = decl.filterable
            if not paginate and decl.paginate:
                paginate = decl.paginate
        else:
            self.collection = collection
        if columns and self._typed_columns is None:
            self._typed_columns = [
                c if isinstance(c, ColumnDef) else ColumnDef(key=c) for c in columns
            ]
            columns = [c.key if isinstance(c, ColumnDef) else c for c in columns]
        self.data = data
        self.rows = rows
        self.columns = columns
        self.label = label
        self.scope = scope
        self.sortable = sortable
        self.filterable = filterable
        self.paginate = paginate
        self.editable = editable
        self.reorderable = reorderable

    def _serialize_columns(self) -> list:
        if self._typed_columns:
            has_types = any(c.type != "text" or c.label or c.format for c in self._typed_columns)
            if has_types:
                return [c.to_dict() for c in self._typed_columns]
        return self.columns if self.columns else []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.label is not None:
            d["label"] = self.label
        if self.collection is not None:
            has_overrides = (
                self.columns
                or self.scope
                or self.sortable
                or self.filterable
                or self.paginate
                or self.editable
                or self.reorderable
            )
            if has_overrides:
                d["collection"] = self.collection
                if self.scope:
                    d["scope"] = self.scope
                if self.columns:
                    d["columns"] = self._serialize_columns()
                if self.sortable:
                    d["sortable"] = True
                if self.filterable:
                    d["filterable"] = True
                if self.paginate > 0:
                    d["paginate"] = self.paginate
                if self.editable:
                    d["editable"] = True
                if self.reorderable:
                    d["reorderable"] = True
            else:
                d["collection_ref"] = self.collection
            return d
        if self.data is not None:
            d["data"] = self.data
        if self.rows is not None:
            d["rows"] = self.rows
        if self.columns is not None:
            d["columns"] = self._serialize_columns()
        if self.sortable:
            d["sortable"] = True
        if self.filterable:
            d["filterable"] = True
        if self.paginate > 0:
            d["paginate"] = self.paginate
        if self.editable:
            d["editable"] = True
        if self.reorderable:
            d["reorderable"] = True
        return d


class TableGroup(_Widget):
    """Named folder for collection-backed tables inside a ``TableBrowser``."""

    _type = "table_group"

    def __init__(self, label: str, items: list[Table | TableGroup]) -> None:
        if not label:
            raise ValueError("TableGroup label is required")
        self.label = label
        self.items = list(items)
        for item in self.items:
            _validate_table_browser_item(item)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self._type,
            "label": self.label,
            "items": [item.to_dict() for item in self.items],
        }


class TableBrowser(_Widget):
    """Hierarchical browser for collection-backed ``Table`` widgets."""

    _type = "table_browser"

    def __init__(
        self,
        items: list[Table | TableGroup],
        *,
        title: str | None = None,
    ) -> None:
        self.items = list(items)
        self.title = title
        for item in self.items:
            _validate_table_browser_item(item)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self._type,
            "items": [item.to_dict() for item in self.items],
        }
        if self.title is not None:
            d["title"] = self.title
        return d


def _validate_table_browser_item(item: Table | TableGroup) -> None:
    if isinstance(item, TableGroup):
        return
    if not isinstance(item, Table):
        raise TypeError("TableBrowser items must be Table or TableGroup instances")
    if item.collection is None:
        raise ValueError("TableBrowser only supports collection-backed Table widgets")


class Chart(_Widget):
    """Chart widget backed by a named data source.

    Args:
        data: Name of the data source to visualise.
        chart_type: Visualisation style — ``"line"``, ``"bar"``,
            ``"pie"``, ``"scatter"``, or ``"area"``.
        x: Column to use for the x-axis.
        y: Column to use for the y-axis.
    """

    _type = "chart"

    def __init__(
        self,
        *,
        data: str | None = None,
        chart_type: ChartType = "line",
        x: str | None = None,
        y: str | None = None,
    ) -> None:
        self.data = data
        self.chart_type = chart_type
        self.x = x
        self.y = y

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "chart_type": self.chart_type}
        if self.data is not None:
            d["data"] = self.data
        if self.x is not None:
            d["x"] = self.x
        if self.y is not None:
            d["y"] = self.y
        return d


class Text(_Widget):
    _type = "text"

    def __init__(self, content: str, *, style: str | None = None) -> None:
        self.content = content
        self.style = style

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "content": self.content}
        if self.style is not None:
            d["style"] = self.style
        return d


class Divider(_Widget):
    _type = "divider"

    def to_dict(self) -> dict[str, Any]:
        return {"type": self._type}


def _target_name(value: Any) -> str:
    name = getattr(value, "name", value)
    if not isinstance(name, str) or not name:
        raise ValueError("action target must be a non-empty string or object with a .name")
    return name


def _page_target_name(value: Any) -> str:
    route = getattr(value, "route", None)
    if isinstance(route, str) and route:
        return route
    return _target_name(value)


def _action_target(
    prompt: Any | None, workflow: Any | None, page: Any | None
) -> tuple[str, str] | None:
    targets = [
        (k, v)
        for k, v in (("prompt", prompt), ("workflow", workflow), ("page", page))
        if v is not None
    ]
    if len(targets) > 1:
        raise ValueError("action widgets must define at most one of prompt=, workflow=, or page=")
    if not targets:
        return None
    key, value = targets[0]
    return key, _page_target_name(value) if key == "page" else _target_name(value)


class Image(_Widget):
    """Static image widget for media-rich pages and home galleries.

    Images can be plain media or clickable actions. Use ``workflow=`` /
    ``input=`` to start a workflow, ``page=`` to navigate, or ``prompt=`` to
    start chat.
    """

    _type = "image"

    def __init__(
        self,
        src: str,
        *,
        alt: str = "",
        caption: str | None = None,
        aspect_ratio: str | None = None,
        prompt: str | None = None,
        workflow: Any | None = None,
        page: Any | None = None,
        input: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.src = src
        self.alt = alt
        self.caption = caption
        self.aspect_ratio = aspect_ratio
        self.target = _action_target(prompt, workflow, page)
        if input and payload:
            raise ValueError("Image accepts input= or payload=, not both")
        if (input or payload) and (self.target is None or self.target[0] != "workflow"):
            raise ValueError("Image input is only supported with workflow=")
        self.payload = input or payload

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "src": self.src, "alt": self.alt}
        if self.caption:
            d["caption"] = self.caption
        if self.aspect_ratio:
            d["aspect_ratio"] = self.aspect_ratio
        if self.target:
            d["target"], d["value"] = self.target
        if self.payload:
            d["payload"] = dict(self.payload)
        return d


class ImageGallery(_Widget):
    """Responsive image gallery for generated media, examples, or screenshots."""

    _type = "image_gallery"

    def __init__(
        self,
        images: list[str | dict[str, Any] | Image] | None = None,
        *,
        data: str | None = None,
        title: str | None = None,
        columns: int | None = None,
    ) -> None:
        self.images = images or []
        self.data = data
        self.title = title
        self.columns = columns

    def _serialize_image(self, image: str | dict[str, Any] | Image) -> dict[str, Any]:
        if isinstance(image, Image):
            d = image.to_dict()
            d.pop("type", None)
            return d
        if isinstance(image, str):
            return {"src": image, "alt": ""}
        return dict(image)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self._type,
            "images": [self._serialize_image(image) for image in self.images],
        }
        if self.data:
            d["data"] = self.data
        if self.title:
            d["title"] = self.title
        if self.columns is not None:
            d["columns"] = self.columns
        return d


class Video(_Widget):
    """Static video player widget for generated clips, walkthroughs, or demos."""

    _type = "video"

    def __init__(
        self,
        src: str,
        *,
        poster: str | None = None,
        title: str | None = None,
        caption: str | None = None,
        controls: bool = True,
        autoplay: bool = False,
        loop: bool = False,
        muted: bool = False,
        width: int | str | None = None,
        aspect_ratio: str | None = None,
    ) -> None:
        self.src = src
        self.poster = poster
        self.title = title
        self.caption = caption
        self.controls = controls
        self.autoplay = autoplay
        self.loop = loop
        self.muted = muted
        self.width = width
        self.aspect_ratio = aspect_ratio

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self._type,
            "src": self.src,
            "controls": self.controls,
        }
        if self.poster:
            d["poster"] = self.poster
        if self.title:
            d["title"] = self.title
        if self.caption:
            d["caption"] = self.caption
        if self.autoplay:
            d["autoplay"] = True
        if self.loop:
            d["loop"] = True
        if self.muted:
            d["muted"] = True
        if self.width is not None:
            d["width"] = self.width
        if self.aspect_ratio:
            d["aspect_ratio"] = self.aspect_ratio
        return d


class VideoGallery(_Widget):
    """Responsive video gallery for generated clips or walkthroughs."""

    _type = "video_gallery"

    def __init__(
        self,
        videos: list[str | dict[str, Any] | Video] | None = None,
        *,
        data: str | None = None,
        title: str | None = None,
        columns: int | None = None,
    ) -> None:
        self.videos = videos or []
        self.data = data
        self.title = title
        self.columns = columns

    def _serialize_video(self, video: str | dict[str, Any] | Video) -> dict[str, Any]:
        if isinstance(video, Video):
            d = video.to_dict()
            d.pop("type", None)
            return d
        if isinstance(video, str):
            return {"src": video}
        return dict(video)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self._type,
            "videos": [self._serialize_video(video) for video in self.videos],
        }
        if self.data:
            d["data"] = self.data
        if self.title:
            d["title"] = self.title
        if self.columns is not None:
            d["columns"] = self.columns
        return d


class ActionCard(_Widget):
    """Clickable card that starts chat, opens a workflow, or navigates to a page.

    ``workflow=`` opens the workflow launcher. Pass either the workflow object
    returned by ``app.workflow(...)`` or its string name. Add ``input=`` to
    start the workflow immediately with that input; ``payload=`` is kept as a
    wire-format alias.
    """

    _type = "action_card"

    def __init__(
        self,
        label: str,
        *,
        description: str | None = None,
        icon: str | None = None,
        image: str | None = None,
        prompt: str | None = None,
        workflow: Any | None = None,
        page: Any | None = None,
        primary: bool = False,
        input: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.label = label
        self.description = description
        self.icon = icon
        self.image = image
        self.target = _action_target(prompt, workflow, page)
        if input and payload:
            raise ValueError("ActionCard accepts input= or payload=, not both")
        if (input or payload) and (self.target is None or self.target[0] != "workflow"):
            raise ValueError("ActionCard input is only supported with workflow=")
        self.primary = primary
        self.payload = input or payload

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "label": self.label}
        if self.description:
            d["description"] = self.description
        if self.icon:
            d["icon"] = self.icon
        if self.image:
            d["image"] = self.image
        if self.target:
            d["target"], d["value"] = self.target
        if self.primary:
            d["primary"] = True
        if self.payload:
            d["payload"] = dict(self.payload)
        return d


class Button(_Widget):
    """Design-system button that can invoke an app action."""

    _type = "button"

    def __init__(
        self,
        label: str,
        *,
        on_click: Any | None = None,
        payload: dict[str, Any] | None = None,
        primary: bool = False,
    ) -> None:
        self.label = label
        self.on_click = on_click
        self.payload = payload or {}
        self.primary = primary

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "label": self.label}
        if self.on_click is not None:
            action_name = getattr(self.on_click, "_cpsl_action_name", None)
            if not action_name and isinstance(self.on_click, str):
                action_name = self.on_click
            if not action_name:
                raise ValueError("Button on_click must be an @app.action handler or action name")
            d["target"] = "action"
            d["value"] = action_name
        if self.payload:
            d["payload"] = dict(self.payload)
        if self.primary:
            d["primary"] = True
        return d


class GalleryCard(ActionCard):
    """Alias for image-forward home cards."""

    _type = "gallery_card"


class Toggle(_Widget):
    """Boolean toggle switch bound to a setting."""

    _type = "toggle"

    def __init__(self, label: str, *, setting: str) -> None:
        self.label = label
        self.setting = setting

    def to_dict(self) -> dict[str, Any]:
        return {"type": self._type, "label": self.label, "setting": self.setting}


class TextInput(_Widget):
    """Text input — bound to a setting or used standalone in workflow forms.

    Pass ``setting`` for settings-backed inputs, or ``name`` for workflow
    form fields.
    """

    _type = "text_input"

    def __init__(
        self,
        label: str = "",
        *,
        name: str | None = None,
        setting: str | None = None,
        multiline: bool = False,
        placeholder: str | None = None,
        required: bool = False,
    ) -> None:
        self.label = label
        self.name = name
        self.setting = setting
        self.multiline = multiline
        self.placeholder = placeholder
        self.required = required

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.label:
            d["label"] = self.label
        if self.name is not None:
            d["name"] = self.name
        if self.setting is not None:
            d["setting"] = self.setting
        if self.multiline:
            d["multiline"] = True
        if self.placeholder is not None:
            d["placeholder"] = self.placeholder
        if self.required:
            d["required"] = True
        return d


class NumberInput(_Widget):
    """Numeric input — bound to a setting or used standalone in workflow forms."""

    _type = "number_input"

    def __init__(
        self,
        label: str = "",
        *,
        name: str | None = None,
        setting: str | None = None,
        min: int | float | None = None,
        max: int | float | None = None,
        step: int | float | None = None,
        required: bool = False,
    ) -> None:
        self.label = label
        self.name = name
        self.setting = setting
        self.min = min
        self.max = max
        self.step = step
        self.required = required

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.label:
            d["label"] = self.label
        if self.name is not None:
            d["name"] = self.name
        if self.setting is not None:
            d["setting"] = self.setting
        if self.min is not None:
            d["min"] = self.min
        if self.max is not None:
            d["max"] = self.max
        if self.step is not None:
            d["step"] = self.step
        if self.required:
            d["required"] = True
        return d


class Select(_Widget):
    """Dropdown select — bound to a setting or used standalone in workflow forms."""

    _type = "select"

    def __init__(
        self,
        label: str = "",
        *,
        name: str | None = None,
        setting: str | None = None,
        options: list[str] | None = None,
        default: str | None = None,
        required: bool = False,
    ) -> None:
        self.label = label
        self.name = name
        self.setting = setting
        self.options = options
        self.default = default
        self.required = required

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.label:
            d["label"] = self.label
        if self.name is not None:
            d["name"] = self.name
        if self.setting is not None:
            d["setting"] = self.setting
        if self.options is not None:
            d["options"] = list(self.options)
        if self.default is not None:
            d["default"] = self.default
        if self.required:
            d["required"] = True
        return d


class TaskBoardColumn:
    """A single column in a TaskBoard, grouping tasks by status."""

    def __init__(self, label: str, statuses: list[str]) -> None:
        self.label = label
        self.statuses = statuses

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "statuses": list(self.statuses)}


class TaskBoard(_Widget):
    """Kanban board of tasks for the current app.

    Tasks are fetched from the gateway's task API and bucketed into columns
    by status. Defaults to Pending / Running / Completed / Failed columns;
    pass ``columns`` to override.

    ``filter`` is forwarded as query parameters to the tasks endpoint, so
    keys like ``task_name``, ``session_id``, or ``status`` all work.
    """

    _type = "task_board"

    def __init__(
        self,
        *,
        title: str | None = None,
        filter: dict[str, Any] | None = None,
        columns: list[TaskBoardColumn] | None = None,
        refresh_ms: int = 5000,
    ) -> None:
        self.title = title
        self.filter = filter
        self.columns = columns
        self.refresh_ms = refresh_ms

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "refresh_ms": self.refresh_ms}
        if self.title is not None:
            d["title"] = self.title
        if self.filter:
            d["filter"] = dict(self.filter)
        if self.columns:
            d["columns"] = [c.to_dict() for c in self.columns]
        return d


class FileBrowser(_Widget):
    """Mounted filesystem manager for app pages.

    The browser is scoped to an app filesystem mount (for example ``/data``)
    and renders list, preview/download, upload, mkdir, rename, and delete
    controls in the Capsule UI.
    """

    _type = "file_browser"

    def __init__(
        self,
        *,
        mount: str,
        path: str = "/",
        title: str | None = None,
        scope: str = "",
        allow_upload: bool = True,
        allow_delete: bool = True,
        allow_rename: bool = True,
        allow_mkdir: bool = True,
        fill: bool = False,
    ) -> None:
        if not mount or not mount.startswith("/"):
            raise ValueError("FileBrowser mount must be an absolute app path, e.g. '/data'")
        if not path.startswith("/"):
            raise ValueError("FileBrowser path must start with '/'")
        if scope and scope not in {"user", "owner"}:
            raise ValueError("FileBrowser scope must be 'user', 'owner', or empty")
        self.mount = mount.rstrip("/") or "/"
        self.path = path
        self.title = title
        self.scope = scope
        self.allow_upload = allow_upload
        self.allow_delete = allow_delete
        self.allow_rename = allow_rename
        self.allow_mkdir = allow_mkdir
        self.fill = fill

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "type": self._type,
            "mount": self.mount,
            "path": self.path,
            "scope": self.scope,
            "allow_upload": self.allow_upload,
            "allow_delete": self.allow_delete,
            "allow_rename": self.allow_rename,
            "allow_mkdir": self.allow_mkdir,
            "fill": self.fill,
        }
        if self.title is not None:
            d["title"] = self.title
        return d


class ChatPanel(_Widget):
    """Placeholder for the active chat session inside ``@app.chat_page()``.

    ``ChatPanel`` does not create a separate conversation. The hosted UI
    replaces it with the normal chat stream/composer for the active session.
    """

    _type = "chat_panel"

    def __init__(
        self,
        *,
        title: str | None = None,
        placeholder: str | None = None,
        height: int | None = None,
        show_header: bool = True,
    ) -> None:
        if height is not None and height <= 0:
            raise ValueError("ChatPanel height must be positive")
        self.title = title
        self.placeholder = placeholder
        self.height = height
        self.show_header = show_header

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "show_header": self.show_header}
        if self.title is not None:
            d["title"] = self.title
        if self.placeholder is not None:
            d["placeholder"] = self.placeholder
        if self.height is not None:
            d["height"] = self.height
        return d


# ---------------------------------------------------------------------------
# Workflow DSL widgets
# ---------------------------------------------------------------------------


class WorkflowShell(_Widget):
    """Top-level container for a workflow launcher UI.

    Wraps form sections, action bars, and status displays into a single
    cohesive layout that the frontend renders as the workflow's launch
    surface.
    """

    _type = "workflow_shell"

    def __init__(
        self,
        title: str = "",
        *,
        children: list[_Widget] | None = None,
    ) -> None:
        self.title = title
        self.children = children or []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.title:
            d["title"] = self.title
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


class FormSection(_Widget):
    """Labelled group of form fields inside a workflow shell."""

    _type = "form_section"

    def __init__(
        self,
        label: str = "",
        *,
        children: list[_Widget] | None = None,
    ) -> None:
        self.label = label
        self.children = children or []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.label:
            d["label"] = self.label
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


class TextArea(_Widget):
    """Multi-line text input for workflow forms."""

    _type = "text_area"

    def __init__(
        self,
        *,
        name: str,
        label: str = "",
        placeholder: str = "",
        required: bool = False,
        rows: int = 4,
    ) -> None:
        self.name = name
        self.label = label
        self.placeholder = placeholder
        self.required = required
        self.rows = rows

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "name": self.name}
        if self.label:
            d["label"] = self.label
        if self.placeholder:
            d["placeholder"] = self.placeholder
        if self.required:
            d["required"] = True
        if self.rows != 4:
            d["rows"] = self.rows
        return d


class FileInput(_Widget):
    """File upload input for workflow forms."""

    _type = "file_input"

    def __init__(
        self,
        *,
        name: str,
        label: str = "",
        accept: list[str] | None = None,
        required: bool = False,
        multiple: bool = False,
    ) -> None:
        self.name = name
        self.label = label
        self.accept = accept
        self.required = required
        self.multiple = multiple

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "name": self.name}
        if self.label:
            d["label"] = self.label
        if self.accept:
            d["accept"] = list(self.accept)
        if self.required:
            d["required"] = True
        if self.multiple:
            d["multiple"] = True
        return d


class ImageInput(_Widget):
    """Image upload input with preview for workflow forms."""

    _type = "image_input"

    def __init__(
        self,
        *,
        name: str,
        label: str = "",
        required: bool = False,
        multiple: bool = False,
    ) -> None:
        self.name = name
        self.label = label
        self.required = required
        self.multiple = multiple

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "name": self.name}
        if self.label:
            d["label"] = self.label
        if self.required:
            d["required"] = True
        if self.multiple:
            d["multiple"] = True
        return d


class UrlInput(_Widget):
    """Single URL input with validation for workflow forms."""

    _type = "url_input"

    def __init__(
        self,
        *,
        name: str,
        label: str = "",
        placeholder: str = "",
        required: bool = False,
    ) -> None:
        self.name = name
        self.label = label
        self.placeholder = placeholder
        self.required = required

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "name": self.name}
        if self.label:
            d["label"] = self.label
        if self.placeholder:
            d["placeholder"] = self.placeholder
        if self.required:
            d["required"] = True
        return d


class UrlListInput(_Widget):
    """Multi-URL input (add/remove list) for workflow forms."""

    _type = "url_list_input"

    def __init__(
        self,
        *,
        name: str,
        label: str = "",
        placeholder: str = "",
    ) -> None:
        self.name = name
        self.label = label
        self.placeholder = placeholder

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "name": self.name}
        if self.label:
            d["label"] = self.label
        if self.placeholder:
            d["placeholder"] = self.placeholder
        return d


class CheckboxGroup(_Widget):
    """Multi-select checkbox group for workflow forms."""

    _type = "checkbox_group"

    def __init__(
        self,
        *,
        name: str,
        label: str = "",
        options: list[str] | None = None,
        default: list[str] | None = None,
    ) -> None:
        self.name = name
        self.label = label
        self.options = options or []
        self.default = default or []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "name": self.name}
        if self.label:
            d["label"] = self.label
        if self.options:
            d["options"] = list(self.options)
        if self.default:
            d["default"] = list(self.default)
        return d


class SubmitButton(_Widget):
    """Button that submits form data to a workflow action handler.

    ``action="start"`` triggers ``@workflow.start()``.  Any other value
    triggers ``@workflow.action(name)`` with the matching name.
    """

    _type = "submit_button"

    def __init__(
        self,
        label: str,
        *,
        action: str = "start",
        primary: bool = False,
    ) -> None:
        self.label = label
        self.action = action
        self.primary = primary

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type, "label": self.label, "action": self.action}
        if self.primary:
            d["primary"] = True
        return d


class ActionBar(_Widget):
    """Horizontal bar of action buttons at the bottom of a workflow shell."""

    _type = "action_bar"

    def __init__(self, *, children: list[_Widget] | None = None) -> None:
        self.children = children or []

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


class RunStatus(_Widget):
    """Displays the current status of a workflow run (active, idle, etc.)."""

    _type = "run_status"

    def to_dict(self) -> dict[str, Any]:
        return {"type": self._type}


class RunList(_Widget):
    """Lists existing workflow run instances for ``mode="runs"`` workflows."""

    _type = "run_list"

    def __init__(self, *, empty_message: str = "No runs yet") -> None:
        self.empty_message = empty_message

    def to_dict(self) -> dict[str, Any]:
        return {"type": self._type, "empty_message": self.empty_message}


class EmptyState(_Widget):
    """Placeholder shown when a workflow has no active session or runs."""

    _type = "empty_state"

    def __init__(
        self,
        message: str = "",
        *,
        icon: str = "",
    ) -> None:
        self.message = message
        self.icon = icon

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"type": self._type}
        if self.message:
            d["message"] = self.message
        if self.icon:
            d["icon"] = self.icon
        return d
