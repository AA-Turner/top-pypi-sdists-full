from adam.commands.command import Command
from adam.commands.postgres.postgres_databases import PostgresDatabases
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import ing

class UndeployPgAgent(Command):
    COMMAND = 'undeploy pg-agent'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(UndeployPgAgent, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return UndeployPgAgent.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with ing('Deleting pod'):
                PostgresDatabases.undeploy_pg_agent(Config().get('pg.agent.name', 'ops-pg-agent'), state.namespace)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'undeploy Postgres agent')