from adam.commands.cql.utils_cql import cassandra
from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import Color, log_timing
from adam.utils_cassandra.address_table import AddressTable, NATError
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils_tabulize import tabulize
from adam.utils_context import Context

class NodeRestartability:
    def probe(state: ReplState, pod: str, in_restartings: list, ctx: Context = Context.NULL):
        if (pod, state.namespace) in in_restartings:
            return NodeRestartability(pod, err=f'{pod} is already in restart.')

        nat: AddressTable = AddressTable.snapshot(state, ctx=ctx)

        ip: str = None
        try:
            ip = nat.local_ip_from_pod_name(pod)
        except NATError as e:
            return NodeRestartability(pod, host_ids_by_pod=nat._host_ids_by_pod, err=str(e))

        # find pod that's up
        running_pods = StatefulSets.running_pods(state.sts, state.namespace)
        pod_to_run_on: str = None
        statuses = nat.status_by_host_id(state)
        for p, host_id in nat._host_ids_by_pod.items():
            if not running_pods or p in running_pods:
                if host_id in statuses:
                    status = statuses[host_id]
                    if 'status' in status and status['status'] == 'UN':
                        pod_to_run_on = p
                        break

        if not pod_to_run_on:
            return NodeRestartability(pod, host_ids_by_pod=nat._host_ids_by_pod, err=f'[DOWN] Cannot locate any pod that works at the moment.')

        ctx.log(f'Chose {pod_to_run_on} for running nodetool ring.')

        with cassandra(state, pod=pod_to_run_on) as pods:
            with log_timing('nodetool ring'):
               r = pods.nodetool('ring', ctx=ctx.copy(show_out=False))

            if isinstance(r, list):
               r = r[0]

            tokens, my_tokens = NodeRestartability.replica_ips(ip, r.stdout)

            if ctx.show_verbose:
               ctx.log2(f'{ip} has {len(my_tokens)} primary token ranges.', verbose=True)
               ctx.log2(verbose=True)
               tabulize(sorted(tokens.keys()),
                        lambda k: f'{nat.status_by_ip(state)[k]["status"]}\t{k}\t{nat.pod_name_from_local_ip[k]}\t{len(tokens[k])}',
                        header='--\tAddress\tPOD\t# Tokens Shared',
                        separator='\t',
                        ctx=ctx.copy(show_out=True, text_color=Color.gray))

            downs = {}
            has_multiple_copies = {}
            try:
                for k, status in nat.status_by_ip(state).items():
                    if p := (nat.pod_name_from_local_ip(k), state.namespace):
                        in_restart = 'yes' if p in in_restartings else 'no'

                        if status["status"] != 'UN' or in_restart == 'yes':
                            token_list = ['Unknown']
                            if k in tokens:
                                token_list = tokens[k]
                            downs[k] = {'status': status['status'], 'pod': p[0], 'namespace': p[1], 'tokens': token_list, 'in_restart': in_restart}

                    if k == ip:
                        has_multiple_copies = tokens[k]
            except NATError as e:
                return NodeRestartability(pod, host_ids_by_pod=nat._host_ids_by_pod, err=str(e))

            return NodeRestartability(pod, downs, has_multiple_copies, host_ids_by_pod=nat._host_ids_by_pod)

    def replica_ips(ip: str, ring_out: str):
         ring = NodeTools.parse_nodetool_ring(ring_out)

         tokens : dict[str, set] = {}

         def line(ip: str):
            if ip not in tokens:
               tokens[ip] = set()

            return tokens[ip]

         my_tokens = set()
         token = None
         s = 0
         for n in ring:
            if s == 0:
               if n['address'] == ip:
                  token = n['token']
                  my_tokens.add(token)

                  s = 1
            elif s == 1:
               line(n['address']).add(token)

               s = 2
            elif s == 2:
               line(n['address']).add(token)

               s = 0

         return tokens, my_tokens


    def __init__(self, pod: str, downs: dict = None, dup_copies: set = None, host_ids_by_pod: dict[str, str] = [], err: str = None):
        self.pod = pod
        self.downs = downs
        self.dup_copies = dup_copies
        self.host_ids_by_pod = host_ids_by_pod
        self.err = err

    def restartable(self):
        if not Config().get('cassandra.restart.check-tokens-dup-hosting', True):
           return not self.downs

        return not self.downs and not self.dup_copies

    def log(self, ctx: Context = Context.NULL):
        if self.err:
            ctx.log2(f'[ERROR] {self.err}')

            return

     #   tabulize(sorted(list(self.host_ids_by_pod.keys())),
     #            lambda p: f'{p}\t{self.host_ids_by_pod[p]}',
     #            header='POD\tHOST_ID',
     #            separator='\t',
     #            ctx=ctx.copy(show_out=True, text_color=ctx.text_color))

        if self.downs:
            ctx.log2(f'[REPLICAS DOWN] The following nodes with replicas are down.')
            ctx.log2()

            downs = self.downs
            tabulize(sorted(list(downs.keys())),
                     lambda k: f'{downs[k]["status"]}\t{k}\t{downs[k]["pod"]}\t{downs[k]["namespace"]}\t{len(downs[k]["tokens"])}\t{downs[k]["in_restart"]}',
                     header='--\tAddress\tPOD\tNAMESPACE\t#_Tokens_Shared\tIn_Restart',
                     separator='\t',
                     text_color=ctx.text_color)

        if self.dup_copies:
            if self.downs:
                ctx.log2()
            ctx.log2(f'[MULTIPLE COPIES ON A SINGLE POD] {self.pod} hosts more than 1 repica of token ranges.')
            ctx.log2(f'  {", ".join(self.dup_copies)}')

        if not self.downs and not self.dup_copies:
            ctx.log2(f'{self.pod} can be restarted safely.')

    def waiting_on(self) -> str:
        if self.err:
            if 'is already in restart' in self.err:
                return self.err.split(' ')[0]

            return '-'

        if self.downs:
            ip = sorted(list(self.downs.keys()))[0]
            if 'pod' in self.downs[ip]:
                pod = self.downs[ip]['pod']

                if self.downs[ip]['status'] != 'UN':
                    return f'DN: {pod}'

                if 'in_restart' in self.downs[ip] and self.downs[ip]['in_restart'] == 'yes':
                    return f'GP: {self.downs[ip]["pod"]}'

                return f'DN: {pod}'

            return '-'

        if self.dup_copies:
            return f'MC: {sorted(list(self.dup_copies))[0]}'

        return '-'