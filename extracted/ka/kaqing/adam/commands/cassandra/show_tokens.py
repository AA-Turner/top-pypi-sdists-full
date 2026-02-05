import re

from adam.commands import extract_trailing_options
from adam.commands.command import Command
from adam.commands.devices.devices import device
from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.repl_state import ReplState, RequiredState
from adam.utils import log_timing
from adam.utils_cassandra.address_table import AddressTable, NATError
from adam.utils_cassandra.pod_service import cassandra
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

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
        # return RequiredState.CLUSTER_OR_POD
        return RequiredState.POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, background):
                with log_timing('show.tokens'):
                    ctx: Context = self.context().copy(background=background)

                    nat: AddressTable = log_timing('nat.build', lambda: AddressTable.snapshot(state, ctx=ctx.copy(show_out=False, background=False)))

                    ip = nat.local_ip_from_pod_name(state.pod)

                    def pod(ip: str):
                        status = '** '
                        if ip in nat.status_by_ip(state) and 'status' in nat.status_by_ip(state)[ip]:
                            # print(ip, nat.status_by_ip(state)[ip])
                            status = '' if nat.status_by_ip(state)[ip]['status'] == 'UN' else '* '

                        try:
                            pod = nat.pod_name_from_local_ip(ip)
                            if groups := re.match(r'.*-(.*-\d+)$', pod):
                                pod = groups[1]

                            return f'{status}{pod}'
                        except NATError:
                            if status:
                                return f'{status}{ip}'
                            else:
                                return f'*** {ip}'

                    with cassandra(state) as pods:
                        r = log_timing('nodetool.ring', lambda: pods.nodetool('ring', samples=1, ctx=ctx.copy(show_out=False, background=False)))
                        if isinstance(r, list):
                            r = r[0]

                        ring = NodeTools.parse_nodetool_ring(r.stdout)

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
        return super().completion(state, {'&': None}, pods=device(state).pods(state, '-'))

    def help(self, state: ReplState):
        return super().help(state, 'show Cassandra tokens', args='[&]')