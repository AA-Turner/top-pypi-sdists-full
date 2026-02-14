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
from collections.abc import Iterator
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
import traceback
from typing import Any

import psutil
import yaml

IS_WINDOWS = platform.system() == "Windows"


parser = argparse.ArgumentParser(
    description="Start development services from .taskfile-data.yaml or command line",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
    %(prog)s                          # Start all services from config
    %(prog)s mcp_server agent         # Start specific services from config
    %(prog)s --manual service1:8080   # Manual mode with explicit ports
    %(prog)s --config custom.yaml     # Use custom config file
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


class DevService:
    def __init__(self, name: str, port: int, print_url: bool = False) -> None:
        self.name = name
        self.port = port
        self.print_url = print_url
        self.process: subprocess.Popen[str] | None = None
        self.output_thread: threading.Thread | None = None

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
                self.process.wait()  # Ensure it's dead
        except Exception as e:
            print(f"⚠️  Error stopping {self.name}: {e}")

        self.process = None
        if self.output_thread:
            self.output_thread.join()
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

    def wait_for_start(self, timeout: int = 120) -> None:
        if self.process is None:
            raise Exception(f"Service {self.name} is not started")

        """Wait for the service to start."""
        print(f"⏳ Waiting for {self.name} on port {self.port}...")

        for _ in range(timeout):
            self.process.poll()
            if self.process.returncode is not None:
                raise Exception(f"❌ {self.name} exited with code {self.process.returncode}")

            if self._is_port_listening():
                print(f"✅ {self.name} is ready on port {self.port}")
                return
            time.sleep(1)

        raise Exception(f"❌ Timeout waiting for {self.name} on port {self.port}")

    def wait(self) -> None:
        """Wait for the service to exit."""
        if self.process is None:
            return
        self.process.wait()

    def _stop_processes_on_port(self) -> None:
        procs = set()
        try:
            for proc in self._get_processes_on_port():
                cmdline = proc.info.get('cmdline', [])
                cmdline_str = ''
                if cmdline:
                    cmdline_str = ' '.join(cmdline)
                print(
                    f"⚠️  Found process on port {self.port}: "
                    f"{proc.info.get('name')} [{proc.pid}] ({cmdline_str}). Stopping it...",
                )
                proc.terminate()
                procs.add(proc)

            _, alive = psutil.wait_procs(procs, timeout=10)
            for proc in alive:
                proc.kill()
        except psutil.NoSuchProcess as e:
            print(f"✅ Process {e.pid} on port {self.port} no longer exists.")

        except Exception as e:
            traceback.print_exc()
            raise Exception(f"❌ Error stopping processes on port {self.port}: {e.__repr__()}") from e

    def _get_processes_on_port(self) -> Iterator[psutil.Process]:
        seen_pids = set()
        for proc in psutil.process_iter(attrs=['name', 'cmdline']):
            try:
                connections = proc.net_connections()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
            for conn in connections:
                if conn.laddr.port == self.port:
                    if proc.pid not in seen_pids:
                        seen_pids.add(proc.pid)
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


def load_config_file(config_path: Path) -> dict[str, Any]:
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


def get_services_from_config(config: dict[str, Any]) -> list[DevService]:
    """Extract services from configuration in the specified order."""
    services: list[DevService] = []
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

        if name and port:
            try:
                services.append(DevService(name, int(port), print_url=print_url))
            except ValueError:
                print(f"❌ Invalid port value for service {name}: {port}")
                sys.exit(1)

    if not services:
        print("❌ No valid services found in configuration")
        sys.exit(1)

    return services


def parse_service_args(args: list[str]) -> list[DevService]:
    """Parse service:port arguments into tuples."""
    services: list[DevService] = []
    for arg in args:
        try:
            service, port_str = arg.split(':')
            port = int(port_str)
            # Print URLs for all services
            services.append(DevService(service, port, print_url=True))
        except ValueError:
            print(f"❌ Invalid argument format: {arg}. Expected format: `service:port`")
            sys.exit(1)
    return services


def stop_services(services: list[DevService]) -> None:
    """Stop all services."""
    print("\n\n🛑 Stopping all services..")
    for service in services:
        service.stop()


def main(args: argparse.Namespace) -> None:
    """Main function to start and manage development services."""

    services: list[DevService]

    # Determine services to start
    if args.manual:
        # Manual mode: parse service:port pairs
        if not args.services:
            print("❌ No services specified in manual mode")
            parser.print_help()
            sys.exit(1)
        services = parse_service_args(args.services)
    else:
        # Config mode: read from YAML file
        config = load_config_file(args.config)
        all_services = get_services_from_config(config)

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
            service.wait_for_start()

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
        # We don't need to stop services explicitly, the signal is propagated to the child processes
        sys.exit(0)

    except Exception as e:
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
