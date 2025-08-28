import difflib
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, List, Literal, Optional, Tuple, Union

import click
from prompt_toolkit import prompt as prompt_toolkit_prompt
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.filters import IsDone
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import ConditionalContainer, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.patch_stdout import patch_stdout as pt_patch_stdout
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style as PromptStyle
from pydantic import BaseModel, Field
from pydantic_ai import RunContext
from requests import Response

from tinybird.tb.modules.agent.memory import load_history
from tinybird.tb.modules.feedback_manager import FeedbackManager

try:
    from colorama import Back, Fore, Style, init

    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class TinybirdAgentContext(BaseModel):
    folder: str
    workspace_id: str
    workspace_name: str
    thinking_animation: Any
    get_project_files: Callable[[], List[str]]
    build_project: Callable[..., None]
    build_project_test: Callable[..., None]
    deploy_project: Callable[..., None]
    deploy_check_project: Callable[[], None]
    mock_data: Callable[..., list[dict[str, Any]]]
    append_data_local: Callable[..., None]
    append_data_cloud: Callable[..., None]
    analyze_fixture: Callable[..., dict[str, Any]]
    execute_query_cloud: Callable[..., dict[str, Any]]
    execute_query_local: Callable[..., dict[str, Any]]
    request_endpoint_cloud: Callable[..., dict[str, Any]]
    request_endpoint_local: Callable[..., dict[str, Any]]
    get_pipe_data_test: Callable[..., Response]
    get_datasource_datafile_cloud: Callable[..., str]
    get_datasource_datafile_local: Callable[..., str]
    get_pipe_datafile_cloud: Callable[..., str]
    get_pipe_datafile_local: Callable[..., str]
    get_connection_datafile_cloud: Callable[..., str]
    get_connection_datafile_local: Callable[..., str]
    run_tests: Callable[..., Optional[str]]
    dangerously_skip_permissions: bool
    token: str
    user_token: str
    host: str
    local_host: str
    local_token: str
    run_id: Optional[str] = None
    get_plan: Callable[..., Optional[str]]
    start_plan: Callable[..., str]
    cancel_plan: Callable[..., Optional[str]]


default_style = PromptStyle.from_dict(
    {
        "separator": "#6C6C6C",
        "questionmark": "#FF9D00 bold",
        "selected": "#5F819D",
        "pointer": "#FF9D00 bold",
        "instruction": "",  # default
        "answer": "#5F819D bold",
        "question": "",
    }
)


class Separator:
    line = "-" * 15

    def __init__(self, line=None):
        if line:
            self.line = line

    def __str__(self):
        return self.line


class PromptParameterException(ValueError):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__("You must provide a `%s` value" % message, errors)


