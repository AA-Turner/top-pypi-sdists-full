import functools
import os
import re

from adam.commands.export.importer import Importer
from adam.commands.export.utils_export import ExportTableStatus, csv_dir, fs_exec, table_log_dir
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import log2, log_to_pods, tabulize, log, parallelize
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils_local import local_downloads_dir

class ExportSessions:
    def clear_export_session_cache():
        ExportSessions.find_export_sessions.cache_clear()
        ExportSessions.export_session_names.cache_clear()

    @functools.lru_cache()
    def export_session_names(sts: str, pod: str, namespace: str, importer: str = None, export_state = None):
        if not sts or not namespace:
            return []

        if not pod:
            pod = StatefulSets.pod_names(sts, namespace)[0]

        if not pod:
            return []

        return [session for session, state in ExportSessions.find_export_sessions(pod, namespace, importer).items() if not export_state or state == export_state]

    @functools.lru_cache()
    def find_export_sessions(pod: str, namespace: str, importer: str = None, limit = 100):
        sessions: dict[str, str] = {}

        prefix = Importer.prefix_from_importer(importer)

        log_files: list[str] = PodFiles.find_files(pod, 'cassandra', namespace, f'{table_log_dir(pod, namespace)}/{prefix}*_*.log*', remote=log_to_pods())

        if not log_files:
            return {}

        for log_file in log_files[:limit]:
            m = re.match(f'{table_log_dir(pod, namespace)}/([ces].*?)_.*\.log?(.*)', log_file)
            if m:
                s = m.group(1)
                state = m.group(2) # '', '.pending_import', '.done'
                if state:
                    state = state.strip('.')
                else:
                    state = 'in_export'

                if s not in sessions:
                    sessions[s] = state
                elif sessions[s] == 'done' and state != 'done':
                    sessions[s] = state

        return sessions

    def clean_up_all_sessions(sts: str, pod: str, namespace: str, ctx: Context = Context.NULL):
        if not sts or not namespace:
            return False

        if not pod:
            pod = StatefulSets.pod_names(sts, namespace)[0]

        CassandraNodes.exec(pod, namespace, f'rm -rf {csv_dir()}/*', ctx=ctx)
        cmd = f'rm -rf {table_log_dir(pod, namespace)}/*.log*'
        fs_exec(pod, namespace, cmd, ctx=ctx)

        return True

    def clean_up_sessions(sts: str, pod: str, namespace: str, sessions: list[str], max_workers = 0, ctx: Context = Context.NULL):
        if not sessions:
            return []

        if not max_workers:
            max_workers = Config().action_workers('export', 8)

        with parallelize(sessions,
                         max_workers,
                         msg='Cleaning|Cleaned up {size} export sessions') as exec:
            cnt_tuples = exec.map(lambda session: ExportSessions.clean_up_session(sts, pod, namespace, session, ctx=ctx.copy(show_out=False)))
            csv_cnt = 0
            log_cnt = 0
            for (csv, log) in cnt_tuples:
                csv_cnt += csv
                log_cnt += log

            return csv_cnt, log_cnt

    def clean_up_session(sts: str, pod: str, namespace: str, session: str, multi_tables = True, ctx: Context = Context.NULL):
        if not sts or not namespace:
            return 0, 0

        if not pod:
            pod = StatefulSets.pod_names(sts, namespace)[0]

        if not pod:
            return 0, 0

        csv_cnt = 0
        log_cnt = 0

        log_files: list[str] = PodFiles.find_files(pod, 'cassandra', namespace, f'{table_log_dir(pod, namespace)}/{session}_*.log*', remote=log_to_pods())

        for log_file in log_files:
            m = re.match(f'{table_log_dir(pod, namespace)}/{session}_(.*?)\.(.*?)\.log.*', log_file)
            if m:
                table = m.group(2)

                CassandraNodes.exec(pod, namespace, f'rm -rf {csv_dir()}/{session}_{table}', shell='bash', ctx=ctx)
                csv_cnt += 1

                cmd = f'rm -rf {log_file}'
                fs_exec(pod, namespace, cmd, ctx=ctx)
                log_cnt += 1

        return csv_cnt, log_cnt

    def show_session(sts: str, pod: str, namespace: str, session: str):
        if not pod:
            pod = StatefulSets.pod_names(sts, namespace)[0]

        if not pod:
            return

        tables, _ = ExportTableStatus.from_session(sts, pod, namespace, session)
        log()
        tabulize(tables,
                 lambda t: f'{t.keyspace}\t{t.target_table}\t{"export_completed_pending_import" if t.status == "pending_import" else t.status}\t{t.csv_file}',
                 header='KEYSPACE\tTARGET_TABLE\tSTATUS\tCSV_FILES',
                 separator='\t')

    def download_session(sts: str, pod: str, namespace: str, session: str):
        if not pod:
            pod = StatefulSets.pod_names(sts, namespace)[0]

        if not pod:
            return

        tables, _ = ExportTableStatus.from_session(sts, pod, namespace, session)
        def download_csv(table):
            from_path: str = table.csv_file

            to_path = from_path.replace(csv_dir(), local_downloads_dir())
            os.makedirs(os.path.dirname(to_path), exist_ok=True)
            PodFiles.download_file(pod, 'cassandra', namespace, from_path, to_path)

            log2(f'[{session}] Downloaded to {to_path}.')

        with parallelize(tables,
                         workers=Config().get('download.workers', 8),
                         msg='Downloading|Downloaded {size} csv files') as exec:
            exec.map(download_csv)

class ExportSessionService:
    def __init__(self, handler: 'ExportSessionHandler'):
        self.handler = handler

    def clean_up(self, sessions: list[str]):
        state = self.handler.state

        csv_cnt, log_cnt = ExportSessions.clean_up_sessions(state.sts, self.pod(), state.namespace, sessions)

        log(f'Removed {csv_cnt} csv and {log_cnt} log files.')

        ExportSessions.clear_export_session_cache()

    def clean_up_all(self, ctx: Context = Context.NULL):
        state = self.handler.state

        if ExportSessions.clean_up_all_sessions(state.sts, self.pod(), state.namespace, ctx=ctx):
            ExportSessions.clear_export_session_cache()

    def show_all_sessions(self):
        state = self.handler.state

        sessions = sorted(ExportSessions.find_export_sessions(self.pod(), state.namespace).items(), reverse=True)
        tabulize(sessions, lambda args: f'{args[0]}\t{args[1]}', header='EXPORT_SESSION\tSTATUS', separator='\t')

    def show_session(self, session: str):
        state = self.handler.state
        ExportSessions.show_session(state.sts, self.pod(), state.namespace, session)

    def download_session(self, session: str):
        state = self.handler.state
        ExportSessions.download_session(state.sts, self.pod(), state.namespace, session)

    def pod(self):
        state = self.handler.state

        pod = state.pod
        if not pod:
            pod = StatefulSets.pod_names(state.sts, state.namespace)[0]

        return pod

class ExportSessionHandler:
    def __init__(self, state: ReplState = None):
        self.state = state

    def __enter__(self):
        return ExportSessionService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def export_session(state: ReplState = None):
    return ExportSessionHandler(state)