"""Module providing instance_manager functionality."""

import json
import logging
import os
import threading
import time
from matrice.compute_manager.actions_manager import ActionsManager
from matrice.compute_manager.actions_scaledown_manager import ActionsScaleDownManager
from matrice.compute_manager.instance_utils import (
    get_instance_info,
    get_decrypted_access_key_pair,
)
from matrice.compute_manager.resources_tracker import (
    MachineResourcesTracker,
    ActionsResourcesTracker,
)
from matrice.compute_manager.scaling import Scaling
from matrice.compute_manager.shutdown_manager import ShutdownManager
from matrice.session import Session
from matrice.utils import log_errors


class InstanceManager:
    """Class for managing compute instances and their associated actions.

    Now includes auto streaming capabilities for specified deployment IDs.
    """

    def __init__(
        self,
        matrice_access_key_id="",
        matrice_secret_access_key="",
        encryption_key="",
        instance_id="",
        service_provider="",
        env="",
        gpus="",
        workspace_dir="matrice_workspace",
    ):
        """Initialize an instance manager.

        Args:
            matrice_access_key_id (str): Access key ID for Matrice authentication.
                Defaults to empty string.
            matrice_secret_access_key (str): Secret access key for Matrice
                authentication. Defaults to empty string.
            encryption_key (str): Key used for encrypting sensitive data.
                Defaults to empty string.
            instance_id (str): Unique identifier for this compute instance.
                Defaults to empty string.
            service_provider (str): Cloud service provider being used.
                Defaults to empty string.
            env (str): Environment name (e.g. dev, prod).
                Defaults to empty string.
            gpus (str): GPU configuration string (e.g. "0,1").
                Defaults to empty string.
            workspace_dir (str): Directory for workspace files.
                Defaults to "matrice_workspace".
        """
        self.session = self._setup_env_credentials(
            env,
            service_provider,
            instance_id,
            encryption_key,
            matrice_access_key_id,
            matrice_secret_access_key,
        )
        os.environ["WORKSPACE_DIR"] = str(workspace_dir)
        os.environ["GPUS"] = json.dumps(gpus)
        self.scaling = Scaling(
            self.session,
            os.environ.get("INSTANCE_ID"),
        )
        logging.info("InstanceManager initialized with scaling")
        jupyter_token = os.environ.get("JUPYTER_TOKEN")
        if jupyter_token:
            self.scaling.update_jupyter_token(jupyter_token)
            logging.info("InstanceManager updated Jupyter token")
        else:
            logging.warning("No Jupyter token found in environment variables")
        self.current_actions = {}
        self.actions_manager = ActionsManager(self.scaling)
        logging.info("InstanceManager initialized with actions manager")
        self.scale_down_manager = ActionsScaleDownManager(self.scaling)
        logging.info("InstanceManager initialized with scale down manager")
        self.shutdown_manager = ShutdownManager(self.scaling)
        logging.info("InstanceManager initialized with shutdown manager")
        self.machine_resources_tracker = MachineResourcesTracker(self.scaling)
        logging.info("InstanceManager initialized with machine resources tracker")
        self.actions_resources_tracker = ActionsResourcesTracker(self.scaling)
        logging.info("InstanceManager initialized with actions resources tracker")
        self.poll_interval = 10
        self.encryption_key = None
        logging.info("InstanceManager initialized.")

    @log_errors(default_return=None, raise_exception=True, log_error=True)
    def _setup_env_credentials(
        self,
        env,
        service_provider,
        instance_id,
        encryption_key,
        matrice_access_key_id,
        matrice_secret_access_key,
    ):
        """Set up environment credentials.

        Args:
            env (str): Environment name
            service_provider (str): Cloud service provider
            instance_id (str): Instance identifier
            encryption_key (str): Encryption key
            matrice_access_key_id (str): Matrice access key ID
            matrice_secret_access_key (str): Matrice secret access key

        Returns:
            Session: Initialized session object

        Raises:
            Exception: If required environment variables are not set
        """
        try:
            (
                auto_service_provider,
                auto_instance_id,
            ) = get_instance_info()
        except Exception as exc:
            logging.error(
                "Error getting instance info: %s",
                str(exc),
            )
            auto_service_provider = ""
            auto_instance_id = ""
        manual_instance_info = {
            "ENV": env or os.environ.get("ENV"),
            "SERVICE_PROVIDER": service_provider
            or os.environ.get("SERVICE_PROVIDER")
            or auto_service_provider,
            "INSTANCE_ID": instance_id
            or os.environ.get("INSTANCE_ID")
            or auto_instance_id,
            "MATRICE_ENCRYPTION_KEY": encryption_key
            or os.environ.get("MATRICE_ENCRYPTION_KEY"),
            "MATRICE_ACCESS_KEY_ID": matrice_access_key_id
            or os.environ.get("MATRICE_ACCESS_KEY_ID"),
            "MATRICE_SECRET_ACCESS_KEY": matrice_secret_access_key
            or os.environ.get("MATRICE_SECRET_ACCESS_KEY"),
        }
        for (
            key,
            value,
        ) in manual_instance_info.items():
            os.environ[key] = value
        if not (os.environ.get("SERVICE_PROVIDER") and os.environ.get("INSTANCE_ID")):
            raise Exception(
                "SERVICE_PROVIDER and INSTANCE_ID must be set as environment variables or passed as arguments"
            )
        self.encryption_key = manual_instance_info["MATRICE_ENCRYPTION_KEY"]

        access_key = manual_instance_info["MATRICE_ACCESS_KEY_ID"]
        secret_key = manual_instance_info["MATRICE_SECRET_ACCESS_KEY"]

        if (  # Keys are not encrypted
            self.encryption_key
            and access_key
            and secret_key
            and len(access_key) != 21
            and len(secret_key) != 21
        ):
            access_key, secret_key = self._decrypt_access_key_pair(
                access_key,
                secret_key,
                self.encryption_key,
            )
        os.environ["MATRICE_SECRET_ACCESS_KEY"] = secret_key
        os.environ["MATRICE_ACCESS_KEY_ID"] = access_key
        os.environ["MATRICE_ENCRYPTION_KEY"] = self.encryption_key
        return Session(
            account_number="",
            secret_key=secret_key,
            access_key=access_key,
        )

    @log_errors(default_return=(None, None), raise_exception=False)
    def _decrypt_access_key_pair(
        self,
        enc_access_key,
        enc_secret_key,
        encryption_key="",
    ):
        """Decrypt the access key pair.

        Args:
            enc_access_key (str): Encrypted access key
            enc_secret_key (str): Encrypted secret key
            encryption_key (str): Key for decryption. Defaults to empty string.

        Returns:
            tuple: Decrypted (access_key, secret_key) pair
        """
        return get_decrypted_access_key_pair(
            enc_access_key,
            enc_secret_key,
            encryption_key,
        )

    @log_errors(raise_exception=True, log_error=True)
    def start_instance_manager(self):
        """Run the instance manager loop."""
        while True:
            try:
                self.shutdown_manager.handle_shutdown(
                    bool(self.actions_manager.get_current_actions())
                )
            except Exception as exc:
                logging.error(
                    "Error in shutdown_manager handle_shutdown: %s",
                    str(exc),
                )
            try:
                self.scale_down_manager.auto_scaledown_actions()
            except Exception as exc:
                logging.error(
                    "Error in scale_down_manager auto_scaledown_actions: %s",
                    str(exc),
                )
            try:
                self.machine_resources_tracker.update_available_resources()
            except Exception as exc:
                logging.error(
                    "Error in machine_resources_tracker update_available_resources: %s",
                    str(exc),
                )
            try:
                self.actions_resources_tracker.update_actions_resources()
            except Exception as exc:
                logging.error(
                    "Error in actions_resources_tracker update_actions_resources: %s",
                    str(exc),
                )

            time.sleep(self.poll_interval)

    @log_errors(default_return=(None, None), raise_exception=True)
    def start(self):
        """Start the instance manager threads.

        Returns:
            tuple: (instance_manager_thread, actions_manager_thread)
        """
        # Create and start threads
        instance_manager_thread = threading.Thread(
            target=self.start_instance_manager,
            name="InstanceManager",
        )
        instance_manager_thread.start()

        actions_manager_thread = threading.Thread(
            target=self.actions_manager.start_actions_manager,
            name="ActionsManager",
        )
        actions_manager_thread.start()

        return (
            instance_manager_thread,
            actions_manager_thread,
        )
