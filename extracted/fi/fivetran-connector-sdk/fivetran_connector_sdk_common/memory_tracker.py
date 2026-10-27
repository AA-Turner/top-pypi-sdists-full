import os
import sys
import subprocess

from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_common.helpers import print_library_log


def get_debug_memory_bytes() -> int:
    """Get current process RSS for local debug monitoring.

    Used by the CLI's DebugMemoryTracker to enforce local memory limits during development, and as the
    fallback of production's SyncMemoryTracker.
    Returns process RSS only, no cgroups (debug runs outside containers).
    Only tracks the current Python process and its threads, not child processes.

    Returns:
        int: RSS in bytes, or -1 if unavailable.
    """
    try:
        if sys.platform == "linux":
            # /proc/self/status provides accurate current RSS in KB
            with open("/proc/self/status") as f:
                for line in f:
                    if line.startswith("VmRSS:"):
                        return int(line.split()[1]) * 1024  # KB to bytes
        elif sys.platform == "darwin":
            # ru_maxrss on macOS returns peak RSS, not current — use ps instead
            result = subprocess.run(
                ["ps", "-o", "rss=", "-p", str(os.getpid())],
                capture_output=True,
                text=True,
            )
            rss_kb = result.stdout.strip()
            if rss_kb:
                return int(rss_kb) * 1024
        elif sys.platform == "win32":
            import ctypes
            import ctypes.wintypes
            
            class ProcessMemoryCounters(ctypes.Structure):
                _fields_ = [
                    ("cb", ctypes.wintypes.DWORD),
                    ("PageFaultCount", ctypes.wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]
            
            pmc = ProcessMemoryCounters()
            pmc.cb = ctypes.sizeof(pmc)
            kernel32 = ctypes.windll.kernel32
            kernel32.GetCurrentProcess.restype = ctypes.wintypes.HANDLE
            psapi = ctypes.WinDLL("psapi")
            psapi.GetProcessMemoryInfo.restype = ctypes.wintypes.BOOL
            psapi.GetProcessMemoryInfo.argtypes = [
                ctypes.wintypes.HANDLE,
                ctypes.POINTER(ProcessMemoryCounters),
                ctypes.wintypes.DWORD,
            ]
            result = psapi.GetProcessMemoryInfo(
                kernel32.GetCurrentProcess(), ctypes.byref(pmc), pmc.cb
            )
            if result:
                return pmc.WorkingSetSize
    except Exception:
        pass
    
    return -1


class MemoryTrackerBase:
    """Shared baseline/peak/average accounting for memory trackers."""

    def __init__(self, sample_interval: float):
        self.sample_interval = sample_interval
        self.baseline_bytes = 0
        self.peak_delta_bytes = 0
        self.total_delta_bytes = 0
        self.sample_count = 0
        self.active = False
        self.monitor_thread = None

    def record_sample(self, current_bytes: int) -> None:
        delta_bytes = current_bytes - self.baseline_bytes
        if delta_bytes > self.peak_delta_bytes:
            self.peak_delta_bytes = delta_bytes
        if delta_bytes > 0:
            self.total_delta_bytes += delta_bytes
            self.sample_count += 1

    def _log_results(self) -> None:
        """Log peak and average memory usage."""
        try:
            if self.sample_count == 0:
                return  # No samples collected
            peak_mb = self.peak_delta_bytes / 1024 / 1024
            average_mb = self.total_delta_bytes / self.sample_count / 1024 / 1024
            print_library_log(
                f"connector process memory usage: average {average_mb:.2f} MB, peak {peak_mb:.2f} MB",
                Logging.Level.INFO,
            )
        except Exception:
            pass  # Fail silently if logging fails
