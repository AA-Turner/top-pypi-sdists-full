import os
import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)




def ensure_namespace_exists(namespace: str) -> None:
    result = run(f"kubectl get namespace {namespace}")
    if result.returncode != 0:
        print(f"🔧 Namespace '{namespace}' not found. Creating it...")
        create = run(f"kubectl create namespace {namespace}")
        if create.returncode != 0:
            print("❌ Failed to create namespace.")
            print(create.stderr)
            raise RuntimeError("Namespace creation failed.")
        else:
            print(f"✅ Namespace '{namespace}' created.")

def enable_gke_monitoring(cluster_name: str, region: str, project: str) -> None:
    def wait_for_cluster_status(desired_status: str = "RUNNING", timeout: int = 600):
        print(f"🔄 Waiting for cluster '{cluster_name}' to reach status: {desired_status}...")
        start = time.time()
        while time.time() - start < timeout:
            result = run(
                f"gcloud container clusters describe {cluster_name} "
                f"--region={region} --project={project} --format='value(status)'"
            )
            status_str = result.stdout.strip()
            if result.returncode == 0:
                print(f"🔍 Current status: {status_str}")
                if status_str == desired_status:
                    print(f"✅ Cluster is now in '{desired_status}' state.")
                    return
            time.sleep(10)
        raise TimeoutError(f"❌ Timed out waiting for cluster to become '{desired_status}'.")

    def is_monitoring_already_enabled() -> bool:
        result = run(
            f"gcloud container clusters describe {cluster_name} "
            f"--region={region} --project={project} --format=json"
        )
        if result.returncode != 0:
            print("⚠️ Failed to check existing monitoring config. Proceeding with update.")
            return False

        try:
            data = json.loads(result.stdout)
            prometheus_enabled = data.get("monitoringConfig", {}).get("managedPrometheusConfig", {}).get("enabled", False)
            components = set(data.get("monitoringConfig", {}).get("componentConfig", {}).get("enableComponents", []))
            required_components = {"SYSTEM_COMPONENTS", "CADVISOR", "KUBELET"}

            if prometheus_enabled and required_components.issubset(components):
                print("ℹ️ Monitoring and Prometheus are already enabled. Skipping update.")
                return True
        except Exception as e:
            print(f"⚠️ Could not parse monitoring config: {e}")
        return False

    # Step 1: Wait for cluster to be in RUNNING state
    wait_for_cluster_status("RUNNING")

    # Step 2: Check and apply update only if needed
    if is_monitoring_already_enabled():
        return

    print(f"🔧 Enabling GKE monitoring and managed Prometheus on '{cluster_name}'...")
    result = run(
        f"gcloud container clusters update {cluster_name} "
        f"--region={region} --project={project} "
        f"--enable-managed-prometheus "
        f"--monitoring=SYSTEM,CADVISOR,KUBELET"
    )

    if result.returncode == 0:
        print("✅ Managed Prometheus and monitoring successfully enabled.")
    else:
        print("❌ Failed to enable monitoring.")
        print(result.stderr)
        raise RuntimeError("Cluster monitoring setup failed.")
def enable_gke_monitoring(cluster_name: str, region: str, project: str) -> None:
    def wait_for_cluster_status(desired_status: str = "RUNNING", timeout: int = 1200):
        print(f"🔄 Waiting for cluster '{cluster_name}' to reach status: {desired_status}...")
        start = time.time()
        while time.time() - start < timeout:
            result = run(
                f"gcloud container clusters describe {cluster_name} "
                f"--region={region} --project={project} --format='value(status)'"
            )
            status_str = result.stdout.strip()
            if result.returncode == 0:
                print(f"🔍 Current status: {status_str}")
                if status_str == desired_status:
                    print(f"✅ Cluster is now in '{desired_status}' state.")
                    return
            time.sleep(10)
        raise TimeoutError(f"❌ Timed out waiting for cluster to become '{desired_status}'.")

    def is_monitoring_already_enabled() -> bool:
        result = run(
            f"gcloud container clusters describe {cluster_name} "
            f"--region={region} --project={project} --format=json"
        )
        if result.returncode != 0:
            print("⚠️ Failed to check existing monitoring config. Proceeding with update.")
            return False

        try:
            data = json.loads(result.stdout)
            prometheus_enabled = data.get("monitoringConfig", {}).get("managedPrometheusConfig", {}).get("enabled", False)
            components = set(data.get("monitoringConfig", {}).get("componentConfig", {}).get("enableComponents", []))
            required_components = {"SYSTEM_COMPONENTS", "CADVISOR", "KUBELET"}

            if prometheus_enabled and required_components.issubset(components):
                print("ℹ️ Monitoring and Prometheus are already enabled. Skipping update.")
                return True
        except Exception as e:
            print(f"⚠️ Could not parse monitoring config: {e}")
        return False

    # Step 1: Wait for cluster to be in RUNNING state
    wait_for_cluster_status("RUNNING")

    # Step 2: Check and apply update only if needed
    if is_monitoring_already_enabled():
        return

    print(f"🔧 Enabling GKE monitoring and managed Prometheus on '{cluster_name}'...")
    result = run(
        f"gcloud container clusters update {cluster_name} "
        f"--region={region} --project={project} "
        f"--enable-managed-prometheus "
        f"--monitoring=SYSTEM,CADVISOR,KUBELET"
    )

    if result.returncode == 0:
        print("✅ Managed Prometheus and monitoring successfully enabled.")
    else:
        print("❌ Failed to enable monitoring.")
        print(result.stderr)
        raise RuntimeError("Cluster monitoring setup failed.")


    if result.returncode == 0:
        print("✅ Managed Prometheus and monitoring successfully enabled.")
    else:
        print("❌ Failed to enable monitoring.")
        print(result.stderr)
        raise RuntimeError("Cluster monitoring setup failed.")


