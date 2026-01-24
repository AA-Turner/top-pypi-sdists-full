from adam.commands.cql.utils_cql import cassandra_keyspaces, cassandra_table_names
from adam.commands.export.export_sessions import ExportSessions
from adam.commands.export.export_databases import ExportDatabases
from adam.config import Config
from adam.repl_state import ReplState
from adam.sql.lark_completer import LarkCompleter
from adam.utils import log_timing
from adam.utils_k8s.statefulsets import StatefulSets

def completions_c(state: ReplState) -> dict[str, any]:
    ps = Config().get('cql.alter-tables.gc-grace-periods', '3600,86400,864000,7776000').split(',')

    with log_timing('lark.completions'):
        return LarkCompleter(
            expandables = {
                'tables': lambda x: cassandra_table_names(state),
                'keyspaces': lambda x: cassandra_keyspaces(state.with_no_pod()),
                'table-props': {
                    'GC_GRACE_SECONDS': ps
                },
                'table-props-value': lambda x: {None: None, 'GC_GRACE_SECONDS': ps}[x],
                'export-database-types': ['athena', 'sqlite', 'csv'],
                'export-databases': lambda x: ExportDatabases.database_names(),
                'export-sessions': lambda x: ExportSessions.export_session_names(state.sts, state.pod, state.namespace),
                'export-sessions-incomplete': lambda x: ExportSessions.export_session_names(state.sts, state.pod, state.namespace, export_state='pending_import'),
                'hosts': lambda x: [f'@{p}' for p in StatefulSets.pod_names(state.sts, state.namespace)],
            },
            variant=ReplState.C
        ).completions_for_nesting()