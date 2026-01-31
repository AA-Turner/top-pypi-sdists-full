import os
import time
from typing import cast
import click
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import HTML

from adam.cli_group import cli
from adam.commands.command import Command, InvalidArgumentsException, InvalidStateException
from adam.commands.command_helpers import ClusterCommandHelper
from adam.commands.devices.devices import Devices
from adam.commands.help import Help
from adam.config import Config
from adam.sql.async_executor import AsyncExecutor
from adam.utils_audits import Audits
from adam.utils_context import Context
from adam.utils_k8s.kube_context import KubeContext
from adam.log import Log
from adam.repl_commands import ReplCommands
from adam.repl_session import ReplSession
from adam.repl_state import ReplState
from adam.utils import CommandLog, clear_wait_log_flag, debug_trace, deep_sort_dict, log2, log_exc, log_timing
from adam.utils_tabulize import tabulize
from adam.apps import Apps
from adam.utils_repl.repl_completer import ReplCompleter, merge_completions
from . import __version__

import nest_asyncio
nest_asyncio.apply()

import asyncio

def enter_repl(state: ReplState):
    if os.getenv('QING_DROPPED', 'false') == 'true':
        log2('You have dropped to bash from another qing instance. Please enter "exit" to go back to qing.')
        return

    cmd_list: list[Command] = ReplCommands.repl_cmd_list() + [Help()]
    # head with the Chain of Responsibility pattern
    cmds: Command = Command.chain(cmd_list)
    session = ReplSession().prompt_session

    def prompt_msg():
        msg = state.__str__()

        return f"{msg}$ " if state.bash_session else f"{msg}> "

    Log.log2(f'kaqing {__version__}')

    Devices.of(state).enter(state)

    kb = KeyBindings()

    @kb.add('c-c')
    def _(event):
        event.app.current_buffer.text = ''

    with Audits.offload() as exec:
        # warm up AWS lambda - this log line may timeout and get lost, which is fine
        exec.submit(Audits.log, 'entering kaqing repl', state.namespace, 'z', 0.0)

        s0 = time.time()

        # use sorted command list only for auto-completion
        sorted_cmds = sorted(cmd_list, key=lambda cmd: cmd.command())
        while True:
            AsyncExecutor.reset()

            cmd: str = None
            result = None
            try:
                completer = ReplCompleter.from_nested_dict({})
                if not state.bash_session:
                    with log_timing('completion-calcs'):
                        completions = {}
                        # app commands are available only on a: drive
                        if state.device == ReplState.A and state.app_app:
                            completions = log_timing('actions', lambda: Apps(path='apps.yaml').commands())

                        for c in sorted_cmds:
                            with log_exc(f'* {c.command()} command returned None completions.'):
                                completions = log_timing(c.command(), lambda: deep_sort_dict(merge_completions(completions, c.completion(state))))

                        # print(json.dumps(completions, indent=4))
                        completer = ReplCompleter.from_nested_dict(completions)

                cmd = session.prompt(HTML(f'<ansibrightblue>{prompt_msg()}</ansibrightblue>'), completer=completer, key_bindings=kb)
                s0 = time.time()

                if state.bash_session:
                    if cmd.strip(' ') == 'exit':
                        state.exit_bash()
                        continue

                    cmd = f'bash {cmd}'

                def targetted(state: ReplState, cmd: str):
                    if not (cmd.startswith('@') and len(arry := cmd.split(' ')) > 1):
                        return state, cmd

                    if state.device == ReplState.A and state.app_app or state.device == ReplState.P:
                        state.push(pod_targetted=True)

                        state.app_pod = arry[0].strip('@')
                        cmd = ' '.join(arry[1:])
                    elif state.device == ReplState.P:
                        state.push(pod_targetted=True)

                        state.app_pod = arry[0].strip('@')
                        cmd = ' '.join(arry[1:])
                    elif state.sts:
                        state.push(pod_targetted=True)

                        state.pod = arry[0].strip('@')
                        cmd = ' '.join(arry[1:])

                    return (state, cmd)

                target, cmd = targetted(state, cmd)
                try:
                    if cmd and cmd.strip(' ') and not (result := cmds.run(cmd, target)):
                        result = try_device_default_action(target, cmds, cmd_list, cmd)
                except InvalidStateException:
                    pass
                except InvalidArgumentsException:
                    pass

                if result and type(result) is ReplState and (s := cast(ReplState, result).export_session) != state.export_session:
                    state.export_session = s

            except EOFError:  # Handle Ctrl+D (EOF) for graceful exit
                break
            except Exception as e:
                if Config().get('debugs.exit-on-error', False):
                    raise e
                else:
                    log2(e)
                    debug_trace()
            finally:
                if not state.bash_session:
                    state.pop()

                clear_wait_log_flag()
                if cmd:
                    log_timing(f'command {cmd}', s0=s0)

                # offload audit logging
                if cmd and (state.device != ReplState.L or Config().get('audit.log-audit-queries', False)):
                    exec.submit(Audits.log, cmd, state.namespace, state.device, time.time() - s0, get_audit_extra(result))

                CommandLog.close_log_file()

def try_device_default_action(state: ReplState, cmds: Command, cmd_list: list[Command], cmd: str, ctx: Context = Context.NULL):
    action_taken, result = Devices.of(state).try_fallback_action(cmds, state, cmd)

    if not action_taken:
        ctx=ctx.copy(show_out=True)
        ctx.log2(f'* Invalid command: {cmd}')
        ctx.log2()
        tabulize([c.help(state) for c in cmd_list if c.help(state)],
                 separator='\t',
                 err=True,
                 ctx=ctx)

    return result

def get_audit_extra(result: any):
    if not result:
        return None

    if type(result) is list:
        extras = set()

        for r in result:
            if hasattr(r, '__audit_extra__') and (x := r.__audit_extra__()):
                extras.add(x)

        return ','.join(list(extras))

    if hasattr(result, '__audit_extra__') and (x := result.__audit_extra__()):
        return x

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