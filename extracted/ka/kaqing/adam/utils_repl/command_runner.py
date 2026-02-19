import time
from typing import Callable, Union, cast

from adam.commands.command import Command, InvalidArgumentsException, InvalidStateException
from adam.commands.command_filter import CommandFilter
from adam.commands.devices.devices import device
from adam.commands.help import Help
from adam.config import Config
from adam.utils_job.job_status import JobStatus
from adam.utils_repl.repl_commands import ReplCommands
from adam.utils_repl.repl_session import ReplSession
from adam.utils_repl.repl_state import ReplState
from adam.sql.async_executor import AsyncExecutor
from adam.commands.audit.utils_audits import Audits, audit
from adam.utils_context import NULL, Context
from adam.thread_locals import thread_local_command
from adam.utils_job.job import Job
from adam.utils_log import CommandLog, clear_wait_log_flag, debug_trace, log2, log_exc, log_timing
from adam.presentation.tabulize import tabulize

import nest_asyncio
nest_asyncio.apply()

import asyncio

def run_command(state: ReplState,
                cmd: str,
                session: ReplSession = None,
                cmd_list: list[Command] = None,
                chain: Command = None,
                audit_submit: callable = None,
                job: Job = None,
                ctx: Context = None) -> Union[ReplState, JobStatus]:
    if not session:
        session = ReplSession().prompt_session

    if not cmd_list or not chain:
        cmd_list, chain = cmd_list_n_chain(run_command)

    AsyncExecutor.reset()

    finalizers = []
    s0 = time.time()
    result = None
    try:
        if cmd and callable(cmd):
            cmd = cmd()

        # store command as is including filters and pod-targetting
        thread_local_command().raw_command = cmd
        s0 = time.time()

        if state.bash_session:
            if cmd.strip(' ') == 'exit':
                state.exit_bash()
                return True

            cmd = f'bash {cmd}'
        else:
            finalizers, targetted_state, cmd = filtered(state, cmd)

        try:
            if cmd and cmd.strip(' ') and not (result := chain.retry(cmd, job, targetted_state, ctx=ctx) if job else chain.run(cmd, targetted_state)):
                result = try_device_default_action(targetted_state, chain, cmd_list, cmd, job=job)
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
                with log_exc():
                    finalizer(result)

        thread_local_command().raw_command = None

        # offload audit logging
        if cmd and (state.device != ReplState.L or Config().get('audit.log-audit-queries', False)):
            if audit_submit:
                audit_submit(Audits.log, cmd, state.namespace, state.device, time.time() - s0, get_audit_extra(result))
            else:
                with audit() as submit:
                    submit(Audits.log, cmd, state.namespace, state.device, time.time() - s0, get_audit_extra(result))

        CommandLog.close_log_file()

    if job:
        return result

    return result or state

def filtered(state: ReplState, cmd: str) -> tuple[list[Callable[[], None]], ReplState, str]:
    cmd_filters: list[CommandFilter] = ReplCommands.filters()

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

def cmd_list_n_chain(run_command: callable = None) -> tuple[list[Command], Command]:
    cmd_list: list[Command] = ReplCommands.repl_cmd_list() + [Help()]
    # head with the Chain of Responsibility pattern
    chain: Command = Command.chain(cmd_list, run_command=run_command)

    return cmd_list, chain

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