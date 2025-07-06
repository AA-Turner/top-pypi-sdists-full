import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def enable_required_apis(cfg: dict, status: StatusManager) -> None:
    status.start("enable_apis")
    project = cfg["project_id"]
    
    run(f"gcloud config set project {project}")

    required_apis = [
        "apigateway.googleapis.com",              # ApiGateway Admin
        "artifactregistry.googleapis.com",        # Artifact Registry Administrator
        "cloudbuild.googleapis.com",              # Cloud Build Editor
        "cloudfunctions.googleapis.com",          # Cloud Functions Admin/Developer
        "sqladmin.googleapis.com",                # Cloud SQL Admin
        "composer.googleapis.com",                # Composer Administrator
        "compute.googleapis.com",                 # Compute Admin/Viewer
        "container.googleapis.com",               # Kubernetes Engine Admin
        "logging.googleapis.com",                 # Logging Admin
        "monitoring.googleapis.com",              # Monitoring Viewer/Writer
        "secretmanager.googleapis.com",           # Secret Manager Admin
        "iam.googleapis.com",                     # Service Account User
        "serviceusage.googleapis.com",            # Service Usage Admin
        "storage.googleapis.com",                 # Storage Admin / Object Admin / Bucket Viewer
        "aiplatform.googleapis.com",              # Vertex AI Administrator
        "servicenetworking.googleapis.com",
        "certificatemanager.googleapis.com"
    ]

    print("🚀 Enabling required GCP APIs...")
    failed_apis = []

    for api in required_apis:
        print(f"📡 Enabling {api} ...")
        with Spinner():
            result = run(f"gcloud services enable {api} --project={project}")

        if result.returncode != 0:
            print(f"❌ Failed to enable {api}")
            print(result.stderr.strip())
            failed_apis.append(api)
        else:
            print(f"✅ {api} enabled successfully.")

    if failed_apis:
        print("\n⚠️ The following APIs could not be enabled automatically:")
        for api in failed_apis:
            print(f"  - {api}")

        print("\n🔧 Please enable them manually in the GCP console or via CLI:\n")
        for api in failed_apis:
            print(f"  gcloud services enable {api} --project={project}")

        print("\n⏳ Polling for manual activation of the remaining APIs...")

        while failed_apis:
            time.sleep(10)
            still_missing = []

            for api in failed_apis:
                with Spinner():
                    check = run(
                        f"gcloud services list --enabled "
                        f"--filter='config.name:{api}' "
                        f"--project={project} --format='value(config.name)'"
                    )
                    if api not in check.stdout.strip().splitlines():
                        still_missing.append(api)
                    else:
                        print(f"✅ {api} is now enabled.")

            if still_missing:
                print(f"⏳ Still waiting on: {', '.join(still_missing)}")

            failed_apis = still_missing 


    print("✅ All required APIs are now enabled.")
    status.complete("enable_apis")
