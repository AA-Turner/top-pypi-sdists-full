from typing import Callable, Iterable, List, Mapping, Optional, Pattern, Union

from prompt_toolkit.completion import CompleteEvent, Completion, WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import AnyFormattedText

__all__ = [
    "TermCompleter",
]

class TermCompleter(WordCompleter):
    def __init__(
        self,
        words: Union[List[str], Callable[[], List[str]]],
        ignore_case: bool = False,
        display_dict: Optional[Mapping[str, AnyFormattedText]] = None,
        meta_dict: Optional[Mapping[str, AnyFormattedText]] = None,
        WORD: bool = False,
        sentence: bool = False,
        match_middle: bool = False,
        pattern: Optional[Pattern[str]] = None,
    ) -> None:
        super().__init__(words, ignore_case, display_dict, meta_dict, WORD, sentence, match_middle, pattern)

    def __str__(self):
        return ','.join(self.words)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        # Get list of words.
        words = self.words
        if callable(words):
            words = words()

        # Get word/text before cursor.
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(
                WORD=self.WORD, pattern=self.pattern
            )

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word: str) -> bool:
            """True when the word before the cursor matches."""
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return word_before_cursor in word
            else:
                return word.startswith(word_before_cursor)

        for a in words:
            if word_before_cursor in ['(', ',', '=', 'in', "',"]:
                display = self.display_dict.get(a, a)
                display_meta = self.meta_dict.get(a, "")
                yield Completion(
                    a,
                    0,
                    display=display,
                    display_meta=display_meta,
                )

            if word_matches(a):
                display = self.display_dict.get(a, a)
                display_meta = self.meta_dict.get(a, "")
                yield Completion(
                    a,
                    -len(word_before_cursor),
                    display=display,
                    display_meta=display_meta,
                )
