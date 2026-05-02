from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path
import re

from .shell_stack import RICH_AVAILABLE, Text, rich_cell_len

BRAND_ACCENT = "#d5ac89"
BRAND_ACCENT_STRONG = "#f0b56e"
BRAND_LIGHT = "#ece7de"
BRAND_MUTED = "#93a1b6"
BRAND_DARK = "#202736"
LIVE_DIFF_FILE_FG = "#f7c48e"
LIVE_DIFF_HUNK_FG = "#ffd07a"
LIVE_DIFF_ADD_FG = "#8ff0aa"
LIVE_DIFF_REMOVE_FG = "#ff9f8f"
LIVE_DIFF_CONTEXT_FG = "#c9d2de"
SETTLED_DIFF_FILE_FG = "#bd926d"
SETTLED_DIFF_HUNK_FG = "#c29a67"
SETTLED_DIFF_ADD_FG = "#5c9a70"
SETTLED_DIFF_REMOVE_FG = "#aa6c63"
SETTLED_DIFF_CONTEXT_FG = "#7d8798"
COMMAND_PALETTE_VISIBLE_ROWS = 6
USER_HISTORY_BG = "#454649"
USER_HISTORY_FG = "#f2efe8"
SHELL_WELCOME_HEADLINE = "Here with you, built to stay."
STARTUP_SEQUENCE_STEP_DELAY = 0.60
STARTUP_SEQUENCE_FINAL_DELAY = 0.60
GROWTH_PROGRESS_WIDTH = 14
GROWTH_PROGRESS_FILLED = "▰"
GROWTH_PROGRESS_EMPTY = "▱"
GROWTH_HIGHLIGHT_FG = BRAND_ACCENT_STRONG
QUEUE_PREVIEW_INSET = 3
MARKDOWN_BOLD_PATTERN = re.compile(r"\*\*(.+?)\*\*")
WEB_URL_PATTERN = re.compile(r"(https?://[^\s]+)", re.IGNORECASE)
EXPERIENCE_NOISE_PATTERN = re.compile(
    r"^(?:it looks like|i couldn't|i could not|sorry|tool failed\b|unable to\b)",
    re.IGNORECASE,
)
GROWTH_LEVEL_PATTERN = re.compile(r"\bLv\.\d+\b")
GROWTH_META_PATTERN = re.compile(r"\b(level-up|stage-shift)\b")
# SVG-derived pixel rows. Growth-stage marks stay on the canonical 24-cell
# horizontal canvas from the source brand assets so left/right geometry does not
# drift from row-parity mismatches.
GUARDIAN_HEAD_ROWS = (
    "          bggb",
    "        bccccccb",
    "       bccccccccb",
    "      bcccmmmmcccb",
    "      bccmmmmmmccb",
    "      bccmttttmccb",
    "      bcctdttdtccb",
    "      bccttddttccb",
)
EGG_STAGE_ROWS = (
    "          kkkk",
    "         kcccck",
    "        kcccccck",
    "       kcccccccck",
    "      kcccccccccck",
    "      kcccccccccck",
    "     kcccccccccccck",
    "     kcccccccccccck",
    "     kcccccccccccck",
    "     kcccccccccccck",
    "      kcccccccccck",
    "      kcccccccccck",
    "       kkcccccckk",
    "         kkkkkk",
)
SEED_STAGE_ROWS = (
    "           gg",
    "          bbbb",
    "         bccccb",
    "        bccccccb",
    "        bcttttcb",
    "        bcxttxcb",
    "        b cccc b",
    "         bbccbb",
    "          bggb",
    "           bb",
)
HATCHLING_STAGE_ROWS = (
    "          bggb",
    "        bccccccb",
    "       bccmmmmccb",
    "      bccccccccccb",
    "      bcctxttxtccb",
    "      bccttxxttccb",
    "      bcc tttt ccb",
    "      b cccccccc b",
    "       bb      bb",
    "        bbbbbbbb",
    "         bbbbbb",
    "         mtggtm",
    "          tggt",
    "          b  b",
    "          b  b",
    "         bbbbbb",
)
SCOUT_STAGE_ROWS = (
    "          bggb",
    "        bccccccb",
    "       bccccccccb",
    "      bcccmmmmcccb",
    "      bccmmmmmmccb",
    "      bcctxttxtccb",
    "      bccttxxttccb",
    "      b ccttttcc b",
    "        bbbbbbbb",
    "       bbbbbbbbbb",
    "        bcmmmmcb",
    "        bctggtcb",
    "        bctggtcb",
    "        bccttccb",
    "         bmmmmbb",
    "         bb  bb",
    "         bb  bb",
    "        bbb  bbb",
)
GUARDIAN_STAGE_ROWS = (
    "          bggb",
    "        bccccccb",
    "       bccccccccb",
    "      bcccmmmmcccb",
    "      bccmmmmmmccb",
    "      bccmttttmccb",
    "      bcctdttdtccb   s",
    "      bccttddttccb  sd",
    "      b ccttttcc b sdb",
    "       bbccddccbb sdb",
    "        bbbbbbbb  db",
    "       bbbbbbbbbbsg",
    "      bccmmmmmmctm",
    "     bbccmttttmctb",
    "     bbcmttggttmcb",
    "      bcmttggttmcb",
    "      b  mttttm  b",
    "       bccmggmccb",
    "        ccm  mcc",
    "        ccm  mcc",
    "        ccm  mcc",
    "       bccb  bccb",
)
GROWTH_STAGE_ROWS = {
    "seed": SEED_STAGE_ROWS,
    "hatchling": HATCHLING_STAGE_ROWS,
    "scout": SCOUT_STAGE_ROWS,
    "guardian": GUARDIAN_STAGE_ROWS,
}
GROWTH_MARK_CANVAS_WIDTH = max(
    24,
    *(
        len(row)
        for rows in (EGG_STAGE_ROWS, SEED_STAGE_ROWS, HATCHLING_STAGE_ROWS, SCOUT_STAGE_ROWS, GUARDIAN_STAGE_ROWS)
        for row in rows
    ),
)


