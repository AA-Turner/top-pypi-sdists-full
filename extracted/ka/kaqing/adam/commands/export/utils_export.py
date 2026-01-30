import io
import os
import re

from adam.config import Config
from adam.utils import ExecResult, creating_dir, log2, log_to_pods
from adam.repl_state import ReplState
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils_local import local_exec

class ImportSpec:
    def __init__(self, table_name: str, session: str = None, files: list[str] = None, importer: str = None):
        self.table_name = table_name
        self.session = session
        self.files = files
        self.importer = importer

    def parse_specs(specs_str: str, files = False):
        session_or_files: str = None
        importer: str = None
        table_name: str = None

        if specs_str:
            importer, rest = ImportSpec._extract_importer(specs_str.strip(' '))

            if rest:
                table_name, session_or_files = ImportSpec._extract_table_name(rest)

        if not files:
            return ImportSpec(table_name, session=session_or_files, importer=importer)

        return ImportSpec(table_name, files=[f.strip(' ') for f in session_or_files.split(',')], importer=importer)

    def _extract_importer(spec_str: str) -> tuple[str, str]:
        importer = None
        rest = spec_str

        p = re.compile(r"(.*?)to\s+(.*)", re.IGNORECASE)
        match = p.match(spec_str)
        if match:
            rest = match.group(1).strip(' ')
            importer = match.group(2).strip(' ')

        return importer, rest

    def _extract_table_name(spec_str: str) -> tuple[str, str]:
        table_name = None
        rest = spec_str

        p = re.compile(r"(.*?)as\s+(.*)", re.IGNORECASE)
        match = p.match(spec_str)
        if match:
            rest = match.group(1).strip(' ')
            table_name = match.group(2).strip(' ')

        return table_name, rest

class ExportSpec(ImportSpec):
    def __init__(self, keyspace: str, consistency: str, importer: str, tables: list['ExportTableSpec'], session: str = None, specs_str: str = None):
        super().__init__(None, importer)

        self.keyspace = keyspace
        self.consistency = consistency
        self.importer = importer
        self.tables = tables
        self.session = session
        self.specs_str = specs_str

    def __str__(self):
        return f'keyspace: {self.keyspace}, consistency: {self.consistency}, importer: {self.importer}, tables: {",".join([t.table for t in self.tables])}, session: {self.session}'

    def __eq__(self, other):
        if not isinstance(other, ExportSpec):
            return NotImplemented

        return self.keyspace == other.keyspace and self.tables == other.tables and self.consistency == other.consistency and self.importer == other.importer and self.session == other.session

    def parse_specs(specs_str: str):
        keyspace: str = None
        consistency: str = None
        importer: str = None
        specs: list[ExportTableSpec] = None

        if specs_str:
            importer, specs_str = ExportSpec._extract_importer(specs_str.strip(' '))
            keyspace, specs_str = ExportSpec._extract_keyspace(specs_str)
            consistency, specs = ExportSpec._extract_consisteny(specs_str)

        return ExportSpec(keyspace, consistency, importer, specs, specs_str=specs_str)

    def _extract_keyspace(spec_str: str) -> tuple[str, str]:
        keyspace = None
        rest = spec_str

        p = re.compile(r"\s*\*\s+in\s+(\S+)(.*)", re.IGNORECASE)
        match = p.match(spec_str)
        if match:
            keyspace = match.group(1).strip(' ')
            rest = match.group(2).strip(' ')
        elif spec_str.startswith('*'):
            keyspace = '*'
            rest = spec_str[1:].strip(' ')

        return keyspace, rest

    def _extract_consisteny(spec_str: str) -> tuple[str, list['ExportTableSpec']]:
        consistency = None

        p = re.compile(r"(.*?)with\s+consistency\s+(.*)", re.IGNORECASE)
        match = p.match(spec_str)
        if match:
            spec_str = match.group(1).strip(' ')
            consistency = match.group(2)

        if spec_str:
            p = r",\s*(?![^()]*\))"
            specs = re.split(p, spec_str)

            return consistency, [ExportTableSpec.parse(spec) for spec in specs]

        return consistency, None

