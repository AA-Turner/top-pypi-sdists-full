"""Command vocabulary — DERIVED from ``matrx_scraper.ai_browser.actions`` (S2 §7).

Command names are identical to the ``actions.py`` function names; parameters are
identical except for the documented divergences (S2 §7.3). The **result models are
imported, not re-declared** — a second declaration of any of these shapes is a
defect under the one-deserializer law (S2 §7.2). The ``FakeWorker`` and the real
worker import the same classes.

Divergences honored here:
  * D1 — no ``session_id`` parameter on any command (the worker serves one run).
  * D2 — ``screenshot`` is not a command; it is ``capture``.
  * D3 — ``eval_js`` drops ``allow_eval_js``; the run policy decides.
  * D4 — ``close`` is replaced by ``shutdown``.
  * D5 — ``navigate`` drops ``user_agent`` / ``viewport`` / ``proxy`` (bootstrap-time
    profile identity); sending one is ``parameter_not_available_on_persistent_run``.
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

# Result models — IMPORTED verbatim. Never re-declared.
from matrx_scraper.ai_browser.actions import (  # noqa: F401
    ClickResult,
    EvalJsResult,
    FillResult,
    GetElementResult,
    GetHtmlResult,
    GetTextResult,
    NavigateResult,
    QuerySelectorsResult,
    ScrollResult,
    SelectOptionResult,
    TypeResult,
    WaitForResult,
    _BaseResult,
)


class _Cmd(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NavigateCommand(_Cmd):
    command: Literal["navigate"] = "navigate"
    url: str
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "load"
    timeout_ms: int = 30_000
    extract_text: bool = False
    # D5 (S2 §7.3): these create a session in actions.py; on a persistent run they
    # are bootstrap-time profile identity and may NOT change mid-session. They are
    # ACCEPTED into the schema only so the worker can reject them with the typed
    # ``parameter_not_available_on_persistent_run`` rather than a bare pydantic 422.
    user_agent: str | None = None
    viewport: dict[str, int] | None = None
    proxy: str | None = None


class ClickCommand(_Cmd):
    command: Literal["click"] = "click"
    selector: str
    wait_after_ms: int = 0
    timeout_ms: int = 10_000


class FillCommand(_Cmd):
    command: Literal["fill"] = "fill"
    selector: str
    value: str
    timeout_ms: int = 10_000


class TypeTextCommand(_Cmd):
    command: Literal["type_text"] = "type_text"
    selector: str
    text: str
    clear_first: bool = False
    press_enter: bool = False
    timeout_ms: int = 10_000


class SelectOptionCommand(_Cmd):
    command: Literal["select_option"] = "select_option"
    selector: str
    value: str | None = None
    label: str | None = None
    timeout_ms: int = 10_000


class WaitForCommand(_Cmd):
    command: Literal["wait_for"] = "wait_for"
    selector: str | None = None
    text: str | None = None
    state: Literal["visible", "attached", "detached", "hidden"] = "visible"
    timeout_ms: int = 10_000


class GetElementCommand(_Cmd):
    command: Literal["get_element"] = "get_element"
    selector: str
    include_html: bool = False


class QuerySelectorsCommand(_Cmd):
    command: Literal["query_selectors"] = "query_selectors"
    selectors: list[str]
    attributes: list[str] | None = None
    limit_per_selector: int = 50


class EvalJsCommand(_Cmd):
    command: Literal["eval_js"] = "eval_js"
    expression: str


class ScrollCommand(_Cmd):
    command: Literal["scroll"] = "scroll"
    direction: Literal["up", "down", "top", "bottom"] = "down"
    pixels: int = 500
    selector: str | None = None


class GetHtmlCommand(_Cmd):
    command: Literal["get_html"] = "get_html"
    cap: int = 500_000


class GetTextCommand(_Cmd):
    command: Literal["get_text"] = "get_text"
    selector: str = "body"
    cap: int = 50_000


# ── Additions required by PLAN.md §Tabs, popups, downloads, and dialogs (S2 §7.1) ──
# The single-page ``actions.py`` pointer cannot express these.


class ActivatePageResult(_BaseResult):
    active_page_id: str | None = None
    url: str | None = None
    title: str | None = None


class ClosePageResult(_BaseResult):
    closed: bool = False
    active_page_id: str | None = None


class HandleDialogResult(_BaseResult):
    dialog_id: str | None = None
    handled: bool = False


class DownloadResult(_BaseResult):
    download_id: str | None = None
    suggested_filename: str | None = None
    state: str | None = None
    byte_count: int | None = None
    content_hash: str | None = None
    uploaded: bool = False


class ActivatePageCommand(_Cmd):
    command: Literal["activate_page"] = "activate_page"
    target_page_id: str


class ClosePageCommand(_Cmd):
    command: Literal["close_page"] = "close_page"
    target_page_id: str


class HandleDialogCommand(_Cmd):
    command: Literal["handle_dialog"] = "handle_dialog"
    dialog_id: str
    action: Literal["accept", "dismiss"]
    prompt_text: str | None = None


class WaitForDownloadCommand(_Cmd):
    command: Literal["wait_for_download"] = "wait_for_download"
    download_id: str
    timeout_ms: int = 60_000


BrowserCommand = Annotated[
    Union[
        NavigateCommand,
        ClickCommand,
        FillCommand,
        TypeTextCommand,
        SelectOptionCommand,
        WaitForCommand,
        GetElementCommand,
        QuerySelectorsCommand,
        EvalJsCommand,
        ScrollCommand,
        GetHtmlCommand,
        GetTextCommand,
        ActivatePageCommand,
        ClosePageCommand,
        HandleDialogCommand,
        WaitForDownloadCommand,
    ],
    Field(discriminator="command"),
]

# Union of every result model a command can produce (S2 §5.3 CommandResponse.result).
BrowserCommandResult = Union[
    NavigateResult,
    ClickResult,
    FillResult,
    TypeResult,
    SelectOptionResult,
    WaitForResult,
    GetElementResult,
    QuerySelectorsResult,
    EvalJsResult,
    ScrollResult,
    GetHtmlResult,
    GetTextResult,
    ActivatePageResult,
    ClosePageResult,
    HandleDialogResult,
    DownloadResult,
]

# The set of command names the worker recognizes — used to reject an unknown
# discriminator with ``command_not_supported`` rather than a pydantic 422 blob.
KNOWN_COMMANDS: frozenset[str] = frozenset(
    {
        "navigate",
        "click",
        "fill",
        "type_text",
        "select_option",
        "wait_for",
        "get_element",
        "query_selectors",
        "eval_js",
        "scroll",
        "get_html",
        "get_text",
        "activate_page",
        "close_page",
        "handle_dialog",
        "wait_for_download",
    }
)
