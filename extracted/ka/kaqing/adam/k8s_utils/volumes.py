from kubernetes import client
from adam.utils import log2

# utility collection on volumes; methods are all static
class Volumes:
    def create_pvc(name: str, storage: int, namespace: str):
        v1 = client.CoreV1Api()
        pvc = client.V1PersistentVolumeClaim(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1PersistentVolumeClaimSpec(
                access_modes=["ReadWriteOnce"],
                resources=client.V1ResourceRequirements(
                    requests={"storage": str(storage)+"Gi"}
                ))
        )
        try:
            v1.create_namespaced_persistent_volume_claim(namespace=namespace, body=pvc)
        except Exception as e:
            if e.status == 409:
                log2("PVC already exists, continue...")
            else:
                raise
        return