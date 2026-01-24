from adam.commands.command import Command
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_athena import Athena
from adam.utils_audits import AuditMeta, Audits

class AuditRun(Command):
    COMMAND = 'audit run'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(AuditRun, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)
        self.auto_repaired = False

    def command(self):
        return AuditRun.COMMAND

    def required(self):
        return ReplState.L

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            meta: AuditMeta = Audits.get_meta()
            clusters = Audits.find_new_clusters(meta.cluster_last_checked)
            Audits.put_meta(Audits.ADD_CLUSTERS, meta, clusters=clusters)
            if clusters:
                log2(f'Added {len(clusters)} new clusters.')
                tables = Config().get('audit.athena.repair-cluster-tables', 'cluster').split(',')
                with Audits.offload() as exec:
                    for table in tables:
                        exec.submit(Athena.query, f'MSCK REPAIR TABLE {table}', None,)
            else:
                log2(f'No new clusters were found.')

            return state

    def completion(self, state: ReplState):
        return {}

    def help(self, state: ReplState):
        return super().help(state, 'run audit')