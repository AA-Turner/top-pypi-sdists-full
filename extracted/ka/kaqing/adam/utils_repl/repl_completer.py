import copy
import re
import traceback
from typing import Iterable, TypeVar, cast
from prompt_toolkit.completion import CompleteEvent, Completion, NestedCompleter, WordCompleter
from prompt_toolkit.document import Document

from adam.utils import debug_complete, log2
from adam.utils_repl.appendable_completer import AppendableCompleter

import nest_asyncio
nest_asyncio.apply()

import asyncio

__all__ = [
    "ReplCompleter",
]

T = TypeVar('T')

def merge_completions(dict1, dict2):
    if isinstance(dict1, dict):
        target = dict1.copy()
    else:
        target = copy.copy(dict1)

    try:
        for key, value in dict2.items():
            if key in target:
                debug_complete(f'[{key}] {type(dict2)} is being merged to {type(target[key])} completions')
                if isinstance(value, dict):
                    if isinstance(target[key], dict):
                        target[key] = merge_completions(target[key], value)
                    elif isinstance(target[key], AppendableCompleter):
                        cast(AppendableCompleter, target[key]).append_completions(key, value)
                    elif isinstance(target[key], NestedCompleter):
                        cast(NestedCompleter, target[key]).options = merge_completions(cast(NestedCompleter, target[key]).options, value)
                elif isinstance(value, AppendableCompleter):
                    if isinstance(target[key], dict):
                        cast(AppendableCompleter, value).append_completions(key, target[key])
                        target[key] = value
                    else:
                        log2(f'* {key} of {type(value)} is overriding existing {type(target[key])} completions')
                else:
                    target[key] = value
            else:
                target[key] = value

    except Exception as e:
        traceback.print_exc()

    return target

class ReplCompleter(NestedCompleter):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        # Split document.
        text = document.text_before_cursor.lstrip()
        stripped_len = len(document.text_before_cursor) - len(text)

        # If there is a space, check for the first term, and use a
        # subcompleter.
        if " " in text:
            first_term = text.split()[0]
            completer = self.options.get(first_term)

            # If we have a sub completer, use this for the completions.
            if completer is not None:
                remaining_text = text[len(first_term) :].lstrip()
                move_cursor = len(text) - len(remaining_text) + stripped_len

                new_document = Document(
                    remaining_text,
                    cursor_position=document.cursor_position - move_cursor,
                )

                try:
                    # potential thread racing
                    for c in completer.get_completions(new_document, complete_event):
                        yield c
                except:
                    pass

        # No space in the input: behave exactly like `WordCompleter`.
        else:
            completer = WordCompleter(
                # Allow dot in the middle or a word
                list(self.options.keys()), ignore_case=self.ignore_case, pattern=re.compile(r"([a-zA-Z0-9_\.\@\&]+|[^a-zA-Z0-9_\.\@\&\s]+)")
            )
            for c in completer.get_completions(document, complete_event):
                yield c
