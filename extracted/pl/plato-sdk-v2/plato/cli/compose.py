"""Plato Compose - Run docker compose across multiple Firecracker VMs.

This module provides CLI commands to:
1. Parse docker-compose files with x-plato annotations
2. Validate VM groupings and configurations
3. Create VMs for each service group
4. Run docker compose services on the appropriate VMs
5. Set up internal networking between VMs
6. Sync local build contexts and volumes via rsync
7. Save/restore VM snapshots for fast iteration
"""

import asyncio
import logging
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Annotated

import typer
import yaml
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from plato.v2 import AsyncPlato, Env
from plato.v2.async_.environment import Environment
from plato.v2.types import SimConfigCompute

GATEWAY_HOST = os.getenv("PLATO_GATEWAY_HOST", "gateway.plato.so")


def parse_gitignore(gitignore_path: Path) -> list[str]:
    """Parse .gitignore file and return list of patterns for rsync --exclude."""
    if not gitignore_path.exists():
        return [".git"]  # Always exclude .git

    patterns = [".git"]  # Always exclude .git
    with open(gitignore_path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Skip negation patterns (rsync doesn't handle these the same way)
            if line.startswith("!"):
                continue
            patterns.append(line)
    return patterns


# Suppress httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
console = Console()

app = typer.Typer(help="Run docker compose across multiple Firecracker VMs")


# =============================================================================
# Models
# =============================================================================


class ValidationError(BaseModel):
    """A validation error or warning."""

    level: str  # "error" or "warning"
    service: str
    message: str


class VMConfig(BaseModel):
    """Configuration for a VM group."""

    name: str
    memory: int  # in MB
    cpus: int = 1
    snapshot: str = "disk"  # "disk" or "memory"
    services: list[str] = Field(default_factory=list)


class PlatoComposeConfig(BaseModel):
    """Parsed x-plato configuration from docker-compose file."""

    vms: dict[str, VMConfig] = Field(default_factory=dict)
    compose_file: Path
    compose_content: dict
    errors: list[ValidationError] = Field(default_factory=list)
    warnings: list[ValidationError] = Field(default_factory=list)
    ignore_paths: list[str] = Field(default_factory=list)  # Paths to exclude from rsync
    name: str = "compose"  # Stack name used for simulator naming in snapshots


# =============================================================================
# Parsing
# =============================================================================


def parse_memory(memory_str: str) -> int:
    """Parse memory string like '2GB' or '512MB' to MB."""
    memory_str = memory_str.strip().upper()
    match = re.match(r"^(\d+(?:\.\d+)?)\s*(GB|MB|G|M)?$", memory_str)
    if not match:
        raise ValueError(f"Invalid memory format: {memory_str}")

    value = float(match.group(1))
    unit = match.group(2) or "MB"

    if unit in ("GB", "G"):
        return int(value * 1024)
    return int(value)


def parse_compose_file(compose_path: Path) -> PlatoComposeConfig:
    """Parse a docker-compose file and extract x-plato configuration."""

    if not compose_path.exists():
        raise FileNotFoundError(f"Compose file not found: {compose_path}")

    with open(compose_path) as f:
        compose = yaml.safe_load(f)

    if not compose:
        raise ValueError("Empty compose file")

    services = compose.get("services", {})
    if not services:
        raise ValueError("No services defined in compose file")

    # Get global x-plato config
    global_plato = compose.get("x-plato", {})
    vm_configs_raw = global_plato.get("services", {})
    ignore_paths = global_plato.get("ignore", [])
    stack_name = global_plato.get("name", "compose")  # Stack name for simulator naming

    # Build VM configs
    vms: dict[str, VMConfig] = {}

    # First, create VM configs from global x-plato.services
    for vm_name, vm_config in vm_configs_raw.items():
        memory = parse_memory(vm_config.get("memory", "2GB"))
        cpus = vm_config.get("cpus", 1)
        snapshot = vm_config.get("snapshot", "disk")

        if snapshot not in ("disk", "memory"):
            raise ValueError(f"Invalid snapshot type for {vm_name}: {snapshot}")

        vms[vm_name] = VMConfig(
            name=vm_name,
            memory=memory,
            cpus=cpus,
            snapshot=snapshot,
        )

    # Now assign services to VMs
    for service_name, service_config in services.items():
        plato_config = service_config.get("x-plato", {})
        vm_name = plato_config.get("service")

        if not vm_name:
            raise ValueError(f"Service '{service_name}' missing x-plato.service annotation")

        # Create VM config if not defined in global x-plato.services
        if vm_name not in vms:
            vms[vm_name] = VMConfig(
                name=vm_name,
                memory=2048,  # 2GB default
                cpus=1,
                snapshot="disk",
            )

        vms[vm_name].services.append(service_name)

    config = PlatoComposeConfig(
        vms=vms,
        compose_file=compose_path,
        compose_content=compose,
        ignore_paths=ignore_paths,
        name=stack_name,
    )

    # Run validation
    validate_config(config, services)

    return config


def validate_config(config: PlatoComposeConfig, services: dict) -> None:
    """Validate the parsed configuration for common issues."""

    errors = config.errors
    warnings = config.warnings

    # Build service -> VM mapping
    service_to_vm: dict[str, str] = {}
    for vm_name, vm_config in config.vms.items():
        for svc in vm_config.services:
            service_to_vm[svc] = vm_name

    # Track volumes used by each VM
    vm_volumes: dict[str, set[str]] = {vm: set() for vm in config.vms}

    # If only one VM, skip cross-VM validation
    single_vm = len(config.vms) == 1

    for service_name, service_config in services.items():
        vm_name = service_to_vm.get(service_name)
        if not vm_name:
            continue

        # ---------------------------------------------------------------------
        # Check 1: Port exposure
        # ---------------------------------------------------------------------
        exposed_ports = set()

        # Collect from 'ports'
        for port in service_config.get("ports", []):
            if isinstance(port, str):
                # Format: "host:container" or "container"
                parts = str(port).replace("/tcp", "").replace("/udp", "").split(":")
                container_port = int(parts[-1].split("-")[0])
                exposed_ports.add(container_port)
            elif isinstance(port, dict):
                exposed_ports.add(port.get("target", 0))
            elif isinstance(port, int):
                exposed_ports.add(port)

        # Collect from 'expose'
        for port in service_config.get("expose", []):
            exposed_ports.add(int(str(port).replace("/tcp", "").replace("/udp", "")))

        # Only warn if NO ports are exposed at all (not about specific missing ports)
        # Services often use non-standard ports, so we shouldn't be prescriptive
        if not exposed_ports and not service_config.get("network_mode") and not service_config.get("build"):
            # Only warn for image-based services with no ports
            # Build-based services might expose ports dynamically
            warnings.append(
                ValidationError(
                    level="warning",
                    service=service_name,
                    message="No ports exposed. Service won't be accessible from other VMs via .plato.internal",
                )
            )

        # ---------------------------------------------------------------------
        # Check 2: Volume sharing across VMs
        # ---------------------------------------------------------------------
        for volume in service_config.get("volumes", []):
            vol_str = str(volume) if isinstance(volume, str) else volume.get("source", "")

            # Named volume (doesn't start with / or .)
            if vol_str and not vol_str.startswith("/") and not vol_str.startswith("."):
                vol_name = vol_str.split(":")[0]
                vm_volumes[vm_name].add(vol_name)

            # Bind mounts are synced via rsync, so no warning needed
            # They'll be available on the VM after sync

        # Cross-VM depends_on is handled by plato compose - we wait for
        # healthchecks on dependent VMs before starting services

        # ---------------------------------------------------------------------
        # Check 4: network_mode issues (only if multiple VMs)
        # ---------------------------------------------------------------------
        if not single_vm:
            network_mode = service_config.get("network_mode", "")
            if network_mode.startswith("service:"):
                ref_service = network_mode.replace("service:", "")
                ref_vm = service_to_vm.get(ref_service)
                if ref_vm and ref_vm != vm_name:
                    errors.append(
                        ValidationError(
                            level="error",
                            service=service_name,
                            message=f"network_mode 'service:{ref_service}' references a service in a different VM ({ref_vm}). "
                            "This won't work. Services sharing network_mode must be in the same VM.",
                        )
                    )

            # -----------------------------------------------------------------
            # Check 5: links (deprecated but still used)
            # -----------------------------------------------------------------
            for link in service_config.get("links", []):
                link_service = link.split(":")[0]
                link_vm = service_to_vm.get(link_service)
                if link_vm and link_vm != vm_name:
                    errors.append(
                        ValidationError(
                            level="error",
                            service=service_name,
                            message=f"links to '{link_service}' which is in a different VM ({link_vm}). "
                            "Links don't work across VMs. Use {service}.plato.internal instead.",
                        )
                    )

    # ---------------------------------------------------------------------
    # Check 6: Named volumes shared across VMs (only if multiple VMs)
    # ---------------------------------------------------------------------
    if not single_vm:
        all_volumes: dict[str, list[str]] = {}
        for vm_name, volumes in vm_volumes.items():
            for vol in volumes:
                if vol not in all_volumes:
                    all_volumes[vol] = []
                all_volumes[vol].append(vm_name)

        for vol_name, vms_using in all_volumes.items():
            if len(vms_using) > 1:
                errors.append(
                    ValidationError(
                        level="error",
                        service="(global)",
                        message=f"Named volume '{vol_name}' is used by services in multiple VMs: {', '.join(vms_using)}. "
                        "Volumes cannot be shared across VMs. Use separate volumes or a shared storage service.",
                    )
                )

        # -----------------------------------------------------------------
        # Check 7: Custom networks (only if multiple VMs)
        # -----------------------------------------------------------------
        if "networks" in config.compose_content:
            for network_name, network_config in config.compose_content.get("networks", {}).items():
                if network_config and network_config.get("external"):
                    errors.append(
                        ValidationError(
                            level="error",
                            service="(global)",
                            message=f"External network '{network_name}' won't exist across VMs. "
                            "Remove external networks or use .plato.internal DNS for cross-VM communication.",
                        )
                    )


def collect_local_paths(config: PlatoComposeConfig) -> dict[str, list[tuple[str, str]]]:
    """Collect local paths that need to be synced for each VM.

    Finds the common ancestor of all build contexts and syncs that.

    Returns:
        Dict mapping vm_name -> list of (local_path, remote_path) tuples
    """
    services = config.compose_content.get("services", {})
    compose_dir = config.compose_file.parent.resolve()

    # Collect all build context paths
    context_paths: list[Path] = [compose_dir]  # Always include compose dir

    for service_config in services.values():
        build_config = service_config.get("build")
        if build_config:
            if isinstance(build_config, str):
                context_path = build_config
            elif isinstance(build_config, dict):
                context_path = build_config.get("context", ".")
            else:
                continue

            # Resolve relative to compose file
            resolved = (compose_dir / context_path).resolve()
            context_paths.append(resolved)

    # Find common ancestor of all paths
    if len(context_paths) == 1:
        sync_dir = context_paths[0]
    else:
        # Get the common prefix of all paths
        sync_dir = Path(os.path.commonpath([str(p) for p in context_paths]))

    sync_dir_str = str(sync_dir)

    vm_paths: dict[str, list[tuple[str, str]]] = {}
    for vm_name in config.vms:
        # Sync to /app on VM
        vm_paths[vm_name] = [(sync_dir_str, "/app")]

    return vm_paths


def generate_vm_compose(config: PlatoComposeConfig, vm_name: str) -> str:
    """Generate a docker-compose file for a specific VM with only its services."""

    vm_config = config.vms[vm_name]
    original = config.compose_content.copy()

    # Build set of services on this VM for filtering depends_on
    services_on_this_vm = set(vm_config.services)

    # Filter services to only those for this VM
    filtered_services = {}
    for service_name in vm_config.services:
        if service_name in original.get("services", {}):
            service = original["services"][service_name].copy()
            # Remove x-plato annotation from output
            service.pop("x-plato", None)

            # Remove depends_on entries that reference services on other VMs
            depends_on = service.get("depends_on")
            if depends_on:
                if isinstance(depends_on, list):
                    # Simple list format
                    filtered_deps = [d for d in depends_on if d in services_on_this_vm]
                    if filtered_deps:
                        service["depends_on"] = filtered_deps
                    else:
                        del service["depends_on"]
                elif isinstance(depends_on, dict):
                    # Extended format with conditions
                    filtered_deps = {k: v for k, v in depends_on.items() if k in services_on_this_vm}
                    if filtered_deps:
                        service["depends_on"] = filtered_deps
                    else:
                        del service["depends_on"]

            filtered_services[service_name] = service

    # Build new compose file (no version - it's obsolete)
    new_compose = {
        "services": filtered_services,
    }

    # Include networks if defined
    if "networks" in original:
        new_compose["networks"] = original["networks"]

    # Include volumes if defined
    if "volumes" in original:
        new_compose["volumes"] = original["volumes"]

    return yaml.dump(new_compose, default_flow_style=False)


# =============================================================================
# Dependency Graph
# =============================================================================


def build_vm_dependency_order(config: PlatoComposeConfig) -> list[list[str]]:
    """Build VM startup order based on service depends_on.

    Returns:
        List of VM groups to start in order. VMs in the same group can start in parallel.
    """
    services = config.compose_content.get("services", {})

    # Build service -> VM mapping
    service_to_vm: dict[str, str] = {}
    for vm_name, vm_config in config.vms.items():
        for svc in vm_config.services:
            service_to_vm[svc] = vm_name

    # Build VM -> VM dependencies
    vm_deps: dict[str, set[str]] = {vm: set() for vm in config.vms}

    for service_name, service_config in services.items():
        service_vm = service_to_vm.get(service_name)
        if not service_vm:
            continue

        depends_on = service_config.get("depends_on", [])
        if isinstance(depends_on, dict):
            depends_on = list(depends_on.keys())

        for dep in depends_on:
            dep_vm = service_to_vm.get(dep)
            if dep_vm and dep_vm != service_vm:
                vm_deps[service_vm].add(dep_vm)

    # Topological sort into levels
    levels: list[list[str]] = []
    remaining = set(config.vms.keys())
    satisfied: set[str] = set()

    while remaining:
        # Find VMs with all dependencies satisfied
        level = [vm for vm in remaining if vm_deps[vm].issubset(satisfied)]

        if not level:
            # Circular dependency - just add remaining
            level = list(remaining)

        levels.append(level)
        satisfied.update(level)
        remaining -= set(level)

    return levels


# =============================================================================
# SSH Helpers
# =============================================================================


def generate_ssh_keypair(key_dir: Path) -> tuple[str, str]:
    """Generate an ED25519 SSH keypair.

    Returns:
        (private_key_path, public_key)
    """
    private_key_path = key_dir / "id_ed25519"
    public_key_path = key_dir / "id_ed25519.pub"

    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", str(private_key_path), "-N", "", "-q"],
        check=True,
    )

    public_key = public_key_path.read_text().strip()
    return str(private_key_path), public_key


# =============================================================================
# FsWatch + Rsync Hot Reload
# =============================================================================


def check_fswatch() -> bool:
    """Check if fswatch is installed."""
    try:
        subprocess.run(["fswatch", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


class FsWatchSync:
    """Watch local directories and rsync changes to VMs.

    Uses fswatch to detect file changes and rsync to sync them to VMs.
    Supports syncing to multiple VMs in parallel.
    """

    def __init__(
        self,
        local_paths: list[str],
        vm_syncs: list[tuple[Environment, str, str]],  # (env, remote_path, private_key_path)
        excludes: list[str],
        verbose: bool = False,
    ):
        """Initialize the watcher.

        Args:
            local_paths: Local directories to watch
            vm_syncs: List of (env, remote_path, private_key_path) for each VM sync target
            excludes: Patterns to exclude (from .gitignore)
            verbose: Print sync status
        """
        self.local_paths = local_paths
        self.vm_syncs = vm_syncs
        self.excludes = excludes
        self.verbose = verbose
        self._fswatch_proc: subprocess.Popen | None = None
        self._sync_task: asyncio.Task | None = None
        self._running = False

    def _build_rsync_cmd(
        self,
        local_path: str,
        remote_path: str,
        job_id: str,
        private_key_path: str,
    ) -> list[str]:
        """Build rsync command for a sync."""
        sni = f"{job_id}--22.{GATEWAY_HOST}"
        proxy_cmd = f"openssl s_client -quiet -connect {GATEWAY_HOST}:443 -servername {sni} 2>/dev/null"
        ssh_cmd = f"ssh -i {private_key_path} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o 'ProxyCommand={proxy_cmd}'"

        cmd = [
            "rsync",
            "-az",
            "--delete",
        ]
        # Add excludes from .gitignore
        for pattern in self.excludes:
            cmd.extend(["--exclude", pattern])

        cmd.extend(
            [
                "-e",
                ssh_cmd,
                f"{local_path}/",
                f"root@{job_id}.plato:{remote_path}/",
            ]
        )
        return cmd

    def _sync_path(self, local_path: str, env: Environment, remote_path: str, private_key_path: str) -> bool:
        """Sync a single path to a single VM."""
        try:
            result = subprocess.run(
                self._build_rsync_cmd(local_path, remote_path, env.job_id, private_key_path),
                capture_output=True,
                text=True,
                timeout=120,
            )
            return result.returncode == 0
        except Exception:
            return False

    def sync_all(self) -> int:
        """Sync all paths to all VMs. Returns number of successful syncs."""
        success = 0
        for local_path in self.local_paths:
            for env, remote_path, private_key_path in self.vm_syncs:
                if self._sync_path(local_path, env, remote_path, private_key_path):
                    success += 1
        return success

    async def _watch_and_sync(self):
        """Watch for changes and sync."""
        # Build fswatch command
        fswatch_cmd = [
            "fswatch",
            "-o",  # Output number of events (batch mode)
            "--latency",
            "0.5",
            "-r",  # Recursive
        ]
        # Add exclude patterns from .gitignore
        for pattern in self.excludes:
            fswatch_cmd.extend(["-e", pattern])

        fswatch_cmd.extend(self.local_paths)

        self._fswatch_proc = subprocess.Popen(
            fswatch_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        loop = asyncio.get_event_loop()

        while self._running:
            try:
                stdout = self._fswatch_proc.stdout
                if stdout is None:
                    break
                line = await loop.run_in_executor(None, stdout.readline)
                if line:
                    # Changes detected, sync all
                    count = await loop.run_in_executor(None, self.sync_all)
                    if self.verbose:
                        console.print(f"  [dim]synced to {count} VM(s)[/dim]")
            except Exception:
                break

    def start(self):
        """Start watching and syncing."""
        self._running = True
        self._sync_task = asyncio.create_task(self._watch_and_sync())

    def stop(self):
        """Stop watching."""
        self._running = False
        if self._fswatch_proc:
            self._fswatch_proc.terminate()
            self._fswatch_proc = None
        if self._sync_task:
            self._sync_task.cancel()
            self._sync_task = None


# =============================================================================
# Async Helpers
# =============================================================================


async def deploy_to_vm(
    env: Environment,
    vm_name: str,
    vm_config: VMConfig,
    compose_content: str,
    compose_dir: str,
) -> tuple[str, bool, str]:
    """Deploy docker compose to a single VM.

    Args:
        env: The VM environment
        vm_name: Name of the VM
        vm_config: VM configuration
        compose_content: The docker-compose.yml content for this VM
        compose_dir: Directory where the original compose file lives (for build contexts)

    Returns:
        (vm_name, success, message)
    """
    try:
        # Write compose file to the synced compose directory (so build contexts work)
        compose_file = f"{compose_dir}/docker-compose.plato.yml"
        escaped_compose = compose_content.replace("'", "'\\''")
        await env.execute(
            f"echo '{escaped_compose}' > '{compose_file}'",
            timeout=30,
        )

        # Start docker compose from the original directory
        result = await env.execute(
            f"cd '{compose_dir}' && docker compose -f docker-compose.plato.yml up --build -d 2>&1 | tee -a /tmp/plato-init.log",
            timeout=300,
        )

        output = result.stdout.strip()

        # Check for common error patterns in output
        error_patterns = ["no such file or directory", "error", "failed", "cannot", "not found"]
        has_error = any(pattern in output.lower() for pattern in error_patterns)

        if result.exit_code != 0 or has_error:
            # Show the actual error output
            error_output = output or result.stderr.strip() or "(no output)"
            return (vm_name, False, f"docker compose failed:\n{error_output}")

        # Verify containers are running
        ps_result = await env.execute(
            f"cd '{compose_dir}' && docker compose -f docker-compose.plato.yml ps -q | wc -l", timeout=30
        )
        container_count = int(ps_result.stdout.strip() or "0")

        if container_count == 0:
            return (vm_name, False, "no containers running - check /tmp/plato-init.log")

        return (vm_name, True, f"started {container_count} container(s)")

    except Exception as e:
        return (vm_name, False, str(e))


async def check_vm_health(env: Environment, vm_name: str) -> tuple[str, bool]:
    """Check if all containers on a VM are healthy.

    Returns:
        (vm_name, all_healthy)
    """
    try:
        result = await env.execute(
            "docker ps --format '{{.Status}}' | grep -v 'Up' | wc -l",
            timeout=30,
        )
        healthy = bool(result.stdout and result.stdout.strip() == "0")
        return (vm_name, healthy)
    except Exception:
        return (vm_name, False)


# =============================================================================
# CLI Commands
# =============================================================================


@app.command()
def validate(
    compose_file: Annotated[
        Path,
        typer.Argument(help="Path to docker-compose file"),
    ] = Path("docker-compose.yml"),
):
    """Validate a docker-compose file with x-plato annotations."""

    try:
        config = parse_compose_file(compose_file)
    except Exception as e:
        console.print(f"[red]Parse error:[/red] {e}")
        raise typer.Exit(1)

    has_issues = False

    # Show errors
    if config.errors:
        console.print(f"\n[red bold]Errors ({len(config.errors)}):[/red bold]")
        for err in config.errors:
            console.print(f"  [red]✗[/red] [{err.service}] {err.message}")
        has_issues = True

    # Show warnings (treated as errors)
    if config.warnings:
        console.print(f"\n[red bold]Errors ({len(config.warnings)}):[/red bold]")
        for warn in config.warnings:
            console.print(f"  [red]✗[/red] [{warn.service}] {warn.message}")
        has_issues = True

    if has_issues:
        total = len(config.errors) + len(config.warnings)
        console.print(f"\n[red]Validation failed with {total} error(s)[/red]")
        raise typer.Exit(1)

    # Show success
    console.print(f"\n[green]✓ Valid![/green] Found {len(config.vms)} VM groups:\n")

    # VM Groups table
    table = Table(title="VM Groups")
    table.add_column("VM", style="cyan")
    table.add_column("Memory", style="green")
    table.add_column("CPUs", style="green")
    table.add_column("Snapshot", style="yellow")
    table.add_column("Services", style="white")

    for vm_name, vm_config in config.vms.items():
        table.add_row(
            vm_name,
            f"{vm_config.memory}MB",
            str(vm_config.cpus),
            vm_config.snapshot,
            ", ".join(vm_config.services),
        )

    console.print(table)

    # Startup order
    vm_levels = build_vm_dependency_order(config)
    console.print("\n[bold]Deploy Order:[/bold]")
    for i, level in enumerate(vm_levels):
        vms_str = ", ".join(level)
        console.print(f"  {i + 1}. {vms_str}")

    # Rsync plans
    local_paths = collect_local_paths(config)
    has_local_paths = any(paths for paths in local_paths.values())

    if has_local_paths:
        console.print("\n[bold]Rsync Plans:[/bold]")
        for vm_name, paths in local_paths.items():
            if paths:
                console.print(f"  [cyan]{vm_name}[/cyan]:")
                for local_p, remote_p in paths:
                    console.print(f"    {local_p} -> {remote_p}")


async def _up_async(
    config: PlatoComposeConfig,
    timeout: int,
    save_name: str | None,
    verbose: bool,
    watch: bool = False,
    from_snapshot: str | None = None,
):
    """Async implementation of the up command."""

    # Collect local paths that need syncing
    local_paths = collect_local_paths(config)
    has_local_paths = any(paths for paths in local_paths.values())

    # Check for fswatch if hot reload requested
    use_watch = False
    if watch:
        if check_fswatch():
            use_watch = True
            console.print("[bold]Watch mode:[/bold] Using rsync + fswatch for hot reload")
        else:
            console.print("[yellow]Warning:[/yellow] fswatch not installed")
            console.print("[dim]Install: brew install fswatch (macOS) or apt install fswatch (Linux)[/dim]")
            use_watch = False

    if has_local_paths and verbose:
        console.print("Local paths to sync:")
        for vm_name, paths in local_paths.items():
            if paths:
                console.print(f"  {vm_name}:")
                for local_p, remote_p in paths:
                    console.print(f"    {local_p} -> {remote_p}")
        console.print("")

    vm_names = ", ".join(config.vms.keys())
    if from_snapshot:
        console.print(f"[bold]Starting {len(config.vms)} VMs from snapshot '{from_snapshot}':[/bold] {vm_names}")
    else:
        console.print(f"[bold]Starting {len(config.vms)} VMs:[/bold] {vm_names}")

    plato = AsyncPlato()
    session = None
    watcher: FsWatchSync | None = None
    total_start = time.time()

    try:
        # Create VMs - either from snapshot (cached) or fresh
        envs = []
        for vm_name, vm_config in config.vms.items():
            if from_snapshot:
                # Use disk snapshot as base (warm cache for docker layers, deps, etc.)
                # Uses version lookup: {config.name}-{vm_name}:version@base
                # restore_memory=False for disk-only snapshots (fresh boot with preserved disk)
                envs.append(
                    Env.simulator(
                        f"{config.name}-{vm_name}:{from_snapshot}@base",
                        alias=vm_name,
                        restore_memory=False,
                    )
                )
            else:
                # Create fresh VMs
                envs.append(
                    Env.resource(
                        simulator=f"{config.name}-{vm_name}",
                        sim_config=SimConfigCompute(
                            cpus=vm_config.cpus,
                            memory=vm_config.memory,
                            disk=10240,  # 10GB default
                        ),
                        alias=vm_name,
                    )
                )

        step_start = time.time()
        status_msg = "[bold green]Starting VMs from snapshot..." if from_snapshot else "[bold green]Creating VMs..."
        with console.status(status_msg, spinner="dots"):
            session = await plato.sessions.create(
                envs=envs,
                timeout=timeout,
                connect_network=True,
            )
            await session.start_heartbeat()
        console.print(f"[green]✓[/green] VMs ready: {time.time() - step_start:.1f}s")

        # Map alias to Environment object
        env_map: dict[str, Environment] = {env.alias: env for env in session.envs}

        # Show job IDs immediately after VMs start
        console.print("")
        for vm_name in config.vms:
            env = env_map.get(vm_name)
            if env:
                console.print(f"  [cyan]{vm_name}[/cyan]: {env.job_id}")

        if verbose:
            console.print("")
            console.print("[dim]SSH into VMs:[/dim]")
            for vm_name in config.vms:
                env = env_map.get(vm_name)
                if env:
                    console.print(f"  [dim]plato sandbox ssh -J {env.job_id}[/dim]")
            console.print("")
            console.print("[dim]Logs stored at /tmp/plato-init.log on each VM[/dim]")

        console.print("")

        # Generate SSH keypair for rsync (if needed)
        private_key_path = None

        if has_local_paths:
            key_dir = Path(tempfile.mkdtemp(prefix="plato_ssh_"))
            private_key_path, public_key = generate_ssh_keypair(key_dir)

            # Set up SSH keys on all VMs using the sessions API (one call adds to all VMs)
            step_start = time.time()
            with console.status("[bold green]Setting up SSH keys...", spinner="dots"):
                ssh_response = await session.add_ssh_key(public_key)

            if ssh_response.success:
                console.print(f"[green]✓[/green] SSH keys ready: {time.time() - step_start:.1f}s")
            else:
                console.print("[red]✗[/red] Failed to set up SSH keys")
                has_local_paths = False  # Skip sync

            if has_local_paths:
                # Show unique sync paths
                unique_syncs = set()
                for paths in local_paths.values():
                    for local_p, remote_p in paths:
                        unique_syncs.add((local_p, remote_p))

                console.print(f"[bold]Syncing to {len(config.vms)} VMs:[/bold]")
                for local_p, remote_p in unique_syncs:
                    console.print(f"  {local_p} -> {remote_p}")

                step_start = time.time()
                with console.status("[bold green]Installing rsync on VMs...", spinner="dots"):
                    rsync_install_tasks = [env.ensure_rsync() for env in session.envs]
                    rsync_install_results = await asyncio.gather(*rsync_install_tasks)

                if all(rsync_install_results):
                    console.print(f"[green]✓[/green] rsync ready: {time.time() - step_start:.1f}s")
                else:
                    console.print("[yellow]![/yellow] Failed to install rsync on some VMs")
                console.print("")
        else:
            console.print("[dim]No local paths to sync[/dim]")
            console.print("")

        # Build VM startup order based on depends_on
        vm_levels = build_vm_dependency_order(config)

        if verbose:
            console.print("Deploy order:")
            for i, level in enumerate(vm_levels):
                console.print(f"  {i + 1}. {', '.join(level)}")
            console.print("")

        # Start ALL rsync tasks upfront (they run in parallel across all VMs)
        # Each stage will wait for only its VMs' rsyncs to complete before deploying
        vm_rsync_tasks: dict[str, list[asyncio.Task]] = {}

        if has_local_paths and private_key_path:
            console.print("[bold]Starting rsync for all VMs...[/bold]")
            for vm_name in config.vms:
                paths = local_paths.get(vm_name, [])
                env = env_map.get(vm_name)
                if not env or not paths:
                    continue

                vm_rsync_tasks[vm_name] = []
                for local_p, remote_p in paths:
                    task = asyncio.create_task(
                        env.rsync(local_p, remote_p, private_key_path, exclude=config.ignore_paths, verbose=verbose)
                    )
                    vm_rsync_tasks[vm_name].append(task)

                if verbose:
                    console.print(f"  [dim]{vm_name}: {len(paths)} path(s)[/dim]")

            total_tasks = sum(len(tasks) for tasks in vm_rsync_tasks.values())
            console.print(f"  [dim]{total_tasks} rsync task(s) started in background[/dim]")
            console.print("")

        # Collect /etc/hosts entries from all VMs and propagate to all
        console.print("[bold]Setting up /etc/hosts...[/bold]")

        # Get hosts entries from each VM (Plato networking adds entries per-VM)
        all_hosts_lines: set[str] = set()
        for env in session.envs:
            result = await env.execute("grep '.plato.internal' /etc/hosts 2>/dev/null || true", timeout=30)
            if result.stdout:
                for line in result.stdout.strip().split("\n"):
                    if line.strip():
                        all_hosts_lines.add(line.strip())

        if all_hosts_lines:
            # Write all entries to all VMs
            hosts_content = "\\n".join(sorted(all_hosts_lines))
            hosts_tasks = []
            for env in session.envs:
                # Remove existing .plato.internal entries and add complete set
                hosts_tasks.append(
                    env.execute(
                        f"sed -i '/.plato.internal/d' /etc/hosts && echo -e \"{hosts_content}\" >> /etc/hosts",
                        timeout=30,
                    )
                )
            await asyncio.gather(*hosts_tasks)
            console.print(f"  [green]✓[/green] Synced {len(all_hosts_lines)} host entries across all VMs")
        else:
            console.print("  [yellow]![/yellow] No .plato.internal entries found")
        console.print("")

        # Deploy VMs in dependency order
        for level_idx, vm_level in enumerate(vm_levels):
            level_name = ", ".join(vm_level)
            stage_start = time.time()
            console.print(f"\n[bold]Stage {level_idx + 1}:[/bold] {level_name}")

            # 1. Wait for rsync tasks for THIS stage's VMs only
            if has_local_paths and private_key_path:
                stage_rsync_tasks = []
                for vm_name in vm_level:
                    stage_rsync_tasks.extend(vm_rsync_tasks.get(vm_name, []))

                if stage_rsync_tasks:
                    with console.status(f"[bold green]Syncing {len(stage_rsync_tasks)} path(s)...", spinner="dots"):
                        rsync_results = await asyncio.gather(*stage_rsync_tasks)
                    failed_syncs = [r for r in rsync_results if not r.success]
                    success_count = len(rsync_results) - len(failed_syncs)
                    if failed_syncs:
                        for r in failed_syncs:
                            console.print(f"  [red]✗[/red] rsync {Path(r.local_path).name}: {r.message}")
                        console.print(f"  [yellow]![/yellow] rsync: {success_count}/{len(rsync_results)} synced")
                    else:
                        console.print(f"  [green]✓[/green] rsync: {success_count} path(s) synced")

            # 2. Deploy docker compose for this stage (in parallel)
            deploy_start = time.time()
            deploy_tasks = []
            for vm_name in vm_level:
                env = env_map.get(vm_name)
                vm_config = config.vms.get(vm_name)
                if not env or not vm_config:
                    continue

                vm_compose = generate_vm_compose(config, vm_name)
                # Compute remote compose dir: /app + relative path from sync root
                local_compose_dir = config.compose_file.parent.resolve()
                local_sync_dir = Path(list(local_paths.values())[0][0][0])  # Get the sync source dir
                relative_compose_dir = local_compose_dir.relative_to(local_sync_dir)
                remote_compose_dir = f"/app/{relative_compose_dir}"
                deploy_tasks.append(deploy_to_vm(env, vm_name, vm_config, vm_compose, remote_compose_dir))

            with console.status("[bold green]Building and starting containers...", spinner="dots"):
                results = await asyncio.gather(*deploy_tasks)
            deploy_elapsed = time.time() - deploy_start

            for vm_name, success, message in results:
                if success:
                    console.print(f"  [green]✓[/green] {vm_name}: {message}")
                else:
                    console.print(f"  [red]✗[/red] {vm_name}: {message}")

            console.print(f"  [dim]deploy: {deploy_elapsed:.1f}s[/dim]")

            # 3. Wait for healthchecks on this stage before proceeding
            health_start = time.time()
            max_wait = 300
            all_healthy = False

            with console.status("[bold green]Waiting for containers to be healthy...", spinner="dots"):
                while time.time() - health_start < max_wait:
                    health_tasks = [
                        check_vm_health(env_map[vm_name], vm_name) for vm_name in vm_level if vm_name in env_map
                    ]

                    health_results = await asyncio.gather(*health_tasks)
                    all_healthy = all(healthy for _, healthy in health_results)

                    if all_healthy:
                        break

                    await asyncio.sleep(5)

            stage_elapsed = time.time() - stage_start
            if all_healthy:
                console.print(f"  [green]✓[/green] healthy ({stage_elapsed:.1f}s)")
            else:
                console.print(f"  [yellow]![/yellow] healthcheck timeout ({stage_elapsed:.1f}s)")

        console.print(f"\n[bold]Total time:[/bold] {time.time() - total_start:.1f}s")

        # Print summary
        console.print("")
        table = Table(title="Running VMs", show_lines=True)
        table.add_column("VM", style="cyan", no_wrap=True)
        table.add_column("Job ID", style="dim", no_wrap=True)
        table.add_column("Services", style="white")
        table.add_column("Connect URL", style="blue", no_wrap=True)

        for vm_name, vm_config in config.vms.items():
            env = env_map.get(vm_name)
            if env:
                table.add_row(
                    vm_name,
                    env.job_id,
                    ", ".join(vm_config.services),
                    f"https://{env.job_id}.connect.plato.so",
                )

        console.print(table)

        # Start fswatch for hot reload if enabled
        if use_watch and has_local_paths and private_key_path:
            console.print("")
            console.print("[bold]Starting hot reload watcher...[/bold]")

            # Parse .gitignore for excludes + x-plato.ignore
            gitignore_path = config.compose_file.parent / ".gitignore"
            excludes = parse_gitignore(gitignore_path) + config.ignore_paths
            if verbose:
                console.print(f"  [dim]Excluding {len(excludes)} patterns[/dim]")

            # Collect all unique local paths and their VM sync targets
            all_local_paths: set[str] = set()
            vm_syncs: list[tuple[Environment, str, str]] = []

            for vm_name, paths in local_paths.items():
                env = env_map.get(vm_name)
                if not env:
                    continue
                for local_p, remote_p in paths:
                    all_local_paths.add(local_p)
                    vm_syncs.append((env, remote_p, private_key_path))

            watcher = FsWatchSync(
                local_paths=list(all_local_paths),
                vm_syncs=vm_syncs,
                excludes=excludes,
                verbose=verbose,
            )
            watcher.start()
            console.print(f"  [green]Watching {len(all_local_paths)} path(s) for changes[/green]")

        console.print("")
        console.print(f"Session: {session.session_id}")
        if verbose:
            console.print("[dim]View logs: cat /tmp/plato-init.log[/dim]")
        console.print("")
        if use_watch:
            console.print("[dim]Hot reload active - file changes will sync automatically[/dim]")
        if save_name:
            console.print(f"Press Enter to save snapshot '{save_name}' and close, Ctrl+C to close without saving")
        else:
            console.print("Press Enter to close, Ctrl+C to close")

        # Wait for user input (blocking)
        try:
            await asyncio.get_event_loop().run_in_executor(None, input)
        except EOFError:
            await asyncio.sleep(10)

        if save_name:
            # Snapshot each VM with its own service/version/dataset
            # Naming: {config.name}:{save_name}@{vm_name}
            # e.g., plato-preview:v1@db, plato-preview:v1@app
            console.print(f"[bold]Saving snapshot '{save_name}'...[/bold]")
            success_count = 0

            # Snapshot each VM in parallel with per-VM naming
            # Naming: {config.name}-{vm_name}:{tag}@base
            async def snapshot_vm(vm_name: str, env: Environment):
                result = await env.disk_snapshot(
                    override_service=f"{config.name}-{vm_name}",
                    override_version=save_name,
                    override_dataset="base",
                    target="sims.plato.so",
                )
                return vm_name, result

            step_start = time.time()
            tasks = [snapshot_vm(vm_name, env) for vm_name, env in env_map.items()]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, BaseException):
                    console.print(f"  [red]✗[/red] Error: {result}")
                    continue
                vm_name, info = result
                if info and hasattr(info, "artifact_id") and info.artifact_id:
                    success_count += 1
                    console.print(f"  [green]✓[/green] {vm_name}: {config.name}-{vm_name}:{save_name}")
                else:
                    error = getattr(info, "error", "unknown error") if info else "no result"
                    console.print(f"  [red]✗[/red] {vm_name}: failed - {error}")

            elapsed = time.time() - step_start
            if success_count > 0:
                console.print(
                    f"\n[green]✓[/green] Snapshot '{save_name}' saved ({success_count} VM(s), {elapsed:.1f}s)"
                )
                console.print(f"  [dim]Restore with: plato compose up {config.compose_file} --from {save_name}[/dim]")
            else:
                console.print("\n[red]✗[/red] Failed to save snapshot - no VMs snapshotted")

        console.print("\nClosing session...")

    except asyncio.CancelledError:
        console.print("\nClosing session...")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        import traceback

        traceback.print_exc()
        raise
    finally:
        # Clean up watcher
        if watcher:
            watcher.stop()
        if session:
            await session.close()
        await plato.close()
        console.print("Done!")


@app.command()
def up(
    compose_file: Annotated[
        Path,
        typer.Argument(help="Path to docker-compose file"),
    ] = Path("docker-compose.yml"),
    timeout: Annotated[
        int,
        typer.Option("--timeout", "-t", help="Session timeout in seconds"),
    ] = 7200,
    save: Annotated[
        str | None,
        typer.Option("--save", "-s", help="Save snapshot with this name when exiting"),
    ] = None,
    restore: Annotated[
        str | None,
        typer.Option("--from", help="Restore from a named snapshot instead of creating fresh VMs"),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed logs and SSH commands"),
    ] = False,
    watch: Annotated[
        bool,
        typer.Option("--watch", "-w", help="Enable hot reload - watch for file changes and rsync automatically"),
    ] = False,
):
    """Start docker compose services across multiple VMs.

    Uses rsync to sync local bind mount paths to VMs. With --watch, uses fswatch
    to detect file changes and automatically rsync them to VMs for hot reload.

    Snapshots provide warm caching - docker layers, dependencies, and build artifacts
    are preserved, making subsequent builds much faster.

    Examples:
        # Fresh start
        plato compose up docker-compose.yml

        # Save snapshot when done (for faster future starts)
        plato compose up docker-compose.yml --save my-stack

        # Start from snapshot (warm cache - faster docker builds)
        plato compose up docker-compose.yml --from my-stack

    Requirements for --watch:
      macOS: brew install fswatch
      Linux: apt install fswatch
    """

    # Parse compose file
    try:
        config = parse_compose_file(compose_file)
    except Exception as e:
        console.print(f"[red]Parse error:[/red] {e}")
        raise typer.Exit(1)

    # Check for validation errors (warnings are also treated as errors)
    has_issues = False

    if config.errors:
        console.print(f"[red bold]Errors ({len(config.errors)}):[/red bold]")
        for err in config.errors:
            console.print(f"  [red]✗[/red] [{err.service}] {err.message}")
        has_issues = True

    if config.warnings:
        console.print(f"\n[red bold]Errors ({len(config.warnings)}):[/red bold]")
        for warn in config.warnings:
            console.print(f"  [red]✗[/red] [{warn.service}] {warn.message}")
        has_issues = True

    if has_issues:
        total = len(config.errors) + len(config.warnings)
        console.print(f"\n[red]Validation failed with {total} error(s)[/red]")
        console.print("Fix errors before running. Use 'plato compose validate' for details.")
        raise typer.Exit(1)

    # Run async implementation
    try:
        asyncio.run(_up_async(config, timeout, save, verbose, watch, restore))
    except KeyboardInterrupt:
        console.print("\nInterrupted.")
        raise typer.Exit(0)


@app.command()
def generate(
    compose_file: Annotated[
        Path,
        typer.Argument(help="Path to docker-compose file"),
    ] = Path("docker-compose.yml"),
    vm: Annotated[
        str,
        typer.Option("--vm", "-v", help="Generate compose for specific VM"),
    ] = "",
):
    """Generate per-VM docker-compose files (for debugging)."""

    try:
        config = parse_compose_file(compose_file)
    except Exception as e:
        console.print(f"[red]Parse error:[/red] {e}")
        raise typer.Exit(1)

    vms_to_generate = [vm] if vm else list(config.vms.keys())

    for vm_name in vms_to_generate:
        if vm_name not in config.vms:
            console.print(f"[red]VM not found:[/red] {vm_name}")
            continue

        console.print(f"[cyan]# {vm_name}[/cyan]")
        console.print(generate_vm_compose(config, vm_name))
        console.print("")


if __name__ == "__main__":
    app()
