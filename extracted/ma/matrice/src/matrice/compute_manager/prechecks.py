"""Module providing prechecks functionality."""

import logging
import sys
import subprocess
from typing import Any, Optional
from matrice.compute_manager.scaling import (
    Scaling,
)
from matrice.compute_manager.actions_scaledown_manager import (
    ActionsScaleDownManager,
)
from matrice.compute_manager.resources_tracker import (
    ResourcesTracker,
    MachineResourcesTracker,
    ActionsResourcesTracker,
)
from matrice.compute_manager.instance_utils import (
    get_instance_info,
    cleanup_docker_storage,
    get_cpu_memory_usage,
    get_gpu_memory_usage,
    get_mem_usage,
    get_gpu_with_sufficient_memory_for_action,
    get_max_file_system,
    has_gpu,
)
from matrice.docker_utils import check_docker


class Prechecks:
    """Class for running pre-checks before compute operations."""

    def __init__(
        self,
        session: Any,
        instance_id: Optional[str] = None,
    ) -> None:
        """Initialize Prechecks.

        Args:
            session: Session object for RPC calls
            instance_id: Optional instance ID
        """
        self.session = session
        self.rpc = session.rpc
        self.instance_id = instance_id
        self.access_key = None
        self.secret_key = None
        self.docker_username = None
        self.docker_password = None
        self.shutdown_threshold = None
        self.launch_duration = None
        self.instance_source = None
        self.scaling = Scaling(session, instance_id)
        self.actions_scale_down_manager = ActionsScaleDownManager(self.scaling)
        self.resources_tracker = ResourcesTracker()
        self.machine_resources_tracker = MachineResourcesTracker(self.scaling)
        self.actions_resources_tracker = ActionsResourcesTracker(self.scaling)

    def setup_docker(self) -> bool:
        """
        Setup docker.

        Returns:
            bool: True if setup successful
        """
        response, error, message = self.scaling.get_docker_hub_credentials()
        if error is None:
            self.docker_username = response.get("username")
            self.docker_password = response.get("password")
        else:
            logging.error(
                "Error getting docker credentials: %s",
                error,
            )
            return False
        try:
            cmd = f"docker login -u {self.docker_username} -p {self.docker_password}"
            subprocess.run(cmd, shell=True, check=True)
            logging.info("Successfully logged into Docker")
            return True
        except subprocess.CalledProcessError as err:
            logging.error(
                "Failed to login to Docker: %s",
                str(err),
            )
            return False

    def create_docker_volume(self) -> bool:
        """
        Create docker volume.

        Returns:
            bool: True if volume created successfully
        """
        try:
            subprocess.run(
                [
                    "docker",
                    "volume",
                    "create",
                    "workspace",
                ],
                check=True,
            )
            return True
        except subprocess.CalledProcessError as err:
            logging.error(
                "Failed to create docker volume: %s",
                str(err),
            )
            return False

    def get_available_resources(self) -> bool:
        """Check available system resources are within valid ranges.

        Returns:
            bool: True if resources are within valid ranges
        """
        (
            available_memory,
            available_cpu,
            gpu_memory_free,
            gpu_utilization,
        ) = self.resources_tracker.get_available_resources()
        if any(
            resource > 100
            for resource in [
                available_memory,
                available_cpu,
            ]
        ):
            logging.error(
                "Resource usage exceeds 100%: Memory %s%%, CPU %s%%",
                available_memory,
                available_cpu,
            )
            sys.exit(1)
        if gpu_memory_free > 256:
            logging.error(
                "GPU memory exceeds 256GB limit: %sGB",
                gpu_memory_free,
            )
            sys.exit(1)
        if any(
            resource < 0
            for resource in [
                available_memory,
                available_cpu,
                gpu_memory_free,
                gpu_utilization,
            ]
        ):
            logging.error(
                "Resource usage cannot be negative: Memory %s%%, CPU %s%%, GPU Memory %sGB",
                available_memory,
                available_cpu,
                gpu_memory_free,
            )
            sys.exit(1)
        if gpu_utilization > 100:
            logging.error(
                "GPU utilization exceeds 100%%: %s%%",
                gpu_utilization,
            )
            sys.exit(1)
        logging.info("Resource availability check passed")
        return True

    def check_credentials(
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> bool:
        """Check if access key and secret key are valid.

        Args:
            access_key: Optional access key to validate
            secret_key: Optional secret key to validate

        Returns:
            bool: True if credentials are valid
        """
        if not access_key or not secret_key:
            logging.error("Missing access key or secret key")
            sys.exit(1)
        logging.info("Credentials check passed")
        return True

    def check_instance_id(self, instance_id: Optional[str] = None) -> bool:
        """Validate instance ID from args or env.

        Args:
            instance_id: Optional instance ID to validate

        Returns:
            bool: True if instance ID is valid
        """
        if not instance_id:
            logging.error("Missing instance ID")
            sys.exit(1)
        if not isinstance(instance_id, str) or len(instance_id) < 8:
            logging.error("Invalid instance ID format")
            sys.exit(1)
        self.instance_id = instance_id
        instance_info = get_instance_info(instance_id)
        if not instance_info:
            logging.error(
                "Invalid instance ID %s",
                self.instance_id,
            )
            sys.exit(1)
        logging.info(
            "Instance ID %s validated",
            self.instance_id,
        )
        return True

    def check_docker(self) -> bool:
        """Check if docker is installed and working.

        Returns:
            bool: True if docker is working
        """
        if not check_docker():
            logging.error("Docker not installed or not running")
            sys.exit(1)
        try:
            import docker

            client = docker.from_env()
            client.ping()
        except Exception as err:
            logging.error(
                "Docker API check failed: %s",
                str(err),
            )
            sys.exit(1)
        logging.info("Docker check passed")
        return True

    def check_gpu(self) -> bool:
        """Check if machine has GPU and it's functioning.

        Returns:
            bool: True if GPU check passes
        """
        gpu_mem = get_gpu_memory_usage()
        if not gpu_mem:
            logging.error("No GPU detected on this machine")
            sys.exit(1)
        if any(mem < 4 for mem in gpu_mem.values()):
            logging.error("GPU has insufficient memory (min 4GB required)")
            sys.exit(1)
        try:
            import torch

            if not torch.cuda.is_available():
                logging.error("CUDA not available")
                sys.exit(1)
        except ImportError:
            logging.warning("PyTorch not installed - skipping CUDA check")
        logging.info("GPU check passed")
        return True

    def check_resources(self) -> bool:
        """Validate system resource limits and availability.

        Returns:
            bool: True if resource checks pass
        """
        cpu_usage = get_cpu_memory_usage()
        if cpu_usage > 100:
            logging.error(
                "CPU usage exceeds 100%%: %s%%",
                cpu_usage,
            )
            sys.exit(1)
        elif cpu_usage > 90:
            logging.warning("High CPU usage: %s%%", cpu_usage)
        mem_usage = get_mem_usage()
        if mem_usage > 100:
            logging.error(
                "Memory usage exceeds 100%%: %s%%",
                mem_usage,
            )
            sys.exit(1)
        elif mem_usage > 90:
            logging.warning(
                "High memory usage: %s%%",
                mem_usage,
            )
        gpu_mem = get_gpu_memory_usage()
        if any(mem > 256 for mem in gpu_mem.values()):
            logging.error("GPU memory exceeds 256GB limit")
            sys.exit(1)
        if cpu_usage > 95 or mem_usage > 95:
            logging.error("Insufficient available resources")
            sys.exit(1)
        logging.info("Resource limits check passed")
        return True

    def cleanup_docker_storage(self) -> bool:
        """Clean up docker storage and verify space freed.

        Returns:
            bool: True if cleanup successful
        """
        try:
            initial_space = get_max_file_system()
            cleanup_docker_storage()
            final_space = get_max_file_system()
            if final_space <= initial_space:
                logging.warning("Docker cleanup did not free any space")
            return True
        except Exception as err:
            logging.error(
                "Docker storage cleanup failed: %s",
                str(err),
            )
            return False

    def get_shutdown_details(self) -> bool:
        """Get and validate shutdown details from response.

        Returns:
            bool: True if shutdown details are valid
        """
        try:
            response = self.scaling.get_shutdown_details()
            if not response:
                logging.error("Empty response from get_shutdown_details")
                return False
            required_fields = [
                "shutdownThreshold",
                "launchDuration",
                "instanceSource",
            ]
            if not all(field in response for field in required_fields):
                logging.error("Invalid shutdown details response")
                return False
            self.shutdown_threshold = response.get("shutdownThreshold")
            self.launch_duration = response.get("launchDuration")
            self.instance_source = response.get("instanceSource")
            if (
                not isinstance(
                    self.shutdown_threshold,
                    (int, float),
                )
                or self.shutdown_threshold <= 0
            ):
                logging.error("Invalid shutdown threshold")
                return False
            if (
                not isinstance(
                    self.launch_duration,
                    (int, float),
                )
                or self.launch_duration <= 0
            ):
                logging.error("Invalid launch duration")
                return False
            return True
        except Exception as err:
            logging.error(
                "Failed to get shutdown details: %s",
                str(err),
            )
            return False

    def test_gpu(self) -> bool:
        """Test if GPU is working and has sufficient memory.

        Returns:
            bool: True if GPU test passes
        """
        if has_gpu():
            action_details = {"memory_required": 4}
            gpu_indices = get_gpu_with_sufficient_memory_for_action(action_details)
            if not gpu_indices:
                logging.error("No GPU with sufficient memory")
                sys.exit(1)
            try:
                import torch

                test_tensor = torch.cuda.FloatTensor(2, 2).fill_(1.0)
                result = torch.matmul(test_tensor, test_tensor)
                if not torch.all(result == 2.0):
                    logging.error("GPU computation test failed")
                    sys.exit(1)
            except Exception as err:
                logging.error(
                    "GPU computation test failed: %s",
                    str(err),
                )
                sys.exit(1)
        return True

    def check_get_gpu_indices(self) -> bool:
        """Check if get_gpu_indices returns valid indices.

        Returns:
            bool: True if GPU indices are valid
        """
        action_details = {"memory_required": 4}
        gpu_indices = get_gpu_with_sufficient_memory_for_action(action_details)
        if not gpu_indices:
            logging.error("Failed to get GPU indices")
            sys.exit(1)
        if not all(isinstance(idx, int) and idx >= 0 for idx in gpu_indices):
            logging.error("Invalid GPU indices returned")
            sys.exit(1)
        if len(gpu_indices) != len(set(gpu_indices)):
            logging.error("Duplicate GPU indices returned")
            sys.exit(1)
        return True

    def check_resources_tracking(self) -> bool:
        """Test resource tracking updates and monitoring.

        Returns:
            bool: True if resource tracking is working
        """
        try:
            self.machine_resources_tracker.update_available_resources()
            self.actions_resources_tracker.update_actions_resources()
            return True
        except Exception as err:
            logging.error(
                "Failed to update resource tracking: %s",
                str(err),
            )
            sys.exit(1)

    def check_scaling_status(self) -> bool:
        """Test scaling service status.

        Returns:
            bool: True if scaling status is ok
        """
        try:
            downscaled_ids = self.scaling.get_downscaled_ids()
            if self.instance_id in downscaled_ids:
                logging.error("Instance is marked for downscaling")
                sys.exit(1)
            return True
        except Exception as err:
            logging.error(
                "Failed to check scaling status: %s",
                str(err),
            )
            sys.exit(1)

    def check_filesystem_space(self) -> bool:
        """Check available filesystem space and usage.

        Returns:
            bool: True if filesystem space is sufficient
        """
        max_fs = get_max_file_system()
        if not max_fs:
            logging.error("Failed to get filesystem information")
            sys.exit(1)
        return True

    def test_actions_scale_down(self) -> bool:
        """Test actions scale down.

        Returns:
            bool: True if scale down test passes
        """
        self.actions_scale_down_manager.auto_scaledown_actions()
        return True

    def check_fetch_actions(self) -> bool:
        """Test action fetching and validation.

        Returns:
            bool: True if action fetching works
        """
        fetched_actions, error, message = self.scaling.assign_jobs(has_gpu())
        if error:
            logging.error("Error assigning jobs: %s", error)
            return False
        if fetched_actions:
            if not isinstance(fetched_actions, list):
                logging.error("Invalid actions format")
                return False
            for action in fetched_actions:
                if not isinstance(action, dict) or "_id" not in action:
                    logging.error("Invalid action format")
                    return False
        return True

    def run_all_checks(
        self,
        instance_id: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> bool:
        """Run all prechecks in sequence.

        Args:
            instance_id: Optional instance ID to validate
            access_key: Optional access key to validate
            secret_key: Optional secret key to validate

        Returns:
            bool: True if all checks pass
        """
        checks = [
            lambda: self.check_credentials(access_key, secret_key),
            lambda: self.check_instance_id(instance_id),
            self.check_docker,
            self.setup_docker,
            self.create_docker_volume,
            self.check_gpu,
            self.check_resources,
            self.cleanup_docker_storage,
            self.check_filesystem_space,
            self.check_resources_tracking,
            self.check_scaling_status,
            self.get_shutdown_details,
            self.test_gpu,
            self.check_get_gpu_indices,
            self.test_actions_scale_down,
            self.check_fetch_actions,
        ]
        for check in checks:
            if not check():
                logging.error(
                    "Check failed: %s",
                    check.__name__,
                )
                return False
        logging.info("All prechecks passed successfully")
        return True