class ExportTableSpec:
    def __init__(self, keyspace: str, table: str, columns: str = None, target_table: str = None):
        self.keyspace = keyspace
        self.table = table
        self.columns = columns
        self.target_table = target_table

    def __str__(self):
        return f'{self.keyspace}.{self.table}({self.columns}) AS {self.target_table}'

    def __eq__(self, other):
        if not isinstance(other, ExportTableSpec):
            return NotImplemented

        return self.keyspace == other.keyspace and self.table == other.table and self.columns == other.columns and self.target_table == other.target_table

    def from_status(status: 'ExportTableStatus'):
        return ExportTableSpec(status.keyspace, status.table, target_table=status.target_table)

    def parse(spec_str: str) -> 'ExportTableSpec':
        target = None

        p = re.compile(r"(.*?)\s+as\s+(.*)", re.IGNORECASE)
        match = p.match(spec_str)
        if match:
            spec_str = match.group(1)
            target = match.group(2)

        keyspace = None
        table = spec_str
        columns = None

        p = re.compile('(.*?)\.(.*?)\((.*)\)')
        match = p.match(spec_str)
        if match:
            keyspace = match.group(1)
            table = match.group(2)
            columns = match.group(3)
        else:
            p = re.compile('(.*?)\.(.*)')
            match = p.match(spec_str)
            if match:
                keyspace = match.group(1)
                table = match.group(2)

        return ExportTableSpec(keyspace, table, columns, target)

    def __eq__(self, other):
        if isinstance(other, ExportTableSpec):
            return self.keyspace == other.keyspace and self.table == other.table and self.columns == other.columns and self.target_table == other.target_table

        return False

    def __str__(self):
        return f'{self.keyspace}.{self.table}({self.columns}) as {self.target_table}'

class ExportTableStatus:
    def __init__(self, keyspace: str, target_table: str, status: str, table: str = None, csv_file: str = ''):
        self.keyspace = keyspace
        self.target_table = target_table
        self.status = status
        self.table = table
        self.csv_file = csv_file

    def __str__(self):
        return f'{self.keyspace}.{self.table} as {self.target_table} = {self.status}'

    def __eq__(self, other):
        if isinstance(other, ExportTableStatus):
            return self.keyspace == other.keyspace and self.table == other.table and self.status == other.status and self.target_table == other.target_table

        return False

    def from_session(sts: str, pod: str, namespace: str, export_session: str) -> tuple['ExportTableStatus', str]:
        statuses: list[ExportTableStatus] = []

        status_in_whole = 'done'
        log_files: list[str] = PodFiles.find_files(pod, 'cassandra', namespace, f'{table_log_dir(pod, namespace)}/{export_session}_*.log*', remote=log_to_pods())

        for log_file in log_files:
            status: ExportTableStatus = ExportTableStatus.from_log_file(pod, namespace, export_session, log_file)
            statuses.append(status)

            if status.status != 'done':
                status_in_whole = status.status

        return statuses, status_in_whole

    def from_log_file(pod: str, namespace: str, copy_session: str, log_file: str, ctx: Context = Context.NULL):
        def get_csv_files_n_table(target_table: str):
            db = f'{copy_session}_{target_table}'
            csv_file = f'{csv_dir()}/{db}/*.csv'
            csv_files: list[str] = PodFiles.find_files(pod, 'cassandra', namespace, csv_file, remote=log_to_pods())
            if csv_files:
                table = target_table
                m = re.match(f'{csv_dir()}/{db}/(.*).csv', csv_files[0])
                if m:
                    table = m.group(1)
                return csv_files, table

            return csv_files, target_table

        m = re.match(f'{table_log_dir(pod, namespace)}/{copy_session}_(.*?)\.(.*?)\.log(.*)', log_file)
        if m:
            keyspace = m.group(1)
            target_table = m.group(2)
            state = m.group(3)
            if state == '.pending_import':
                csv_files, table = get_csv_files_n_table(target_table)
                return ExportTableStatus(keyspace, target_table, 'pending_import', table, csv_files[0] if csv_files else '')
            elif state == '.done':
                return ExportTableStatus(keyspace, target_table, 'done', target_table)

            # 4 rows exported to 1 files in 0 day, 0 hour, 0 minute, and 1.335 seconds.
            pattern = 'rows exported to'
            if log_to_pods():
                r: ExecResult = Pods.exec(pod, 'cassandra', namespace, f"grep '{pattern}' {log_file}", ctx=ctx)
            else:
                r: ExecResult = local_exec(["grep", pattern, log_file], show_out=ctx.debug)

            if r.exit_code() == 0:
                csv_files, table = get_csv_files_n_table(target_table)
                if csv_files:
                    return ExportTableStatus(keyspace, target_table, 'exported', table, csv_files[0])
                else:
                    return ExportTableStatus(keyspace, target_table, 'imported', target_table)
            else:
                return ExportTableStatus(keyspace, target_table, 'export_in_pregress')

        return ExportTableStatus(None, None, 'unknown')

