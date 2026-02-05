"""
CSSL Service Manager - Dark theme constants and ttk styling.
Matches the IncludeCPP project aesthetic (black/white professional).
"""
import tkinter as tk
from tkinter import ttk

# ── Color Palette ──────────────────────────────────────────────
BG = "#0a0a0a"
SURFACE = "#141414"
CARD = "#1a1a1a"
BORDER = "#2a2a2a"
HOVER = "#252525"
ACTIVE = "#303030"

TEXT = "#ffffff"
TEXT_DIM = "#888888"
TEXT_MUTED = "#555555"

GREEN = "#4ade80"
RED = "#f87171"
YELLOW = "#fbbf24"
BLUE = "#3b82f6"
ACCENT = "#a78bfa"
CYAN = "#22d3ee"
ORANGE = "#fb923c"

# ── Font Configuration ─────────────────────────────────────────
FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"
FONT_SIZE = 10
FONT_SIZE_SMALL = 9
FONT_SIZE_LARGE = 12
FONT_SIZE_TITLE = 14

FONT = (FONT_FAMILY, FONT_SIZE)
FONT_SMALL = (FONT_FAMILY, FONT_SIZE_SMALL)
FONT_BOLD = (FONT_FAMILY, FONT_SIZE, "bold")
FONT_TITLE = (FONT_FAMILY, FONT_SIZE_TITLE, "bold")
FONT_CODE = (FONT_MONO, FONT_SIZE)
FONT_CODE_SMALL = (FONT_MONO, FONT_SIZE_SMALL)

# ── Status Colors ──────────────────────────────────────────────
STATUS_COLORS = {
    "running": GREEN,
    "attached": BLUE,
    "scanning": YELLOW,
    "discovered": TEXT_DIM,
    "dead": RED,
    "disconnected": ORANGE,
    "error": RED,
}

# ── Syntax Highlighting Colors ─────────────────────────────────
SYNTAX = {
    "keyword": "#c678dd",
    "string": "#98c379",
    "number": "#d19a66",
    "comment": "#5c6370",
    "function": "#61afef",
    "type": "#e5c07b",
    "operator": "#56b6c2",
    "builtin": "#e06c75",
    "identifier": TEXT,
}


