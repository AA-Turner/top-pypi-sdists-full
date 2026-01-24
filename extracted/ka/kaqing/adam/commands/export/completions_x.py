from adam.commands.export.export_databases import ExportDatabases
from adam.repl_state import ReplState
from adam.sql.lark_completer import LarkCompleter
from adam.utils_athena import Athena

def completions_x(state: ReplState):
    return LarkCompleter(expandables={
        'tables': lambda x: ExportDatabases.table_names(state.export_session),
        'export-databases': lambda x: ExportDatabases.database_names(),
        'columns': lambda x: Athena.column_names(database=state.export_session, function='export'),
    }, variant=ReplState.X).completions_for_nesting()