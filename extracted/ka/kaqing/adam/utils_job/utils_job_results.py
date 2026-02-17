import os
import re

from adam.commands.devices.devices import device
from adam.commands.export.export_sessions import export_session
from adam.utils_repl.repl_state import ReplState
from adam.utils import datetime_sec_precision
from adam.utils_color import Color
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_cassandra.node_restart_schedules import NodeRestartSchedules
from adam.utils_concurrent import parallelize
from adam.directories import Directories
from adam.utils_job.job_schedules import JobSchedules
from adam.utils_job.job_status import JobStatus
from adam.utils_job.utils_ps import LogLine, proc_for_pid
from adam.utils_k8s.k8s_context import K8sContext
from adam.utils_tabulize import tabulize
from adam.utils_context import NULL
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods, strip_pod_name
from adam.utils_log import PodLogFile, log2
from adam.utils_job.job import Job

def show_last_results(state: ReplState, args: str = None, ctx = NULL):
    job_id = args
    if job_id and isinstance(job_id, list):
        job_id = job_id[0]

    job: Job = Job.last_job(job_id)
    if not job:
        if job_id:
            log2(f'Last command with job_id: {job_id} was NOT found.')
        else:
            log2('Last command was NOT found.')

        return

    show_last_results_with_local_log(state, job, ctx)

    if job and (tokens := job.command.strip(' &').split(' ')):
        if tokens[0] in ['export']:
            return show_last_results_for_export(state, job, ctx=ctx)
        elif tokens[0] in ['show', 'xelect', 'audit', 'sp', 'ss', 'st', 'stp']:
            return
        elif tokens[0] in ['restart']:
            return show_last_results_for_node_schedules(state, job, ctx=ctx)

    # default to finding logs from pods
    show_last_results_with_pod_logs(state, job, ctx=ctx)

def show_last_results_with_local_log(state: ReplState, job: Job, ctx = NULL):
        ctx.log2(f'[{job.job_id}] {job.command}')
        show_local_log(job, ctx=ctx.copy(text_color=Color.gray))
        ctx.log2()

def show_last_results_with_pod_logs(state: ReplState, job: Job, ctx = NULL):
    container = device(state).default_container(state)

    with parallelize(device(state).pod_names(state),
                     msg='d`Running|Ran find-files onto {size} pods') as exec:
        results: list[LogLine] = exec.map(lambda pod: find_logs_for_pod(pod, container, state.namespace, Directories.remote_log_dir(), job, remote=True, ctx=ctx))

        tabulize(sorted([l for l in results if l.pod_name != '-'], key=lambda l: l.pod_name),
                 fn=lambda l: l.table_line(),
                 header=LogLine.header,
                 separator='\t',
                 ctx=ctx)

class PodJobStatus(JobStatus):
    def __init__(self, job_id: str, failed_pods: list[str], running: int, succeeded: int, job: Job = None):
        super().__init__()
        self._job_id = job_id
        self.failed_pods = failed_pods
        self._running = running
        self._succeeded = succeeded
        self._job = job

    def job_id(self) -> int:
        return self._job_id

    def is_running(self) -> int:
        return self._running

    def all_completed(self) -> bool:
        return not self.failed() and not self._running

    def succeeded(self) -> int:
        return self._succeeded

    def failed(self) -> int:
        return len(self.failed_pods)

    def running(self) -> int:
        return self._running

    def job(self) -> Job:
        return self._job

def find_job_status(state: ReplState, job: Job, ctx = NULL) -> PodJobStatus:
    pods = []
    running = 0
    succeeded = 0

    for pod, code in find_exit_codes(state, job, ctx):
        if code and code.isdigit():
            if int(code):
                pods.append(pod)
            else:
                succeeded += 1
        else:
            running += 1

    return PodJobStatus(job.job_id, pods, running, succeeded, job=job)

def find_exit_codes(state: ReplState, job: Job, ctx = NULL) -> list[tuple[str, str]]:
    container = device(state).default_container(state)

    with parallelize([state.pod] if state.pod else device(state).pod_names(state),
                     msg='d`Running|Ran find-files onto {size} pods') as exec:
        return exec.map(lambda pod: (pod, find_exit_code_for_pod(pod, container, state.namespace, Directories.remote_log_dir(), job.job_id, remote=True, ctx=ctx)))

def show_last_results_for_export(state: ReplState, job: Job, ctx = NULL):
    if 'session' not in job.extra:
        ctx.log2(f'[{job.job_id}] {job.command}')

        return

    with export_session(state) as sessions:
        session = job.extra['session']
        ctx.log2(f'show export session {session}', text_color='gray')
        sessions.show_session(session)

