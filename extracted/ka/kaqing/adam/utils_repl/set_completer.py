import copy
from typing import Iterable
from prompt_toolkit.completion import CompleteEvent, Completer, Completion, NestedCompleter, WordCompleter
from prompt_toolkit.document import Document

class SetCompleter(Completer):
    def __init__(self, words: list[str], options: dict = None, sub_completer = False, ignore_case = False) -> None:
        self.words = words
        self.sub_completer = sub_completer
        if options:
            opts = NestedCompleter.from_nested_dict(options)
            self.options = opts.options
        self.ignore_case = ignore_case

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
            words = copy.copy(self.words)
            if words and first_term in words:
                words.remove(first_term)

            # already moved to nested completion part
            if first_term not in self.options:
                completer = SetCompleter(words, self.options, sub_completer=True)

                # If we have a sub completer, use this for the completions.
                if completer is not None:
                    remaining_text = text[len(first_term) :].lstrip()
                    move_cursor = len(text) - len(remaining_text) + stripped_len

                    new_document = Document(
                        remaining_text,
                        cursor_position=document.cursor_position - move_cursor,
                    )

                    for c in completer.get_completions(new_document, complete_event):
                        yield c

            if self.sub_completer:
                completer = self.options.get(first_term)

                # If we have a sub completer, use this for the completions.
                if completer is not None:
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
                list(self.words), ignore_case=self.ignore_case
            )
            for c in completer.get_completions(document, complete_event):
                yield c

            if self.sub_completer:
                completer = WordCompleter(
                    list(self.options.keys()), ignore_case=self.ignore_case
                )
                for c in completer.get_completions(document, complete_event):
                    yield c