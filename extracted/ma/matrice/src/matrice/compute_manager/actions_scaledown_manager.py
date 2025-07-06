"""Module providing actions_scaledown_manager functionality."""

import logging
import docker
from matrice.compute_manager.scaling import (
    Scaling,
)
from matrice.utils import log_errors


class ActionsScaleDownManager:
    """Class for managing container scale down operations."""

    def __init__(self, scaling: Scaling):
        """Initialize the scale down manager.

        Args:
            scaling (Scaling): Scaling service instance
        """
        self.docker_client = docker.from_env()
        self.scaling = scaling

    @log_errors(raise_exception=False, log_error=True)
    def auto_scaledown_actions(self):
        """Start polling for containers that need to be scaled down and stop them."""
        down_scaled_jobs, error, _ = self.scaling.get_downscaled_ids()
        if error is not None:
            logging.error(
                "Error getting downscaled ids: %s",
                error,
            )
            return
        containers = self.docker_client.containers.list(
            filters={"status": "running"},
            all=True,
        )
        if down_scaled_jobs:
            for container in containers:
                container_id = container.id
                inspect_data = self.docker_client.api.inspect_container(container_id)
                action_record_id = next(
                    (arg for arg in inspect_data["Args"] if len(arg) == 24),
                    None,
                )
                if action_record_id in down_scaled_jobs:
                    try:
                        container.stop()
                        logging.info(
                            "Container %s stopped.",
                            container_id,
                        )
                    except docker.errors.APIError as err:
                        logging.error(
                            "Failed to stop container %s: %s",
                            container_id,
                            str(err),
                        )
