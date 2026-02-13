from adam.commands import extract_options, validate_args
from adam.commands.command import Command
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.utils_cassandra.node_scheduler import NodeScheduler
from adam.utils_cassandra.node_schedules import NodeSchedules
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils_color import Color
from adam.utils_repl.set_completer import SetCompleter

class RestartNodes(Command):
    COMMAND = 'restart cassandra nodes'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RestartNodes, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RestartNodes.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def backgrounable(self):
        return True

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state, apply=False) as (args, state):
            with self.context(args) as (args, ctx):
                with extract_options(args, '--force') as (args, forced):
                    with validate_args(args, state, name='pod name'):
                        # restart nodes allows comma separator
                        args = self.comma_separated_args(args)

                        if ctx.background:
                            # start with foreground, it becomes background if the node scheduler is not yet runnig during scheduling
                            for pod in args:
                                NodeScheduler.schedule(state, pod, ctx.copy(background=False))
                        else:
                            if not forced:
                                for pod in args:
                                    ctx.log(f'[{pod}] Checking...')
                                    node: NodeRestartability = NodeRestartability.probe(state,
                                                                                        pod,
                                                                                        in_restartings=NodeSchedules.restartings(ctx=ctx),
                                                                                        ctx=ctx.copy(show_out=False))
                                    if not node.restartable():
                                        node.log(ctx=ctx.copy(text_color=Color.gray))
                                        ctx.log2('Please add --force for restarting pod unsafely.')

                                        return 'force-needed'

                            for pod in args:
                                ctx.log(f'[{pod}] Restarting...')
                                Pods.delete(pod, state.namespace)
                                ctx.log(f'[{pod}] OK')

                        return state

    def completion(self, state: ReplState):
        # TODO auto append {&: None} to SetCompleter
        return super().completion(state, lambda: SetCompleter(StatefulSets.pod_names(state.sts, state.namespace), options={'--force': {'&': None}, '&': None}))

    def help(self, state: ReplState):
        return super().help(state, 'restart Cassandra nodes  --force ignore node dependency', args='<pod-name>,... [--force]')