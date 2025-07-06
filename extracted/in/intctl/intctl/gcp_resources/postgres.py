# intctl/setup_resources/postgres.py

import os
import subprocess
import secrets
import string
import time
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def create_postgres(cfg: dict, status: StatusManager):
    status.start("postgres")
    project = cfg["project_id"]
    region = cfg["region"]
    org = cfg["organization_uuid"]
    workspace = cfg["workspace_uuid"]
    
    # --- NO CHANGE HERE ---
    # Instance naming logic is preserved.
    instance = f"intellithing-pg-{workspace}".lower()
    instance = instance[:80] if instance[0].isalpha() else "pg-" + instance[:77]

    # --- MINIMAL CHANGE HERE ---
    # Define the VPC name based on the consistent naming convention.
    # This is needed for the create command.
    vpc_name = f"intellithing-vpc-{workspace}".lower()

    # Step 1: Check if instance exists
    # --- NO CHANGE HERE ---
    # Idempotency check is preserved.
    with Spinner(f"Checking if Cloud SQL instance '{instance}' exists..."):
        if run(f"gcloud sql instances describe {instance} --project={project}").returncode == 0:
            print(f"✅ Cloud SQL instance '{instance}' already exists.")
            status.complete("postgres")
            return

    # Step 2: Create or retrieve DB password from Secret Manager
    # --- NO CHANGE HERE ---
    # All secret management logic is preserved exactly as it was.
    print("🔍 Checking for existing DB password...")
    pw_secret = f"{org}-{workspace}-pg-password"
    with Spinner("Checking for existing DB password..."):
        res = run(f"gcloud secrets versions access latest --secret={pw_secret} --project={project}")
    if res.returncode == 0:
        password = res.stdout.strip()
        print("✅ Reusing existing password from Secret Manager.")
    else:
        print("🔐 Generating new password...")
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20))
        with Spinner(f"Creating secret {pw_secret}..."):
            result = run(
                f"echo -n '{password}' | gcloud secrets create {pw_secret} "
                f"--data-file=- --replication-policy=automatic --project={project}"
            )
        if result.returncode != 0:
            print("❌ Failed to create password secret.")
            print(result.stderr.strip())
            print("Please create the secret manually and re-run the command.")
            return
        else:
            print(f"✅ Stored new password in Secret Manager under secret: {pw_secret}")


    # Step 3: Ensure the username secret exists
    # --- NO CHANGE HERE ---
    # Username secret logic is preserved.
    user_secret = f"{org}-{workspace}-pg-username"
    with Spinner(f"Checking secret {user_secret}..."):
        if run(f"gcloud secrets describe {user_secret} --project={project}").returncode != 0:
            with Spinner(f"Creating secret {user_secret}..."):
                result = run(
                    f"echo -n 'postgres' | gcloud secrets create {user_secret} "
                    f"--data-file=- --replication-policy=automatic --project={project}"
                )
            if result.returncode != 0:
                print("❌ Failed to create username secret.")
                print(result.stderr.strip())
                print("Please create the secret manually and re-run the command.")
                return

    # Step 4: Attempt to create the Cloud SQL instance
    # --- CRITICAL CHANGES ARE IN THIS BLOCK ---
    print(f"🚀 Creating Cloud SQL instance '{instance}' with a private IP in VPC '{vpc_name}'. This can take up to 20 minutes...")
    with Spinner(f"Creating Cloud SQL instance '{instance}'..."):
        
        # This is the command that has been modified.
        create_command = (
            f"gcloud sql instances create {instance} "
            f"--database-version=POSTGRES_15 --tier=db-f1-micro --region={region} "
            f"--root-password='{password}' --storage-size=10 --storage-type=SSD "
            f"--availability-type=ZONAL --no-backup "
            # --- MODIFICATION START ---
            f"--network={vpc_name} --no-assign-ip "  # Assigns to our VPC and denies a public IP
            # --- MODIFICATION END ---
            f"--project={project} --quiet"
        )
        
        result = run(create_command)

    if result.returncode != 0:
        print("❌ Failed to create Cloud SQL instance.")
        print(result.stderr.strip())
        
        # --- MODIFICATION HERE: The manual command is updated to reflect the private network setup ---
        manual_command = (
            f"gcloud sql instances create {instance} \\\n"
            f"  --database-version=POSTGRES_15 --tier=db-f1-micro --region={region} \\\n"
            f"  --root-password='{password}' --storage-size=10 --storage-type=SSD \\\n"
            f"  --availability-type=ZONAL --no-backup \\\n"
            f"  --network={vpc_name} --no-assign-ip \\\n"
            f"  --project={project}"
        )
        
        print(f"""
🔧 You may not have sufficient permissions to create a Cloud SQL instance, or the instance name may conflict.

Please create the instance manually using:

{manual_command}

⏳ Waiting for instance '{instance}' to become available...
""")

        # --- NO CHANGE HERE ---
        # Polling logic for manual creation is preserved.
        while True:
            time.sleep(10)
            with Spinner("Polling for Cloud SQL instance..."):
                check = run(f"gcloud sql instances describe {instance} --project={project}")
            if check.returncode == 0:
                print(f"✅ Cloud SQL PostgreSQL instance '{instance}' is now available.")
                break
            else:
                print("⏳ Still waiting for Cloud SQL instance...")

    else:
        print(f"🎉 Cloud SQL PostgreSQL instance '{instance}' created with a private IP.")

    status.complete("postgres")