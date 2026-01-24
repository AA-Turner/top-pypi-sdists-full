import functools
import re

from adam.commands.reaper.utils_reaper import Reapers
from adam.config import Config
from adam.utils import log_timing
from adam.utils_k8s.kube_context import KubeContext
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.statefulsets import StatefulSets
from adam.repl_state import ReplState

class CliCommands:
    def values(state: ReplState, collapse = False):
        with log_timing('CliCommands.values'):
            return CliCommands._values(state, collapse)

    @functools.lru_cache()
    def _values(state: ReplState, collapse = False):
        # node-exec-?, nodetool-?, cql-?, reaper-exec, reaper-forward, reaper-ui, reaper-usernae, reaper-password
        d = {}

        if state.sts:
            pod_names: list[str] = [pod.metadata.name for pod in StatefulSets.pods(state.sts, state.namespace)]
        else:
            pod_names = [state.pod]

        if collapse:
            pod_names = pod_names[:1]
            pod_names[0] = pod_names[0].replace('-0', '-?')

        if KubeContext.in_cluster_namespace():
            d |= {
                f'node-exec-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -- bash' for i, pod in enumerate(pod_names)
            }
        else:
            d |= {
                f'node-exec-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -n {state.namespace} -- bash' for i, pod in enumerate(pod_names)
            }

        ncd = {}
        nuser, npw = state.user_pass()
        cuser, cpw = state.user_pass(secret_path='cql.secret')
        if KubeContext.in_cluster_namespace():
            # ping cs-a526330d23-cs-a526330d23-default-sts-0.cs-a526330d23-cs-a526330d23-all-pods-service.stgawsscpsr.svc.cluster.local
            groups = re.match(r'(.*?-.*?-.*?-.*?-).*', state.pod if state.pod else state.sts)
            if groups:
                svc = Config().get('cassandra.service-name', 'all-pods-service')
                ncd |= {
                    f'nodetool-{"?" if collapse else i}': f'nodetool -h {pod}.{groups[1]}{svc} -u {nuser} -pw {npw}' for i, pod in enumerate(pod_names)
                }

                ncd |= {
                    f'cql-{"?" if collapse else i}': f'cqlsh -u {cuser} -p {cpw} {pod}.{groups[1]}{svc}' for i, pod in enumerate(pod_names)
                }

        if not ncd:
            ncd |= {
                f'nodetool-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -n {state.namespace} -- nodetool -u {nuser} -pw {npw}' for i, pod in enumerate(pod_names)
            }

            ncd |= {
                f'cql-{"?" if collapse else i}': f'kubectl exec -it {pod} -c cassandra -n {state.namespace} -- cqlsh -u {cuser} -p {cpw}' for i, pod in enumerate(pod_names)
            }

        d |= ncd

        # PGPASSWORD=pass1234 psql -h host-name -p port -U MyUsername myDatabaseName
        pgs = Secrets.list_secrets(state.namespace, name_pattern=Config().get('pg.name-pattern', '^{namespace}.*k8spg.*'))
        data = {pg: Secrets.get_data(state.namespace, pg) for pg in pgs}
        def reduce_key(key: str):
            return key.replace(f'{state.namespace}-', '').replace('-k8spg-cs-001', '')
        d |= {f'pg-{reduce_key(k)}': f'PGPASSWORD={v["postgres-admin-password"]} psql -h {v["postgres-db-endpoint"]} -p {v["postgres-db-port"]} -U {v["postgres-admin-username"]} postgres' for k, v in data.items()}

        if reaper := Reapers.reaper_spec(state):
            d |= {
                'reaper-exec': reaper["exec"],
                'reaper-forward': reaper["forward"],
                'reaper-ui': reaper["web-uri"],
                'reaper-username': reaper["username"],
                'reaper-password': reaper["password"]
            }

        return d