class InquirerControl(FormattedTextControl):
    def __init__(self, choices, default, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.choices = choices
        self._init_choices(choices, default)
        super().__init__(self._get_choice_tokens, **kwargs)

    def _init_choices(self, choices, default):
        # helper to convert from question format to internal format
        self.choices = []  # list (name, value, disabled)
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append((c, None, None))
            else:
                if isinstance(c, str):
                    self.choices.append((c, c, None))
                else:
                    name = c.get("name")
                    value = c.get("value", name)
                    disabled = c.get("disabled", None)
                    self.choices.append((name, value, disabled))
                    if value == default:
                        self.selected_option_index = i
                        searching_first_choice = False
                if searching_first_choice:
                    self.selected_option_index = i  # found the first choice
                    searching_first_choice = False
                if default and (default in (i, c)):
                    self.selected_option_index = i  # default choice exists
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens: list[Any] = []

        def append(index, choice):
            selected = index == self.selected_option_index

            def select_item():
                self.selected_option_index = index
                self.answered = True
                get_app().exit(result=self.get_selection()[0])

            if isinstance(choice[0], Separator):
                tokens.append(("class:separator", "  %s\n" % choice[0]))
            else:
                tokens.append(
                    (
                        "",
                        "\u276f " if selected else "  ",
                    )
                )
                if selected:
                    tokens.append(("[SetCursorPosition]", ""))
                if choice[2]:  # disabled
                    tokens.append(
                        (
                            "",
                            "- %s (%s)" % (choice[0], choice[2]),
                        )
                    )
                else:
                    try:
                        tokens.append(
                            (
                                "",
                                str(choice[0]),
                                select_item,
                            )
                        )
                    except Exception:
                        tokens.append(
                            (
                                "",
                                choice[0],
                                select_item,
                            )
                        )
                tokens.append(("", "\n"))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def get_selection(self):
        return self.choices[self.selected_option_index]


def prompt_question(message, **kwargs):
    # TODO disabled, dict choices
    if "choices" not in kwargs:
        raise PromptParameterException("choices")

    choices = kwargs.pop("choices", None)
    default = kwargs.pop("default", None)
    style = kwargs.pop("style", default_style)

    ic = InquirerControl(choices, default=default)

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:question", "%s " % message))
        if ic.answered:
            tokens.append(("class:answer", " " + ic.get_selection()[0]))
        else:
            tokens.append(("class:instruction", " (Use arrow keys)"))
        return tokens

    # assemble layout
    layout = HSplit(
        [
            Window(height=D.exact(1), content=FormattedTextControl(get_prompt_tokens)),
            ConditionalContainer(Window(ic), filter=~IsDone()),
        ]
    )

    # key bindings
    kb = KeyBindings()

    @kb.add("c-q", eager=True)
    @kb.add("c-c", eager=True)
    def _(event):
        raise KeyboardInterrupt()
        # event.app.exit(result=None)

    @kb.add("down", eager=True)
    def move_cursor_down(event):
        def _next():
            ic.selected_option_index = (ic.selected_option_index + 1) % ic.choice_count

        _next()
        while isinstance(ic.choices[ic.selected_option_index][0], Separator) or ic.choices[ic.selected_option_index][2]:
            _next()

    @kb.add("up", eager=True)
    def move_cursor_up(event):
        def _prev():
            ic.selected_option_index = (ic.selected_option_index - 1) % ic.choice_count

        _prev()
        while isinstance(ic.choices[ic.selected_option_index][0], Separator) or ic.choices[ic.selected_option_index][2]:
            _prev()

    @kb.add("enter", eager=True)
    def set_answer(event):
        ic.answered = True
        event.app.exit(result=ic.get_selection()[1])

    return Application(layout=Layout(layout), key_bindings=kb, mouse_support=False, style=style)


def prompt(questions, answers=None, **kwargs):
    if isinstance(questions, dict):
        questions = [questions]
    answers = answers or {}

    patch_stdout = kwargs.pop("patch_stdout", False)
    kbi_msg = kwargs.pop("keyboard_interrupt_msg", "Cancelled by user")
    raise_kbi = kwargs.pop("raise_keyboard_interrupt", False)

    for question in questions:
        # import the question
        if "type" not in question:
            raise PromptParameterException("type")
        if "name" not in question:
            raise PromptParameterException("name")
        if "message" not in question:
            raise PromptParameterException("message")
        try:
            choices = question.get("choices")
            if choices is not None and callable(choices):
                question["choices"] = choices(answers)

            _kwargs = {}
            _kwargs.update(kwargs)
            _kwargs.update(question)
            type_ = _kwargs.pop("type")
            name = _kwargs.pop("name")
            message = _kwargs.pop("message")
            when = _kwargs.pop("when", None)
            filter = _kwargs.pop("filter", None)

            if when:
                # at least a little sanity check!
                if callable(question["when"]):
                    try:
                        if not question["when"](answers):
                            continue
                    except Exception as e:
                        raise ValueError("Problem in 'when' check of %s question: %s" % (name, e))
                else:
                    raise ValueError("'when' needs to be function that accepts a dict argument")
            if filter and not callable(question["filter"]):
                raise ValueError("'filter' needs to be function that accepts an argument")

            if callable(question.get("default")):
                _kwargs["default"] = question["default"](answers)

            with pt_patch_stdout() if patch_stdout else _dummy_context_manager():
                result = prompt_question(message, **_kwargs)

                if isinstance(result, PromptSession):
                    answer = result.prompt()
                elif isinstance(result, Application):
                    answer = result.run()
                else:
                    # assert isinstance(answer, str)
                    answer = result

                # answer = application.run(
                #    return_asyncio_coroutine=return_asyncio_coroutine,
                #    true_color=true_color,
                #    refresh_interval=refresh_interval)

            if answer is not None:
                if filter:
                    try:
                        answer = question["filter"](answer)
                    except Exception as e:
                        raise ValueError("Problem processing 'filter' of %s question: %s" % (name, e))
                answers[name] = answer
        except AttributeError:
            raise ValueError("No question type '%s'" % type_)
        except KeyboardInterrupt as exc:
            if raise_kbi:
                raise exc from None
            if kbi_msg:
                click.echo(kbi_msg)
            return {}
    return answers


@contextmanager
def _dummy_context_manager():
    yield


def show_options(options: List[str], title: str = "Select an option") -> Optional[str]:
    questions = [
        {
            "type": "list",
            "name": "option",
            "message": title,
            "choices": options,
        }
    ]
    result = prompt(questions)

    if "option" not in result:
        return None

    return result["option"]


ConfirmationResult = Literal["yes", "review"]


def load_existing_resources(folder: str) -> str:
    """Load existing Tinybird resources from the workspace"""
    existing_resources = []

    # Check for datasources
    datasources_dir = os.path.join(folder, "datasources")
    if os.path.exists(datasources_dir):
        for file in os.listdir(datasources_dir):
            if file.endswith(".datasource"):
                file_path = os.path.join(datasources_dir, file)
                try:
                    with open(file_path, "r") as f:
                        existing_resources.append(f"DATASOURCE {file}:\n{f.read()}\n")
                except Exception as e:
                    click.echo(f"Warning: Could not read {file_path}: {e}")

    # Check for pipes
    pipes_dir = os.path.join(folder, "pipes")
    if os.path.exists(pipes_dir):
        for file in os.listdir(pipes_dir):
            if file.endswith(".pipe"):
                file_path = os.path.join(pipes_dir, file)
                try:
                    with open(file_path, "r") as f:
                        existing_resources.append(f"PIPE {file}:\n{f.read()}\n")
                except Exception as e:
                    click.echo(f"Warning: Could not read {file_path}: {e}")

    # Check for connections
    connections_dir = os.path.join(folder, "connections")
    if os.path.exists(connections_dir):
        for file in os.listdir(connections_dir):
            if file.endswith(".connection"):
                file_path = os.path.join(connections_dir, file)
                try:
                    with open(file_path, "r") as f:
                        existing_resources.append(f"CONNECTION {file}:\n{f.read()}\n")
                except Exception as e:
                    click.echo(f"Warning: Could not read {file_path}: {e}")

    return "\n".join(existing_resources)


class Datafile(BaseModel):
    """Represents a generated Tinybird datafile"""

    type: str
    name: str
    content: str
    description: str
    pathname: str
    dependencies: List[str] = Field(default_factory=list)


def create_terminal_box(content: str, new_content: Optional[str] = None, title: Optional[str] = None) -> str:
    """
    Create a formatted box with automatic line numbers that fills the terminal width.
    Optionally shows a diff between content and new_content.

    Args:
        content: The original text content to display in the box (without line numbers)
        new_content: Optional new content to show as a diff against the original
        title: Optional title to display as header, if not provided will use first line of content

    Returns:
        A string containing the formatted box with line numbers added
    """
    # Get terminal width, default to 80 if can't determine
    try:
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 80

    # Box characters
    top_left = "╭"
    top_right = "╮"
    bottom_left = "╰"
    bottom_right = "╯"
    horizontal = "─"
    vertical = "│"

    # Calculate available width for content (terminal_width - 2 borders - 2 spaces padding)
    available_width = terminal_width - 4

    # Split content into lines
    lines = content.strip().split("\n")
    new_lines = new_content.strip().split("\n") if new_content else []

    # Check if we have a title parameter or should use first line as header
    header = title
    content_lines = lines
    new_content_lines = new_lines

    if header is None and lines:
        # Use first line as header if no title provided
        header = lines[0]
        content_lines = lines[1:] if len(lines) > 1 else []
        if new_lines:
            # Skip header in new content too
            new_content_lines = new_lines[1:] if len(new_lines) > 1 else []
    elif header is not None:
        # Title provided, use all content lines as-is
        content_lines = lines
        new_content_lines = new_lines

    # Process content lines
    processed_lines = []

    if new_content is None:
        # No diff, just add line numbers
        line_number = 1
        for line in content_lines:
            processed_lines.extend(_process_line(line, line_number, available_width, None))
            line_number += 1
    else:
        # Create diff and process it properly
        diff = list(
            difflib.unified_diff(
                content_lines,
                new_content_lines,
                lineterm="",
                n=3,  # Add some context lines
            )
        )

        # Process the unified diff output
        old_line_num = 1
        new_line_num = 1
        old_index = 0
        new_index = 0

        # Parse the diff output
        i = 0
        while i < len(diff):
            line = diff[i]
            if line.startswith("@@"):
                # Parse hunk header to get line numbers
                import re

                match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
                if match:
                    old_line_num = int(match.group(1))
                    new_line_num = int(match.group(2))
                    old_index = old_line_num - 1
                    new_index = new_line_num - 1
            elif line.startswith("---") or line.startswith("+++"):
                # Skip file headers
                pass
            elif line.startswith(" "):
                # Context line (unchanged)
                content = line[1:]  # Remove the leading space
                if old_index < len(content_lines) and content_lines[old_index] == content:
                    processed_lines.extend(_process_line(content, old_line_num, available_width, None))
                    old_line_num += 1
                    new_line_num += 1
                    old_index += 1
                    new_index += 1
            elif line.startswith("-"):
                # Removed line
                content = line[1:]  # Remove the leading minus
                processed_lines.extend(_process_line(content, old_line_num, available_width, "-"))
                old_line_num += 1
                old_index += 1
            elif line.startswith("+"):
                # Added line
                content = line[1:]  # Remove the leading plus
                processed_lines.extend(_process_line(content, new_line_num, available_width, "+"))
                new_line_num += 1
                new_index += 1
            i += 1

        # Add any remaining unchanged lines that weren't in the diff
        while old_index < len(content_lines) and new_index < len(new_content_lines):
            if content_lines[old_index] == new_content_lines[new_index]:
                processed_lines.extend(_process_line(content_lines[old_index], old_line_num, available_width, None))
                old_line_num += 1
                new_line_num += 1
                old_index += 1
                new_index += 1
            else:
                break

    # Build the box
    result = []

    # Top border
    result.append(top_left + horizontal * (terminal_width - 2) + top_right)

    # Add header if exists
    if header:
        # Center the header
        header_padding = (available_width - len(header)) // 2
        header_line = (
            vertical
            + " "
            + " " * header_padding
            + header
            + " " * (available_width - len(header) - header_padding)
            + " "
            + vertical
        )
        result.append(header_line)
        # Empty line after header
        result.append(vertical + " " * (terminal_width - 2) + vertical)

    # Content lines
    for line_num, content, diff_marker in processed_lines:
        if line_num is not None:
            # Line with number
            if COLORAMA_AVAILABLE:
                line_num_str = f"{Fore.LIGHTBLACK_EX}{line_num:>4}{Style.RESET_ALL}"
            else:
                line_num_str = f"{line_num:>4}"

            if diff_marker:
                if COLORAMA_AVAILABLE:
                    if diff_marker == "-":
                        # Fill the entire content area with red background
                        content_with_bg = f"{Back.RED}{diff_marker}   {content}{Style.RESET_ALL}"
                        # Calculate padding needed for the content area
                        content_area_width = available_width - 9  # 9 is reduced prefix length
                        content_padding = content_area_width - len(f"{diff_marker}   {content}")
                        if content_padding > 0:
                            content_with_bg = (
                                f"{Back.RED}{diff_marker}   {content}{' ' * content_padding}{Style.RESET_ALL}"
                            )
                        line = f"{vertical} {line_num_str} {content_with_bg}"
                    elif diff_marker == "+":
                        # Fill the entire content area with green background
                        content_with_bg = f"{Back.GREEN}{diff_marker}   {content}{Style.RESET_ALL}"
                        # Calculate padding needed for the content area
                        content_area_width = available_width - 9  # 9 is reduced prefix length
                        content_padding = content_area_width - len(f"{diff_marker}   {content}")
                        if content_padding > 0:
                            content_with_bg = (
                                f"{Back.GREEN}{diff_marker}   {content}{' ' * content_padding}{Style.RESET_ALL}"
                            )
                        line = f"{vertical} {line_num_str} {content_with_bg}"
                else:
                    line = f"{vertical} {line_num:>4} {diff_marker}   {content}"
            else:
                line = f"{vertical} {line_num_str}     {content}"
        else:
            # Continuation line without number - fill background starting from where symbol would be
            if diff_marker and COLORAMA_AVAILABLE:
                if diff_marker == "-":
                    # Calculate how much space we need to fill with background
                    content_area_width = available_width - 9  # 9 is reduced prefix length
                    content_padding = content_area_width - len(
                        content
                    )  # Don't subtract spaces, they're in the background
                    if content_padding > 0:
                        line = f"{vertical}      {Back.RED}    {content}{' ' * content_padding}{Style.RESET_ALL}"
                    else:
                        line = f"{vertical}      {Back.RED}    {content}{Style.RESET_ALL}"
                elif diff_marker == "+":
                    # Calculate how much space we need to fill with background
                    content_area_width = available_width - 9  # 9 is reduced prefix length
                    content_padding = content_area_width - len(
                        content
                    )  # Don't subtract spaces, they're in the background
                    if content_padding > 0:
                        line = f"{vertical}      {Back.GREEN}    {content}{' ' * content_padding}{Style.RESET_ALL}"
                    else:
                        line = f"{vertical}      {Back.GREEN}    {content}{Style.RESET_ALL}"
            else:
                line = f"{vertical}          {content}"

        # Pad to terminal width
        # Need to account for ANSI escape sequences not taking visual space
        if COLORAMA_AVAILABLE:
            # Calculate visible length (excluding ANSI codes)
            visible_line = line
            # Remove all ANSI escape sequences for length calculation
            import re

            ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
            visible_line = ansi_escape.sub("", visible_line)
            padding_needed = terminal_width - len(visible_line) - 1
        else:
            padding_needed = terminal_width - len(line) - 1

        line += " " * padding_needed + vertical
        result.append(line)

    # Empty line before bottom (only if we have content)
    if processed_lines:
        result.append(vertical + " " * (terminal_width - 2) + vertical)

    # Bottom border
    result.append(bottom_left + horizontal * (terminal_width - 2) + bottom_right)

    return "\n".join(result)


def _process_line(
    line: str, line_number: int, available_width: int, diff_marker: Optional[str]
) -> List[Tuple[Optional[int], str, Optional[str]]]:
    """
    Process a single line, handling wrapping if necessary.

    Returns a list of tuples (line_number, content, diff_marker)
    """
    # Calculate space needed for line number and spacing
    # " 9999     " for normal lines or " 9999 +   " for diff lines
    prefix_length = 9  # Reduced from 13 to 9

    # Available width for actual content
    content_width = available_width - prefix_length

    processed: List[Tuple[Optional[int], str, Optional[str]]] = []

    if len(line) <= content_width:
        # Line fits, add it as is
        processed.append((line_number, line, diff_marker))
    else:
        # Line needs wrapping
        # First line with line number
        first_part = line[:content_width]
        processed.append((line_number, first_part, diff_marker))

        # Remaining wrapped lines without line numbers
        remaining = line[content_width:]
        while remaining:
            if len(remaining) <= content_width:
                processed.append((None, remaining, diff_marker))
                break
            else:
                processed.append((None, remaining[:content_width], diff_marker))
                remaining = remaining[content_width:]

    return processed


def show_input(workspace_name: str) -> str:
    return prompt_toolkit_prompt(
        [("class:prompt", f"tb ({workspace_name}) » ")],
        history=load_history(),
        cursor=CursorShape.BLOCK,
        style=PromptStyle.from_dict(
            {
                "prompt": "fg:#27f795 bold",
                "": "",  # Normal color for user input
            }
        ),
    )


class AgentRunCancelled(Exception):
    """Exception raised when user cancels an operation"""

    pass


class SubAgentRunCancelled(Exception):
    """Exception raised when sub-agent cancels an operation"""

    pass


def show_confirmation(title: str, skip_confirmation: bool = False, show_review: bool = True) -> ConfirmationResult:
    if skip_confirmation:
        return "yes"

    while True:
        result = show_options(
            options=["Yes, continue", "No, tell Tinybird Code what to do", "Cancel"]
            if show_review
            else ["Yes, continue", "Cancel"],
            title=title,
        )

        if result is None:  # Cancelled
            raise AgentRunCancelled(f"User cancelled the operation: {title}")

        if result.startswith("Yes"):
            return "yes"
        elif result.startswith("No"):
            return "review"

        raise AgentRunCancelled(f"User cancelled the operation: {title}")


def show_env_options(ctx: "RunContext[TinybirdAgentContext]") -> Optional[bool]:
    """Show environment options for user to choose between local and cloud.

    Args:
        ctx: The run context containing TinybirdAgentContext

    Returns:
        bool: True for cloud, False for local, None if cancelled
    """

    ctx.deps.thinking_animation.stop()
    click.echo(FeedbackManager.highlight(message="» Agent is uncertain about target environment"))

    choice = show_options(
        options=["Tinybird Local", f"Tinybird Cloud ({ctx.deps.host})"], title="Where should this query be executed?"
    )
    ctx.deps.thinking_animation.start()

    if choice is None:
        return None

    return choice.startswith("Tinybird Cloud")


def copy_fixture_to_project_folder_if_needed(
    ctx: RunContext[TinybirdAgentContext], fixture_pathname: str
) -> Union[Path, str]:
    """Copy a fixture data file to the project folder if it's outside the project folder"""
    # Check if the path is absolute and outside the project folder
    input_path = Path(fixture_pathname).expanduser()
    project_folder = Path(ctx.deps.folder)

    if input_path.is_absolute():
        # Check if the file exists outside the project
        if input_path.exists() and not _is_path_inside_project(input_path, project_folder):
            # Ask for confirmation to copy the file
            click.echo(FeedbackManager.highlight(message=f"» File {fixture_pathname} is outside the project folder."))
            active_plan = ctx.deps.get_plan() is not None
            confirmation = show_confirmation(
                title=f"Copy {input_path.name} to project folder for analysis?",
                skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
            )

            if confirmation == "review":
                feedback = show_input(ctx.deps.workspace_name)
                return f"User did not confirm file copy and gave the following feedback: {feedback}"

            # Copy the file to the project folder
            destination_path = project_folder / "fixtures" / input_path.name
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            if destination_path.exists():
                return f"Error: File {input_path.name} already exists in the project folder. Please rename the source file or remove the existing file first."

            shutil.copy2(input_path, destination_path)
            click.echo(FeedbackManager.success(message=f"✓ File copied to {destination_path.name}"))

            # Update the path to the copied file
            fixture_path = destination_path
        else:
            # File is absolute but inside project or doesn't exist
            fixture_path = input_path
    else:
        # Relative path, treat as before
        fixture_path = project_folder / fixture_pathname.lstrip("/")

    return fixture_path


def _is_path_inside_project(file_path: Path, project_path: Path) -> bool:
    """Check if a file path is inside the project folder"""
    try:
        file_path.resolve().relative_to(project_path.resolve())
        return True
    except ValueError:
        return False


def limit_result_output(
    result: dict[str, Any], max_rows: int = 10, max_column_length: int = 200
) -> tuple[dict[str, Any], set[str]]:
    """
    Limit result output by truncating column values and limiting number of rows.
    Modifies the result dict in place and returns truncation info.

    Args:
        result: Result dictionary containing 'data' key with list of row dictionaries
        max_rows: Maximum number of rows to return
        max_column_length: Maximum length for column values before truncation

    Returns:
        Tuple of (modified_result, truncated_columns_set)
    """
    truncated_columns: set[str] = set()

    # Handle case where data doesn't exist or is empty
    if not result.get("data"):
        return result, truncated_columns

    result_data = result["data"]

    # Limit to max_rows
    limited_data = result_data[:max_rows]

    # Truncate column values and track which columns were truncated
    for row in limited_data:
        for column, value in row.items():
            value_str = str(value)
            if len(value_str) > max_column_length:
                row[column] = value_str[:max_column_length] + "..."
                truncated_columns.add(column)

    # Update the result dict with limited data
    result["data"] = limited_data

    return result, truncated_columns
