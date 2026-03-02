"""Sandbox CLI commands for Plato."""

import asyncio
import base64
import io
import json
import logging
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, quote_plus

import typer
import yaml
from rich.logging import RichHandler
from sqlalchemy import create_engine, text

from plato._generated.api.v1.gitea import (
    create_simulator_repository,
    get_accessible_simulators,
    get_gitea_credentials,
    get_simulator_repository,
)
from plato._generated.api.v1.sandbox import start_worker
from plato._generated.api.v2.jobs import get_flows as jobs_get_flows
from plato._generated.api.v2.jobs import state as jobs_state
from plato._generated.api.v2.sessions import (
    add_ssh_key as sessions_add_ssh_key,
)
from plato._generated.api.v2.sessions import (
    close as sessions_close,
)
from plato._generated.api.v2.sessions import (
    connect_network as sessions_connect_network,
)
from plato._generated.api.v2.sessions import (
    execute as sessions_execute,
)
from plato._generated.api.v2.sessions import (
    get_public_url as sessions_get_public_url,
)
from plato._generated.api.v2.sessions import (
    get_session_details,
)
from plato._generated.api.v2.sessions import (
    snapshot as sessions_snapshot,
)
from plato._generated.api.v2.sessions import (
    state as sessions_state,
)
from plato._generated.models import (
    AddSSHKeyRequest,
    AppSchemasBuildModelsSimConfigCompute,
    AppSchemasBuildModelsSimConfigDataset,
    AppSchemasBuildModelsSimConfigMetadata,
    CreateCheckpointRequest,
    ExecuteCommandRequest,
    Flow,
    VMManagementRequest,
)
from plato.v1.cli.proxy import ssh as gateway_ssh_command
from plato.v1.cli.proxy import tunnel as gateway_tunnel_command
from plato.v1.cli.ssh import generate_ssh_key_pair
from plato.v1.cli.utils import (
    SANDBOX_FILE,
    console,
    get_http_client,
    handle_async,
    read_plato_config,
    remove_sandbox_state,
    require_api_key,
    require_sandbox_field,
    require_sandbox_state,
    save_sandbox_state,
)
from plato.v1.cli.verify import sandbox_verify_app
from plato.v2.async_.flow_executor import FlowExecutor
from plato.v2.sync.client import Plato as PlatoV2
from plato.v2.types import Env, SimConfigCompute
from plato.v2.utils.proxy_tunnel import ProxyTunnel, find_free_port

# UUID pattern for detecting artifact IDs in colon notation
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

sandbox_app = typer.Typer(help="Manage sandboxes for simulator development")
sandbox_app.add_typer(sandbox_verify_app, name="verify")

# Register gateway SSH/tunnel commands
sandbox_app.command(name="ssh")(gateway_ssh_command)
sandbox_app.command(name="tunnel")(gateway_tunnel_command)


def format_public_url_with_router_target(public_url: str | None, service_name: str | None) -> str | None:
    """Format public URL with _plato_router_target parameter for browser access.

    Args:
        public_url: The base public URL (e.g., https://job-id.sims.plato.so)
        service_name: The service/simulator name (e.g., docuseal)

    Returns:
        URL with _plato_router_target parameter appended, or original URL if service is None
    """
    if not public_url or not service_name:
        return public_url

    # Check if router target already exists (idempotent)
    if "_plato_router_target=" in public_url:
        return public_url

    target_param = f"_plato_router_target={service_name}.web.plato.so"
    if "?" in public_url:
        return f"{public_url}&{target_param}"
    else:
        return f"{public_url}?{target_param}"


