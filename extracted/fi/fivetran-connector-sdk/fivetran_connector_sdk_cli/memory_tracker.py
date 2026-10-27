"""Memory limit and usage report for a local `debug` run."""
import atexit
import os
import sys
import threading
import time

from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_common.memory_tracker import MemoryTrackerBase, get_debug_memory_bytes


def _log_memory_constraint_warning(memory_limit_bytes: int) -> None:
    print_library_log(
        f"could not enforce memory constraint of {memory_limit_bytes // (1024 ** 3)} GB; "
        "debug will continue without memory constraint",
        Logging.Level.WARNING
    )


class DebugMemoryTracker(MemoryTrackerBase):
    """Enforces a memory limit during local `fivetran debug` runs.

    Runs for the entire debug session (including any Update() calls) as a
    daemon thread, using RSS-only reads (no cgroups needed for local dev).
    Kills the process if the limit is exceeded, and logs peak + average
    usage via an atexit hook when the session ends.
    """

    def __init__(self, sample_interval=1.0):
        super().__init__(sample_interval)
        self.memory_limit_bytes = constants.MEMORY_LIMIT_BYTES
        self.atexit_registered = False

    def start(self):
        """Measure baseline and start background monitoring."""
        self.baseline_bytes = get_debug_memory_bytes()
        if self.baseline_bytes == -1:
            _log_memory_constraint_warning(self.memory_limit_bytes)
            return  # Don't start monitoring if we can't read memory

        print_library_log(
            f"enforcing a {self.memory_limit_bytes // (1024 ** 3)} GB memory limit for local testing. "
            "Connectors may be subject to memory limits in production as well",
            Logging.Level.INFO
        )

        try:
            self.active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
        except Exception:
            _log_memory_constraint_warning(self.memory_limit_bytes)
            self.active = False
            self.monitor_thread = None
            return

        if not self.atexit_registered:
            try:
                atexit.register(self._log_results)
                self.atexit_registered = True
            except Exception:
                print_library_log(
                    "peak memory reporting could not be registered; memory limit is still enforced",
                    Logging.Level.WARNING
                )

    def _monitor_loop(self):
        """Background thread that samples memory at the configured interval."""
        logged_read_failure = False

        while self.active:
            try:
                current_bytes = get_debug_memory_bytes()
                if current_bytes == -1:
                    if not logged_read_failure:
                        _log_memory_constraint_warning(self.memory_limit_bytes)
                        logged_read_failure = True
                    time.sleep(self.sample_interval)
                    continue

                self.record_sample(current_bytes)

                if current_bytes > self.memory_limit_bytes:
                    used_gb = current_bytes / (1024 ** 3)
                    limit_gb = self.memory_limit_bytes / (1024 ** 3)
                    print_library_log(
                        f"memory usage of connector code exceeded the allowed limit "
                        f"(used: {used_gb:.2f} GB, limit: {limit_gb:.2f} GB)",
                        Logging.Level.SEVERE
                    )
                    print_library_log(
                        "refer to https://fivetran.com/docs/connector-sdk/connector-development-and-configuration/connector-memory-management "
                        "for analysing and fixing memory usage",
                        Logging.Level.SEVERE
                    )
                    sys.stdout.flush()
                    sys.stderr.flush()
                    os._exit(1)

            except Exception:
                if not logged_read_failure:
                    _log_memory_constraint_warning(self.memory_limit_bytes)
                    logged_read_failure = True

            time.sleep(self.sample_interval)

    def stop(self, timeout=3.0):
        """Stop monitoring (no-op for debug mode).
        
        Debug mode logs at exit via atexit hook, not here.
        The daemon thread will exit when the main thread exits.
        """
        pass
