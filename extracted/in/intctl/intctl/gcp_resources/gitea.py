import subprocess
import secrets
import string
from intctl.status import StatusManager
from .utils import Spinner
from typing import Dict
import time

def run(cmd: str, input: str = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, shell=True, input=input, capture_output=True, text=True
    )

# --- Core Logic for Gitea Secret Management ---
def setup_gitea_secrets(cfg: Dict[str, str], status: StatusManager):
    """
    Checks for Gitea credentials in Google Secret Manager.
    If they don't exist, it generates them and stores them securely.

    Args:
        cfg (Dict[str, str]): A dictionary containing configuration like:
                             'project_id', 'organization_uuid', 'workspace_uuid'.
    """
    project = cfg["project_id"]
    org = cfg["organization_uuid"]
    workspace = cfg["workspace_uuid"]

    print("--- Setting up Gitea Credentials in Secret Manager ---")

    # Step 1: Manage the Gitea Password
    # ------------------------------------
    # Define the secret name using the same org-workspace convention
    pw_secret = f"{org}-{workspace}-gitea-password"
    print(f"🔍 Checking for Gitea password in secret '{pw_secret}'...")
    res = run(f"gcloud secrets versions access latest --secret={pw_secret} --project={project}")

    if res.returncode == 0:
        print(f"✅ Reusing existing Gitea password from Secret Manager.")
    else:
        print("🔐 Password secret not found. Generating a new secure password for Gitea...")
        password = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*()") for _ in range(24))
        create_secret_cmd = (
            f"echo -n '{password}' | gcloud secrets create {pw_secret} "
            f"--data-file=- --replication-policy=automatic --project={project}")
        result = run(create_secret_cmd)
        if result.returncode != 0:
            print(f"❌ Failed to create password secret '{pw_secret}'.")
            print(result.stderr.strip())
            print("Please check your permissions or create the secret manually and re-run.")
            return # Stop execution if password creation fails
        else:
            print(f"✅ Stored new Gitea password in Secret Manager under secret: {pw_secret}")

    # Step 2: Manage the Gitea Username
    # ---------------------------------
    user_secret = f"{org}-{workspace}-gitea-username"
    print(f"🔍 Checking for Gitea username in secret '{user_secret}'...")
    if run(f"gcloud secrets describe {user_secret} --project={project}").returncode == 0:
        print(f"✅ Gitea username secret '{user_secret}' already exists.")
    else:
        default_username = "gitea_admin"
        print(f"🔐 Username secret not found. Creating it with default user '{default_username}'...")

        create_user_secret_cmd = (
            f"echo -n '{default_username}' | gcloud secrets create {user_secret} "
            f"--data-file=- --replication-policy=automatic --project={project}")
        result = run(create_user_secret_cmd)
        if result.returncode != 0:
            print(f"❌ Failed to create username secret '{user_secret}'.")
            print(result.stderr.strip())
            print("Please check your permissions or create the secret manually and re-run.")
            return # Stop execution
        else:
            print(f"✅ Created new Gitea username secret '{user_secret}'.")
    print("\n--- Gitea Credentials Setup Complete ---")
    

# In your setup_gitea_secrets.py or a similar setup script

def create_gitea_internal_secret(cfg: Dict[str, str], status: StatusManager):
    """Creates a long, random secret for internal app use, like Gitea's SECRET_KEY."""
    project = cfg["project_id"]
    org = cfg["organization_uuid"]
    workspace = cfg["workspace_uuid"]

    full_secret_name = f"{org}-{workspace}-gitea-secret"
    print(f"🔍 Checking for internal secret '{full_secret_name}'...")

    # Check if the secret already exists. If so, do nothing.
    if run(f"gcloud secrets describe {full_secret_name} --project={project}").returncode == 0:
        print(f"✅ Reusing existing secret '{full_secret_name}'.")
        return

    # If it doesn't exist, create it.
    print(f"🔐 Secret not found. Generating new random value for '{full_secret_name}'...")
    # Generate a URL-safe random string
    length = 64
    random_value = secrets.token_urlsafe(length)

    create_secret_cmd = (
        f"echo -n '{random_value}' | gcloud secrets create {full_secret_name} "
        f"--data-file=- --replication-policy=automatic --project={project}"
    )
    result = run(create_secret_cmd)

    if result.returncode != 0:
        print(f"❌ Failed to create secret '{full_secret_name}'.")
        print(result.stderr.strip())
        raise Exception(f"Failed to create secret {full_secret_name}")
    else:
        print(f"✅ Stored new random value in secret: {full_secret_name}")
        