@sandbox_app.command(name="start")
def sandbox_start(
    # Mode flags
    from_config: bool = typer.Option(False, "--from-config", "-c", help="Use plato-config.yml in current directory"),
    simulator: str = typer.Option(
        None,
        "--simulator",
        "-s",
        help="Simulator name. Supports: -s sim, -s sim:tag, -s sim:<artifact-uuid>",
    ),
    artifact_id: str = typer.Option(None, "--artifact-id", "-a", help="Specific artifact UUID"),
    blank: bool = typer.Option(False, "--blank", "-b", help="Create blank VM"),
    # Config mode options
    dataset: str = typer.Option(None, "--dataset", "-d", help="Dataset from config or simulator"),
    # Artifact mode options
    tag: str = typer.Option("latest", "--tag", "-t", help="Artifact tag (used with -s)"),
    # Blank VM options
    service: str = typer.Option(None, "--service", help="Service name (required for blank VM)"),
    cpus: int = typer.Option(2, "--cpus", help="Number of CPUs (blank VM)"),
    memory: int = typer.Option(1024, "--memory", help="Memory in MB (blank VM)"),
    disk: int = typer.Option(10240, "--disk", help="Disk in MB (blank VM)"),
    # Common options
    timeout: int = typer.Option(1800, "--timeout", help="VM lifetime in seconds (default: 30 minutes)"),
    connect_network: bool = typer.Option(
        True, "--network/--no-network", help="Connect VMs to WireGuard network for SSH access (default: enabled)"
    ),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
    working_dir: Path = typer.Option(
        None, "--working-dir", "-w", help="Working directory for .sandbox.yaml and .plato/"
    ),
):
    """Start a sandbox environment for simulator development.

    Creates a VM that can be used to develop and test simulators. You must pick exactly
    one mode to specify how the sandbox should be created.

    Mode Options (pick exactly one):
        -c, --from-config: Create VM using settings from plato-config.yml in the current
            directory. Uses the compute specs (cpus, memory, disk) from the config file.
        -s, --simulator: Start from an existing simulator. Supports formats:
            '-s name' (latest tag), '-s name:tag' (specific tag), '-s name:uuid' (specific artifact)
        -a, --artifact-id: Start directly from a specific artifact UUID
        -b, --blank: Create a blank VM with custom specs (requires --service)

    Config Mode Options:
        -d, --dataset: Which dataset from the config to use (default: "base")

    Simulator Mode Options:
        -t, --tag: Artifact tag to use (default: "latest")

    Blank VM Options:
        --service: Service name for the blank VM (required with -b)
        --cpus: Number of CPUs (default: 2)
        --memory: Memory in MB (default: 1024)
        --disk: Disk size in MB (default: 10240)

    Common Options:
        --timeout: VM lifetime in seconds before auto-shutdown (default: 1800 = 30 min)
        --no-reset: Skip the initial environment reset after the VM is ready
        --no-network: Disable WireGuard network connection (enabled by default for SSH access)
        -j, --json: Output results as JSON instead of formatted text
        -w, --working-dir: Directory to store .sandbox.yaml and .plato/ files
    """
    api_key = require_api_key()

    # Validate mode selection - exactly one must be specified
    modes_selected = sum([from_config, simulator is not None, artifact_id is not None, blank])
    if modes_selected == 0:
        console.print("[red]❌ No mode specified[/red]")
        console.print()
        console.print("[yellow]Usage (pick one):[/yellow]")
        console.print("  plato sandbox start -c                           # From plato-config.yml")
        console.print("  plato sandbox start -s <simulator>               # From simulator (latest)")
        console.print("  plato sandbox start -s <simulator>:<artifact>    # From specific artifact")
        console.print("  plato sandbox start -a <artifact-uuid>           # From artifact directly")
        console.print("  plato sandbox start -b --service <name>          # Blank VM")
        raise typer.Exit(1)
    if modes_selected > 1:
        console.print("[red]❌ Multiple modes specified - pick only one[/red]")
        console.print()
        console.print("[yellow]Use ONE of:[/yellow]")
        console.print("  -c (--from-config)   # From plato-config.yml")
        console.print("  -s (--simulator)     # From simulator name")
        console.print("  -a (--artifact-id)   # From artifact UUID")
        console.print("  -b (--blank)         # Blank VM")
        raise typer.Exit(1)

    # Validate mode-specific options
    if blank and not service:
        console.print("[red]❌ --service is required for blank VM mode[/red]")
        console.print()
        console.print("[yellow]Usage:[/yellow]")
        console.print("  plato sandbox start -b --service <name>")
        raise typer.Exit(1)

    # Build environment configuration
    env_config = None
    mode = None
    state_extras = {}
    full_dataset_config_dict = None  # For setup_sandbox call in --from-config mode
    config_path = None
    sim_name = None
    dataset_name = None

    if from_config:
        # MODE 1: From plato-config.yml - creates a BLANK VM with specs from config
        mode = "config"
        config_path = Path.cwd() / "plato-config.yml"
        if not config_path.exists():
            config_path = Path.cwd() / "plato-config.yaml"
        if not config_path.exists():
            console.print("[red]plato-config.yml not found in current directory[/red]")
            raise typer.Exit(1)

        with open(config_path) as f:
            plato_config = yaml.safe_load(f)

        sim_name = plato_config.get("service")
        if not sim_name:
            console.print("[red]plato-config.yml missing 'service' field[/red]")
            raise typer.Exit(1)

        # Get dataset (default to "base")
        dataset_name = dataset or "base"
        datasets = plato_config.get("datasets", {})
        if dataset_name not in datasets:
            console.print(f"[red]Dataset '{dataset_name}' not found in plato-config.yml[/red]")
            console.print(f"[yellow]Available datasets: {list(datasets.keys())}[/yellow]")
            raise typer.Exit(1)

        full_dataset_config_dict = datasets[dataset_name]

        # Extract compute specs from config
        compute_config = full_dataset_config_dict.get("compute", {})
        config_cpus = compute_config.get("cpus", 2)
        config_memory = compute_config.get("memory", 2048)
        config_disk = compute_config.get("disk", 10240)
        config_app_port = compute_config.get("app_port", 80)

        # Create blank VM with specs from config
        config_messaging_port = compute_config.get("plato_messaging_port", 7000)
        sim_config = SimConfigCompute(
            cpus=config_cpus, memory=config_memory, disk=config_disk, app_port=config_app_port
        )
        env_config = Env.resource(sim_name, sim_config)
        state_extras = {
            "plato_config_path": str(config_path),
            "service": sim_name,
            "dataset": dataset_name,
            "cpus": config_cpus,
            "memory": config_memory,
            "disk": config_disk,
            "app_port": config_app_port,
            "messaging_port": config_messaging_port,
        }
        if not json_output:
            console.print(f"[cyan]Using plato-config.yml: {config_path}[/cyan]")
            console.print(f"[cyan]Service: {sim_name}, Dataset: {dataset_name}[/cyan]")
            console.print(f"[cyan]Specs: {config_cpus} CPUs, {config_memory}MB RAM, {config_disk}MB disk[/cyan]")

    elif simulator:
        # MODE 2a: From simulator name (or simulator:artifact_id notation)
        mode = "artifact"
        # Default dataset to "base" if not provided
        effective_dataset = dataset or "base"

        # Extract sim_name and check if colon part is a UUID (artifact ID)
        if ":" in simulator:
            sim_name, colon_part = simulator.split(":", 1)
            if UUID_PATTERN.match(colon_part):
                # Colon part is a UUID -> treat as artifact ID
                env_config = Env.artifact(colon_part)
                state_extras = {
                    "simulator": sim_name,
                    "artifact_id": colon_part,
                    "dataset": effective_dataset,
                    "service": sim_name,
                }
                if not json_output:
                    console.print(f"[cyan]Starting from artifact: {sim_name}:{colon_part}[/cyan]")
            else:
                # Colon part is a tag name
                env_config = Env.simulator(simulator, tag=tag, dataset=effective_dataset)
                state_extras = {
                    "simulator": simulator,
                    "tag": colon_part,
                    "dataset": effective_dataset,
                    "service": sim_name,
                }
                if not json_output:
                    console.print(f"[cyan]Starting from simulator: {simulator}[/cyan]")
        else:
            sim_name = simulator
            env_config = Env.simulator(simulator, tag=tag, dataset=effective_dataset)
            state_extras = {"simulator": simulator, "tag": tag, "dataset": effective_dataset, "service": sim_name}
            if not json_output:
                console.print(f"[cyan]Starting from simulator: {simulator}:{tag}[/cyan]")

    elif artifact_id:
        # MODE 2b: From artifact ID
        mode = "artifact"
        env_config = Env.artifact(artifact_id)
        # Default dataset to "base" for artifact mode
        state_extras = {"artifact_id": artifact_id, "dataset": "base"}
        if not json_output:
            console.print(f"[cyan]Starting from artifact: {artifact_id}[/cyan]")

    elif blank:
        # MODE 3: Blank VM
        mode = "blank"
        sim_config = SimConfigCompute(cpus=cpus, memory=memory, disk=disk)
        env_config = Env.resource(service, sim_config)
        state_extras = {
            "service": service,
            "cpus": cpus,
            "memory": memory,
            "disk": disk,
        }
        if not json_output:
            console.print(f"[cyan]Creating blank VM for service: {service}[/cyan]")
            console.print(f"[cyan]Specs: {cpus} CPUs, {memory}MB RAM, {disk}MB disk[/cyan]")

    # Create session using v2 SDK
    if not json_output:
        console.print("[cyan]Creating sandbox...[/cyan]")
        if connect_network:
            console.print("[cyan]Network connection will be established after VM is ready...[/cyan]")
            console.print(
                "[yellow]Note: First connection on older VMs may take a few minutes to install WireGuard[/yellow]"
            )

    try:
        plato = PlatoV2(api_key=api_key)
        if not env_config:
            raise ValueError("No environment configuration provided")
        session = plato.sessions.create(envs=[env_config], timeout=timeout, connect_network=connect_network)

        # Get session info
        session_id = session.session_id
        job_id = session.envs[0].job_id if session.envs else None

        # Get public URL
        public_url = None
        try:
            with get_http_client() as client:
                url_response = sessions_get_public_url.sync(
                    client=client,
                    session_id=session_id,
                    x_api_key=api_key,
                )
                if url_response and url_response.results:
                    for jid, result in url_response.results.items():
                        public_url = result.url if hasattr(result, "url") else str(result)
                        break
        except Exception as e:
            if not json_output:
                console.print(f"[yellow]Could not get public URL: {e}[/yellow]")

        # Note: We don't reset here - start just launches the sandbox.
        # Reset is a separate action the user can take later if needed.

        # Setup SSH for ALL modes (so you can SSH into any sandbox)
        ssh_private_key_path = None

        if session_id and connect_network:
            if not json_output:
                console.print("[cyan]Setting up SSH access...[/cyan]")
            try:
                # Step 1: Generate SSH key pair
                if not json_output:
                    console.print("[cyan]  Generating SSH key pair...[/cyan]")

                public_key, private_key_path = generate_ssh_key_pair(session_id[:8], working_dir)
                ssh_private_key_path = private_key_path

                # Step 2: Add SSH key to all VMs in the session via API
                if not json_output:
                    console.print("[cyan]  Adding SSH key to VMs...[/cyan]")

                ssh_username = "root"
                add_key_request = AddSSHKeyRequest(
                    public_key=public_key,
                    username=ssh_username,
                )

                with get_http_client() as client:
                    add_key_response = sessions_add_ssh_key.sync(
                        client=client,
                        session_id=session_id,
                        body=add_key_request,
                        x_api_key=api_key,
                    )

                if not json_output:
                    # Debug: show full response
                    console.print("[yellow]DEBUG add_ssh_key response:[/yellow]")
                    console.print(f"  success: {add_key_response.success}")

                    # Show results for each job
                    for jid, result in add_key_response.results.items():
                        console.print(f"  [cyan]Job {jid}:[/cyan]")
                        console.print(f"    success: {result.success}")
                        console.print(f"    error: {result.error}")
                        console.print("    output:")
                        if result.output:
                            console.print(result.output)
                        else:
                            console.print("      (none)")
                        if result.success:
                            console.print(f"  [green]✓[/green] {jid}: SSH key added")
                        else:
                            console.print(f"  [red]✗[/red] {jid}: {result.error}")

                if add_key_response.success:
                    if not json_output:
                        console.print("[green]SSH setup complete![/green]")
                        console.print("  [cyan]SSH:[/cyan] plato sandbox ssh")
                else:
                    if not json_output:
                        console.print("[red]SSH key setup failed - SSH may not work[/red]")

            except Exception as e:
                if not json_output:
                    console.print(f"[yellow]Warning: SSH setup failed: {e}[/yellow]")
                    console.print("[yellow]You may not be able to SSH into this sandbox[/yellow]")

        # Start background heartbeat process to keep session alive
        heartbeat_pid = _start_heartbeat_process(session_id, api_key)
        if not json_output and heartbeat_pid:
            console.print(f"[cyan]Started heartbeat process (PID: {heartbeat_pid})[/cyan]")

        # Build the full URL with router target for browser access
        display_url = format_public_url_with_router_target(public_url, sim_name)

        # Save state
        state = {
            "session_id": session_id,
            "job_id": job_id,
            "public_url": display_url,  # Full URL with _plato_router_target
            "mode": mode,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **state_extras,
        }
        # Add SSH private key path if available
        if ssh_private_key_path:
            state["ssh_private_key_path"] = ssh_private_key_path
        # Add heartbeat PID
        if heartbeat_pid:
            state["heartbeat_pid"] = heartbeat_pid
        # Add network connection status
        if connect_network:
            state["network_connected"] = True
        save_sandbox_state(state, working_dir)

        # Close the plato client (heartbeat process keeps session alive)
        plato.close()

        # Output
        if json_output:
            output = {
                "session_id": session_id,
                "job_id": job_id,
                "public_url": display_url,  # Full URL with _plato_router_target
            }
            if ssh_private_key_path:
                output["ssh_private_key_path"] = ssh_private_key_path
                output["ssh_command"] = "plato sandbox ssh"
            console.print(json.dumps(output))
        else:
            console.print("\n[green]Sandbox started successfully![/green]")
            console.print(f"  [cyan]Session ID:[/cyan]  {session_id}")
            console.print(f"  [cyan]Job ID:[/cyan]      {job_id}")
            if public_url:
                display_url = format_public_url_with_router_target(public_url, sim_name)
                console.print(f"  [cyan]Public URL:[/cyan]  {display_url}")
            if ssh_private_key_path:
                console.print("  [cyan]SSH:[/cyan]         plato sandbox ssh")
            console.print(f"\n[dim]State saved to {SANDBOX_FILE}[/dim]")

    except Exception as e:
        if json_output:
            console.print(json.dumps({"error": str(e)}))
        else:
            error_msg = str(e)
            # Check if it's a network connection error with VM details
            if "Network connection failed" in error_msg or "WireGuard" in error_msg:
                console.print("[red]Failed to start sandbox - network setup failed[/red]")
                console.print("[yellow]VM error:[/yellow]")
                # Clean up error message - remove SSH warnings and format nicely
                clean_lines = []
                for line in error_msg.split("\n"):
                    line = line.strip()
                    # Skip SSH warnings
                    if line.startswith("Warning:") or "known hosts" in line:
                        continue
                    if line:
                        clean_lines.append(line)
                for line in clean_lines:
                    console.print(f"  {line}")
            else:
                console.print(f"[red]Failed to start sandbox: {e}[/red]")
        raise typer.Exit(1) from e


