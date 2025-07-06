import base64
import json
import os
import subprocess
import time
from typing import List
from intctl.status import StatusManager
from tqdm import tqdm
from .utils import Spinner
from intctl.utils.pathing import k8s_path

def run(cmd: str, input: str = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        shell=True,
        input=input,
        capture_output=True,
        text=True
    )


def wait_for_cluster(project: str, region: str, cluster_name: str):
    print(f"🔍 Waiting for GKE cluster '{cluster_name}' to become available...")
    while True:
        with Spinner(f"Checking cluster '{cluster_name}' status..."):
            check = run(
                f"gcloud container clusters describe {cluster_name} "
                f"--region={region} --project={project}"
            )
        if check.returncode == 0:
            print(f"✅ Cluster '{cluster_name}' is available.")
            break
        print(f"⏳ Still waiting for cluster '{cluster_name}'...")
        time.sleep(10)


def transfer_and_deploy(cfg: dict, status: StatusManager):
    status.start("deploy")

    # Step 0: Config
    source_project = "intellithing"
    source_location = "europe-west2"
    target_project = cfg["project_id"]
    target_location = cfg["region"]
    workspace = cfg["workspace_uuid"]
    target_repo = f"intellithing-{workspace}".lower()
    cluster_name = f"int-{workspace}".lower()
    images = ["project-manager", "status-manager", "gateway-manager"]
    

    # Step 1: Docker auth
    for loc in [source_location, target_location]:
        while True:
            print(f"🔐 Authenticating Docker for {loc}-docker.pkg.dev...")
            if loc == source_location:
                auth_cmd = (
                    f"echo '{cfg.get('intellithing_key')}' | "
                    f"docker login -u oauth2accesstoken --password-stdin {loc}-docker.pkg.dev"
                )
            else:
                auth_cmd = (
                    f"gcloud auth print-access-token | "
                    f"docker login -u oauth2accesstoken --password-stdin {loc}-docker.pkg.dev"
                )
            with Spinner(f"Logging into {loc}-docker.pkg.dev..."):
                result = run(auth_cmd)
            if result.returncode == 0:
                break
            print(f"❌ Docker auth failed for {loc}. Retrying in 10s...\n{result.stderr.strip()}")
            time.sleep(10)


    # Step 2: Pull, tag, and push Docker images
    for image in tqdm(images, desc="📦 Pulling & Pushing Docker Images", unit="image"):
        src = f"{source_location}-docker.pkg.dev/{source_project}/intellithing-public/{image}:latest"
        tgt = f"{target_location}-docker.pkg.dev/{target_project}/{target_repo}/{image}:latest"

        while True:
            tqdm.write(f"📦 Pulling image: {src}")
            with Spinner(f"Pulling {src}..."):
                pull = run(f"docker pull {src}")
            if pull.returncode == 0:
                break
            tqdm.write(f"❌ Failed to pull {src}. Retrying in 10s...\n{pull.stderr.strip()}")
            time.sleep(10)

        run(f"docker tag {src} {tgt}")

        while True:
            tqdm.write(f"🚀 Pushing image: {tgt}")
            with Spinner(f"Pushing {tgt}..."):
                push = run(f"docker push {tgt}")
            if push.returncode == 0:
                break
            tqdm.write(f"❌ Failed to push {tgt}. Retrying in 10s...\n{push.stderr.strip()}")
            time.sleep(10)

    # Step 3: Wait for cluster and get credentials
    wait_for_cluster(target_project, target_location, cluster_name)

    while True:
        print(f"📡 Fetching GKE credentials for '{cluster_name}'...")
        with Spinner(f"Getting credentials for '{cluster_name}'..."):
            creds = run(
                f"gcloud container clusters get-credentials {cluster_name} "
                f"--region={target_location} --project={target_project}"
            )
        if creds.returncode == 0:
            break
        print(f"❌ Failed to get GKE credentials. Retrying in 10s...\n{creds.stderr.strip()}")
        time.sleep(10)


    # Step 4: Patch secret
    key = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
    env = cfg.get("environment", "dev")
    if not key:
        print("❌ GCP_SERVICE_ACCOUNT_KEY environment variable is missing.")
        status.fail("deploy")
        return
 
    
    # Ensure the secret exists before patching
    print("🔍 Checking if 'gcp-creds' secret exists...")
    check = run("kubectl get secret gcp-creds -n intellithing")
    if check.returncode != 0:
        print("🆕 Creating 'gcp-creds' secret placeholder...")
        create = run("kubectl create secret generic gcp-creds -n intellithing")
        if create.returncode != 0:
            print("❌ Failed to create 'gcp-creds' secret.")
            print(create.stderr)
            status.fail("deploy")
            return
        print("✅ 'gcp-creds' secret created.")

    while True:
            print("🔧 Patching gcp-creds secret...")
            with Spinner("Patching Kubernetes secret..."):
                key_single_encoded = os.environ.get("GCP_SERVICE_ACCOUNT_KEY")
                env = cfg.get("environment", "dev")
                key_double_encoded = base64.b64encode(key_single_encoded.encode('utf-8')).decode('utf-8')
                env_encoded = base64.b64encode(env.encode('utf-8')).decode('utf-8')

                patch_payload_dict = {
                    "data": {
                        "GCP_SERVICE_ACCOUNT_KEY": key_double_encoded,
                        "ENVIRONMENT": env_encoded
                    }
                }

                patch_payload_json = json.dumps(patch_payload_dict)

                patch_cmd_list = [
                    "kubectl", "patch", "secret", "gcp-creds",
                    "-n", "intellithing",
                    "--type=merge",
                    "-p", patch_payload_json
                ]
                
                patch = subprocess.run(patch_cmd_list, capture_output=True, text=True)

            if patch.returncode == 0:
                print("✅ Secret patched successfully.")
                break
            
            print(f"❌ Failed to patch secret. Retrying in 10s...")
            print(f"   STDOUT: {patch.stdout.strip()}")
            print(f"   STDERR: {patch.stderr.strip()}")
            time.sleep(10)

    # Step 5: Apply Kubernetes manifests
    repo_base = f"{target_location}-docker.pkg.dev/{target_project}/{target_repo}"

    for service in tqdm(images, desc="☸️ Deploying to Kubernetes", unit="service"):
        svc_dir = str(k8s_path(service))
        deploy_yaml = os.path.join(svc_dir, "deployment.yaml")

        if os.path.exists(deploy_yaml):
            image_path = f"{repo_base}/{service}:latest"
            tqdm.write(f"☸️ Deploying {service}")
            with open(deploy_yaml, "r") as f:
                raw_yaml = f.read().replace("__IMAGE_TAG__", image_path)

            while True:
                with Spinner(f"Applying deployment.yaml for {service}..."):
                    apply_result = run("kubectl apply -f -", input=raw_yaml)
                if apply_result.returncode == 0:
                    break
                tqdm.write(f"❌ Failed to apply deployment.yaml for {service}. Retrying in 10s...\n{apply_result.stderr.strip()}")
                time.sleep(10)
                
        # Apply all manifests except deployment.yaml
        manifests = [
            os.path.join(svc_dir, f) for f in os.listdir(svc_dir)
            if f.endswith(".yaml") and f != "deployment.yaml"
        ]

        for manifest in manifests:
            with open(manifest, "r") as f:
                content = f.read()

            while True:
                tqdm.write(f"☸️ Applying {manifest}")
                with Spinner(f"Applying {manifest}..."):
                    apply_other = run("kubectl apply -f -", input=content)
                if apply_other.returncode == 0:
                    break
                tqdm.write(f"❌ Failed to apply {manifest}. Retrying in 10s...\n{apply_other.stderr.strip()}")
                time.sleep(10)




    status.complete("deploy")
    print("✅ Deployment complete.")
