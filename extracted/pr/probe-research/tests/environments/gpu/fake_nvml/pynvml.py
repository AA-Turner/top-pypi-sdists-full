"""A stand-in for NVIDIA's ``pynvml`` (nvidia-ml-py), for machines with no GPU.

Put this directory first on ``PYTHONPATH`` and the released SDK's hardware
collector imports it instead of the real module. It mirrors the names, return
shapes and error classes of nvidia-ml-py 12.x for the calls the collector makes
(``probe/hw/resources/nvidia.py``), and nothing else.

Behaviour comes from ``FAKE_NVML_MODE``:

* ``ok``               two devices with fixed readings (see READINGS)
* ``init_raises``      ``nvmlInit`` raises NVMLError_DriverNotLoaded (no driver)
* ``lost_midrun``      after ``FAKE_NVML_OK_SAMPLES`` samples every device call
                       raises NVMLError_GpuIsLost (an XID 79 mid-training)
* ``not_supported``    power, temperature and the process list raise
                       NVMLError_NotSupported (consumer / some cloud GPUs)
* ``foreign_raise``    after init, ``nvmlDeviceGetCount`` raises RuntimeError --
                       not an NVMLError at all (a broken binding)

Every call is appended to ``FAKE_NVML_LOG`` (one name per line) so a test can
prove the fake was reached rather than silently skipped.
"""

from __future__ import annotations

import os
import threading

NVML_TEMPERATURE_GPU = 0
NVML_ERROR_DRIVER_NOT_LOADED = 9
NVML_ERROR_NOT_SUPPORTED = 3
NVML_ERROR_GPU_IS_LOST = 15

#: device index -> (utilization %, memory used, memory total, power mW, temp C)
READINGS = {
    0: (37, 3 * 1024**3, 80 * 1024**3, 215_000, 61),
    1: (81, 70 * 1024**3, 80 * 1024**3, 402_000, 74),
}
#: GPU memory this process holds on each device (the per-process attribution).
PROC_MEMORY = {0: 1_500_000_000, 1: 2_500_000_000}

_lock = threading.Lock()
_samples = 0


class NVMLError(Exception):
    def __init__(self, value: int = 999):
        super().__init__(value)
        self.value = value

    def __str__(self) -> str:
        return f"NVML error {self.value}"


class NVMLError_DriverNotLoaded(NVMLError):  # noqa: N801 -- the real module's spelling
    def __init__(self):
        super().__init__(NVML_ERROR_DRIVER_NOT_LOADED)


class NVMLError_NotSupported(NVMLError):  # noqa: N801
    def __init__(self):
        super().__init__(NVML_ERROR_NOT_SUPPORTED)


class NVMLError_GpuIsLost(NVMLError):  # noqa: N801
    def __init__(self):
        super().__init__(NVML_ERROR_GPU_IS_LOST)


class _Struct:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def _mode() -> str:
    return os.environ.get("FAKE_NVML_MODE", "ok")


def _log(name: str) -> None:
    path = os.environ.get("FAKE_NVML_LOG")
    if path:
        with _lock, open(path, "a", encoding="utf-8") as fh:
            fh.write(name + "\n")


def _device_call(name: str) -> None:
    _log(name)
    if _mode() == "lost_midrun" and _samples > int(os.environ.get("FAKE_NVML_OK_SAMPLES", "2")):
        raise NVMLError_GpuIsLost()


def nvmlInit():
    _log("nvmlInit")
    if _mode() == "init_raises":
        raise NVMLError_DriverNotLoaded()


def nvmlShutdown():
    _log("nvmlShutdown")


def nvmlDeviceGetCount():
    global _samples
    with _lock:
        _samples += 1
    _log("nvmlDeviceGetCount")
    if _mode() == "foreign_raise" and _samples > 1:
        raise RuntimeError("fake binding broke")
    if _mode() == "lost_midrun" and _samples > int(os.environ.get("FAKE_NVML_OK_SAMPLES", "2")):
        raise NVMLError_GpuIsLost()
    return len(READINGS)


def nvmlDeviceGetHandleByIndex(index):
    _device_call("nvmlDeviceGetHandleByIndex")
    if index not in READINGS:
        raise NVMLError(2)
    return _Struct(index=index)


def nvmlDeviceGetUUID(handle):
    _device_call("nvmlDeviceGetUUID")
    return f"GPU-00000000-0000-0000-0000-00000000000{handle.index}"


def nvmlDeviceGetName(handle):
    _device_call("nvmlDeviceGetName")
    return "NVIDIA H100 80GB HBM3 (fake)"


def nvmlDeviceGetMemoryInfo(handle):
    _device_call("nvmlDeviceGetMemoryInfo")
    _util, used, total, _p, _t = READINGS[handle.index]
    return _Struct(total=total, used=used, free=total - used)


def nvmlDeviceGetUtilizationRates(handle):
    _device_call("nvmlDeviceGetUtilizationRates")
    return _Struct(gpu=READINGS[handle.index][0], memory=READINGS[handle.index][0] // 2)


def nvmlDeviceGetPowerUsage(handle):
    _device_call("nvmlDeviceGetPowerUsage")
    if _mode() == "not_supported":
        raise NVMLError_NotSupported()
    return READINGS[handle.index][3]


def nvmlDeviceGetTemperature(handle, sensor):
    _device_call("nvmlDeviceGetTemperature")
    if _mode() == "not_supported":
        raise NVMLError_NotSupported()
    return READINGS[handle.index][4]


def nvmlDeviceGetComputeRunningProcesses(handle):
    _device_call("nvmlDeviceGetComputeRunningProcesses")
    if _mode() == "not_supported":
        raise NVMLError_NotSupported()
    return [_Struct(pid=os.getpid(), usedGpuMemory=PROC_MEMORY[handle.index])]


def nvmlSystemGetDriverVersion():
    _log("nvmlSystemGetDriverVersion")
    return "550.54.15"


def nvmlSystemGetCudaDriverVersion_v2():  # noqa: N802
    _log("nvmlSystemGetCudaDriverVersion_v2")
    return 12040
