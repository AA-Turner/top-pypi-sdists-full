from __future__ import annotations

from pathlib import Path

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from trajectory.lib.cli.benchmark_source import BenchmarkSource

EXIT = "__exit__"


class NavigationList(OptionList):
  BINDINGS = [
    Binding("j", "cursor_down", "Down", show=False),
    Binding("k", "cursor_up", "Up", show=False),
    Binding("l,right", "select", "Open", show=False),
  ]


class ChoiceApp(App[str | None]):
  CSS = """
  Screen { height: auto; }
  #question { height: auto; padding: 1 2; text-style: bold; }
  OptionList { height: auto; max-height: 12; margin: 0 2; }
  #hint { height: 1; margin: 1 2; color: $text-muted; }
  """
  BINDINGS = [
    Binding("escape,h,left", "cancel", "Back"),
    Binding("ctrl+c,ctrl+d", "quit_setup", "Exit", priority=True),
  ]

  def action_quit_setup(self) -> None:
    self.exit(EXIT)

  def __init__(self, question: str, options: list[tuple[str, str]]) -> None:
    super().__init__()
    self.question = question
    self.options = options

  def compose(self) -> ComposeResult:
    yield Static(self.question, id="question", markup=False)
    yield NavigationList(*(Option(Text(label), id=value) for label, value in self.options))
    yield Static("↑/↓ or j/k Move   Enter/l Select   Esc/h Back   Ctrl+C Exit", id="hint")

  def on_mount(self) -> None:
    self.query_one(OptionList).focus()

  @on(OptionList.OptionSelected)
  def choose(self, event: OptionList.OptionSelected) -> None:
    self.exit(event.option.id)

  def action_cancel(self) -> None:
    self.exit(None)


def choose(question: str, options: list[tuple[str, str]]) -> str | None:
  return ChoiceApp(question, options).run(inline=True)


class DirectoryApp(App[Path | None]):
  CSS = """
  Screen { height: auto; }
  Static { height: auto; padding: 1 2; }
  Input { margin: 0 2; }
  #error { color: $error; }
  """
  BINDINGS = [
    Binding("escape", "cancel", "Back"),
    Binding("ctrl+c,ctrl+d", "cancel", "Exit", priority=True),
  ]

  def __init__(self, directory: Path, question: str = "Which project should we set up?") -> None:
    super().__init__()
    self.directory = directory
    self.question = question

  def compose(self) -> ComposeResult:
    yield Static(self.question, markup=False)
    yield Input(value=str(self.directory), id="directory", select_on_focus=False)
    yield Static("Enter to use this directory · Esc to cancel", id="error", markup=False)

  def on_mount(self) -> None:
    directory = self.query_one(Input)
    directory.focus()
    directory.cursor_position = len(directory.value)

  @on(Input.Submitted)
  def select_directory(self, event: Input.Submitted) -> None:
    directory = Path(event.value).expanduser().resolve()
    if not event.value.strip() or not directory.is_dir():
      self.query_one("#error", Static).update("Enter an existing project directory.")
      return
    self.exit(directory)

  def action_cancel(self) -> None:
    self.exit(None)


def choose_directory(
  directory: Path, question: str = "Which project should we set up?"
) -> Path | None:
  return DirectoryApp(directory, question).run(inline=True)


class RepositoryApp(App[str | None]):
  CSS = DirectoryApp.CSS
  BINDINGS = DirectoryApp.BINDINGS

  def compose(self) -> ComposeResult:
    yield Static("Paste the benchmark repository URL", markup=False)
    yield Input(placeholder="https://github.com/organization/benchmark", id="repository")
    yield Static(
      "HTTPS or git@host:organization/repository.git · Esc to cancel", id="error", markup=False
    )

  def on_mount(self) -> None:
    self.query_one(Input).focus()

  @on(Input.Submitted)
  def select_repository(self, event: Input.Submitted) -> None:
    try:
      source = BenchmarkSource.parse(event.value)
      if source.kind != "repository":
        raise ValueError("Paste a repository URL, or go back to choose a local repository.")
    except ValueError as error:
      self.query_one("#error", Static).update(str(error))
      return
    self.exit(source.value)

  def action_cancel(self) -> None:
    self.exit(None)

  @staticmethod
  def prompt() -> str | None:
    return RepositoryApp().run(inline=True)
