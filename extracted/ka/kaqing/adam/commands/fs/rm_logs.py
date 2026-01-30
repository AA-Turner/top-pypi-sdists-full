import os

from adam.commands.command import Command
from adam.commands.devices.devices import Devices
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import Color, log2, log_dir, pod_log_dir
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods

class RmLogs(Command):
    COMMAND = 'rm logs'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RmLogs, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RmLogs.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            cmd = f'rm -rf {pod_log_dir()}/*'
            action = 'rm-logs'
            msg = 'd`Running|Ran ' + action + ' onto {size} pods'
            pods = Devices.of(state).pod_names(state)
            container = Devices.of(state).default_container(state)
            with Pods.parallelize(pods, len(pods), msg=msg, action=action) as exec:
                ctx: Context = Context.new(show_out=True)

                for r in exec.map(lambda pod: Pods.exec(pod, container, state.namespace, cmd, ctx)):
                    ctx.log(r.command)
                    r.log(ctx)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, f'remove all qing log files under {pod_log_dir()}')