def display_path(path: Path) -> str:
    home = Path.home()
    try:
        return f"~/{path.relative_to(home)}"
    except ValueError:
        return str(path)


def display_width(content: str) -> int:
    if RICH_AVAILABLE:
        return rich_cell_len(content)
    return len(content)


def compact_line(value: str, *, limit: int) -> str:
    compact = " ".join(value.split()).strip()
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 3)].rstrip() + "..."


def render_guardian_mark():
    return _render_pixel_mark(centered_guardian_rows(), fallback="[Aegis guardian]")


def render_growth_mark(stage_id: str, *, level: int | None = None):
    rows = _growth_rows(stage_id, level=level)
    fallback = "[Aegis egg]" if stage_id == "seed" and (level or 0) <= 0 else f"[Aegis {stage_id}]"
    centered = (
        centered_guardian_rows()
        if rows is GUARDIAN_STAGE_ROWS
        else visual_centered_rows(rows, width=GROWTH_MARK_CANVAS_WIDTH)
    )
    return _render_pixel_mark(centered, fallback=fallback)


def centered_guardian_rows() -> tuple[str, ...]:
    """Keep the guardian body optically centered while preserving the right accessory."""
    return source_canvas_rows(GUARDIAN_STAGE_ROWS, width=GROWTH_MARK_CANVAS_WIDTH)


def centered_rows(rows: tuple[str, ...], *, width: int | None = None) -> tuple[str, ...]:
    resolved_width = width or max(len(row) for row in rows)
    centered: list[str] = []
    for row in rows:
        padding = resolved_width - len(row)
        left = padding // 2
        right = padding - left
        centered.append((" " * left) + row + (" " * right))
    return tuple(centered)


def source_canvas_rows(rows: tuple[str, ...], *, width: int | None = None) -> tuple[str, ...]:
    resolved_width = max(width or 0, *(len(row) for row in rows))
    return tuple(row.ljust(resolved_width) for row in rows)


def visual_centered_rows(rows: tuple[str, ...], *, width: int | None = None) -> tuple[str, ...]:
    """Center the visible pixels, not the transparent source-canvas whitespace."""
    visible_cells = [
        index
        for row in rows
        for index, cell in enumerate(row)
        if cell != " "
    ]
    if not visible_cells:
        return centered_rows(rows, width=width)
    visible_left = min(visible_cells)
    visible_right = max(visible_cells)
    visible_width = visible_right - visible_left + 1
    resolved_width = max(width or visible_width, visible_width)
    target_left = (resolved_width - visible_width) // 2
    target_right = resolved_width - visible_width - target_left
    centered: list[str] = []
    for row in rows:
        segment = row.ljust(visible_right + 1)[visible_left : visible_right + 1]
        centered.append((" " * target_left) + segment + (" " * target_right))
    return tuple(centered)


def resolve_aegis_version() -> str:
    try:
        return package_version("aegis-ag")
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        if pyproject.exists():
            for raw in pyproject.read_text(encoding="utf-8").splitlines():
                stripped = raw.strip()
                if stripped.startswith("version = "):
                    return stripped.split("=", 1)[1].strip().strip('"')
        return "dev"


def strip_markdown_bold(text: str) -> str:
    return MARKDOWN_BOLD_PATTERN.sub(lambda match: match.group(1), text)


def render_markdown_bold(text: str, *, base_style: str) -> Text:
    rendered = Text()
    cursor = 0
    for match in MARKDOWN_BOLD_PATTERN.finditer(text):
        if match.start() > cursor:
            rendered.append(text[cursor : match.start()], style=base_style)
        rendered.append(match.group(1), style=f"bold {base_style}")
        cursor = match.end()
    if cursor < len(text):
        rendered.append(text[cursor:], style=base_style)
    if not text:
        rendered.append("", style=base_style)
    return rendered


def render_highlighted_history_line(
    text: str,
    *,
    base_style: str,
    highlight_pattern: re.Pattern[str],
    highlight_style: str,
) -> Text:
    rendered = Text(text, style=base_style)
    for match in highlight_pattern.finditer(text):
        rendered.stylize(highlight_style, match.start(), match.end())
    return rendered


def _growth_rows(stage_id: str, *, level: int | None = None) -> tuple[str, ...]:
    if stage_id == "seed" and (level or 0) <= 0:
        return EGG_STAGE_ROWS
    return GROWTH_STAGE_ROWS.get(stage_id, GUARDIAN_STAGE_ROWS)


def _render_pixel_mark(rows: tuple[str, ...], *, fallback: str):
    if not RICH_AVAILABLE:
        return Text(fallback)
    palette = {
        "g": BRAND_ACCENT_STRONG,
        "b": "#5d78a0",
        "c": "#e8e1d6",
        "t": BRAND_ACCENT,
        "m": BRAND_MUTED,
        "d": "#415a7b",
        "s": "#c7d3e3",
        "k": "#13161c",
        "x": "#08090c",
        " ": None,
    }
    glyph = Text(no_wrap=True)
    for row_index, row in enumerate(rows):
        for cell in row:
            color = palette.get(cell)
            if color is None:
                glyph.append("  ")
            else:
                glyph.append("██", style=color)
        if row_index < len(rows) - 1:
            glyph.append("\n")
    return glyph
