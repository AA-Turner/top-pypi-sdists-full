"""Module containing Data Store subscription related classes"""

import atexit
import json
import signal
import ssl
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import certifi

import paho.mqtt.client as mqtt
from eumdac.logging import logger
from eumdac.signals import signal_registry

# Constants for reconnecting to the MQTT server
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 5
MAX_RECONNECT_DELAY = 60
VERSION = 5


class EumdacMQTTClient:
    """
    EUMDAC MQTTClient implementation. Wraps a mqtt.Client instance.
    """

    def __init__(
        self, endpoint: str, username: Optional[str] = None, password: Optional[str] = None
    ):
        """Initialize the client for an endpoint with optional authentication."""
        self.client = mqtt.Client(
            client_id=str(uuid.uuid4()),
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            transport="tcp",
            protocol=mqtt.MQTTv5,
        )
        self.endpoint = endpoint
        self.topic_list: List[Tuple[str, int]] = []
        self.download_dir = Path(".")
        self.downloadProducts = False
        self.setup_tls()
        self.setup_callbacks()
        if username or password:
            self.client.username_pw_set(username, password)
        self.on_msg_callbacks: List[Callable[[Any, Any, Any, Any], None]] = []

    def setup_tls(self) -> None:
        """Configure network encryption settings."""
        self.client.tls_set(
            ca_certs=certifi.where(),
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )

    def add_on_msg_callback(self, func: Callable[[Any, Any, Any, Any], None]) -> None:
        """Add a message callback function"""
        self.on_msg_callbacks.append(func)

    def setup_callbacks(self) -> None:
        """Setup internal callbacks"""
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        self.client.on_log = self.on_log

    def connect(self) -> None:
        """Establish a connection with the established configuration."""
        logger.debug("Connecting to %s", self.endpoint)
        try:
            self.client.connect(
                self.endpoint.split(":")[0],
                int(self.endpoint.split(":")[1]),
                clean_start=True,
                bind_address="",
                keepalive=10,  # Increased keepalive interval
            )
        except Exception as e:
            logger.error(f"Connection failed: {e}")

    def add_subscription(self, topic: str, qos: int = 1) -> bool:
        """
        Set a subscription for a specific topic with a given QoS.

        Args:
            topic (str): The topic to subscription to.
            qos (int): The quality of service level for the subscription.

        Returns:
            bool: True if a new subscription is added, False if the subscription already exists with the same QoS.

        Raises:
            ValueError: If the subscription already exists with a different QoS.

        """
        for i, (t, q) in enumerate(self.topic_list):
            if t == topic:
                if q != qos:
                    raise ValueError(
                        f"Subscription for topic {topic} already exists with a different QoS"
                    )
                else:
                    logger.debug(f"Topic {topic} already subscriptiond with QoS {qos}")
                    return False
        self.topic_list.append((topic, qos))
        logger.debug(f"Subscribing to {topic} with QoS {qos}")
        return True

    def subscribe(self, topic: str, qos: int = 1) -> None:
        """Subscribe to a given topic with a target QoS"""
        if self.add_subscription(topic, qos):
            logger.debug(f"Subscribing to {topic} with QoS {qos}")
            self.client.subscribe(topic, qos)

    def subscribe_all(self) -> None:
        """Subscribe to all the registered topics"""
        for topic, qos in self.topic_list:
            self.client.subscribe(topic, qos)

    def on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        disconnect_flags: mqtt.DisconnectFlags,
        reasoncode: mqtt.ReasonCode,
        properties: Optional[mqtt.Properties],
    ) -> None:
        """Handler for disconnection event, will try to re-establish the connection."""
        logger.debug(f"Disconnected with result code: {reasoncode}")
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logger.debug(f"Reconnecting in {reconnect_delay} seconds...")
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logger.debug("Reconnected successfully!")
                self.renew_subscriptions()
                return
            except Exception as err:
                logger.error(f"Reconnect failed: {err}. Retrying...")

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logger.debug(f"Reconnect failed after {reconnect_count} attempts. Exiting...")

    def on_connect(
        self, client: Any, userdata: Any, flags: Any, reason_code: Any, properties: Any
    ) -> None:
        """Handler for connection event."""
        if reason_code.is_failure:
            raise MQTTConnectionError(
                f"Failed to connect: {reason_code}. loop_forever() will retry connection"
            )
        else:
            logger.debug(f"Connected with result code {reason_code}")
            self.renew_subscriptions()

    def renew_subscriptions(self) -> None:
        """Renew all the already established subscriptions."""
        logger.debug("Renewing subscriptions")
        self.subscribe_all()

    def on_message(self, client: Any, userdata: Any, message: Any, properties: Any = None) -> None:
        """Handler for the message received event. Triggers registered callbacks."""
        logger.debug(f"Received message on topic: {message.topic}")
        for callback in self.on_msg_callbacks:
            callback(client, userdata, message, properties)

    def on_subscribe(
        self,
        client: mqtt.Client,
        userdata: Any,
        mid: int,
        reason_code_list: List[mqtt.ReasonCode],
        properties: Optional[mqtt.Properties],
    ) -> None:
        """Handler for the subscription event."""
        logger.debug(f"{datetime.now()} Subscription started")

    def on_log(self, client: Any, userdata: Any, level: Any, buf: str) -> None:
        """Handler for the log event."""
        return


