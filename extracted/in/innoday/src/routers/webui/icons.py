"""Pixel-block glyphs for repository layers, plus the PixelFuel wordmark.

Drawn from the logo's own construction rather than a generic icon set: the
PixelFuel mark (``pixelfuel-website/components/ui/PixelFuelLogo.tsx``) is built
from square blocks with one orange square inside the ``P``. Each glyph here is a
4x4 grid of 4px cells on a 16px canvas, and the single orange cell repeats that
motif -- so ``legacy`` and ``unassigned``, which have no orange cell, read as
unclassified at a glance without anyone reading the label beside them.

Inline SVG rather than files: no static mount, no second request, and nothing to
serve. Colour comes from ``currentColor`` on the wrapping tile so one glyph works
at every accent.
"""

from typing import Dict, List, Optional, Tuple

from src.domain.project import RepositoryLayer

_CELL = 4
_SIZE = 3.6  # a hairline short of _CELL, so the blocks read as pixels not a slab

# (column, row) cells per glyph, and which cell (if any) is the orange accent.
# Coordinates are grid positions 0-3, scaled by _CELL on render.
_GLYPHS: Dict[str, Tuple[List[Tuple[int, int]], Optional[Tuple[int, int]]]] = {
    # A browser window: title bar, two frame sides, sill.
    "ui": (
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (0, 1),
            (3, 1),
            (0, 2),
            (3, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ],
        (0, 0),
    ),
    # A rack: three stacked units, accent as the status light on the top one.
    "api": (
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 1),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ],
        (3, 0),
    ),
    # A drum, narrowed top and bottom.
    "data": (
        [
            (1, 0),
            (2, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 1),
            (0, 2),
            (1, 2),
            (2, 2),
            (3, 2),
            (1, 3),
            (2, 3),
        ],
        (1, 0),
    ),
    # A node with four satellites -- distinct in silhouette from the solid shapes.
    "ai": (
        [
            (0, 0),
            (3, 0),
            (1, 1),
            (2, 1),
            (1, 2),
            (2, 2),
            (0, 3),
            (3, 3),
        ],
        (0, 0),
    ),
    # Scaffolding: two uprights and two crossbeams. Reads as structure holding
    # something else up, which is what infra is.
    "infra": (
        [
            (0, 0),
            (3, 0),
            (0, 1),
            (1, 1),
            (2, 1),
            (3, 1),
            (0, 2),
            (3, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ],
        (3, 0),
    ),
    # An archive box: lid, handle, body. No accent -- deliberately inert.
    "legacy": (
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (1, 1),
            (2, 1),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ],
        None,
    ),
    # Four corners only: a placeholder outline. No accent.
    "unassigned": ([(0, 0), (3, 0), (0, 3), (3, 3)], None),
}

ACCENT = "#F15B35"

# Categorical hues for the layer tiles. Orange and amber are the brand's own;
# purple is its secondary card accent; teal and slate fill out the set at low
# saturation so none of them competes with the orange CTA.
LAYER_HUE: Dict[str, str] = {
    "ui": "#fbbf24",
    "api": "#F15B35",
    "data": "#2dd4bf",
    "ai": "#a855f7",
    "infra": "#38bdf8",
    "legacy": "#64748b",
    "unassigned": "#4b5563",
}

# How each layer is written in the interface.
#
# These are the team's own names for the set, not invented synonyms. An earlier
# version rendered `ui` as "interface" and `api` as "service" -- which reads fine
# but means the label on screen matches nothing anyone says out loud, nothing in
# the enum, and nothing in the CLI. Keep this table boring.
LAYER_LABEL: Dict[str, str] = {
    "ui": "ui/ux",
    "api": "api",
    "data": "data",
    "ai": "intelligence",
    "infra": "infra",
    "legacy": "legacy",
    "unassigned": "unassigned",
}


def layer_glyph(layer: str) -> str:
    """Inline SVG for one repository layer, falling back to ``unassigned``."""
    cells, accent = _GLYPHS.get(layer, _GLYPHS["unassigned"])
    rects = []
    for col, row in cells:
        fill = f' fill="{ACCENT}"' if accent == (col, row) else ""
        rects.append(
            f'<rect x="{col * _CELL}" y="{row * _CELL}" '
            f'width="{_SIZE}" height="{_SIZE}"{fill}/>'
        )
    return (
        '<svg viewBox="0 0 16 16" width="15" height="15" fill="currentColor" '
        'aria-hidden="true">' + "".join(rects) + "</svg>"
    )


def layer_hue(layer: str) -> str:
    return LAYER_HUE.get(layer, LAYER_HUE["unassigned"])


