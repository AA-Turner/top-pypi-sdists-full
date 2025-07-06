"""Module providing shutdown_manager functionality."""

import logging
import time
import os
import sys
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
        self._load_shutdown_configuration()
        self.last_no_queued_time = None
        self.shutdown_threshold = 500
        self.launch_duration = 1
        self.instance_source = "auto"
        self.encryption_key = None
        self.reserved_instance = None
        self.shutdown_attempts = 0
        self.max_shutdown_attempts = 3

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

    @log_errors(raise_exception=True, log_error=True)
    def do_cleanup_and_shutdown(self):
        """Clean up resources and shut down the instance."""
        try:
            logging.info("Initiating instance stop request")
            result, error, message = self.scaling.stop_instance()
            
            if error:
                logging.error("Error stopping instance API call: %s", error)
                self.shutdown_attempts += 1
                if self.shutdown_attempts < self.max_shutdown_attempts:
                    logging.info("Will retry shutdown later (attempt %s of %s)", 
                                self.shutdown_attempts, self.max_shutdown_attempts)
                    return False
            else:
                logging.info("Stop instance request successful: %s", message)
            
            logging.info("Shutting down the machine")
            try:
                os.system("shutdown now")
            except Exception as e:
                logging.error("Failed to execute shutdown command: %s", str(e))
            sys.exit(0)
            return True
        except Exception as e:
            logging.error("Critical error in shutdown process: %s", str(e))
            self.shutdown_attempts += 1
            if self.shutdown_attempts >= self.max_shutdown_attempts:
                logging.error("Maximum shutdown attempts reached, forcing exit")
                sys.exit(1)
            return False

    @log_errors(raise_exception=False, log_error=True)
    def handle_shutdown(self, tasks_running):
        """Check idle time and trigger shutdown if threshold is exceeded.

        Args:
            tasks_running: Boolean indicating if there are running tasks
        """
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

            # Try to shut down and return success/failure
            shutdown_success = self.do_cleanup_and_shutdown()
            if not shutdown_success:
                logging.warning("Shutdown attempt failed, will retry on next cycle")