@sandbox_app.command(name="snapshot")
def sandbox_snapshot(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
    include_config: bool = typer.Option(
        None,
        "--include-config",
        "-c",
        help="Include plato-config.yml and flows.yml in snapshot. Auto-enabled for sandboxes started from config.",
    ),
    app_port: int = typer.Option(None, "--app-port", help="Override internal app port"),
    messaging_port: int = typer.Option(None, "--messaging-port", help="Override messaging port"),
    target: str = typer.Option(None, "--target", help="Override target domain (e.g., myapp.web.plato.so)"),
):
    """Create a snapshot of the current sandbox state.

    Captures the current VM state as an artifact that can be submitted for review or
    used as a starting point for future sandboxes. The artifact ID is saved to
    .sandbox.yaml so it can be used by 'plato pm submit base'.

    For sandboxes started from config (-c), automatically includes plato-config.yml and
    flows.yml in the snapshot. For sandboxes started from an artifact, config is inherited
    from the parent.

    Options:
        -j, --json: Output results as JSON instead of formatted text
        -c, --include-config: Force including local plato-config.yml and flows.yml in the
            snapshot. Auto-enabled for sandboxes started from config.
        --app-port: Override the internal application port stored in the artifact
        --messaging-port: Override the Plato messaging port stored in the artifact
        --target: Override the target domain (e.g., myapp.web.plato.so)
    """
    api_key = require_api_key()
    state = require_sandbox_state()
    session_id = require_sandbox_field(state, "session_id")
    mode = state.get("mode", "artifact")
    service_name = state.get("service")

    # Determine whether to include config
    # Auto-enable for "config" mode sandboxes, unless explicitly disabled
    should_include_config = include_config if include_config is not None else (mode == "config")

    if not json_output:
        console.print("[cyan]Creating snapshot...[/cyan]")

    # Build the request with optional config fields
    request_kwargs = {}

    # Get port info from state or CLI overrides
    if app_port is not None:
        request_kwargs["internal_app_port"] = app_port
    elif should_include_config and state.get("app_port"):
        request_kwargs["internal_app_port"] = state.get("app_port")

    if messaging_port is not None:
        request_kwargs["messaging_port"] = messaging_port
    elif should_include_config and state.get("messaging_port"):
        request_kwargs["messaging_port"] = state.get("messaging_port")

    # Set target domain
    if target is not None:
        request_kwargs["target"] = target
    elif should_include_config and service_name:
        request_kwargs["target"] = f"{service_name}.web.plato.so"

    # Include config files if requested
    if should_include_config:
        plato_config_path = state.get("plato_config_path")
        if plato_config_path:
            config_file = Path(plato_config_path)
            if config_file.exists():
                request_kwargs["plato_config"] = config_file.read_text()
                if not json_output:
                    console.print(f"[dim]Including plato-config.yml from {plato_config_path}[/dim]")

            # Also check for flows.yml in same directory
            flows_file = config_file.parent / "flows.yml"
            if not flows_file.exists():
                flows_file = config_file.parent / "base" / "flows.yml"
            if flows_file.exists():
                request_kwargs["flows"] = flows_file.read_text()
                if not json_output:
                    console.print(f"[dim]Including flows.yml from {flows_file}[/dim]")

    if not json_output and request_kwargs:
        console.print(f"[dim]Snapshot config: {list(request_kwargs.keys())}[/dim]")

    try:
        with get_http_client() as client:
            response = sessions_snapshot.sync(
                client=client,
                session_id=session_id,
                body=CreateCheckpointRequest(**request_kwargs),
                x_api_key=api_key,
            )

            # Extract artifact ID from response
            artifact_id = None
            if response and response.results:
                for job_id, result in response.results.items():
                    artifact_id = result.artifact_id if hasattr(result, "artifact_id") else None
                    break

            # Save artifact_id to sandbox state for pm submit base
            if artifact_id:
                state["artifact_id"] = artifact_id
                save_sandbox_state(state)

            if json_output:
                console.print(json.dumps({"artifact_id": artifact_id}))
            else:
                console.print("\n[green]Snapshot created successfully![/green]")
                console.print(f"  [cyan]Artifact ID:[/cyan] {artifact_id}")
                console.print("  [dim]Saved to .sandbox.yaml for 'plato pm submit base'[/dim]")

    except Exception as e:
        if json_output:
            console.print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Failed to create snapshot: {e}[/red]")
        raise typer.Exit(1) from e


@sandbox_app.command(name="stop")
def sandbox_stop():
    """Stop and destroy the current sandbox.

    Terminates the remote VM session, stops the heartbeat background process,
    cleans up local SSH keys created for this sandbox, and removes .sandbox.yaml.
    Run this when you're done with the sandbox or want to start fresh.
    """
    api_key = require_api_key()
    state = require_sandbox_state()
    session_id = require_sandbox_field(state, "session_id")

    console.print("[cyan]Stopping sandbox...[/cyan]")

    try:
        # Stop heartbeat process first
        heartbeat_pid = state.get("heartbeat_pid")
        if heartbeat_pid:
            if _stop_heartbeat_process(heartbeat_pid):
                console.print(f"[dim]Stopped heartbeat process (PID: {heartbeat_pid})[/dim]")
            else:
                console.print(f"[yellow]Could not stop heartbeat process (PID: {heartbeat_pid})[/yellow]")

        with get_http_client() as client:
            sessions_close.sync(
                client=client,
                session_id=session_id,
                x_api_key=api_key,
            )

        # Clean up SSH key files
        ssh_private_key_path = state.get("ssh_private_key_path")

        if ssh_private_key_path:
            private_key_file = Path(ssh_private_key_path)
            public_key_file = Path(ssh_private_key_path + ".pub")
            if private_key_file.exists():
                private_key_file.unlink()
            if public_key_file.exists():
                public_key_file.unlink()
            console.print("[dim]Removed SSH keys[/dim]")

        remove_sandbox_state()
        console.print("[green]Sandbox stopped successfully.[/green]")
        console.print(f"[dim]Removed {SANDBOX_FILE}[/dim]")

    except Exception as e:
        console.print(f"[red]Failed to stop sandbox: {e}[/red]")
        raise typer.Exit(1) from e