def layer_label(layer: str) -> str:
    return LAYER_LABEL.get(layer, layer)


def known_layers() -> List[str]:
    """Layer values with a glyph, in the enum's own order."""
    return [member.value for member in RepositoryLayer if member.value in _GLYPHS]


def selectable_layers() -> List[str]:
    """Layers offered in the picker: every real one, plus `unassigned` last.

    `unassigned` is included deliberately -- classifying a repo wrongly and having
    no way back to "we haven't decided" would make people leave a bad label rather
    than an honest blank.
    """
    real = [layer for layer in known_layers() if layer != "unassigned"]
    return real + ["unassigned"]


# Two arrows chasing each other round a circle -- the universal "sync now".
# Stroked rather than pixel-blocked: it is a control, not a classification, and
# should not read as another layer glyph.
SYNC_SVG = (
    '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M21 12a9 9 0 0 1-9 9 9 9 0 0 1-7.7-4.4"/>'
    '<path d="M3 12a9 9 0 0 1 9-9 9 9 0 0 1 7.7 4.4"/>'
    '<polyline points="21 3 19.7 7.4 15.3 6.1"/>'
    '<polyline points="3 21 4.3 16.6 8.7 17.9"/>'
    "</svg>"
)

# --------------------------------------------------------------------------- #
# Integration status glyphs
#
# One per thing a project can be wired to. Stroked or solid to match each
# vendor's own mark rather than pixel-blocked: these are *identities*, not
# classifications, and a repo-layer-shaped GitHub logo would read as a layer.
#
# All take colour from ``currentColor`` on the wrapping tile, which is what
# carries the state -- grey for unconfigured, green for connected. The glyph
# never encodes the state itself, so one glyph serves every state and there is
# no second copy to keep in step when a third state is added (issue #499).
# --------------------------------------------------------------------------- #

GITHUB_SVG = (
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor" '
    'aria-hidden="true">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
    "0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53"
    ".63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95"
    " 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.4 7.4 0 0 1 2-.27c.68 0 "
    "1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 "
    "3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 "
    '8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>'
    "</svg>"
)

# Linear's mark: the corner-to-corner diagonal bands of a rounded square.
LINEAR_SVG = (
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor" '
    'aria-hidden="true">'
    '<path d="M.6 9.6a7.4 7.4 0 0 0 5.8 5.8L.6 9.6Z"/>'
    '<path d="M.1 6.9l9 9c.6-.1 1.2-.3 1.7-.6L.7 5.2c-.3.5-.5 1.1-.6 1.7Z"/>'
    '<path d="M1.7 3.6l10.7 10.7c.4-.3.8-.6 1.2-1L2.7 2.4c-.4.4-.7.8-1 1.2Z"/>'
    '<path d="M4.2 1.4l10.4 10.4A7.4 7.4 0 0 0 4.2 1.4Z"/>'
    "</svg>"
)

# Jira: three stacked chevrons.
JIRA_SVG = (
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M8 1.5 14 7.5 8 13.5 2 7.5Z"/><path d="M8 6 11 9l-3 3-3-3Z"/>'
    "</svg>"
)

# Trello: a board with two lists of unequal height.
TRELLO_SVG = (
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
    'stroke-width="1.5" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="1.8" y="1.8" width="12.4" height="12.4" rx="1.8"/>'
    '<rect x="4" y="4" width="3.2" height="7.4" rx=".7" fill="currentColor" stroke="none"/>'
    '<rect x="8.8" y="4" width="3.2" height="4.2" rx=".7" fill="currentColor" stroke="none"/>'
    "</svg>"
)

# Notion: the ruled page with its slanted spine.
NOTION_SVG = (
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
    'stroke-width="1.5" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="2.2" y="2.2" width="11.6" height="11.6" rx="1.6"/>'
    '<path d="M5.6 11V5l4.8 6V5" stroke-linecap="round"/>'
    "</svg>"
)

# A written page: the project's own context, generated from its repositories.
# Ruled lines rather than a blank sheet -- a blank page and a written one are
# exactly the distinction this icon exists to report.
DOC_SVG = (
    '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" '
    'stroke-width="1.4" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M9 1.6H4.3a.9.9 0 0 0-.9.9v11a.9.9 0 0 0 .9.9h7.4a.9.9 0 0 0 .9-.9V5.1L9 1.6Z"/>'
    '<path d="M8.9 1.7v3.4h3.5"/>'
    '<path d="M5.6 9.1h4.8M5.6 11.4h3.2" stroke-linecap="round"/>'
    "</svg>"
)

