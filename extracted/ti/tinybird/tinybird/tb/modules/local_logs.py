import json
import platform
from typing import Optional

from docker.client import DockerClient
from docker.models.containers import Container


def clickhouse_is_ready(container: Container) -> bool:
    try:
        result = container.exec_run("clickhouse 'SELECT 1 AS healthcheck'")
        return result.output.decode("utf-8").strip() == "1"
    except Exception:
        return False


def redis_is_ready(container: Container) -> bool:
    try:
        result = container.exec_run("redis-cli PING")
        return result.output.decode("utf-8").strip() == "PONG"
    except Exception:
        return False


def local_authentication_is_ready(container: Container) -> bool:
    try:
        result = container.exec_run("curl -s http://localhost:8000/tokens")
        data = json.loads(result.output.decode("utf-8").strip())
        token_keys = ["admin_token", "user_token", "workspace_admin_token"]
        return all(key in data for key in token_keys)
    except Exception:
        return False


def server_is_ready(container: Container) -> bool:
    try:
        result = container.exec_run("curl -s http://localhost:8001/health/liveness")
        is_live = result.output.decode("utf-8").strip() == "alive"
        if not is_live:
            return False
        result = container.exec_run("curl -s http://localhost:8001/health/readiness")
        return result.output.decode("utf-8").strip() == "ready"
    except Exception:
        return False


def events_is_ready(container: Container) -> bool:
    try:
        result = container.exec_run("curl -s http://localhost:8042/health/liveness")
        is_live = result.output.decode("utf-8").strip() == "alive"
        if not is_live:
            return False
        result = container.exec_run("curl -s http://localhost:8042/health/readiness")
        return result.output.decode("utf-8").strip() == "ready"
    except Exception:
        return False


def container_is_ready(container: Container) -> bool:
    health = container.attrs.get("State", {}).get("Health", {}).get("Status")
    status = container.status
    return health == "healthy" and status == "running"


def container_is_starting(container: Container) -> bool:
    status = container.status
    health = container.attrs.get("State", {}).get("Health", {}).get("Status")
    return status == "restarting" or (status == "running" and health == "starting")


def container_is_stopping(container: Container) -> bool:
    status = container.status
    return status == "stopping"


def container_is_unhealthy(container: Container) -> bool:
    health = container.attrs.get("State", {}).get("Health", {}).get("Status")
    return health == "unhealthy"


def bytes_to_gb(b):
    return round(b / (1024**3), 2)  # two decimal places (e.g., 1.75 GB)


def get_container(client, name_or_id):
    return client.containers.get(name_or_id)


def get_image_arch(client, image_ref):
    try:
        image = client.images.get(image_ref)
        return (image.attrs.get("Architecture") or "").lower()
    except Exception:
        return ""


def is_emulated(host_arch, image_arch):
    # Architecture equivalents - same arch with different names
    arch_equivalents = [
        {"x86_64", "amd64"},
        {"aarch64", "arm64"},
    ]

    if not host_arch or not image_arch:
        return False

    if host_arch == image_arch:
        return False

    # Check if architectures are equivalent
    return all(not (host_arch in equiv_set and image_arch in equiv_set) for equiv_set in arch_equivalents)


def mem_usage_percent(container):
    st = container.stats(stream=False)
    mem = st.get("memory_stats", {}) or {}
    limit = float(mem.get("limit") or 0.0)
    usage = float(mem.get("usage") or 0.0)
    stats = mem.get("stats", {}) or {}
    inactive = float(stats.get("total_inactive_file") or stats.get("inactive_file") or 0.0)
    used = max(usage - inactive, 0.0)
    pct = (used / limit * 100.0) if limit > 0 else None
    return used, limit, pct


def container_stats(container: Container, client: DockerClient):
    host_arch = platform.machine().lower()
    image_arch = get_image_arch(client, container.attrs.get("Config", {}).get("Image", ""))
    emu = is_emulated(host_arch, image_arch)
    used_b, limit_b, pct = mem_usage_percent(container)
    pct = round(pct, 1) if pct is not None else None
    used_gb = bytes_to_gb(used_b)
    limit_gb = bytes_to_gb(limit_b) if limit_b > 0 else None
    lim_str = f"{limit_gb} GB" if limit_gb else "no-limit"
    arch_str = f"arch={host_arch} img={image_arch or 'unknown'} emulated={str(emu).lower()}"
    cpu_usage_pct = cpu_usage_stats(container)
    return f"memory {used_gb}/{lim_str} cpu {cpu_usage_pct} {arch_str}"


def cpu_usage_stats(container: Container) -> str:
    st = container.stats(stream=False)
    cpu = st.get("cpu_stats", {}) or {}
    cpu_usage = cpu.get("cpu_usage", {}) or {}
    total_usage = cpu_usage.get("total_usage", 0)
    system_cpu_usage = cpu.get("system_cpu_usage", 0)
    pct = (total_usage / system_cpu_usage * 100.0) if system_cpu_usage > 0 else None
    return f"{round(pct, 1) if pct is not None else 'N/A'}%"


def check_memory_sufficient(container: Container, client: DockerClient) -> tuple[bool, Optional[str]]:
    """
    Check if container has sufficient memory.

    Returns:
        tuple[bool, str | None]: (is_sufficient, warning_message)
            - is_sufficient: True if memory is sufficient, False otherwise
            - warning_message: None if sufficient, otherwise a warning message
    """
    host_arch = platform.machine().lower()
    image_arch = get_image_arch(client, container.attrs.get("Config", {}).get("Image", ""))
    is_emu = is_emulated(host_arch, image_arch)
    used_b, limit_b, pct = mem_usage_percent(container)

    if limit_b <= 0:
        # No memory limit set
        return True, None

    limit_gb = bytes_to_gb(limit_b)
    used_gb = bytes_to_gb(used_b)

    # Memory thresholds
    # For emulated containers, we need more memory and lower threshold
    HIGH_MEMORY_THRESHOLD_EMULATED = 70.0  # 70% for emulated
    HIGH_MEMORY_THRESHOLD_NATIVE = 85.0  # 85% for native
    MINIMUM_MEMORY_GB_EMULATED = 6.0  # Minimum 6GB for emulated
    MINIMUM_MEMORY_GB_NATIVE = 4.0  # Minimum 4GB for native

    warnings = []

    # Check memory percentage
    if pct is not None:
        threshold = HIGH_MEMORY_THRESHOLD_EMULATED if is_emu else HIGH_MEMORY_THRESHOLD_NATIVE
        if pct >= threshold:
            warnings.append(
                f"Memory usage is at {pct:.1f}% ({used_gb}/{limit_gb:.2f} GB), "
                f"which exceeds the recommended threshold of {threshold:.0f}%."
            )

    # Check absolute memory limit
    min_memory = MINIMUM_MEMORY_GB_EMULATED if is_emu else MINIMUM_MEMORY_GB_NATIVE
    if limit_gb < min_memory:
        arch_msg = f" (running emulated {image_arch} on {host_arch})" if is_emu else ""
        warnings.append(
            f"Memory limit is {limit_gb:.2f} GB{arch_msg}, but at least {min_memory:.1f} GB is recommended."
        )

    if warnings:
        warning_msg = " ".join(warnings)
        if is_emu:
            warning_msg += (
                "\n"
                f"You're running an emulated container ({image_arch} on {host_arch}), which requires more resources.\n"
                "Consider increasing Docker's memory allocation."
            )
        else:
            warning_msg += "Consider increasing Docker's memory allocation."
        return False, warning_msg

    return True, None
