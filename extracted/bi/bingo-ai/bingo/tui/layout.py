"""
Bingo TUI Layout - Cursor/VSCode 스타일 레이아웃
좌측: 파일 트리, 우측: 채팅/에디터
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, DirectoryTree, TextArea, Input, Static, Label
from textual.binding import Binding
from pathlib import Path
from rich.syntax import Syntax
from rich.text import Text
import os


class FilePanel(Container):
    """좌측 파일 패널"""

    def compose(self) -> ComposeResult:
        yield Label("📁 FILES", classes="panel-title")
        yield DirectoryTree(str(Path.cwd()), id="file-tree")


class ChatPanel(Vertical):
    """우측 채팅 패널"""

    def compose(self) -> ComposeResult:
        yield Label("💬 CHAT", classes="panel-title")
        yield Container(id="chat-messages", classes="chat-messages")
        yield Input(placeholder="Type your message or /command...", id="chat-input")


class EditorPanel(Vertical):
    """파일 에디터 패널"""

    def compose(self) -> ComposeResult:
        yield Label("📝 EDITOR", classes="panel-title", id="editor-title")
        yield TextArea("", id="editor", language="python")


class StatusBar(Static):
    """하단 상태바"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = "pentest"
        self.target = ""

    def update_status(self, mode: str = None, target: str = None):
        if mode:
            self.mode = mode
        if target:
            self.target = target

        status = f"[bold cyan]Mode:[/] {self.mode}"
        if self.target:
            status += f" | [bold yellow]Target:[/] {self.target}"

        self.update(status)


class BingoTUI(App):
    """Bingo TUI Main App"""

    CSS = """
    Screen {
        background: #1e1e1e;
    }

    .panel-title {
        background: #252526;
        color: #cccccc;
        padding: 0 1;
        text-style: bold;
    }

    #sidebar {
        width: 30%;
        border-right: solid #3c3c3c;
        background: #252526;
    }

    #main-panel {
        width: 70%;
    }

    #file-tree {
        height: 1fr;
        background: #252526;
        color: #cccccc;
    }

    #chat-messages {
        height: 1fr;
        border: solid #3c3c3c;
        background: #1e1e1e;
        padding: 1;
        overflow-y: auto;
    }

    #chat-input {
        dock: bottom;
        height: 3;
        border: solid #007acc;
    }

    #editor {
        height: 1fr;
        background: #1e1e1e;
    }

    #status-bar {
        dock: bottom;
        background: #007acc;
        color: white;
        padding: 0 1;
        height: 1;
    }

    #tab-bar {
        height: 3;
        background: #2d2d30;
        color: #cccccc;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("tab", "switch_mode", "Switch Mode"),
        Binding("ctrl+o", "open_file", "Open File"),
        Binding("ctrl+s", "save_file", "Save File"),
    ]

    def __init__(self):
        super().__init__()
        self._current_mode = "chat"  # chat or editor
        self._current_file = None

    def compose(self) -> ComposeResult:
        """레이아웃 구성"""
        yield Header(show_clock=True)

        with Horizontal():
            # 좌측 파일 패널
            with Container(id="sidebar"):
                yield FilePanel()

            # 우측 메인 패널
            with Container(id="main-panel"):
                yield Static("Tab: Switch Mode | Ctrl+O: Open | Ctrl+S: Save | Ctrl+C: Quit", id="tab-bar")
                yield ChatPanel(id="chat-panel")
                yield EditorPanel(id="editor-panel", classes="hidden")

        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """앱 시작 시 초기화"""
        self.query_one(StatusBar).update_status(mode="pentest")

    def action_switch_mode(self) -> None:
        """Tab: 채팅 ↔ 에디터 모드 전환"""
        chat_panel = self.query_one("#chat-panel")
        editor_panel = self.query_one("#editor-panel")

        if self._current_mode == "chat":
            chat_panel.add_class("hidden")
            editor_panel.remove_class("hidden")
            self._current_mode = "editor"
        else:
            editor_panel.add_class("hidden")
            chat_panel.remove_class("hidden")
            self._current_mode = "chat"

    def action_open_file(self) -> None:
        """Ctrl+O: 파일 열기"""
        # TODO: 파일 선택 다이얼로그
        pass

    def action_save_file(self) -> None:
        """Ctrl+S: 파일 저장"""
        if self._current_file:
            editor = self.query_one("#editor", TextArea)
            Path(self._current_file).write_text(editor.text)

    def on_directory_tree_file_selected(self, event) -> None:
        """파일 트리에서 파일 선택"""
        file_path = event.path

        if file_path.is_file():
            self.open_file_in_editor(str(file_path))

    def open_file_in_editor(self, file_path: str):
        """에디터에서 파일 열기"""
        path = Path(file_path)

        if not path.exists():
            return

        try:
            content = path.read_text(encoding='utf-8')
            editor = self.query_one("#editor", TextArea)
            editor.text = content

            # 언어 감지
            suffix = path.suffix[1:] if path.suffix else "text"
            if suffix in ["py", "js", "ts", "java", "go", "rs", "cpp", "c", "h"]:
                editor.language = suffix

            # 타이틀 업데이트
            title = self.query_one("#editor-title", Label)
            title.update(f"📝 {path.name}")

            self._current_file = file_path

            # 에디터 모드로 전환
            if self._current_mode == "chat":
                self.action_switch_mode()

        except Exception as e:
            self.notify(f"Error opening file: {e}", severity="error")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """채팅 입력 제출"""
        if event.input.id == "chat-input":
            message = event.value.strip()

            if not message:
                return

            # 메시지 표시
            messages = self.query_one("#chat-messages")
            messages.mount(Static(f"[bold cyan]You:[/] {message}"))

            # 입력창 초기화
            event.input.value = ""

            # 슬래시 명령어 처리
            if message.startswith("/"):
                await self.handle_command(message)
            else:
                # TODO: Agent 호출
                messages.mount(Static(f"[bold green]Bingo:[/] 처리 중..."))

    async def handle_command(self, cmd: str):
        """슬래시 명령어 처리"""
        messages = self.query_one("#chat-messages")

        if cmd == "/help":
            help_text = """
[bold]Commands:[/]
/target <url> - Set target
/model - Change model
/status - Show status
/clear - Clear chat
/files - Show file tree
/exit - Exit
            """
            messages.mount(Static(help_text))

        elif cmd.startswith("/target"):
            parts = cmd.split(maxsplit=1)
            if len(parts) > 1:
                target = parts[1]
                self.query_one(StatusBar).update_status(target=target)
                messages.mount(Static(f"[green]Target set:[/] {target}"))
            else:
                messages.mount(Static("[red]Usage:[/] /target <url>"))

        elif cmd == "/clear":
            messages.remove_children()

        elif cmd == "/exit":
            self.exit()

        else:
            messages.mount(Static(f"[red]Unknown command:[/] {cmd}"))


def run_tui():
    """TUI 실행"""
    app = BingoTUI()
    app.run()
