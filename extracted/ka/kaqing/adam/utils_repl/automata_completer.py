from typing import Generic, Iterable, TypeVar
from prompt_toolkit.completion import CompleteEvent, Completer, Completion, WordCompleter
from prompt_toolkit.document import Document

from adam.utils_repl.state_machine import StateMachine, State

__all__ = [
    "AutomataCompleter",
]

T = TypeVar('T')

class AutomataCompleter(Completer, Generic[T]):
    def __init__(self,
                 state_machine: StateMachine,
                 first_term: str = '',
                 debug = False):
        super().__init__()
        self.machine = state_machine
        self.first_term = first_term
        self.debug = debug

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        text = document.text_before_cursor.lstrip()
        state = ''
        if self.first_term:
            text = f'{self.first_term} {text}'

        completer: Completer = None
        state: State = self.machine.traverse_tokens(self.tokens(text), State(state))
        if self.debug:
            print('\n  =>', state.state if isinstance(state, State) else '')

        if state.state in self.machine.suggestions:
            if completer := self.suggestions_completer(state, self.machine.suggestions[state.state].strip(' ')):
                for c in completer.get_completions(document, complete_event):
                    yield c

    def tokens(self, text: str) -> list[T]:
        return text.split(' ')

    def suggestions_completer(self, _: State, suggestions: str) -> list[str]:
        if not suggestions:
            return None

        return WordCompleter(suggestions.split(','))