def show_last_results_for_node_schedules(state: ReplState, job: Job, ctx = NULL):
        lines = []

        waiting_ons: dict[tuple[str, str], str] = NodeRestartSchedules.waiting_ons()
        def wo(pod: tuple[str, str]):
            if pod in waiting_ons:
                return waiting_ons[pod]

            return '-'

        # TODO handle multiple namespaces
        status: CassandraStatus = CassandraStatus.snapshot(state, k8s=K8sContext.preload_pods(state.sts, state.namespace), ctx=ctx)

        pod_status = {Pods.pod_name(p): Pods.pod_status(p, '-') for p in status.pods}

        def node_status(pod_name):
            if pod_name in status.status_by_pod_name() and 'status' in status.status_by_pod_name()[pod_name]:
                return status.status_by_pod_name()[pod_name]['status']

            return '-'

        in_pending_or_restartings = set()

        for k, v in sorted(list(NodeRestartSchedules.restartings().items()), key=lambda kv: kv[0]):
            in_pending_or_restartings.add(k)
            lines.append(f'{strip_pod_name(k[0])}\t{k[1]}\tIn Restart\t{pod_status[k[0]]}\t{node_status(k[0])}\t{datetime_sec_precision(v)}\t-')
        for k, v in sorted(list(NodeRestartSchedules.pending().items()), key=lambda kv: kv[0]):
            in_pending_or_restartings.add(k)
            lines.append(f'{strip_pod_name(k[0])}\t{k[1]}\tPending\t{pod_status[k[0]]}\t{node_status(k[0])}\t{datetime_sec_precision(v)}\t{wo(k)}')

        restarted_lines = []
        for k, v in sorted(list(NodeRestartSchedules.completed().items()), key=lambda kv: kv[0]):
            if k not in in_pending_or_restartings:
                restarted_lines.append(f'{strip_pod_name(k[0])}\t{k[1]}\tRestarted\t{pod_status[k[0]]}\t{node_status(k[0])}\t{datetime_sec_precision(v)}\t-')

        tabulize(restarted_lines + lines,
                 header='POD\tNAMESPACE\tRESTART_STATUS\tPOD_STATUS\t\tSCHEDULED/COMPLETED\tWAITING_ON',
                 separator='\t',
                 ctx=ctx)
        ctx.log2()
        if any(d.startswith('DN: ') for d in waiting_ons.values()):
            ctx.log2('  *DN  node is down')
        if any(d.startswith('MC: ') for d in waiting_ons.values()):
            ctx.log2('  *MC  node has more than one copy of some token ranges; cannot be restarted until the copies are relocated to other nodes')
        if any(d.startswith('GP: ') for d in waiting_ons.values()):
            ctx.log2('  *GP  node is in grace period after restart')

def show_last_results_for_job_schedules(state: ReplState, job: Job, ctx = NULL):
        lines = []

        for k, v in sorted(list(JobSchedules._completed.items()), key=lambda kv: kv[0]):
            status: JobStatus = v
            lines.append(f'{status.job_id()}\tended\t{status.running()}\t{status.succeeded()}\t{status.failed()}\t{datetime_sec_precision(v)}')
        for k, v in sorted(list(JobSchedules.pending().items()), key=lambda kv: kv[0]):
            status: JobStatus = v
            lines.append(f'{status.job_id()}\trunning\t{status.running()}\t{status.succeeded()}\t{status.failed()}\t{datetime_sec_precision(v)}')

        tabulize(lines,
                 header='JOB_ID\tSTATUS\tRUNNING\tSUCCEEDED\tFAILED\tSCHEDULED/COMPLETED',
                 separator='\t',
                 ctx=ctx)
        ctx.log2()

def find_logs_for_pod(pod: str, container: str, namespace: str, dir: str, job: Job, remote: bool, ctx = NULL):
    ctx = ctx.copy(show_out=True, text_color=Color.gray)
    logs: list[PodLogFile] = PodFiles.find_files(pod, container, namespace, f'{dir}/{job.job_id}*', remote=remote, capture_pid=True, ctx=ctx)

    line = LogLine()

    for log in logs:
        l = str(log)
        if l.endswith('.log'):
            line.out = log.size
        elif l.endswith('.err'):
            line.err = log.size
        elif l.endswith('.pid'):
            if log.ts:
                line.exit_ts = log.ts
            if log.exit_code:
                line.exit_code = log.exit_code
            if log.pid:
                line.pid = log.pid
            continue

        line.pod_name = pod_suffix(log.pod)
        line.file = l.replace('.log', '.err')

    if line.pid and line.pid != '-':
        procs = proc_for_pid(pod, container, namespace, line.pid)

        for proc in procs:
            line.merge(proc)

    if not line.cmd or line.cmd == '-':
        command = job.command
        if command.endswith(' &'):
            command = command[:-2]

        tokens = command.split(' ')
        line.cmd = tokens[0]
        if line.cmd not in ['cqlsh']:
            line.last_arg = tokens[-1].strip('"')

    return line

def find_exit_code_for_pod(pod: str, container: str, namespace: str, dir: str, job_id: str, remote: bool, ctx = NULL):
    ctx = ctx.copy(show_out=True, text_color=Color.gray)
    logs: list[PodLogFile] = PodFiles.find_files(pod, container, namespace, f'{dir}/{job_id}*.pid', remote=remote, capture_pid=True, ctx=ctx)
    for log in logs:
        if log.exit_code:
            return log.exit_code

    return None

def pod_suffix(pod_name: str):
    if groups := re.match(r'.*-(.*-\d+)$', pod_name):
        pod_name = groups[1]
    else:
        pod_name = pod_name.split('-')[-1]

    return pod_name

def show_local_log(cmd: Job, ctx = NULL):
    ctx = ctx.copy(show_out=True)

    log_file = cmd._local_log_file()
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                ctx.log2(line.strip('\r\n'))