def create_kubernetes_cluster(cfg: dict, status: StatusManager) -> None:
    status.start("kubernetes")
    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    cluster_name = f"int-{workspace}".lower()

    print(f"🔍 Checking if Kubernetes cluster '{cluster_name}' exists...")

    with Spinner(f"Checking if GKE cluster '{cluster_name}' exists..."):
        exists = run(
            f"gcloud container clusters describe {cluster_name} "
            f"--region={region} --project={project}"
        )
    if exists.returncode == 0:
        print(f"✅ Cluster '{cluster_name}' already exists in region '{region}'.")
        ensure_namespace_exists("intellithing")
        apply_rbac()
        enable_gke_monitoring(cluster_name, region, project)
        status.complete("kubernetes")
        return


    print(f"🚀 Creating Autopilot GKE cluster '{cluster_name}' in {region}...")

    with Spinner(f"Creating GKE cluster '{cluster_name}'..."):
        result = run(
            f"gcloud container clusters create-auto {cluster_name} "
            f"--region={region} --project={project}"
        )

    if result.returncode == 0:
        print(f"✅ Cluster '{cluster_name}' created.")
        apply_rbac()
        enable_gke_monitoring(cluster_name, region, project)
        status.complete("kubernetes")
        return

    print("❌ Failed to create GKE cluster.")
    print(result.stderr.strip())

    print(f"""
🔐 You might not have permission, or there may be quota/policy issues.

Please create the cluster manually using the following command:

  gcloud container clusters create-auto {cluster_name} \\
      --region={region} --project={project}

⏳ Waiting until the cluster '{cluster_name}' is created...
""")

    # Retry loop to poll for existence
    while True:
        time.sleep(10)
        with Spinner("Polling for GKE cluster creation..."):
            check = run(
                f"gcloud container clusters describe {cluster_name} "
                f"--region={region} --project={project}"
            )
        if check.returncode == 0:
            print(f"✅ Cluster '{cluster_name}' has been created.")
            ensure_namespace_exists("intellithing")
            apply_rbac()
            break
        else:
            print("⏳ Still waiting for cluster...")


    status.complete("kubernetes")


import json

def get_service_accounts_to_bind() -> list[tuple[str, str]]:
    result = run("kubectl get serviceaccounts --all-namespaces -o json")
    if result.returncode != 0:
        raise RuntimeError("Failed to fetch service accounts")

    sa_data = json.loads(result.stdout)
    to_bind = []

    for item in sa_data["items"]:
        name = item["metadata"]["name"]
        namespace = item["metadata"]["namespace"]

        # Optional: filter only namespaces you're watching
        if namespace in {"default", "intellithing"} and name == "default":
            to_bind.append((namespace, name))

    return to_bind


def apply_rbac():
    subjects = get_service_accounts_to_bind()

    if not subjects:
        raise RuntimeError("❌ No service accounts found to bind RBAC to.")

    print(f"🔐 Applying RBAC for service accounts: {subjects}")

    # Build subject entries for ClusterRoleBinding
    subject_entries = "\n".join([
        f"""  - kind: ServiceAccount
    name: {name}
    namespace: {namespace}""" for namespace, name in subjects
    ])

    # ClusterRole + ClusterRoleBinding (global read access)
    cluster_rbac_manifest = f"""
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: proxy-service-reader
rules:
  - apiGroups: [""]
    resources: ["services", "endpoints", "pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: proxy-service-reader-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: proxy-service-reader
subjects:
{subject_entries}
"""

    # Role + RoleBinding (specifically for intellithing:default to access default namespace)
    rolebinding_manifest = """
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: proxy-service-reader
  namespace: default
rules:
  - apiGroups: [""]
    resources: ["services", "endpoints", "pods", "pods/log"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: proxy-access-from-intellithing
  namespace: default
subjects:
  - kind: ServiceAccount
    name: default
    namespace: intellithing
roleRef:
  kind: Role
  name: proxy-service-reader
  apiGroup: rbac.authorization.k8s.io
"""

    # Apply both manifests
    for name, manifest in [("ClusterRoleBinding", cluster_rbac_manifest), ("RoleBinding", rolebinding_manifest)]:
        result = subprocess.run(
            ["kubectl", "apply", "-f", "-"],
            input=manifest,
            text=True,
            capture_output=True
        )

        if result.returncode == 0:
            print(f"✅ {name} applied successfully.")
        else:
            print(f"❌ Failed to apply {name}.")
            print(result.stderr)
            raise RuntimeError(f"{name} setup failed.")
