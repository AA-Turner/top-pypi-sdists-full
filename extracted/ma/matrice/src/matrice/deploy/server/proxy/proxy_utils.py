"""Module providing proxy_utils functionality for authentication and request logging."""

import logging
import threading
import time
from datetime import datetime
from queue import Queue
from typing import Any, Dict, Set
import numpy as np
import requests


class AuthKeyValidator:
    """Validates authentication keys for deployments."""

    def __init__(self, deployment_id: str, session: Any) -> None:
        """Initialize the AuthKeyValidator.

        Args:
            deployment_id: ID of the deployment
            session: Session object containing RPC client
        """
        self.deployment_id = deployment_id
        self.session = session
        self.rpc = self.session.rpc
        self.auth_keys_info = None
        self.auth_keys: Set[str] = set()
        self._stop = False

    def __call__(self, auth_key: str) -> bool:
        """Check if an auth key is valid.

        Args:
            auth_key: Authentication key to validate

        Returns:
            bool: True if key is valid, False otherwise
        """
        return auth_key in self.auth_keys

    def _parse_expiry_time(self, expiry_time_str: str) -> float:
            # Handle different ISO format variations
            try:
                # Replace Z with timezone if needed
                if expiry_time_str.endswith("Z"):
                    expiry_time_str = expiry_time_str.replace("Z", "+00:00")
                
                # Normalize ISO format for proper parsing
                if '.' in expiry_time_str:
                    main, rest = expiry_time_str.split('.', 1)
                    if '+' in rest:
                        frac, tz = rest.split('+', 1)
                        frac = (frac + '000000')[:6]  # pad/truncate to 6 digits
                        expiry_time_str = f"{main}.{frac}+{tz}"
                    elif '-' in rest:
                        frac, tz = rest.split('-', 1)
                        frac = (frac + '000000')[:6]  # pad/truncate to 6 digits
                        expiry_time_str = f"{main}.{frac}-{tz}"
            except Exception as err:
                logging.error("Error parsing expiry time: %s", str(err))
                expiry_time_str = expiry_time_str.replace("Z", "+00:00")
            return datetime.fromisoformat(expiry_time_str).timestamp()
    
    def update_auth_keys(self) -> None:
        """Fetch and validate auth keys for the deployment."""      
        try:
            response = self.rpc.get(f"/v1/inference/{self.deployment_id}", raise_exception=False)
            if not response.get("success"):
                logging.error("Failed to fetch auth keys")
                return
            if response["data"]["authKeys"]:
                self.auth_keys_info = response["data"]["authKeys"]
            else:
                self.auth_keys_info = []
            if not self.auth_keys_info:
                logging.debug("No auth keys found for deployment")
                return
            current_time = time.time()
            self.auth_keys.clear()
            for auth_key_info in self.auth_keys_info:
                try:
                    expiry_time = self._parse_expiry_time(auth_key_info["expiryTime"])
                    if expiry_time > current_time:
                        self.auth_keys.add(auth_key_info["key"])
                    else:
                        logging.debug("Skipping expired auth key")
                except (
                    ValueError,
                    KeyError,
                ) as err:
                    logging.error(
                        "Invalid auth key data: %s",
                        err,
                    )
                    continue
            logging.debug(
                "Successfully loaded %d valid auth keys",
                len(self.auth_keys),
            )
        except Exception as err:
            logging.error(
                "Error fetching auth keys: %s",
                str(err),
            )
            raise

    def update_auth_keys_loop(self) -> None:
        """Run continuous loop to update auth keys."""
        while not self._stop:
            try:
                self.update_auth_keys()
                time.sleep(60)
            except Exception as err:
                logging.error(
                    "Error in auth key update loop: %s",
                    str(err),
                )
                time.sleep(5)

    def start(self) -> None:
        """Start the auth key update loop in a background thread."""
        threading.Thread(
            target=self.update_auth_keys_loop,
            daemon=True,
        ).start()

    def stop(self) -> None:
        """Stop the auth key update loop."""
        self._stop = True