@sandbox_app.command(name="connect-network")
def sandbox_connect_network(
    session_id: str = typer.Option(None, "--session", "-s", help="Session ID (uses .sandbox.yaml if not provided)"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Connect all jobs in a session to a WireGuard network.

    Establishes encrypted peer-to-peer networking between VMs in the session,
    allowing SSH access from outside and VM-to-VM communication. Pre-generates
    WireGuard keys, allocates IPs from the session network subnet, and configures
    full mesh networking.

    Options:
        -s, --session: Session ID to connect. If not provided, reads from .sandbox.yaml
        -j, --json: Output results as JSON instead of formatted text
    """
    api_key = require_api_key()

    # Get session ID from argument or .sandbox.yaml
    if session_id is None:
        state = require_sandbox_state()
        session_id = require_sandbox_field(state, "session_id")

    console.print(f"[cyan]Connecting session {session_id} to network...[/cyan]")

    try:
        with get_http_client() as client:
            result = sessions_connect_network.sync(
                client=client,
                session_id=session_id,
                x_api_key=api_key,
            )

        if json_output:
            console.print_json(data=result)
        else:
            # Display results
            statuses = result.get("statuses", {})
            success_count = sum(1 for s in statuses.values() if s.get("success"))
            total_count = len(statuses)

            if success_count == total_count:
                console.print(f"[green]All {total_count} jobs connected to network[/green]")
            else:
                console.print(f"[yellow]{success_count}/{total_count} jobs connected[/yellow]")

            for job_id, status in statuses.items():
                if status.get("success"):
                    wg_ip = status.get("wireguard_ip", "unknown")
                    console.print(f"  [green]✓[/green] {job_id}: {wg_ip}")
                else:
                    error = status.get("error", "unknown error")
                    console.print(f"  [red]✗[/red] {job_id}: {error}")

    except Exception as e:
        console.print(f"[red]Failed to connect network: {e}[/red]")
        raise typer.Exit(1) from e


@sandbox_app.command(name="status")
def sandbox_status(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Show current sandbox status and connection info.

    Displays information from .sandbox.yaml combined with live status from the API.
    Shows session ID, job ID, VM status (running/stopped/etc.), public URL for browser
    access, SSH connection details, network connection status, and heartbeat status.

    Options:
        -j, --json: Output all status info as JSON instead of formatted text
    """
    state = require_sandbox_state()

    # Check VM status via API
    api_key = require_api_key()
    session_id = state.get("session_id")
    vm_status = "unknown"
    vm_status_reason = None
    vm_running = False

    if session_id:
        try:
            with get_http_client() as client:
                details = get_session_details.sync(
                    client=client,
                    session_id=session_id,
                    x_api_key=api_key,
                )
                # Check session status from response - try different possible locations
                if details:
                    # Try top-level status first
                    vm_status = details.get("status")
                    vm_status_reason = details.get("status_reason") or details.get("error") or details.get("message")
                    # Try jobs array (each job has its own status)
                    if not vm_status and "jobs" in details:
                        jobs = details.get("jobs", [])
                        if jobs and len(jobs) > 0:
                            # Get status from first job
                            first_job = jobs[0] if isinstance(jobs, list) else list(jobs.values())[0]
                            if isinstance(first_job, dict):
                                vm_status = first_job.get("status")
                                vm_status_reason = (
                                    first_job.get("status_reason") or first_job.get("error") or first_job.get("message")
                                )
                    # Try envs array
                    if not vm_status and "envs" in details:
                        envs = details.get("envs", [])
                        if envs and len(envs) > 0:
                            first_env = envs[0]
                            if isinstance(first_env, dict):
                                vm_status = first_env.get("status")
                                vm_status_reason = (
                                    first_env.get("status_reason") or first_env.get("error") or first_env.get("message")
                                )
                    # Default if nothing found
                    if not vm_status:
                        vm_status = "active" if details else "unknown"
                    # Common status values: "running", "stopped", "terminated", "pending", "active"
                    vm_running = vm_status.lower() in ("running", "active", "ready", "healthy")
        except Exception:
            vm_status = "unreachable"
            vm_running = False

    if json_output:
        output = {**state, "vm_status": vm_status, "vm_status_reason": vm_status_reason, "vm_running": vm_running}

        # Add heartbeat status to JSON output
        if session_id:
            try:
                with get_http_client() as client:
                    response = client.post(
                        f"/api/v2/sessions/{session_id}/heartbeat",
                        headers={"X-API-Key": api_key},
                    )
                    heartbeat_data = response.json()
                    output["heartbeat"] = {
                        "success": heartbeat_data.get("success", False),
                        "timestamp": heartbeat_data.get("timestamp"),
                        "jobs": {},
                    }
                    for job_id, job_result in heartbeat_data.get("results", {}).items():
                        errors = job_result.get("errors", [])
                        vm_ok = not any("registry_heartbeat_update" in e for e in errors)
                        worker_ok = not any("vm_heartbeat_message" in e for e in errors)
                        output["heartbeat"]["jobs"][job_id] = {
                            "success": job_result.get("success", False),
                            "vm_heartbeat_ok": vm_ok,
                            "worker_heartbeat_ok": worker_ok,
                            "errors": errors,
                        }
            except Exception as e:
                output["heartbeat"] = {"error": str(e)}

        console.print(json.dumps(output))
    else:
        console.print("\n[bold]Sandbox Status[/bold]")
        console.print(f"  [cyan]Session ID:[/cyan]  {state.get('session_id')}")
        console.print(f"  [cyan]Job ID:[/cyan]      {state.get('job_id')}")
        console.print(f"  [cyan]Mode:[/cyan]        {state.get('mode')}")

        # Show VM status with color
        if vm_running:
            console.print(f"  [cyan]VM Status:[/cyan]   [green]{vm_status}[/green]")
        elif vm_status == "unreachable":
            console.print(f"  [cyan]VM Status:[/cyan]   [yellow]{vm_status}[/yellow]")
        else:
            console.print(f"  [cyan]VM Status:[/cyan]   [red]{vm_status}[/red]")

        # Show failure reason if available
        if vm_status_reason:
            console.print(f"  [cyan]Reason:[/cyan]      [red]{vm_status_reason}[/red]")

        if state.get("simulator"):
            console.print(f"  [cyan]Simulator:[/cyan]   {state.get('simulator')}")
        if state.get("service"):
            console.print(f"  [cyan]Service:[/cyan]     {state.get('service')}")
        if state.get("public_url"):
            # Get service name, extracting from simulator if needed (e.g., "docuseal:prod-latest" -> "docuseal")
            service_name = state.get("service")
            if not service_name:
                simulator = state.get("simulator")
                if simulator:
                    service_name = simulator.split(":")[0] if ":" in simulator else simulator
            display_url = format_public_url_with_router_target(state.get("public_url"), service_name)
            console.print(f"  [cyan]Public URL:[/cyan]  {display_url}")
        if state.get("created_at"):
            console.print(f"  [cyan]Created:[/cyan]     {state.get('created_at')}")

        # Display SSH command if available
        ssh_private_key_path = state.get("ssh_private_key_path")
        job_id = state.get("job_id")
        if ssh_private_key_path and job_id:
            console.print("  [cyan]SSH:[/cyan]         plato sandbox ssh")

        # Display network connection status
        if state.get("network_connected"):
            console.print("  [cyan]Network:[/cyan]     [green]connected[/green] (WireGuard)")

        # Display heartbeat process status
        heartbeat_pid = state.get("heartbeat_pid")
        if heartbeat_pid:
            # Check if process is still running
            try:
                os.kill(heartbeat_pid, 0)  # Signal 0 just checks if process exists
                console.print(f"  [cyan]Heartbeat:[/cyan]   [green]running[/green] (PID: {heartbeat_pid})")
            except ProcessLookupError:
                console.print(f"  [cyan]Heartbeat:[/cyan]   [red]stopped[/red] (PID: {heartbeat_pid} not found)")

        # Call heartbeat endpoint and show detailed status
        if session_id:
            console.print("\n[bold]Heartbeat[/bold]")
            try:
                with get_http_client() as client:
                    response = client.post(
                        f"/api/v2/sessions/{session_id}/heartbeat",
                        headers={"X-API-Key": api_key},
                    )
                    hb = response.json()
                    console.print(f"  success: {hb.get('success')}")
                    for job_id, result in hb.get("results", {}).items():
                        console.print(f"  job {job_id[:8]}: success={result.get('success')}")
                        for err in result.get("errors") or []:
                            # Simplify error - just show type
                            if "502" in err:
                                console.print("    worker: 502 (not running)")
                            elif "registry" in err:
                                console.print("    vm: registry update failed")
                            else:
                                console.print(f"    {err[:50]}")
            except Exception as e:
                console.print(f"  error: {e}")


@sandbox_app.command(name="start-worker")
def sandbox_start_worker(
    service: str = typer.Option(
        None,
        "--service",
        "-s",
        help="Service name (defaults to value in .sandbox.yaml)",
    ),
    dataset: str = typer.Option("base", "--dataset", "-d", help="Dataset name"),
    config_path: Path | None = typer.Option(None, "--config-path", help="Path to plato-config.yml"),
    wait: bool = typer.Option(False, "--wait", "-w", help="Wait for worker to be ready (polls state API)"),
    wait_timeout: int = typer.Option(240, "--wait-timeout", help="Timeout in seconds for --wait (default: 240)"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Start the Plato worker in the sandbox.

    The worker is the Plato component that handles flow execution, database audit
    tracking, and state management. It should be started AFTER verifying the login
    flow works manually, since a broken login with an active worker causes error loops.

    Reads the dataset configuration from plato-config.yml to configure the worker
    with the correct services, listeners, and compute settings.

    Options:
        -s, --service: Service name to configure the worker for. Defaults to value in
            .sandbox.yaml if not provided.
        -d, --dataset: Dataset name from plato-config.yml (default: "base")
        --config-path: Path to plato-config.yml. Defaults to current directory.
        -w, --wait: After starting, poll the state API until the worker is ready.
            Useful in scripts to ensure the worker is fully initialized.
        --wait-timeout: Timeout in seconds for --wait (default: 240 seconds)
        -j, --json: Output results as JSON instead of formatted text
    """
    api_key = require_api_key()
    state = require_sandbox_state()
    job_id = state.get("job_id")

    if not job_id:
        console.print("[red].sandbox.yaml missing job_id[/red]")
        raise typer.Exit(1)

    # Use service from state if not provided
    if not service and state.get("service"):
        service = str(state.get("service"))
    if not service:
        console.print("[red]--service is required (or must be set in .sandbox.yaml)[/red]")
        raise typer.Exit(1)

    # Config path is required for start-worker
    if not config_path:
        # Try to find plato-config.yml in current directory
        config_path = Path.cwd() / "plato-config.yml"
        if not config_path.exists():
            config_path = Path.cwd() / "plato-config.yaml"
        if not config_path.exists():
            console.print("[red]--config-path is required or plato-config.yml must exist in current directory[/red]")
            raise typer.Exit(1)
        config_path = Path(config_path)

    config_file = Path(config_path)
    if not config_file.exists():
        console.print(f"[red]Config file not found: {config_file}[/red]")
        raise typer.Exit(1)

    with open(config_file) as f:
        plato_config = yaml.safe_load(f)

    # Extract dataset config
    datasets = plato_config.get("datasets", {})
    if dataset not in datasets:
        console.print(f"[red]Dataset '{dataset}' not found in {config_path}[/red]")
        console.print(f"[yellow]Available datasets: {list(datasets.keys())}[/yellow]")
        raise typer.Exit(1)

    dataset_config_dict = datasets[dataset]

    if not json_output:
        console.print(f"[cyan]Starting worker for service: {service}, dataset: {dataset}[/cyan]")

    try:
        with get_http_client() as client:
            # Extract compute and metadata from config, with defaults
            compute_dict = dataset_config_dict.get("compute", {})
            metadata_dict = dataset_config_dict.get("metadata", {})

            compute = AppSchemasBuildModelsSimConfigCompute(**compute_dict)
            metadata = AppSchemasBuildModelsSimConfigMetadata(**metadata_dict)

            # Also get services and listeners from config
            services_dict = dataset_config_dict.get("services")
            listeners_dict = dataset_config_dict.get("listeners")

            dataset_config = AppSchemasBuildModelsSimConfigDataset(
                compute=compute,
                metadata=metadata,
                services=services_dict,
                listeners=listeners_dict,
            )

            request = VMManagementRequest(
                service=service,
                dataset=dataset,
                plato_dataset_config=dataset_config,
            )

            response = start_worker.sync(
                client=client,
                public_id=job_id,
                body=request,
                x_api_key=api_key,
            )

            if not json_output:
                console.print("[green]Worker started successfully![/green]")

            # Wait for worker to be ready if --wait flag is set
            if wait:
                if not json_output:
                    console.print(f"[cyan]Waiting for worker to be ready (timeout: {wait_timeout}s)...[/cyan]")

                session_id = state.get("session_id")
                if not session_id:
                    console.print("[red]Session ID not found in .sandbox.yaml[/red]")
                    raise typer.Exit(1)
                start_time = time.time()
                poll_interval = 10  # seconds between polls
                worker_ready = False

                while time.time() - start_time < wait_timeout:
                    try:
                        # Try to get state - if it works without error, worker is ready
                        state_response = sessions_state.sync(
                            client=client,
                            session_id=session_id,
                            x_api_key=api_key,
                        )
                        # Check if response has an error (like 502)
                        if state_response and state_response.results:
                            has_error = False
                            for jid, result in state_response.results.items():
                                result_dict = result.model_dump() if hasattr(result, "model_dump") else result
                                if isinstance(result_dict, dict) and "error" in result_dict:
                                    has_error = True
                                    break
                            if not has_error:
                                worker_ready = True
                                break
                    except Exception:
                        pass  # Worker not ready yet

                    elapsed = int(time.time() - start_time)
                    if not json_output:
                        console.print(f"  [dim]Worker not ready yet... ({elapsed}s elapsed)[/dim]")
                    time.sleep(poll_interval)

                if worker_ready:
                    if not json_output:
                        elapsed = int(time.time() - start_time)
                        console.print(f"[green]Worker ready after {elapsed}s![/green]")
                else:
                    if not json_output:
                        console.print(f"[yellow]Warning: Worker not ready after {wait_timeout}s timeout[/yellow]")

            if json_output:
                result = {
                    "status": response.status if hasattr(response, "status") else "ok",
                    "correlation_id": response.correlation_id if hasattr(response, "correlation_id") else None,
                }
                if wait:
                    result["worker_ready"] = worker_ready
                console.print(json.dumps(result))

    except Exception as e:
        if json_output:
            console.print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Failed to start worker: {e}[/red]")
        raise typer.Exit(1) from e


@sandbox_app.command(name="sync")
def sandbox_sync(
    path: str = typer.Argument(".", help="Local path to sync (default: current directory)"),
    remote_path: str = typer.Option(
        None,
        "--remote-path",
        "-r",
        help="Remote path (default: /home/plato/worktree/<service>)",
    ),
    timeout: int = typer.Option(120, "--timeout", "-t", help="Command timeout in seconds"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Sync local files to the sandbox VM.

    Creates a tar archive of local files and uploads it to the remote VM via the
    execute API. Excludes common build artifacts (.git, __pycache__, node_modules,
    .venv, etc.) to reduce transfer size.

    Arguments:
        path: Local path to sync (default: current directory)

    Options:
        -r, --remote-path: Destination path on the VM. Defaults to
            /home/plato/worktree/<service> based on the service in .sandbox.yaml
        -t, --timeout: Command timeout in seconds for the extract operation (default: 120)
        -j, --json: Output results as JSON instead of formatted text
    """
    api_key = require_api_key()
    state = require_sandbox_state()
    session_id = require_sandbox_field(state, "session_id")

    # Get service name for default remote path
    service = state.get("service")
    plato_config_path = state.get("plato_config_path")

    # If service not in state, try to get from plato-config.yml
    if not service and plato_config_path:
        try:
            with open(plato_config_path) as f:
                plato_config = yaml.safe_load(f)
                service = plato_config.get("service")
        except Exception:
            pass  # Optional fallback, continue silently

    # Determine remote path
    if not remote_path:
        if service:
            remote_path = f"/home/plato/worktree/{service}"
        else:
            console.print(
                "[red]Cannot determine remote path. Use --remote-path or ensure .sandbox.yaml has 'service'[/red]"
            )
            raise typer.Exit(1)

    # Resolve local path
    local_path = Path(path).resolve()
    if not local_path.exists():
        console.print(f"[red]Local path not found: {local_path}[/red]")
        raise typer.Exit(1)

    if not json_output:
        console.print(f"[cyan]Local path:[/cyan]  {local_path}")
        console.print(f"[cyan]Remote path:[/cyan] {remote_path}")

    # Patterns to exclude
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        ".git",
        ".venv",
        "venv",
        "node_modules",
        ".sandbox.yaml",
        "*.egg-info",
        ".pytest_cache",
        ".mypy_cache",
        ".DS_Store",
        "*.swp",
        "*.swo",
    ]

    def should_exclude(file_path: Path, base_path: Path) -> bool:
        """Check if a file should be excluded from the archive."""
        rel_path = file_path.relative_to(base_path)

        for pattern in exclude_patterns:
            # Check each part of the path
            for part in rel_path.parts:
                if pattern.startswith("*"):
                    # Wildcard pattern like *.pyc
                    if part.endswith(pattern[1:]):
                        return True
                elif part == pattern:
                    return True
        return False

    if not json_output:
        console.print("[cyan]Creating archive...[/cyan]")

    try:
        # Create tar archive in memory
        tar_buffer = io.BytesIO()
        file_count = 0

        with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
            if local_path.is_file():
                # Single file
                tar.add(local_path, arcname=local_path.name)
                file_count = 1
            else:
                # Directory - walk and add files
                for file_path in local_path.rglob("*"):
                    if file_path.is_file() and not should_exclude(file_path, local_path):
                        arcname = file_path.relative_to(local_path)
                        tar.add(file_path, arcname=str(arcname))
                        file_count += 1

        tar_data = tar_buffer.getvalue()
        tar_size = len(tar_data)

        if not json_output:
            console.print(f"[cyan]Archive size:[/cyan] {tar_size:,} bytes ({file_count} files)")

        # Base64 encode
        tar_b64 = base64.b64encode(tar_data).decode("ascii")

        if not json_output:
            console.print("[cyan]Uploading and extracting...[/cyan]")

        # Execute command to decode and extract on remote
        chunk_size = 50000  # Base64 chars per chunk

        with get_http_client() as client:
            # First, ensure remote directory exists and clean it
            prep_cmd = f"mkdir -p {remote_path} && rm -rf {remote_path}/*"
            prep_request = ExecuteCommandRequest(command=prep_cmd, timeout=30)
            sessions_execute.sync(
                client=client,
                session_id=session_id,
                body=prep_request,
                x_api_key=api_key,
            )

            # Write base64 data to a temp file on remote in chunks
            temp_file = f"/tmp/sync_{session_id[:8]}.tar.gz.b64"

            # Clear temp file first
            clear_cmd = f"rm -f {temp_file}"
            clear_request = ExecuteCommandRequest(command=clear_cmd, timeout=10)
            sessions_execute.sync(
                client=client,
                session_id=session_id,
                body=clear_request,
                x_api_key=api_key,
            )

            # Write chunks
            for i in range(0, len(tar_b64), chunk_size):
                chunk = tar_b64[i : i + chunk_size]
                # Use printf to append chunk (handles special chars better than echo)
                write_cmd = f"printf '%s' '{chunk}' >> {temp_file}"
                write_request = ExecuteCommandRequest(command=write_cmd, timeout=30)
                sessions_execute.sync(
                    client=client,
                    session_id=session_id,
                    body=write_request,
                    x_api_key=api_key,
                )

            # Decode and extract
            extract_cmd = f"base64 -d {temp_file} | tar -xzf - -C {remote_path} && rm -f {temp_file}"
            extract_request = ExecuteCommandRequest(command=extract_cmd, timeout=timeout)
            response = sessions_execute.sync(
                client=client,
                session_id=session_id,
                body=extract_request,
                x_api_key=api_key,
            )

            # Check result
            stderr = ""
            exit_code = 0
            if response and response.results:
                for job_id, result in response.results.items():
                    stderr = result.stderr or ""
                    exit_code = result.exit_code if hasattr(result, "exit_code") else 0
                    break

            if exit_code != 0:
                if json_output:
                    console.print(
                        json.dumps(
                            {
                                "error": f"Extract failed: {stderr}",
                                "exit_code": exit_code,
                            }
                        )
                    )
                else:
                    console.print(f"[red]Sync failed: {stderr}[/red]")
                raise typer.Exit(exit_code)

        if json_output:
            console.print(
                json.dumps(
                    {
                        "status": "ok",
                        "files": file_count,
                        "bytes": tar_size,
                        "remote_path": remote_path,
                    }
                )
            )
        else:
            console.print(f"\n[green]Successfully synced {file_count} files to {remote_path}[/green]")

    except typer.Exit:
        raise
    except Exception as e:
        if json_output:
            console.print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]Sync failed: {e}[/red]")
        raise typer.Exit(1) from e


# Set up Rich logging handler for FlowExecutor
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, show_time=False, show_path=False)],
)
_flow_logger = logging.getLogger("plato.flow")