def subscription_json_to_args_dict(d: Dict[str, Any]) -> Dict[str, str]:
    """Returns relevant subscription event data in dict format."""
    ret = {}
    try:
        ret["collection"] = d["_eumetsat_product_information"]["parentIdentifier"]
        ret["product"] = d["properties"]["data_id"]
    except KeyError as e:
        raise InsufficientInfoError(str(e)) from e
    except TypeError as e:
        raise CorruptedJsonError(str(e)) from e
    return ret


class MQTTConnectionError(Exception):
    """Error raised on MQTT connection failures."""

    pass


class CorruptedJsonError(Exception):
    """Error raised on Json parsing errors."""

    pass


class InsufficientInfoError(Exception):
    """Error raised when messages miss important values."""

    pass


def extract_payload(message: Any, parse_times: bool = False) -> Dict[str, Any]:
    """Returns the payload from the received message, ready for processing."""
    try:
        payload = message.payload.decode("utf-8") if message.payload else ""
    except UnicodeDecodeError as e:
        logger.error(f"UnicodeDecodeError: {e}")
    try:
        json_data = json.loads(payload)
    except json.JSONDecodeError as e:
        logger.warning(
            f"JSON error in mqtt message, exception: {e}, "
            f"topic: {message.topic}, payload: {message.payload}"
        )
    if parse_times:
        for dt in ["datetime", "start_datetime", "end_datetime", "pubtime"]:
            # Handle notifications without start_datetime or end_datetime, only datetime
            if not dt in json_data["properties"]:
                continue
            original_dt_str = json_data["properties"][dt]
            # Remove the 'Z' if present
            original_dt_str = original_dt_str.replace("Z", "")
            # Ensure the fractional part is always present and has exactly 6 digits
            if "." in original_dt_str:
                main_part, fractional_part = original_dt_str.split(".")
                # Pad the fractional part with zeros to ensure it has 6 digits
                fractional_part = fractional_part.ljust(6, "0")[
                    :6
                ]  # Ensure it has exactly 6 digits
                modified_dt_str = f"{main_part}.{fractional_part}"
            else:
                # If there's no fractional part, we can add a default one (e.g., '.000000')
                modified_dt_str = f"{original_dt_str}.000000"
            # Parse the modified datetime string
            json_data["properties"][dt] = datetime.fromisoformat(modified_dt_str)
    return json_data


class TimeWindow:
    """Helper class for working with time windows."""

    def __init__(self, start: datetime, end: datetime):
        """Init with start and end datetimes."""
        self.start = start
        self.end = end

    def overlaps_with(self, other: "TimeWindow") -> bool:
        """ "Check if the time windows do overlap"""
        return not (self.end <= other.start or self.start >= other.end)

    def contains(self, time: datetime) -> bool:
        """Check if the time is within the time window."""
        return self.start <= time <= self.end


class ProcessFile:
    """Subscription process file for managing listeners and downloaders."""

    def __init__(self, path: Path, contents: str):
        """Create the file and setup cleanup handlers."""
        signal_registry.register(signal.SIGINT, self.cleanup)
        # signal_registry.register(signal.SIGTERM, self.cleanup)
        if not sys.platform.startswith("win"):
            signal_registry.register(signal.SIGQUIT, self.cleanup)
            signal_registry.register(signal.SIGHUP, self.cleanup)
        self.path = Path(path)
        with self.path.open("w") as f:
            f.write(contents)
        atexit.register(self.cleanup)

    def cleanup(self) -> None:
        """Unlink the process file, if not already done."""
        try:
            self.path.unlink()
        except FileNotFoundError:
            # Don't care if the file was already deleted
            pass