# The arrow leaving a frame: this link goes to somebody else's application.
# Small and low-contrast on purpose -- it is an annotation on a link, not a
# control, and at full weight it competed with the ticket reference beside it.
EXTERNAL_SVG = (
    '<svg class="ext" viewBox="0 0 12 12" width="9" height="9" fill="none" '
    'stroke="currentColor" '
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M9.5 6.75V10a.75.75 0 0 1-.75.75H2A.75.75 0 0 1 1.25 10V3.25A.75.75 0 0 1 2 2.5h3.25"/>'
    '<path d="M7.5 1.5h3v3"/><path d="M5.25 6.75 10.5 1.5"/>'
    "</svg>"
)

# Which glyph stands for which board. Keyed on ``BoardType`` values, which are
# lowercase. Linear is the fallback for an unregistered board rather than a
# generic clipboard: the slot means "the board", and a project with none is
# overwhelmingly a project that has not connected Linear yet.
_BOARD_GLYPHS: Dict[str, str] = {
    "linear": LINEAR_SVG,
    "jira": JIRA_SVG,
    "trello": TRELLO_SVG,
    "notion": NOTION_SVG,
}


def board_glyph(platform: Optional[str]) -> str:
    """Inline SVG for one board platform, or the fallback when there is none."""
    if not platform:
        return LINEAR_SVG
    return _BOARD_GLYPHS.get(str(platform).lower(), LINEAR_SVG)


# Three bars / a back-chevron: show and hide the project menu. Two glyphs
# because the control reports which way it will move, and CSS picks between
# them off the ``<details>`` open state -- there is no script to swap them.
# Shown when the menu is **shut**: a rail with a chevron pointing out of it, so
# the affordance is "this panel opens" rather than "here is a list of things".
# A hamburger said the latter, which is wrong for a rail that is already visible.
MENU_SVG = (
    '<svg viewBox="0 0 16 16" width="15" height="15" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M3 2.6v10.8"/><path d="M7 8h6"/><path d="M10.6 5.4 13.2 8l-2.6 2.6"/>'
    "</svg>"
)

# Shown when the menu is **open**: the same rail with the chevron pointing back
# into it. Mirrored deliberately -- the pair reads as one control with two
# directions rather than two unrelated glyphs.
MENU_CLOSE_SVG = (
    '<svg viewBox="0 0 16 16" width="15" height="15" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M13 2.6v10.8"/><path d="M9 8H3"/><path d="M5.4 5.4 2.8 8l2.6 2.6"/>'
    "</svg>"
)

# Two overlapping sheets -- copy to clipboard.
COPY_SVG = (
    '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="9" y="9" width="11" height="11" rx="2"/>'
    '<path d="M5 15V5a2 2 0 0 1 2-2h10"/>'
    "</svg>"
)

# innoday, the rocket: nose, body, fins, exhaust. Same pixel grid as the glyphs.
ROCKET_SVG = (
    '<svg viewBox="0 0 14 18" height="15" aria-hidden="true">'
    '<rect x="5" y="0" width="4" height="4" fill="#fbbf24"/>'
    '<rect x="5" y="4" width="4" height="4" fill="#F15B35"/>'
    '<rect x="1" y="8" width="4" height="4" fill="#F15B35"/>'
    '<rect x="5" y="8" width="4" height="4" fill="#F15B35"/>'
    '<rect x="9" y="8" width="4" height="4" fill="#F15B35"/>'
    '<rect x="5" y="13" width="4" height="3" fill="#fbbf24" opacity=".75"/>'
    '<rect x="5" y="17" width="4" height="1" fill="#fbbf24" opacity=".4"/>'
    "</svg>"
)

