"""the summary outlines the writer sees: each draft's headings and what the session did to its entity since."""

from __future__ import annotations
import json
import re
from html.parser import HTMLParser
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.store.events import scrub


#: The outline's lines (ARTIFACT-PAGES P3). Wording NEW
#: (fixtures/daemon_prompts/bite/summary-outline.NEW.md).
OUTLINE_HEADER = "# Summaries you keep (outline {digest})"
OUTLINE_ENTITY = "## {kind} {label} · v{version} · {size} characters"
OUTLINE_DRAFT = "- draft: {path} · push: probe summary push {flags}"
OUTLINE_EDITED = "- last edited by {who}, {when}"
OUTLINE_NO_PAGE = "- no page yet"
OUTLINE_HEADINGS = "- headings: {headings}"
OUTLINE_OPENS = "- opens: {opening}"
OUTLINE_SINCE = "- since v{version}: {activity}"
OUTLINE_QUIET = "- since v{version}: nothing recorded"
OUTLINE_DIRTY = "- draft has unpushed edits"
OUTLINE_MISSING = "- draft is gone: probe summary checkout {flags}"
#: The opening paragraph, at most this many characters.
OUTLINE_OPENING_CHARS = 400
#: Headings listed, then "…".
OUTLINE_HEADINGS_SHOWN = 12
#: Kinds of activity listed per entity, then "and N more".
OUTLINE_ACTIVITY_SHOWN = 6


