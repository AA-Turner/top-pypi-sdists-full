import os
import subprocess
import sys
from typing import List

import click
import humanfriendly
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style

from tinybird.tb.client import TinyB
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.feedback_manager import FeedbackManager, bcolors
from tinybird.tb.modules.project import Project
from tinybird.tb.modules.table import format_table


class DynamicCompleter(Completer):
    def __init__(self, project: Project):
        self.project = project
        self.static_commands = [
            "create",
            "mock",
            "test",
            "select",
            "datasource",
            "pipe",
            "endpoint",
            "copy",
        ]
        self.test_commands = ["create", "run", "update"]
        self.sql_keywords = ["select", "from", "where", "group by", "order by", "limit"]

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()

        # Normalize command by removing 'tb' prefix if present
        if words and words[0] == "tb":
            words = words[1:]

        if not words:
            # Show all available commands when no input
            yield from self._yield_static_commands("")
            return

        command = words[0].lower()

        if command == "mock":
            yield from self._handle_mock_completions(words)
        elif command == "test":
            yield from self._handle_test_completions(words)
        elif command == "select" or self._is_sql_query(text.lower()):
            yield from self._handle_sql_completions(text)
        else:
            # Handle general command completions
            yield from self._yield_static_commands(words[-1])

    def _is_sql_query(self, text: str) -> bool:
        """Check if the input looks like a SQL query."""
        sql_starters = ["select", "with"]
        return any(text.startswith(starter) for starter in sql_starters)

    def _handle_sql_completions(self, text: str):
        """Handle completions for SQL queries."""
        text_lower = text.lower()

        # Find the last complete word
        words = text_lower.split()
        if not words:
            return

        # If we're after FROM, suggest filtered datasources and pipes
        if "from" in words:
            from_index = words.index("from")
            # Check if we're typing after FROM
            if len(words) > from_index + 1:
                current_word = words[-1].lower()
                # Suggest filtered datasources and pipes based on current word
                for x in self.project.datasources:
                    if current_word in x.lower():
                        yield Completion(
                            x, start_position=-len(current_word), display=x, style="class:completion.datasource"
                        )
                for x in self.project.pipes:
                    if current_word in x.lower():
                        yield Completion(x, start_position=-len(current_word), display=x, style="class:completion.pipe")
            else:
                # Just typed FROM, show all datasources and pipes
                for x in self.project.datasources:
                    yield Completion(x, start_position=0, display=x, style="class:completion.datasource")
                for x in self.project.pipes:
                    yield Completion(x, start_position=0, display=x, style="class:completion.pipe")
            return

        # If we're starting a query, suggest SQL keywords
        if len(words) <= 2:
            for keyword in self.sql_keywords:
                if keyword.lower().startswith(words[-1]):
                    yield Completion(
                        keyword, start_position=-len(words[-1]), display=keyword, style="class:completion.keyword"
                    )

    def _handle_mock_completions(self, words: List[str]):
        if len(words) == 1 or len(words) == 2:
            # After 'mock', show datasources
            current_word = words[-1]
            for cmd in self.project.datasources:
                if current_word in cmd.lower():
                    yield Completion(
                        cmd,
                        start_position=-len(current_word) if current_word else 0,
                        display=cmd,
                        style="class:completion.datasource",
                    )
            return

    def _handle_test_completions(self, words: List[str]):
        if len(words) == 1:
            for cmd in self.test_commands:
                yield Completion(cmd, start_position=0, display=cmd, style="class:completion.cmd")
            return
        elif len(words) == 2 or len(words) == 3:
            current_word = words[-1]
            for cmd in self.project.pipes:
                if current_word in cmd.lower():
                    yield Completion(
                        cmd,
                        start_position=-len(current_word) if current_word else 0,
                        display=cmd,
                        style="class:completion.pipe",
                    )
            return

    def _yield_static_commands(self, current_word: str):
        for cmd in self.static_commands:
            if cmd.startswith(current_word):
                yield Completion(
                    cmd,
                    start_position=-len(current_word) if current_word else 0,
                    display=cmd,
                    style="class:completion.cmd",
                )

        for cmd in self.project.datasources:
            if current_word in cmd.lower():
                yield Completion(
                    cmd,
                    start_position=-len(current_word) if current_word else 0,
                    display=cmd,
                    style="class:completion.datasource",
                )

        for cmd in self.project.pipes:
            if current_word in cmd.lower():
                yield Completion(
                    cmd,
                    start_position=-len(current_word) if current_word else 0,
                    display=cmd,
                    style="class:completion.pipe",
                )


style = Style.from_dict(
    {
        "prompt": "fg:#34D399 bold",
        "completion.cmd": "fg:#34D399 bg:#111111 bold",
        "completion.datasource": "fg:#AB49D0 bg:#111111",
        "completion.pipe": "fg:#FEA827 bg:#111111",
        "completion.keyword": "fg:#34D399 bg:#111111",
    }
)

key_bindings = KeyBindings()


@key_bindings.add("c-d")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


