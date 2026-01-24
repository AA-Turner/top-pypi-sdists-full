from adam.commands.command import Command
from adam.utils_k8s.pods import Pods
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2
from adam.config import Config

class RepairScan(Command):
    COMMAND = 'repair scan'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RepairScan, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RepairScan.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            n = "7"
            if len(args) == 1:
                n = str(args[0])
            image = Config().get('repair.image', 'ci-registry.c3iot.io/cloudops/cassrepair:2.0.11')
            secret = Config().get('repair.secret', 'ciregistryc3iotio')
            log_path = secret = Config().get('repair.log-path', '/home/cassrepair/logs/')
            ns = state.namespace
            pvc_name ='cassrepair-log-' + state.sts
            pod_name = 'repair-scan'

            try:
                Pods.create(ns, pod_name, image, ["sh", "-c", "tail -f /dev/null"],
                        secret=secret,
                        env={},
                        volume_name='cassrepair-log',
                        pvc_name=pvc_name,
                        mount_path='/home/cassrepair/logs/')
            except Exception as e:
                if e.status == 409:
                    log2(f"Pod {pod_name} already exists")
                else:
                    log2("Exception when calling BatchV1Apii->create_namespaced_job: %s\n" % e)

            Pods.wait_for_running(ns, pod_name, 'Waiting for the scanner pod to start up...')

            try:
                Pods.exec(pod_name, pod_name, ns, f"find {log_path} -type f -mtime -{n} -print0 | xargs -0 grep failed")
            finally:
                Pods.delete(pod_name, ns)

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'scan last n days repair log, default 7 days')