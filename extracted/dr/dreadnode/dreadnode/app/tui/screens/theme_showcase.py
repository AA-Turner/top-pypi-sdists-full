"""Hidden theme showcase — visual reference for all palette colors, symbols, and patterns."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from rich.text import Text
from textual.binding import Binding
from textual.widgets import Static

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import (
    ACCENT,
    BG,
    BG_LIGHT,
    BG_LIGHTER,
    BORDER,
    BORDER_LIGHT,
    BRAND,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    PURPLE,
    SUCCESS,
    TEAL,
    WARNING,
)

if TYPE_CHECKING:
    from textual.app import ComposeResult


def _section(output: Text, title: str) -> None:
    """Append a section header."""
    output.append("\n")
    output.append(f"  {title}", style=f"bold {FG}")
    output.append("\n")
    output.append(f"  {'─' * 60}", style=FG_FAINTEST)
    output.append("\n")


def _swatch(output: Text, name: str, color: str, width: int = 16) -> None:
    """Append a color swatch: colored block + label."""
    output.append("  ")
    output.append("██ ", style=color)
    output.append(f"{name:<{width}}", style=f"bold {color}")
    output.append(f" {color}", style=FG_FAINTEST)
    output.append("\n")


def _render_showcase() -> Text:
    t = Text()

    # Title
    t.append("\n")
    t.append("  Theme Showcase", style=f"bold {FG}")
    t.append("  —  ", style=FG_FAINTEST)
    t.append("visual reference for the Dreadnode TUI palette\n", style=FG_MUTED)

    # ── Core palette ──
    _section(t, "Core Palette")

    _swatch(t, "FG", FG)
    _swatch(t, "FG_SUBTLE", FG_SUBTLE)
    _swatch(t, "FG_MUTED", FG_MUTED)
    _swatch(t, "FG_FAINTEST", FG_FAINTEST)
    t.append("\n")
    _swatch(t, "BG", BG)
    _swatch(t, "BG_LIGHT", BG_LIGHT)
    _swatch(t, "BG_LIGHTER", BG_LIGHTER)
    t.append("\n")
    _swatch(t, "BORDER", BORDER)
    _swatch(t, "BORDER_LIGHT", BORDER_LIGHT)

    # ── Semantic colors ──
    _section(t, "Semantic Colors")

    _swatch(t, "ACCENT", ACCENT)
    _swatch(t, "INFO", INFO)
    _swatch(t, "SUCCESS", SUCCESS)
    _swatch(t, "WARNING", WARNING)
    _swatch(t, "ERROR", ERROR)

    # ── Extended palette ──
    _section(t, "Extended Palette")

    _swatch(t, "BRAND", BRAND)
    _swatch(t, "PURPLE", PURPLE)
    _swatch(t, "TEAL", TEAL)

    # ── Status indicators ──
    _section(t, "Status Indicators")

    t.append("  ")
    t.append("✓ ", style=SUCCESS)
    t.append("Connected", style=FG)
    t.append("     ")
    t.append("✗ ", style=ERROR)
    t.append("Disconnected", style=FG)
    t.append("     ")
    t.append("⚠ ", style=WARNING)
    t.append("Degraded", style=FG)
    t.append("     ")
    t.append("● ", style=INFO)
    t.append("Active", style=FG)
    t.append("\n\n")

    t.append("  ")
    t.append("✓ ", style=SUCCESS)
    t.append("connected", style=FG_MUTED)
    t.append("   ")
    t.append("✗ ", style=ERROR)
    t.append("connection failed", style=ERROR)
    t.append("   ")
    t.append("⚠ ", style=WARNING)
    t.append("degraded", style=WARNING)
    t.append("\n\n")

    t.append("  ")
    t.append("✓ ", style=f"bold {SUCCESS}")
    t.append("Task completed successfully", style=f"bold {SUCCESS}")
    t.append("\n")
    t.append("  ")
    t.append("✗ ", style=f"bold {ERROR}")
    t.append("Task failed with errors", style=f"bold {ERROR}")
    t.append("\n")
    t.append("  ")
    t.append("⚠ ", style=f"bold {WARNING}")
    t.append("Task completed with warnings", style=f"bold {WARNING}")
    t.append("\n")
    t.append("  ")
    t.append("● ", style=f"bold {INFO}")
    t.append("Task in progress", style=f"bold {INFO}")
    t.append("\n")

    # ── Symbols & icons ──
    _section(t, "Symbols & Icons")

    symbols = [
        ("✓", SUCCESS, "success"),
        ("✗", ERROR, "error/failure"),
        ("⚠", WARNING, "warning"),
        ("●", INFO, "active/running"),
        ("◯", FG_FAINTEST, "disabled/inactive"),
        ("◆", ACCENT, "selected"),
        ("◇", FG_FAINTEST, "unselected"),
        ("↑", WARNING, "update available"),
        ("→", ACCENT, "navigation"),
        ("·", FG_FAINTEST, "separator"),
        ("─", FG_FAINTEST, "divider"),
        ("▸", ACCENT, "expanded"),
        ("▾", FG_MUTED, "collapsed"),
    ]

    for symbol, color, label in symbols:
        t.append(f"  {symbol} ", style=color)
        t.append(f"{label:<20}", style=FG_MUTED)

    t.append("\n")

    # ── Text hierarchy ──
    _section(t, "Text Hierarchy")

    t.append("  ")
    t.append("Heading", style=f"bold {FG}")
    t.append("\n")
    t.append("  ")
    t.append("Body text — primary content for reading", style=FG)
    t.append("\n")
    t.append("  ")
    t.append("Subtle — secondary information and labels", style=FG_SUBTLE)
    t.append("\n")
    t.append("  ")
    t.append("Muted — tertiary details, timestamps, metadata", style=FG_MUTED)
    t.append("\n")
    t.append("  ")
    t.append("Faintest — hints, borders, decorative elements", style=FG_FAINTEST)
    t.append("\n")
    t.append("  ")
    t.append("Accent highlight", style=f"bold {ACCENT}")
    t.append("  ")
    t.append("Info link", style=f"underline {INFO}")
    t.append("  ")
    t.append("Brand text", style=f"bold {BRAND}")
    t.append("\n")

    # ── Box drawing ──
    _section(t, "Box Drawing")

    # Light box
    t.append(f"  ┌{'─' * 30}┐", style=FG_FAINTEST)
    t.append("\n")
    t.append("  │", style=FG_FAINTEST)
    t.append("  Light box with border      ", style=FG_MUTED)
    t.append("│", style=FG_FAINTEST)
    t.append("\n")
    t.append(f"  └{'─' * 30}┘", style=FG_FAINTEST)
    t.append("\n\n")

    # Accent box
    t.append(f"  ┌{'─' * 30}┐", style=ACCENT)
    t.append("\n")
    t.append("  │", style=ACCENT)
    t.append("  Accent-bordered box        ", style=FG)
    t.append("│", style=ACCENT)
    t.append("\n")
    t.append(f"  └{'─' * 30}┘", style=ACCENT)
    t.append("\n\n")

    # Double box
    t.append(f"  ╔{'═' * 30}╗", style=BORDER_LIGHT)
    t.append("\n")
    t.append("  ║", style=BORDER_LIGHT)
    t.append("  Double-line box            ", style=FG)
    t.append("║", style=BORDER_LIGHT)
    t.append("\n")
    t.append(f"  ╚{'═' * 30}╝", style=BORDER_LIGHT)
    t.append("\n")

    # ── List patterns ──
    _section(t, "List Patterns")

    # Selected item
    t.append("  ", style="")
    t.append("> ", style=ACCENT)
    t.append("Selected item", style=f"bold {FG}")
    t.append(" · ", style=FG_FAINTEST)
    t.append("✓ ", style=SUCCESS)
    t.append("ready", style=FG_MUTED)
    t.append("\n")

    # Normal items
    t.append("    Normal item", style=FG)
    t.append(" · ", style=FG_FAINTEST)
    t.append("✓ ", style=SUCCESS)
    t.append("ready", style=FG_MUTED)
    t.append("\n")

    t.append("    Another item", style=FG)
    t.append(" · ", style=FG_FAINTEST)
    t.append("⚠ ", style=WARNING)
    t.append("degraded", style=WARNING)
    t.append("\n")

    t.append("    Errored item", style=FG)
    t.append(" · ", style=FG_FAINTEST)
    t.append("✗ ", style=ERROR)
    t.append("connection refused", style=ERROR)
    t.append("\n")

    t.append("    Disabled item", style=FG_MUTED)
    t.append(" · ", style=FG_FAINTEST)
    t.append("◯ ", style=FG_FAINTEST)
    t.append("disabled", style=FG_FAINTEST)
    t.append("\n")

    # ── Progress & loading ──
    _section(t, "Progress & Loading")

    # Filled bar
    filled = 18
    empty = 12
    t.append("  ")
    t.append("█" * filled, style=SUCCESS)
    t.append("░" * empty, style=FG_FAINTEST)
    t.append(f"  {filled}/{filled + empty}", style=FG_MUTED)
    t.append("\n")

    # Warning bar
    filled_w = 22
    empty_w = 8
    t.append("  ")
    t.append("█" * filled_w, style=WARNING)
    t.append("░" * empty_w, style=FG_FAINTEST)
    t.append(f"  {filled_w}/{filled_w + empty_w}", style=FG_MUTED)
    t.append("\n")

    # Error bar
    filled_e = 28
    empty_e = 2
    t.append("  ")
    t.append("█" * filled_e, style=ERROR)
    t.append("░" * empty_e, style=FG_FAINTEST)
    t.append(f"  {filled_e}/{filled_e + empty_e}", style=FG_MUTED)
    t.append("\n\n")

    # Spinner states
    t.append("  ")
    t.append("⠋ ", style=ACCENT)
    t.append("Loading...", style=FG_MUTED)
    t.append("    ")
    t.append("⣾ ", style=INFO)
    t.append("Fetching...", style=FG_MUTED)
    t.append("    ")
    t.append("⠸ ", style=PURPLE)
    t.append("Processing...", style=FG_MUTED)
    t.append("\n")

    # ── Keybinding hints ──
    _section(t, "Keybinding Hints")

    hints = [
        ("Esc", "Back"),
        ("Enter", "Select"),
        ("Tab", "Next"),
        ("↑↓", "Navigate"),
        ("^P", "Capabilities"),
        ("^B", "Sessions"),
    ]
    t.append("  ")
    for i, (key, desc) in enumerate(hints):
        t.append(key, style=FG_MUTED)
        t.append(f" {desc}", style=FG_FAINTEST)
        if i < len(hints) - 1:
            t.append("  ")
    t.append("\n")

    # ── Flash messages ──
    _section(t, "Flash Messages")

    for label, color in [
        ("Success flash — operation completed", SUCCESS),
        ("Error flash — something went wrong", ERROR),
        ("Warning flash — proceed with caution", WARNING),
        ("Info flash — here's some context", INFO),
    ]:
        t.append("  ")
        t.append(f"  {label}  ", style=f"bold {color}")
        t.append("\n")

    # ── Data visualization colors ──
    _section(t, "Data Visualization")

    viz_colors = [
        ("Series 1", ACCENT),
        ("Series 2", INFO),
        ("Series 3", SUCCESS),
        ("Series 4", WARNING),
        ("Series 5", PURPLE),
        ("Series 6", TEAL),
        ("Series 7", BRAND),
        ("Series 8", ERROR),
    ]

    t.append("  ")
    for _label, color in viz_colors:
        t.append("██", style=color)
        t.append(" ")
    t.append("\n")

    t.append("  ")
    for label, color in viz_colors:
        t.append(f"{label}  ", style=color)
    t.append("\n\n")

    # Sparkline-style
    bars = [3, 5, 2, 7, 4, 8, 6, 3, 5, 9, 7, 4, 6, 8, 5, 3, 7, 6, 4, 8]
    t.append("  ")
    for h in bars:
        char = "▁▂▃▄▅▆▇█"[min(h, 8) - 1]
        t.append(char, style=TEAL if h < 6 else WARNING if h < 8 else ERROR)
    t.append("  ", style="")
    t.append("request latency (p99)", style=FG_FAINTEST)
    t.append("\n")

    # ── Status bar preview ──
    _section(t, "Status Bar Patterns")

    # Healthy
    t.append("  ")
    t.append("✓ ", style=SUCCESS)
    t.append("local", style=FG_MUTED)
    t.append(" · ", style=FG_FAINTEST)
    t.append("dreadnode/default", style=FG_MUTED)
    t.append("\n")

    # With update
    t.append("  ")
    t.append("✓ ", style=SUCCESS)
    t.append("local", style=FG_MUTED)
    t.append(" · ", style=FG_FAINTEST)
    t.append("dreadnode/default", style=FG_MUTED)
    t.append(" · ", style=FG_FAINTEST)
    t.append("↑ 1.2.3", style=WARNING)
    t.append("\n")

    # Error
    t.append("  ")
    t.append("✗ ", style=ERROR)
    t.append("runtime unreachable", style=ERROR)
    t.append("\n")

    t.append("\n")

    return t


class ThemeShowcaseScreen(DreadnodeScreen):
    """Hidden theme showcase — visual reference for palette, symbols, and patterns."""

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("j", "scroll_down", show=False),
        Binding("k", "scroll_up", show=False),
        Binding("g", "scroll_top", show=False),
        Binding("G", "scroll_bottom", show=False),
    ]

    DEFAULT_CSS = f"""
    ThemeShowcaseScreen {{
        background: {BG};
    }}

    #showcase-scroll {{
        height: 1fr;
    }}

    #showcase-content {{
        height: auto;
        padding: 0 0 2 0;
    }}
    """

    def compose_content(self) -> ComposeResult:
        from textual.containers import VerticalScroll

        with VerticalScroll(id="showcase-scroll"):
            yield Static(_render_showcase(), id="showcase-content")

    def action_go_back(self) -> None:
        self.dismiss()

    def action_scroll_down(self) -> None:
        self.query_one("#showcase-scroll").scroll_down()

    def action_scroll_up(self) -> None:
        self.query_one("#showcase-scroll").scroll_up()

    def action_scroll_top(self) -> None:
        self.query_one("#showcase-scroll").scroll_home()

    def action_scroll_bottom(self) -> None:
        self.query_one("#showcase-scroll").scroll_end()
