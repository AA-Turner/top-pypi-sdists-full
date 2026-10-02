"""A folder dialog with fixed controls and a separately scrolling directory list.

Loaded only by the import wizard. Browsing reads one directory level; confirming
returns its path to the existing import review flow.
"""

from __future__ import annotations

from pathlib import Path
from collections.abc import Callable

from prompt_toolkit.application import Application
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.data_structures import Point
from prompt_toolkit.document import Document
from prompt_toolkit.filters import Condition, to_filter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, VSplit, Layout, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.widgets import Button, Frame, TextArea

from . import tui


class DirectoryPicker:
    MAX_VISIBLE_FOLDERS = 10
    # Title, two frames, status, actions and help. Whitespace is budgeted
    # separately so it can yield before a control on a short terminal.
    CHROME_ROWS = 9

    def __init__(self, start: Path, list_directories: Callable[[Path], list[Path]]):
        self.here = start.resolve()
        self.list_directories = list_directories
        self.children = list_directories(self.here)
        self.selected = int(bool(self.children) and self.here.parent != self.here)
        self.error = ""

        self.path = TextArea(
            text=str(self.here),
            multiline=False,
            wrap_lines=False,
            height=1,
            focus_on_click=True,
            completer=PathCompleter(
                only_directories=True,
                expanduser=True,
                get_paths=lambda: [str(self.here)],
            ),
            complete_while_typing=False,
            accept_handler=self.open_path,
        )
        self.folders = FormattedTextControl(
            self.folder_rows,
            focusable=True,
            get_cursor_position=lambda: Point(x=0, y=self.selected),
        )
        self.folder_window = Window(
            self.folders,
            height=lambda: Dimension.exact(self.visible_rows()),
            wrap_lines=False,
            always_hide_cursor=True,
        )
        back = Button("< Back (b)", lambda: self.app.exit(result=tui.BACK),
                      width=10, left_symbol="", right_symbol="")
        skip = Button("Skip (s)", lambda: self.app.exit(result=tui.SKIP),
                      width=8, left_symbol="", right_symbol="")
        self.confirm = Button("Import this folder (i) >", self.import_folder,
                              width=24, left_symbol="", right_symbol="")
        back.window.always_hide_cursor = to_filter(True)
        skip.window.always_hide_cursor = to_filter(True)
        self.confirm.window.always_hide_cursor = to_filter(True)
        path_frame = Frame(self.path, title="Current folder · Ctrl+L to edit")
        path_frame.container.style = lambda: (
            "class:frame class:path-box" if self.app.layout.has_focus(self.path) else "class:frame"
        )

        body = HSplit(
            [
                Window(
                    FormattedTextControl(lambda: "\n".join(tui.onboarding_header())),
                    height=lambda: Dimension.exact(len(tui.onboarding_header())),
                    wrap_lines=False,
                ),
                Window(height=lambda: Dimension.exact(self.gap("header"))),
                Window(FormattedTextControl([("bold", "Import a folder")]), height=1),
                Window(height=lambda: Dimension.exact(self.gap("title"))),
                Window(
                    FormattedTextControl(lambda: "\n".join(self.description_lines())),
                    height=lambda: Dimension.exact(len(self.description_lines())),
                    wrap_lines=False,
                ),
                Window(height=lambda: Dimension.exact(self.gap("description"))),
                path_frame,
                Window(height=lambda: Dimension.exact(self.gap("folders"))),
                Frame(self.folder_window, title=self.folder_title),
                Window(FormattedTextControl(self.status), height=1, wrap_lines=False),
                Window(height=lambda: Dimension.exact(self.gap("actions"))),
                VSplit([back, Window(), skip, Window(), self.confirm], height=1),
                Window(height=lambda: Dimension.exact(self.gap("help"))),
                Window(FormattedTextControl(self.hint), height=1, wrap_lines=False),
                Window(height=Dimension(min=0, preferred=0, weight=1)),
            ],
            width=lambda: Dimension.exact(min(tui.CONTENT_WIDTH, max(1, self.size().columns))),
        )
        layout = HSplit(
            [
                Window(height=lambda: Dimension.exact(self.outer_rows().top)),
                VSplit(
                    [Window(width=lambda: tui.left_pad()), body, Window()]
                ),
                Window(height=lambda: Dimension.exact(self.outer_rows().bottom)),
            ]
        )
        self.app = Application(
            layout=Layout(layout, focused_element=self.folders),
            full_screen=True,
            mouse_support=True,
            key_bindings=self.bindings(),
            style=merge_styles(
                [
                    tui.style(),
                    Style.from_dict(
                        {
                            "frame.border": "#868684",
                            "frame.label": "bold",
                            "path-box frame.border": "#5f87ff",
                            "folder.focused": "reverse bold",
                            "button": "noreverse",
                            "button.focused": "reverse bold",
                            "primary": "bg:#5f87ff #000000 bold",
                            "primary button.focused": "reverse bold",
                            "error": "#ff5f5f",
                        }
                    ),
                ]
            ),
        )
        # Style the primary action independently of the secondary Back button.
        self.confirm.window.style = lambda: (
            "class:primary class:button.focused"
            if self.app.layout.has_focus(self.confirm)
            else "class:primary"
        )

        def refresh_action_labels(_app):
            columns = self.size().columns
            label = "Import (i) >" if columns < 50 else "Import this folder (i) >"
            self.confirm.text, self.confirm.width = label, len(label)
            self.confirm.window.width = Dimension.exact(len(label))

        self.app.before_render += refresh_action_labels

    def size(self):
        return self.app.output.get_size()

    def description_lines(self) -> list[str]:
        width = max(1, min(tui.CONTENT_WIDTH, self.size().columns))
        description = (
            "Pick a project folder. Your agent describes its files and results in "
            "Probe. You review the plan before upload."
        )
        lines = tui.wrap(description, width=width)
        available = self.size().rows - self.CHROME_ROWS - len(tui.onboarding_header()) - 1
        if len(lines) > available:
            lines = tui.wrap(
                "Your agent describes the files. You review before upload.",
                width=width,
            )
        return lines

    def chrome_rows(self) -> int:
        return self.CHROME_ROWS + len(tui.onboarding_header()) + len(self.description_lines())

    def visible_rows(self) -> int:
        # Reserve the whole dialog first. Only the folder window may scroll;
        # whitespace yields on short terminals before any control disappears.
        rows = self.size().rows
        chrome = self.chrome_rows() + len(self.gaps())
        return max(1, min(
            len(self.entries()), self.MAX_VISIBLE_FOLDERS, rows - chrome - 2 * self.margin(),
        ))

    def margin(self) -> int:
        minimum = self.chrome_rows() + 1
        return min(tui.safe_margin(self.size().rows), max(0, (self.size().rows - minimum) // 2))

    def gaps(self) -> tuple[str, ...]:
        header = tui.onboarding_header()
        # Keep progress separated from the page and help separated from the
        # actions first. Optional gaps yield before the list loses the parent
        # row and the neighboring folders that explain where the selection is.
        available = self.size().rows - self.chrome_rows() - 2 * self.margin()
        essential = ((("header",) if header else ()) + ("help",))[:max(0, available - 1)]
        folders = min(3, max(1, len(self.entries())))
        optional = ("description", "title", "folders", "actions")[
            :max(0, available - len(essential) - folders)
        ]
        return essential + optional

    def gap(self, name: str) -> int:
        return int(name in self.gaps())

    def outer_rows(self):
        rows = self.size().rows
        margin = self.margin()
        return tui.Frame(top=margin, header=0, body=max(1, rows - 2 * margin), bottom=margin)

    def entries(self) -> list[Path]:
        return ([self.here.parent] if self.here.parent != self.here else []) + self.children

    def folder_title(self):
        count = len(self.children)
        return f"Folders · {count}"

    def folder_rows(self):
        entries = self.entries()
        if not entries:
            return [("class:instruction", "  No subfolders")]
        rows = []
        for i, path in enumerate(entries):
            if i:
                rows.append(("", "\n"))
            active = i == self.selected and self.app.layout.has_focus(self.folders)
            label = "../  Up one folder" if path == self.here.parent else path.name + "/"
            # Names are labels, never terminal control text. Window clipping
            # keeps even a long name on one row, so scrolling stays predictable.
            label = "".join(c if c.isprintable() else "�" for c in label)

            def mouse(event, index=i):
                if event.event_type == MouseEventType.MOUSE_UP:
                    self.selected = index
                    self.app.layout.focus(self.folders)
                elif event.event_type == MouseEventType.SCROLL_DOWN:
                    self.move(3)
                elif event.event_type == MouseEventType.SCROLL_UP:
                    self.move(-3)

            rows.append(
                (
                    "class:folder.focused" if active else "",
                    ("› " if active else "  ") + label,
                    mouse,
                )
            )
        return rows

    def move(self, amount: int):
        self.selected = max(0, min(self.selected + amount, len(self.entries()) - 1))

    def navigate(self, target: Path):
        previous = self.here
        self.here = target.resolve()
        self.children = self.list_directories(self.here)
        entries = self.entries()
        self.selected = (
            entries.index(previous)
            if previous in entries
            else int(bool(self.children) and self.here.parent != self.here)
        )
        self.path.buffer.set_document(Document(str(self.here), cursor_position=0))
        self.error = ""
        self.folder_window.vertical_scroll = 0
        self.app.layout.focus(self.folders)

    def path_target(self) -> Path | None:
        text = self.path.text.strip().strip("'\"")
        try:
            candidate = Path(text).expanduser()
            if not candidate.is_absolute():
                candidate = self.here / candidate
            candidate = candidate.resolve()
            if not text or not candidate.is_dir():
                raise ValueError("Enter an existing folder path.")
        except (OSError, RuntimeError, ValueError):
            self.error = "Folder not found. Check the path and try again."
            self.app.layout.focus(self.path)
            return None
        return candidate

    def open_path(self, _buffer):
        target = self.path_target()
        if target is not None:
            self.navigate(target)
        return True  # Keep the address in the field after Enter.

    def import_folder(self):
        target = self.path_target()
        if target is None:
            return
        if target != self.here:
            # A changed address first opens the folder for inspection. The
            # explicit action always confirms the directory currently shown.
            self.navigate(target)
            return
        self.app.exit(result=self.here)

    def status(self):
        if self.error:
            return [("class:error", self.error)]
        if self.size().columns < 64:
            return [("class:instruction", "Import to review this folder’s files.")]
        if not self.children:
            return [("class:instruction", "No subfolders. You can import this folder.")]
        return [
            ("class:instruction", "Choose a folder, then import. You’ll review its contents next.")
        ]

    def hint(self):
        compact = self.size().columns < 64
        shortcuts = "i Import · s Skip · b Back"
        if self.app.layout.has_focus(self.path):
            text = "Enter Open path · Esc Back"
        elif compact:
            text = f"↑↓ Browse · {shortcuts}"
        elif self.app.layout.has_focus(self.folders):
            text = f"↑↓ Browse · Enter Open · {shortcuts} · Ctrl+L Path"
        else:
            text = f"Enter selects · {shortcuts}"
        return [("class:instruction", text)]

    def bindings(self):
        keys = KeyBindings()
        browsing = Condition(lambda: self.app.layout.has_focus(self.folders))
        actions = Condition(lambda: not self.app.layout.has_focus(self.path))

        @keys.add("tab")
        def next_control(event):
            event.app.layout.focus_next()

        @keys.add("s-tab")
        def previous_control(event):
            event.app.layout.focus_previous()

        @keys.add("c-l")
        def edit_path(event):
            event.app.layout.focus(self.path)
            self.path.buffer.cursor_position = len(self.path.text)

        @keys.add("escape", eager=True)
        @keys.add("b", filter=actions, eager=True)
        def back(event):
            event.app.exit(result=tui.BACK)

        @keys.add("i", filter=actions, eager=True)
        def confirm_folder(_event):
            self.import_folder()

        @keys.add("s", filter=actions, eager=True)
        def skip_folder(event):
            event.app.exit(result=tui.SKIP)

        @keys.add("c-c")
        def quit_picker(event):
            event.app.exit(result=None)

        @keys.add("up", filter=browsing)
        def up(event):
            self.move(-1)

        @keys.add("down", filter=browsing)
        def down(event):
            self.move(1)

        @keys.add("pageup", filter=browsing)
        def page_up(event):
            self.move(-self.visible_rows())

        @keys.add("pagedown", filter=browsing)
        def page_down(event):
            self.move(self.visible_rows())

        @keys.add("home", filter=browsing)
        def first(event):
            self.selected = 0

        @keys.add("end", filter=browsing)
        def last(event):
            self.selected = max(0, len(self.entries()) - 1)

        @keys.add("enter", filter=browsing)
        def open_folder(event):
            entries = self.entries()
            if entries:
                self.navigate(entries[self.selected])

        @keys.add("left", filter=browsing)
        @keys.add("right", filter=browsing)
        @keys.add("backspace", filter=browsing)
        def ignore_navigation_shortcuts(_event):
            pass

        return keys

    def run(self):
        return self.app.run()
