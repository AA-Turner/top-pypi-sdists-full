from datetime import datetime
import os

from adam.commands.devices.devices import device
from adam.commands.export.export_sessions import export_session
from adam.repl_state import ReplState
from adam.utils import Color, PodLogFile, log2, log_dir, log_to_pods, pod_log_dir
from adam.utils_job.utils_fs import LogLine, find_pids_for_pod, proc_for_pid
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils_tabulize import tabulize
from adam.utils_cassandra.node_scheduler import NodeScheduler
from adam.utils_context import Context
from adam.utils_k8s.pod_files import PodFiles
from adam.utils_k8s.pods import Pods, strip_pod_name
from adam.utils_local import find_local_files
from adam.utils_job.async_job import AsyncJobs, CommandInfo

def show_last_local_results(state: ReplState, ctx: Context = Context.NULL):
    last_id, last_command, last_extra = AsyncJobs.last_command()
    logs: list[str] = find_local_files(f'{log_dir()}/{last_id}*')

    # /tmp/qing-db/q/logs/16145959.repair-0.err
    # /tmp/qing-db/q/logs/16145959.repair-0.log

    logs_by_n: dict[str, LogLine] = {}
    for l in logs:
        size = str(os.path.getsize(l))
        n = l[len(f'{log_dir()}/{last_id}'):]
        if n.startswith('.'):
            n = n[1:]

        if n.endswith('.log'):
            n = n[:-4]
            key = 'out'
        else:
            n = n[:-4]
            key = 'err'

        n = n.split('-')[-1]

        if n not in logs_by_n:
            logs_by_n[n] = LogLine(n, file=l.replace('.log', '.err'))

        if key == 'out':
            logs_by_n[n].out = size
        else:
            logs_by_n[n].err = size

    if last_command:
        keywords = last_command.strip(' &').split(' ')
        if keywords and keywords[0] == 'nodetool':
            # nodetool -u cs-a7b13e29bd-superuser -pw lDed6uXQAQP72kHOYuML repair &
            keywords = keywords[-1:]

        for ps in find_pids_for_pod(state.pod, device(state).default_container(state), state.namespace, keywords, match_last_arg=True, ctx=ctx.copy(show_out=False)):
            n = ps.pod.split('-')[-1]
            if n in logs_by_n:
                logs_by_n[n].merge(ps)

    ctx.log2(f'[{last_id}] {last_command}')
    ctx.log2()
    tabulize(sorted(logs_by_n.keys()),
             fn=lambda n: logs_by_n[n].table_line(),
             header=LogLine.header,
             separator='\t',
             ctx=ctx)

def show_last_results(state: ReplState, args: str = None, ctx: Context = Context.NULL):
    job_id = args
    if job_id and isinstance(job_id, list):
        job_id = job_id[0]

    cmd: CommandInfo = AsyncJobs.last_command(job_id)

    if not cmd:
        if job_id:
            log2(f'Last command with job_id: {job_id} was NOT found.')
        else:
            log2('Last command was NOT found.')

        return

    if cmd and (tokens := cmd.command.strip(' &').split(' ')):
        if tokens[0] in ['export']:
            return show_last_results_for_export(state, cmd, ctx=ctx)
        elif tokens[0] in ['show', 'xelect', 'audit']:
            return show_last_results_with_local_log(state, cmd, ctx=ctx)
        elif tokens[0] == 'restart':
            return show_last_results_for_background_jobs(state, cmd, ctx=ctx)

    # default to finding logs from pods
    show_last_results_with_pod_logs(state, cmd, ctx=ctx)

def show_last_results_with_local_log(state: ReplState, cmd: CommandInfo, ctx: Context = Context.NULL):
        ctx.log2(f'[{cmd.job_id}] {cmd.command}')
        log_file = AsyncJobs.local_log_file(cmd.command, job_id = cmd.job_id)
        os.system(f'cat {log_file}')
        ctx.log2()

def show_last_results_with_pod_logs(state: ReplState, cmd: CommandInfo, ctx: Context = Context.NULL):
    container = device(state).default_container(state)

    action = 'find-files'
    msg = 'd`Running|Ran ' + action + ' onto {size} pods'
    pods = device(state).pod_names(state)
    with Pods.parallelize(pods, len(pods), msg=msg, action=action) as exec:
        results: list[LogLine] = exec.map(lambda pod: find_logs_for_pod(pod, container, state.namespace, pod_log_dir(), cmd, log_to_pods()))

        ctx.log2(f'[{cmd.job_id}] {cmd.command}')
        ctx.log2()
        tabulize(sorted([l for l in results if l.ordinal != '-'], key=lambda l: l.ordinal),
                 fn=lambda l: l.table_line(),
                 header=LogLine.header,
                 separator='\t',
                 ctx=ctx)

