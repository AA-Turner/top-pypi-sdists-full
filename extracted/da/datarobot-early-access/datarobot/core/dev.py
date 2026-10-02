#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

# /// script
# dependencies = [
#   "pyyaml>=6.0.3",
#   "psutil>=7.2.1",
# ]
# ///

"""
Development services startup script
"""

from __future__ import annotations

import argparse
import contextlib
import os
from pathlib import Path
import platform
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
from typing import Any, Dict, Iterator, List

import psutil
import yaml

IS_WINDOWS = platform.system() == "Windows"
# Set on every service drdev starts and inherited by everything they spawn. The value names the
# service and its directory, so a later run reclaims its own leftovers, not another project's.
DRDEV_MANAGED_ENV = "DRDEV_MANAGED"

DEFAULT_STARTUP_TIMEOUT = 120
STARTUP_TIMEOUT_ENV_VAR = "DRDEV_STARTUP_TIMEOUT"


parser = argparse.ArgumentParser(
    description="Start development services from .taskfile-data.yaml or command line",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
    %(prog)s                          # Start all services from config
    %(prog)s mcp_server agent         # Start specific services from config
    %(prog)s --manual service1:8080   # Manual mode with explicit ports
    %(prog)s --config custom.yaml     # Use custom config file
    %(prog)s --timeout 300            # Wait longer for a slow service
    %(prog)s --force                  # Also stop processes this drdev run does not manage
    """,
)
parser.add_argument(
    "services",
    nargs="*",
    help="Service names to start (from config), or leave empty for all",
)
parser.add_argument(
    "--config",
    "-c",
    type=Path,
    default=Path(".taskfile-data.yaml"),
    help="Path to configuration file (default: .taskfile-data.yaml)",
)
parser.add_argument(
    "--manual",
    "-m",
    action="store_true",
    help="Manual mode: provide services as name:port pairs",
)
parser.add_argument(
    "--force",
    "-f",
    action="store_true",
    help="Also stop processes occupying a service port that this drdev run does not manage",
)
parser.add_argument(
    "--timeout",
    "-t",
    metavar="SECONDS",
    help=f"Seconds to wait for a service to start (default: {DEFAULT_STARTUP_TIMEOUT} or ${STARTUP_TIMEOUT_ENV_VAR})",
)


def _describe_process(proc: psutil.Process) -> str:
    cmdline = ' '.join(proc.info.get('cmdline') or [])
    return f"{proc.info.get('name') or 'unknown process'} [{proc.pid}]" + (f" ({cmdline})" if cmdline else "")


class DevService:
    def __init__(self, name: str, port: int, print_url: bool = False, force: bool = False) -> None:
        self.name = name
        self.port = port
        self.print_url = print_url
        self.force = force
        self.process: subprocess.Popen[str] | None = None
        self.output_thread: threading.Thread | None = None
        self._marker = f"{name}@{Path.cwd().resolve()}"

    def start(self) -> None:
        """
        Start a service using task command and prefix its output.
        """
        self._stop_processes_on_port()

        print(f"Starting {self.name}...")

        # Calculate the prefix length to account for in terminal width
        prefix = f"[{self.name}] "
        prefix_length = len(prefix) + 1

        # Get current terminal size and adjust for prefix
        try:
            terminal_size = shutil.get_terminal_size()
            adjusted_columns = max(40, terminal_size.columns - prefix_length)  # Ensure minimum width
        except Exception:
            adjusted_columns = max(40, 80 - prefix_length)  # Fallback to standard width minus prefix

        # Prepare environment with adjusted COLUMNS
        env = os.environ.copy()
        env['COLUMNS'] = str(adjusted_columns)
        env[DRDEV_MANAGED_ENV] = self._marker

        # Prepare subprocess arguments
        if IS_WINDOWS:
            # Windows-specific configuration
            # Use unbuffered I/O and handle shell differently
            process = subprocess.Popen(
                ["task", f"{self.name}:dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,  # Unbuffered on Windows
                env=env,
                # Own process group, so stop() can reach the whole child tree with CTRL_BREAK_EVENT
                creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
            )
        else:
            # Unix-like systems (Linux, macOS)
            process = subprocess.Popen(
                ["task", f"{self.name}:dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered on Unix
                env=env,
            )

        self.process = process

        # Create a thread to handle output with prefix
        def handle_output() -> None:
            if process.stdout is None:
                return
            try:
                # Use different reading strategy based on platform
                if IS_WINDOWS:
                    # Windows: read character by character to handle buffering issues
                    line_buffer = ''
                    while True:
                        char = process.stdout.read(1)
                        if not char:
                            break
                        line_buffer += char
                        if char == '\n':
                            print(f"{prefix} {line_buffer}", end='')
                            line_buffer = ''
                    # Print any remaining characters
                    if line_buffer:
                        print(f"{prefix} {line_buffer}")
                else:
                    # Unix: readline works well
                    for line in iter(process.stdout.readline, ''):
                        if line:
                            print(f"{prefix} {line}", end='')
            except Exception as e:
                print(f"{prefix} Error reading output: {e}")
            finally:
                if process.stdout:
                    process.stdout.close()

        self.output_thread = threading.Thread(target=handle_output, daemon=True)
        self.output_thread.start()

    def stop(self) -> None:
        """Stop the service."""
        if self.process is None:
            return

        try:
            if IS_WINDOWS:
                # On Windows, send CTRL_BREAK_EVENT to the process group
                # This is more graceful than terminate()
                try:
                    ctrl_break = getattr(signal, "CTRL_BREAK_EVENT", signal.SIGTERM)
                    self.process.send_signal(ctrl_break)
                except Exception:
                    self.process.terminate()
            else:
                # On Unix, terminate sends SIGTERM
                self.process.terminate()

            # Give processes time to clean up
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"⚠️  Force killing {self.name}...")
                self.process.kill()
                self.process.wait(timeout=5)
        except Exception as e:
            print(f"⚠️  Error stopping {self.name}: {e}")

        self.process = None
        if self.output_thread:
            self.output_thread.join(timeout=5)
            self.output_thread = None

    def get_url(self) -> str:
        """Determine the URL prefix based on environment."""
        notebook_id = os.environ.get('NOTEBOOK_ID')

        if notebook_id:
            api_endpoint = os.environ.get("DATAROBOT_API_ENDPOINT", "")
            # Replace api/v2 with notebook-sessions/{id}/ports/
            prefix = api_endpoint.replace(
                "api/v2",
                f"notebook-sessions/{notebook_id}/ports/",
            )

            return f"{prefix}{self.port}/"

        else:
            return f"http://localhost:{self.port}/"

    def wait_for_start(self, timeout: int = DEFAULT_STARTUP_TIMEOUT) -> None:
        """Wait for the service to start."""
        if self.process is None:
            raise Exception(f"Service {self.name} is not started")

        print(f"⏳ Waiting for {self.name} on port {self.port} (up to {timeout}s)...")

        # Sleep before every probe but the first, so the deadline second is probed too.
        for probe in range(timeout + 1):
            if probe > 0:
                time.sleep(1)

            self.process.poll()

            if self._is_port_listening():
                print(f"✅ {self.name} is ready on port {self.port}")
                return

            if self.process.returncode is not None:
                # A service can legitimately exit once it detects the port is already
                # served (e.g. by another task starting the same shared process) and
                # defer to that existing instance. Only a nonzero exit before the port
                # ever came up is a real failure.
                if self.process.returncode != 0:
                    raise Exception(f"{self.name} exited with code {self.process.returncode}")
                raise Exception(f"{self.name} exited with code 0 without starting on port {self.port}")

        raise Exception(
            f"Timeout waiting for {self.name} on port {self.port} after {timeout}s. "
            f"Raise it with --timeout or ${STARTUP_TIMEOUT_ENV_VAR}",
        )

    def wait(self) -> None:
        """Wait for the service to exit."""
        # Poll on both platforms: a blocking wait cannot be interrupted by Ctrl+C on Windows
        while self.process is not None and self.process.poll() is None:
            time.sleep(1)

    def drain_output(self) -> None:
        """Let the output thread print what the service logged on its way out."""
        if self.output_thread:
            self.output_thread.join(1)

    def _stop_processes_on_port(self) -> None:
        managed: List[psutil.Process] = []
        foreign: List[psutil.Process] = []
        for proc in self._get_processes_on_port():
            try:
                is_managed = proc.environ().get(DRDEV_MANAGED_ENV) == self._marker
            except psutil.NoSuchProcess:
                continue
            except (psutil.Error, OSError):
                # Cannot read its environment, so we never claim it.
                is_managed = False
            (managed if is_managed else foreign).append(proc)

        if foreign:
            if not self.force:
                details = ', '.join(_describe_process(proc) for proc in foreign)
                them = "them" if len(foreign) > 1 else "it"
                raise Exception(
                    f"Port {self.port} is in use by {details}, which this drdev run does not manage. "
                    f"Stop {them} yourself, run {self.name} on another port, "
                    f'or re-run with "drdev --force".',
                )
            print("⚠️  --force given, also stopping processes this drdev run does not manage.")
            managed.extend(foreign)

        for proc in managed:
            print(f"⚠️  Found process on port {self.port}: {_describe_process(proc)}. Stopping it...")
            with contextlib.suppress(psutil.Error):
                proc.terminate()

        _, alive = psutil.wait_procs(managed, timeout=10)
        for proc in alive:
            with contextlib.suppress(psutil.Error):
                proc.kill()
        # Let the kill land before deciding the port is still held.
        psutil.wait_procs(alive, timeout=5)

        # Whoever holds the port now is what matters: a process we stopped may have been replaced.
        holders = list(self._get_processes_on_port()) if managed else []
        if holders:
            details = ', '.join(_describe_process(proc) for proc in holders)
            raise Exception(f"Port {self.port} is still in use by {details} after cleanup.")

    def _get_processes_on_port(self) -> Iterator[psutil.Process]:
        for proc in psutil.process_iter(attrs=['name', 'cmdline']):
            try:
                connections = proc.net_connections()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
            if any(conn.status == psutil.CONN_LISTEN and conn.laddr.port == self.port for conn in connections):
                yield proc

    def _is_port_listening(self) -> bool:
        """Check if a port is listening using socket connection attempt."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.1)
                result = sock.connect_ex(('127.0.0.1', self.port))
                return result == 0
        except Exception:
            return False

    def __str__(self) -> str:
        return f"{self.name}:{self.port}"


def load_config_file(config_path: Path) -> Dict[str, Any]:
    """Load the .taskfile-data.yaml configuration file."""
    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
            return config or {}
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML configuration: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading configuration file: {e}")
        sys.exit(1)


def _resolve_startup_timeout(cli_value: str | None) -> int:
    """Resolve the startup timeout: CLI flag, then environment, then default."""
    if cli_value is not None:
        source, value = "--timeout", cli_value
    else:
        # An unset variable and a blank one both mean "not configured".
        source, value = STARTUP_TIMEOUT_ENV_VAR, os.environ.get(STARTUP_TIMEOUT_ENV_VAR, "").strip()
        if not value:
            return DEFAULT_STARTUP_TIMEOUT

    try:
        timeout = int(value)
    except ValueError:
        timeout = 0

    if timeout <= 0:
        print(f"❌ Invalid {source} value: {value!r}. Must be a positive whole number of seconds.")
        sys.exit(1)
    return timeout


def _parse_port(value: Any) -> int:
    """Parse a port value, raising ValueError or TypeError if int() cannot make a usable TCP port."""
    port = int(value)
    if not 1 <= port <= 65535:
        raise ValueError(f"port out of range: {port}")
    return port


def get_services_from_config(config: Dict[str, Any], force: bool = False) -> List[DevService]:
    """Extract services from configuration in the specified order."""
    services: List[DevService] = []
    ports_config = config.get('ports', [])

    if not ports_config:
        print("❌ No services defined in configuration file")
        sys.exit(1)

    for service_config in ports_config:
        if not isinstance(service_config, dict):
            continue

        name = service_config.get('name')
        port = service_config.get('port')
        print_url = service_config.get('print_url', False)

        if name and port is not None:
            try:
                services.append(DevService(name, _parse_port(port), print_url=print_url, force=force))
            except (TypeError, ValueError):
                print(f"❌ Invalid port value for service {name}: {port}. Expected a port in 1-65535")
                sys.exit(1)

    if not services:
        print("❌ No valid services found in configuration")
        sys.exit(1)

    return services


def parse_service_args(args: List[str], force: bool = False) -> List[DevService]:
    """Parse service:port arguments into tuples."""
    services: List[DevService] = []
    for arg in args:
        try:
            service, port_str = arg.split(':')
            port = _parse_port(port_str)
            # Print URLs for all services
            services.append(DevService(service, port, print_url=True, force=force))
        except ValueError:
            print(f"❌ Invalid argument: {arg}. Expected `service:port` with a port in 1-65535")
            sys.exit(1)
    return services


def stop_services(services: List[DevService]) -> None:
    """Stop all services."""
    print("\n\n🛑 Stopping all services..")
    for service in services:
        service.stop()


def main(args: argparse.Namespace) -> None:
    """Main function to start and manage development services."""

    services: List[DevService]

    startup_timeout = _resolve_startup_timeout(args.timeout)

    # Determine services to start
    if args.manual:
        # Manual mode: parse service:port pairs
        if not args.services:
            print("❌ No services specified in manual mode")
            parser.print_help()
            sys.exit(1)
        services = parse_service_args(args.services, args.force)
    else:
        # Config mode: read from YAML file
        config = load_config_file(args.config)
        all_services = get_services_from_config(config, args.force)

        if args.services:
            # Filter to requested services only, maintaining order from config
            requested = set(args.services)
            services = []
            for service in all_services:
                if service.name in requested:
                    services.append(service)
                    requested.remove(service.name)

            # Check for unknown services
            if requested:
                unknown = ', '.join(requested)
                available = ', '.join(s.name for s in all_services)
                print(f"❌ Unknown services: {unknown}")
                print(f"Available services: {available}")
                sys.exit(1)
        else:
            # Use all services from config in specified order
            services = all_services

    if not services:
        print("❌ No services to start")
        sys.exit(1)

    # Display startup information
    print("🚀 Starting development services...")
    print(f"📋 Services to start (in order): {', '.join(s.name for s in services)}")
    if not args.manual:
        print(f"📁 Using config: {args.config}")
    print()

    try:
        # First pass: start all services
        for service in services:
            service.start()

        print()

        # Second pass: wait for all services to be ready
        for service in services:
            service.wait_for_start(startup_timeout)

        print()
        print("✅ All services started successfully!")
        print()

        # Third pass: print URLs
        for service in services:
            if service.print_url:
                url = service.get_url()
                print(f"🔗 {service.name} is accessible at: {url}")
        print()
        print("Press Ctrl+C to stop all services")

        # Wait for all processes
        for service in services:
            service.wait()

    except KeyboardInterrupt:
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # a second Ctrl+C must not abort shutdown
        if IS_WINDOWS:
            # Windows children have Ctrl+C disabled by their process group, so stop them explicitly
            stop_services(services)
        else:
            # The terminal signalled the children too, so just let their last output through
            for service in services:
                service.drain_output()
        sys.exit(0)

    except Exception as e:
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # aborting cleanup would leak the service tree
        print(f"❌ Error: {e}")
        # Clean up processes on error
        stop_services(services)
        sys.exit(1)


def cli_main() -> None:
    # Parse arguments
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli_main()
