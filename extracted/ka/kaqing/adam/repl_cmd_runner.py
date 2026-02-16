import time
import traceback
from typing import Callable, cast

from adam.commands.command import Command, InvalidArgumentsException, InvalidStateException
from adam.commands.command_filter import CommandFilter
from adam.commands.devices.devices import device
from adam.commands.help import Help
from adam.config import Config
from adam.repl_commands import ReplCommands
from adam.repl_session import ReplSession
from adam.repl_state import ReplState
from adam.sql.async_executor import AsyncExecutor
from adam.utils_audits import Audits, audit
from adam.utils_context import NULL, Context
from adam.utils_global import thread_local
from adam.utils_job.job import Job
from adam.utils_log import CommandLog, clear_wait_log_flag, debug_trace, log2, log_timing
from adam.utils_tabulize import tabulize
from . import __version__

import nest_asyncio
nest_asyncio.apply()

import asyncio

def run_command(state: ReplState,
                cmd: str,
                session: ReplSession = None,
                cmd_list: list[Command] = None,
                cmds: Command = None,
                audit_submit: callable = None,
                job: Job = None,
                ctx: Context = None):
    if not session:
        session = ReplSession().prompt_session

    if not cmd_list or not cmds:
        cmd_list, cmds = cmd_list_n_chain(run_command)

    AsyncExecutor.reset()

    finalizers = []
    s0 = time.time()
    result = None
    try:
        if cmd and callable(cmd):
            cmd = cmd()

        # store command as is including filters and pod-targetting
        thread_local.cmd = cmd

        if state.bash_session:
            if cmd.strip(' ') == 'exit':
                state.exit_bash()
                return True

            cmd = f'bash {cmd}'
        else:
            finalizers, targetted_state, cmd = filtered(state, cmd)
            # targetted_state, cmd = targetted(state, cmd)

        try:
            if cmd and cmd.strip(' ') and not (result := cmds.retry(cmd, job, targetted_state, ctx=ctx) if job else cmds.run(cmd, targetted_state)):
                result = try_device_default_action(targetted_state, cmds, cmd_list, cmd, job=job)
        except InvalidStateException:
            pass
        except InvalidArgumentsException:
            pass

        if result and type(result) is ReplState and (s := cast(ReplState, result).export_session) != state.export_session:
            state.export_session = s
    except EOFError:  # Handle Ctrl+D (EOF) for graceful exit
        return False
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

        if finalizers:
            for finalizer in finalizers:
                try:
                    finalizer(result)
                except:
                    # if Config().is_debug():
                        traceback.print_exc()

        if hasattr(thread_local, 'cmd'):
            thread_local.cmd = None

        # offload audit logging
        if cmd and (state.device != ReplState.L or Config().get('audit.log-audit-queries', False)):
            if audit_submit:
                audit_submit(Audits.log, cmd, state.namespace, state.device, time.time() - s0, get_audit_extra(result))
            else:
                with audit() as submit:
                    submit(Audits.log, cmd, state.namespace, state.device, time.time() - s0, get_audit_extra(result))

        CommandLog.close_log_file()

    return result or state

def filtered(state: ReplState, cmd: str) -> tuple[list[Callable[[], None]], ReplState, str]:
    cmd_filters: list[CommandFilter] = ReplCommands.filters()
    # TODO SEAN optimize this
    for f in cmd_filters:
        f.run_command = run_command

    if not cmd_filters:
        return [], cmd

    final_calls = []

    filter_processed = True
    while filter_processed:
        filter_processed = False
        for filter in cmd_filters:
            fn, state, cmd = filter.process(state, cmd)
            if fn:
                final_calls.append(fn)
                filter_processed = True

    return final_calls, state, cmd

def process_config_filter(state: ReplState, cmd: str, word: str, key: str, value = True, default = False) -> tuple[Callable[[], None], str]:
    if (pre := f'{word} ') and cmd.startswith(pre):
        cmd = cmd[len(pre):]
        final_value = Config().get(key, default=default)

        Config().set(key, value)

        return lambda: Config().set(key, final_value), cmd

    return None, cmd

# def targetted(state: ReplState, cmd: str):
#     if not (cmd.startswith('@') and len(arry := cmd.split(' ')) > 1):
#         return state, cmd

#     if state.device == ReplState.A and state.app_app or state.device == ReplState.P:
#         state.push(pod_targetted=True)

#         state.app_pod = arry[0].strip('@')
#         cmd = ' '.join(arry[1:])
#     elif state.device == ReplState.P:
#         state.push(pod_targetted=True)

#         state.app_pod = arry[0].strip('@')
#         cmd = ' '.join(arry[1:])
#     elif state.sts:
#         state.push(pod_targetted=True)

#         state.pod = arry[0].strip('@')
#         cmd = ' '.join(arry[1:])

#     return (state, cmd)

def cmd_list_n_chain(run_command: callable = None) -> tuple[list[Command], Command]:
    cmd_list: list[Command] = ReplCommands.repl_cmd_list() + [Help()]
    # head with the Chain of Responsibility pattern
    cmds: Command = Command.chain(cmd_list, run_command=run_command)

    return cmd_list, cmds

def try_device_default_action(state: ReplState, cmds: Command, cmd_list: list[Command], cmd: str, job: Job = None, ctx = NULL):
    action_taken, result = device(state).try_fallback_action(cmds, state, cmd, job=job, ctx=ctx)

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