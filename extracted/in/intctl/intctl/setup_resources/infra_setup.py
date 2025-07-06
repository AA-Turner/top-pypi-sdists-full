import subprocess
import time
from intctl.status import StatusManager
from .utils import Spinner
import json
import requests
import os
import typer 

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
    api_base_url = os.getenv("INTELLITHING_API_BASE_URL", "http://34.39.53.4") # Default for local dev
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



def restrict_sql_access(cfg: dict, status: StatusManager):
    status.start("sql_lockdown")
    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]

    # Construct resource names
    sql_instance = f"intellithing-pg-{workspace}".lower()
    vpc_name = f"intellithing-vpc-{workspace}".lower()
    subnet_name = f"intellithing-subnet-{workspace}".lower()

    print(f"🔍 Using SQL instance: {sql_instance}")
    print(f"🔍 Target VPC: {vpc_name}")
    print(f"🔍 Target Subnet: {subnet_name}")

    # (VPC and Subnet creation logic is fine)
    print(f"🔧 Checking if VPC '{vpc_name}' exists...")
    with Spinner(f"Checking VPC '{vpc_name}'..."):
        vpc_check = run(f"gcloud compute networks describe {vpc_name} --project={project} --format='value(name)'")
    if vpc_check.returncode != 0:
        print(f"🆕 Creating VPC '{vpc_name}'...")
        with Spinner(f"Creating VPC '{vpc_name}'..."):
            vpc_create = run(f"gcloud compute networks create {vpc_name} --subnet-mode=custom --project={project}")
        if vpc_create.returncode != 0:
            print("❌ Failed to create VPC."); print(vpc_create.stderr.strip()); status.fail("sql_lockdown"); return
        print("✅ VPC created.")
    else:
        print("✅ VPC already exists.")

    print(f"🔧 Checking if Subnet '{subnet_name}' exists...")
    with Spinner(f"Checking Subnet '{subnet_name}'..."):
        subnet_check = run(f"gcloud compute networks subnets describe {subnet_name} --region={region} --project={project} --format='value(name)'")
    if subnet_check.returncode != 0:
        print(f"🆕 Creating Subnet '{subnet_name}'...")
        with Spinner(f"Creating Subnet '{subnet_name}'..."):
            subnet_create = run(
                f"gcloud compute networks subnets create {subnet_name} --network={vpc_name} --region={region} "
                f"--range=10.0.0.0/16 --project={project}"
            )
        if subnet_create.returncode != 0:
            print("❌ Failed to create Subnet."); print(subnet_create.stderr.strip()); status.fail("sql_lockdown"); return
        print("✅ Subnet created.")
    else:
        print("✅ Subnet already exists.")

    network = vpc_name
    vpc_uri = f"https://www.googleapis.com/compute/v1/projects/{project}/global/networks/{vpc_name}"
    print(f"✅ Using VPC URI: {vpc_uri}")

    # (Allocated IP range logic is fine)
    print("🔧 Checking if allocated IP range 'sql-range' exists for VPC peering...")
    with Spinner("Checking allocated peering range..."):
        check_range = run(f"gcloud compute addresses describe sql-range --global --project={project} --format='value(name)'")
    if check_range.returncode != 0:
        print("🆕 Creating allocated IP range 'sql-range'...")
        create_range = run(
            f"gcloud compute addresses create sql-range --global --prefix-length=16 "
            f"--description='Peering range for Cloud SQL' --network={network} --purpose=VPC_PEERING --project={project}"
        )
        if create_range.returncode != 0:
            print("❌ Failed to create allocated IP range for VPC peering."); print(create_range.stderr.strip()); status.fail("sql_lockdown"); return
        print("✅ Allocated IP range created.")
    else:
        print("✅ Allocated IP range 'sql-range' already exists.")

    # (Peering connect logic is fine)
    print(f"🔌 Ensuring VPC peering exists between '{network}' and Service Networking...")
    with Spinner(f"Connecting VPC peering for '{network}'..."):
        peer_connect = run(
            f"gcloud services vpc-peerings connect "
            f"--service=servicenetworking.googleapis.com "
            f"--network={network} --ranges=sql-range --project={project}"
        )
    if peer_connect.returncode != 0 and "already exists" not in peer_connect.stderr:
        print("⚠️ Peering failed or already exists."); print(peer_connect.stderr.strip())
    else:
        print("✅ Peering connection initiated or already exists.")

    # --- THIS IS THE DEFINITIVE POLLING FIX USING JSON ---
    print("⏳ Waiting for VPC peering to become ACTIVE...")
    peering_is_active = False

    for i in range(30):  # Retry loop: up to ~2.5 min total
        with Spinner(f"Checking peering status (attempt {i+1}/30)..."):
            peer_status = run(
                f"gcloud compute networks peerings list "
                f"--network={network} --project={project} --format=json"
            )

        if peer_status.returncode == 0 and peer_status.stdout.strip():
            try:
                networks_list = json.loads(peer_status.stdout)
                for network in networks_list:
                    for peering in network.get('peerings', []):
                        peering_name = peering.get('name', '')
                        peering_state = peering.get('state', '')
                        print(f"🔍 Checking peering '{peering_name}' with state '{peering_state}'...")
                        if peering_name == 'servicenetworking-googleapis-com' and peering_state == 'ACTIVE':
                            peering_is_active = True
                            break
                    if peering_is_active:
                        break
            except json.JSONDecodeError as e:
                print(f"❌ Failed to decode JSON: {e}")

        if peering_is_active:
            print("\n✅ VPC peering is ACTIVE.")
            break  # Exit the retry loop immediately

        print(f"🔄 Peering not active yet, retrying in 5 seconds...")
        time.sleep(5)

    if not peering_is_active:
        print("\n❌ VPC peering did not become ACTIVE in time. Check GCP console.")
        status.fail("sql_lockdown")
        return

    # (SQL clearing is usually fast, but this is fine)
    print("🔐 Removing all public access from SQL instance...")
    with Spinner(f"Clearing authorized networks on '{sql_instance}'..."):
        run(f"gcloud sql instances patch {sql_instance} --project={project} --clear-authorized-networks")

    # (SQL private IP check is fine)
    print("🔎 Checking if SQL has private IP enabled...")
    with Spinner(f"Describing SQL instance '{sql_instance}'..."):
        check_private = run(f"gcloud sql instances describe {sql_instance} --project={project} --format='value(settings.ipConfiguration.privateNetwork)'")

    # --- THIS IS THE DEFINITIVE SQL PATCH FIX ---
    if not check_private.stdout.strip():
        print("🔐 Enabling private IP and connecting SQL to GKE VPC...")
        enable_private = run(
            f"gcloud sql instances patch {sql_instance} "
            f"--project={project} --network={vpc_uri} --no-assign-ip --async "
            f"--format='value(name)'"
        )
        if enable_private.returncode != 0:
            print("❌ Failed to start the operation to enable private IP."); print(enable_private.stderr.strip()); status.fail("sql_lockdown"); return
        
        operation_id = enable_private.stdout.strip()
        print(f"⏳ Waiting for SQL patch operation '{operation_id}' to complete...")
        with Spinner(f"Patching SQL instance '{sql_instance}'..."):
            wait_for_op = run(f"gcloud sql operations wait {operation_id} --project={project} --timeout=3600")
        
        if wait_for_op.returncode != 0:
            print("\n❌ Operation to enable private IP failed or timed out."); print(f"   Check status with: gcloud sql operations describe {operation_id} --project={project}"); status.fail("sql_lockdown"); return
            
        print("\n✅ SQL is now private and VPC-attached.")
    else:
        print("✅ SQL already has a private network configuration.")

    status.complete("sql_lockdown")