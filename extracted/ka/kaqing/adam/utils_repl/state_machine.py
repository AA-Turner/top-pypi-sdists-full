from abc import abstractmethod
from typing import Generic, TypeVar

from adam.utils import log_exc

__all__ = [
    'State',
    'StateMachine',
]

T = TypeVar('T')

class State:
    def __init__(self, state: str, comeback_token: str = None, comeback_state: str = None):
        self.state = state
        self.comeback_token = comeback_token
        self.comeback_state = comeback_state
        self.context: dict[str, str] = {}

    def __str__(self):
        return f'{self.state if self.state else None} comeback[{self.comeback_token} {self.comeback_state}]'

class StateMachine(Generic[T]):
    @abstractmethod
    def spec(self) -> str:
        return None

    @abstractmethod
    def keywords(self) -> list[str]:
        return None

    def expandable_names(self):
        return []

    def incomplete_name_transition_condition(self, from_s: str, token: str, to_s: str, suggestions: str) -> list[str]:
        if not suggestions:
            return None

        tokens = [token]
        if '|' in token:
            tokens = token.split('|')

        if 'name' not in tokens:
            return None

        return tokens

    def __init__(self, indent=0, push_level = 0, debug = False):
        self.states: dict[str, State] = {}
        self.suggestions: dict[str, str] = {}

        self.indent = indent
        self.push_level = push_level
        self.comebacks: dict[int, str] = {}
        self.debug = debug

        from_ss_to_add = []
        from_ss = ['']
        words: str = None
        for l in self.spec():
            t_and_w = l.split('^')
            if len(t_and_w) > 1:
                words = t_and_w[1].strip()
            else:
                words = None

            tks = t_and_w[0].strip(' ').split('>')
            if not l.startswith('-'):
                if words:
                    self.suggestions[tks[0].strip(' ')] = words

                if len(tks) == 1:
                    from_ss_to_add.append(tks[0].strip(' '))
                    continue

                from_ss = []
                from_ss.extend(from_ss_to_add)
                from_ss_to_add = []
                from_ss.append(tks[0].strip(' '))

            self.add_transitions(from_ss, tks, words)

    def add_transitions(self, from_ss: list[str], tks: list[str], words: str):
        token = tks[1].strip(' ')
        if len(tks) > 2:
            to_s = tks[2].strip(' ')
            for from_s in from_ss:
                self.add_whitespace_transition(from_s, to_s)
                self.add_transition(from_s, token, to_s)
                self.add_incomplete_name_transition(from_s, token, to_s, words)
        elif '<' in tks[0]:
            from_and_token = tks[0].split('<')
            if len(from_and_token) > 1:
                for from_s in from_ss:
                    self.add_comeback_transition(from_s, from_and_token[1], tks[1].strip(' '))

    def add_whitespace_transition(self, from_s: str, to_s: str):
        if self.witespace_transition_condition(from_s, to_s):
            if self.debug:
                print(f'{from_s[:-1]} > _ = {to_s}')
            self.states[f'{from_s[:-1]} > _'] = State(from_s)

    def witespace_transition_condition(self, from_s: str, to_s: str):
        return from_s.endswith('_')

    def add_incomplete_name_transition(self, from_s: str, token: str, to_s: str, words: str):
        if tokens := self.incomplete_name_transition_condition(from_s, token, to_s, words):
            self.suggestions[to_s] = words
            for token in tokens:
                if self.debug:
                    print(f'{to_s} > {token} = {to_s}')
                self.states[f'{to_s} > {token}'] = State(to_s)

    def add_transition(self, from_s: str, token: str, to_s: str):
        tokens = [token]
        if '|' in token:
            tokens = token.split('|')

        for t in tokens:
            if t == '_or_':
                t = '||'
            elif t == 'pipe':
                t = '|'
            elif t == '_rdr0_':
                t = '<'
            elif t == '_rdr1_':
                t = '>'
            elif t == '_rdr2_':
                t = '2>'

            if self.debug:
                print(f'{from_s} > {t} = {to_s}')
            self.states[f'{from_s} > {t}'] = State(to_s)

    def add_comeback_transition(self, from_s: str, token: str, to_s: str):
        key = f'{from_s} > ('
        orig = self.states[key]
        if not orig:
            raise Exception(f'from state not found for {key}')

        orig.comeback_token = token
        orig.comeback_state = to_s
        if self.debug:
            print(f'{from_s} > ) = {to_s}')
        self.states[key] = orig

    def traverse_tokens(self, tokens: list[str], state: State = State('')):
        for token in tokens[:-1]:
            if not token:
                continue

            if self.debug:
                print(f'{token} ', end='')

            last_name = None

            if (t := token.lower()) in self.keywords():
                token = t
            elif token in ['*', ',', '.']:
                pass
            else:
                last_name = token
                token = 'word'

            with log_exc():
                context = state.context
                state = self.states[f'{state.state} > {token}']
                state.context = context

                if last_name:
                    state.context['last_name'] = last_name

        return state