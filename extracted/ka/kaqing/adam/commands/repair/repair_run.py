from adam.commands.command import Command
from adam.k8s_utils.jobs import Jobs
from adam.k8s_utils.volumes import Volumes
from adam.repl_state import ReplState, RequiredState
from adam.config import Config
from adam.commands.reaper.reaper_session import ReaperSession
from adam.commands.reaper.reaper_runs_abort import ReaperRunsAbort
from adam.commands.reaper.reaper_schedule_stop import ReaperScheduleStop
from adam.utils import log2

class RepairRun(Command):
    COMMAND = 'repair run'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RepairRun, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RepairRun.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        replace = False
        if len(args) == 1:
            replace = args[0] == 'replace'

        log2("Stopping all reaper schedules...")
        reaper = ReaperSession.create(state)
        schedules = reaper.schedule_ids(state)
        for schedule_id in schedules:
            ReaperScheduleStop().run(f'reaper stop schedule {schedule_id}', state)
        log2("Aborting all reaper runs...")
        state = ReaperRunsAbort().run('reaper abort runs', state)

        image = Config().get('repair.image', 'ci-registry.c3iot.io/cloudops/cassrepair:2.0.11')
        secret = Config().get('repair.secret', 'ciregistryc3iotio')
        log_path = Config().get('repair.log-path', '/home/cassrepair/logs/')
        user, _ = state.user_pass()
        ns = state.namespace
        env = Config().get('repair.env', {})
        env["cluster"] = ns
        env_from = {"username": user, "password": user}
        pvc_name ='cassrepair-log-' + state.sts
        Volumes.create_pvc(pvc_name, 30, ns)
        if replace:
            Jobs.delete('cassrepair-'+state.sts, ns)
        Jobs.create('cassrepair-'+state.sts, ns, image, secret, env, env_from, 'cassrepair', pvc_name, log_path)

        return state

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{RepairRun.COMMAND} [replace]\t start a repair job, default not replacing'
