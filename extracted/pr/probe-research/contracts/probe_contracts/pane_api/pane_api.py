"""PaneApi: what a pane's code may call and the caps it lives under, read from `pane_api.json`.

The one list: codegen draws the server's enums (`app/projects/panes/generated/pane_api.py`) and the
dashboard's (`dashboard/src/shared/generated/pane-api.generated.ts`) from it. Stdlib only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PANE_API_PATH = Path(__file__).with_name("pane_api.json")


@dataclass(frozen=True)
class PaneApiName:
    """One named member of a list (a call, a state, a reason), with why it exists."""

    name: str
    doc: str


@dataclass(frozen=True)
class PaneApiCap:
    """One cap: its snake_case name, its value and its unit in words."""

    name: str
    value: int
    doc: str


@dataclass(frozen=True)
class PanePreviewPane:
    """A project's one automatic preview pane: its slug, the floor template's root attribute, and the
    most words its `.about` line holds."""

    slug: str
    floor_marker: str
    line_max_words: int
    doc: str


@dataclass(frozen=True)
class PaneApi:
    """The parsed `pane_api.json`."""

    doc: str
    #: The recipe's `runs` value that means "the runs in view".
    run_scope: str
    #: `PROBE.<name>('<recipe id>')`: one per source kind, same names.
    data_calls: tuple[PaneApiName, ...]
    #: `PROBE.<name>(file)`: read a file through the host bridge.
    file_calls: tuple[PaneApiName, ...]
    #: What a rejected file call's error says.
    file_errors: tuple[PaneApiName, ...]
    #: `PROBE.<name>(...)` calls that read no recipe entry and no file (`onData`, `open`).
    page_calls: tuple[PaneApiName, ...]
    #: The one key of a `PROBE.open` ref: what it opens.
    open_refs: tuple[PaneApiName, ...]
    #: What a refused `PROBE.open` rejects with.
    open_errors: tuple[PaneApiName, ...]
    #: A resolved entry's `state`.
    states: tuple[PaneApiName, ...]
    #: Why an entry is `partial`.
    reasons: tuple[PaneApiName, ...]
    #: What the render check at push answered.
    check_statuses: tuple[PaneApiName, ...]
    #: A state the render check draws the pane in.
    check_states: tuple[PaneApiName, ...]
    #: A project's canvas preview choice (`project_previews`).
    preview_states: tuple[PaneApiName, ...]
    #: Who last wrote a pane or a preview choice, from the credential.
    writer_kinds: tuple[PaneApiName, ...]
    #: The `code` of a preview refusal.
    preview_error_codes: tuple[PaneApiName, ...]
    #: The one automatic preview pane (slug, floor marker, line cap).
    preview_pane: PanePreviewPane
    caps: tuple[PaneApiCap, ...]

    @classmethod
    def load(cls, path: Path = PANE_API_PATH) -> PaneApi:
        raw = json.loads(path.read_text(encoding="utf-8"))

        def read_names(key: str) -> tuple[PaneApiName, ...]:
            return tuple(PaneApiName(item["name"], item["doc"]) for item in raw[key])

        return cls(
            doc=raw["doc"],
            run_scope=raw["run_scope"],
            data_calls=read_names("data_calls"),
            file_calls=read_names("file_calls"),
            file_errors=read_names("file_errors"),
            page_calls=read_names("page_calls"),
            open_refs=read_names("open_refs"),
            open_errors=read_names("open_errors"),
            states=read_names("states"),
            reasons=read_names("reasons"),
            check_statuses=read_names("check_statuses"),
            check_states=read_names("check_states"),
            preview_states=read_names("preview_states"),
            writer_kinds=read_names("writer_kinds"),
            preview_error_codes=read_names("preview_error_codes"),
            preview_pane=PanePreviewPane(
                slug=raw["preview_pane"]["slug"],
                floor_marker=raw["preview_pane"]["floor_marker"],
                line_max_words=int(raw["preview_pane"]["line_max_words"]),
                doc=raw["preview_pane"]["doc"],
            ),
            caps=tuple(PaneApiCap(c["name"], int(c["value"]), c["doc"]) for c in raw["caps"]),
        )
