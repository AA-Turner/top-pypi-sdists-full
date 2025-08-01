# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


import base64
import contextlib
from dataclasses import dataclass
from http.cookiejar import CookieJar, DefaultCookiePolicy
import queue
import threading
from collections.abc import Generator
import uuid

from contrast.agent.request import Request
from contrast.configuration.agent_config import AgentConfig
from contrast.configuration.config_option import DEFAULT_VALUE_SRC
from contrast.utils import timer
import contrast_fireball
import contrast

from contrast.agent import scope
from contrast.agent.disable_reaction import DisableReaction
from contrast.agent.settings import Settings
from contrast.reporting.request_audit import RequestAudit
from contrast.reporting.teamserver_messages.base_ts_message import (
    PYTHON,
    b64url_stripped,
)
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast_vendor import structlog as logging

from .teamserver_messages import BaseTsMessage
from contrast.reporting import teamserver_messages

logger = logging.getLogger("contrast")

REPORTING_CLIENT_THREAD_NAME = "ContrastReportingClient"

MAX_ATTEMPTS = 2
ERROR_STATUS_CODE = -1


class ReportingClient(threading.Thread):
    def __init__(self, instance_id: str | None = None):
        super().__init__(name=REPORTING_CLIENT_THREAD_NAME, daemon=True)
        from contrast.agent import agent_state

        self.instance_id = instance_id or uuid.uuid4().hex
        self._stopper = object()  # sentinel sent over message_q to stop the thread
        self.message_q = queue.Queue(maxsize=128)
        self.settings = Settings()

        self.init_certs(self.settings)
        self.proxies = (
            self.settings.build_proxy_url() if self.settings.is_proxy_enabled else {}
        )
        # disable persisting cookies, per Architecture team recommendation.
        self.cookies = CookieJar(policy=DefaultCookiePolicy(allowed_domains=[]))
        server_name_b64 = b64url_stripped(agent_state.get_server_name())
        server_path_b64 = b64url_stripped(self.settings.get_server_path())
        server_type_b64 = b64url_stripped(self.settings.server_type)
        auth_header = f"{self.settings.api_user_name}:{self.settings.api_service_key}"
        self.always_headers = {
            # the Authorization header must not have its padding stripped
            "Authorization": base64.urlsafe_b64encode(auth_header.encode()).decode(),
            "API-Key": self.settings.api_key,
            "Server-Name": server_name_b64,
            "Server-Path": server_path_b64,
            "Server-Type": server_type_b64,
            "X-Contrast-Agent": f"{PYTHON} {contrast.__version__}",
            "X-Contrast-Header-Encoding": "base64",
            "X-Contrast-Reporting-Instance": self.instance_id,
            "Application-Language": PYTHON,
            "Application-Name": b64url_stripped(agent_state.get_app_name()),
            "Application-Path": b64url_stripped(self.settings.app_path),
        }

        self.request_audit = (
            RequestAudit(self.settings.config)
            if self.settings.config.is_request_audit_enabled
            else None
        )
        if self.request_audit:
            self.request_audit.prepare_dirs()

    @fail_quietly(return_value=False)
    def initialize_application(self, config: AgentConfig, server_type="") -> bool:
        """
        Initialize the application with the given configuration.

        Returns True if the application was successfully initialized.
        """
        attempt = 1
        while True:
            if _success := self._agent_startup():
                return True

            attempt += 1
            if attempt > MAX_ATTEMPTS:
                break

            logger.debug(
                "App initialization did not connect -  will retry sleeping for 1 second"
            )
            timer.sleep(1)

        return False

    def _agent_startup(self) -> bool:
        msg = teamserver_messages.AgentStartup()
        if (response := self.send_message(msg)) is not None:
            msg.process_response(response, self)
            if response.status_code < 500:
                return True
            elif response.status_code == 500:
                raise RuntimeError("Unexpected 500 response code from AgentStartup")
        return False

    def new_discovered_routes(self, routes: set[contrast_fireball.DiscoveredRoute]):
        self.add_message(teamserver_messages.ApplicationInventory(routes))

    def new_observed_route(self, route: contrast_fireball.ObservedRoute):
        self.add_message(teamserver_messages.ObservedRoute(route))

    def new_findings(
        self, findings: list[contrast_fireball.AssessFinding], request: Request | None
    ):
        self.add_message(teamserver_messages.Preflight(findings, request))

    def new_inventory_components(
        self, components: list[contrast_fireball.InventoryComponent]
    ):
        self.add_message(
            teamserver_messages.ApplicationActivity(inventory_components=components)
        )

    def new_libraries(self, libraries: list[contrast_fireball.Library]):
        self.add_message(teamserver_messages.ApplicationUpdate(libraries))

    def new_library_observations(
        self, observations: list[contrast_fireball.LibraryObservation]
    ):
        self.add_message(teamserver_messages.LibraryUsage(observations))

    @contextlib.contextmanager
    def observability_trace(
        self,
        *,
        send_trace: bool,
        attributes: contrast_fireball.OtelAttributes | None = None,
    ) -> Generator:
        logger.error(
            "Observe mode requires `api.reporting_client = fireball`, but direct"
            " reporting is in use. Disabling observe mode."
        )
        from contrast.agent import agent_state

        agent_state.set_observe_enabled({"observe.enable": False})
        yield None

    def init_certs(self, settings: Settings) -> None:
        self.verify = True
        self.cert = None

        certificate_enable_config_option = settings.config.get_option(
            "api.certificate.enable"
        )
        assert certificate_enable_config_option is not None
        if not certificate_enable_config_option.value():
            return

        # custom certificate settings
        if settings.ca_file:
            self.verify = settings.ca_file
        if settings.client_cert_file and settings.client_private_key:
            self.cert = (
                settings.client_cert_file,
                settings.client_private_key,
            )
        if settings.ignore_cert_errors:
            self.verify = False
            logger.warning("Certificate verification is disabled.")

        # misconfig checks
        if (settings.client_cert_file and not settings.client_private_key) or (
            not settings.client_cert_file and settings.client_private_key
        ):
            logger.error(
                "Unable to communicate with Contrast. "
                "Certificate configuration is not set properly. "
                "Certificate PEM file or private key PEM file is missing.",
                cert_file=settings.client_cert_file,
                key_file=settings.client_private_key,
            )
            DisableReaction.run(settings.config)
            return

        if certificate_enable_config_option.source() != DEFAULT_VALUE_SRC and not any(
            (settings.ca_file, settings.client_cert_file, settings.client_private_key)
        ):
            logger.warning(
                "Certificate configuration is explicitly enabled, but no certificate files are set."
            )

    def stop(self):
        self.message_q.put(self._stopper)
        self.join()

    def run(self):
        with scope.contrast_scope():
            logger.debug("Starting reporting thread")

            while self.settings.is_agent_config_enabled():
                try:
                    msg = self.message_q.get(block=True, timeout=5)
                    if msg is self._stopper:
                        break
                    response = self.send_message(msg)
                    msg.process_response(response, self)
                except queue.Empty:
                    pass
                except Exception as e:
                    logger.debug(
                        "WARNING: reporting client failed to send message", exc_info=e
                    )

    @fail_loudly("Failed to send message to Contrast")
    def send_message(self, msg: BaseTsMessage):
        """
        _send_message sends msg to Teamserver and returns the response.

        It is the caller's responsibility to handle any network exceptions.

        See send_message for the public interface, which handles exceptions.
        """
        status_code = ERROR_STATUS_CODE
        msg_name = msg.class_name

        url = msg.base_url + msg.path
        logger.debug("Sending %s message to Teamserver: %s", msg_name, url)
        response = msg.request_method(
            url,
            json=msg.body,
            headers={**self.always_headers, **msg.extra_headers},
            cookies=self.cookies,
            allow_redirects=False,
            proxies=self.proxies,
            verify=self.verify,
            cert=self.cert,
        )

        try:
            status_code = response.status_code
            msg_success_status = response.json().get("success")
            messages = response.json().get("messages")
            if not (msg_success_status or status_code == 200):
                logger.error(
                    "Failure on Contrast UI processing request reason - (%s): %s",
                    messages,
                    status_code,
                )
        except Exception as e:
            if status_code == ERROR_STATUS_CODE:
                logger.debug(
                    "Failed to receive response from Contrast UI: %s ",
                    e,
                )

        logger.debug("Contrast UI response (%s): %s", msg_name, status_code)

        if self.request_audit:
            self.request_audit.audit(msg, response)

        msg.sent()
        return response

    def add_message(self, msg):
        if msg is None or not isinstance(msg, BaseTsMessage):
            return

        logger.debug("Adding msg to reporting queue: %s", msg.class_name)

        self.message_q.put(msg)

    def retry_message(self, msg):
        # Never send a message more than twice (original time plus one retry)
        # To prevent queue from filling up or causing memory issues.
        if msg.sent_count < MAX_ATTEMPTS:
            logger.debug("Re-enqueuing %s message", msg.class_name)
            self.add_message(msg)


@dataclass
class StackFrame:
    """
    StackFrame represents a single stack frame used used during direct
    reporting.

    We might be able to use AssessStackFrame in the future. We're using
    this for now because it's quicker to implement.
    """

    line_number: int | None
    file_name: str
    method_name: str
    declaring_class: str | None = None
    signature: str | None = None
    type: str | None = None
    eval: str | None = None
