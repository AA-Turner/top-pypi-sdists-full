from adam.app_session import AppSession
from adam.commands.command import Command
from adam.k8s_utils.ingresses import Ingresses
from adam.k8s_utils.services import Services
from adam.repl_state import ReplState, RequiredState
from adam.utils import log2

class SetupFrontend(Command):
    COMMAND = 'setup frontend'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(SetupFrontend, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return SetupFrontend.COMMAND

    def required(self):
        return RequiredState.NAMESPACE

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        log2('This will support c3/c3 only for demo.')

        app_session: AppSession = AppSession.create('c3', 'c3', state.namespace)
        try:
            name = 'ops'
            port = 7678
            Services.create_service(name, state.namespace, port, {"run": "ops"})
            Ingresses.create_ingress(name, state.namespace, app_session.host, '/c3/c3/ops($|/)', port, annotations={
                'kubernetes.io/ingress.class': 'nginx',
                'nginx.ingress.kubernetes.io/use-regex': 'true',
                'nginx.ingress.kubernetes.io/rewrite-target': '/'
            })
        except Exception as e:
            if e.status == 409:
                log2(f"Error: '{name}' already exists in namespace '{state.namespace}'.")
            else:
                log2(f"Error creating ingress or service: {e}")

        return state

    def completion(self, _: ReplState):
        return {}

    def help(self, _: ReplState):
        return f'{SetupFrontend.COMMAND}\t sets up frontend'