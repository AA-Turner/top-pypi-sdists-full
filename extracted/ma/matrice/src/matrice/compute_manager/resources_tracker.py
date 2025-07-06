"""
This module contains classes for tracking machine and action resources.
"""

import os
import subprocess
import logging
from datetime import datetime, timezone
import psutil
import docker
from matrice.compute_manager.instance_utils import (
    has_gpu,
    get_gpu_info,
    calculate_time_difference,
)
from matrice.compute_manager.scaling import (
    Scaling,
)
from matrice.utils import log_errors


class ResourcesTracker:
    """Tracks machine and pid resources"""

    def __init__(self):
        """Initialize ResourcesTracker"""

    @log_errors(default_return=(0, 0), raise_exception=False)
    def get_container_cpu_and_memory(self, container):
        """Get CPU and memory usage for a container"""
        stats = container.stats(stream=False)
        if stats:
            cpu_utilization = 0
            cpu_delta = (
                stats["cpu_stats"]["cpu_usage"]["total_usage"]
                - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            )
            system_delta = stats["cpu_stats"].get("system_cpu_usage", 0) - stats[
                "precpu_stats"
            ].get("system_cpu_usage", 0)
            if system_delta > 0:
                cpu_utilization = cpu_delta / system_delta * 100.0
            memory_usage = stats["memory_stats"].get("usage", 0)
            memory_limit = stats["memory_stats"].get("limit", 1)
            memory_utilization = memory_usage / memory_limit * 100.0
            return (
                cpu_utilization,
                memory_utilization,
            )
        return 0, 0

    @log_errors(default_return=(0, 0), raise_exception=False)
    def get_container_cpu_and_memory_with_container_id(self, container_id):
        """Get CPU and memory usage for a specific container"""
        stats_result = subprocess.run(
            [
                "docker",
                "stats",
                "--no-stream",
                "--format",
                "{{.ID}}: {{.CPUPerc}} CPU, {{.MemUsage}} RAM",
                container_id,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        stats = stats_result.stdout.strip().split(": ")[1].split(", ")
        cpu_usage = float(stats[0].replace("% CPU", "").strip())
        memory_usage = stats[1].split(" / ")[0]
        mem_value, mem_unit = (
            memory_usage[:-3],
            memory_usage[-3:],
        )
        if mem_unit == "KiB":
            memory_usage_mb = float(mem_value) / 1024
        elif mem_unit == "MiB":
            memory_usage_mb = float(mem_value)
        elif mem_unit == "GiB":
            memory_usage_mb = float(mem_value) * 1024
        else:
            memory_usage_mb = float(mem_value)
        return cpu_usage, memory_usage_mb

    @log_errors(default_return=(0, 0), raise_exception=False, log_error=False)
    def get_container_gpu_info(self, container_id):
        """Get GPU usage for a specific container"""
        container_pid = self.get_pid_id_by_container_id(container_id)
        gpu_util = self.get_container_gpu_usage(container_pid)
        gpu_mem_used = self.get_container_gpu_memory_usage(container_pid)
        return gpu_util, gpu_mem_used

    @log_errors(default_return="", raise_exception=False)
    def get_pid_id_by_container_id(self, container_id):
        """Get PID for a container ID"""
        pid_result = subprocess.run(
            [
                "docker",
                "inspect",
                "--format",
                "{{.State.Pid}}",
                container_id,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        container_pid = pid_result.stdout.strip()
        return container_pid

    @log_errors(default_return=0, raise_exception=False, log_error=False)
    def get_container_gpu_usage(self, container_pid):
        """Get GPU usage for a container PID"""
        if not has_gpu():
            return 0
        gpu_util = 0
        result = subprocess.run(
            ["nvidia-smi", "pmon", "-c", "1"],
            capture_output=True,
            text=True,
            check=True,
        )
        pmon_output = result.stdout.strip().split("\n")
        for line in pmon_output[2:]:
            parts = line.split()
            if len(parts) >= 8:
                pid = parts[1]
                gpu_usage = parts[3]
                if pid == str(container_pid):
                    gpu_util += float(gpu_usage) if gpu_usage != "-" else 0
        return gpu_util

    @log_errors(default_return=0, raise_exception=False, log_error=False)
    def get_container_gpu_memory_usage(self, container_pid):
        """Get GPU memory usage for a container PID"""
        if not has_gpu():
            return 0
        cmd = [
            "nvidia-smi",
            "--query-compute-apps=pid,used_memory",
            "--format=csv,noheader,nounits",
        ]
        total_memory = 0
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        for line in result.stdout.splitlines():
            parts = line.strip().split(", ")
            if len(parts) == 2:
                process_pid, used_memory = parts
                if process_pid == str(container_pid):
                    total_memory += int(used_memory)
        return total_memory

    @log_errors(default_return=(0, 0, 0, 0), raise_exception=False, log_error=True)
    def get_available_resources(self):
        """Get available machine resources"""
        available_memory = psutil.virtual_memory().available / 1024**3
        available_cpu = 100 - psutil.cpu_percent(1)
        gpu_memory_free, gpu_utilization = self._get_gpu_resources()
        return (
            available_memory,
            available_cpu,
            gpu_memory_free,
            gpu_utilization,
        )

    @log_errors(default_return=(0, 0.0), raise_exception=False, log_error=False)
    def _get_gpu_resources(self):
        """Get available GPU resources"""
        gpu_memory_free = 0
        gpu_utilization = 0.0
        if not has_gpu():
            return gpu_memory_free, gpu_utilization
        
        subprocess.check_output("nvidia-smi")
        info_list = get_gpu_info()
        for info in info_list:
            info_split = info.split(", ")
            gpu_memory_free += int(info_split[5])
            gpu_utilization += float(info_split[2])
        gpu_utilization /= len(info_list) if info_list else 1
        
        return gpu_memory_free, gpu_utilization


class ActionsResourcesTracker:
    """Tracks Docker container action resources"""

    def __init__(self, scaling: Scaling):
        """Initialize ActionsResourcesTracker"""
        self.scaling = scaling
        self.max_actions_usage = {}
        self.resources_tracker = ResourcesTracker()
        self.client = docker.from_env()

    @log_errors(raise_exception=False, log_error=True)
    def update_actions_resources(self):
        """Process both running and exited containers"""
        exited_containers = self.client.containers.list(
            filters={"status": "exited"},
            all=True,
        )
        running_containers = self.client.containers.list(filters={"status": "running"})
        if exited_containers:
            for container in exited_containers:
                try:
                    self._update_container_action_status(container, "completed")
                    container.remove()
                except Exception as err:
                    logging.error(
                        "Error processing exited container %s: %s",
                        container.id,
                        str(err),
                    )
        if running_containers:
            for container in running_containers:
                try:
                    self._update_container_action_status(container, "running")
                except Exception as err:
                    logging.error(
                        "Error processing running container %s: %s",
                        container.id,
                        str(err),
                    )

    @log_errors(default_return=[], raise_exception=False)
    def get_sub_containers_by_label(self, label_key, label_value):
        """Get running containers with specified label key and value"""
        containers = self.client.containers.list(
            filters={
                "label": [f"{label_key}={label_value}"],
                "status": "running",
            }
        )
        return containers

    @log_errors(raise_exception=False, log_error=True)
    def _update_container_action_status(self, container, status):
        """Update action status for a specific container"""
        inspect_data = self.client.api.inspect_container(container.id)
        start_time = inspect_data["State"]["StartedAt"]
        finish_time = (
            inspect_data["State"]["FinishedAt"]
            if status == "completed"
            else datetime.now(timezone.utc).isoformat()
        )

        def remove_quotation_marks(args):
            """Remove quotes from container args"""
            new_args = []
            for arg in args:
                new_args.extend(x.replace('"', "").replace("'", "") for x in arg.split(" "))
            return new_args

        args_24 = [arg for arg in remove_quotation_marks(inspect_data["Args"]) if len(arg) == 24 and "pypi" not in arg]
        action_record_id = args_24[-1] if args_24 else None
        if not action_record_id:
            logging.warning("No valid action_id found for the container. Container ID: %s, Args: %s", container.id, inspect_data["Args"])
        duration = calculate_time_difference(start_time, finish_time)
        (
            current_gpu_utilization,
            current_gpu_memory,
            current_cpu_utilization,
            current_memory_utilization,
        ) = self.get_current_action_usage(container, status)
        sub_containers = self.get_sub_containers_by_label("action_id", action_record_id)
        for sub_container in sub_containers:
            (
                sub_container_gpu_utilization,
                sub_container_gpu_memory,
                sub_container_cpu_utilization,
                sub_container_memory_utilization,
            ) = self.get_current_action_usage(sub_container, status)
            current_gpu_utilization += sub_container_gpu_utilization
            current_gpu_memory += sub_container_gpu_memory
            current_cpu_utilization += sub_container_cpu_utilization
            current_memory_utilization += sub_container_memory_utilization
            if status == "completed":
                try:
                    sub_container.stop()
                    sub_container.remove(force=True)
                except Exception as err:
                    logging.error(
                        "Error removing sub-container %s: %s",
                        sub_container.id,
                        str(err),
                    )
        (
            max_gpu_utilization,
            max_gpu_memory,
            max_cpu_utilization,
            max_memory_utilization,
        ) = self.update_max_action_usage(
            action_record_id,
            current_gpu_utilization,
            current_gpu_memory,
            current_cpu_utilization,
            current_memory_utilization,
        )
        logging.info(
            "Updating action status: service_provider=%s, action_id=%s, running=%s, status=%s, duration=%s, start=%s, gpu_util=%.2f%%, cpu_util=%.2f%%, gpu_mem=%dMB, mem_util=%.2f%%, created=%s, updated=%s",
            os.environ["SERVICE_PROVIDER"],
            action_record_id,
            status == "running",
            status,
            duration,
            start_time,
            max_gpu_utilization,
            max_cpu_utilization,
            max_gpu_memory,
            max_memory_utilization,
            start_time,
            finish_time,
        )
        self.scaling.update_action_status(
            service_provider=os.environ["SERVICE_PROVIDER"],
            action_record_id=action_record_id,
            isRunning=status == "running",
            status=status,
            action_duration=duration,
            docker_start_time=start_time,
            gpuUtilisation=max_gpu_utilization,
            cpuUtilisation=max_cpu_utilization,
            gpuMemoryUsed=max_gpu_memory,
            memoryUtilisation=max_memory_utilization,
            createdAt=start_time,
            updatedAt=finish_time,
        )

    @log_errors(default_return=(0, 0, 0, 0), raise_exception=False)
    def get_current_action_usage(self, container, status):
        """Get current resource usage for a container"""
        current_gpu_utilization = 0
        current_gpu_memory = 0
        current_cpu_utilization = 0
        current_memory_utilization = 0
        if status == "running":
            try:
                (
                    current_cpu_utilization,
                    current_memory_utilization,
                ) = self.resources_tracker.get_container_cpu_and_memory(container)
                (
                    current_gpu_utilization,
                    current_gpu_memory,
                ) = self.resources_tracker.get_container_gpu_info(container_id=container.id)
            except Exception as err:
                logging.error(
                    "Error getting container usage metrics: %s",
                    str(err),
                )
        return (
            current_gpu_utilization,
            current_gpu_memory,
            current_cpu_utilization,
            current_memory_utilization,
        )

    @log_errors(default_return=(0, 0, 0, 0), raise_exception=False, log_error=True)
    def update_max_action_usage(
        self,
        action_record_id,
        current_gpu_utilization,
        current_gpu_memory,
        current_cpu_utilization,
        current_memory_utilization,
    ):
        """Update and return maximum resource usage values for an action"""
        if action_record_id not in self.max_actions_usage:
            self.max_actions_usage[action_record_id] = {
                "gpu_utilization": 0,
                "gpu_memory": 0,
                "cpu_utilization": 0,
                "memory_utilization": 0,
            }
        current_values = {
            "gpu_utilization": current_gpu_utilization or 0,
            "gpu_memory": current_gpu_memory or 0,
            "cpu_utilization": current_cpu_utilization or 0,
            "memory_utilization": current_memory_utilization or 0,
        }
        for key in current_values:
            self.max_actions_usage[action_record_id][key] = max(
                current_values[key],
                self.max_actions_usage[action_record_id][key],
            )
        return (
            self.max_actions_usage[action_record_id]["gpu_utilization"],
            self.max_actions_usage[action_record_id]["gpu_memory"],
            self.max_actions_usage[action_record_id]["cpu_utilization"],
            self.max_actions_usage[action_record_id]["memory_utilization"],
        )


class MachineResourcesTracker:
    """Tracks machine-level resources like CPU, memory and GPU"""

    def __init__(self, scaling: Scaling):
        """Initialize MachineResourcesTracker"""
        self.scaling = scaling
        self.resources_tracker = ResourcesTracker()

    @log_errors(raise_exception=False, log_error=True)
    def update_available_resources(self):
        """Update available machine resources"""
        (
            available_memory,
            available_cpu,
            gpu_memory_free,
            gpu_utilization,
        ) = self.resources_tracker.get_available_resources()
        _, err, _ = self.scaling.update_available_resources(
            availableCPU=available_cpu,
            availableMemory=available_memory,
            availableGPU=100 - gpu_utilization,
            availableGPUMemory=gpu_memory_free,
        )
        if err is not None:
            logging.error(
                "Error in updating available resources: %s",
                err,
            )
