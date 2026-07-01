"""Full-screen model browser for searching and switching inference models."""

from __future__ import annotations

import typing as t
from dataclasses import dataclass, field

from rich.text import Text
from textual import on, work
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Static

from dreadnode.app.model_catalog import display_name, infer_provider
from dreadnode.app.tui.screens.base import (
    _bind_status_bar_to_app,
    handle_search_input_key,
    handle_search_input_paste,
    render_search_bar,
)
from dreadnode.app.tui.theme import BRAND, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE, WARNING
from dreadnode.app.tui.widgets.status_bar import StatusBar

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.events import Key, Paste


class SearchModelsCallback(t.Protocol):
    """Async callback for catalog-backed BYOK model searches."""

    async def __call__(
        self,
        query: str | None,
        *,
        filters: dict[str, t.Any] | None = None,
    ) -> list[dict[str, t.Any]]: ...


_TRUE_VALUES = {"1", "true", "yes", "y", "open"}
_FALSE_VALUES = {"0", "false", "no", "n", "closed"}
RESTRICTED_ACCESS_BANNER = (
    "Your org has restricted available models. Contact your org owner for changes."
)


@dataclass(slots=True, frozen=True)
class ModelEntry:
    """A selectable model row in the browser."""

    model_id: str
    name: str
    provider: str
    source: t.Literal["dreadnode", "byok"]
    status: str | None = None
    cost_input: float | None = None
    cost_output: float | None = None
    context_window: int | None = None
    max_output_tokens: int | None = None
    capabilities: tuple[str, ...] = ()
    modalities_input: tuple[str, ...] = ()
    modalities_output: tuple[str, ...] = ()
    knowledge: str | None = None
    release_date: str | None = None
    open_weights: bool | None = None
    order: int | None = None


@dataclass(slots=True, frozen=True)
class ModelSearch:
    """Parsed query text and structured filters for the browser."""

    text: str = ""
    provider: str | None = None
    source: t.Literal["all", "dreadnode", "byok"] = "all"
    open_weights: bool | None = None
    min_context: int | None = None
    max_context: int | None = None
    min_price: float | None = None
    max_price: float | None = None
    capabilities: tuple[str, ...] = field(default_factory=tuple)

    def api_filters(self) -> dict[str, t.Any] | None:
        """Return the subset of filters the catalog API understands."""
        filters = {
            key: value
            for key, value in {
                "provider": self.provider,
                "open_weights": self.open_weights,
                "min_context": self.min_context,
                "max_context": self.max_context,
                "min_price": self.min_price,
                "max_price": self.max_price,
                "capabilities": list(self.capabilities) if self.capabilities else None,
            }.items()
            if value is not None and value != []
        }
        return filters or None


def _provider_label(model_id: str) -> str:
    """Return a human-friendly provider label for a model ID."""
    provider = infer_provider(model_id)
    if provider:
        return provider
    if model_id.startswith("dn/"):
        return "dreadnode"
    if "/" in model_id:
        return model_id.split("/", 1)[0]
    return ""


def _source_label(source: str) -> str:
    if source == "dreadnode":
        return "Dreadnode"
    return "BYOK"


def _format_compact_int(value: int | None) -> str:
    if value is None:
        return "-"
    if value >= 1_000_000:
        return f"{value / 1_000_000:g}m"
    if value >= 1_000:
        return f"{value / 1_000:g}k"
    return str(value)


def _format_context(value: int | None) -> str:
    return _format_compact_int(value)


def _format_compact_number(value: float) -> str:
    rounded_value = round(value, 6)
    if abs(rounded_value) >= 1_000_000:
        return f"{rounded_value / 1_000_000:g}m"
    if abs(rounded_value) >= 1_000:
        return f"{rounded_value / 1_000:g}k"
    if rounded_value.is_integer():
        return str(int(rounded_value))
    return f"{rounded_value:g}"


