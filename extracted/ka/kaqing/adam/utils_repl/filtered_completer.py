from typing import Iterable
from prompt_toolkit.completion import CompleteEvent, Completer, Completion, WordCompleter
from prompt_toolkit.document import Document

from adam.commands.command import Command
from adam.commands.command_filter import CommandFilter
from adam.utils import deep_sort_dict
from adam.utils_apps.apps import Apps
from adam.utils_log import log_exc, log_timing
from adam.utils_repl.repl_completer import ReplCompleter, merge_completions
from adam.utils_repl.repl_state import ReplState

class FilteredCompleter(Completer):
    def __init__(self, state: ReplState, filters: list[CommandFilter], cmd_list: list[Command], ignore_case = False) -> None:
        self.state = state
        self.filters = filters
        self.cmd_list = cmd_list
        self.ignore_case = ignore_case

        # warm up
        self.command_completions()

    def __repr__(self) -> str:
        return "SetCompleter(%r, ignore_case=%r)" % (self.options, self.ignore_case)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        # Split document.
        text = document.text_before_cursor.lstrip(' ,')
        stripped_len = len(document.text_before_cursor) - len(text)

        # If there is a space, check for the first term, and use a
        # subcompleter.
        if "," in text or " " in text:
            first_term = text.split(',')[0].split(' ')[0]

            sub_filters = []
            filtered_commands = []
            for filter in self.filters:
                filtered_commands.append(filter.command())
                if first_term == filter.command():
                    self.cmd_list = filter.applicable_commands(self.cmd_list)
                else:
                    sub_filters.append(filter)

            opts = self.command_completions()

            # still in the filters
            if not opts or first_term in filtered_commands:
                completer = FilteredCompleter(self.state, sub_filters, self.cmd_list, self.ignore_case)

                remaining_text = text[len(first_term) :].lstrip()
                move_cursor = len(text) - len(remaining_text) + stripped_len

                new_document = Document(
                    remaining_text,
                    cursor_position=document.cursor_position - move_cursor,
                )

                for c in completer.get_completions(new_document, complete_event):
                    yield c

            # If we have a sub completer, use this for the completions.
            if opts and (completer := opts.get(first_term)):
                remaining_text = text[len(first_term) :].lstrip()
                move_cursor = len(text) - len(remaining_text) + stripped_len

                new_document = Document(
                    remaining_text,
                    cursor_position=document.cursor_position - move_cursor,
                )

                for c in completer.get_completions(new_document, complete_event):
                    yield c

        # No space in the input: behave exactly like `WordCompleter`.
        else:
            completer = WordCompleter(
                list([filter.command() for filter in self.filters]), ignore_case=self.ignore_case
            )
            for c in completer.get_completions(document, complete_event):
                yield c

            if opts := self.command_completions():
                completer = WordCompleter(
                    list(opts.keys()), ignore_case=self.ignore_case
                )
                for c in completer.get_completions(document, complete_event):
                    yield c

    def command_completions(self):
        # use sorted command list only for auto-completion
        sorted_cmds = sorted(self.cmd_list, key=lambda cmd: cmd.command())

        completions = {}
        # app commands are available only on a: drive
        if self.state.device == ReplState.A and self.state.app_app:
            completions = log_timing('actions', lambda: Apps(path='apps.yaml').commands())

        for c in sorted_cmds:
            with log_exc(f'* {c.command()} command returned None completions.'):
                completions = log_timing(c.command(), lambda: deep_sort_dict(merge_completions(completions, c.completion(self.state))))

        opts = ReplCompleter.from_nested_dict(completions)
        return opts.options