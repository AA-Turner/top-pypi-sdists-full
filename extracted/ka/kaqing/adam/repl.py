import os
import click
from prompt_toolkit.key_binding import KeyBindings

from adam.cli_group import cli
from adam.commands.filters.debug_filter import DebugFilter
from adam.commands.filters.schedule_filter import ScheduleFilter
from adam.commands.filters.time_filter import TimeFilter
from adam.commands.command import Command
from adam.commands.command_helpers import ClusterCommandHelper
from adam.commands.devices.devices import device
from adam.config import Config
from adam.commands.audit.utils_audits import Audits, audit
from adam.utils_color import Color, colored_text
from adam.utils_job.job_scheduler import JobScheduler
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_log import Log, log2, log_timing
from adam.utils_repl.filtered_completer import FilteredCompleter
from adam.utils_repl.command_runner import cmd_list_n_chain, run_command
from adam.utils_repl.repl_completer import ReplCompleter
from adam.utils_repl.repl_session import ReplSession
from adam.utils_repl.repl_state import ReplState
from adam.utils_version import get_latest_version
from . import __version__

import nest_asyncio
nest_asyncio.apply()

import asyncio

def enter_repl(state: ReplState):
    if os.getenv('QING_DROPPED', 'false') == 'true':
        log2('You have dropped to bash from another qing instance. Please enter "exit" to go back to qing.')
        return

    session = ReplSession().prompt_session

    def prompt_msg():
        msg = state.__str__()

        return f"{msg}$ " if state.bash_session else f"{msg}> "

    Log.log2(f'kaqing {__version__}')

    # 2.1.37-CA4.1.9PG15
    latest_version = get_latest_version()
    if latest_version and (v := latest_version.split('-')[0]) != __version__:
        Log.log2('*')
        Log.log2(f'* Docker repository has newer version: {v}. Please update ops pod.')
        Log.log2('*')

    device(state).enter(state)

    kb = KeyBindings()

    @kb.add('c-c')
    def _(event):
        event.app.current_buffer.text = ''

    # inject run_command to JobScheduler
    JobScheduler.run_command = run_command

    with audit() as submit:
        # warm up AWS lambda - this log line may timeout and get lost, which is fine
        submit(Audits.log, 'entering kaqing repl', state.namespace, 'z', 0.0)

        # inject run_command to Commands, for example, Retry command needs it
        cmd_list, cmds = cmd_list_n_chain(run_command=run_command)

        cont = True
        while cont:
            def collect_cmd():
                return session.prompt(colored_text(prompt_msg(), Color.brightblue),
                                     completer=repl_completer(state, cmd_list),
                                     key_bindings=kb,
                                     bottom_toolbar=None)
            cont = run_command(state, collect_cmd, session=session, cmd_list=cmd_list, cmds=cmds, audit_submit=submit)

def repl_completer(state: ReplState, cmd_list: list[Command]):
    if state.bash_session:
        return ReplCompleter.from_nested_dict({})

    with log_timing('completion-calcs'):
        return FilteredCompleter(state, [DebugFilter(), ScheduleFilter(), TimeFilter()], cmd_list)

@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=ClusterCommandHelper, help="Enter interactive shell.")
@click.option('--kubeconfig', '-k', required=False, metavar='path', help='path to kubeconfig file')
@click.option('--config', default='params.yaml', metavar='path', help='path to kaqing parameters file')
@click.option('--param', '-v', multiple=True, metavar='<key>=<value>', help='parameter override')
@click.option('--cluster', '-c', required=False, metavar='statefulset', help='Kubernetes statefulset name')
@click.option('--namespace', '-n', required=False, metavar='namespace', help='Kubernetes namespace')
@click.argument('extra_args', nargs=-1, metavar='[cluster]', type=click.UNPROCESSED)
def repl(kubeconfig: str, config: str, param: list[str], cluster:str, namespace: str, extra_args):
    KubeContext.init_config(kubeconfig)
    if not KubeContext.init_params(config, param):
        return

    state = ReplState(ns_sts=cluster, namespace=namespace, in_repl=True)
    state, _ = state.apply_device_arg(extra_args)
    if not state.device:
        state.device=Config().get('repl.start-drive', 'a')

    enter_repl(state)