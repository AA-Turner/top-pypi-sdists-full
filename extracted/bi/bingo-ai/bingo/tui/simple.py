"""
Bingo TUI - 단순하고 안정적인 레이아웃
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, DirectoryTree, Static, Input, RichLog
from textual.binding import Binding
from pathlib import Path


class BingoTUI(App):
    """Bingo TUI - Cursor 스타일"""

    CSS = """
    Screen {
        background: #1e1e1e;
    }

    #sidebar {
        width: 30%;
        border-right: solid #3c3c3c;
        background: #252526;
    }

    #main-content {
        width: 70%;
        background: #1e1e1e;
    }

    #file-tree {
        height: 1fr;
        background: #252526;
    }

    #chat-log {
        height: 1fr;
        background: #1e1e1e;
        border: solid #3c3c3c;
    }

    #chat-input {
        dock: bottom;
        height: 3;
        border: solid #007acc;
    }

    #status {
        dock: bottom;
        background: #007acc;
        color: white;
        height: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """레이아웃 구성"""
        yield Header(show_clock=True)

        with Horizontal():
            # 좌측: 파일 트리
            with Container(id="sidebar"):
                yield Static("📁 FILES", classes="panel-title")
                yield DirectoryTree(str(Path.cwd()), id="file-tree")

            # 우측: 채팅
            with Vertical(id="main-content"):
                yield Static("💬 CHAT", classes="panel-title")
                yield RichLog(id="chat-log", highlight=True, markup=True)
                yield Input(placeholder="Type message or /command...", id="chat-input")

        yield Static("Bingo v7.1.6 | Ctrl+C: Quit", id="status")
        yield Footer()

    def on_mount(self) -> None:
        """앱 시작"""
        log = self.query_one("#chat-log", RichLog)
        log.write("[bold green]Welcome to Bingo![/]")
        log.write("[dim]Type /help for commands[/]")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """채팅 입력"""
        if event.input.id != "chat-input":
            return

        message = event.value.strip()
        if not message:
            return

        log = self.query_one("#chat-log", RichLog)
        log.write(f"[bold cyan]You:[/] {message}")

        event.input.value = ""

        # 슬래시 명령어
        if message.startswith("/"):
            await self.handle_command(message, log)
        else:
            log.write(f"[bold green]Bingo:[/] Processing...")

    async def handle_command(self, cmd: str, log: RichLog):
        """명령어 처리"""
        if cmd == "/help":
            log.write("[bold]Commands:[/]")
            log.write("/help - Show this help")
            log.write("/clear - Clear chat")
            log.write("/exit - Exit app")
        elif cmd == "/clear":
            log.clear()
        elif cmd == "/exit":
            self.exit()
        else:
            log.write(f"[red]Unknown command:[/] {cmd}")

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """파일 선택 - 내용 표시"""
        log = self.query_one("#chat-log", RichLog)

        try:
            content = event.path.read_text(encoding='utf-8')
            log.write(f"[bold yellow]📄 {event.path.name}[/]")
            log.write("─" * 60)

            # 파일 내용 표시 (최대 50줄)
            lines = content.split('\n')
            if len(lines) > 50:
                for line in lines[:50]:
                    log.write(line)
                log.write(f"[dim]... ({len(lines) - 50} more lines)[/]")
            else:
                for line in lines:
                    log.write(line)

            log.write("─" * 60)
        except Exception as e:
            log.write(f"[red]Error reading file:[/] {e}")


def run_tui():
    """TUI 실행"""
    app = BingoTUI()
    app.run()
