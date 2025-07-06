import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def setup_artifact_registry(cfg: dict, status: StatusManager) -> None:
    status.start("artifact_registry")

    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    repo_id = f"intellithing-{workspace}".lower()

    print(f"🔍 Checking if Artifact Registry repo '{repo_id}' exists in region '{region}'...")

    with Spinner(f"Checking repository '{repo_id}'..."):
        exists = run(
            f"gcloud artifacts repositories describe {repo_id} "
            f"--location={region} --project={project}"
        )

    if exists.returncode == 0:
        print(f"✅ Repository '{repo_id}' already exists.")
        status.complete("artifact_registry")
        return

    print("🛠 Enabling Artifact Registry API...")
    with Spinner("Enabling Artifact Registry API..."):
        run(f"gcloud services enable artifactregistry.googleapis.com --project={project}")

    print(f"🚀 Creating Docker Artifact Registry repository '{repo_id}'...")
    with Spinner(f"Creating repository '{repo_id}'..."):
        result = run(
            f"gcloud artifacts repositories create {repo_id} "
            f"--repository-format=docker --location={region} "
            f"--description='Repository for project workspace' "
            f"--project={project}"
        )

    if result.returncode == 0:
        print("✅ Artifact Registry repository created successfully.")
        status.complete("artifact_registry")
        return

    print("❌ Failed to create Artifact Registry repository.")
    print(result.stderr.strip())

    print(f"""
🔐 You may not have permission to create Artifact Registry repositories,
or a constraint may be blocking this operation.

Please create it manually using this command:

  gcloud artifacts repositories create {repo_id} \\
      --repository-format=docker \\
      --location={region} \\
      --description="Repository for project workspace" \\
      --project={project}

⏳ Waiting for repository '{repo_id}' to become available...
""")

    # Retry loop
    while True:
        time.sleep(10)
        with Spinner("Polling for Artifact Registry repository..."):
            check = run(
                f"gcloud artifacts repositories describe {repo_id} "
                f"--location={region} --project={project}"
            )
        if check.returncode == 0:
            print("✅ Detected that Artifact Registry repository was created.")
            break
        else:
            print("⏳ Still waiting for repository...")

    status.complete("artifact_registry")
