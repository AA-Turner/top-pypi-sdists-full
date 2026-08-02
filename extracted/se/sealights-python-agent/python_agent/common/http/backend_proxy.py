import json
import logging
import os

from python_agent import __package_name__ as PACKAGE_NAME
from python_agent import __version__ as VERSION
from python_agent.common.build_session.build_session_data import BuildSessionData
from python_agent.common.http import remote_config_merge
from python_agent.common.http.requests_wrapper import Requests
from python_agent.common.http.sl_metadata import SLMetadata
from python_agent.common.http.sl_routes import SLRoutes
import requests
from requests import HTTPError

from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates

log = logging.getLogger(__name__)


class BackendProxy(object):
    def __init__(self, config_data):
        self.requests = Requests(config_data)
        self.config_data = config_data
        self.debug_calls = os.environ.get("SL_DEBUG_CALLS", False)

    def get_build_session(self, config_data, build_session_id):
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)
            sl_metadata.buildSessionId = build_session_id
            response = self.requests.get(
                SLRoutes.build_session_v2(build_session_id),
                sl_metadata=sl_metadata,
            )
            response.raise_for_status()
            build_session_dict = response.json()
            return self._create_build_session_data(build_session_dict)
        except Exception as e:
            log.error("Failed getting Build Session Id. Error: %s" % str(e))
            raise ConnectionError("Failed Getting Build Session Id. Error: %s" % str(e))

    def create_build_session_id(self, config_data, build_session_data):
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)

            sl_metadata.buildSessionId = build_session_data.buildSessionId
            response = self.requests.post(
                SLRoutes.build_session_v2(),
                data=json.dumps(build_session_data, default=lambda m: m.__dict__),
                sl_metadata=sl_metadata,
            )
            response.raise_for_status()
            build_session_id = response.json()
            return build_session_id
        except Exception as e:
            ConsoleMessageTemplates.render_and_print(
                "common.build-scanner.config-build-session-error"
            )
            raise ConnectionError(
                "Failed Creating Build Session Id. Error: %s" % str(e)
            )

    def create_pr_build_session_id(self, config_data, build_session_data):
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)
            sl_metadata.buildSessionId = build_session_data.buildSessionId
            response = self.requests.post(
                SLRoutes.pr_build_session_v2(),
                data=json.dumps(build_session_data, default=lambda m: m.__dict__),
                sl_metadata=sl_metadata,
            )
            response.raise_for_status()
            build_session_id = response.json()
            return build_session_id
        except Exception as e:
            log.error("Failed Creating Build Session Id for PR. Error: %s" % str(e))
            return None

    def submit_build_mapping(self, config_data, build_mapping):
        try:
            response = self.requests.post(
                SLRoutes.build_mapping_v5(),
                data=json.dumps(build_mapping, default=lambda m: m.__dict__),
                sl_metadata=SLMetadata().from_config_data(config_data),
            )
            response.raise_for_status()
            log.info("Scanned build map submitted successfully")
        except HTTPError as e:
            if e.response.status_code == 409:
                log.error(
                    "Scanned build map already exists for the current build session id. No new scann was submitted"
                )
            else:
                raise ConnectionError(
                    "Failed Submitting Build Mapping. Error: %s" % str(e)
                )
        except Exception as e:
            raise ConnectionError("Failed Submitting Build Mapping. Error: %s" % str(e))

    def check_build_session_submitted(self, config_data, build_session_id):
        """
        Check if a build session has already been scanned/submitted.

        Returns True if the build session was already submitted, False otherwise.
        Returns None if the API call fails (graceful fallback).
        """
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)
            sl_metadata.buildSessionId = build_session_id
            response = self.requests.get(
                SLRoutes.build_mapping_submitted(build_session_id),
                sl_metadata=sl_metadata,
            )
            response.raise_for_status()
            result = response.json()
            # API returns {"data": {"submitted": true/false}}
            data = result.get("data", {})
            return data.get("submitted", False)
        except Exception as e:
            log.warning(
                "Failed to check if build session was already submitted. "
                "Proceeding with scan. Error: %s" % str(e)
            )
            return None

    def send_footprints(self, config_data, footprints):
        response = self.requests.post(
            SLRoutes.footprints_v5(),
            data=json.dumps(footprints, default=lambda m: m.__dict__),
            sl_metadata=SLMetadata().from_config_data(config_data),
        )
        response.raise_for_status()

    def send_footprints_v6(
        self,
        config_data,
        footprints,
        execution_build_session_id: str,
        test_stage: str,
        execution_id: str,
    ):
        sl_metadata = SLMetadata().from_config_data(config_data)
        sl_metadata.buildSessionId = execution_build_session_id
        sl_metadata.executionId = execution_id
        response = self.requests.post(
            SLRoutes.footprints_v6(
                execution_build_session_id, test_stage, config_data.buildSessionId
            ),
            data=footprints,
            sl_metadata=sl_metadata,
        )
        response.raise_for_status()

    def send_events(self, config_data, events, execution_id):
        sl_metadata = SLMetadata().from_config_data(config_data)
        sl_metadata.executionId = execution_id
        response = self.requests.post(
            SLRoutes.events_v2(),
            data=json.dumps(events, default=lambda m: m.__dict__),
            sl_metadata=sl_metadata,
        )
        response.raise_for_status()

    def start_execution(self, config_data, start_execution_request):
        sl_metadata = SLMetadata().from_config_data(config_data)
        if hasattr(start_execution_request, "executionId"):
            sl_metadata.executionId = start_execution_request.executionId
        try:
            response = self.requests.post(
                SLRoutes.test_execution_v3(),
                data=json.dumps(start_execution_request, default=lambda m: m.__dict__),
                sl_metadata=sl_metadata,
            )
            if response.content:
                parsed_response = response.json()
            response.raise_for_status()
            ConsoleMessageTemplates.render_and_print(
                "common.test-listener.test-stage-opened-by-agent",
                testStage=config_data.testStage,
                executionId=sl_metadata.executionId or "Anonymous Execution",
            )
            return parsed_response
        except Exception as e:
            log.error("Failed Starting Execution. Error: %s" % str(e))
            raise ConnectionError("Failed Starting Execution. Error: %s" % str(e))

    def end_execution(self, config_data, lab_id, test_group_id, execution_id=None):
        params = {
            "labId": lab_id,
        }
        if execution_id:
            params["executionId"] = execution_id
        if test_group_id:
            params["testGroupId"] = test_group_id
        sl_metadata = SLMetadata().from_config_data(config_data)
        sl_metadata.executionId = execution_id
        sl_metadata.labId = lab_id
        response = self.requests.delete(
            SLRoutes.test_execution_v3(), params=params, sl_metadata=sl_metadata
        )
        response.raise_for_status()
        ConsoleMessageTemplates.render_and_print(
            "common.test-listener.test-stage-closed-by-agent",
            testStage=config_data.testStage,
            executionId=execution_id or "Anonymous Execution",
        )

    def upload_reports(self, upload_reports_request, config_data):
        response = self.requests.post(
            SLRoutes.external_data_v3(),
            files=upload_reports_request.__dict__,
            patch_content_type=False,
            sl_metadata=SLMetadata().from_config_data(config_data),
        )
        response.raise_for_status()

    def has_active_execution(self, customer_id, labid, config_data):
        params = {"customerId": customer_id, "labId": labid, "environment": labid}
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)
            sl_metadata.labId = labid
            response = self.requests.get(
                SLRoutes.test_execution_v3(), params=params, sl_metadata=sl_metadata
            )
            parsed_response = {}
            if response.content:
                parsed_response = response.json()
            status = parsed_response.get("status")
            if status in ["pendingDelete", "created"]:
                return True
            if response.status_code == requests.codes.not_found:
                return False
        except Exception as e:
            log.exception("Error while trying to send request. Error: %s" % str(e))
            return False

    def has_active_execution_v4(self, config_data):
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)
            response = self.requests.get(
                SLRoutes.test_execution_v4(config_data.labId), sl_metadata=sl_metadata
            )
            parsed_response = {}
            if response.content:
                parsed_response = response.json()
            execution = parsed_response.get("execution")
            if not execution:
                return {}
            execution_response = {
                "executionId": execution.get("executionId"),
                "status": execution.get("status"),
                "testStage": execution.get("testStage"),
                "executionBuildSessionId": execution.get("buildSessionId"),
            }
            return execution_response

        except Exception as e:
            log.exception("Error while trying to send request. Error: %s" % str(e))
            return False

    def submit_logs(self, config_data, logs_request):
        response = self.requests.post(
            SLRoutes.logsubmission_v2(),
            data=json.dumps(logs_request, default=lambda m: m.__dict__),
            sl_metadata=SLMetadata().from_config_data(config_data),
        )
        response.raise_for_status()

    def get_recommended_version(self, config_data):
        status_code = None
        try:
            response = self.requests.get(
                SLRoutes.recommended_v2(),
                sl_metadata=SLMetadata().from_config_data(config_data),
            )
            status_code = response.status_code
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if status_code == 404:
                log.info("Not upgrading agent")
            else:
                log.warning("Failed Getting Recommended Version. Error: %s" % str(e))
            return {}

    def check_version_exists_in_pypi(self, version):
        url = "https://pypi.python.org/pypi/%s/%s" % (PACKAGE_NAME, version)
        try:
            response = self.requests.get(url)
            response.raise_for_status()
            return True
        except Exception as e:
            log.warning(
                "Version: %s Doesn't exist. URL: %s. Error: %s" % (version, url, str(e))
            )
            return False

    def get_remote_configuration(self, config_data):
        """
        Fetch remote configuration from the v3 endpoint.

        Contract (matches the .NET RemoteConfigurationApiClient):
          * ``GET /v3/config?<query>`` — 8 optional query params, all
            from ConfigData and the JWT-implied customerId.
          * Success body is a flat ``dict[str, str]``.
          * 404 / connection errors are NON-fatal — the agent returns ``{}``
            and continues with its existing defaults, matching today's
            behavior on a legacy v2 404.

        There is intentionally no v2 fallback and no version feature flag:
        v2 is gone from this code path. The old configuration_v2 method on
        SLRoutes has been removed; a cleanup PR can delete unused imports
        once everything else is verified.
        """
        try:
            url = SLRoutes.configuration_v3(
                agent_id=config_data.agentId,
                agent_type=PACKAGE_NAME,
                agent_version=VERSION,
                app_name=config_data.appName,
                branch_name=config_data.branchName,
                build_name=config_data.buildName,
                lab_id=config_data.labId,
                test_stage=config_data.testStage,
            )
            response = self.requests.get(
                url, sl_metadata=SLMetadata().from_config_data(config_data)
            )
            response.raise_for_status()
            body = response.json()
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                log.debug(
                    "Server returned 404 (Not Found) for v3 remote configuration."
                )
            else:
                log.error("Failed getting v3 remote configuration. Error: %s" % str(e))
            return {}
        except Exception as e:
            log.error("Failed getting v3 remote configuration. Error: %s" % str(e))
            return {}

        # Diagnostic: log raw keys so support bundles immediately surface any
        # mismatch between the Agents microservice and this agent's expected
        # alias names without requiring a code change.
        if isinstance(body, dict):
            try:
                log.debug("v3 remote-config keys received: %s", sorted(body.keys()))
            except Exception:
                # Never let logging break the merge path.
                pass
        else:
            log.warning(
                "v3 remote-config response is not a JSON object (type=%s) — ignoring",
                type(body).__name__,
            )
            return {}

        # Translate aliases + coerce string values to the declared types.
        target_attrs = set(vars(config_data).keys()) | set(dir(config_data))
        return remote_config_merge.build_typed_update(body, target_attrs)

    def try_get_recommendations(self, config_data):
        url = SLRoutes.test_exclusions(
            config_data.buildSessionId, config_data.testStage, config_data.testGroupId
        )
        try:
            response = self.requests.get(
                url, sl_metadata=SLMetadata().from_config_data(config_data)
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            log.warning(
                "failed get recommendation tests from server URL: %s. Error: %s"
                % (url, str(e))
            )
            return {}

    def get_build_session_from_labid(self, labid, config_data):
        url = SLRoutes.lab_ids_active_build_session_v1(labid)
        try:
            sl_metadata = SLMetadata().from_config_data(config_data)
            sl_metadata.labId = labid
            response = self.requests.get(url, sl_metadata=sl_metadata)
            response.raise_for_status()
            build_session_dict = response.json()
            return self._create_build_session_data(build_session_dict)
        except Exception as e:
            log.warning(
                "Failed getting active build session from lab id: %s. Error: %s"
                % (labid, str(e))
            )
            return None

    def _create_build_session_data(self, build_session_dict):
        return BuildSessionData(
            build_session_dict["appName"],
            build_session_dict["buildName"],
            build_session_dict["branchName"],
            build_session_dict["buildSessionId"],
            additional_params=build_session_dict.get("additionalParams"),
        )

    def send_agent_event(self, agent_event, config_data):
        sl_metadata = SLMetadata().from_config_data(config_data)
        if hasattr(agent_event, "message_type"):
            sl_metadata.messageType = agent_event.message_type
        if hasattr(agent_event, "agentType"):
            sl_metadata.agentType = agent_event.agentType
        if hasattr(agent_event, "labId"):
            sl_metadata.labId = agent_event.labId
        if hasattr(agent_event, "buildSessionId"):
            sl_metadata.buildSessionId = agent_event.buildSessionId
        if hasattr(agent_event, "agentId"):
            sl_metadata.agentId = agent_event.agentId

        response = self.requests.post(
            SLRoutes.agent_events_v3(),
            data=json.dumps(agent_event, default=lambda m: m.__dict__),
            sl_metadata=sl_metadata,
        )
        response.raise_for_status()

    def _format_response(self, response):
        """
        Formats the response for logging, handling different response types.
        """
        if response is None:
            return "No Response"

        # Try to get a JSON response
        try:
            json_response = response.json()
            return json.dumps(
                json_response,
                default=lambda m: m.__dict__ if hasattr(m, "__dict__") else str(m),
                indent=4,
            )
        except ValueError:
            pass

        # If response is not JSON, try to decode bytes to string
        try:
            return response.content.decode()
        except AttributeError:
            pass

        # If it's neither JSON nor bytes, use json.dumps to serialize
        try:
            return json.dumps(
                response,
                default=lambda m: m.__dict__ if hasattr(m, "__dict__") else str(m),
                indent=4,
            )
        except TypeError:
            pass

        # Fallback for other types not handled above
        return str(response)
