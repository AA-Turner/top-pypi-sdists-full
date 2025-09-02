from adam.commands.command import Command
from adam.k8s_utils.cassandra_clusters import CassandraClusters
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.repl_state import BashSession, ReplState, RequiredState

class Bash(Command):
    COMMAND = 'bash'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Bash, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Bash.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, s0: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, s0)

        state, args = self.apply_state(args, s0)
        if not self.validate_state(state):
            return state

        if state.in_repl:
            r = self.exec_with_dir(s0, args)
            if not r:
                state.exit_bash()

                return 'inconsistent pwd'

            return r
        else:
            a = ' '.join(args)
            command = f'bash -c "{a}"'

            if state.pod:
                CassandraNodes.exec(state.pod, state.namespace, command, show_out=True)
            elif state.sts:
                CassandraClusters.exec(state.sts, state.namespace, command, action='bash', show_out=True)

            return state

    def exec_with_dir(self, state: ReplState, args: list[str]):
        session_just_created = False
        if not args:
            session_just_created = True
            session = BashSession(state.device)
            state.enter_bash(session)

        if state.bash_session:
            if args != ['pwd']:
                if args:
                    args.append('&&')
                args.extend(['pwd', '>', f'/tmp/.qing-{state.bash_session.session_id}'])

            if not session_just_created:
                if pwd := state.bash_session.pwd(state):
                    args = ['cd', pwd, '&&'] + args

        a = ' '.join(args)
        command = f'bash -c "{a}"'

        rs = []

        if state.pod:
            rs = [CassandraNodes.exec(state.pod, state.namespace, command, show_out=not session_just_created)]
        elif state.sts:
            rs = CassandraClusters.exec(state.sts, state.namespace, command, action='bash', show_out=not session_just_created)

        return rs

    def completion(self, state: ReplState):
        if state.pod or state.sts:
            return {Bash.COMMAND: None}

        return {}

    def help(self, _: ReplState):
        return f'{Bash.COMMAND} [bash-commands]\t run bash'