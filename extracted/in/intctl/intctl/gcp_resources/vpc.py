# intctl/setup_resources/vpc.py

import subprocess
import time
import json
import typer
from intctl.status import StatusManager
from .utils import Spinner


def run(cmd: str) -> subprocess.CompletedProcess:
    """A helper function to run shell commands."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

# --- NEW PERMANENT FIREWALL RULE FOR GKE GATEWAY ---
def ensure_gateway_health_check_firewall_rule(cfg: dict, status: StatusManager):
    """
    Ensures a firewall rule exists to allow ingress from Google Cloud's
    health checkers, which is required for all external load balancers.
    """
    status.start("static_ip")
    project = cfg["project_id"]
    vpc_name = cfg["vpc_name"]
    rule_name = "allow-ingress-from-gcp-health-checkers"
    # These are the two documented IP ranges for all GCP health checks.
    source_ranges = "35.191.0.0/16,130.211.0.0/22"

    print(f"🔍 Checking for firewall rule '{rule_name}' for GKE Gateway...")
    if run(f"gcloud compute firewall-rules describe {rule_name} --project={project}").returncode == 0:
        print(f"✅ Firewall rule '{rule_name}' already exists.")
        return

    print(f"🔥 Creating firewall rule '{rule_name}' to allow GKE Gateway health checks...")
    with Spinner(f"Creating firewall rule '{rule_name}'..."):
        # We allow all TCP ports because GKE can use various ports for its health checks
        # on different services. This is a standard and safe practice for this rule.
        result = run(
            f"gcloud compute firewall-rules create {rule_name} "
            f"--network={vpc_name} "
            f"--allow=tcp "
            f"--source-ranges='{source_ranges}' "
            f"--description='Allow Ingress from GCP health checkers for GKE Gateway/Ingress' "
            f"--project={project}"
        )

    if result.returncode != 0:
        print(f"❌ Failed to create health check firewall rule '{rule_name}'.")
        print(result.stderr)
        raise RuntimeError("Health check firewall rule creation failed. Gateways will not function.")
    
    print(f"✅ Firewall rule '{rule_name}' for health checks created successfully.")

def ensure_vpc_and_peering(cfg: dict, status: StatusManager):
    """
    Ensures a custom VPC, subnet, and VPC peering for Google services exist.

    This function is idempotent and performs the following steps:
    1. Creates a custom VPC network if it doesn't exist.
    2. Creates a subnet within that VPC.
    3. Reserves a global IP range for VPC peering with Google services.
    4. Establishes the VPC peering connection.
    5. Waits until the peering connection is ACTIVE and ready for use.
    """
    status.start("vpc_setup")
    
    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    
    # Define dynamic resource names for consistency
    vpc_name = f"intellithing-vpc-{workspace}".lower()
    subnet_name = f"intellithing-subnet-{workspace}".lower()
    peering_range_name = "google-services-range" # A descriptive, static name is fine
    
    cfg["vpc_name"] = vpc_name
    cfg["subnet_name"] = subnet_name
    cfg["peering_range_name"] = peering_range_name

    # --- Step 1: Create the VPC Network ---
    print(f"🔍 Checking if VPC '{vpc_name}' exists...")
    if run(f"gcloud compute networks describe {vpc_name} --project={project}").returncode != 0:
        print(f"🔧 Creating VPC '{vpc_name}'...")
        with Spinner(f"Creating VPC '{vpc_name}'..."):
            result = run(f"gcloud compute networks create {vpc_name} --subnet-mode=custom --project={project}")
            if result.returncode != 0:
                print(f"❌ Failed to create VPC '{vpc_name}'.")
                print(result.stderr)
                status.fail("vpc_setup")
                raise RuntimeError("VPC creation failed.")
        print(f"✅ VPC '{vpc_name}' created.")
    else:
        print(f"✅ VPC '{vpc_name}' already exists.")

    # --- Step 2: Create the Subnet ---
    print(f"🔍 Checking if subnet '{subnet_name}' exists...")
    if run(f"gcloud compute networks subnets describe {subnet_name} --region={region} --project={project}").returncode != 0:
        print(f"🔧 Creating subnet '{subnet_name}'...")
        with Spinner(f"Creating subnet '{subnet_name}'..."):
            result = run(
                f"gcloud compute networks subnets create {subnet_name} "
                f"--network={vpc_name} --region={region} --range=10.0.0.0/16 " # A /16 range provides ample space
                f"--project={project}"
            )
            if result.returncode != 0:
                print(f"❌ Failed to create subnet '{subnet_name}'.")
                print(result.stderr)
                status.fail("vpc_setup")
                raise RuntimeError("Subnet creation failed.")
        print(f"✅ Subnet '{subnet_name}' created.")
    else:
        print(f"✅ Subnet '{subnet_name}' already exists.")

    # --- Step 3: Reserve IP Range for Service Networking Peering ---
    print(f"🔍 Checking for reserved IP range '{peering_range_name}'...")
    if run(f"gcloud compute addresses describe {peering_range_name} --global --project={project}").returncode != 0:
        print(f"🔧 Reserving IP range '{peering_range_name}' for Google services...")
        with Spinner("Reserving IP range..."):
            result = run(
                f"gcloud compute addresses create {peering_range_name} "
                f"--global --prefix-length=16 --network={vpc_name} "
                f"--purpose=VPC_PEERING --project={project} "
                f"--description='Peering range for Cloud SQL and other Google services'"
            )
            if result.returncode != 0:
                print("❌ Failed to reserve IP range for VPC peering.")
                print(result.stderr)
                status.fail("vpc_setup")
                raise RuntimeError("IP range reservation failed.")
        print("✅ Reserved IP range for peering.")
    else:
        print(f"✅ Peering IP range '{peering_range_name}' already exists.")
        
    # --- Step 4: Establish VPC Peering Connection ---
    print("🔌 Ensuring VPC peering connection to Google services...")
    with Spinner("Connecting VPC peering..."):
        peer_connect = run(
            f"gcloud services vpc-peerings connect "
            f"--service=servicenetworking.googleapis.com "
            f"--network={vpc_name} --ranges={peering_range_name} --project={project}"
        )
    # This command fails if it already exists, so we check for that specific error.
    if peer_connect.returncode != 0 and "already exists" not in peer_connect.stderr:
        print("❌ Peering connection failed.")
        print(peer_connect.stderr)
        status.fail("vpc_setup")
        raise RuntimeError("VPC peering failed.")
    else:
        print("✅ Peering connection initiated or already exists.")

    # --- Step 5: Wait for Peering to become ACTIVE ---
    print("⏳ Waiting for VPC peering to become ACTIVE...")
    peering_is_active = False
    for i in range(30):  # Wait up to 5 minutes
        with Spinner(f"Checking peering status (attempt {i+1}/30)..."):
            peer_status = run(f"gcloud compute networks peerings list --network={vpc_name} --project={project} --format=json")
            if peer_status.returncode == 0 and peer_status.stdout.strip():
                try:
                    # FIXED: This block now correctly handles the nested JSON structure.
                    networks_list = json.loads(peer_status.stdout)
                    for network_obj in networks_list:
                        for peering in network_obj.get('peerings', []):
                            if peering.get('name') == 'servicenetworking-googleapis-com' and peering.get('state') == 'ACTIVE':
                                peering_is_active = True
                                break
                        if peering_is_active:
                            break
                except json.JSONDecodeError:
                    pass # Ignore parse errors and retry
        
        if peering_is_active:
            print("\n✅ VPC peering is ACTIVE.")
            break
        cfg["vpc_name"] = vpc_name
        cfg["subnet_name"] = subnet_name
        cfg["peering_range_name"] = peering_range_name
        time.sleep(10)

    if not peering_is_active:
        print("\n❌ VPC peering did not become ACTIVE in the allotted time.")
        print("   Please check the GCP console for network peering status.")
        status.fail("vpc_setup")
        raise RuntimeError("VPC peering timed out.")

    status.complete("vpc_setup")