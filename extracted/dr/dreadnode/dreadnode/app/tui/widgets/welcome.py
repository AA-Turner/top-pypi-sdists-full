"""Startup and welcome screen shown before first interaction.

Before the runtime connects, the job is *readiness*: show only a compact,
factual state while the lower status bar owns the spinner and connection
chrome. Once connected, the job becomes *persistent context*, not onboarding —
the user sees the welcome every session. Anything also rendered by the chrome
(status bar, context bar, page status) belongs there, not here.

Layout
------

The widget is structured as three labeled blocks — **Capabilities**,
**(composer keys)**, and **Docs** — each a column-aligned label/value
list. The label sits in a fixed-width left column; the value sits in
the right column; multi-line values (e.g. the capability slug row,
the action hint) wrap by indenting back to the value column. The
visual spine reads like a key/value reference card rather than a
pile of independent one-liners.

Centering
---------

The text is *not* line-by-line centered (``Text(justify="center")``).
Every line in this widget has a different width — wordmark (~78),
tagline, label rows (~25), slug list (~60) — so per-line centering
puts each line at a different horizontal column and the eye reads
"shift" instead of "structure." Instead, the inner ``Text`` is
left-aligned and the widget centers the whole block via
``content-align: center top``. That gives a centered card with
internally-aligned columns. The wordmark, being the widest line,
sets the bounding-box width; everything else aligns to its left edge.

The slug line is also clamped to the wordmark's rendered width via
``_visible_slugs`` — otherwise a long slug list could become wider
than the wordmark, widening the bounding box when the capability
block hydrates async and shoving every other line a few columns
left.

Color
-----

Three coloured threads run through the screen:

  - **BRAND** (warm orange) — wordmark and composer keys. The keys
    pick up the wordmark's accent so the whole "card" feels of a
    piece.
  - **ACCENT** (intense orange) — reserved for the primary capability
    number. The eye lands on it and knows immediately how much capability
    is at hand.
  - **FG_SUBTLE** (neutral) — section labels (``Capabilities``,
    ``Docs``). Distinct from the keys' BRAND so a section header
    reads as orientation, not as a hotkey.

Everything else is graded mute (``FG_MUTED`` → ``FG_FAINTEST``). Disabled
capabilities are expressed as part of the enabled/installed ratio, not as
a separate warning-like count.

Capability source
-----------------

The capabilities block deliberately excludes the bundled ``dreadnode``
capability — it ships in the SDK wheel and is always loaded, so
counting it would inflate the user-visible "you have N capabilities"
in a way the user can't act on. See
``builtin_capabilities/dreadnode/skills/creating-capabilities/runtime-default-capability.md``
for the full story.

Doc-link clickability
---------------------

Doc-link clickability follows the Markdown widget's pattern exactly
(``textual/widgets/_markdown.py:341``): each link span carries only a
``Style.from_meta({"@click": ...})`` — *not* a ``Style(link=url)``.

Mixing the two causes a render storm: when the cursor moves over a span
with ``link=url`` set, Textual's :py:meth:`Widget.watch_hover_style`
updates the ``highlight_link_id`` reactive (``widget.py:1924``), which
refreshes the widget. Hovering off → empty link id → another refresh.
Move one cell → another refresh. The visible result is rapid flashing
of the hover overlay. Markdown links don't carry ``link=url``, so they
don't hit this path; we follow that.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.style import Style
from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from dreadnode.app.tui.theme import (
    ACCENT,
    BG,
    BRAND,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    WARNING,
    pick_logo,
)

if TYPE_CHECKING:
    from dreadnode.app.tui.capabilities_manager import CapabilitiesSummary
    from dreadnode.app.tui.update_check import UpdateInfo


_TAGLINE = "Terminal-native platform for security agents."

_DOCS_URL = "https://docs.dreadnode.io"
_GETTING_STARTED_URL = f"{_DOCS_URL}/getting-started/quickstart/"
_GETTING_STARTED_DISPLAY = "docs.dreadnode.io"

# Composer-side keys the chrome doesn't already advertise. Status bar shows
# nav keys (^P, ^B, ...); context bar shows agent/model controls
# (^A, ^O, ^K). Four entries, one per row, mirrors the old welcome's
# key-reference table — the user has to learn these to drive the composer
# at all, and the per-row layout is what made the old screen feel
# structured instead of like prose.
_COMPOSER_KEYS: tuple[tuple[str, str], ...] = (
    ("Enter", "send"),
    ("Esc", "interrupt"),
    ("/", "commands"),
    ("?", "help"),
)

# Hard ceiling on slugs we'll *try* to render before reaching for overflow.
# The actual visible count is also bounded below by available width — see
# ``_visible_slugs`` for the packing logic.
_MAX_VISIBLE_SLUGS = 4

# Keep the startup render block the same height as the connected welcome's
# baseline rows. The parent centers this widget, so changing rendered height
# would move the logo during the pre-runtime -> connected transition.
_STARTUP_RESERVED_LINES = 11

# Approximate width of "DREADNODE" when no logo art fits. Used as the
# bounding-box ceiling at very narrow widths so the slug clamp still has
# a sensible upper bound.
_FALLBACK_LOGO_WIDTH = len("DREADNODE")

# Column geometry for the labeled rows. Labels sit flush left to align
# with the unlabeled prose lines (tagline, cwd) so the whole card has a
# single left edge. "Capabilities" (12 chars) is the longest label; the
# 4-char gutter to the value column gives it breathing room.
_LABEL_INDENT = 0
_VALUE_COL = 16  # column where values start (label + gutter)
_VALUE_INDENT = " " * _VALUE_COL


def _link(url: str) -> Style:
    """Style for a clickable doc-link span.

    Mirrors Textual's Markdown widget exactly (``_markdown.py:341``): only
    a ``@click`` meta. **Do not** add ``Style(link=url)``: that path triggers
    a ``highlight_link_id`` refresh storm on hover (see module docstring).
    """
    return Style.from_meta({"@click": f"open_url({url!r})"})


def _logo_width(width: int) -> int:
    """Rendered width of the largest logo that fits in *width*.

    Used to bound the slug line so the centered bounding box doesn't
    widen when the capability block hydrates — see module docstring.
    """
    logo = pick_logo(width)
    if logo is None:
        return _FALLBACK_LOGO_WIDTH
    return max(len(line) for line in logo.splitlines())


def _label_prefix(label: str) -> str:
    """Render the leading 'indent + label + gutter' for a labeled row.

    Pads the label out to the value column so values across rows
    line up regardless of label length. If a label is unusually
    long it still gets at least one trailing space before the value.
    """
    pad = max(1, _VALUE_COL - _LABEL_INDENT - len(label))
    return " " * _LABEL_INDENT + label + " " * pad


def _visible_slugs(slugs: tuple[str, ...], max_chars: int) -> tuple[list[str], int]:
    """Pack as many slugs as fit, separated by " · ", under *max_chars*.

    Returns ``(visible, overflow_count)``. The overflow count is the
    number of slugs not shown — the caller renders that as ``(+N more)``.
    Stops adding slugs once the next one (plus its separator and the
    overflow indicator if more remain) would exceed *max_chars*. Always
    shows at least one slug if any are present, even if a single long
    name would individually exceed the budget — suppressing it loses
    real signal.
    """
    if not slugs:
        return [], 0

    sep = " · "
    visible: list[str] = []
    used = 0
    for i, slug in enumerate(slugs):
        remaining = len(slugs) - i
        cost = len(slug) + (len(sep) if visible else 0)
        # Reserve room for "(+N more)" when there's still tail to elide.
        overflow_marker = f"  (+{remaining - 1} more)"
        reserve = len(overflow_marker) if remaining > 1 else 0
        if used + cost + reserve > max_chars and visible:
            break
        visible.append(slug)
        used += cost
        if len(visible) >= _MAX_VISIBLE_SLUGS:
            break
    return visible, len(slugs) - len(visible)


class Welcome(Static):
    """Top-anchored startup/welcome card.

    Before the runtime is ready, this renders a compact factual startup
    state. The lower status bar already owns the animated spinner and
    connection chrome, so the center pane stays quiet: logo plus one line.
    Once connected, it switches to the full persistent reference card.
    """

    DEFAULT_CSS = f"""
    Welcome {{
        height: 1fr;
        /* The widget centers the whole text block as a unit. The text
         * itself is left-aligned (no per-line ``justify="center"``) so
         * column alignment is preserved across rows of different widths. */
        content-align: center top;
        background: {BG};
        padding: 2 2 0 2;
    }}
    Welcome.-hidden {{
        display: none;
    }}
    """

    version: reactive[str] = reactive("")
    working_dir: reactive[str] = reactive("")
    update_info: reactive[UpdateInfo | None] = reactive(None)
    runtime_connected: reactive[bool] = reactive(False)
    # ``None`` means "runtime hasn't replied yet" — render suppresses the
    # counts and slug rows so we don't flash a wrong empty state. The
    # action hint always renders (it's true regardless of state) so the
    # orientation pointer is anchored across the full pre→post-hydration
    # transition.
    capabilities_summary: reactive[CapabilitiesSummary | None] = reactive(None)

    def render(self) -> Text:
        w = self.size.width
        # No ``justify="center"`` — see module docstring on Centering.
        t = Text()
        logo_width = _logo_width(w)

        logo = pick_logo(w)
        if logo is not None:
            for line in logo.splitlines():
                t.append(line, style=BRAND)
                t.append("\n")
        else:
            t.append("DREADNODE", style=f"bold {BRAND}")
            t.append("\n")

        t.append("\n")
        self._append_identity_line(t)

        # The update banner is app-level state — render it regardless of
        # runtime connection so users see it during the cold-boot window
        # too.
        if self.update_info is not None:
            t.append("\n")
            t.append(
                f"  Update available: v{self.update_info.current} → v{self.update_info.latest}\n",
                style=f"bold {WARNING}",
            )
            t.append("  Run /update\n", style=FG_MUTED)

        if not self.runtime_connected:
            t.append("\n" * _STARTUP_RESERVED_LINES)
            return t

        t.append("\n")
        self._append_capabilities_block(t, max_chars=logo_width)
        t.append("\n")
        self._append_docs_link(t)
        t.append("\n")
        self._append_composer_keys(t)

        if self.working_dir:
            t.append(f"\n{self.working_dir}", style=FG_FAINTEST)

        return t

    def _append_identity_line(self, t: Text) -> None:
        """Stable line under the logo; startup and welcome share this exactly."""
        if self.version:
            t.append(self.version, style=FG_FAINTEST)
            t.append(" · ", style=FG_FAINTEST)
        t.append(f"{_TAGLINE}\n", style=FG_MUTED)

    def _append_capabilities_block(self, t: Text, *, max_chars: int) -> None:
        """``Capabilities    <counts> / <slugs> / <action>``.

        Three rendered rows max — counts on the label row, slug list on a
        continuation row, action hint on a third continuation row. The
        action hint always renders (even pre-hydration) so the orientation
        pointer is anchored across the cold-boot window.

        ``max_chars`` is the wordmark's rendered width; the slug row
        clamps to ``max_chars - _VALUE_COL`` so the line can't widen the
        centered bounding box. See module docstring on Centering.
        """
        summary = self.capabilities_summary
        value_budget = max(20, max_chars - _VALUE_COL)

        t.append(_label_prefix("Capabilities"), style=FG_SUBTLE)

        if summary is None:
            # Pre-hydration: counts row collapses to "loading…", a single
            # neutral token in place of the count, so the bounding box is
            # locked from frame zero rather than widening when slugs land.
            t.append("…\n", style=FG_FAINTEST)
        else:
            enabled, disabled = summary.enabled_count, summary.disabled_count
            installed = enabled + disabled
            action = "manage" if installed > 0 else "browse"
            if enabled == 0 and disabled == 0:
                t.append("0", style=FG_SUBTLE)
                t.append(" installed", style=FG_MUTED)
            elif disabled == 0:
                t.append(str(installed), style=ACCENT)
                t.append(" ready", style=FG_MUTED)
            else:
                t.append(str(enabled), style=ACCENT)
                t.append(f"/{installed} enabled", style=FG_MUTED)

            t.append(" · ", style=FG_FAINTEST)
            t.append("/capabilities", style=FG_SUBTLE)
            t.append(f" to {action}", style=FG_FAINTEST)
            t.append("\n")

            visible, overflow = _visible_slugs(summary.enabled_slugs, max_chars=value_budget)
            if visible:
                t.append(_VALUE_INDENT, style="")
                for i, slug in enumerate(visible):
                    if i > 0:
                        t.append(" · ", style=FG_FAINTEST)
                    t.append(slug, style=FG_MUTED)
                if overflow > 0:
                    t.append(f"  (+{overflow} more)", style=FG_FAINTEST)
                t.append("\n")

    def _append_composer_keys(self, t: Text) -> None:
        """Per-key rows in BRAND — mirrors the old welcome's key reference.

        Each row is ``  <key>           <description>`` with the key in
        BRAND (the warm-accent thread that ties to the wordmark) and the
        description in ``FG_FAINTEST``. Per-row instead of inline keeps
        the visual structure that was lost when the section first
        collapsed to a single comma list.
        """
        for key, label in _COMPOSER_KEYS:
            t.append(_label_prefix(key), style=BRAND)
            t.append(f"{label}\n", style=FG_FAINTEST)

    def _append_docs_link(self, t: Text) -> None:
        """``New here?    <getting-started URL>``.

        Single focused link, not a sitemap — the welcome's job is
        orientation, not navigation. The URL slug ``getting-started`` is
        self-orienting for newcomers; experienced users read past it.
        """
        t.append(_label_prefix("New here?"), style=FG_SUBTLE)
        t.append(f"{_GETTING_STARTED_DISPLAY}", style=_link(_GETTING_STARTED_URL))
        # t.append("\n")
        # t.append(_VALUE_INDENT, style="")
        t.append(" or ", style=FG_FAINTEST)
        t.append('"Help me get started"', style=FG_SUBTLE)
        t.append("\n")

    def action_open_url(self, url: str) -> None:
        """Click handler dispatched by the doc-link spans' @click meta."""
        self.app.open_url(url)

    def dismiss(self) -> None:
        """Hide the welcome screen."""
        self.add_class("-hidden")

    def restore(self) -> None:
        """Re-show the welcome screen after it was previously dismissed."""
        self.remove_class("-hidden")

    @property
    def is_visible(self) -> bool:
        return not self.has_class("-hidden")
