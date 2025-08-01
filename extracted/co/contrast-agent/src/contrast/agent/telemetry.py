# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections import defaultdict
from functools import cached_property
import hashlib
import os
from pathlib import Path
import queue
import threading
import time
import uuid
import sys

import contrast

from contrast.agent import agent_state
from contrast import __version__
from contrast.agent import scope
from contrast import AGENT_CURR_WORKING_DIR
from contrast.agent.settings import Settings
from contrast_vendor import structlog as logging
from requests import post as post_request, get as get_request
from contrast.agent.events import StartupMetricsTelemetryEvent, ErrorTelemetryEvent

logger = logging.getLogger("contrast")

FILE_LOCATIONS = [
    # Most stable place but some OS may not allow creating here
    "/etc/contrast/python/",
    os.path.join(AGENT_CURR_WORKING_DIR, "config", "contrast"),
]

DISCLAIMER = (
    "The Contrast Python Agent collects usage data "
    "in order to help us improve compatibility and security coverage. "
    "The data is anonymous and does not contain application data. "
    "It is collected by Contrast and is never shared. "
    "You can opt-out of telemetry by setting the "
    "CONTRAST_AGENT_TELEMETRY_OPTOUT environment variable to '1' or 'true'. "
    "Read more about Contrast Python Agent telemetry: "
    "https://docs.contrastsecurity.com/en/python-telemetry.html"
)

BASE_URL = "https://telemetry.python.contrastsecurity.com"
BASE_ENDPOINT = "api/v1/telemetry"
URL = f"{BASE_URL}/{BASE_ENDPOINT}"
HEADERS = {"User-Agent": f"python-{__version__}"}

TELEMETRY_THREAD_NAME = "ContrastTelemetry"


