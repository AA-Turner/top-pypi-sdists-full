"""
Process Management Utilities

Handles background process lifecycle, PID tracking, and log management
for InnoDay services.
"""

import asyncio
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional

import psutil


class ProcessManager:
    """
    Manages background processes with PID tracking and log management.

    Provides utilities for starting, stopping, and monitoring processes
    in the background with proper cleanup and logging.
    """

    def __init__(self, pid_dir: Path, log_dir: Path):
        """Initialize process manager with directories for PIDs and logs."""
        self.pid_dir = Path(pid_dir)
        self.log_dir = Path(log_dir)

        # Ensure directories exist
        self.pid_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _get_pid_file(self, service_name: str) -> Path:
        """Get PID file path for a service."""
        return self.pid_dir / f"{service_name}.pid"

    def _get_log_file(self, service_name: str) -> Path:
        """Get log file path for a service."""
        return self.log_dir / f"{service_name}.log"

    async def start_process(
        self, service_name: str, cmd: List[str], cwd: Optional[Path] = None
    ) -> bool:
        """
        Start a background process and track its PID.

        Args:
            service_name: Name of the service for tracking
            cmd: Command and arguments to execute
            cwd: Working directory for the process

        Returns:
            True if process started successfully, False otherwise
        """
        try:
            pid_file = self._get_pid_file(service_name)
            log_file = self._get_log_file(service_name)

            # Check if process is already running
            if await self.is_process_running(service_name):
                return False

            # Open log file
            with open(log_file, "a") as log_fp:
                log_fp.write(
                    f"\n--- Starting {service_name} at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n"
                )
                log_fp.flush()

                # Start process in background
                process = subprocess.Popen(
                    cmd,
                    stdout=log_fp,
                    stderr=subprocess.STDOUT,
                    cwd=cwd,
                    start_new_session=True,  # Detach from parent
                    env=dict(os.environ),  # Inherit environment
                )

                # Write PID file
                with open(pid_file, "w") as pid_fp:
                    pid_fp.write(str(process.pid))

                # Wait a moment to ensure process doesn't immediately exit
                await asyncio.sleep(0.5)

                # Check if process is still running
                if process.poll() is None:
                    return True
                else:
                    # Process exited, clean up PID file
                    pid_file.unlink(missing_ok=True)
                    return False

        except Exception as e:
            print(f"Failed to start process {service_name}: {e}")
            return False

    async def stop_process(self, service_name: str, timeout: int = 10) -> bool:
        """
        Stop a background process gracefully.

        Args:
            service_name: Name of the service to stop
            timeout: Maximum time to wait for graceful shutdown

        Returns:
            True if process stopped successfully, False otherwise
        """
        try:
            pid_file = self._get_pid_file(service_name)

            if not pid_file.exists():
                return True  # Already stopped

            # Read PID
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())

            try:
                process = psutil.Process(pid)

                # Send SIGTERM for graceful shutdown
                process.terminate()

                # Wait for graceful shutdown
                try:
                    process.wait(timeout=timeout)
                except psutil.TimeoutExpired:
                    # Force kill if graceful shutdown failed
                    process.kill()
                    process.wait(timeout=5)

                # Clean up PID file
                pid_file.unlink(missing_ok=True)

                # Log shutdown
                log_file = self._get_log_file(service_name)
                with open(log_file, "a") as log_fp:
                    log_fp.write(
                        f"\n--- Stopped {service_name} at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n"
                    )

                return True

            except psutil.NoSuchProcess:
                # Process doesn't exist, clean up PID file
                pid_file.unlink(missing_ok=True)
                return True

        except Exception as e:
            print(f"Failed to stop process {service_name}: {e}")
            return False

    async def is_process_running(self, service_name: str) -> bool:
        """Check if a process is currently running."""
        try:
            pid_file = self._get_pid_file(service_name)

            if not pid_file.exists():
                return False

            # Read PID
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())

            # Check if process exists and is running
            try:
                process = psutil.Process(pid)
                return process.is_running()
            except psutil.NoSuchProcess:
                # Process doesn't exist, clean up PID file
                pid_file.unlink(missing_ok=True)
                return False

        except Exception:
            return False

    async def get_process_pid(self, service_name: str) -> Optional[int]:
        """Get the PID of a running process."""
        try:
            pid_file = self._get_pid_file(service_name)

            if not pid_file.exists():
                return None

            with open(pid_file, "r") as f:
                pid = int(f.read().strip())

            # Verify process exists
            try:
                psutil.Process(pid)
                return pid
            except psutil.NoSuchProcess:
                pid_file.unlink(missing_ok=True)
                return None

        except Exception:
            return None

    async def get_logs(
        self, service_name: str, lines: int = 50, follow: bool = False
    ) -> Optional[str]:
        """
        Get logs for a service.

        Args:
            service_name: Name of the service
            lines: Number of lines to return (from end)
            follow: If True, stream logs continuously (not implemented yet)

        Returns:
            Log content as string, or None if no logs
        """
        try:
            log_file = self._get_log_file(service_name)

            if not log_file.exists():
                return None

            # Read last N lines
            with open(log_file, "r") as f:
                all_lines = f.readlines()

            if lines > 0:
                recent_lines = all_lines[-lines:]
            else:
                recent_lines = all_lines

            return "".join(recent_lines)

        except Exception as e:
            print(f"Failed to read logs for {service_name}: {e}")
            return None

    async def cleanup_stale_pids(self) -> int:
        """
        Clean up stale PID files for processes that are no longer running.

        Returns:
            Number of stale PID files cleaned up
        """
        cleaned = 0

        for pid_file in self.pid_dir.glob("*.pid"):
            try:
                with open(pid_file, "r") as f:
                    pid = int(f.read().strip())

                try:
                    psutil.Process(pid)
                    # Process exists, keep PID file
                except psutil.NoSuchProcess:
                    # Process doesn't exist, remove PID file
                    pid_file.unlink()
                    cleaned += 1

            except Exception:
                # Invalid PID file, remove it
                pid_file.unlink(missing_ok=True)
                cleaned += 1

        return cleaned

    def list_tracked_services(self) -> List[str]:
        """Get list of services that have PID files."""
        services = []
        for pid_file in self.pid_dir.glob("*.pid"):
            service_name = pid_file.stem
            services.append(service_name)
        return services

    def get_log_files(self) -> Dict[str, Path]:
        """Get mapping of service names to their log files."""
        log_files = {}
        for log_file in self.log_dir.glob("*.log"):
            service_name = log_file.stem
            log_files[service_name] = log_file
        return log_files