def setup_theme(root: tk.Tk):
    """Configure ttk dark theme for the entire application."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # ── Global ──
    root.configure(bg=BG)
    root.option_add("*TCombobox*Listbox.background", CARD)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", HOVER)
    root.option_add("*TCombobox*Listbox.selectForeground", TEXT)

    # ── Frame ──
    style.configure("TFrame", background=BG)
    style.configure("Surface.TFrame", background=SURFACE)
    style.configure("Card.TFrame", background=CARD)
    style.configure("Border.TFrame", background=BORDER)

    # ── Label ──
    style.configure("TLabel", background=BG, foreground=TEXT, font=FONT)
    style.configure("Dim.TLabel", foreground=TEXT_DIM)
    style.configure("Muted.TLabel", foreground=TEXT_MUTED)
    style.configure("Title.TLabel", font=FONT_TITLE)
    style.configure("Status.TLabel", background=SURFACE, foreground=TEXT_DIM, font=FONT_SMALL)
    style.configure("Green.TLabel", foreground=GREEN)
    style.configure("Red.TLabel", foreground=RED)
    style.configure("Yellow.TLabel", foreground=YELLOW)
    style.configure("Blue.TLabel", foreground=BLUE)

    # ── Button ──
    style.configure("TButton",
                    background=CARD, foreground=TEXT, font=FONT,
                    bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                    focuscolor=BORDER, padding=(10, 4))
    style.map("TButton",
              background=[("active", HOVER), ("pressed", ACTIVE)],
              foreground=[("disabled", TEXT_MUTED)])

    style.configure("Accent.TButton", background=BLUE, foreground=TEXT)
    style.map("Accent.TButton", background=[("active", "#2563eb")])

    style.configure("Danger.TButton", background="#991b1b", foreground=TEXT)
    style.map("Danger.TButton", background=[("active", RED)])

    style.configure("Small.TButton", padding=(6, 2), font=FONT_SMALL)

    # ── Entry ──
    style.configure("TEntry",
                    fieldbackground=CARD, foreground=TEXT,
                    bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                    insertcolor=TEXT, font=FONT)
    style.map("TEntry",
              fieldbackground=[("focus", SURFACE)],
              bordercolor=[("focus", BLUE)])

    # ── Combobox ──
    style.configure("TCombobox",
                    fieldbackground=CARD, foreground=TEXT,
                    background=CARD, bordercolor=BORDER,
                    arrowcolor=TEXT_DIM, font=FONT)
    style.map("TCombobox",
              fieldbackground=[("focus", SURFACE)],
              bordercolor=[("focus", BLUE)])

    # ── Treeview ──
    style.configure("Treeview",
                    background=SURFACE, foreground=TEXT,
                    fieldbackground=SURFACE, borderwidth=0,
                    rowheight=24, font=FONT)
    style.configure("Treeview.Heading",
                    background=CARD, foreground=TEXT_DIM,
                    bordercolor=BORDER, font=FONT_BOLD)
    style.map("Treeview",
              background=[("selected", HOVER)],
              foreground=[("selected", TEXT)])
    style.map("Treeview.Heading",
              background=[("active", HOVER)])

    # ── Notebook (Tabs) ──
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=CARD, foreground=TEXT_DIM,
                    padding=(12, 6), font=FONT)
    style.map("TNotebook.Tab",
              background=[("selected", SURFACE)],
              foreground=[("selected", TEXT)])

    # ── Scrollbar ──
    style.configure("Vertical.TScrollbar",
                    background=CARD, troughcolor=BG,
                    bordercolor=BG, arrowcolor=TEXT_MUTED,
                    lightcolor=CARD, darkcolor=CARD)
    style.map("Vertical.TScrollbar",
              background=[("active", HOVER)])
    style.configure("Horizontal.TScrollbar",
                    background=CARD, troughcolor=BG,
                    bordercolor=BG, arrowcolor=TEXT_MUTED,
                    lightcolor=CARD, darkcolor=CARD)

    # ── Progressbar ──
    style.configure("TProgressbar",
                    background=BLUE, troughcolor=CARD,
                    bordercolor=BORDER, lightcolor=BLUE, darkcolor=BLUE)
    style.configure("Green.Horizontal.TProgressbar", background=GREEN)
    style.configure("Yellow.Horizontal.TProgressbar", background=YELLOW)

    # ── Separator ──
    style.configure("TSeparator", background=BORDER)

    # ── PanedWindow ──
    style.configure("TPanedwindow", background=BORDER)
    style.configure("Sash", sashthickness=4, gripcount=0)

    # ── Checkbutton ──
    style.configure("TCheckbutton",
                    background=BG, foreground=TEXT, font=FONT,
                    indicatorcolor=CARD, indicatorrelief="flat")
    style.map("TCheckbutton",
              indicatorcolor=[("selected", BLUE)],
              background=[("active", BG)])

    # ── Radiobutton ──
    style.configure("TRadiobutton",
                    background=BG, foreground=TEXT, font=FONT,
                    indicatorcolor=CARD)
    style.map("TRadiobutton",
              indicatorcolor=[("selected", BLUE)],
              background=[("active", BG)])

    # ── LabelFrame ──
    style.configure("TLabelframe",
                    background=BG, foreground=TEXT_DIM,
                    bordercolor=BORDER, font=FONT)
    style.configure("TLabelframe.Label",
                    background=BG, foreground=TEXT_DIM, font=FONT_BOLD)

    # ── Scale ──
    style.configure("TScale",
                    background=BG, troughcolor=CARD,
                    bordercolor=BORDER, lightcolor=BLUE, darkcolor=BLUE)

    return style
