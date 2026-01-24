from adam.config import Config
from adam.repl_state import ReplState
from adam.utils_k8s.custom_resources import CustomResources
from adam.utils_k8s.statefulsets import StatefulSets

def medusa_backup_names(state: ReplState, warm=False):
    if warm and (auto := Config().get('medusa.restore-auto-complete', 'off')) in ['off', 'jit', 'lazy']:
        return {}

    ns = state.namespace
    dc: str = StatefulSets.get_datacenter(state.sts, ns)
    if not dc:
        return {}

    return {id: None for id in [f"{x['metadata']['name']}" for x in CustomResources.medusa_show_backupjobs(dc, ns)]}