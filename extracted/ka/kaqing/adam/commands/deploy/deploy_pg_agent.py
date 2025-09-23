from adam.commands.command import Command
from adam.commands.postgres.postgres_session import PostgresSession
from adam.config import Config
from adam.repl_state import ReplState, RequiredState

class DeployPgAgent(Command):
    COMMAND = 'deploy pg-agent'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(DeployPgAgent, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return DeployPgAgent.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        PostgresSession.deploy_pg_agent(Config().get('pg.agent.name', 'ops-pg-agent'), state.namespace)

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, _: ReplState):
        return f'{DeployPgAgent.COMMAND}\t deploy Postgres agent'