def _format_price(
    input_cost: float | None,
    output_cost: float | None,
    *,
    source: t.Literal["dreadnode", "byok"],
    inference_credits_per_dollar: float | None,
) -> str:
    if input_cost is None and output_cost is None:
        return "-"

    if source == "dreadnode":
        if not (
            isinstance(inference_credits_per_dollar, int | float)
            and inference_credits_per_dollar > 0
        ):
            return "-"
        input_credits = (
            _format_compact_number(input_cost * inference_credits_per_dollar)
            if input_cost is not None
            else None
        )
        output_credits = (
            _format_compact_number(output_cost * inference_credits_per_dollar)
            if output_cost is not None
            else None
        )
        if input_credits is not None and output_credits is not None:
            return f"{input_credits}/{output_credits} cr"
        value = input_credits if input_credits is not None else output_credits
        return f"{value} cr"

    if input_cost is not None and output_cost is not None:
        return f"${input_cost:g}/${output_cost:g}"
    value = input_cost if input_cost is not None else output_cost
    return f"${value:g}"


def _format_open_weights(value: bool | None) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "-"


def _parse_float_value(raw: t.Any) -> float | None:
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int | float):
        return float(raw)
    return None


def _parse_int_value(raw: t.Any) -> int | None:
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int | float):
        return int(raw)
    return None


def _parse_cost_fields(entry: dict[str, t.Any]) -> tuple[float | None, float | None]:
    cost = entry.get("cost")
    input_cost = cost.get("input") if isinstance(cost, dict) else None
    output_cost = cost.get("output") if isinstance(cost, dict) else None

    parsed_input_cost = _parse_float_value(input_cost)
    if parsed_input_cost is None:
        parsed_input_cost = _parse_float_value(entry.get("cost_input"))

    parsed_output_cost = _parse_float_value(output_cost)
    if parsed_output_cost is None:
        parsed_output_cost = _parse_float_value(entry.get("cost_output"))

    return (
        parsed_input_cost,
        parsed_output_cost,
    )


def _parse_limit_fields(entry: dict[str, t.Any]) -> tuple[int | None, int | None]:
    limits = entry.get("limits")
    context_window = limits.get("context") if isinstance(limits, dict) else None
    max_output = limits.get("output") if isinstance(limits, dict) else None

    parsed_context_window = _parse_int_value(context_window)
    if parsed_context_window is None:
        parsed_context_window = _parse_int_value(entry.get("context_window"))

    parsed_max_output = _parse_int_value(max_output)
    if parsed_max_output is None:
        parsed_max_output = _parse_int_value(entry.get("max_output"))

    return (
        parsed_context_window,
        parsed_max_output,
    )