class Telemetry(threading.Thread):
    # While the telemetry spec suggests waiting for 3 hours, we've decided
    # that 30 minutes is reasonable for this agent.
    WAIT = 60 * 30  # 30 mins
    RETRY_WAIT = 60
    QUEUE_GET_TIMEOUT = 5
    REPORTED_ERRORS = {}
    # Limit the number of messages stored each reporting period.
    MAX_MESSAGES = 300

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.name = TELEMETRY_THREAD_NAME

        self.enabled = True
        self.is_public_build = True
        self.message_q = queue.Queue(maxsize=100)
        self._stopper = object()  # sentinel sent over message_q to stop the thread
        self._msgs = defaultdict(list)
        self._msg_count = 0
        self.settings = Settings()

    def stop(self):
        self.message_q.put(self._stopper)
        timeout = 30
        self.join(timeout)
        if self.is_alive():
            logger.warn("failed to stop Telemetry thread", timeout=timeout)

    @cached_property
    def instance_id(self):
        if self._mac_addr is None:
            return "_" + uuid.uuid4().hex
        return self._sha256(hex(self._mac_addr))

    @cached_property
    def application_id(self):
        if self._mac_addr is None:
            return "_" + uuid.uuid4().hex
        return self._sha256(hex(self._mac_addr) + agent_state.get_app_name())

    @cached_property
    def _mac_addr(self):
        """
        The MAC address for the current machine's primary network adapter as a base-10
        integer. If we find a multicast MAC address, return None.
        See _is_multicast_mac_address.
        """
        _mac_addr = uuid.getnode()
        if self._is_multicast_mac_address(_mac_addr):
            return None
        return _mac_addr

    def run(self):
        self._check_enabled()

        if not self.enabled:
            return

        # Ensure thread runs in scope because it is initialized
        # before our thread.start patch is applied.
        with scope.contrast_scope():
            logger.debug("Starting telemetry thread")

            # Do not move creating startup msg outside of this function
            # so the work stays in the telemetry thread, not the main thread.
            startup_msg = StartupMetricsTelemetryEvent(self.instance_id)
            logger.debug("Sending StartupMetrics msg: %s", startup_msg)
            self._store_message(startup_msg)
            self._send_messages()  # send StartupMetrics immediately

            # send first message immediately, future messages will be sent after wait_time.
            next_send_time = time.time()
            while self.settings.is_agent_config_enabled():
                try:
                    msg = self.message_q.get(block=True, timeout=self.QUEUE_GET_TIMEOUT)
                    if msg is self._stopper:
                        self._send_messages()
                        break
                    self._store_message(msg)
                    now = time.time()
                    if now >= next_send_time:
                        wait_time = self._send_messages()
                        next_send_time = now + wait_time
                except queue.Empty:
                    pass
                except Exception as e:
                    logger.debug(
                        "WARNING: reporting client failed to send message", exc_info=e
                    )

    def add_message(self, msg):
        if not self.enabled or msg is None:
            return

        logger.debug("Adding msg to telemetry queue: %s", msg)
        try:
            self.message_q.put_nowait(msg)
        except queue.Full:
            logger.debug("WARNING: Telemetry queue is full, dropping message", msg=msg)

    def _send_messages(self) -> int:
        """
        Send all stored messages, one batch request for each path for group of
        messages. Returns a time in seconds that a caller should wait before
        sending messages again.
        """
        # It would be more natural to iterate over self._msgs.items() here, but
        # if a retry_after response is sent, we can't easily remove already sent
        # messages from self._msgs or save still-to-be-sent messages from within
        # the items() loop. Instead, we pop individual messages to handle this
        # case.
        for _ in range(len(self._msgs)):
            path, messages = self._msgs.popitem()
            self._msg_count -= len(messages)
            try:
                response = self._post(messages, path)
                if retry_wait := self._retry_after(response):
                    # readd message so it can be sent again after retry_wait.
                    self._msgs[path] = messages
                    return retry_wait
            except Exception as ex:
                logger.debug(
                    "Could not send batch of telemetry messages.", exception=str(ex)
                )

        return self.WAIT

    def _store_message(self, msg):
        if self._msg_count >= self.MAX_MESSAGES:
            logger.debug(
                "WARNING: message store limit reached, dropping message", msg=msg
            )
            return
        self._msgs[msg.path].append(msg)
        self._msg_count += 1

    def should_report_error(self, error, original_func):
        key = " ".join(
            [
                type(error).__name__,
                original_func.__name__,
                original_func.__module__,
                str(error),
            ]
        )

        if key in self.REPORTED_ERRORS:
            self.REPORTED_ERRORS[key] += 1
            return False

        self.REPORTED_ERRORS[key] = 1

        return True

    def report_error(self, error, original_func, logger_="", message="", skip_frames=0):
        """
        Report an agent error/exception to Telemetry.

        Take great care to avoid calling this where application errors or customer
        code may be caught.
        """
        if self.should_report_error(error, original_func):
            self.add_message(
                ErrorTelemetryEvent(
                    self.instance_id,
                    error=error,
                    logger_=logger_,
                    message=message,
                    # +1 to remove the current report_error frame
                    skip_frames=skip_frames + 1,
                )
            )

    def _post(self, messages, path):
        """
        Send a list of `messages` to telemetry `path`
        """
        logger.debug("Sending %s Telemetry messages to %s.", len(messages), path)

        response = post_request(
            f"{URL}{path}",
            json=[msg.to_json() for msg in messages],
            headers=HEADERS,
            allow_redirects=False,
            verify=True,
        )

        logger.debug("Telemetry response: %s %s", response.status_code, response.reason)
        return response

    def _retry_after(self, response) -> int | None:
        """
        Per RFC-6585, check response status code for 429 and returns the value
        of the Retry-After present or self.RETRY_WAIT.
        """
        if response.status_code == 429:
            wait_time = int(response.headers.get("Retry-After", self.RETRY_WAIT))
            logger.debug("Telemetry waiting for %s seconds", wait_time)
            return wait_time
        return None

    def _is_multicast_mac_address(self, mac_addr):
        """
        A multicast MAC address is an indication that we're not seeing a hardware MAC
        address, which means this value is subject to change even on a single server.
        MAC addresses have a multicast bit that is only set for such addresses. This
        method returns True if the supplied mac address is a multicast address.

        Note that when uuid.getnode() isn't able to find a hardware MAC address, it
        randomly generates an address and (critically) sets the multicast bit.
        """
        return bool(mac_addr & (1 << 40))

    def _sha256(self, str_input):
        return hashlib.sha256(str_input.encode()).hexdigest()

    def _check_enabled(self):
        self._check_is_public_build()

        if contrast.telemetry_disabled() or self._connection_failed():
            self.enabled = False
        else:
            self._find_or_create_file()

        # Debug log for dev purposes. The only time an agent user should see anything
        # about telemetry is if the disclaimer is print/logged.
        logger.debug("Agent telemetry is %s", "enabled" if self.enabled else "disabled")

    def _check_is_public_build(self) -> None:
        is_public = os.environ.get("CONTRAST_PUBLIC_BUILD")
        self.is_public_build = True

        if is_public and is_public.lower() in ("0", "false"):
            self.is_public_build = False

        # Debug log for dev purposes. The only time an agent user should see anything
        # about telemetry is if the disclaimer is print/logged.
        logger.debug(
            "Agent telemetry %s",
            (
                "is in public build mode"
                if self.is_public_build
                else "is not in public build mode"
            ),
        )

    def _connection_failed(self):
        try:
            # any response here is fine as long as no error is raised.
            get_request(BASE_URL)
            return False
        except Exception as ex:
            # Any exception such as SSLError, ConnectionError, etc
            logger.debug("Telemetry connection failed: %s", ex)

        return True

    def _find_or_create_file(self):
        """
        Find an existing .telemetry file or create an empty one.

        /etc/contrast/python/ is the preferred location because it's permanent
        across any agent, but in some OS we may not be able to create it.

        The .telemetry file is intended to be an empty file only as a marker
        to let us know if we have print/logged the disclaimer. Failing to find it
        in any situation means we should print/log.
        """
        name = ".telemetry"

        # 1. If .telemetry file exists, don't print/log disclaimer
        for path in FILE_LOCATIONS:
            file_path = os.path.join(path, name)
            if Path(file_path).exists():
                return

        # 2. If .telemetry file does not exist, attempt to create dir structure
        # and the empty file
        for path in FILE_LOCATIONS:
            file_path = os.path.join(path, name)
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
                Path(file_path).touch()
                break
            except Exception:
                continue

        # 3. Print/log disclaimer if .telemetry file was created or if it failed to
        # be created
        sys.stderr.write(f"{DISCLAIMER}\n")  # pylint: disable=superfluous-parens
        logger.info(DISCLAIMER)