# The PixelFuel horizontal wordmark, paths lifted verbatim from
# pixelfuel-website/components/ui/PixelFuelLogo.tsx (the `horizontal` variant,
# `colorLight`: PIXEL in white, FUEL in brand orange). Do not re-draw by hand --
# copy from that component if the brand mark changes.
WORDMARK_SVG = (
    '<svg viewBox="0 0 454 55" fill="none" height="13" aria-label="PixelFuel">'
    '<path d="M0 0V34.966V38.1211V52.343H17.377V38.1211H42.0141V0H0Z" fill="#fff"/>'
    '<path d="M28.8989 11.1685H13.1152V26.9522H28.8989V11.1685Z" fill="#F15B35"/>'
    '<path d="M67.3104 0H50.5535V52.343H67.3104V0Z" fill="#fff"/>'
    '<path d="M108.901 26.1597L120.909 14.2061V0H104.152V10.0856V10.1091L98.4619 '
    "15.7759L92.8109 10.1248V0H76.0539V14.0021V14.1434L76.1167 14.2061L88.0781 "
    "26.1597L76.1088 38.129H76.0539V52.343H92.8109V42.2025L98.4619 36.5514L104.152 "
    '42.2417V52.343H120.909V38.286V38.2232L120.815 38.129L108.846 26.1597V26.1126L108.901 26.1597Z" fill="#fff"/>'
    '<path d="M169.249 13.7431V0H130.288V5.01532V13.7431V52.343H146.543H169.249V38.4115H147.038V32.3523H163.363V19.3392H147.038V13.7431H169.249Z" fill="#fff"/>'
    '<path d="M203.101 24.2054V38.2075H194.326V0H177.828V52.343H192.686H194.326H218.877V46.9509V38.2075V24.2054H203.101Z" fill="#fff"/>'
    '<path d="M283.0141 14.0256V0H241V8.3039V9.7559V14.0256V52.335H257.498H258.3456V35.3976H277.1276V21.4426H258.3456V14.0256H283.0141Z" fill="#F15B35"/>'
    '<path d="M317.0146 0V38.937H308.3104V0H291.5535V52.335H303.8288H308.3104H333.8109V46.943V38.937V0H317.0146Z" fill="#F15B35"/>'
    '<path d="M384.121 13.735V0H345.152V5.0153V13.735V52.335H361.415H384.121V38.411H361.909V32.3444H378.235V19.3313H361.909V13.735H384.121Z" fill="#F15B35"/>'
    '<path d="M418.899 24.2054V38.1866H410.124V0H393.626V52.335H408.483H410.124H434.667V46.943V38.1866V24.2054H418.899Z" fill="#F15B35"/>'
    '<path d="M453.877 36.559H438.093V52.343H453.877V36.559Z" fill="#fff"/>'
    "</svg>"
)

# --------------------------------------------------------------------------- #
# Left-nav glyphs
#
# Stroked and simple: they sit beside a word that already names the destination,
# so their job is to make the row scannable, not to carry the meaning alone.
#
# The first two are the org-level pair, the rest the project block. All of them
# render in the same rail, so they share `class="ic"` and `currentColor` and dim
# and brighten with their row -- see the note on `NAV_ROCKET_SVG`.
# --------------------------------------------------------------------------- #

#: Workflows: a play mark in a frame. Every other glyph in this rail names
#: something you *read*; the launcher is the one row that starts something, so a
#: run mark says what a list or a document glyph could not.
NAV_WORKFLOWS_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true">'
    '<rect x="1.9" y="1.9" width="12.2" height="12.2" rx="2.4" fill="none" '
    'stroke="currentColor" stroke-width="1.3"/>'
    '<path d="M6.4 5.1 11 8l-4.6 2.9Z" fill="currentColor"/>'
    "</svg>"
)

#: Projects: four cards. The destination is the dashboard, and the dashboard is a
#: grid of project cards -- so the glyph is a picture of the page rather than a
#: folder, which would have implied a container the app does not have.
NAV_PROJECTS_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
    '<rect x="1.8" y="1.8" width="5.4" height="5.4" rx="1.2"/>'
    '<rect x="8.8" y="1.8" width="5.4" height="5.4" rx="1.2"/>'
    '<rect x="1.8" y="8.8" width="5.4" height="5.4" rx="1.2"/>'
    '<rect x="8.8" y="8.8" width="5.4" height="5.4" rx="1.2"/>'
    "</svg>"
)

#: The rocket, in the nav's own idiom, for the project overview row.
#:
#: **`currentColor`, not the brand's amber and orange.** `ROCKET_SVG` carries its
#: colours as literal fills, which is right in the wordmark where it is the only
#: mark on the page. In this rail the glyph has to dim with its row: siblings sit
#: at `opacity:.7` and brighten to 1 when active or hovered, so a hardcoded amber
#: rocket would read as the selected row no matter which row was selected.
#:
#: **The silhouette, not the brand's pixel blocks.** Drawn to match
#: `_brand_pages.FAVICON_SVG` for the reason discovered there: a block rocket
#: needs its amber nose to say which way is up, and in one flat colour at 15px
#: the level fins and square body collapse into a **thumbtack**. Rasterised and
#: looked at, which is the only way to know -- a first version of this constant
#: shipped the blocks with a docstring asserting they "read cleanly at 15px", and
#: they did not. Nose, body, swept-back fins, and a plume separated by a gap so
#: the exhaust does not merge into the body it comes out of.
NAV_ROCKET_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
    '<polygon points="8,0.6 11,6 11,10.4 5,10.4 5,6"/>'
    '<polygon points="5,10.4 5,14.4 2.3,12.4"/>'
    '<polygon points="11,10.4 11,14.4 13.7,12.4"/>'
    '<polygon points="6.6,11.6 9.4,11.6 8,15.6"/>'
    "</svg>"
)