class GeneratorStream(io.RawIOBase):
    def __init__(self, generator):
        self._generator = generator
        self._buffer = b''  # Buffer to store leftover bytes from generator yields

    def readable(self):
        return True

    def _read_from_generator(self):
        try:
            chunk = next(self._generator)
            if isinstance(chunk, str):
                chunk = chunk.encode('utf-8')  # Encode if generator yields strings
            self._buffer += chunk
        except StopIteration:
            pass  # Generator exhausted

    def readinto(self, b):
        # Fill the buffer if necessary
        while len(self._buffer) < len(b):
            old_buffer_len = len(self._buffer)
            self._read_from_generator()
            if len(self._buffer) == old_buffer_len:  # Generator exhausted and buffer empty
                break

        bytes_to_read = min(len(b), len(self._buffer))
        b[:bytes_to_read] = self._buffer[:bytes_to_read]
        self._buffer = self._buffer[bytes_to_read:]
        return bytes_to_read

    def read(self, size=-1):
        if size == -1:  # Read all remaining data
            while True:
                old_buffer_len = len(self._buffer)
                self._read_from_generator()
                if len(self._buffer) == old_buffer_len:
                    break
            data = self._buffer
            self._buffer = b''
            return data
        else:
            # Ensure enough data in buffer
            while len(self._buffer) < size:
                old_buffer_len = len(self._buffer)
                self._read_from_generator()
                if len(self._buffer) == old_buffer_len:
                    break

            data = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return data

class PodPushHandler:
    def __init__(self, state: ReplState, pod: str = None):
        self.state = state
        self.pushed = False
        self.pod = pod

    def __enter__(self):
        state = self.state

        if not state.pod:
            self.pushed = True
            state.push()

            if not self.pod:
                self.pod = StatefulSets.pod_names(state.sts, state.namespace)[0]
            state.pod = self.pod

        return state

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pushed:
            self.state.pop()

        return False

def state_with_pod(state: ReplState, pod: str = None):
    return PodPushHandler(state, pod=pod)

def fs_exec(pod: str, namespace: str, cmd: str, ctx: Context = Context.NULL):
    if log_to_pods():
        CassandraNodes.exec(pod, namespace, cmd, ctx=ctx)
    else:
        os_system_exec(cmd, show_out=ctx.show_out)

def os_system_exec(cmd: str, show_out = False):
    if show_out:
        log2(cmd)

    os.system(cmd)

def csv_dir():
    return Config().get('export.csv_dir', '/c3/cassandra/tmp')

def table_log_dir(pod: str, namespace: str):
    if log_to_pods():
        return remote_export_log_dir(pod, namespace)
    else:
        return export_log_dir()

def export_log_dir():
    return creating_dir(Config().get('export.log-dir', '/tmp/qing-db/q/export/logs'))

def remote_export_log_dir(pod: str, namespace: str):
    return PodFiles.creating_dir(pod, 'cassandra', namespace, Config().get('export.remote.log-dir', '/tmp/q/export/logs'))