from adam.commands import extract_options
from adam.commands.command import Command
from adam.config import Config
from adam.utils_k8s.deployment import Deployments
from adam.utils_k8s.pods import Pods
from adam.utils_log import ing
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.utils_tabulize import tabulize
from adam.utils_version import get_container_version, get_latest_version

class Upgrade(Command):
    COMMAND = 'upgrade'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(Upgrade, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return Upgrade.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_options(args, '--force') as (args, forced):
                with self.context(args) as (_, ctx):
                    version, exit_code, err = get_container_version(state, ctx)
                    if not version:
                        version = '-'

                    newer = get_latest_version()
                    if newer:
                        newer = newer.split('-')[0]
                    if not newer:
                        newer = '-'

                    ctx.log('Image Versions')
                    tabulize([f'Current\t{version}', f'New\t{newer}'], separator='\t', ctx=ctx)
                    ctx.log()

                    if version == '-':
                        ctx.log("Upgrade cannot work until you deploy the pod first with \n  'deploy pod'")
                        return state

                    if version == newer:
                        ctx.log('Ops pod is already with latest version.')
                        return state

                    if version.split('.')[0] != newer.split('.')[0]:
                        ctx.log("Upgrade cannot work as major version has been changed. Please re-deploy pod with \n  'deploy pod --force'.")
                        return state

                    if not forced:
                        ctx.log2('Please add --force.')
                        return state

                    label_selector = Config().get('pod.label-selector', 'run=ops')
                    with ing('Deleting pod'):
                        Pods.delete_with_selector(state.namespace, label_selector, grace_period_seconds=0)

                    version = 'latest'
                    if v := get_latest_version():
                        version = v
                    image = Config().get('pod.image', 'seanahnsf/kaqing-cloud:{version}').replace('{version}', version)
                    pod_name = Config().get('pod.name', 'ops')
                    with ing('Patching deployment'):
                        Deployments.update_image(state.namespace,
                                                 pod_name,
                                                 pod_name,
                                                 image,
                                                 ctx=ctx)

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, {'--force': None})

    def help(self, state: ReplState):
        return super().help(state, 'upgrade ops pod  --force needed for this command', args='[--force]')