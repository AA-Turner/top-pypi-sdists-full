from typing import Callable
from prompt_toolkit.completion import WordCompleter

from adam.utils_repl.automata_completer import AutomataCompleter
from adam.utils_repl.state_machine import State, StateMachine

BASH_SPEC = [
    # <command> ::= <simple_command> | <pipeline> | <conditional_command>
    # <simple_command> ::= <word> <argument>* <redirection>*
    # <pipeline> ::= <command> '|' <command>
    # <conditional_command> ::= <command> '&&' <command> | <command> '||' <command>
    # <word> ::= <letter> <letter_or_digit>*
    # <argument> ::= <word>
    # <redirection> ::= '>' <filename> | '<' <filename>
    # <filename> ::= <word>
    # <letter> ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'
    # <digit> ::= '0' | '1' | ... | '9'
    # <letter_or_digit> ::= <letter> | <digit>

    '                                > word           > cmd                                ^ hosts',
    'cmd                             > word           > cmd                                ^ |,>,2>,<,&,&&,||',
    '-                               > pipe           > cmd_pipe',
    '-                               > _rdr0_         > cmd_rdr0',
    '-                               > _rdr1_         > cmd_rdr1',
    '-                               > _rdr2_         > cmd_rdr2',
    '-                               > &              > cmd_bg                             ^ |,>,2>,<,&,&&,||',
    '-                               > &&|_or_        > nocmd',
    'cmd_a                           > word           > cmd',
    'cmd_pipe                        > word           > cmd',
    'cmd_rdr0                        > word           > cmd_rdr0_f',
    'cmd_rdr1                        > word           > cmd_rdr1_f',
    'cmd_rdr2                        > word           > cmd_rdr2_f',
    'cmd_rdr1_f                      > pipe           > cmd_pipe                           ^ |,2>,<,&,&&,||',
    '-                               > _rdr2_         > cmd_rdr2',
    '-                               > _rdr0_         > cmd_rdr0',
    'cmd_rdr2_f                      > pipe           > cmd_pipe                           ^ |,<,&,&&,||',
    '-                               > _rdr0_         > cmd_rdr0',
    '-                               > &              > cmd_bg                             ^ |,>,2>,<,&,&&,||',
    '-                               > &&|_or_        > nocmd',
    'cmd_rdr0_f                      > pipe           > cmd_pipe                           ^ |,&,&&,||',
    '-                               > &              > cmd_bg                             ^ |,>,2>,<,&,&&,||',
    '-                               > &&|_or_        > cmd',
    'cmd_bg                          > &&|_or_        > nocmd                              ^ &&,||',
    'nocmd                           > word           > cmd',
]

BASH_KEYWORDS = [
    '&',
    '&&',
    '|',
    '||',
    '>',
    '2>',
    '>>',
    '<',
    'hosts'
]

class BashStateMachine(StateMachine[str]):
    def spec(self) -> str:
        return BASH_SPEC

    def keywords(self) -> list[str]:
        return BASH_KEYWORDS

class BashCompleter(AutomataCompleter[str]):
    def __init__(self,
                 hosts: Callable[[], list[str]],
                 debug = False):
        super().__init__(BashStateMachine(debug=debug), '', debug=debug)

        self.hosts = hosts
        self.debug = debug

    def suggestions_completer(self, state: State, suggestions: str) -> list[str]:
        if not suggestions:
            return None

        terms = []
        for suggestion in suggestions.split(','):
            terms.extend(self._terms(state, suggestion))

        return WordCompleter(terms)

    def _terms(self, _: State, word: str) -> list[str]:
        terms = []

        if word == 'hosts':
            terms.extend(self.hosts())
        else:
            terms.append(word)

        return terms