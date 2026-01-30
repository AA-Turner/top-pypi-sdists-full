import re

from adam.commands import extract_trailing_options, validate_args
from adam.commands.command import Command
from adam.commands.cql.utils_cql import cassandra
from adam.repl_state import ReplState, RequiredState
from adam.utils import tabulize
from adam.utils_context import Context

class ShowCassandraRing(Command):
    COMMAND = 'show cassandra ring'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowCassandraRing, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowCassandraRing.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        with self.validate(args, state) as (args, state):
            with extract_trailing_options(args, '&') as (args, backgrounded):
                with validate_args(args, state, name='Cassandra Node IP'):
                    ip = args[0]

                    with cassandra(state) as pods:
                        r = pods.nodetool('ring', Context.new(cmd, backgrounded=backgrounded))
                        if isinstance(r, list):
                            r = r[0]

                        ring = parse_nodetool_ring(r.stdout)
                        # print(ring)

                        lines : dict[str, set] = {}

                        def line(ip: str):
                            if ip not in lines:
                                lines[ip] = set()

                            return lines[ip]

                        # s = 0
                        # for n in ring:
                        #     if s == 0:
                        #         if n['address'] == ip:
                        #             line(ip).add(n['token'])

                        #             s = 1
                            # elif s == 1:
                            #     line(n['address']).add(n['token'])

                            #     s = 2
                            # elif s == 2:
                            #     line(n['address']).add(n['token'])

                            #     s = 0

                        # tabulize(sorted(lines.keys()), lambda k: f'{k}\t{", ".join(lines[k])}', header='Address\tTokens', separator='\t')

                        token = None
                        s = 0
                        for n in ring[1:]:
                            if s == 0:
                                if n['address'] == ip:
                                    token = n['token']
                                    # line(token).add(n['address'])

                                    s = 1
                            elif s == 1:
                                line(token).add(n['address'])

                                s = 2
                            elif s == 2:
                                line(token).add(n['address'])

                                s = 0

                        tabulize(sorted(lines.keys()), lambda k: f'{k}\t{", ".join(sorted(list(lines[k])))}', header='Token\tAddresses', separator='\t')


                        return state

            #                 result = CassandraNodes.exec(ctx.pod, ctx.namespace, f"nodetool -u {ctx.user} -pw {ctx.pw} status", ctx=ctx_fg)
            # status = parse_nodetool_status(result.stdout)


    def completion(self, state: ReplState):
        return super().completion(state, {'&': None})

    def help(self, state: ReplState):
        return super().help(state, 'show Cassandra tokens', args='[&]')

def parse_nodetool_ring(stdout: str):
    # Datacenter: cs-a7b13e29bd
    # ==========
    # Address           Rack        Status State   Load            Owns                Token
    #                                                                                 9092166997895998344
    # 172.18.7.7        default     Up     Normal  8.32 MiB        ?                   -9051871175443108837
    nodes: list[dict] = []

    s = 0
    for line in stdout.splitlines():
        if s == 0:
            if line.startswith('Address'):
                s = 1
        elif s == 1:
            nodes.append({'address': None, 'token': line.strip(' ')})
            s = 2
        elif s == 2:
            groups = re.match(r"(\S*)\s+(\S*)\s+(\S*)\s+(\S*)\s+(.*B)\s+(\S*)\s+(\S*)", line)
            if groups:
                nodes.append({
                    'address': groups[1],
                    'rack': groups[2],
                    'status': groups[3],
                    'state': groups[4],
                    'load': groups[5],
                    'owns': groups[6],
                    'token': groups[7]
                })

    return nodes