import functools
import re
from kubernetes import client

from adam.config import Config
from .kube_context import KubeContext
from adam.utils import log2, log_exc


# utility collection; methods are all static
class CustomResources:
    def get_app_ids():
        app_ids_by_ss: dict[str, str] = {}

        group = Config().get('app.cr.group', 'ops.c3.ai')
        v = Config().get('app.cr.v', 'v2')
        plural = Config().get('app.cr.plural', 'c3cassandras')
        label = Config().get('app.label', 'c3__app_id-0')
        strip = Config().get('app.strip', '0')

        v1 = client.CustomObjectsApi()
        with log_exc():
            c3cassandras = v1.list_cluster_custom_object(group=group, version=v, plural=plural)
            for c in c3cassandras.items():
                if c[0] == 'items':
                    for item in c[1]:
                        app_ids_by_ss[f"{item['metadata']['name']}@{item['metadata']['namespace']}"] = item['metadata']['labels'][label].strip(strip)

        return app_ids_by_ss

    def get_cr_name(cluster: str, namespace: str = None):
        nn = cluster.split('@')
        # cs-9834d85c68-cs-9834d85c68-default-sts
        if not namespace and len(nn) > 1:
            namespace = nn[1]
        if not namespace:
            namespace = KubeContext.in_cluster_namespace()
        groups = re.match(Config().get('app.cr.cluster-regex', r"(.*?-.*?)-.*"), nn[0])

        return f"{groups[1]}@{namespace}"

    def get_app_id(sts_or_pod: str, namespace: str):
        c3_app_id = None

        apps = CustomResources.get_app_ids()
        cr_name = CustomResources.get_cr_name(cluster = sts_or_pod, namespace=namespace)
        if cr_name in apps:
            c3_app_id = (apps[cr_name])

        return c3_app_id

    def get_metrics(namespace: str, pod_name: str, container_name: str = None) -> dict[str, any]:
        # 'containers': [
        #     {
        #     'name': 'cassandra',
        #     'usage': {
        #         'cpu': '31325875n',
        #         'memory': '17095800Ki'
        #     }
        #     },
        #     {
        #     'name': 'medusa',
        #     'usage': {
        #         'cpu': '17947213n',
        #         'memory': '236456Ki'
        #     }
        #     },
        #     {
        #     'name': 'server-system-logger',
        #     'usage': {
        #         'cpu': '49282n',
        #         'memory': '1608Ki'
        #     }
        #     }
        # ]
        for pod in CustomResources.list_metrics_crs(namespace)['items']:
            p_name = pod["metadata"]["name"]
            if p_name == pod_name:
                if not container_name:
                    return pod

                for container in pod["containers"]:
                    if container["name"] == container_name:
                        return container

        return None

    def list_metrics_crs(namespace: str, plural = "pods") -> dict[str, any]:
        group = "metrics.k8s.io"
        version = "v1beta1"

        api = client.CustomObjectsApi()

        return api.list_namespaced_custom_object(group=group, version=version, namespace=namespace, plural=plural)

    def create_medusa_backupjob(bkname: str, dc: str, ns: str):
        bkspecs = {
            "apiVersion": "medusa.k8ssandra.io/v1alpha1",
            "kind": "MedusaBackupJob",
            "metadata": {
                "name": bkname,
                "namespace": ns,
                "labels": {
                    "cassandra.datastax.com/cluster": dc,
                    "cassandra.datastax.com/datacenter": dc
                }
            },
            "spec": {
                "backupType": "full",
                "cassandraDatacenter": dc
            }
        }
        # create an instance of the API class
        api_instance = client.CustomObjectsApi()
        group = 'medusa.k8ssandra.io'
        version = 'v1alpha1'
        namespace = ns
        plural = 'medusabackupjobs'
        body = bkspecs
        pretty = 'true'

        with log_exc(lambda e: "Exception when calling create_medusa_backupjob.create_namespaced_custom_object: %s\n" % e):
            api_instance.create_namespaced_custom_object(group, version, namespace, plural, body, pretty=pretty)
            log2(f"create_medusa_backupjob: created Full Backup {bkname}: {api_instance}")

        return None

    def create_medusa_restorejob(restorejobname: str, bkname: str, dc: str, ns: str):
        rtspecs = {
            "apiVersion": "medusa.k8ssandra.io/v1alpha1",
            "kind": "MedusaRestoreJob",
            "metadata": {
                "name": restorejobname,
                "namespace": ns,
                "labels": {
                    "cassandra.datastax.com/cluster": dc,
                    "cassandra.datastax.com/datacenter": dc
                }
            },
            "spec": {
                "backup": bkname,
                "cassandraDatacenter": dc
            }
        }
        # create an instance of the API class
        api_instance = client.CustomObjectsApi()
        group = 'medusa.k8ssandra.io'
        version = 'v1alpha1'
        namespace = ns
        plural = 'medusarestorejobs'
        body = rtspecs
        pretty = 'true'

        with log_exc(lambda e: "Exception when calling create_medusa_restorejob.create_namespaced_custom_object: %s\n" % e):
            api_instance.create_namespaced_custom_object(group, version, namespace, plural, body, pretty=pretty)
            log2(f"create_medusa_restorejob: created Restore Job {restorejobname}: {api_instance}")

        return None

    def medusa_show_backup_names(dc: str, ns: str) -> list[dict]:
        return [job['metadata']['name'] for job in CustomResources.medusa_show_backupjobs(dc, ns)]

    def medusa_get_backupjob(dc: str, ns: str, name: str) -> dict:
        for job in CustomResources.medusa_show_backupjobs(dc, ns):
            if job['metadata']['name'] == name:
                return job

        return None

    def clear_caches():
        CustomResources.medusa_show_backupjobs.cache_clear()

    @functools.lru_cache()
    def medusa_show_backupjobs(dc: str, ns: str) -> list[dict]:
        api_instance = client.CustomObjectsApi()
        group = 'medusa.k8ssandra.io'
        version = 'v1alpha1'
        namespace = ns
        plural = 'medusabackupjobs'
        pretty = 'true'
        label_selector = 'cassandra.datastax.com/datacenter=' + dc

        with log_exc(lambda e: "Exception when calling medusa_show_backupjobs.list_namespaced_custom_object: %s\n" % e):
            api_response = api_instance.list_namespaced_custom_object(group, version, namespace, plural, pretty=pretty, label_selector=label_selector)
            return api_response['items']

        return None

    def medusa_show_restorejobs(dc: str, ns: str):
        api_instance = client.CustomObjectsApi()
        group = 'medusa.k8ssandra.io'
        version = 'v1alpha1'
        namespace = ns
        plural = 'medusarestorejobs'
        pretty = 'true'
        label_selector = 'cassandra.datastax.com/datacenter=' + dc
        rtlist = []

        with log_exc(lambda e: "Exception when calling medusa_show_restorejobs.list_namespaced_custom_object: %s\n" % e):
            api_response = api_instance.list_namespaced_custom_object(group, version, namespace, plural, pretty=pretty, label_selector=label_selector)
            for x in api_response['items']:
                rtlist.append(f"{x['metadata']['name']}\t{x['metadata']['creationTimestamp']}\t{x['status'].get('finishTime', '')}")
            return rtlist

        return None