def create_gitea_values_secret(cfg: dict, status: StatusManager):
    """
    Fetches all dynamic values from GCP and packages them into a single K8s Secret.
    """
    print("🚀 Pre-computing all values for Gitea deployment...")
    
    # --- 1. Gather all necessary values ---
    project_id = cfg["project_id"]
    org_uuid = cfg["organization_uuid"]
    workspace_uuid = cfg["workspace_uuid"]
    instance_name = f"intellithing-pg-{workspace_uuid}".lower()
    db_name = f"intellithing-gitea-{workspace_uuid}".lower()
    
    def get_secret(secret_name):
        full_name = f"{org_uuid}-{workspace_uuid}-{secret_name}"
        print(f"  -> Fetching secret: {full_name}")
        return run(f"gcloud secrets versions access latest --secret={full_name} --project={project_id}").stdout.strip()

    # Fetch secrets and infrastructure details from GCP
    db_host = run(f"gcloud sql instances describe {instance_name} --project={project_id} --format='value(ipAddresses[0].ipAddress)'").stdout.strip()
    db_name = db_name
    db_user = get_secret("pg-username")
    db_password = get_secret("pg-password")
    gitea_admin_user = get_secret("gitea-username")
    gitea_admin_password = get_secret("gitea-password")
    gitea_secret_key = get_secret("gitea-secret")
    
    print("✅ All values fetched successfully.")

    secret_name = f"gitea-resolved-{workspace_uuid}"
    print(f"📦 Packaging values into Kubernetes Secret '{secret_name}'...")

    command = (
        f"kubectl create secret generic {secret_name} -n intellithing "
        f"--from-literal=db.host='{db_host}' "
        f"--from-literal=db.name='{db_name}' "
        f"--from-literal=db.user='{db_user}' "
        f"--from-literal=db.password='{db_password}' "
        f"--from-literal=gitea.admin.user='{gitea_admin_user}' "
        f"--from-literal=gitea.admin.password='{gitea_admin_password}' "
        f"--from-literal=gitea.secret.key='{gitea_secret_key}' "
        "--dry-run=client -o yaml | kubectl apply -f -"
    )
    
    # Execute the command
    run(command)
    
    print(f"🎉 Successfully created/updated Secret '{secret_name}'.")
    

def synchronize_gitea_api_token(cfg: dict, status: StatusManager) -> None:
    """
    Generate a *raw* Gitea API token inside the running pod and save it
    to Google Secret Manager (idempotent).
    """
    print("🔑 Performing post-deployment Gitea token synchronization…")

    project_id   = cfg["project_id"]
    org_uuid     = cfg["organization_uuid"]
    workspace_uuid = cfg["workspace_uuid"]
    api_token_secret_name = f"{org_uuid}-{workspace_uuid}-gitea-api-token"

    # ------------------------------------------------------------------ #
    # 1. Skip everything if the secret already exists
    # ------------------------------------------------------------------ #
    if run(f"gcloud secrets describe {api_token_secret_name} --project={project_id}").returncode == 0:
        print(f"✅ Secret “{api_token_secret_name}” already present – nothing to do.")
        return

    # ------------------------------------------------------------------ #
    # 2. Wait for a running Gitea pod
    # ------------------------------------------------------------------ #
    print("⏳ Waiting for a Gitea pod to be running…")
    pod_name = ""
    for attempt in range(32):                 # 12 × 10 s → 120 s max
        proc = run(
            "kubectl get pods -n intellithing "
            "-l app=gitea --field-selector=status.phase=Running "
            "-o jsonpath={.items[0].metadata.name}"
        )
        if proc.returncode == 0 and proc.stdout.strip():
            pod_name = proc.stdout.strip()
            print(f"✅ Found pod: {pod_name}")
            break

        time.sleep(40)
        print(f"  ↻ still waiting… ({attempt + 1}/12)")

    if not pod_name:
        raise RuntimeError("❌ Timed out waiting for a running Gitea pod")


    # ------------------------------------------------------------------ #
    # 3. Generate a *raw* token inside that pod
    # ------------------------------------------------------------------ #
    gitea_admin_user = "gitea_admin"
    token_name = f"custom-api-layer-token-{int(time.time())}"

    generate_token_cmd = (
        "gitea admin user generate-access-token "
        f"--username '{gitea_admin_user}' "
        f"--token-name '{token_name}' "
        "--scopes all "
        "--raw "
        "--config /etc/gitea/app.ini"
    )

    exec_cmd = (
        f"kubectl exec {pod_name} -n intellithing -c gitea -- {generate_token_cmd}"
    )

    proc = run(exec_cmd)

    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError(
            f"❌ kubectl exec failed:\nSTDERR: {proc.stderr.strip()}"
        )

    raw_token = proc.stdout.strip()
    print("✅ Raw token generated inside pod.")


    # ------------------------------------------------------------------ #
    # 4. Store the token in Secret Manager (create once)
    # ------------------------------------------------------------------ #
    store_cmd = (
        f"echo -n '{raw_token}' | "
        f"gcloud secrets create {api_token_secret_name} "
        f"--data-file=- --replication-policy=automatic "
        f"--project={project_id}"
    )

    store_proc = run(store_cmd)

    if store_proc.returncode != 0:
        raise RuntimeError(
            f"❌ Failed to store token:\nSTDERR: {store_proc.stderr.strip()}"
        )

    print(f"🎉 Token stored in Secret Manager as “{api_token_secret_name}”.")

