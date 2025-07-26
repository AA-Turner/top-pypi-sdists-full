"""Module providing actions_manager functionality."""

import logging
import os
import time
from matrice.compute_manager.action_instance import (
    ActionInstance,
)
from matrice.compute_manager.instance_utils import (
    has_gpu,
    get_mem_usage,
    cleanup_docker_storage,
)
from matrice.compute_manager.scaling import (
    Scaling,
)
from matrice.utils import log_errors


class ActionsManager:
    """Class for managing actions."""

    def __init__(self, scaling: Scaling):
        """Initialize an action manager.

        Args:
            scaling (Scaling): Scaling service instance
        """
        self.current_actions: dict[str, ActionInstance] = {}
        self.scaling = scaling
        self.memory_threshold = 0.9
        self.poll_interval = 10
        self.last_actions_check = 0
        logging.info("ActionsManager initialized")

    @log_errors(default_return=[], raise_exception=False)
    def fetch_actions(self):
        """Poll for actions and process them if memory threshold is not exceeded.

        Returns:
            list: List of fetched actions
        """
        actions = []
        logging.info("Polling backend for new jobs")
        fetched_actions, error, _ = self.scaling.assign_jobs(has_gpu())
        if error:
            logging.error("Error assigning jobs: %s", error)
            return actions
        if not isinstance(fetched_actions, list):
            fetched_actions = [fetched_actions]
        for action in fetched_actions:
            if not action:
                continue
            if action["_id"] != "000000000000000000000000":
                actions.append(action)
                logging.info(
                    "Fetched action details: %s",
                    actions,
                )
        return actions

    @log_errors(default_return=None, raise_exception=False)
    def process_action(self, action):
        """Process the given action.

        Args:
            action (dict): Action details to process

        Returns:
            ActionInstance: Processed action instance or None if failed
        """
        logging.info(
            "Processing action: %s",
            action["_id"],
        )
        action_instance = ActionInstance(self.scaling, action)
        self.scaling.update_action_status(
            service_provider=os.environ["SERVICE_PROVIDER"],
            action_record_id=action["_id"],
            status="starting",
            action_duration=0,
        )
        logging.info("locking action")
        self.scaling.update_action_status(
            service_provider=os.environ["SERVICE_PROVIDER"],
            status="started",
            action_record_id=action["_id"],
            isRunning=True,
            action_duration=0,
            cpuUtilisation=0.0,
            gpuUtilisation=0.0,
            memoryUtilisation=0.0,
            gpuMemoryUsed=0,
        )
        self.scaling.update_status(
            action["_id"],
            action["action"],
            "bg-job-scheduler",
            "JBSS_LCK",
            "OK",
            "Job is locked for processing",
        )
        action_instance.execute()
        logging.info(
            "action %s started.",
            action_instance.action_record_id,
        )
        return action_instance

    @log_errors(raise_exception=False)
    def process_actions(self):
        """Process fetched actions."""
        for action in self.fetch_actions():
            action_instance = self.process_action(action)
            if action_instance:
                self.current_actions[action["_id"]] = action_instance

    @log_errors(raise_exception=False)
    def purge_unwanted(self):
        """Purge completed or failed actions.
        
        This method checks all actions in the current_actions dictionary and removes any that:
        1. Are explicitly reported as not running by the is_running() method
        2. Have invalid or corrupted process objects
        """
        purged_count = 0
        
        # Check each action and purge if needed
        for action_id, instance in list(self.current_actions.items()):
            should_purge = False
            purge_reason = ""
            
            # Check if process is reported as not running
            if not instance.is_running():
                should_purge = True
                purge_reason = "process reported as not running"
            
            # Check for process object validity
            elif not hasattr(instance, 'process') or instance.process is None:
                should_purge = True
                purge_reason = "invalid process object"
            
            # Purge if any condition was met
            if should_purge:
                logging.info(
                    "Action %s is being purged: %s",
                    action_id,
                    purge_reason
                )
                
                # Remove from tracking dictionaries
                del self.current_actions[action_id]
                purged_count += 1

                # Try to explicitly stop the action if possible
                try:
                    if hasattr(instance, 'stop'):
                        instance.stop()
                except Exception as e:
                    logging.error(f"Error stopping action {action_id}: {str(e)}")
        
        if purged_count > 0:
            logging.info(
                "Purged %d completed actions, %d actions remain in queue",
                purged_count,
                len(self.current_actions)
            )

    @log_errors(default_return={}, raise_exception=False)
    def get_current_actions(self):
        """Get the current actions.

        This method:
        1. Purges any completed actions using purge_unwanted()
        2. Double-checks remaining actions to ensure they are truly running
        3. Provides detailed logging about current actions state

        Returns:
            dict: Current active actions
        """
        # Always purge unwanted actions first
        self.purge_unwanted()
        if self.current_actions:
            action_ids = list(self.current_actions.keys())
            logging.info(
                "Currently running %d actions: %s",
                len(self.current_actions),
                action_ids
            )
        else:
            logging.debug("No actions currently running")
            return {}
        return self.current_actions

    @log_errors(raise_exception=True)
    def start_actions_manager(self):
        """Start the actions manager main loop."""
        while True:
            try:
                mem_usage = get_mem_usage()
                logging.info("Memory usage: %d", mem_usage)
                waiting_time = int(
                    min(
                        self.poll_interval
                        / max(
                            0.001,
                            self.memory_threshold - mem_usage,
                        ),
                        120,
                    )
                )
                if mem_usage < self.memory_threshold:
                    self.process_actions()
                    logging.info(
                        "Waiting for %d seconds before next poll",
                        waiting_time,
                    )
                else:
                    logging.info(
                        "Memory threshold exceeded, waiting for %d seconds",
                        waiting_time,
                    )
                cleanup_docker_storage()
            except Exception as e:
                logging.error("Error in actions manager: %s", e)
            time.sleep(waiting_time)
