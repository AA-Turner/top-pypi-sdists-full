from datetime import datetime, timedelta

from adam.config import Config
from adam.utils import log2, log_exc
from adam.utils_athena import Athena
from adam.utils_audits import Audits
from adam.utils_context import Context
from adam.utils_repl.automata_completer import AutomataCompleter
from adam.utils_repl.state_machine import StateMachine

def run_configured_query(config_key: str, args: list[str], ctx: Context = Context.NULL):
    limit, date_condition = extract_limit_and_duration(args)
    if query := Config().get(config_key, None):
        query = '\n    '.join(query.split('\n'))
        query = query.replace('{date_condition}', date_condition)
        query = query.replace('{limit}', str(limit))

        log2(query)
        log2()
        Athena.run_query(query, ctx=ctx)

def extract_limit_and_duration(args: list[str]) -> tuple[int, datetime]:
    limit = 10
    _from = datetime.now() - timedelta(days=30)
    if args:
        with log_exc():
            limit = int(args[0])

        if len(args) > 2 and args[1] == 'over':
            if args[2] == 'day':
                _from = datetime.now() - timedelta(days=1)

    return (limit, Audits.date_from(_from))

def limit_and_duration_completion():
    return {'10': {'over': {
        'day': None,
        'month': None
    }}}

SHOW_TOP10_SPEC = [
    '                                > show           > show',
    'show                            > last|slow|top  > show_top                            ^ last,slow,top',
    'show_top                        > word           > show_top_n                          ^ 10',
    'show_top_n                      > over           > show_top_n_over                     ^ over',
    'show_top_n_over                 > day|month      > show_top_n_over$                    ^ day,month',
]

SHOW_TOP10_KEYWORDS = [
    'show',
    'top',
    'last',
    'slow',
    'over',
    'day',
    'month'
]

class ShowTop10StateMachine(StateMachine[str]):
    def spec(self) -> str:
        return SHOW_TOP10_SPEC

    def keywords(self) -> list[str]:
        return SHOW_TOP10_KEYWORDS

def show_top10_completions_for_nesting():
    return {
        'show': {
            'last': AutomataCompleter(ShowTop10StateMachine(), first_term='show last'),
            'slow': AutomataCompleter(ShowTop10StateMachine(), first_term='show slow'),
            'top': AutomataCompleter(ShowTop10StateMachine(), first_term='show top'),
    }}