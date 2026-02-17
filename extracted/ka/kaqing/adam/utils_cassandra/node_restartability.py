from adam.commands.nodetool.utils_nodetools import NodeTools
from adam.config import Config
from adam.utils_repl.repl_state import ReplState
from adam.utils import Holder
from adam.utils_cassandra.cassandra_status import AddressTranslationError, CassandraStatus
from adam.utils_cassandra.pod_service import cassandra
from adam.utils_color import Color
from adam.utils_concurrent import parallelize
from adam.utils_k8s.k8s_context import K8sContext
from adam.utils_k8s.pods import strip_pod_name
from adam.utils_log import log_timing
from adam.utils_tabulize import tabulize
from adam.utils_context import NULL

class NodeRestartability:
    def tokens(state: ReplState, ctx = NULL) -> tuple[CassandraStatus, list[dict]]:
        with cassandra(state) as pods:
            # both status snapshot and nodetool ring needs k8s pods info
            k8s = K8sContext.preload_pods(state.sts, state.namespace)

            status_holder: Holder[CassandraStatus] = Holder()
            ring_holder: Holder[list[dict]] = Holder()

            def fetch_status():
                status_holder.set(log_timing('cassandra.status.snapshot', lambda: CassandraStatus.snapshot(state, k8s=k8s)))

            def fetch_ring():
                r = pods.nodetool('ring', samples=1, k8s=k8s, ctx=ctx.copy(show_out=False, background=False))
                if isinstance(r, list):
                    r = r[0]

                ring_holder.set(NodeTools.parse_nodetool_ring(r.stdout))

            with parallelize([fetch_status, fetch_ring],
                            msg='d`Fetching|Fetched tokens on {size} nodes') as exec:
                exec.join(lambda fn: fn())

            return status_holder.get(), ring_holder.get()

    def probe(state: ReplState, pod: str, in_restartings: list, ctx = NULL):
        if (pod, state.namespace) in in_restartings:
            return NodeRestartability(pod, err=f'{pod} is already in restart.')

        status: CassandraStatus = None
        ring: list[dict] = None
        status, ring = NodeRestartability.tokens(state, ctx)

        ip: str = None
        try:
            ip = status.ip_from_pod_name(pod)
        except AddressTranslationError as e:
            return NodeRestartability(pod, host_ids_by_pod=status.host_ids_by_pod, err=str(e))

        tokens, my_tokens = NodeRestartability.replica_ips(ip, ring)

        if ctx.debug:
            ctx.debug(f'{ip} has {len(my_tokens)} primary token ranges.', verbose=True)
            ctx.debug(verbose=True)
            tabulize(sorted(tokens.keys()),
                    lambda k: f'{status.status_by_ip()[k]["status"]}\t{k}\t{status.pod_name_from_ip[k]}\t{len(tokens[k])}',
                    header='--\tAddress\tPOD\t# Tokens Shared',
                    separator='\t',
                    ctx=ctx.copy(show_out=True, text_color=Color.gray))

        downs = {}
        has_multiple_copies = {}
        try:
            for k, s in status.status_by_ip().items():
                if p := (status.pod_name_from_ip(k), state.namespace):
                    in_restart = 'yes' if p in in_restartings else 'no'

                    if s["status"] != 'UN' or in_restart == 'yes':
                        token_list = ['Unknown']
                        if k in tokens:
                            token_list = tokens[k]
                        downs[k] = {'status': s['status'], 'pod': p[0], 'namespace': p[1], 'tokens': token_list, 'in_restart': in_restart}

                if k == ip:
                    has_multiple_copies = tokens[k]
        except AddressTranslationError as e:
            return NodeRestartability(pod, host_ids_by_pod=status._host_ids_by_pod, err=str(e))

        return NodeRestartability(pod, downs, has_multiple_copies, host_ids_by_pod=status.host_ids_by_pod)

    def replica_ips(ip: str, ring: list[dict]):
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

    def log(self, ctx = NULL):
        if self.err:
            ctx.log2(f'[ERROR] {self.err}')

            return

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
                pod = strip_pod_name(self.downs[ip]['pod'])

                if self.downs[ip]['status'] != 'UN':
                    return f'DN: {pod}'

                if 'in_restart' in self.downs[ip] and self.downs[ip]['in_restart'] == 'yes':
                    return f'GP: {self.downs[ip]["pod"]}'

                return f'DN: {pod}'

            return '-'

        if self.dup_copies:
            return f'MC: {sorted(list(self.dup_copies))[0]}'

        return '-'