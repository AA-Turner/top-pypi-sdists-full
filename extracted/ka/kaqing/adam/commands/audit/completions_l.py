from adam.repl_state import ReplState
from adam.sql.lark_completer import LarkCompleter
from adam.utils_athena import Athena

def completions_l():
    return LarkCompleter(
        expandables={
            'tables': lambda x: Athena.table_names(),
            'columns': lambda table: Athena.column_names(),
            'partition-columns': lambda table: Athena.column_names(partition_cols_only=True),
            'topn-counts': lambda x: ['10'],
            'topn-types': lambda x: ['last', 'slow', 'top'],
            'topn-windows': lambda x: ['day', 'month'],
        }, variant=ReplState.L
    ).completions_for_nesting()