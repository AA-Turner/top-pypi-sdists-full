import os
import re
from kubernetes import config as kconfig

from adam.config import Config
from adam.utils import idp_token_from_env, lines_to_tabular, log2

class KubeContext:
    _in_cluster = False

    def in_cluster_namespace():
        if 'NAMESPACE' in os.environ:
            return os.environ['NAMESPACE']

        return None

    def in_cluster():
        # KUBERNETES_SERVICE_HOST=172.16.0.1
        return os.environ['KUBERNETES_SERVICE_HOST'] if 'KUBERNETES_SERVICE_HOST' in os.environ else None

    def init_config(config: str = None, is_user_entry = False):
        # try with kubeconfig file first
        # then, try in-cluster access
        loaded = False
        msg = None
        if not config:
            config = os.getenv('KUBECONFIG')

        if config:
            try:
                kconfig.load_kube_config(config_file=config)
                loaded = True
            except:
                msg = f'Kubernetes config file: {config} does not exist or is not valid.'
        else:
            msg = 'Use --config or set KUBECONFIG env variable to path to your config file.'

        if not loaded:
            try:
                kconfig.load_incluster_config()
                loaded = True
                KubeContext._in_cluster = True
                msg = "Kubernetes access initialized with in-cluster access."
            except kconfig.ConfigException:
                pass

        if msg and not is_user_entry and not idp_token_from_env():
            log2(msg)
        if not loaded:
            exit(1)

    def init_params(params_file: str, param_ovrs: list[str], is_user_entry = False):
        Config(params_file, is_user_entry=is_user_entry)

        def err():
            log2('Use -v <key>=<value> format.')
            log2()
            lines = [f'{key}\t{Config().get(key, None)}' for key in Config().keys()]
            log2(lines_to_tabular(lines, separator='\t'))

        for p in param_ovrs:
            tokens = p.split('=')
            if len(tokens) == 2:
                if m := Config().set(tokens[0], tokens[1]):
                    log2(f'set {tokens[0]} {tokens[1]}')
                    log2(m)
                else:
                    err()
                    return None
            else:
                err()
                return None

        return Config().params

    def is_pod_name(name: str):
        namespace = None
        # cs-d0767a536f-cs-d0767a536f-default-sts-0
        nn = name.split('@')
        if len(nn) > 1:
            namespace = nn[1]
        groups = re.match(r"^cs-.*-sts-\d+$", nn[0])
        if groups:
            return (nn[0], namespace)

        return (None, None)

    def is_sts_name(name: str):
        namespace = None
        # cs-d0767a536f-cs-d0767a536f-default-sts
        nn = name.split('@')
        if len(nn) > 1:
            namespace = nn[1]
        groups = re.match(r"^cs-.*-sts$", nn[0])
        if groups:
            return (nn[0], namespace)

        return (None, None)

    def is_pg_name(name: str):
        # stgawsscpsr-c3-c3-k8spg-cs-001
        return name if re.match(r"^(?!pg-).*-k8spg-.*$", name) else None

    def show_out(s: bool):
        return s or Config().is_debug()

    def show_parallelism():
        return Config().get('debugs.show-parallelism', False)