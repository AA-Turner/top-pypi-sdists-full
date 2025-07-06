import os
import subprocess
import tempfile
import base64
import time
import typer
from typing import List
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def create_service_account(cfg: dict, status: StatusManager):
    status.start("service_account")
    project = cfg["project_id"]
    sa_name = "intellithing"
    sa_email = f"{sa_name}@{project}.iam.gserviceaccount.com"
    os.environ["GCP_SERVICE_ACCOUNT_EMAIL"] = sa_email


    # Step 1: Ensure the service account exists
    with Spinner(f"Checking if service account '{sa_email}' exists..."):
        if run(f"gcloud iam service-accounts describe {sa_email} --project {project}").returncode == 0:
            print("✅ Service account exists.")
        else:
            print("🔧 Creating service account...")

            with Spinner(f"Creating service account '{sa_email}'..."):
             result = run(f"gcloud iam service-accounts create {sa_name} --project {project}")
            if result.returncode != 0:
                print("❌ Failed to create service account.")
                print(result.stderr.strip())
                print(f"""
🔐 The currently authenticated account does not have permission to create a service account.

Please do the following manually:
  1. Authenticate with a user who has sufficient IAM permissions:
     gcloud auth login

  2. Or create the service account manually:
     gcloud iam service-accounts create {sa_name} --project {project}

⏳ Waiting for service account '{sa_email}' to be created...
""")

            while True:
                time.sleep(10)
                with Spinner("Polling for service account creation..."):
                    check = run(f"gcloud iam service-accounts describe {sa_email} --project {project}")
                if check.returncode == 0:
                    print("✅ Service account created.")
                    break
                else:
                    print("⏳ Still waiting for service account...")


    # Step 2: Assign roles
    roles: List[str] = [
        "roles/apigateway.admin", "roles/artifactregistry.admin", "roles/cloudbuild.builds.editor",
        "roles/cloudfunctions.admin", "roles/cloudfunctions.developer", "roles/cloudsql.admin",
        "roles/composer.admin", "roles/compute.admin", "roles/compute.viewer", "roles/container.admin",
        "roles/logging.admin", "roles/monitoring.metricWriter", "roles/monitoring.viewer",
        "roles/secretmanager.admin", "roles/iam.serviceAccountUser", "roles/serviceusage.serviceUsageAdmin",
        "roles/storage.admin", "roles/storage.objectAdmin", "roles/storage.objectViewer",
        "roles/storage.bucketViewer", "roles/aiplatform.admin"
    ]

    failed_roles = []

    print("\n🔐 Assigning IAM roles to the service account...")

    for role in roles:
        with Spinner(f"Assigning role {role}..."):
            result = run(
                f"gcloud projects add-iam-policy-binding {project} "
                f"--member=serviceAccount:{sa_email} --role={role}"
            )
        if result.returncode != 0:
            failed_roles.append(role)


    if failed_roles:
        print("\n⚠️ Some roles could not be assigned automatically.")
        for role in failed_roles:
            print(f"  - {role}")
        print(f"""
Please assign these roles manually to the service account:
  {sa_email}

You can do this via the IAM console or CLI.

⏳ Waiting until all roles are assigned...
""")

        while True:
            still_missing = []
            with Spinner("🔄 Verifying role assignments..."):
                time.sleep(10)
                for role in failed_roles:
                    check = run(
                        f"gcloud projects get-iam-policy {project} "
                        f"--flatten='bindings[].members' "
                        f"--filter='bindings.role={role} AND bindings.members=serviceAccount:{sa_email}' "
                        f"--format='value(bindings.role)'"
                    )
                    if role not in check.stdout.strip().splitlines():
                        still_missing.append(role)

            if not still_missing:
                print("✅ All roles successfully assigned.")
                break
            else:
                print(f"⏳ Still waiting for roles: {', '.join(still_missing)}")

    # Step 3: Check and delete existing keys (if any), then create a new one
    print("\n🔑 Managing service account keys...")

    # 1. List existing keys
    with Spinner("🔍 Checking for existing keys..."):
        list_keys_result = run(
            f"gcloud iam service-accounts keys list "
            f"--iam-account {sa_email} --project {project} "
            f"--format='value(name)'"
        )

    existing_keys = list_keys_result.stdout.strip().splitlines()

    # 2. Try deleting existing keys (best effort)
    if existing_keys:
        print(f"🧹 Found {len(existing_keys)} existing key(s). Attempting cleanup...")
        for key in existing_keys:
            key_id = key.split("/")[-1]
            with Spinner(f"Deleting key {key_id}..."):
                delete_result = run(
                    f"gcloud iam service-accounts keys delete {key_id} "
                    f"--iam-account {sa_email} --project {project} --quiet"
                )
                if delete_result.returncode != 0:
                    print(f"⚠️ Warning: Failed to delete key {key_id}. This can safely be ignored.")
                    print(delete_result.stderr.strip())
    else:
        print("✅ No existing keys found.")

    # 3. Create a new key
    fd, key_file = tempfile.mkstemp(suffix=".json")
    os.close(fd)

    while True:
        with Spinner("🔑 Creating service account key..."):
            result = run(
                f"gcloud iam service-accounts keys create {key_file} "
                f"--iam-account {sa_email} --project {project}"
            )
        if result.returncode == 0:
            print("✅ Service account key created.")
            break
        else:
            print("❌ Failed to create key. Make sure you have 'iam.serviceAccountKeys.create' permission.")
            print(result.stderr.strip())
            print("⏳ Retrying in 10 seconds...")
            time.sleep(10)


            
    # Ensure Secret Manager API is enabled
    print("🚀 Enabling Secret Manager API...")
    with Spinner("🔧 Enabling Secret Manager API..."):
        enable_secret_result = run(f"gcloud services enable secretmanager.googleapis.com --project {project}")
    if enable_secret_result.returncode != 0:
        print("❌ Failed to enable Secret Manager API.")
        print(enable_secret_result.stderr.strip())
        raise typer.Exit(1)
    else:
        print("✅ Secret Manager API enabled.")

    #TODO: secret_name base name sa-key can also be taken from the user inpt to match the API. I did not see a point to have this customised.            
    # Step 4: Upload to Secret Manager
    secret = cfg.get('secret_name', 'sa-key') 
    secret_name = f"{cfg['organization_uuid']}-{cfg['workspace_uuid']}-{secret}"

    with Spinner(f"Checking if secret {secret_name} exists..."):
        describe_result = run(f"gcloud secrets describe {secret_name} --project {project}")
    if describe_result.returncode != 0:
        print(f"🔐 Creating secret {secret_name}...")
        run(f"gcloud secrets create {secret_name} --replication-policy=automatic --project {project}")
    else:
        print(f"✅ Secret {secret_name} already exists.")

    print("⬆️ Uploading service account key to Secret Manager...")
    with Spinner("Uploading key to Secret Manager..."):
        run(f"gcloud secrets versions add {secret_name} --data-file={key_file} --project {project}")

    # Step 5: Encode key and store in env
    with open(key_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    os.environ["GCP_SERVICE_ACCOUNT_KEY"] = encoded

    print("✅ Service account setup complete.")
    status.complete("service_account")

