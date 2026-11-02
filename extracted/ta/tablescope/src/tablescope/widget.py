from __future__ import annotations

import threading
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from anywidget import AnyWidget
from traitlets import Bool, Dict, Int, Unicode

from tablescope._frontend import CSS, JS
from tablescope.engine import (
    DEFAULT_MAX_CELL_BYTES,
    FilterSpec,
    SortSpec,
    TableEngine,
)


class TableScopeWidget(AnyWidget):
    _esm = JS
    _css = CSS

    initial_payload = Dict({}).tag(sync=True)
    page_size = Int(100).tag(sync=True)
    total_rows = Int(0).tag(sync=True)
    supports_random_access = Bool(True).tag(sync=True)
    package_version = Unicode("0.0.0").tag(sync=True)

    def __init__(
        self,
        source: Any,
        *,
        page_size: int = 100,
        frequency_limit: int = 25,
        max_cell_bytes: int = DEFAULT_MAX_CELL_BYTES,
    ) -> None:
        super().__init__()
        self._engine = TableEngine(
            source,
            page_size=page_size,
            frequency_limit=frequency_limit,
            max_cell_bytes=max_cell_bytes,
        )
        self.page_size = self._engine.page_size
        self.total_rows = self._engine.total_rows
        self.supports_random_access = self._engine.supports_random_access
        self.package_version = self._package_version()
        self.initial_payload = self._engine.initial_payload()
        self.on_msg(self._handle_frontend_message)

    def _handle_frontend_message(
        self, _widget: Any, content: dict[str, Any], _buffers: Any
    ) -> None:
        message_type = content.get("type")
        request_id = content.get("request_id")
        payload = content.get("payload", {})

        try:
            if message_type == "fetch_rows":
                result = self._engine.fetch_rows(
                    offset=int(payload.get("offset", 0)),
                    limit=int(payload.get("limit", self.page_size)),
                    sort=self._parse_sort(payload.get("sort", [])),
                    filters=self._parse_filters(payload.get("filters", [])),
                )
            elif message_type == "fetch_cell":
                result = self._engine.fetch_cell(
                    offset=int(payload.get("offset", 0)),
                    column=str(payload["column"]),
                    sort=self._parse_sort(payload.get("sort", [])),
                    filters=self._parse_filters(payload.get("filters", [])),
                )
            elif message_type == "jump_to_fraction":
                result = self._engine.jump_to_fraction(
                    float(payload.get("fraction", 0.0)),
                    limit=int(payload.get("limit", self.page_size)),
                    sort=self._parse_sort(payload.get("sort", [])),
                    filters=self._parse_filters(payload.get("filters", [])),
                )
            elif message_type == "describe_column":
                result = self._engine.describe_column(
                    str(payload["column"]),
                    filters=self._parse_filters(payload.get("filters", [])),
                )
            elif message_type == "value_counts":
                result = self._engine.value_counts(
                    str(payload["column"]),
                    limit=int(payload.get("limit", 25)),
                    filters=self._parse_filters(payload.get("filters", [])),
                )
            elif message_type == "histogram":
                result = self._engine.histogram(
                    str(payload["column"]),
                    bin_count=int(payload.get("bin_count", 20)),
                    filters=self._parse_filters(payload.get("filters", [])),
                )
            elif message_type == "add_column":
                column = self._engine.add_column(
                    str(payload["name"]),
                    str(payload["expr"]),
                )
                self._sync_schema()
                result = {"column": column}
            elif message_type == "update_column":
                column = self._engine.update_column(
                    str(payload["name"]),
                    str(payload["expr"]),
                )
                self._sync_schema()
                result = {"column": column}
            elif message_type == "remove_column":
                removed = self._engine.remove_column(str(payload["name"]))
                self._sync_schema()
                result = removed
            elif message_type == "stop_server":
                # Acknowledge first, then stop. The shutdown is deferred on a
                # short timer so this response frame flushes to the browser
                # before uvicorn tears down the websocket; otherwise the page
                # can't reliably show its "server stopped" state.
                from tablescope._server_control import request_shutdown

                threading.Timer(0.25, request_shutdown).start()
                result = {"stopped": True}
            else:
                raise ValueError(f"Unknown message type {message_type!r}.")

            self.send(
                {
                    "type": "response",
                    "request_id": request_id,
                    "ok": True,
                    "payload": result,
                }
            )
        except Exception as exc:
            self.send(
                {
                    "type": "response",
                    "request_id": request_id,
                    "ok": False,
                    "error": str(exc),
                }
            )

    def _sync_schema(self) -> None:
        # The derived-column set changed, so the schema did too. Refresh the
        # synced initial_payload (and row count) so a notebook re-render or a
        # fresh frontend sees the current columns.
        self.initial_payload = self._engine.initial_payload()
        self.total_rows = self._engine.total_rows

    def _parse_sort(self, raw_sort: list[dict[str, Any]]) -> list[SortSpec]:
        result: list[SortSpec] = []
        for item in raw_sort:
            column = str(item["column"])
            direction = "desc" if bool(item.get("descending", False)) else "asc"
            result.append(SortSpec(column=column, direction=direction))
        return result

    def _parse_filters(self, raw_filters: list[dict[str, Any]]) -> list[FilterSpec]:
        result: list[FilterSpec] = []
        for item in raw_filters:
            result.append(
                FilterSpec(
                    column=str(item["column"]),
                    operator=str(item["operator"]),
                    value=item.get("value"),
                    value_to=item.get("value_to"),
                )
            )
        return result

    def _package_version(self) -> str:
        try:
            return version("tablescope")
        except PackageNotFoundError:
            return "0.0.0"


def widget(
    source: Any,
    *,
    page_size: int = 100,
    frequency_limit: int = 25,
    max_cell_bytes: int = DEFAULT_MAX_CELL_BYTES,
) -> TableScopeWidget:
    return TableScopeWidget(
        source,
        page_size=page_size,
        frequency_limit=frequency_limit,
        max_cell_bytes=max_cell_bytes,
    )


def view(
    source: Any,
    *,
    page_size: int = 100,
    frequency_limit: int = 25,
    max_cell_bytes: int = DEFAULT_MAX_CELL_BYTES,
):
    # Imported lazily so widget() stays usable in environments (e.g. plain
    # Jupyter) where marimo is not installed.
    import marimo as mo

    return mo.ui.anywidget(
        widget(
            source,
            page_size=page_size,
            frequency_limit=frequency_limit,
            max_cell_bytes=max_cell_bytes,
        )
    )