@sandbox_app.command(name="flow")
def sandbox_flow(
    flow_name: str = typer.Option("login", "--flow-name", "-f", help="Name of the flow to execute"),
    local: bool = typer.Option(False, "--local", "-l", help="Force using local flows.yml only"),
    api: bool = typer.Option(False, "--api", "-a", help="Force fetching flows from API only"),
):
    """Execute a test flow against the running sandbox.

    Runs a named flow (like "login") using Playwright to verify it works correctly.
    Opens a visible browser window, navigates to the sandbox public URL, and executes
    the flow steps automatically. Useful for testing login flows before starting
    the worker.

    By default, looks for flows in local flows.yml (path from plato-config.yml
    metadata.flows_path), then falls back to fetching from the API if the sandbox
    was started from an artifact.

    Options:
        -f, --flow-name: Name of the flow to execute from flows.yml (default: "login")
        -l, --local: Only use local flows.yml file. Errors if not found instead of
            falling back to API.
        -a, --api: Only fetch flows from the API (from the artifact). Ignores any
            local flows.yml file.

    Note: --local and --api are mutually exclusive.
    """
    # Validate mutually exclusive flags
    if local and api:
        console.print("[red]❌ Cannot use both --local and --api[/red]")
        raise typer.Exit(1)

    api_key = require_api_key()
    sandbox_data = require_sandbox_state()
    job_id = sandbox_data.get("job_id")

    # Get service name for router target
    service_name = sandbox_data.get("service")
    if not service_name:
        # Try to extract from simulator (e.g., "docuseal:prod-latest" -> "docuseal")
        simulator = sandbox_data.get("simulator")
        if simulator:
            service_name = simulator.split(":")[0] if ":" in simulator else simulator

    # Get URL from sandbox state
    url = sandbox_data.get("public_url")
    if not url:
        console.print("[red]❌ No public_url found in .sandbox.yaml[/red]")
        raise typer.Exit(1)

    # Ensure URL has router target (in case of older .sandbox.yaml files)
    url = format_public_url_with_router_target(url, service_name)

    # Try to get flows from local plato-config.yml first (unless --api is set)
    flow_obj = None
    flow_file = None
    screenshots_dir = None

    # Check for local plato-config.yml
    plato_config_path = sandbox_data.get("plato_config_path")
    dataset = sandbox_data.get("dataset", "base")

    # Try local config first (either from state or current directory) unless --api forces API
    local_config_paths = []
    if not api:  # Skip local if --api flag is set
        if plato_config_path:
            local_config_paths.append(Path(plato_config_path))
        local_config_paths.extend([Path.cwd() / "plato-config.yml", Path.cwd() / "plato-config.yaml"])

    for config_path in local_config_paths:
        if config_path.exists():
            try:
                plato_config = read_plato_config(str(config_path))
                if "datasets" in plato_config:
                    dataset_config = plato_config["datasets"].get(dataset, {})
                    metadata = dataset_config.get("metadata", {})
                    flows_path = metadata.get("flows_path")

                    if flows_path:
                        if not Path(flows_path).is_absolute():
                            config_dir = config_path.parent
                            flow_file = str(config_dir / flows_path)
                        else:
                            flow_file = flows_path

                        if Path(flow_file).exists():
                            with open(flow_file) as f:
                                flow_dict = yaml.safe_load(f)
                            flow_obj = next(
                                (
                                    Flow.model_validate(fl)
                                    for fl in flow_dict.get("flows", [])
                                    if fl.get("name") == flow_name
                                ),
                                None,
                            )
                            if flow_obj:
                                screenshots_dir = Path(flow_file).parent / "screenshots"
                                console.print(f"[cyan]Flow source: local ({flow_file})[/cyan]")
                                break
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to load flow from {config_path}: {e}[/yellow]")
                pass  # Try next config or fall back to API

    # If no local flow found, fetch from API
    # If no local flow found (or --api forced), fetch from API
    if not flow_obj:
        # If --local was specified and we didn't find a local flow, error out
        if local:
            console.print("[red]❌ No local flow found and --local flag was specified[/red]")
            console.print("[yellow]Ensure plato-config.yml exists with flows_path pointing to flows.yml[/yellow]")
            raise typer.Exit(1)

        if not job_id:
            console.print("[red]❌ No local plato-config.yml found and no job_id in .sandbox.yaml[/red]")
            console.print("[yellow]Either create a local plato-config.yml or start sandbox from an artifact[/yellow]")
            raise typer.Exit(1)

        console.print("[cyan]Flow source: API (fetching from artifact)[/cyan]")
        try:
            with get_http_client() as client:
                flows_response = jobs_get_flows.sync(
                    client=client,
                    job_id=job_id,
                    x_api_key=api_key,
                )

                if not flows_response:
                    console.print("[red]❌ No flows found in artifact[/red]")
                    raise typer.Exit(1)

                # Find the requested flow
                for flow_data in flows_response:
                    if isinstance(flow_data, dict):
                        if flow_data.get("name") == flow_name:
                            flow_obj = Flow.model_validate(flow_data)
                            break
                    elif hasattr(flow_data, "name") and flow_data.name == flow_name:
                        flow_obj = (
                            flow_data if isinstance(flow_data, Flow) else Flow.model_validate(flow_data.model_dump())
                        )
                        break

                if not flow_obj:
                    available_flows = [
                        f.get("name") if isinstance(f, dict) else getattr(f, "name", "?") for f in flows_response
                    ]
                    console.print(f"[red]❌ Flow '{flow_name}' not found in artifact[/red]")
                    console.print(f"[yellow]Available flows: {available_flows}[/yellow]")
                    raise typer.Exit(1)

                # Use temp directory for screenshots when fetching from API
                screenshots_dir = Path.cwd() / "screenshots"
                screenshots_dir.mkdir(exist_ok=True)

        except typer.Exit:
            raise
        except Exception as e:
            console.print(f"[red]❌ Failed to fetch flows from API: {e}[/red]")
            raise typer.Exit(1) from e

    # At this point, url and flow_obj must be set (validated above)
    if not url:
        console.print("[red]❌ URL is not set[/red]")
        raise typer.Exit(1)
    if not flow_obj:
        console.print("[red]❌ Flow object could not be loaded[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]URL: {url}[/cyan]")
    console.print(f"[cyan]Flow name: {flow_name}[/cyan]")

    # Capture for closure (narrowed types)
    _url: str = url
    _flow_obj: Flow = flow_obj

    async def _run():
        from playwright.async_api import async_playwright

        browser = None
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()
                await page.goto(_url)
                executor = FlowExecutor(page, _flow_obj, screenshots_dir, log=_flow_logger)
                await executor.execute()
                console.print("[green]✅ Flow executed successfully[/green]")
        except Exception as e:
            console.print(f"[red]❌ Flow execution failed: {e}[/red]")
            raise typer.Exit(1) from e
        finally:
            if browser:
                await browser.close()

    handle_async(_run())


