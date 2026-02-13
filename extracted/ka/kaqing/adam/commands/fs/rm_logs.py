from adam.commands.command import Command
from adam.commands.devices.devices import device
from adam.repl_state import ReplState
from adam.utils_concurrent import parallelize
from adam.directories import Directories
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
            with self.context() as (_, ctx):
                cmd = f'rm -rf {Directories.remote_log_dir()}/*'
                action = 'rm-logs'
                pods = device(state).pod_names(state)
                container = device(state).default_container(state)

                with parallelize(pods,
                                msg='d`Running|Ran ' + action + ' onto {size} pods') as exec:
                    for r in exec.map(lambda pod: Pods.exec(pod, container, state.namespace, cmd, ctx)):
                        ctx.log(r.command)
                        r.log(ctx)

                return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, f'remove all qing log files under {Directories.remote_log_dir()}')