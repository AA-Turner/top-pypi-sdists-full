import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner
import json
import requests
import os
import typer 
from dotenv import load_dotenv
load_dotenv()

def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def ensure_static_ip(cfg: dict, status: StatusManager):
    status.start("static_ip")
    project = cfg["project_id"]
    region = cfg["region"]
    ip_name = f"gateway-manager-ip-{cfg['workspace_uuid']}".lower()

    print(f"🔍 Checking if static IP '{ip_name}' exists...")
    with Spinner(f"Checking for existing static IP '{ip_name}'..."):
        result = run(f"gcloud compute addresses describe {ip_name} --global --project={project}")

    if result.returncode != 0:
        print(f"📡 Reserving static IP '{ip_name}'...")
        with Spinner(f"Creating static IP '{ip_name}'..."):
            result = run(
                f"gcloud compute addresses create {ip_name} "
                f"--global --project={project}"
            )
        if result.returncode != 0:
            print("❌ Failed to reserve static IP.")
            print(result.stderr.strip())
            status.fail("static_ip")
            return
        print("✅ Static IP reserved.")
    else:
        print("✅ Static IP already exists.")
        
        # 🔹 Minimal addition: fetch and store IP in cfg
    ip_result = run(
        f"gcloud compute addresses describe {ip_name} "
        f"--global --project={project} --format='value(address)'"
    )
    if ip_result.returncode == 0:
        cfg["static_ip"] = ip_result.stdout.strip()
        print(f"🌐 static_ip set: {cfg['static_ip']}")
    else:
        print("⚠️ Failed to retrieve static IP value.")    
        
    status.complete("static_ip")
    
    # ===================================================================
    #  Step 2: Create Subdomain via API (New Logic)
    # ===================================================================
    status.start("subdomain_setup")
    print(f"⚙️  Configuring subdomain for organization '{cfg['organization_name']}'...")

    # Get API configuration
    api_base_url = os.getenv("INTELLITHING_API_BASE_URL", "http://34.39.118.103") # Default for local dev
    # api_key = cfg.get("intellithing_key")
    
    # if not api_key:
    #     print("❌ Configuration Error: 'intellithing_key' is missing. Please run 'intctl configure' and sync again.")
    #     status.fail("subdomain_setup")
    #     raise typer.Exit(code=1)

    endpoint = f"{api_base_url}/create_subdomain"

    #TODO Security implmenetation
    # headers = {
    #     "Authorization": f"Bearer {api_key}", # Assuming Bearer token auth
    #     "Content-Type": "application/json"
    # }
    
    payload = {
        "setup_uuid": cfg.get("setup_uuid"),
        "organization_name": cfg.get("organization_name"),
        "user_uuid": cfg.get("user_uuid"),
        "organization_uuid": cfg.get("organization_uuid"),
        "workspace_uuid": cfg.get("workspace_uuid"),
        "static_ip": cfg.get("static_ip")
    }

    # Validate that all required payload fields are present
    if not all(payload.values()):
        print("❌ Internal Error: Missing required data to create subdomain. Please ensure sync was successful.")
        status.fail("subdomain_setup")
        raise typer.Exit(code=1)

    try:
        with Spinner(f"Setting up domain and resolving DNS..."):
            response = requests.post(endpoint, json=payload, timeout=45) #headrs to be included when security is implmeneted.
        
        if response.status_code == 200:
            response_data = response.json()
            domain_name = response_data.get("domain_name")
            if not domain_name:
                print("❌ API Error: Response was successful but did not contain the expected 'domain_name'.")
                status.fail("subdomain_setup")
                raise typer.Exit(code=1)
            
            # Success! Store the domain in the config for subsequent steps.
            cfg["domain"] = domain_name
            print(f"✅ Domain configured successfully: {cfg['domain']}")
            status.complete("subdomain_setup")
        else:
            # Handle API errors gracefully
            error_detail = "No details provided."
            try:
                error_detail = response.json().get("detail", response.text)
            except requests.exceptions.JSONDecodeError:
                error_detail = response.text
                
            print(f"❌ API Error ({response.status_code}): Failed to configure subdomain.")
            print(f"   Reason: {error_detail}")
            status.fail("subdomain_setup")
            raise typer.Exit(code=1)

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: Could not connect to the API at {api_base_url}.")
        print(f"   Details: {e}")
        status.fail("subdomain_setup")
        raise typer.Exit(code=1)
