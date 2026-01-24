import datetime
from kubernetes import client
from kubernetes.client.rest import ApiException

from adam.commands import extract_options
from adam.commands.cassandra.watch import Watch
from adam.commands.command import Command
from adam.utils_k8s.statefulsets import StatefulSets
from adam.config import Config
from adam.repl_state import ReplState, RequiredState
from adam.utils import duration, log2

class RollOut(Command):
    COMMAND = 'rollout'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(RollOut, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return RollOut.COMMAND

    def required(self):
        return RequiredState.CLUSTER

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--force') as (args, forced):
                restarted, rollingout = StatefulSets.restarted_at(state.sts, state.namespace)
                if rollingout and not forced:
                    log2(f"* Cluster is being rolled out for {duration(restarted)}. Please wait until it's done or use --force.")

                    return state

                self.rolling_restart(state.sts, state.namespace)

                auto_watch = False
                if (auto_watch_cmds := Config().get('watch.auto', 'rollout')):
                    cmds = [c.strip(' ') for c in auto_watch_cmds.split(',')]
                    if self.command() in cmds:
                        auto_watch = True
                        log2('Rolling out cluster with auto watch...')
                        Watch().run('watch', state)

                if not auto_watch:
                    log2('Rolling out cluster...')

                return state

    def rolling_restart(self, statefulset, namespace):
        # kubectl rollout restart statefulset <statefulset-name>
        v1_apps = client.AppsV1Api()

        now = datetime.datetime.now(datetime.timezone.utc)
        now = str(now.isoformat("T") + "Z")
        body = {
            'spec': {
                'template':{
                    'metadata': {
                        'annotations': {
                            'kubectl.kubernetes.io/restartedAt': now
                        }
                    }
                }
            }
        }

        try:
            v1_apps.patch_namespaced_stateful_set(statefulset, namespace, body, pretty='true')
        except ApiException as e:
            log2("Exception when calling AppsV1Api->read_namespaced_statefulset_status: %s\n" % e)

    def completion(self, state: ReplState):
        if super().completion(state):
            return {RollOut.COMMAND: None}

        return {}

    def help(self, state: ReplState):
        return super().help(state, 'rollout all nodes  --force ignore current rolling out', args='[--force]')