@sandbox_app.command(name="state")
def sandbox_state_cmd(
    verify_no_mutations: bool = typer.Option(
        False, "--verify-no-mutations", "-v", help="Exit with code 1 if mutations are detected (for CI/automation)"
    ),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Get the database state/mutations from the simulator.

    Queries the worker to show what database changes have been detected since the last
    reset. Displays mutations grouped by table and operation type (INSERT/UPDATE/DELETE).
    Useful for verifying that login flows don't cause unwanted database mutations and
    that the audit system is properly tracking changes.

    Options:
        -v, --verify-no-mutations: Exit with code 1 if any mutations are detected.
            Useful for CI/automation to verify login doesn't cause database changes.
            If mutations are found, the exit code indicates failure.
        -j, --json: Output the full state response as JSON instead of formatted text.
            Includes has_mutations and has_error fields for scripting.
    """
    sandbox_state = require_sandbox_state()
    api_key = require_api_key()

    # Try session_id first (v2 SDK), then job_id, then job_group_id (legacy)
    session_id = sandbox_state.get("session_id")
    job_id = sandbox_state.get("job_id")
    job_group_id = sandbox_state.get("job_group_id")

    state_dict = None
    has_mutations = False
    has_error = False
    error_message = None

    def check_mutations(result_dict: dict) -> tuple[bool, bool, str | None]:
        """Check if result has mutations or errors. Returns (has_mutations, has_error, error_msg)."""
        if isinstance(result_dict, dict):
            # Check for state
            state = result_dict.get("state", {})
            if isinstance(state, dict):
                # Check for error wrapped in state (from API layer transformation)
                if "error" in state:
                    return False, True, state["error"]
                # Check for db state
                db_state = state.get("db", {})
                if isinstance(db_state, dict):
                    mutations = db_state.get("mutations", [])
                    if mutations:
                        return True, False, None
                    # Also check audit_log_count
                    audit_count = db_state.get("audit_log_count", 0)
                    if audit_count > 0:
                        return True, False, None
            # Check top-level mutations as fallback
            mutations = result_dict.get("mutations", [])
            if mutations:
                return True, False, None
        return False, False, None

    all_mutations = []

    if session_id:
        if not json_output:
            console.print(f"[cyan]Getting state for session: {session_id}[/cyan]")
        with get_http_client() as client:
            response = sessions_state.sync(
                client=client,
                session_id=session_id,
                merge_mutations=True,
                x_api_key=api_key,
            )
            if response and response.results:
                state_dict = {
                    jid: result.model_dump() if hasattr(result, "model_dump") else result
                    for jid, result in response.results.items()
                }
                for jid, result in state_dict.items():
                    m, e, msg = check_mutations(result)
                    has_mutations = has_mutations or m
                    has_error = has_error or e
                    if msg:
                        error_message = msg
                    # Extract mutations from state
                    if isinstance(result, dict) and "state" in result:
                        state_data = result.get("state", {})
                        if isinstance(state_data, dict):
                            mutations = state_data.get("mutations", [])
                            if mutations:
                                all_mutations.extend(mutations)
    elif job_id:
        if not json_output:
            console.print(f"[cyan]Getting state for job: {job_id}[/cyan]")
        with get_http_client() as client:
            response = jobs_state.sync(
                client=client,
                job_id=job_id,
                x_api_key=api_key,
            )
            if response:
                state_dict = response.model_dump() if hasattr(response, "model_dump") else response
                m, e, msg = check_mutations(state_dict)
                has_mutations = m
                has_error = e
                error_message = msg
                # Extract mutations from state
                if isinstance(state_dict, dict) and "state" in state_dict:
                    state_data = state_dict.get("state", {})
                    if isinstance(state_data, dict):
                        mutations = state_data.get("mutations", [])
                        if mutations:
                            all_mutations.extend(mutations)
    elif job_group_id:
        if not json_output:
            console.print(f"[cyan]Getting state for job_group: {job_group_id}[/cyan]")
        with get_http_client() as client:
            response = sessions_state.sync(
                client=client,
                session_id=job_group_id,
                merge_mutations=True,
                x_api_key=api_key,
            )
            if response and response.results:
                state_dict = {
                    jid: result.model_dump() if hasattr(result, "model_dump") else result
                    for jid, result in response.results.items()
                }
                for jid, result in state_dict.items():
                    m, e, msg = check_mutations(result)
                    has_mutations = has_mutations or m
                    has_error = has_error or e
                    if msg:
                        error_message = msg
                    # Extract mutations from state
                    if isinstance(result, dict) and "state" in result:
                        state_data = result.get("state", {})
                        if isinstance(state_data, dict):
                            mutations = state_data.get("mutations", [])
                            if mutations:
                                all_mutations.extend(mutations)
    else:
        console.print("[red]❌ .sandbox.yaml missing session_id, job_id, or job_group_id[/red]")
        raise typer.Exit(1)

    # Output results
    if json_output:
        result = {
            "state": state_dict,
            "has_mutations": has_mutations,
            "has_error": has_error,
        }
        if error_message:
            result["error"] = error_message
        console.print(json.dumps(result, indent=2, default=str))
    else:
        if has_error:
            console.print(f"\n[red]Error getting state:[/red] {error_message}")
        elif state_dict:
            console.print("\n[bold]Environment State:[/bold]")
            console.print(json.dumps(state_dict, indent=2, default=str))

            # Display mutations if any
            if all_mutations:
                console.print(f"\n[bold red]Mutations ({len(all_mutations)}):[/bold red]")
                # Group by table and action for summary
                from collections import defaultdict

                table_ops: dict[str, dict[str, int]] = defaultdict(lambda: {"INSERT": 0, "UPDATE": 0, "DELETE": 0})
                for mutation in all_mutations:
                    table = mutation.get("table_name", mutation.get("table", "unknown"))
                    op = mutation.get("action", mutation.get("operation", "UNKNOWN")).upper()
                    if op in table_ops[table]:
                        table_ops[table][op] += 1

                console.print("\n  [dim]Table                           INSERT  UPDATE  DELETE[/dim]")
                console.print("  [dim]───────────────────────────────────────────────────────[/dim]")
                for table, ops in sorted(table_ops.items(), key=lambda x: sum(x[1].values()), reverse=True):
                    console.print(f"  {table:<30} {ops['INSERT']:>6}  {ops['UPDATE']:>6}  {ops['DELETE']:>6}")
            else:
                console.print("\n[green]No mutations recorded[/green]")
        else:
            console.print("[yellow]No state returned[/yellow]")

        # Summary for verify mode
        if verify_no_mutations:
            if has_error:
                console.print("\n[red]❌ Error checking state - worker may not be ready[/red]")
            elif has_mutations:
                console.print("\n[red]❌ FAIL: Mutations detected after login![/red]")
                console.print(
                    "[yellow]Fix: Add affected tables/columns to audit_ignore_tables in plato-config.yml[/yellow]"
                )
            else:
                console.print("\n[green]✅ PASS: No mutations detected[/green]")

    # Exit with error code if verify mode and mutations/errors found
    if verify_no_mutations and (has_mutations or has_error):
        raise typer.Exit(1)


@sandbox_app.command(name="clear-audit")
def sandbox_clear_audit(
    config_path: Path | None = typer.Option(None, "--config-path", help="Path to plato-config.yml"),
    dataset: str = typer.Option("base", "--dataset", "-d", help="Dataset name"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Clear the audit_log table(s) in the sandbox database.

    Truncates all audit_log tables to reset mutation tracking. Use this after initial
    setup or login has generated expected mutations, so you can verify that subsequent
    login flows don't create new mutations.

    Reads database connection info from plato-config.yml listeners and executes the
    appropriate SQL (PostgreSQL TRUNCATE or MySQL DELETE) via SSH to the sandbox VM.

    Options:
        --config-path: Path to plato-config.yml file (default: looks in current directory)
        -d, --dataset: Dataset name to read listener configuration from (default: "base")
        -j, --json: Output results as JSON instead of formatted text
    """
    state = require_sandbox_state()
    job_id = state.get("job_id")

    if not job_id:
        console.print("[red]❌ No job_id found in .sandbox.yaml[/red]")
        raise typer.Exit(1)

    # Find plato-config.yml
    if not config_path:
        config_path = Path.cwd() / "plato-config.yml"
        if not config_path.exists():
            config_path = Path.cwd() / "plato-config.yaml"
        if not config_path.exists():
            console.print("[red]❌ plato-config.yml not found[/red]")
            raise typer.Exit(1)

    with open(config_path) as f:
        plato_config = yaml.safe_load(f)

    # Get dataset config
    datasets = plato_config.get("datasets", {})
    if dataset not in datasets:
        console.print(f"[red]❌ Dataset '{dataset}' not found[/red]")
        raise typer.Exit(1)

    dataset_config = datasets[dataset]
    listeners = dataset_config.get("listeners", {})

    # Find DB listeners
    db_listeners = []
    for name, listener in listeners.items():
        if isinstance(listener, dict) and listener.get("type") == "db":
            db_listeners.append((name, listener))

    if not db_listeners:
        console.print("[red]❌ No database listeners found in plato-config.yml[/red]")
        console.print("[yellow]Expected: datasets.<dataset>.listeners.<name>.type = 'db'[/yellow]")
        raise typer.Exit(1)

    results = []

    def _execute_db_cleanup(name: str, db_config: dict, local_port: int) -> dict:
        """Execute DB cleanup using sync SQLAlchemy (called after tunnel is up)."""
        db_type = db_config.get("db_type", "postgresql").lower()
        db_user = db_config.get("db_user", "postgres" if db_type == "postgresql" else "root")
        db_password = db_config.get("db_password", "")
        db_database = db_config.get("db_database", "postgres")

        # Build SQLAlchemy URL based on db_type (sync drivers)
        user = quote_plus(db_user)
        password = quote_plus(db_password)
        database = quote_plus(db_database)

        if db_type == "postgresql":
            db_url = f"postgresql+psycopg2://{user}:{password}@127.0.0.1:{local_port}/{database}"
        elif db_type in ("mysql", "mariadb"):
            db_url = f"mysql+pymysql://{user}:{password}@127.0.0.1:{local_port}/{database}"
        else:
            return {"listener": name, "success": False, "error": f"Unsupported db_type: {db_type}"}

        engine = create_engine(db_url, pool_pre_ping=True)
        tables_truncated = []

        with engine.begin() as conn:
            if db_type == "postgresql":
                # Find and truncate audit_log tables in all schemas
                result = conn.execute(text("SELECT schemaname, tablename FROM pg_tables WHERE tablename = 'audit_log'"))
                tables = result.fetchall()
                for schema, table in tables:
                    conn.execute(text(f"TRUNCATE TABLE {schema}.{table} RESTART IDENTITY CASCADE"))
                    tables_truncated.append(f"{schema}.{table}")

            elif db_type in ("mysql", "mariadb"):
                # Find and delete from audit_log tables
                result = conn.execute(
                    text(
                        "SELECT table_schema, table_name FROM information_schema.tables "
                        "WHERE table_name = 'audit_log' AND table_schema = DATABASE()"
                    )
                )
                tables = result.fetchall()
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
                for schema, table in tables:
                    conn.execute(text(f"DELETE FROM `{table}`"))
                    tables_truncated.append(table)
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        engine.dispose()
        return {"listener": name, "success": True, "tables_truncated": tables_truncated}

    async def clear_audit_via_tunnel(name: str, db_config: dict) -> dict:
        """Clear audit_log by connecting via proxy tunnel."""
        db_type = db_config.get("db_type", "postgresql").lower()
        db_port = db_config.get("db_port", 5432 if db_type == "postgresql" else 3306)

        if not json_output:
            console.print(f"[cyan]Clearing audit_log for listener '{name}' ({db_type})...[/cyan]")

        # Find a free local port for the tunnel
        local_port = find_free_port()

        # Create tunnel and connect
        tunnel = ProxyTunnel(
            env_id=job_id,
            db_port=db_port,
            temp_password="newpass",
            host_port=local_port,
        )

        try:
            await tunnel.start()

            # Run sync DB cleanup in a thread to avoid blocking the event loop
            result = await asyncio.to_thread(_execute_db_cleanup, name, db_config, local_port)

            if result["success"]:
                tables_truncated = result.get("tables_truncated", [])
                if not json_output:
                    console.print(f"[green]✅ Cleared audit_log for '{name}' ({len(tables_truncated)} tables)[/green]")
            return result

        except Exception as e:
            if not json_output:
                console.print(f"[red]❌ Failed to clear audit_log for '{name}': {e}[/red]")
            return {"listener": name, "success": False, "error": str(e)}
        finally:
            await tunnel.stop()

    # Run async cleanup for each listener
    async def run_all():
        tasks = [clear_audit_via_tunnel(name, db_config) for name, db_config in db_listeners]
        return await asyncio.gather(*tasks)

    results = asyncio.run(run_all())

    # Call state API to refresh in-memory mutation cache
    session_id = state.get("session_id")
    api_key = require_api_key()
    if session_id:
        if not json_output:
            console.print("[dim]Refreshing state cache...[/dim]")
        try:
            with get_http_client() as client:
                sessions_state.sync(
                    client=client,
                    session_id=session_id,
                    x_api_key=api_key,
                )
        except Exception as e:
            if not json_output:
                console.print(f"[yellow]⚠ Failed to refresh state cache: {e}[/yellow]")

    if json_output:
        console.print(json.dumps({"results": results}))
    else:
        # Summary
        success_count = sum(1 for r in results if r["success"])
        total = len(results)
        if success_count == total:
            console.print(f"\n[green]✅ All {total} audit logs cleared successfully[/green]")
        else:
            console.print(f"\n[yellow]⚠ {success_count}/{total} audit logs cleared[/yellow]")
            raise typer.Exit(1)


@sandbox_app.command(name="audit-ui")
def sandbox_audit_ui():
    """Launch Streamlit UI for configuring database audit rules.

    Opens a visual web interface to help configure audit_ignore_tables in plato-config.yml.
    The UI shows database tables and their recent mutations, making it easy to identify
    which tables or columns should be ignored (like session tables, last_login timestamps,
    etc. that change on every login).

    Requires streamlit and database drivers to be installed:
        pip install streamlit psycopg2-binary pymysql
    """
    # Check if streamlit is installed
    if not shutil.which("streamlit"):
        console.print("[red]❌ streamlit is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install streamlit psycopg2-binary pymysql")
        raise typer.Exit(1)

    # Find the audit_ui.py file - go up from cli/ to v1/
    package_dir = Path(__file__).resolve().parent.parent
    ui_file = package_dir / "audit_ui.py"

    if not ui_file.exists():
        console.print(f"[red]❌ UI file not found: {ui_file}[/red]")
        raise typer.Exit(1)

    console.print("[cyan]Launching Streamlit UI...[/cyan]")

    try:
        # Launch streamlit
        os.execvp("streamlit", ["streamlit", "run", str(ui_file)])
    except Exception as e:
        console.print(f"[red]❌ Failed to launch Streamlit: {e}[/red]")
        raise typer.Exit(1) from e


def _copy_files_respecting_gitignore(src_dir: Path, dst_dir: Path) -> None:
    """Copy files from src to dst, skipping .git/ and .plato-hub.json.

    Note: This function intentionally does NOT respect .gitignore because
    start-services needs to copy all workspace files to the VM, including
    config files that might be gitignored locally (like docker-compose.yml
    in a 'base/' directory).
    """

    def should_skip(rel_path: Path) -> bool:
        """Check if path should be skipped."""
        parts = rel_path.parts
        # Skip anything inside .git/ directory
        if ".git" in parts:
            return True
        # Skip .plato-hub.json
        if rel_path.name == ".plato-hub.json":
            return True
        return False

    # Walk through source directory
    for src_path in src_dir.rglob("*"):
        rel_path = src_path.relative_to(src_dir)

        # Skip root
        if str(rel_path) == ".":
            continue

        # Check if should skip
        if should_skip(rel_path):
            continue

        dst_path = dst_dir / rel_path

        if src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
        else:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)