class _PageShape(HTMLParser):
    """An HTML draft's headings and its first paragraph, as plain text: never
    from inside a script, a style, a diagram, a template or a person's mark."""

    _SKIP = frozenset({"script", "style", "svg", "math", "template"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.headings: list[str] = []
        self.opening: str | None = None
        #: Open elements, innermost last: (tag, skipped there).
        self._stack: list[tuple[str, bool]] = []
        self._buf: list[str] | None = None
        self._kind: str | None = None

    def _skipped(self) -> bool:
        return any(skip for _tag, skip in self._stack)

    def handle_starttag(self, tag, attrs) -> None:
        if tag in ("br", "hr", "img", "meta", "link", "input", "wbr"):
            return
        marked = any((n or "").lower() == "data-owner" for n, _v in attrs)
        outside = not self._skipped()
        self._stack.append((tag, tag in self._SKIP or marked))
        if self._buf is None and outside and not marked and (
                tag in ("h1", "h2", "h3", "h4", "h5", "h6") or (tag == "p" and self.opening is None)):
            self._buf, self._kind = [], tag

    def handle_endtag(self, tag) -> None:
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i][0] == tag:
                del self._stack[i:]
                break
        if self._buf is not None and tag == self._kind:
            text = " ".join("".join(self._buf).split())
            if text:
                if tag == "p":
                    self.opening = text
                else:
                    self.headings.append(text)
            self._buf = self._kind = None

    def handle_data(self, data) -> None:
        if self._buf is not None and not self._skipped():
            self._buf.append(data)


#: A kept block in an HTML draft, markers and the person's html between them.
_KEPT_BLOCK = re.compile(r"<!--\s*kept:[^>]*-->.*?<!--\s*/kept\s*-->", re.S)
_KEPT_MARK = re.compile(r"<!--\s*/?kept[^>]*-->")
_SERIES_BLOCK = re.compile(r"<script\b[^>]*data-probe-series[^>]*>.*?</script>", re.S | re.I)


def _shape(text: str, fmt: str) -> tuple[list[str], str | None]:
    """`(headings, opening paragraph)` of a draft."""
    if fmt == "html":
        parser = _PageShape()
        # A person's kept text is theirs: never the page's opening or headings.
        parser.feed(_KEPT_MARK.sub("", _KEPT_BLOCK.sub("", _SERIES_BLOCK.sub("", text))))
        parser.close()
        return parser.headings, parser.opening
    headings: list[str] = []
    opening: str | None = None
    block: list[str] = []
    inside_kept = False
    for line in [*text.splitlines(), ""]:
        stripped = line.strip()
        if stripped.startswith("<!-- kept:"):
            inside_kept = True
        if inside_kept:
            inside_kept = not stripped.startswith("<!-- /kept")
            continue
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
            continue
        if stripped and opening is None and not stripped.startswith((">", "-", "*", "|", "<!--")):
            block.append(stripped)
        elif block and opening is None:
            opening = " ".join(block)
    return headings, opening


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _since_ts(entry: dict) -> float:
    when = entry.get("edited_at")
    if not isinstance(when, str) or not when:
        return 0.0
    from datetime import datetime

    try:
        return datetime.fromisoformat(when.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return 0.0


def _run_names(words: list[str], parsed: precheck.Parsed, output: str | None) -> set[str]:
    """Every spelling of the run a `run start` made: its `--name`, and the id,
    slug and name the command printed."""
    names = {v for v in precheck._strings(parsed.params.get("name")) if v.strip()}
    try:
        value, _end = json.JSONDecoder().raw_decode((output or "").lstrip())
    except ValueError:
        value = None
    if isinstance(value, dict):
        names |= {str(value[k]) for k in ("id", "slug", "name") if value.get(k)}
        names |= {f"id:{value['id']}"} if value.get("id") else set()
    return names


def entity_activity(store, kind: str, ref: str, since: float) -> list[str]:
    """What the session's writes did to the entity since `since` (epoch), from
    the logbook: a conclusion set, a dead end marked or cleared, a new
    experiment under a project, a run started under it and how it ended (a run
    is the entity's when the session started it there), else the command;
    repeated ones counted. Oldest first.
    A run the agent's own code ended, with no write of the daemon's, is not in
    the logbook and is not listed."""
    from probe.shared.notes import summary as summary_cli

    counts: dict[str, int] = {}
    runs: set[str] = set()
    rows = store.db.execute("SELECT argv, at, output FROM writes WHERE status = 'ran' ORDER BY id")
    for row in rows:
        words = _probe_words(row["argv"])
        if not words:
            continue
        try:
            parsed = precheck.parse(words)
        except precheck.ParseError:
            continue
        found = summary_cli.landing(words)
        first = lambda name: next((v for v in precheck._strings(parsed.params.get(name)) if v.strip()), None)  # noqa: E731
        if parsed.path == "run start" and found == (kind, ref):
            runs |= _run_names(words, parsed, row["output"])
        if float(row["at"]) <= since:
            continue
        what: str | None = None
        if parsed.path == "experiment create" and kind == summary_cli.PROJECT and first("project") == ref:
            what = f"new experiment {first('slug') or ''}".strip()
        elif parsed.path in ("run end", "run set") and first("status") and first("run") in runs:
            what = f"run {first('run')} {first('status')}"
        elif found == (kind, ref):
            if parsed.path == "experiment create":
                what = "created"
            elif first("conclusion"):
                what = "conclusion set"
            elif first("dead_end"):
                what = "dead end marked"
            elif parsed.path == "experiment set" and parsed.params.get("clear_dead_end"):
                what = "dead end cleared"
            elif parsed.path == "run start":
                what = "run started"
            else:
                what = parsed.path
        if what:
            counts[what] = counts.get(what, 0) + 1
    items = [w if n == 1 else f"{w} ×{n}" for w, n in counts.items()]
    if len(items) > OUTLINE_ACTIVITY_SHOWN:
        items = [*items[:OUTLINE_ACTIVITY_SHOWN], f"and {len(items) - OUTLINE_ACTIVITY_SHOWN} more"]
    return items


def summary_outline(store) -> str:
    """The outlines of the summaries the writer keeps (`SUMMARY_DRAFTS`), most
    recently touched first, or "": per entity its label and kind, version and
    size, the draft and the push that sends it, who edited it last and when,
    its headings, its opening paragraph, what the session did to it since that
    version, and whether the draft holds unpushed edits. Never the page's text.
    Plain code from the drafts on disk and the logbook."""
    from probe.shared.notes import summary as summary_cli

    blocks: list[str] = []
    drafts = _bound_drafts(_drafts(store))
    for anchor, entry in drafts.items():
        # The anchor is the checkout's own flags (`_anchor_key`): the push must
        # repeat them to find the draft (`_document_path`).
        flags = " ".join(f"--{k} {v}" for k, _, v in (part.partition("=") for part in anchor.split("|")))
        kind = str(entry.get("kind") or anchor.partition("=")[0])
        label = str(entry.get("label") or anchor.partition("=")[2])
        ref = label
        version = int(entry.get("version") or 0)
        path = str(entry.get("path") or "")
        text = _read(path)
        lines = [OUTLINE_ENTITY.format(kind=kind.capitalize(), label=label, version=version,
                                       size=len(text) if text is not None else 0)]
        if text is None:
            lines.append(OUTLINE_MISSING.format(flags=flags))
            blocks.append("\n".join(lines))
            continue
        lines.append(OUTLINE_DRAFT.format(path=path, flags=flags))
        if version and entry.get("edited_at"):
            when = str(entry["edited_at"]).replace("T", " ")[:16]
            lines.append(OUTLINE_EDITED.format(who=entry.get("edited_by") or "someone", when=when))
        elif not version:
            lines.append(OUTLINE_NO_PAGE)
        headings, opening = _shape(text, str(entry.get("format") or summary_cli.FORMAT_MARKDOWN))
        if headings:
            shown = headings[:OUTLINE_HEADINGS_SHOWN] + (["…"] if len(headings) > OUTLINE_HEADINGS_SHOWN else [])
            lines.append(OUTLINE_HEADINGS.format(headings=" · ".join(_clip(h, 80) for h in shown)))
        if opening:
            lines.append(OUTLINE_OPENS.format(opening=_clip(opening, OUTLINE_OPENING_CHARS)))
        activity = entity_activity(store, kind, ref, _since_ts(entry))
        lines.append(OUTLINE_SINCE.format(version=version, activity="; ".join(activity)) if activity
                     else OUTLINE_QUIET.format(version=version))
        if _draft_dirty(path):
            lines.append(OUTLINE_DIRTY)
        blocks.append("\n".join(lines))
    return scrub("\n\n".join(blocks))


def outline_header(block: str) -> str:
    """The outline's header line, naming the outline by its content: the same
    outline is shown once; a changed one is shown again (`worker._summary_outline`)."""
    import hashlib

    return OUTLINE_HEADER.format(digest=hashlib.sha256(block.encode("utf-8")).hexdigest()[:8])
from probe.daemon.agent.tools.drafts import _bound_drafts, _draft_dirty, _drafts  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.summaries import _probe_words  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.team_note import _read  # noqa: E402 -- pieces need each other; the front door loads this one first