class Shell:
    def __init__(self, project: Project, tb_client: TinyB, playground: bool = False):
        self.history = self.get_history()
        self.project = project
        self.tb_client = tb_client
        self.env = "cloud" if playground else "local"
        self.prompt_message = "\ntb » "
        self.session: PromptSession = PromptSession(
            completer=DynamicCompleter(project),
            complete_style=CompleteStyle.COLUMN,
            complete_while_typing=True,
            history=self.history,
        )

    def get_history(self):
        try:
            history_file = os.path.expanduser("~/.tb_history")
            return FileHistory(history_file)
        except Exception:
            return None

    def run(self):
        while True:
            try:
                user_input = self.session.prompt(
                    [("class:prompt", self.prompt_message)], style=style, key_bindings=key_bindings
                )
                self.handle_input(user_input)
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)
            except CLIException as e:
                click.echo(str(e))
            except Exception as e:
                # Catch-all for unexpected exceptions
                click.echo(FeedbackManager.error_exception(error=str(e)))

    def handle_input(self, argline):
        line = argline.strip()
        if not line:
            return
        # Implement the command logic here
        # Replace do_* methods with equivalent logic:
        command_parts = line.split(maxsplit=1)
        cmd = command_parts[0].lower()
        arg = command_parts[1] if len(command_parts) > 1 else ""

        if cmd in ["exit", "quit"]:
            sys.exit(0)
        elif cmd == "build":
            self.handle_build()
        elif cmd == "auth":
            self.handle_auth()
        elif cmd == "workspace":
            self.handle_workspace()
        elif cmd == "deploy":
            self.handle_deploy()
        elif cmd == "mock":
            self.handle_mock(arg)
        elif cmd == "tb":
            self.handle_tb(arg)
        else:
            # Check if it looks like a SQL query or run as a tb command
            self.default(line)

    def handle_build(self):
        click.echo(FeedbackManager.error(message="'tb build' is not available in the dev shell"))

    def handle_auth(self):
        click.echo(FeedbackManager.error(message="'tb auth' is not available in the dev shell"))

    def handle_workspace(self):
        click.echo(FeedbackManager.error(message="'tb workspace' is not available in the dev shell"))

    def handle_deploy(self):
        click.echo(FeedbackManager.error(message="'tb deploy' is not available in the dev shell"))

    def handle_mock(self, arg):
        if "mock" in arg.strip().lower():
            arg = arg.replace("mock", "")
        subprocess.run(f"tb --{self.env} mock {arg}", shell=True, text=True)

    def handle_tb(self, argline):
        click.echo("")
        arg = argline.strip().lower()
        if arg.startswith("build"):
            self.handle_build()
        elif arg.startswith("auth"):
            self.handle_auth()
        elif arg.startswith("workspace"):
            self.handle_workspace()
        elif arg.startswith("mock"):
            self.handle_mock(argline)
        else:
            need_skip = ("mock", "test create", "create")
            if any(arg.startswith(cmd) for cmd in need_skip):
                argline = f"{argline}"
            subprocess.run(f"tb --{self.env} {argline}", shell=True, text=True)

    def default(self, argline):
        click.echo("")
        arg = argline.strip().lower()
        if not arg:
            return
        if arg.startswith("with") or arg.startswith("select"):
            self.run_sql(argline)
        elif len(arg.split()) == 1 and arg in self.project.pipes + self.project.datasources:
            self.run_sql(f"select * from {argline}")
        else:
            need_skip = ("mock", "test create", "create")
            if any(arg.startswith(cmd) for cmd in need_skip):
                argline = f"{argline}"
            subprocess.run(f"tb --{self.env} {argline}", shell=True, text=True)

    def run_sql(self, query, rows_limit=20):
        try:
            q = query.strip()
            if q.lower().startswith("insert"):
                click.echo(FeedbackManager.info_append_data())
                raise CLIException(FeedbackManager.error_invalid_query())
            if q.lower().startswith("delete"):
                raise CLIException(FeedbackManager.error_invalid_query())

            res = self.tb_client.query(f"SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON")

            if isinstance(res, dict) and "error" in res:
                click.echo(FeedbackManager.error_exception(error=res["error"]))

            if isinstance(res, dict) and "data" in res and res["data"]:
                print_table_formatted(res, "QUERY")
            else:
                click.echo(FeedbackManager.info_no_rows())

        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))

    def reprint_prompt(self):
        click.echo(f"{bcolors.OKGREEN}{self.prompt_message}{bcolors.ENDC}", nl=False)


def print_table_formatted(res: dict, name: str):
    data = []
    limit = 20
    for d in res["data"][:limit]:
        data.append(d.values())
    meta = res["meta"]
    stats = res.get("statistics", {})
    row_count = stats.get("rows_read", 0)
    elapsed = stats.get("elapsed", 0)
    cols = len(meta)
    try:
        table = format_table(data, meta)
        click.echo(FeedbackManager.highlight(message=f"\n» Running {name}\n"))
        click.echo(table)
        click.echo("")
        rows_read = humanfriendly.format_number(stats.get("rows_read", 0))
        bytes_read = humanfriendly.format_size(stats.get("bytes_read", 0))
        elapsed = humanfriendly.format_timespan(elapsed) if elapsed >= 1 else f"{elapsed * 1000:.2f}ms"
        stats_message = f"» {bytes_read} ({rows_read} rows x {cols} cols) in {elapsed}"
        rows_message = f"» Showing first {limit} rows" if row_count > limit else "» Showing all rows"
        click.echo(FeedbackManager.success(message=stats_message))
        click.echo(FeedbackManager.gray(message=rows_message))
    except ValueError as exc:
        if str(exc) == "max() arg is an empty sequence":
            click.echo("------------")
            click.echo("Empty")
            click.echo("------------")
        else:
            raise exc
