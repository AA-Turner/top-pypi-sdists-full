from enum import Enum
from typing import Callable

import sqlparse
from sqlparse.sql import Token

from adam.sql.term_completer import TermCompleter
from adam.utils_repl.automata_completer import AutomataCompleter
from adam.sql.sql_state_machine import AthenaStateMachine, CqlStateMachine, SqlStateMachine
from adam.utils_repl.state_machine import State

__all__ = [
    "SqlCompleter",
]

def default_columns(x: list[str]):
    return 'id,x.,y.,z.'.split(',')

class SqlVariant(Enum):
    SQL = 'sql'
    CQL = 'cql'
    ATHENA = 'athena'

class SqlCompleter(AutomataCompleter[Token]):
    def tokens(self, text: str) -> list[Token]:
        tokens = []

        stmts = sqlparse.parse(text)
        if stmts:
            for stmt in stmts:
                tokens.extend(stmt.tokens)

        return tokens

    def __init__(self,
                 tables: Callable[[], list[str]],
                 dml: str = None,
                 expandables: dict = {},
                 variant: SqlVariant = SqlVariant.SQL,
                 debug = False):
        machine = SqlStateMachine(debug=debug)
        if variant == SqlVariant.CQL:
            machine = CqlStateMachine(debug=debug)
        elif variant == SqlVariant.ATHENA:
            machine = AthenaStateMachine(debug=debug)
        super().__init__(machine, dml, debug)

        self.tables = tables
        if 'columns' not in expandables:
            expandables['columns'] = default_columns
        self.expandables = expandables
        self.variant = variant
        self.debug = debug

    def suggestions_completer(self, state: State, suggestions: str) -> list[str]:
        if not suggestions:
            return None

        terms = []
        for suggestion in suggestions.split(','):
            terms.extend(self._terms(state, suggestion))

        return TermCompleter(terms)

    def _terms(self, state: State, word: str) -> list[str]:
        terms = []

        if word.startswith('`') and word.endswith('`'):
            terms.append(word.strip('`'))
        elif word == 'tables':
            terms.extend(self.tables())
        elif word == 'columns':
            if 'last_name' in state.context and (n := state.context['last_name']):
                if 'last_namespace' in state.context and (ns := state.context['last_namespace']):
                    n = f'{ns}.{n}'
                terms.extend(self._call_expandable(word, [n]))
            else:
                terms.extend(self._call_expandable(word, []))
        elif word == 'partition-columns':
            terms.extend(self._call_expandable(word, []))
        elif word == 'table-props':
            terms.extend(self._call_expandable(word).keys())
        elif word == 'table-prop-values':
            if 'last_name' in state.context and state.context['last_name']:
                table_props = self._call_expandable('table-props')
                terms.extend(table_props[state.context['last_name']])
        elif word == 'single':
            terms.append("'")
        elif word == 'comma':
            terms.append(",")
        elif word in self.machine.expandable_names():
            terms.extend(self._call_expandable(word))
        else:
            terms.append(word)

        return terms

    def _call_expandable(self, name: str, *args):
        if name in self.expandables:
            c = self.expandables[name]
            if args:
                return c(args)
            else:
                return c()

        return []

    def completions_for_nesting(self, dml: str = None):
        if dml:
            return {dml: SqlCompleter(self.tables, dml, expandables=self.expandables, variant=self.variant)}

        return {
            word: SqlCompleter(self.tables, word, expandables=self.expandables, variant=self.variant)
            for word in self.machine.suggestions[''].strip(' ').split(',')
        }

    def __str__(self):
        return f'{self.variant}, {self.first_term}'