def _parse_modalities(entry: dict[str, t.Any]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    modalities = entry.get("modalities")
    if not isinstance(modalities, dict):
        return ((), ())
    raw_input = modalities.get("input")
    raw_output = modalities.get("output")
    return (
        tuple(value for value in raw_input if isinstance(value, str))
        if isinstance(raw_input, list)
        else (),
        tuple(value for value in raw_output if isinstance(value, str))
        if isinstance(raw_output, list)
        else (),
    )


def _max_price(entry: ModelEntry) -> float | None:
    values = [value for value in (entry.cost_input, entry.cost_output) if value is not None]
    if not values:
        return None
    return max(values)


def _parse_scaled_int(raw: str) -> int | None:
    token = raw.strip().lower().replace(",", "").rstrip("+")
    multiplier = 1
    if token.endswith("k"):
        multiplier = 1_000
        token = token[:-1]
    elif token.endswith("m"):
        multiplier = 1_000_000
        token = token[:-1]
    if not token:
        return None
    try:
        return int(float(token) * multiplier)
    except ValueError:
        return None


def _parse_float(raw: str) -> float | None:
    token = raw.strip().lower().replace(",", "").removeprefix("$").removesuffix("+")
    if not token:
        return None
    try:
        return float(token)
    except ValueError:
        return None


def _parse_context_filter(raw: str) -> tuple[int | None, int | None] | None:
    token = raw.strip().lower()
    if not token:
        return None
    if token.startswith(">="):
        value = _parse_scaled_int(token[2:])
        return (value, None) if value is not None else None
    if token.startswith(">"):
        value = _parse_scaled_int(token[1:])
        return (value, None) if value is not None else None
    if token.startswith("<="):
        value = _parse_scaled_int(token[2:])
        return (None, value) if value is not None else None
    if token.startswith("<"):
        value = _parse_scaled_int(token[1:])
        return (None, value) if value is not None else None
    if token.startswith("="):
        value = _parse_scaled_int(token[1:])
        return (value, value) if value is not None else None
    value = _parse_scaled_int(token)
    return (value, None) if value is not None else None


def _parse_price_filter(raw: str) -> tuple[float | None, float | None] | None:
    token = raw.strip().lower()
    if not token:
        return None
    if token.startswith(">="):
        value = _parse_float(token[2:])
        return (value, None) if value is not None else None
    if token.startswith(">"):
        value = _parse_float(token[1:])
        return (value, None) if value is not None else None
    if token.startswith("<="):
        value = _parse_float(token[2:])
        return (None, value) if value is not None else None
    if token.startswith("<"):
        value = _parse_float(token[1:])
        return (None, value) if value is not None else None
    if token.startswith("="):
        value = _parse_float(token[1:])
        return (value, value) if value is not None else None
    value = _parse_float(token)
    return (None, value) if value is not None else None


def _normalize_source(raw: str) -> t.Literal["all", "dreadnode", "byok"] | None:
    token = raw.strip().lower()
    if token in {"all", "*"}:
        return "all"
    if token in {"dn", "dreadnode", "hosted"}:
        return "dreadnode"
    if token in {"byok", "provider", "providers"}:
        return "byok"
    return None


def _parse_search_query(raw: str) -> ModelSearch:
    """Parse search text into free text plus structured filter tokens."""
    terms: list[str] = []
    provider: str | None = None
    source: t.Literal["all", "dreadnode", "byok"] = "all"
    open_weights: bool | None = None
    min_context: int | None = None
    max_context: int | None = None
    min_price: float | None = None
    max_price: float | None = None
    capabilities: list[str] = []

    for token in raw.split():
        if ":" not in token:
            terms.append(token)
            continue

        key, value = token.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if not value:
            terms.append(token)
            continue

        if key in {"provider", "prov"}:
            provider = value.lower()
            continue

        if key in {"source", "src"}:
            normalized_source = _normalize_source(value)
            if normalized_source is None:
                terms.append(token)
            else:
                source = normalized_source
            continue

        if key in {"open", "open_weights", "weights"}:
            normalized = value.lower()
            if normalized in _TRUE_VALUES:
                open_weights = True
                continue
            if normalized in _FALSE_VALUES:
                open_weights = False
                continue
            terms.append(token)
            continue

        if key in {"ctx", "context"}:
            parsed = _parse_context_filter(value)
            if parsed is None:
                terms.append(token)
                continue
            parsed_min, parsed_max = parsed
            min_context = parsed_min if parsed_min is not None else min_context
            max_context = parsed_max if parsed_max is not None else max_context
            continue

        if key in {"price", "cost"}:
            parsed = _parse_price_filter(value)
            if parsed is None:
                terms.append(token)
                continue
            parsed_min, parsed_max = parsed
            min_price = parsed_min if parsed_min is not None else min_price
            max_price = parsed_max if parsed_max is not None else max_price
            continue

        if key in {"cap", "caps", "capability"}:
            capabilities.extend(part.lower() for part in value.split(",") if part.strip())
            continue

        terms.append(token)

    return ModelSearch(
        text=" ".join(terms).strip(),
        provider=provider,
        source=source,
        open_weights=open_weights,
        min_context=min_context,
        max_context=max_context,
        min_price=min_price,
        max_price=max_price,
        capabilities=tuple(capabilities),
    )


def _build_entries(
    platform_models: list[dict[str, t.Any]],
    byok_models: list[dict[str, t.Any]],
    current_model: str,
    access_restricted: bool = False,
) -> list[ModelEntry]:
    """Build the full model-browser entry list from platform and BYOK sources."""
    hosted: dict[str, ModelEntry] = {}
    byok: dict[str, ModelEntry] = {}

    def parse_order(value: object) -> int | None:
        if isinstance(value, bool):
            return None
        if isinstance(value, int) and value >= 1:
            return value
        if isinstance(value, str) and value.strip():
            try:
                parsed = int(value)
            except ValueError:
                return None
            return parsed if parsed >= 1 else None
        return None

    for entry in platform_models:
        if not isinstance(entry, dict):
            continue
        model_id = entry.get("id")
        if not isinstance(model_id, str) or not model_id.strip():
            continue
        if not entry.get("enabled", True):
            continue
        input_cost, output_cost = _parse_cost_fields(entry)
        context_window, max_output = _parse_limit_fields(entry)
        modalities_input, modalities_output = _parse_modalities(entry)
        name_raw = entry.get("name")
        name = name_raw if isinstance(name_raw, str) else display_name(model_id)
        status = entry.get("status") if isinstance(entry.get("status"), str) else None
        caps_raw = entry.get("capabilities")
        capabilities = caps_raw if isinstance(caps_raw, list) else []
        hosted[model_id] = ModelEntry(
            model_id=model_id,
            name=name,
            provider=_provider_label(model_id),
            source="dreadnode",
            status=status,
            cost_input=input_cost,
            cost_output=output_cost,
            context_window=context_window,
            max_output_tokens=max_output,
            capabilities=tuple(
                value for value in capabilities if isinstance(value, str) and value.strip()
            ),
            modalities_input=modalities_input,
            modalities_output=modalities_output,
            knowledge=entry.get("knowledge") if isinstance(entry.get("knowledge"), str) else None,
            release_date=entry.get("release_date")
            if isinstance(entry.get("release_date"), str)
            else None,
            open_weights=entry.get("open_weights")
            if isinstance(entry.get("open_weights"), bool)
            else None,
            order=parse_order(entry.get("order")),
        )

    for entry in byok_models:
        if not isinstance(entry, dict):
            continue
        model_id = entry.get("id")
        if not isinstance(model_id, str) or not model_id.strip():
            continue
        if model_id.startswith("dn/"):
            continue
        input_cost, output_cost = _parse_cost_fields(entry)
        context_window, max_output = _parse_limit_fields(entry)
        modalities_input, modalities_output = _parse_modalities(entry)
        name_raw = entry.get("name")
        name = name_raw if isinstance(name_raw, str) else display_name(model_id)
        provider = entry.get("provider") if isinstance(entry.get("provider"), str) else None
        status = entry.get("status") if isinstance(entry.get("status"), str) else None
        caps_raw = entry.get("capabilities")
        capabilities = caps_raw if isinstance(caps_raw, list) else []
        byok[model_id] = ModelEntry(
            model_id=model_id,
            name=name,
            provider=provider or _provider_label(model_id),
            source="byok",
            status=status,
            cost_input=input_cost,
            cost_output=output_cost,
            context_window=context_window,
            max_output_tokens=max_output,
            capabilities=tuple(
                value for value in capabilities if isinstance(value, str) and value.strip()
            ),
            modalities_input=modalities_input,
            modalities_output=modalities_output,
            knowledge=entry.get("knowledge") if isinstance(entry.get("knowledge"), str) else None,
            release_date=entry.get("release_date")
            if isinstance(entry.get("release_date"), str)
            else None,
            open_weights=entry.get("open_weights")
            if isinstance(entry.get("open_weights"), bool)
            else None,
        )

    should_add_current_model = not (access_restricted and current_model.startswith("dn/"))
    if (
        should_add_current_model
        and current_model
        and current_model not in hosted
        and current_model not in byok
    ):
        bucket = hosted if current_model.startswith("dn/") else byok
        bucket[current_model] = ModelEntry(
            model_id=current_model,
            name=display_name(current_model),
            provider=_provider_label(current_model),
            source="dreadnode" if current_model.startswith("dn/") else "byok",
        )

    ordered_hosted = sorted(
        enumerate(hosted.values()),
        key=lambda item: (item[1].order is None, item[1].order or 0, item[0]),
    )
    return [*(entry for _index, entry in ordered_hosted), *byok.values()]


def _matches_text(
    entry: ModelEntry,
    query: str,
    *,
    inference_credits_per_dollar: float | None,
) -> bool:
    if not query:
        return True
    haystack = " ".join(
        part.lower()
        for part in [
            entry.name,
            entry.model_id,
            entry.provider,
            _source_label(entry.source),
            entry.status or "",
            _format_context(entry.context_window),
            _format_price(
                entry.cost_input,
                entry.cost_output,
                source=entry.source,
                inference_credits_per_dollar=inference_credits_per_dollar,
            ),
            _format_open_weights(entry.open_weights),
            entry.knowledge or "",
            entry.release_date or "",
            *entry.capabilities,
            *entry.modalities_input,
            *entry.modalities_output,
        ]
        if part
    )
    return query.lower() in haystack


def _filter_entries(
    entries: list[ModelEntry],
    search: ModelSearch | str,
    *,
    inference_credits_per_dollar: float | None = None,
) -> list[ModelEntry]:
    """Filter model entries by free text and structured metadata filters."""
    normalized = _parse_search_query(search) if isinstance(search, str) else search

    results: list[ModelEntry] = []
    for entry in entries:
        if normalized.source not in {"all", entry.source}:
            continue
        if normalized.provider and entry.provider.lower() != normalized.provider.lower():
            continue
        if normalized.open_weights is not None and entry.open_weights != normalized.open_weights:
            continue
        if normalized.capabilities and not set(normalized.capabilities).issubset(
            {capability.lower() for capability in entry.capabilities}
        ):
            continue
        if normalized.min_context is not None and (
            entry.context_window is None or entry.context_window < normalized.min_context
        ):
            continue
        if normalized.max_context is not None and (
            entry.context_window is None or entry.context_window > normalized.max_context
        ):
            continue
        price = _max_price(entry)
        if normalized.min_price is not None and (price is None or price < normalized.min_price):
            continue
        if normalized.max_price is not None and (price is None or price > normalized.max_price):
            continue
        if not _matches_text(
            entry,
            normalized.text,
            inference_credits_per_dollar=inference_credits_per_dollar,
        ):
            continue
        results.append(entry)
    return results


class ModelBrowserScreen(Screen[str | None]):
    """Full-screen searchable browser for supported models."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        # Navigation / selection — declared so the screen drives the cursor
        # even when typing into the search bar (which is a Static, not an
        # Input — see ``on_key`` for typing semantics).
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("pageup", "cursor_page_up", "Page Up", show=False),
        Binding("pagedown", "cursor_page_down", "Page Down", show=False),
        Binding("home", "cursor_home", "Home", show=False),
        Binding("end", "cursor_end", "End", show=False),
        Binding("enter", "select", "Select", show=False),
        Binding("escape", "escape", "Back", show=False),
    ]

    def __init__(
        self,
        *,
        platform_models: list[dict[str, t.Any]],
        byok_models: list[dict[str, t.Any]],
        current_model: str,
        inference_credits_per_dollar: float | None = None,
        access_restricted: bool = False,
        search_models: SearchModelsCallback | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._platform_models = list(platform_models)
        self._seed_byok_models = list(byok_models)
        self._catalog_byok_models = list(byok_models)
        self._current_model = current_model
        self._inference_credits_per_dollar = inference_credits_per_dollar
        self._access_restricted = access_restricted
        self._search_models = search_models
        self._search_loading = False
        self._search_error: str | None = None
        self._search_generation = 0
        self._entries: list[ModelEntry] = _build_entries(
            self._platform_models,
            self._combined_byok_models(),
            self._current_model,
            access_restricted=self._access_restricted,
        )
        self._visible: list[ModelEntry] = list(self._entries)
        self._cursor: int = self._current_index(self._visible)
        self._search_query: str = ""

    def compose(self) -> ComposeResult:
        yield Static(id="models-header")
        yield Static(id="models-restricted-banner", classes="-hidden")
        # The query bar — Static driven by ``self._search_query`` so the
        # DataTable can keep focus and arrow keys navigate without a
        # mouse click (matching sessions.py / capabilities.py). Transient
        # search status (loading, error, short-query hint) is appended
        # inline so we don't reserve an always-on row that's empty most
        # of the time.
        yield Static(id="models-query")
        yield DataTable(id="models-table")
        yield Static(id="models-hint-bar")
        yield StatusBar(id="global-status-bar")

    def on_mount(self) -> None:
        _bind_status_bar_to_app(self, self.query_one("#global-status-bar", StatusBar))
        table = self.query_one("#models-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            "",
            "Name",
            "Provider",
            "Source",
            "Context",
            "Price",
            "Open",
            "Model ID",
        )
        self._render_all()
        # Focus the table at the active model row so arrow keys work
        # immediately without requiring a click (ENG-6260).
        table.focus()
        if self._visible:
            table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)
        if self._search_models is not None:
            self._request_catalog_refresh()

    def set_models(
        self,
        *,
        platform_models: list[dict[str, t.Any]],
        byok_models: list[dict[str, t.Any]],
        current_model: str,
        inference_credits_per_dollar: float | None = None,
        access_restricted: bool,
    ) -> None:
        """Refresh the browser contents from app state."""
        self._platform_models = list(platform_models)
        self._seed_byok_models = list(byok_models)
        self._current_model = current_model
        self._inference_credits_per_dollar = inference_credits_per_dollar
        self._access_restricted = access_restricted
        self._rebuild_entries()
        if not self._search_query:
            self._cursor = self._current_index(self._entries)
        if self.is_mounted:
            self._render_all()

    def on_key(self, event: Key) -> None:
        """Route typed characters into the search query.

        Navigation keys (arrows, enter, escape, page-up/down, home/end) are
        declared in ``BINDINGS`` and fire via ``action_*`` methods. This
        handler only feeds the search bar and lets ``escape`` clear the
        search before the binding's dismiss fires.
        """
        key = event.key

        # Control combos and function keys pass through to BINDINGS / app.
        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        # Escape clears search when active; BINDINGS handles dismiss otherwise.
        if key == "escape" and self._search_query:
            self._search_query = ""
            self._cursor = 0
            self._request_catalog_refresh()
            event.prevent_default()
            event.stop()
            return

        if key == "escape":
            return  # let BINDINGS handle dismiss

        search_result = handle_search_input_key(
            self._search_query, key=key, character=event.character
        )
        if not search_result.handled:
            return
        if search_result.new_query == self._search_query:
            return
        self._search_query = search_result.new_query
        if search_result.cursor_should_reset:
            self._cursor = 0
        self._request_catalog_refresh()
        event.prevent_default()
        event.stop()

    def on_paste(self, event: Paste) -> None:
        """Append bracketed-paste text to the search query."""
        result = handle_search_input_paste(self._search_query, text=event.text)
        if not result.handled:
            return
        self._search_query = result.new_query
        if result.cursor_should_reset:
            self._cursor = 0
        self._request_catalog_refresh()
        event.prevent_default()
        event.stop()

    # ── BINDINGS actions ─────────────────────────────────────────────────

    def action_cursor_up(self) -> None:
        if not self._visible:
            return
        self._cursor = max(0, self._cursor - 1)
        self._apply_cursor_to_table()

    def action_cursor_down(self) -> None:
        if not self._visible:
            return
        self._cursor = min(len(self._visible) - 1, self._cursor + 1)
        self._apply_cursor_to_table()

    def action_cursor_page_up(self) -> None:
        if not self._visible:
            return
        table = self.query_one("#models-table", DataTable)
        table.action_page_up()

    def action_cursor_page_down(self) -> None:
        if not self._visible:
            return
        table = self.query_one("#models-table", DataTable)
        table.action_page_down()

    def action_cursor_home(self) -> None:
        if not self._visible:
            return
        self._cursor = 0
        self._apply_cursor_to_table()

    def action_cursor_end(self) -> None:
        if not self._visible:
            return
        self._cursor = len(self._visible) - 1
        self._apply_cursor_to_table()

    def action_select(self) -> None:
        if not self._visible or not (0 <= self._cursor < len(self._visible)):
            return
        self.dismiss(self._visible[self._cursor].model_id)

    def action_escape(self) -> None:
        # Search-clear is handled in ``on_key`` so escape can intercept it
        # before this binding fires. Reaching here means search is empty —
        # dismiss the screen.
        self.dismiss(None)

    def _apply_cursor_to_table(self) -> None:
        table = self.query_one("#models-table", DataTable)
        if 0 <= self._cursor < len(self._visible):
            table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)
        self._render_query_bar()

    def _current_index(self, entries: list[ModelEntry]) -> int:
        for idx, entry in enumerate(entries):
            if entry.model_id == self._current_model:
                return idx
        return 0

    def _render_all(self) -> None:
        self._render_header()
        self._render_restricted_banner()
        self._render_query_bar()
        self._render_table()
        self._render_hints()

    def _render_restricted_banner(self) -> None:
        banner = self.query_one("#models-restricted-banner", Static)
        if not self._access_restricted:
            banner.update("")
            banner.add_class("-hidden")
            return

        text = Text()
        text.append(RESTRICTED_ACCESS_BANNER, style=WARNING)
        banner.update(text)
        banner.remove_class("-hidden")

    def _render_query_bar(self) -> None:
        text = render_search_bar(
            self._search_query,
            cursor=self._cursor,
            visible_count=len(self._visible),
            placeholder=("Search…  filters: provider:  source:  open:  ctx:  price:  cap:"),
        )
        # Inline transient search status — keeps this row as the single
        # source of truth for query state (no separate always-on Static).
        search = _parse_search_query(self._search_query)
        if search.text and len(search.text.strip()) < 2 and search.api_filters() is None:
            text.append("  type 2+ chars to search the full catalog", style=FG_FAINTEST)
        elif self._search_loading:
            text.append("  searching…", style=FG_MUTED)
        elif self._search_error:
            text.append("  search unavailable", style=FG_MUTED)
        self.query_one("#models-query", Static).update(text)

    def _combined_byok_models(self) -> list[dict[str, t.Any]]:
        results: list[dict[str, t.Any]] = []
        seen: set[str] = set()

        for entry in self._catalog_byok_models:
            model_id = entry.get("id") if isinstance(entry, dict) else None
            if not isinstance(model_id, str) or not model_id.strip() or model_id in seen:
                continue
            seen.add(model_id)
            results.append(dict(entry))

        for entry in self._seed_byok_models:
            model_id = entry.get("id") if isinstance(entry, dict) else None
            if not isinstance(model_id, str) or not model_id.strip() or model_id in seen:
                continue
            seen.add(model_id)
            results.append(dict(entry))

        return results

    def _rebuild_entries(self) -> None:
        self._entries = _build_entries(
            self._platform_models,
            self._combined_byok_models(),
            self._current_model,
            access_restricted=self._access_restricted,
        )

    def _render_header(self) -> None:
        hosted_count = sum(1 for entry in self._entries if entry.source == "dreadnode")
        byok_count = len(self._entries) - hosted_count

        text = Text()
        text.append(" Models", style=f"bold {FG}")
        text.append(f"  {len(self._entries)}", style=FG_MUTED)
        text.append("\n")
        text.append(" Search and filter inference models", style=FG_FAINTEST)
        if self._entries:
            text.append("\n")
            text.append(f" Hosted {hosted_count}", style=FG_SUBTLE)
            text.append(" · ", style=FG_FAINTEST)
            text.append(f"BYOK {byok_count}", style=FG_SUBTLE)
            text.append(" · ", style=FG_FAINTEST)
            text.append("Current ", style=FG_FAINTEST)
            text.append(display_name(self._current_model), style=FG)
        self.query_one("#models-header", Static).update(text)

    def _render_table(self) -> None:
        self._visible = _filter_entries(
            self._entries,
            _parse_search_query(self._search_query),
            inference_credits_per_dollar=self._inference_credits_per_dollar,
        )
        self._cursor = min(self._cursor, max(0, len(self._visible) - 1))
        self._render_query_bar()
        table = self.query_one("#models-table", DataTable)
        table.clear()

        for entry in self._visible:
            is_current = entry.model_id == self._current_model
            marker = Text("\u25cf", style=BRAND) if is_current else Text("")
            # Surface non-"active" platform statuses (e.g. preview, deprecated)
            # inline in the Name cell — the marker dot already conveys active.
            name_text = entry.name
            if entry.status and entry.status.lower() != "active":
                name_text = f"{entry.name}  ({entry.status})"
            name = Text(name_text, style=f"bold {FG}" if is_current else FG)
            source = Text(_source_label(entry.source), style=FG_SUBTLE)

            table.add_row(
                marker,
                name,
                entry.provider or "-",
                source,
                _format_context(entry.context_window),
                _format_price(
                    entry.cost_input,
                    entry.cost_output,
                    source=entry.source,
                    inference_credits_per_dollar=self._inference_credits_per_dollar,
                ),
                _format_open_weights(entry.open_weights),
                entry.model_id,
                key=entry.model_id,
            )

        if self._visible:
            table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)

    def _render_hints(self) -> None:
        text = Text()
        text.append(" ↑↓", style=FG_MUTED)
        text.append(" navigate", style=FG_FAINTEST)
        text.append("  ")
        text.append("Enter", style=FG_MUTED)
        text.append(" select", style=FG_FAINTEST)
        text.append("  ")
        text.append("Filters", style=FG_MUTED)
        text.append(" provider:  open:  ctx:  price:  cap:  source:", style=FG_FAINTEST)
        text.append("  ")
        text.append("Esc", style=FG_MUTED)
        text.append(" clear/close", style=FG_FAINTEST)
        self.query_one("#models-hint-bar", Static).update(text)

    @on(DataTable.RowHighlighted, "#models-table")
    def _on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self._cursor = event.cursor_row
        self._render_query_bar()

    @on(DataTable.RowSelected, "#models-table")
    def _on_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.row_key is None:
            return
        self.dismiss(str(event.row_key.value))

    def _request_catalog_refresh(self) -> None:
        self._search_error = None
        search = _parse_search_query(self._search_query)
        query = search.text.strip() or None
        api_filters = search.api_filters()

        if self._search_models is None or search.source == "dreadnode":
            self._search_loading = False
            self._render_all()
            return

        if query and len(query) < 2 and api_filters is None:
            self._search_loading = False
            self._render_all()
            return

        self._search_generation += 1
        generation = self._search_generation
        self._search_loading = True
        self._render_all()
        self._load_catalog_models(query, api_filters, generation)

    @work(exclusive=True, group="model-browser-search", exit_on_error=False)
    async def _load_catalog_models(
        self,
        query: str | None,
        filters: dict[str, t.Any] | None,
        generation: int,
    ) -> None:
        if self._search_models is None:
            return
        try:
            results = await self._search_models(query, filters=filters)
        except Exception:
            if generation != self._search_generation:
                return
            self._search_loading = False
            self._search_error = "Search failed. Try again."
            if self.is_mounted:
                self._render_all()
            return

        if generation != self._search_generation:
            return

        self._search_loading = False
        self._search_error = None
        self._catalog_byok_models = list(results)
        self._rebuild_entries()
        self._cursor = self._current_index(
            _filter_entries(
                self._entries,
                _parse_search_query(self._search_query),
                inference_credits_per_dollar=self._inference_credits_per_dollar,
            )
        )
        if self.is_mounted:
            self._render_all()