def show_last_results_for_export(state: ReplState, cmd: CommandInfo, ctx: Context = Context.NULL):
    if 'session' not in cmd.extra:
        ctx.log2(f'[{cmd.job_id}] {cmd.command}')

        return

    with export_session(state) as sessions:
        session = cmd.extra['session']
        ctx.log2(f'[job:{cmd.job_id}][export-session:{session}] {cmd.command}')
        ctx.log2()
        ctx.log2(f'show export session {session}', text_color='gray')
        sessions.show_session(session)

def show_last_results_for_background_jobs(state: ReplState, cmd: CommandInfo, ctx: Context = Context.NULL):
        ctx.log2(f'[{cmd.job_id}] {cmd.command}')
        log_file = AsyncJobs.local_log_file(cmd.command, job_id = cmd.job_id)
        os.system(f'cat {log_file}')
        ctx.log2()
        lines = []

        waiting_ons: dict[tuple[str, str], str] = NodeScheduler.waiting_ons()
        def wo(pod: tuple[str, str]):
            if pod in waiting_ons:
                return waiting_ons[pod]

            return '-'

        # TODO handle multiple namespaces
        status_by_pod_name = {p.metadata.name: Pods.pod_status(p, '-') for p in StatefulSets.pods(state.sts, state.namespace)}

        def status(pod_name):
            if pod_name in status_by_pod_name:
                return status_by_pod_name[pod_name]

            return '-'

        in_pending_or_restartings = set()

        for k, v in sorted(list(NodeScheduler.restartings().items()), key=lambda kv: kv[1]):
            in_pending_or_restartings.add(k)
            lines.append(f'{strip_pod_name(k[0])}\t{k[1]}\tIn Restart\t{status(k[0])}\t{datetime.fromtimestamp(v).replace(microsecond=0)}\t-')
        for k, v in sorted(list(NodeScheduler.pending().items()), key=lambda kv: kv[1]):
            in_pending_or_restartings.add(k)
            lines.append(f'{strip_pod_name(k[0])}\t{k[1]}\tPending\t{status(k[0])}\t{datetime.fromtimestamp(v).replace(microsecond=0)}\t{wo(k)}')

        restarted_lines = []
        for k, v in sorted(list(NodeScheduler.completed().items()), key=lambda kv: kv[1]):
            if k not in in_pending_or_restartings:
                restarted_lines.append(f'{strip_pod_name(k[0])}\t{k[1]}\tRestarted\t{status(k[0])}\t{datetime.fromtimestamp(v).replace(microsecond=0)}\t-')

        tabulize(restarted_lines + lines,
                 header='POD\tNAMESPACE\tRESTART_STATUS\tPOD_STATUS\tSCHEDULED/COMPLETED\tWAITING_ON',
                 separator='\t',
                 ctx=ctx)
        ctx.log2()
        if any(d.startswith('DN: ') for d in waiting_ons.values()):
            ctx.log2('  *DN  node is down')
        if any(d.startswith('MC: ') for d in waiting_ons.values()):
            ctx.log2('  *MC  node has more than one copy of some token ranges; cannot be restarted until the copies are relocated to other nodes')
        if any(d.startswith('GP: ') for d in waiting_ons.values()):
            ctx.log2('  *GP  node is in grace period after restart')

def find_logs_for_pod(pod: str, container: str, namespace: str, dir: str, cmd: CommandInfo, remote: bool, ctx: Context = Context.NULL):
    ctx = ctx.copy(show_out=True, text_color=Color.gray)
    logs: list[PodLogFile] = PodFiles.find_files(pod, container, namespace, f'{dir}/{cmd.job_id}*', remote=remote, capture_pid=True, ctx=ctx)

    line = LogLine()

    for log in logs:
        l = str(log)
        if l.endswith('.log'):
            line.out = log.size
        elif l.endswith('.err'):
            line.err = log.size
        elif l.endswith('.pid'):
            if log.exit_code:
                line.exit_code = log.exit_code
            if log.pid:
                line.pid = log.pid
            continue

        line.ordinal = log.pod.split('-')[-1]
        line.file = l.replace('.log', '.err')

    if line.pid and line.pid != '-':
        procs = proc_for_pid(pod, container, namespace, line.pid)

        for proc in procs:
            line.merge(proc)

    if not line.cmd or line.cmd == '-':
        command = cmd.command
        if command.endswith(' &'):
            command = command[:-2]

        tokens = command.split(' ')
        line.cmd = tokens[0]
        if line.cmd not in ['cqlsh']:
            line.last_arg = tokens[-1].strip('"')

    return line