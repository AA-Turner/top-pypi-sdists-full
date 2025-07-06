import subprocess
import time
import json
import typer

from intctl.status import StatusManager
from .utils import Spinner

def run(cmd: str, input: str = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, shell=True, input=input, capture_output=True, text=True
    )
    
def has_pending_cluster_operations(project: str, region: str) -> bool:
    cmd = (
        f"gcloud container operations list "
        f"--project={project} --region={region} "
        f"--format=json"
    )
    result = run(cmd)
    if result.returncode != 0:
        print("⚠️ Failed to check GKE operations:")
        print(result.stderr)
        return True  # Assume pending to be safe

    operations = json.loads(result.stdout)
    for op in operations:
        if op.get("status") in {"RUNNING", "PENDING"}:
            return True
    return False
    
    
def setup_https_gateway(cfg: dict, status: StatusManager):
    """
    Sets up a GKE Gateway, a Google-managed certificate,
    and an HTTPRoute to enable HTTPS for the gateway-manager.
    """
    status.start("https_gateway")

    project = cfg["project_id"]
    region = cfg["region"]
    workspace = cfg["workspace_uuid"]
    ip_name = f"gateway-manager-ip-{workspace}".lower()
    gateway_name = f"intellithing-gateway-{workspace}".lower()
    domain = cfg.get("domain")
    gatewayClassName = "gke-l7-gxlb"
    
    
    print("⏳ Checking for ongoing GKE operations before enabling Gateway API addon...")

    for i in range(60):  # Wait up to 20 minutes
        with Spinner(f"Checking for pending cluster operations (Attempt {i+1}/30)"):
            if not has_pending_cluster_operations(project, region):
                print("✅ No pending operations. Proceeding.")
                break
        time.sleep(20)
    else:
        print("❌ Cluster has ongoing operations after waiting 10 minutes.")
        status.fail("https_gateway", "Cluster operations blocked the update")
        raise typer.Exit(1)

    # 1. Ensure the GKE Gateway Controller is enabled
    print("🚀 Ensuring GKE Gateway API controller is enabled...")
    with Spinner("Enabling GKE Gateway addon..."):
        update_result = run(
            "gcloud container clusters update int-" + workspace.lower() +
            f" --project={project} --region={region} "
            "--gateway-api=standard"
        )

    if update_result.returncode != 0:
        print("❌ Failed to send 'enable addon' command. Check permissions or gcloud version.")
        print(update_result.stderr)
        status.fail("https_gateway: Command to enable addon failed")
        raise typer.Exit(1)
    
    print("✅ GKE Gateway addon command sent successfully.")

    # 2. Verify the controller is ready (handles both Autopilot and Standard)
    print("🕵️ Verifying controller readiness...")
    
    # First, check if the cluster is Autopilot
    autopilot_check = run(f"gcloud container clusters describe int-{workspace} --region={region} --format='value(autopilot.enabled)'")
    is_autopilot = autopilot_check.stdout.strip().lower() == 'true'

    if is_autopilot:
        print("✅ Autopilot cluster detected. Verifying CRDs are present...")
        # On Autopilot, the proof of a working controller is the presence of CRDs.
        crd_check_result = run("kubectl get crds gatewayclasses.gateway.networking.k8s.io")
        if crd_check_result.returncode != 0:
            print("❌ Gateway API CRDs not found, even on Autopilot. Installation may have failed.")
            status.fail("https_gateway", "CRDs not found on Autopilot cluster")
            raise typer.Exit(1)
        print("✅ Gateway API CRDs are present. Controller is considered ready.")
    else:
        # For Standard clusters, we wait for the controller pod to be running.
        print("⏳ Standard cluster detected. Waiting for Gateway controller pod to become ready...")
        for i in range(30): # Wait up to 10 minutes
            with Spinner(f"Checking for controller pod in gke-gateway-system... (Attempt {i+1}/30)"):
                pods_result = run("kubectl get pods -n gke-gateway-system -o json")
                if pods_result.returncode == 0:
                    pods_json = json.loads(pods_result.stdout)
                    if pods_json.get("items"):
                        # Ensure all pods are running and their containers are ready
                        all_ready = all(
                            p.get("status", {}).get("phase") == "Running" and
                            all(cs.get("ready") for cs in p.get("status", {}).get("containerStatuses", []))
                            for p in pods_json["items"]
                        )
                        if all_ready:
                            print("\n✅ GKE Gateway controller is running.")
                            break
            time.sleep(20)
        else:
            print("\n❌ GKE Gateway controller did not become ready in time.")
            print("   Please check the cluster's status or run: kubectl get pods -n gke-gateway-system")
            status.fail("https_gateway", "Gateway controller installation timed out")
            raise typer.Exit(1)

    # 2. Get the Static IP Address
    print(f"🔍 Fetching static IP address for '{ip_name}'...")
    ip_result = run(f"gcloud compute addresses describe {ip_name} --global --project={project} --format='value(address)'")
    if ip_result.returncode != 0:
        print(f"❌ Could not find static IP '{ip_name}'. Please run setup first.")
        status.fail("https_gateway", f"Static IP not found: {ip_name}")
        raise typer.Exit(1)
    
    static_ip = ip_result.stdout.strip()
    print(f"✅ Found static IP: {static_ip}")
    
    # Get the custom domain from the configuration dictionary
    if not domain:
        print(f"❌ Could not find the custom domain in the configuration. Please ensure the subdomain setup step was successful.")
        status.fail("https_gateway", "Custom domain not found in config")
        raise typer.Exit(1)
    
    print(f"✅ Using custom domain: {domain}")
    
    # 3. Ensure backend service (gateway-manager-deployment) is ready before applying manifests
    def is_service_ready():
        result = run("kubectl get endpoints gateway-manager-deployment -n intellithing -o json")
        if result.returncode != 0:
            return False
        obj = json.loads(result.stdout)
        return bool(obj.get("subsets"))

    print("⏳ Waiting for gateway-manager-deployment service to become ready...")
    for i in range(30):  # 10 minutes max
        with Spinner(f"Checking service readiness (Attempt {i+1}/30)"):
            if is_service_ready():
                print("✅ Service is ready.")
                break
        time.sleep(20)
    else:
        print("❌ Service 'gateway-manager-deployment' is not ready.")
        status.fail("https_gateway", "Service readiness timed out")
        raise typer.Exit(1)


    # 3. Ensure Google-managed SSL certificate exists
    print(f"📄 Creating pre-shared SSL certificate '{gateway_name}-cert' if not exists...")
    cert_check = run(
        f"gcloud compute ssl-certificates describe {gateway_name}-cert "
        f"--global --project={project}"
    )

    if cert_check.returncode != 0:
        create_cert = run(
            f"gcloud compute ssl-certificates create {gateway_name}-cert "
            f"--domains={domain} --global --project={project}"
        )
        if create_cert.returncode != 0:
            print("❌ Failed to create SSL certificate.")
            print(create_cert.stderr)
            status.fail("https_gateway", "Failed to create pre-shared certificate")
            raise typer.Exit(1)
        print("✅ SSL certificate created.")
    else:
        print("✅ Pre-shared SSL certificate already exists.")
        
        
    # 4. Verify the GatewayClass is accepted
    print(f"🔍 Checking GatewayClass '{gateway_name}' acceptance…")
    gc = run(f"kubectl get gatewayclass {gatewayClassName} -o json")
    if gc.returncode != 0:
        print("❌ Couldn't fetch GatewayClass. Aborting.")
        status.fail("https_gateway", "GatewayClass not found")
        raise typer.Exit(1)

    gc_status = json.loads(gc.stdout).get("status", {}).get("conditions", [])
    accepted = any(c["type"] == "Accepted" and c["status"] == "True" for c in gc_status)
    if not accepted:
        print("⏳ GatewayClass not yet Accepted. Waiting…")
        for _ in range(30):
            time.sleep(5)
            gc = run(f"kubectl get gatewayclass {gatewayClassName} -o json")
            gc_status = json.loads(gc.stdout).get("status", {}).get("conditions", [])
            if any(c["type"] == "Accepted" and c["status"] == "True" for c in gc_status):
                print("✅ GatewayClass is Accepted.")
                break
        else:
            print("❌ GatewayClass never became Accepted.")
            status.fail("https_gateway", "GatewayClass acceptance timed out")
            raise typer.Exit(1)
        
    
  # 4. Create the Gateway and HTTPRoute manifests referencing pre-shared cert
    manifests = f"""
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: {gateway_name}
  namespace: intellithing
spec:
  gatewayClassName: gke-l7-gxlb
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: All
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      options:
        networking.gke.io/pre-shared-certs: {gateway_name}-cert
    allowedRoutes:
      namespaces:
        from: All
  addresses:
  - type: NamedAddress
    value: {ip_name}
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: gateway-manager-route
  namespace: intellithing
spec:
  parentRefs:
  - name: {gateway_name}
  hostnames:
  - "{domain}"
  rules:
  - backendRefs:
    - name: gateway-manager-deployment
      port: 80
"""



    print("☸️ Applying Kubernetes Gateway manifests...")
    with Spinner("Applying Gateway, Certificate, and Route..."):
        apply_result = run("kubectl apply -f -", input=manifests)
    
    if apply_result.returncode != 0:
        print("❌ Failed to apply Gateway manifests.")
        print(apply_result.stderr)
        status.fail("https_gateway", "kubectl apply failed")
        raise typer.Exit(1)

    print("✅ Gateway manifests applied successfully.")
    
   
   
    # 5. Wait for the Gateway to be Accepted & Programmed
    print("⏳ Waiting for Gateway to be Accepted & Programmed…")
    for i in range(30):  # ~5 minutes
        gw = run(f"kubectl get gateway {gateway_name} -n intellithing -o json")
        if gw.returncode == 0:
            conds = json.loads(gw.stdout).get("status", {}).get("conditions", [])
            accepted  = any(c["type"] == "Accepted"  and c["status"] == "True" for c in conds)
            programmed = any(c["type"] == "Programmed" and c["status"] == "True" for c in conds)
            if accepted and programmed:
                print("✅ Gateway is Accepted & Programmed.")
                break
        time.sleep(10)
    else:
        print("❌ Gateway never reached Accepted/Programmed.")
        print(f"   kubectl describe gateway {gateway_name} -n intellithing")
        status.fail("https_gateway", "Gateway provisioning timed out")
        raise typer.Exit(1)

    # 6. Wait for HTTPRoute to be Accepted by the Gateway
    print("⏳ Waiting for HTTPRoute to be Accepted…")
    for i in range(30):  # ~5 minutes
        rt = run("kubectl get httproute gateway-manager-route -n intellithing -o json")
        if rt.returncode == 0:
            parents = json.loads(rt.stdout).get("status", {}).get("parents", [])
            if any(
                cond["type"] == "Accepted" and cond["status"] == "True"
                for p in parents for cond in p.get("conditions", [])
            ):
                print("✅ HTTPRoute is Accepted.")
                status.complete("https_gateway")
                return
        time.sleep(10)
    print("❌ HTTPRoute never became Accepted.")
    print("   kubectl describe httproute gateway-manager-route -n intellithing")
    status.fail("https_gateway", "HTTPRoute acceptance timed out")
    raise typer.Exit(1)
    
    
