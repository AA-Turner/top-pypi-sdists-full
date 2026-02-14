import time
import click

from adam.commands import extract_options
from adam.commands.command import Command
from adam.commands.command_helpers import ClusterOrPodCommandHelper
from adam.commands.devices.devices import device
from adam.commands.nodetool.nodetool_commands import NODETOOL_COMMANDS
from adam.commands.nodetool.utils_nodetool import abort_nodetool_tasks, find_running_nodetool_tasks
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils_context import Context
from adam.utils_job.job import Job
from adam.utils_job.utils_job_results import find_failed_pods
from adam.utils_log import log
from adam.utils_cassandra.pod_service import cassandra
from adam.utils_tabulize import tabulize

class NodeTool(Command):
    COMMAND = 'nodetool'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(NodeTool, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return NodeTool.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                return self._run(args, state, ctx=ctx)

    def retry(self, cmd: str, job: Job, state: ReplState):
        if not(args := self.args(cmd)):
            return super().retry(cmd, job, state)

        with self.validate(args, state) as (args, state):
            with self.context(args, job_id=job.job_id) as (args, ctx):
                if not (pods := find_failed_pods(state, job, ctx=ctx.copy(show_out=False, background=False))):
                    ctx.copy(background=False).log2(f'No failures are reported for job: {job.job_id}.')

                    return state

                ctx.copy(background=False).log2(f'{len(pods)} nodetool compacts are being retried...')

                return self._run(args, state, pods=pods, ctx=ctx)

    def _run(self, args: list[str], state: ReplState, pods: list[str] = None, ctx: Context = None):
        with extract_options(args, '--force') as (args, forced):
            if not pods:
                pods = state.pod

            with cassandra(state, pod=pods) as pods:
                if subcommand := args[0]:
                    if subcommand in ['repair']:
                        ps = find_running_nodetool_tasks(subcommand, state)
                        if ps:
                            tabulize(ps,
                                        lambda p: '\t'.join(p),
                                        header='POD\tCMD\tID/PID\tLAST_ARG\tREAPER_RUN_STATE',
                                        separator='\t',
                                        ctx=ctx)
                            ctx.log2()

                            if forced:
                                ctx.log2(f"* Found running instances of 'nodetool {subcommand}', aborting existing ones...")
                                abort_nodetool_tasks(state, subcommand, ps)

                                wait_duration = Config().get('nodetool.grace-period-after-abort', 10)
                                ctx.log2(f"* Scheduling new 'nodetool {subcommand}' in {wait_duration} secs...")
                                time.sleep(wait_duration)
                            else:
                                ctx.log2(f"* Found running instances of 'nodetool {subcommand}', add --force to abort existing ones.")

                                return state

                pods.nodetool(' '.join(args), status=(args[0] == 'status'), ctx=ctx)

                return state

    def completion(self, state: ReplState):
        return super().completion(state, {c: {'--force': None, '&': None} for c in NODETOOL_COMMANDS}, pods=device(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'run nodetool with arguments', args='<sub-command>')

class NodeToolCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()
        log('Sub-Commands:')

        cmds = ''
        for c in NODETOOL_COMMANDS:
            if cmds:
                cmds += ', '
            cmds += c
            if len(cmds) > Config().get('nodetool.commands_in_line', 40):
                log('  ' + cmds)
                cmds = ''

        if len(cmds) > 0:
            log('  ' + cmds)
        log()
        ClusterOrPodCommandHelper.cluter_or_pod_help()