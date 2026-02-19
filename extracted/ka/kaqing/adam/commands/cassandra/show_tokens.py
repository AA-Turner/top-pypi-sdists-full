import re

from adam.commands.command import Command
from adam.commands.devices.device_cass import DeviceCass
from adam.utils_repl.repl_state import ReplState, RequiredState
from adam.utils_log import log_timing
from adam.utils_cassandra.cassandra_status import AddressTranslationError, CassandraStatus
from adam.utils_cassandra.node_restartability import NodeRestartability
from adam.presentation.tabulize import tabulize

class ShowTokens(Command):
    COMMAND = 'show tokens'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowTokens, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowTokens.COMMAND

    def required(self):
        return RequiredState.POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with self.context(args) as (args, ctx):
                with log_timing('show.tokens'):
                    status: CassandraStatus = None
                    ring: list[dict] = None
                    status, ring = NodeRestartability.tokens(state, ctx)
                    ip = status.ip_from_pod_name(state.pod)

                    def pod(ip: str):
                        s = '** '
                        if ip in status.status_by_ip() and 'status' in status.status_by_ip()[ip]:
                            s = '' if status.status_by_ip()[ip]['status'] == 'UN' else '* '

                        try:
                            pod = status.pod_name_from_ip(ip)
                            if groups := re.match(r'.*-(.*-\d+)$', pod):
                                pod = groups[1]

                            return f'{s}{pod}'
                        except AddressTranslationError:
                            if s:
                                return f'{s}{ip}'
                            else:
                                return f'*** {ip}'

                    lines : dict[str, set] = {}

                    def line(ip: str):
                        if ip not in lines:
                            lines[ip] = set()

                        return lines[ip]

                    token = None
                    s = 0
                    for n in ring[1:]:
                        if s == 0:
                            if n['address'] == ip:
                                token = n['token']

                                s = 1
                        elif s == 1:
                            line(token).add(pod(n['address']))

                            s = 2
                        elif s == 2:
                            line(token).add(pod(n['address']))

                            s = 0

                    tabulize(sorted(lines.keys()),
                                lambda k: f'{k}\t' + "\t".join(sorted(list(lines[k]))),
                                header='Token\tPods',
                                separator='\t',
                                ctx=ctx)

                    ctx.log()
                    ctx.log2('*   node is down')
                    ctx.log2('**  status cannot be located from ip address')
                    ctx.log2('*** pod name cannot be located from ip address')

                    return state

    def completion(self, state: ReplState):
        return super().completion(state, pods=DeviceCass().pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'show Cassandra tokens')