import multiprocessing
import platform
import subprocess


def detect_cpu_threads() -> int:
    return max(1, multiprocessing.cpu_count())


def detect_gpu() -> dict:
    system = platform.system()

    # macOS: check for Apple Silicon (Metal / MPS)
    if system == "Darwin":
        return _detect_apple_gpu()

    # Linux/Windows: check NVIDIA
    return _detect_nvidia_gpu()


def _detect_apple_gpu() -> dict:
    try:
        output = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"], text=True, timeout=2
        ).strip()
        is_apple_silicon = "Apple" in output
        if is_apple_silicon:
            # Get GPU core count from system_profiler
            gpu_info = subprocess.check_output(
                ["system_profiler", "SPDisplaysDataType"], text=True, timeout=5
            )
            cores = ""
            for line in gpu_info.splitlines():
                if "Total Number of Cores" in line:
                    cores = line.split(":")[-1].strip()
                    break
            return {
                "available": True,
                "backend": "metal",
                "devices": [f"{output} ({cores} GPU cores)" if cores else output],
            }
        return {"available": False, "backend": None, "devices": []}
    except Exception:
        return {"available": False, "backend": None, "devices": []}


def _detect_nvidia_gpu() -> dict:
    try:
        output = subprocess.check_output(["nvidia-smi", "-L"], text=True, timeout=2)
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        return {
            "available": bool(lines),
            "backend": "cuda" if lines else None,
            "devices": lines,
        }
    except Exception:
        return {"available": False, "backend": None, "devices": []}


def detect_hardware_summary() -> dict:
    return {
        "cpu_threads": detect_cpu_threads(),
        "platform": platform.system(),
        "arch": platform.machine(),
        "gpu": detect_gpu(),
    }
