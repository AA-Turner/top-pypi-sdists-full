"""Module providing shutdown_manager functionality."""

import logging
import time
import os
import sys
import platform
import subprocess
import signal
from matrice.utils import log_errors
from matrice.compute_manager.scaling import (
    Scaling,
)


class ShutdownManager:
    """Class for managing compute instance shutdown."""

    def __init__(self, scaling: Scaling):
        """Initialize ShutdownManager.

        Args:
            scaling: Scaling instance to manage shutdown
        """
        self.scaling = scaling
        self.launch_time = time.time()
        # Initialize default values before loading configuration
        self.last_no_queued_time = None
        self.shutdown_threshold = 500
        self.launch_duration = 1
        self.instance_source = "auto"
        self.encryption_key = None
        self.reserved_instance = None
        self.shutdown_attempts = 0
        self.max_shutdown_attempts = 3
        self.force_shutdown_attempts = 0
        self.max_force_shutdown_attempts = 2
        # Load configuration (may override defaults)
        self._load_shutdown_configuration()

    @log_errors(raise_exception=False, log_error=True)
    def _load_shutdown_configuration(self):
        """Load shutdown configuration from AWS secrets and initialize parameters."""
        response, error, message = self.scaling.get_shutdown_details()
        if error is None:
            self.shutdown_threshold = response["shutdownThreshold"] or 500
            self.launch_duration = response["launchDuration"] or 1
            self.instance_source = response["instanceSource"] or "auto"
            self.encryption_key = response.get("encryptionKey")
        self.launch_duration_seconds = self.launch_duration * 60 # minutes to seconds
        self.reserved_instance = self.instance_source == "reserved"
        logging.info(
            "Loaded shutdown configuration: threshold=%s, duration=%s, source=%s, reserved=%s",
            self.shutdown_threshold,
            self.launch_duration,
            self.instance_source,
            self.reserved_instance
        )

    def _force_emergency_shutdown(self):
        """Force emergency shutdown using most aggressive methods."""
        logging.critical("Executing emergency shutdown procedures")
        
        try:
            # Step 1: Kill all running Docker containers first
            self._kill_all_docker_containers()
            
            # Step 2: Try to kill all non-essential processes
            self._kill_non_essential_processes()
            
            # Step 3: Clear any remaining resources
            self._cleanup_system_resources()
            
        except Exception as e:
            logging.error("Error during emergency shutdown cleanup: %s", str(e))
        
        # Step 4: Force immediate exit with extreme prejudice
        try:
            logging.critical("Forcing immediate system exit")
            os._exit(1)  # Immediate exit without cleanup
        except Exception:
            # Last resort - signal ourselves
            try:
                os.kill(os.getpid(), signal.SIGKILL)
            except Exception:
                pass

    def _kill_all_docker_containers(self):
        """Kill all running Docker containers to free up resources."""
        try:
            logging.info("Killing all Docker containers during emergency shutdown")
            
            # Try to stop all containers gracefully first
            try:
                subprocess.run(["docker", "stop", "$(docker ps -q)"], 
                              shell=True, check=False, timeout=30)
            except Exception as e:
                logging.warning("Error stopping Docker containers gracefully: %s", str(e))
            
            # Force kill any remaining containers
            try:
                subprocess.run(["docker", "kill", "$(docker ps -q)"], 
                              shell=True, check=False, timeout=15)
            except Exception as e:
                logging.warning("Error force-killing Docker containers: %s", str(e))
                
            # Clean up Docker system
            try:
                subprocess.run(["docker", "system", "prune", "-af"], 
                              shell=True, check=False, timeout=30)
            except Exception as e:
                logging.warning("Error pruning Docker system: %s", str(e))
                
        except Exception as e:
            logging.error("Error during Docker container cleanup: %s", str(e))

    def _kill_non_essential_processes(self):
        """Kill non-essential processes that might be preventing shutdown."""
        try:
            system = platform.system().lower()
            
            if system == "linux":
                # Kill Python processes (except our own)
                current_pid = os.getpid()
                try:
                    # Get all python processes
                    result = subprocess.run(["pgrep", "-f", "python"], 
                                          capture_output=True, text=True, check=False)
                    if result.returncode == 0:
                        pids = result.stdout.strip().split('\n')
                        for pid in pids:
                            try:
                                pid_int = int(pid.strip())
                                if pid_int != current_pid:  # Don't kill ourselves
                                    os.kill(pid_int, signal.SIGTERM)
                                    time.sleep(0.1)  # Brief pause
                                    try:
                                        os.kill(pid_int, signal.SIGKILL)  # Force kill
                                    except ProcessLookupError:
                                        pass  # Already dead
                            except (ValueError, ProcessLookupError, PermissionError):
                                continue
                except Exception as e:
                    logging.warning("Error killing Python processes: %s", str(e))
                
                # Kill Docker daemon if possible
                try:
                    subprocess.run(["killall", "-9", "dockerd"], check=False, timeout=10)
                    subprocess.run(["killall", "-9", "docker"], check=False, timeout=10)
                except Exception as e:
                    logging.warning("Error killing Docker daemon: %s", str(e))
                    
                # Kill any stuck SSH connections
                try:
                    subprocess.run(["killall", "-9", "sshd"], check=False, timeout=5)
                except Exception as e:
                    logging.warning("Error killing SSH connections: %s", str(e))
                    
        except Exception as e:
            logging.error("Error killing non-essential processes: %s", str(e))

    def _cleanup_system_resources(self):
        """Clean up system resources before shutdown."""
        try:
            # Sync filesystem
            try:
                subprocess.run(["sync"], check=False, timeout=10)
                logging.info("Filesystem sync completed")
            except Exception as e:
                logging.warning("Error syncing filesystem: %s", str(e))
            
            # Clear memory caches
            try:
                if platform.system().lower() == "linux":
                    subprocess.run(["echo", "3", ">", "/proc/sys/vm/drop_caches"], 
                                  shell=True, check=False, timeout=5)
            except Exception as e:
                logging.warning("Error clearing memory caches: %s", str(e))
                
            # Unmount any problematic filesystems (if possible)
            try:
                if platform.system().lower() == "linux":
                    # Try to unmount any Docker volumes or temporary mounts
                    subprocess.run(["umount", "-fl", "/var/lib/docker"], 
                                  check=False, timeout=10)
            except Exception as e:
                logging.warning("Error unmounting filesystems: %s", str(e))
                
        except Exception as e:
            logging.error("Error during system resource cleanup: %s", str(e))

    def _execute_shutdown_command(self):
        """Execute system shutdown command with multiple fallbacks.
        
        Enhanced version with more aggressive shutdown methods.
        
        Returns:
            bool: True if any shutdown command succeeded, False otherwise
        """
        system = platform.system().lower()
        
        # Define shutdown commands in order of preference (most graceful first)
        shutdown_commands = []
        
        if system == "linux":
            shutdown_commands = [
                ["shutdown", "now"],  # Standard Linux shutdown
                ["systemctl", "poweroff"],  # Systemd poweroff
                ["systemctl", "poweroff", "--force"],  # Force systemd poweroff
                ["halt", "-f"],  # Force halt
                ["poweroff", "-f"],  # Force poweroff
                ["init", "0"],  # Init level 0 (shutdown)
                ["telinit", "0"],  # Alternative init command
            ]
        elif system == "windows":
            shutdown_commands = [
                ["shutdown", "/s", "/t", "0"],  # Windows shutdown
                ["shutdown", "/s", "/f", "/t", "0"],  # Windows force shutdown
                ["shutdown", "/p"],  # Windows immediate poweroff
            ]
        elif system == "darwin":  # macOS
            shutdown_commands = [
                ["shutdown", "-h", "now"],  # macOS shutdown
                ["halt"],  # macOS halt
                ["sudo", "shutdown", "-h", "now"],  # Sudo shutdown
            ]
        else:
            # Generic Unix-like fallbacks
            shutdown_commands = [
                ["shutdown", "-h", "now"],
                ["halt"],
                ["poweroff"],
                ["init", "0"],
            ]
        
        # Try each command in sequence
        for cmd in shutdown_commands:
            try:
                logging.info("Attempting shutdown with command: %s", " ".join(cmd))
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30,
                    check=False
                )
                
                if result.returncode == 0:
                    logging.info("Shutdown command succeeded: %s", " ".join(cmd))
                    return True
                else:
                    logging.warning(
                        "Shutdown command failed with return code %d: %s. STDERR: %s", 
                        result.returncode, 
                        " ".join(cmd),
                        result.stderr
                    )
            except subprocess.TimeoutExpired:
                logging.warning("Shutdown command timed out: %s", " ".join(cmd))
            except FileNotFoundError:
                logging.warning("Shutdown command not found: %s", " ".join(cmd))
            except Exception as e:
                logging.warning("Shutdown command failed: %s. Error: %s", " ".join(cmd), str(e))
        
        # If all standard commands failed, try more aggressive methods
        return self._try_aggressive_shutdown()

    def _try_aggressive_shutdown(self):
        """Try more aggressive shutdown methods when standard commands fail."""
        logging.warning("Standard shutdown commands failed, trying aggressive methods")
        
        try:
            system = platform.system().lower()
            
            if system == "linux":
                # Try writing directly to kernel interfaces
                aggressive_commands = [
                    # Magic SysRq key sequences
                    ["echo", "o", ">", "/proc/sysrq-trigger"],  # Immediate poweroff
                    ["echo", "b", ">", "/proc/sysrq-trigger"],  # Immediate reboot
                    # ACPI shutdown
                    ["echo", "4", ">", "/proc/acpi/sleep"],
                    # Direct kernel poweroff
                    ["echo", "1", ">", "/proc/sys/kernel/sysrq"],
                ]
                
                for cmd in aggressive_commands:
                    try:
                        logging.info("Trying aggressive shutdown: %s", " ".join(cmd))
                        result = subprocess.run(cmd, shell=True, check=False, timeout=10)
                        if result.returncode == 0:
                            logging.info("Aggressive shutdown command succeeded")
                            return True
                    except Exception as e:
                        logging.debug("Aggressive command failed: %s", str(e))
                        
        except Exception as e:
            logging.error("Error in aggressive shutdown methods: %s", str(e))
            
        return False
    @log_errors(raise_exception=True, log_error=True)
    def do_cleanup_and_shutdown(self):
        """Clean up resources and shut down the instance.
        
        This method attempts a coordinated shutdown with multiple fallback strategies:
        1. API call to notify the scaling service
        2. Graceful OS shutdown command
        3. Aggressive shutdown methods if needed
        4. Emergency forced shutdown as last resort
        
        Returns:
            bool: True if shutdown was initiated successfully, False otherwise
        """
        max_retries = self.max_shutdown_attempts
        
        for attempt in range(1, max_retries + 1):
            try:
                logging.info("Shutdown attempt %d of %d", attempt, max_retries)
                
                # Step 1: Notify scaling service of shutdown
                logging.info("Notifying scaling service of instance shutdown")
                result, error, message = self.scaling.stop_instance()
                
                if error:
                    logging.error("Failed to notify scaling service (attempt %d): %s", attempt, error)
                    if attempt < max_retries:
                        logging.info("Retrying in 5 seconds...")
                        time.sleep(5)
                        continue
                    else:
                        logging.warning("Proceeding with shutdown despite API notification failure")
                else:
                    logging.info("Scaling service notified successfully: %s", message)
                
                # Step 2: Attempt graceful system shutdown
                logging.info("Initiating graceful system shutdown")
                shutdown_success = self._execute_shutdown_command()
                
                if shutdown_success:
                    logging.info("Graceful shutdown command executed successfully")
                    # Give the system time to process the shutdown
                    time.sleep(10)
                    # If we reach here, graceful shutdown may have failed
                    logging.warning("System did not shut down gracefully, trying aggressive methods")
                
                # Step 3: Try aggressive shutdown methods
                logging.warning("Attempting aggressive shutdown methods")
                aggressive_success = self._try_aggressive_shutdown()
                
                if aggressive_success:
                    logging.info("Aggressive shutdown initiated")
                    time.sleep(5)
                    # If still running, proceed to emergency shutdown
                
                # Step 4: Emergency shutdown as absolute last resort
                logging.critical("All standard shutdown methods failed, executing emergency shutdown")
                self._force_emergency_shutdown()
                
                # Should not reach this point due to emergency shutdown
                return True
                
            except Exception as e:
                logging.error("Critical error during shutdown attempt %d: %s", attempt, str(e))
                
                if attempt >= max_retries:
                    logging.critical("All shutdown attempts exhausted, forcing immediate emergency exit")
                    try:
                        self._force_emergency_shutdown()
                    except Exception as emergency_error:
                        logging.critical("Emergency shutdown also failed: %s", str(emergency_error))
                        # Last resort - immediate exit
                        os._exit(1)
                    return False
                else:
                    logging.info("Waiting before retry attempt...")
                    time.sleep(5)
        
        # Fallback - should never reach here
        logging.critical("Shutdown loop completed unexpectedly, forcing emergency exit")
        self._force_emergency_shutdown()
        return False

    @log_errors(raise_exception=False, log_error=True)
    def handle_shutdown(self, tasks_running):
        """Check idle time and trigger shutdown if threshold is exceeded.

        Args:
            tasks_running: Boolean indicating if there are running tasks
        """
        # CRITICAL: Check if this is a reserved instance that should not be shut down
        # if self.reserved_instance:
        #     logging.debug("Reserved instance detected, skipping shutdown check")
        #     return

        # Update idle time tracking
        if tasks_running:
            self.last_no_queued_time = None
            logging.info("Tasks are running, resetting idle timer")
        elif self.last_no_queued_time is None:
            self.last_no_queued_time = time.time()
            logging.info("No tasks running, starting idle timer")

        if self.last_no_queued_time is not None:
            idle_time = time.time() - self.last_no_queued_time
            launch_time_passed = (time.time() - self.launch_time) > self.launch_duration_seconds

            # Log current status
            logging.info(
                "Time since last action: %s seconds. Time left to shutdown: %s seconds.",
                idle_time,
                max(0, self.shutdown_threshold - idle_time),
            )

            # Check if we should shut down
            if idle_time <= self.shutdown_threshold:
                return

            if not launch_time_passed:
                logging.info(
                "Instance not shutting down yet. Launch duration: %s seconds, elapsed: %s seconds",
                    self.launch_duration_seconds,
                    time.time() - self.launch_time,
                )
                return

            logging.info(
                "Idle time %s seconds exceeded threshold %s seconds. Shutting down.",
                idle_time,
                self.shutdown_threshold
            )

            self.do_cleanup_and_shutdown()
