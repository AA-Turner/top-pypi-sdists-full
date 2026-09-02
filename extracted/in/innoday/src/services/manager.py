"""
Service Manager for InnoDay Platform

Manages the lifecycle of all InnoDay services (API, UI) with unified
start/stop/restart/status operations and monitoring capabilities.
"""

import asyncio
import socket
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import psutil
import toml

from ..config.schema import InnoServiceConfig, ServiceStatus
from ..utils.process import ProcessManager


class InnoServiceManager:
    """
    Unified service manager for all InnoDay services.

    Provides centralized control over API and UI services with
    background process management, PID tracking, and status monitoring.
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize service manager with configuration."""
        self.config_path = config_path or self._get_default_config_path()
        self.data_dir = self._get_data_dir()
        self.pid_dir = self.data_dir / "pids"
        self.log_dir = self.data_dir / "logs"

        # Ensure directories exist
        self.pid_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.config = self._load_config()
        self.process_manager = ProcessManager(self.pid_dir, self.log_dir)

        # Service definitions
        self.services = {
            "api": {
                "name": "InnoDay API",
                "module": "src.main",
                "args": ["api"],
                "port": self.config.api.port,
                "enabled": self.config.api.enabled,
            },
        }

    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        return str(Path.home() / ".innoday" / "config.toml")

    def _get_data_dir(self) -> Path:
        """Get data directory for InnoDay files."""
        return Path.home() / ".innoday" / "data"

    def _load_config(self) -> InnoServiceConfig:
        """Load configuration from file or create default."""
        config_path = Path(self.config_path)

        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config_data = toml.load(f)
                return InnoServiceConfig.from_dict(config_data)
            except Exception as e:
                print(f"Warning: Failed to load config from {config_path}: {e}")
                print("Using default configuration")

        # Create default config
        config = InnoServiceConfig()
        self._save_config(config)
        return config

    def _save_config(self, config: InnoServiceConfig) -> None:
        """Save configuration to file."""
        config_path = Path(self.config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            toml.dump(config.to_dict(), f)

    def _check_port_available(self, port: int) -> Tuple[bool, Optional[str]]:
        """Check if a port is available for binding.

        Returns:
            Tuple of (is_available, process_info)
        """
        try:
            # Try to bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("0.0.0.0", port))
                return True, None
        except OSError:
            # Port is in use, try to find what's using it
            try:
                for proc in psutil.process_iter(["pid", "name"]):
                    try:
                        for conn in proc.connections():
                            if conn.laddr.port == port and conn.status == "LISTEN":
                                return (
                                    False,
                                    f"{proc.info['name']} (PID: {proc.info['pid']})",
                                )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                return False, "Unknown process"
            except Exception:
                return False, "Unknown process"

    async def start_service(self, service_name: str) -> bool:
        """Start a specific service."""
        if service_name not in self.services:
            raise ValueError(f"Unknown service: {service_name}")

        service = self.services[service_name]

        if not service["enabled"]:
            print(f"Service {service_name} is disabled in configuration")
            return False

        if await self.is_service_running(service_name):
            print(f"Service {service_name} is already running")
            return True

        # Check if port is available before starting
        if "port" in service and service["port"]:
            port = service["port"]
            is_available, process_info = self._check_port_available(port)
            if not is_available:
                print(
                    f"✗ Cannot start {service['name']}: Port {port} is already in use by {process_info}"
                )
                print(
                    "  Please stop the conflicting process or change the port in configuration"
                )
                return False

        print(f"Starting {service['name']}...")

        # Use sys.executable so the spawned process runs inside the same
        # virtual environment as the CLI (which already has src/ installed).
        # Previously used `uv run python -m src.main`, which requires the
        # current working directory to be the repo root — broken when the
        # CLI is invoked from any other directory (issue #201).
        cmd = [sys.executable, "-m", service["module"]] + service["args"]

        # Add port argument for API
        if service_name == "api" and "port" in service and service["port"]:
            cmd.extend(["--port", str(service["port"])])

        # Add host argument for API
        if service_name == "api":
            cmd.extend(["--host", self.config.api.host])

        # Start process in background
        success = await self.process_manager.start_process(
            service_name, cmd, cwd=Path.cwd()
        )

        if success:
            print(f"✓ {service['name']} started successfully")

            # Wait a moment and verify it's running
            await asyncio.sleep(2)
            if await self.is_service_running(service_name):
                return True
            else:
                print(f"✗ {service['name']} failed to start properly")
                return False
        else:
            print(f"✗ Failed to start {service['name']}")
            return False

    async def stop_service(self, service_name: str) -> bool:
        """Stop a specific service."""
        if service_name not in self.services:
            raise ValueError(f"Unknown service: {service_name}")

        service = self.services[service_name]

        if not await self.is_service_running(service_name):
            print(f"Service {service_name} is not running")
            return True

        print(f"Stopping {service['name']}...")

        success = await self.process_manager.stop_process(service_name)

        if success:
            print(f"✓ {service['name']} stopped successfully")
            return True
        else:
            print(f"✗ Failed to stop {service['name']}")
            return False

    async def restart_service(self, service_name: str) -> bool:
        """Restart a specific service."""
        print(f"Restarting {self.services[service_name]['name']}...")

        # Stop first
        await self.stop_service(service_name)

        # Wait a moment
        await asyncio.sleep(1)

        # Start again
        return await self.start_service(service_name)

    async def start_all(self) -> bool:
        """Start all enabled services."""
        print("Starting all enabled services...")

        # First check all ports before starting any services
        port_conflicts = []
        for service_name, service in self.services.items():
            if service["enabled"] and "port" in service and service["port"]:
                port = service["port"]
                is_available, process_info = self._check_port_available(port)
                if not is_available:
                    port_conflicts.append(
                        f"  - {service['name']} (port {port}): blocked by {process_info}"
                    )

        if port_conflicts:
            print("✗ Cannot start services due to port conflicts:")
            for conflict in port_conflicts:
                print(conflict)
            print("\nPlease resolve these conflicts before starting services.")
            return False

        results = {}
        for service_name in self.services:
            if self.services[service_name]["enabled"]:
                results[service_name] = await self.start_service(service_name)

        success_count = sum(results.values())
        total_enabled = sum(1 for s in self.services.values() if s["enabled"])

        if success_count == total_enabled:
            print(f"✓ All {success_count} services started successfully")
            return True
        else:
            print(f"⚠ {success_count}/{total_enabled} services started successfully")
            return False

    async def stop_all(self) -> bool:
        """Stop all running services."""
        print("Stopping all services...")

        # Track which services were actually running
        running_services = []
        for service_name in self.services:
            if await self.is_service_running(service_name):
                running_services.append(service_name)

        if not running_services:
            print("No services were running")
            return True

        # Stop all running services
        results = {}
        for service_name in running_services:
            results[service_name] = await self.stop_service(service_name)

        success_count = sum(results.values())
        total_services = len(self.services)
        total_running = len(running_services)

        # Report based on total services to match start_all behavior
        if success_count == total_running:
            print(
                f"✓ Stopped {success_count} of {total_services} services (only {total_running} were running)"
            )
            return True
        else:
            print(f"⚠ {success_count}/{total_running} services stopped successfully")
            return False

    async def restart_all(self) -> bool:
        """Restart all enabled services."""
        print("Restarting all services...")

        # Stop all first
        await self.stop_all()

        # Wait a moment
        await asyncio.sleep(2)

        # Start all enabled
        return await self.start_all()

    async def is_service_running(self, service_name: str) -> bool:
        """Check if a service is running."""
        return await self.process_manager.is_process_running(service_name)

    async def get_service_status(self, service_name: str) -> ServiceStatus:
        """Get detailed status of a service."""
        if service_name not in self.services:
            raise ValueError(f"Unknown service: {service_name}")

        service = self.services[service_name]
        is_running = await self.is_service_running(service_name)

        pid = None
        uptime = None
        memory_usage = None
        cpu_percent = None

        if is_running:
            pid = await self.process_manager.get_process_pid(service_name)
            if pid:
                try:
                    process = psutil.Process(pid)
                    uptime = time.time() - process.create_time()
                    memory_usage = process.memory_info().rss
                    cpu_percent = process.cpu_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    is_running = False

        return ServiceStatus(
            name=service_name,
            display_name=service["name"],
            enabled=service["enabled"],
            running=is_running,
            pid=pid,
            port=service.get("port"),
            uptime=uptime,
            memory_usage=memory_usage,
            cpu_percent=cpu_percent,
        )

    async def get_all_status(self) -> Dict[str, ServiceStatus]:
        """Get status of all services."""
        status = {}
        for service_name in self.services:
            status[service_name] = await self.get_service_status(service_name)
        return status

    async def get_logs(
        self, service_name: str, lines: int = 50, follow: bool = False
    ) -> Optional[str]:
        """Get logs for a specific service."""
        if service_name not in self.services:
            raise ValueError(f"Unknown service: {service_name}")

        return await self.process_manager.get_logs(service_name, lines, follow)

    def get_config(self) -> InnoServiceConfig:
        """Get current configuration."""
        return self.config

    def update_config(self, **kwargs) -> None:
        """Update configuration and save to file."""
        # Update config object
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        # Save to file
        self._save_config(self.config)

        # Reload services configuration
        for service_name, service in self.services.items():
            if service_name == "api":
                service["port"] = self.config.api.port
                service["enabled"] = self.config.api.enabled
