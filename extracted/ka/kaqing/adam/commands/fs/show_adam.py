import sys
import os

from adam.app_session import AppSession
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_tabulize import tabulize

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

from adam.utils_version import get_container_version, get_latest_version
from version import __version__
from adam.commands.command import Command
from adam.repl_state import ReplState

class ShowAdam(Command):
    COMMAND = 'show adam'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowAdam, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowAdam.COMMAND

    def run(self, cmd: str, state: ReplState):
        if not self.args(cmd):
            return super().run(cmd, state)

        with self.context() as (_, ctx):
            package = os.path.dirname(os.path.abspath(__file__))
            package = package.split('/adam/')[0] + '/adam'

            lines = [
                f'version\t{__version__}',
                f'source\t{package}',
            ]

            version = None
            exit_code = 0
            err = None

            if not KubeContext.in_cluster():
                version, exit_code, err = get_container_version(state, ctx)
                if version:
                    app_session = AppSession.create('c3', 'c3', state.namespace)
                    lines.extend(['',
                                'Kubernetes Cluster',
                                f'ops-pod version\t{version}',
                                f'ops-pod url\thttps://{app_session.host}/c3/c3/ops'])

            lines.extend(['',
                          'Docker Repositories',
                          f'latest\t{get_latest_version()}'])

            tabulize(lines, separator='\t', err=True, ctx=ctx)
            ctx.log()

            if not KubeContext.in_cluster() and not version:
                if err:
                    ctx.log2(err)
                elif exit_code:
                    ctx.log2(f'exit code: {exit_code}')
                else:
                    ctx.log2('Could not resolve pod version.')

            return state

    def completion(self, state: ReplState):
        return super().completion(state)

    def help(self, state: ReplState):
        return super().help(state, 'show kaqing version')