def _run_ssh_command(ssh_config_path: str, ssh_host: str, command: str) -> tuple[int, str, str]:
    """Run a command on the remote VM via SSH."""
    result = subprocess.run(
        ["ssh", "-F", ssh_config_path, ssh_host, command],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def _start_heartbeat_process(session_id: str, api_key: str) -> int | None:
    """Start a background process that sends heartbeats to keep the session alive.

    Returns the PID of the background process, or None if failed.
    """
    # Log file for heartbeat debugging
    log_file = f"/tmp/plato_heartbeat_{session_id}.log"

    # Python script to run in background
    heartbeat_script = f'''
import time
import os
import httpx
from datetime import datetime

session_id = "{session_id}"
api_key = "{api_key}"
base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
log_file = "{log_file}"

def log(msg):
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"[{{timestamp}}] {{msg}}\\n")
        f.flush()

log(f"Heartbeat process started for session {{session_id}}")
log(f"Base URL: {{base_url}}")

heartbeat_count = 0
while True:
    heartbeat_count += 1
    try:
        with httpx.Client(base_url=base_url, timeout=30) as client:
            # base_url already includes /api, so just use /v2/...
            response = client.post(
                f"/v2/sessions/{{session_id}}/heartbeat",
                headers={{"X-API-Key": api_key}},
            )
            result = response.json()
            success = result.get("success", False)
            log(f"Heartbeat #{{heartbeat_count}}: status={{response.status_code}}, success={{success}}")
            if not success:
                results = result.get("results", {{}})
                for job_id, job_result in results.items():
                    errors = job_result.get("errors", [])
                    if errors:
                        log(f"  Job {{job_id}} errors: {{errors}}")
    except Exception as e:
        log(f"Heartbeat #{{heartbeat_count}} EXCEPTION: {{type(e).__name__}}: {{e}}")
    time.sleep(30)
'''

    try:
        # Start detached background process
        process = subprocess.Popen(
            ["python3", "-c", heartbeat_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,  # Detach from parent process
        )
        return process.pid
    except Exception:
        return None


def _stop_heartbeat_process(pid: int) -> bool:
    """Stop the heartbeat background process.

    Returns True if successfully stopped, False otherwise.
    """
    import signal

    try:
        os.kill(pid, signal.SIGTERM)
        return True
    except ProcessLookupError:
        # Process already dead
        return True
    except Exception:
        return False


@sandbox_app.command(name="start-services")
def sandbox_start_services(
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Deploy and start docker compose services on the sandbox.

    Syncs your local code to the sandbox VM and starts containers. The process:
    1. Gets Gitea credentials and pushes local code to a new branch on Plato Hub
    2. Clones the code on the VM via SSH
    3. Runs 'docker compose up -d' for each docker-compose service defined in
       the plato-config.yml services section

    Run this command again after making local changes to re-sync and restart containers.
    Requires SSH to be configured (network is enabled by default).

    Options:
        -j, --json: Output results as JSON instead of formatted text. Includes
            branch name, repo URL, VM path, and list of services started.
    """
    api_key = require_api_key()
    state = require_sandbox_state()

    # Get required state
    ssh_host = state.get("ssh_host")
    ssh_config_path = state.get("ssh_config_path")
    service_name = state.get("service")

    if not ssh_host or not ssh_config_path:
        console.print("[red]❌ SSH not configured. Did you run 'plato sandbox start --from-config'?[/red]")
        raise typer.Exit(1)

    if not service_name:
        console.print("[red]❌ Service name not found in .sandbox.yaml[/red]")
        raise typer.Exit(1)

    # Load plato-config.yml to get services
    plato_config_path = state.get("plato_config_path")
    if not plato_config_path or not Path(plato_config_path).exists():
        # Try current directory
        for candidate in ["plato-config.yml", "plato-config.yaml"]:
            if Path(candidate).exists():
                plato_config_path = candidate
                break

    if not plato_config_path or not Path(plato_config_path).exists():
        console.print("[red]❌ plato-config.yml not found[/red]")
        raise typer.Exit(1)

    with open(plato_config_path) as f:
        plato_config = yaml.safe_load(f)

    dataset_name = state.get("dataset", "base")
    dataset_config = plato_config.get("datasets", {}).get(dataset_name, {})
    services_config = dataset_config.get("services", {})

    if not services_config:
        console.print(f"[yellow]⚠ No services defined in dataset '{dataset_name}'[/yellow]")

    try:
        with get_http_client() as client:

            def start_services_on_vm(repo_dir: str) -> list[dict[str, str]]:
                """Start docker compose services on the VM."""
                services_started: list[dict[str, str]] = []
                for svc_name, svc_config in services_config.items():
                    svc_type = svc_config.get("type", "")
                    if svc_type == "docker-compose":
                        compose_file = svc_config.get("file", "docker-compose.yml")
                        compose_cmd = f"cd {repo_dir} && docker compose -f {compose_file} up -d"

                        if not json_output:
                            console.print(f"[cyan]  Starting docker compose service: {svc_name}...[/cyan]")

                        ret, stdout, stderr = _run_ssh_command(ssh_config_path, ssh_host, compose_cmd)
                        if ret != 0:
                            console.print(f"[red]❌ Failed to start service '{svc_name}': {stderr}[/red]")
                            raise typer.Exit(1)

                        services_started.append({"name": svc_name, "type": "docker-compose", "file": compose_file})
                        if not json_output:
                            console.print(f"[green]  ✓ Started docker compose service: {svc_name}[/green]")
                    else:
                        if not json_output:
                            console.print(
                                f"[yellow]  ⚠ Skipped service '{svc_name}' (unknown type: {svc_type})[/yellow]"
                            )
                return services_started

            # Step 1: Get Gitea credentials
            if not json_output:
                console.print("[cyan]Step 1: Getting Gitea credentials...[/cyan]")

            creds = get_gitea_credentials.sync(client=client, x_api_key=api_key)

            # Step 2: Find simulator
            if not json_output:
                console.print(f"[cyan]Step 2: Finding simulator '{service_name}'...[/cyan]")

            simulators = get_accessible_simulators.sync(client=client, x_api_key=api_key)
            simulator = None
            for sim in simulators:
                sim_name = sim.get("name") if isinstance(sim, dict) else getattr(sim, "name", None)
                if sim_name and sim_name.lower() == service_name.lower():
                    simulator = sim
                    break

            if not simulator:
                console.print(f"[red]❌ Simulator '{service_name}' not found in hub[/red]")
                raise typer.Exit(1)

            sim_id = simulator.get("id") if isinstance(simulator, dict) else getattr(simulator, "id", None)
            has_repo = (
                simulator.get("has_repo") if isinstance(simulator, dict) else getattr(simulator, "has_repo", False)
            )

            # Step 3: Get or create repository
            if not json_output:
                console.print("[cyan]Step 3: Getting/creating repository...[/cyan]")

            if sim_id is None:
                console.print("[red]❌ Simulator ID not available[/red]")
                raise typer.Exit(1)

            if has_repo:
                repo = get_simulator_repository.sync(client=client, simulator_id=sim_id, x_api_key=api_key)
            else:
                repo = create_simulator_repository.sync(client=client, simulator_id=sim_id, x_api_key=api_key)

            clone_url = repo.clone_url
            if not clone_url:
                console.print("[red]❌ Repository clone URL not available[/red]")
                raise typer.Exit(1)

            # Build authenticated clone URL with URL-encoded credentials
            if clone_url.startswith("https://"):
                encoded_username = quote(creds.username, safe="")
                encoded_password = quote(creds.password, safe="")
                auth_clone_url = clone_url.replace("https://", f"https://{encoded_username}:{encoded_password}@", 1)
            else:
                auth_clone_url = clone_url

            # Step 4: Clone to temp directory and push
            if not json_output:
                console.print("[cyan]Step 4: Pushing code to hub...[/cyan]")

            repo_dir = f"/home/plato/worktree/{service_name}"

            with tempfile.TemporaryDirectory(prefix="plato-hub-") as temp_dir:
                temp_repo = Path(temp_dir) / "repo"

                # Set up git environment to avoid credential helpers interfering
                git_env = os.environ.copy()
                git_env["GIT_TERMINAL_PROMPT"] = "0"
                git_env["GIT_ASKPASS"] = ""

                # Clone the repo
                result = subprocess.run(
                    ["git", "clone", auth_clone_url, str(temp_repo)],
                    capture_output=True,
                    text=True,
                    env=git_env,
                )
                if result.returncode != 0:
                    console.print(f"[red]❌ Failed to clone repo: {result.stderr}[/red]")
                    raise typer.Exit(1)

                # Create and checkout new branch
                branch_name = f"workspace-{int(time.time())}"
                result = subprocess.run(
                    ["git", "checkout", "-b", branch_name],
                    cwd=temp_repo,
                    capture_output=True,
                    text=True,
                    env=git_env,
                )
                if result.returncode != 0:
                    console.print(f"[red]❌ Failed to create branch: {result.stderr}[/red]")
                    raise typer.Exit(1)

                # Copy files respecting .gitignore
                current_dir = Path.cwd()
                _copy_files_respecting_gitignore(current_dir, temp_repo)

                # Git add
                subprocess.run(["git", "add", "."], cwd=temp_repo, capture_output=True, env=git_env)

                # Check for changes
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    cwd=temp_repo,
                    capture_output=True,
                    text=True,
                    env=git_env,
                )

                if result.stdout.strip():
                    # Commit changes
                    subprocess.run(
                        ["git", "commit", "-m", "Sync from local workspace"],
                        cwd=temp_repo,
                        capture_output=True,
                        env=git_env,
                    )

                # Set the remote URL with credentials explicitly for push
                subprocess.run(
                    ["git", "remote", "set-url", "origin", auth_clone_url],
                    cwd=temp_repo,
                    capture_output=True,
                    env=git_env,
                )

                # Push the branch
                result = subprocess.run(
                    ["git", "push", "-u", "origin", branch_name],
                    cwd=temp_repo,
                    capture_output=True,
                    text=True,
                    env=git_env,
                )
                if result.returncode != 0:
                    console.print(f"[red]❌ Failed to push: {result.stderr}[/red]")
                    raise typer.Exit(1)

            if not json_output:
                console.print(f"[green]✓ Code pushed to branch: {branch_name}[/green]")

            # Step 5: Clone repo on VM via SSH
            if not json_output:
                console.print("[cyan]Step 5: Cloning repo on VM...[/cyan]")

            # Create worktree directory
            _run_ssh_command(ssh_config_path, ssh_host, "mkdir -p /home/plato/worktree")

            # Remove existing directory
            _run_ssh_command(ssh_config_path, ssh_host, f"rm -rf {repo_dir}")

            # Clone on VM
            clone_cmd = f"git clone -b {branch_name} {auth_clone_url} {repo_dir}"
            ret, stdout, stderr = _run_ssh_command(ssh_config_path, ssh_host, clone_cmd)
            if ret != 0:
                console.print(f"[red]❌ Failed to clone on VM: {stderr}[/red]")
                raise typer.Exit(1)

            if not json_output:
                console.print(f"[green]✓ Code cloned to {repo_dir}[/green]")

            # Step 6: Authenticate ECR
            if not json_output:
                console.print("[cyan]Step 6: Authenticating Docker with ECR...[/cyan]")

            ecr_registry = "383806609161.dkr.ecr.us-west-1.amazonaws.com"
            ecr_token_result = subprocess.run(
                ["aws", "ecr", "get-login-password", "--region", "us-west-1"],
                capture_output=True,
                text=True,
            )
            if ecr_token_result.returncode != 0:
                console.print(f"[red]❌ Failed to get ECR token: {ecr_token_result.stderr}[/red]")
                raise typer.Exit(1)

            ecr_token = ecr_token_result.stdout.strip()
            docker_login_cmd = f"echo '{ecr_token}' | docker login --username AWS --password-stdin {ecr_registry}"
            ret, stdout, stderr = _run_ssh_command(ssh_config_path, ssh_host, docker_login_cmd)
            if ret != 0:
                console.print(f"[red]❌ Failed to authenticate Docker with ECR: {stderr}[/red]")
                raise typer.Exit(1)

            if not json_output:
                console.print("[green]✓ Docker authenticated with ECR[/green]")

            # Step 7: Start services
            if not json_output:
                console.print("[cyan]Step 7: Starting services...[/cyan]")

            services_started = start_services_on_vm(repo_dir)

            # Output results
            if json_output:
                console.print(
                    json.dumps(
                        {
                            "status": "ok",
                            "branch": branch_name,
                            "repo_url": clone_url,
                            "vm_path": repo_dir,
                            "services_started": services_started,
                        }
                    )
                )
            else:
                console.print("\n[green]✅ Services started successfully![/green]")
                console.print(f"  [cyan]Branch:[/cyan]  {branch_name}")
                console.print(f"  [cyan]VM Path:[/cyan] {repo_dir}")

    except typer.Exit:
        raise
    except Exception as e:
        if json_output:
            console.print(json.dumps({"error": str(e)}))
        else:
            console.print(f"[red]❌ Failed to start services: {e}[/red]")
        raise typer.Exit(1) from e
