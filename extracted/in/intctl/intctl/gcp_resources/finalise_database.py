# intctl/setup_resources/finalise_database.py

import asyncio
import os
import time
from pathlib import Path
import traceback
from google.cloud.sql.connector import Connector, IPTypes
from google.auth.transport.requests import Request as AuthRequest
from google.cloud import secretmanager_v1
from google.auth import default
import asyncpg
from intctl.status import StatusManager
from intctl.utils.pathing import scripts_path
from .utils import Spinner
import uuid
from textwrap import dedent
import uuid
import subprocess
import tempfile
from googleapiclient.discovery import build



def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    """Helper function to run shell commands."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)


# Use an official, small, pre-built image that includes Python and gcloud SDK.
BASE_IMAGE_URI = "google/cloud-sdk:slim"


def create_database(cfg: dict, status: StatusManager) -> None:
    """
    Checks if the Cloud SQL instance is ready and creates the specific database
    within that instance if it doesn't already exist.
    """
    status.start("cloudsql_instance_check")
    
    workspace_uuid = cfg["workspace_uuid"]
    project_id = cfg["project_id"]
    
    db_name = f"intellithing-pg-{workspace_uuid}".replace("_", "-").lower()
    if not db_name[0].isalpha():
        db_name = "pg-" + db_name
    db_name = db_name[:80]

    print(f"🔎 Checking if SQL instance '{db_name}' exists...")
    while True:
        with Spinner(f"Checking Cloud SQL instance '{db_name}'..."):
            inst_check = os.system(
                f"gcloud sql instances describe {db_name} --project={project_id} >/dev/null 2>&1"
            )
        if inst_check == 0:
            print(f"✅ SQL instance '{db_name}' is available.")
            break
        print(f"⏳ Waiting for SQL instance '{db_name}' to be ready. This may take a minute...")
        time.sleep(10)
    status.complete("cloudsql_instance_check")

    status.start("cloudsql_database")
    print(f"🔎 Checking if database '{db_name}' exists...")
    while True:
        db_check = os.system(
            f"gcloud sql databases describe {db_name} --instance={db_name} --project={project_id} >/dev/null 2>&1"
        )
        if db_check == 0:
            print(f"✅ Database '{db_name}' already exists.")
            break
        print(f"🚧 Creating database '{db_name}'...")
        create = os.system(
            f"gcloud sql databases create {db_name} --instance={db_name} --project={project_id}"
        )
        if create == 0:
            print(f"✅ Database '{db_name}' created.")
            break
        print(f"❌ Failed to create database. Retrying in 10s...")
        time.sleep(10)
    status.complete("cloudsql_database")


def execute_sql_job(cfg: dict, status: StatusManager):
    """
    Spawns a Kubernetes Job using a generic cloud-sdk image to execute the
    initialisation SQL from within the VPC. It waits for completion and verifies success.
    """
    status.start("execute_sql_job")

    # --- 1. Get Configuration (No changes here) ---
    project_id = cfg["project_id"]
    workspace_uuid = cfg["workspace_uuid"]
    organization_uuid = cfg["organization_uuid"]
    
    db_instance_name = f"intellithing-pg-{workspace_uuid}".lower()
    if not db_instance_name[0].isalpha():
        db_instance_name = "pg-" + db_instance_name
    db_instance_name = db_instance_name[:80]
    db_name = db_instance_name

    job_suffix = uuid.uuid4().hex[:8]
    job_name = f"sql-init-job-{job_suffix}"
    configmap_name = f"sql-runner-scripts-{job_suffix}"

    # --- 2. Define the Runner Scripts ---
    sql_script_path = scripts_path("status.sql")
    if not sql_script_path.exists():
        raise FileNotFoundError(f"SQL file not found at: {sql_script_path}")
    sql_script_content = sql_script_path.read_text()

    # --- START OF THE FIX ---
    # The python_runner_script is modified to manually handle the double-encoded key.
    python_runner_script = dedent("""\
    import os
    import asyncio
    import traceback
    import base64
    import json
    from google.oauth2 import service_account
    from google.cloud import secretmanager_v1
    from googleapiclient.discovery import build
    import asyncpg

    async def run_sql():

        try:
            print("🔐 Loading service account credentials...")
            key_file_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            with open(key_file_path, 'r') as f:
                singly_encoded_key = f.read()
            decoded_key_json = base64.b64decode(singly_encoded_key).decode('utf-8')
            service_account_info = json.loads(decoded_key_json)
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            project_id = service_account_info['project_id']
            print("✅ Credentials loaded.")

            # Get DB config from env
            db_instance_name = os.environ["DB_INSTANCE_NAME"]
            db_name = os.environ["DB_NAME"]
            org_id = os.environ["ORG_ID"]
            ws_id = os.environ["WS_ID"]

            # Get Private IP from SQL Admin API
            print(f"🌐 Fetching Private IP for SQL instance '{db_instance_name}'...")
            sqladmin = build("sqladmin", "v1beta4", credentials=credentials)
            response = sqladmin.instances().get(project=project_id, instance=db_instance_name).execute()
            ip_addresses = response.get("ipAddresses", [])
            private_ip = next((ip["ipAddress"] for ip in ip_addresses if ip["type"] == "PRIVATE"), None)
            if not private_ip:
                raise RuntimeError("❌ No PRIVATE IP found for the Cloud SQL instance.")
            print(f"✅ Private IP: {private_ip}")

            # Fetch DB secrets
            print("🔑 Fetching DB credentials...")
            client = secretmanager_v1.SecretManagerServiceClient(credentials=credentials)
            def get_secret(name):
                path = f"projects/{project_id}/secrets/{name}/versions/latest"
                return client.access_secret_version(request={"name": path}).payload.data.decode("UTF-8")

            pg_user = get_secret(f"{org_id}-{ws_id}-pg-username")
            pg_pass = get_secret(f"{org_id}-{ws_id}-pg-password")
            print("✅ Credentials fetched.")

            with open("/app/status.sql") as f:
                sql_to_execute = f.read()

            # Connect to DB
            print(f"📡 Connecting to DB '{db_name}' at {private_ip}...")
            conn = await asyncpg.connect(user=pg_user, password=pg_pass, database=db_name, host=private_ip, port=5432)

            try:
                print("📜 Executing SQL script...")
                await conn.execute(sql_to_execute)
                print("✅✅✅ SQL SCRIPT EXECUTED SUCCESSFULLY ✅✅✅")
            finally:
                await conn.close()

        except Exception:
            print("❌ An error occurred during SQL execution.")
            traceback.print_exc()
            exit(1)

    if __name__ == "__main__":
        asyncio.run(run_sql())
    """)
    # --- END OF THE FIX ---

    entrypoint_script = dedent("""\
    #!/bin/sh
    set -e
    echo "Installing Python dependencies..."
    pip install --quiet --no-cache-dir --break-system-packages google-api-python-client google-auth google-cloud-secret-manager asyncpg
    echo "Dependencies installed. Running SQL initialisation script..."
    python3 /app/runner.py
    """)

    # --- 3. Define the Kubernetes Job Manifest (No changes here) ---
    job_yaml = dedent(f"""\
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: {job_name}
      namespace: intellithing
    spec:
      ttlSecondsAfterFinished: 300
      backoffLimit: 2
      template:
        spec:
          restartPolicy: Never
          containers:
          - name: sql-runner
            image: "{BASE_IMAGE_URI}"
            command: ["/bin/sh", "/app/entrypoint.sh"]
            resources:
              requests:
                cpu: "250m"
                memory: "512Mi"
            env:
            - name: GOOGLE_APPLICATION_CREDENTIALS
              value: /var/secrets/google/key.json
            - name: DB_INSTANCE_NAME
              value: "{db_instance_name}"
            - name: DB_NAME
              value: "{db_name}"
            - name: ORG_ID
              value: "{organization_uuid}"
            - name: WS_ID
              value: "{workspace_uuid}"
            volumeMounts:
            - name: scripts-volume
              mountPath: /app
              readOnly: true
            - name: gcp-sa-key
              mountPath: /var/secrets/google
              readOnly: true
          volumes:
          - name: scripts-volume
            configMap:
              name: {configmap_name}
              defaultMode: 0755
          - name: gcp-sa-key
            secret:
              secretName: gcp-creds
              items:
              - key: GCP_SERVICE_ACCOUNT_KEY
                path: key.json
    """)
    
    # (The rest of the function: creating resources, waiting, verifying, and cleaning up remains the same)
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            runner_path = os.path.join(tmpdir, "runner.py"); sql_path = os.path.join(tmpdir, "status.sql"); entrypoint_path = os.path.join(tmpdir, "entrypoint.sh"); job_path = os.path.join(tmpdir, "job.yaml")
            with open(runner_path, "w") as f: f.write(python_runner_script)
            with open(sql_path, "w") as f: f.write(sql_script_content)
            with open(entrypoint_path, "w") as f: f.write(entrypoint_script)
            os.chmod(entrypoint_path, 0o755)
            with open(job_path, "w") as f: f.write(job_yaml)

            print(f"📜 Creating ConfigMap '{configmap_name}' for runner scripts...")
            run(f"kubectl create configmap {configmap_name} -n intellithing --from-file={entrypoint_path} --from-file={runner_path} --from-file={sql_path}")
            
            print(f"🚀 Deploying Kubernetes Job '{job_name}'...")
            run(f"kubectl apply -f {job_path}")

            print(f"⏳ Waiting for Job '{job_name}' to complete... (Timeout: 5 minutes)")
            run(f"kubectl wait --for=condition=complete job/{job_name} -n intellithing --timeout=5m")
            
            print("✅ Job completed. Verifying logs for success message...")
            pod_name = run(f"kubectl get pods -n intellithing --selector=job-name={job_name} -o jsonpath='{{.items[0].metadata.name}}'").stdout.strip()
            logs = run(f"kubectl logs {pod_name} -n intellithing").stdout

            if "✅✅✅ SQL SCRIPT EXECUTED SUCCESSFULLY ✅✅✅" in logs:
                print("🎉 SQL initialization successful!")
                status.complete("execute_sql_job")
            else:
                print("❌ Job completed, but success message was not found in logs."); print("--- POD LOGS ---"); print(logs); print("--- END POD LOGS ---")
                raise RuntimeError("SQL Job execution failed. Check logs for details.")

        finally:
            print("🧹 Cleaning up Kubernetes resources...")
            run(f"kubectl delete job {job_name} -n intellithing --ignore-not-found=true", check=False)
            run(f"kubectl delete configmap {configmap_name} -n intellithing --ignore-not-found=true", check=False)