class RequestsLogger:
    """Logs prediction requests and handles drift monitoring."""

    def __init__(self, deployment_id: str, session: Any) -> None:
        """Initialize the RequestsLogger.

        Args:
            deployment_id: ID of the deployment
            session: Session object containing RPC client
        """
        self.deployment_id = deployment_id
        self.session = session
        self.rpc = self.session.rpc
        self.log_prediction_info_queue: Queue = Queue()
        self._stop = False

    def add_log_to_queue(
        self,
        prediction: Any,
        latency: float,
        request_time: str,
        input_data: bytes,
        deployment_instance_id: str,
        auth_key: str,
    ) -> None:
        """Add prediction log to queue for async processing.

        Args:
            prediction: The model prediction
            latency: Request latency in seconds
            request_time: Timestamp of the request
            input_data: Raw input data bytes
            deployment_instance_id: ID of deployment instance
            auth_key: Authentication key used
        """
        self.log_prediction_info_queue.put(
            (
                prediction,
                latency,
                request_time,
                input_data,
                deployment_instance_id,
                auth_key,
            )
        )

    def log_prediction_info(
        self,
        prediction: Any,
        latency: float,
        request_time: str,
        input_data: bytes,
        deployment_instance_id: str,
        auth_key: str,
    ) -> Dict:
        """Log prediction information to the server.

        Args:
            prediction: The model prediction
            latency: Request latency in seconds
            request_time: Timestamp of the request
            input_data: Raw input data bytes
            deployment_instance_id: ID of deployment instance
            auth_key: Authentication key used

        Returns:
            Dict: Response from logging endpoint
        """
        try:
            logging.debug("Logging prediction info")
            payload = {
                "prediction": (
                    prediction.tolist() if isinstance(prediction, np.ndarray) else prediction
                ),
                "latency": latency,
                "reqTime": request_time,
                "_idDeploymentInstance": deployment_instance_id,
                "isMLAssisted": False,
                "authKey": auth_key,
            }
            log_response = self.rpc.post(
                path=f"/v1/model_prediction/log_prediction_info/{self.deployment_id}",
                payload=payload,
            )
            if log_response.get("success"):
                self.upload_input_for_drift_monitoring(log_response, input_data)
                logging.debug("Successfully logged prediction info")
            else:
                logging.warning(
                    "Failed to log prediction: %s",
                    log_response.get("message"),
                )
            return log_response
        except Exception as err:
            logging.warning(
                "Failed to log prediction info: %s",
                err,
            )
            return None

    def upload_input_for_drift_monitoring(
        self,
        log_response: Dict,
        input_data: bytes,
    ) -> None:
        """Upload input data for drift monitoring.

        Args:
            log_response: Response from logging endpoint
            input_data: Raw input data bytes
        """
        if not log_response.get("success") or not log_response.get("data"):
            return
        urls = log_response.get("data")
        if not isinstance(urls, list):
            logging.warning("Invalid URL data format for drift monitoring")
            return
        for url in urls:
            try:
                response = requests.put(
                    url,
                    data=input_data,
                    timeout=30,
                )
                if response.status_code != 200:
                    logging.warning(
                        "Failed to upload input for drift monitoring: %d",
                        response.status_code,
                    )
            except Exception as err:
                logging.warning(
                    "Failed to upload input for drift monitoring: %s",
                    err,
                )

    def log_prediction_info_thread(self) -> None:
        """Background thread for processing prediction logs."""
        logging.debug("Starting prediction info logging thread")
        while not self._stop or not self.log_prediction_info_queue.empty():
            try:
                (
                    prediction,
                    latency,
                    request_time,
                    input_data,
                    instance_id,
                    auth_key,
                ) = self.log_prediction_info_queue.get()
                self.log_prediction_info(
                    prediction,
                    latency,
                    request_time,
                    input_data,
                    instance_id,
                    auth_key,
                )
            except Exception as err:
                logging.error(
                    "Error in prediction info logging thread: %s",
                    err,
                )

    def start(self) -> None:
        """Start the prediction logging thread."""
        threading.Thread(
            target=self.log_prediction_info_thread,
            daemon=True,
        ).start()

    def stop(self) -> None:
        """Stop the prediction logging thread."""
        self._stop = True
