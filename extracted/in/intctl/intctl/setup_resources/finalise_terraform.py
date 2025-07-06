import subprocess
import time
from pathlib import Path
from .utils import Spinner
from intctl.utils.pathing import terraform_path


def run(cmd: str, cwd: Path = None) -> subprocess.CompletedProcess:
    print(f"⚙️  Running: {cmd}")
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)


def check_k8s_deployments_healthy() -> bool:
    print("🔍 Checking Kubernetes deployment statuses...")
    result = run("kubectl get deployments -A -o json")
    if result.returncode != 0:
        print("❌ Failed to get deployments:", result.stderr)
        return False

    import json
    try:
        deployments = json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Failed to parse deployment list: {e}")
        return False

    for item in deployments.get("items", []):
        name = item["metadata"]["name"]
        ns = item["metadata"]["namespace"]
        status = item["status"]
        desired = status.get("replicas", 1)
        available = status.get("availableReplicas", 0)
        if available < desired:
            print(f"⏳ Deployment {ns}/{name} not ready ({available}/{desired} replicas)")
            return False

    print("✅ All deployments are healthy.")
    return True


def check_resource_exists(description: str, check_cmd: str) -> bool:
    print(f"🔍 Checking {description}...")
    result = run(check_cmd)
    return result.returncode == 0


def finalise_terraform(cfg: dict, status) -> None:
    env = cfg.get("environment", "prod")
    terraform_dir = terraform_path("kubernetes", env)
    workspace_uuid = cfg["workspace_uuid"]
    project_id = cfg["project_id"]
    region = cfg["region"]

    status.start("terraform", f"Validating resources before running Terraform for workspace {workspace_uuid}")

    # Wait for GKE deployments to be healthy
    for _ in range(30):
        with Spinner("Checking Kubernetes deployments..."):
            if check_k8s_deployments_healthy():
                break
        print("⏳ Waiting for all K8s deployments to be healthy...")
        time.sleep(10)
    else:
        print("❌ Timeout waiting for K8s deployments to be healthy.")
        status.fail("terraform", "Kubernetes deployments not healthy.")
        return

    # Wait for core GCP resources
    gcs_bucket = f"gs://intellithing-{workspace_uuid}".lower()
    cluster_name = f"int-{workspace_uuid}".lower()
    gateway_id = f"intellithing-{workspace_uuid}-gateway".lower()
    api_id = f"intellithing-{workspace_uuid}".lower()
    db_name = f"intellithing-{workspace_uuid}".replace("_", "-").lower()

    required_resources = [
        ("GCS bucket", f"gsutil ls -b {gcs_bucket}"),
        ("Artifact Registry", f"gcloud artifacts repositories describe intellithing-{workspace_uuid} --location={region} --project={project_id}"),
        ("API Gateway", f"gcloud api-gateway gateways describe {gateway_id} --location={region} --project={project_id}"),
        ("Cloud SQL DB", f"gcloud sql databases describe {db_name} --instance={db_name} --project={project_id}"),
        ("Cloud SQL Instance", f"gcloud sql instances describe {db_name} --project={project_id}"),
    ]

    for label, cmd in required_resources:
        for _ in range(30):
            with Spinner(f"Checking {label}..."):
                if check_resource_exists(label, cmd):
                    print(f"✅ {label} is available.")
                    break
            print(f"⏳ Waiting for {label} to become ready...")
            time.sleep(10)
        else:
            print(f"❌ Timeout waiting for {label}.")
            status.fail("terraform", f"{label} not available.")
            return

    # Now we apply Terraform
    try:
        print(f"📦 Terraform directory: {terraform_dir}")

        def tf(cmd: str):
            result = run(cmd, cwd=terraform_dir)
            if result.returncode != 0:
                raise RuntimeError(f"Terraform command failed: {cmd}\n{result.stderr}")

        with Spinner("Running: terraform init"):
            tf("terraform init -input=false")
        with Spinner("Running: terraform plan"):
            tf("terraform plan -input=false -out=tfplan")
        with Spinner("Running: terraform apply"):
            tf("terraform apply -input=false -auto-approve tfplan")


        print("✅ Terraform apply completed.")
        status.complete("terraform")

    except Exception as e:
        print(f"❌ Terraform failed: {e}")
        status.fail("terraform", str(e))