NAV_TICKETS_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
    '<path d="M2 3.5A1.5 1.5 0 0 1 3.5 2h9A1.5 1.5 0 0 1 14 3.5v9a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 12.5v-9Z'
    'M4.5 5h7v1.4h-7V5Zm0 2.8h7v1.4h-7V7.8Zm0 2.8h4.4V12H4.5v-1.4Z"/>'
    "</svg>"
)

NAV_TIMELINE_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
    '<path d="M8 1.4A6.6 6.6 0 1 0 8 14.6 6.6 6.6 0 0 0 8 1.4Zm.7 6.9-2.4 1.4-.7-1.2 1.7-1V4.2h1.4v4.1Z"/>'
    "</svg>"
)

# A version tag, not a rocket. The app already spends the launch metaphor on the
# *act* of shipping ("Next launch", blastoff); this menu item is the list of
# versions, and a second rocket would say the two are the same thing.
NAV_RELEASES_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" fill="currentColor" '
    'fill-rule="evenodd" aria-hidden="true">'
    '<path d="M7.3 1.6H13A1.4 1.4 0 0 1 14.4 3v5.7a1.4 1.4 0 0 1-.41.99l-5.2 5.2'
    "a1.4 1.4 0 0 1-1.98 0L1.72 9.79a1.4 1.4 0 0 1 0-1.98l5.2-5.2a1.4 1.4 0 0 1 "
    '.99-.41Zm3.6 2.55a.95.95 0 1 0 0 1.9.95.95 0 0 0 0-1.9Z"/>'
    "</svg>"
)

NAV_SETTINGS_SVG = (
    '<svg class="ic" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
    '<path d="M8 10.2a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4Z"/>'
    '<path d="M13.4 8.8 13.42 8l-.02-.8 1.3-1-1.3-2.3-1.55.5a5.6 5.6 0 0 0-1.4-.8L10.2.9H7.5l-.25 1.7c-.5.2-.97.47-1.4.8'
    "l-1.55-.5-1.3 2.3 1.3 1a6 6 0 0 0 0 1.6l-1.3 1 1.3 2.3 1.55-.5c.43.33.9.6 1.4.8l.25 1.7h2.7l.25-1.7c.5-.2.97-.47 "
    '1.4-.8l1.55.5 1.3-2.3-1.3-1Z" fill="none" stroke="currentColor" stroke-width="1.1"/>'
    "</svg>"
)


# Google's mark, four-colour. Reproduced rather than tinted with `currentColor`:
# Google's brand terms require the official colours on a light button, and a
# monochrome version would be both off-brand and less recognisable in the one
# place recognition is the entire point.
GOOGLE_SVG = (
    '<svg viewBox="0 0 18 18" width="17" height="17" aria-hidden="true">'
    '<path fill="#4285F4" d="M17.64 9.2c0-.64-.06-1.25-.16-1.84H9v3.48h4.84a4.14 4.14 0 0 1-1.8 2.72v2.26h2.92c1.7-1.57 2.68-3.88 2.68-6.62Z"/>'
    '<path fill="#34A853" d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.92-2.26c-.8.54-1.84.86-3.04.86-2.34 0-4.32-1.58-5.03-3.7H.96v2.33A9 9 0 0 0 9 18Z"/>'
    '<path fill="#FBBC05" d="M3.97 10.72a5.4 5.4 0 0 1 0-3.44V4.95H.96a9 9 0 0 0 0 8.1l3.01-2.33Z"/>'
    '<path fill="#EA4335" d="M9 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.58C13.46.89 11.43 0 9 0A9 9 0 0 0 .96 4.95l3.01 2.33C4.68 5.16 6.66 3.58 9 3.58Z"/>'
    "</svg>"
)


# The one-click plan control: an arrow into a bracket. Not a plus -- this moves a
# ticket into a release rather than creating anything.
PLAN_ARROW_SVG = (
    '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" '
    'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M2 8h8"/><path d="M7.4 4.6 10.8 8l-3.4 3.4"/><path d="M13.4 3v10"/>'
    "</svg>"
)


# A disclosure chevron. Rotated by CSS when its `<details>` opens, so one glyph
# serves both directions -- two would be two things to keep pointing correctly.
CHEVRON_SVG = (
    '<svg viewBox="0 0 16 16" width="11" height="11" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M5.5 3.5 10 8l-4.5 4.5"/>'
    "</svg>"
)
