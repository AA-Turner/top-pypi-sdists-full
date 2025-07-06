import asyncio
import os
import time
from pathlib import Path
from .utils import Spinner

from google.auth.transport.requests import Request as AuthRequest
from google.cloud import secretmanager_v1
from google.cloud.sql.connector import Connector
from google.auth import default
import asyncpg
from intctl.utils.pathing import scripts_path
from googleapiclient.discovery import build



def finalise_database(cfg: dict, status) -> None:
    status.start("cloudsql_instance_check")

    workspace_uuid = cfg["workspace_uuid"]
    organization_uuid = cfg["organization_uuid"]
    region = cfg["region"]
    project_id = cfg["project_id"]

    # Use default credentials from Cloud Shell
    credentials, _ = default()
    credentials.refresh(AuthRequest())

    db_name = f"intellithing-pg-{workspace_uuid}".replace("_", "-").lower()
    if not db_name[0].isalpha():
        db_name = "pg-" + db_name
    db_name = db_name[:80]

    # STEP 1: Wait for SQL instance to exist
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

    # STEP 2: Check/Create database
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

    # STEP 3: Fetch credentials
    status.start("fetch_db_credentials")

    def access_secret(name: str) -> str:
        client = secretmanager_v1.SecretManagerServiceClient(credentials=credentials)
        secret_name = f"projects/{project_id}/secrets/{name}/versions/latest"
        return client.access_secret_version(request={"name": secret_name}).payload.data.decode()

    try:
        user_secret = f"{organization_uuid}-{workspace_uuid}-pg-username"
        pass_secret = f"{organization_uuid}-{workspace_uuid}-pg-password"

        pg_user = access_secret(user_secret)
        pg_pass = access_secret(pass_secret)

        print("🔐 Fetched DB credentials from Secret Manager.")
        status.complete("fetch_db_credentials")
    except Exception as e:
        print(f"❌ Failed to fetch secrets: {e}")
        status.fail("fetch_db_credentials")
        return

    # STEP 4: Read SQL file
    status.start("load_sql_script")

    sql_path = scripts_path("status.sql")
    if not sql_path.exists():
        print(f"❌ SQL file not found at {sql_path}")
        status.fail("load_sql_script")
        return

    try:
        sql = sql_path.read_text()
        print("📄 Loaded SQL script.")
        status.complete("load_sql_script")
    except Exception as e:
        print(f"❌ Failed to read SQL script: {e}")
        status.fail("load_sql_script")
        return

    # STEP 5: Connect and execute SQL
    status.start("run_sql_script")

    async def execute_sql():
        # Build service client
        service = build(
            "sqladmin", "v1beta4", credentials=credentials, cache_discovery=False
        )
        instance_info = service.instances().get(project=project_id, instance=db_name).execute()

        ip_addr = next(
            (ip["ipAddress"] for ip in instance_info.get("ipAddresses", []) if ip["type"] == "PRIMARY"),
            None
        )

        if not ip_addr:
            ip_addr = next(
                (ip["ipAddress"] for ip in instance_info.get("ipAddresses", []) if ip["type"] == "PRIVATE"),
                None
            )

        if not ip_addr:
            raise RuntimeError("Could not determine Cloud SQL instance public or private IP.")


        conn = await asyncpg.connect(
            user=pg_user,
            password=pg_pass,
            database=db_name,
            host=ip_addr,
            port=5432,
            ssl="require",
        )
        try:
            await conn.execute(sql)
        finally:
            await conn.close()


    try:
        try:
            asyncio.run(execute_sql())
        except RuntimeError as e:
            if "already running" in str(e):
                print("⚠️ Event loop already running, falling back to manual scheduling...")
                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(execute_sql())
            else:
                raise
        print("✅ SQL script executed successfully.")
        status.complete("run_sql_script")
    except Exception as e:
        print(f"❌ SQL execution failed: {e}")
        status.fail("run_sql_script")

