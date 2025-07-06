import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def setup_gcs_bucket(cfg: dict, status: StatusManager) -> None:
    status.start("gcs_bucket")

    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    bucket_name = f"intellithing-{workspace}".lower()

    print(f"🔍 Checking if GCS bucket '{bucket_name}' exists...")

    with Spinner(f"Checking if bucket '{bucket_name}' exists..."):
        exists = run(f"gsutil ls -p {project} -b gs://{bucket_name}")

    if exists.returncode == 0:
        print(f"✅ Bucket '{bucket_name}' already exists.")
        status.complete("gcs_bucket")
        return

    print(f"🚀 Attempting to create GCS bucket '{bucket_name}' in region '{region}'...")

    with Spinner(f"Creating bucket '{bucket_name}' in {region}..."):
        result = run(
            f"gcloud storage buckets create gs://{bucket_name} "
            f"--project={project} --location={region}"
        )

    if result.returncode == 0:
        print(f"✅ Bucket '{bucket_name}' created successfully.")
        status.complete("gcs_bucket")
        return

    print("❌ Failed to create GCS bucket.")
    print(result.stderr.strip())

    print(f"""
🔐 You may not have the required permissions or quota to create a bucket.

Please create the bucket manually using this command:

  gcloud storage buckets create gs://{bucket_name} \\
      --project={project} --location={region}

⏳ Waiting for bucket '{bucket_name}' to be created...
We'll poll every 10 seconds until the bucket is found.
""")

    while True:
        time.sleep(10)
        poll = run(f"gsutil ls -p {project} -b gs://{bucket_name}")
        if poll.returncode == 0:
            print(f"✅ Detected that bucket '{bucket_name}' now exists.")
            break
        print("⏳ Still waiting for bucket to be created...")

    # Optional verification
    run(f"gcloud storage buckets describe {bucket_name} --project={project}")
    print(f"✅ Bucket '{bucket_name}' verified.")
    status.complete("gcs_bucket")
