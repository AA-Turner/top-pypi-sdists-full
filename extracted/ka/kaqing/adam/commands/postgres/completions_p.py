from adam.commands.postgres.postgres_databases import PostgresDatabases
from adam.commands.postgres.utils_postgres import pg_table_names
from adam.repl_state import ReplState
from adam.sql.lark_completer import LarkCompleter

def completions_p(state: ReplState):
    return {
        '\h': None,
        '\d': None,
        '\dt': None,
        '\du': None
    } | LarkCompleter(expandables={
        'tables': lambda x: pg_table_names(state),
        'columns': ['id'],
        'hosts': ['@' + PostgresDatabases.pod_and_container(state.namespace)[0]],
    }, variant=ReplState.P).completions_for_nesting()

def psql0_completions(state: ReplState):
    return {
        '\h': None,
        '\l': None,
    }