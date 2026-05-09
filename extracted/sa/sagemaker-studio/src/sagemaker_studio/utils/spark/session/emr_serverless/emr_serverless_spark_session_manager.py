"""
EMR Serverless Spark Session Management.

This module provides the EMRServerlessSparkSessionManager class that creates and returns
a configured SparkSession object connected to EMR Serverless.
"""

import logging
import os
import time
import traceback
import uuid

import boto3
from pyspark.sql.connect.session import SparkSession as _SparkSession

from sagemaker_studio.project import ClientConfig, Project
from sagemaker_studio.utils._internal import InternalUtils
from sagemaker_studio.utils.loggerutils import sync_with_metrics
from sagemaker_studio.utils.spark.internal_spark_utils import generate_spark_configs
from sagemaker_studio.utils.spark.session.constants import SPARK_CONNECT_LOG_FILE
from sagemaker_studio.utils.spark.session.emr_serverless.interceptors import CustomChannelBuilder
from sagemaker_studio.utils.spark.session.spark_session_manager import SparkSessionManager

_parent_logger = logging.getLogger("SparkConnect")
SparkSessionManager.setup_logger(_parent_logger, SPARK_CONNECT_LOG_FILE)
logger = logging.getLogger("SparkConnect.EMRServerless")


class EMRServerlessSparkSessionManager(SparkSessionManager):
    """
    Creates and returns a SparkSession object connected to EMR Serverless.

    This class handles the creation of an EMR Serverless session and returns a configured
    SparkSession that can be used directly for Spark operations.
    """

    def __init__(
        self, connection_name=None, config: ClientConfig = ClientConfig(), *, connection=None
    ):
        """
        Initialize the EMR Serverless Spark session.

        Args:
            connection_name (str): The connection name (backward compat, used if connection not provided).
            config (ClientConfig): Configuration for the client.
            connection: Pre-resolved Connection object (from sparkutils routing). Keyword-only.
        """
        self._connection = connection
        self.connection_name = connection_name
        self.config = config
        self.application_id = None
        self.emr_serverless_session_id = None
        self.emr_serverless_runtime_role = None
        self._spark_session = None
        self.emr_serverless_client = None
        self.sts_client = None

    def _lazy_init(self):
        _utils = InternalUtils()
        region = _utils._get_domain_region()

        emr_override_config = self.config.overrides.get("emr-serverless", {})
        emr_endpoint_url = emr_override_config.get("endpoint_url")

        # Load custom EMR-S service model if available (includes start_session,
        # get_session_endpoint, etc. — APIs not yet in the public botocore model).
        import botocore.loaders
        import botocore.session

        model_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "boto3_models")
        )
        if os.path.isdir(model_path):
            loader = botocore.loaders.Loader(extra_search_paths=[model_path])
            botocore_session = botocore.session.get_session()
            botocore_session.register_component("data_loader", loader)
            internal_model_session = boto3.Session(botocore_session=botocore_session)
        else:
            logger.warning(
                f"Custom boto3 model path not found: {model_path}; using default session"
            )
            internal_model_session = boto3.Session()

        emr_kwargs = {"region_name": region}
        if emr_endpoint_url:
            emr_kwargs["endpoint_url"] = emr_endpoint_url

        self.emr_serverless_client = internal_model_session.client("emr-serverless", **emr_kwargs)
        self.sts_client = boto3.client("sts", region_name=region)
        self.project = Project()

        # Use pre-resolved connection if available, otherwise look up by name
        connection = self._connection
        if connection is None:
            if self.connection_name:
                connection = self.project.connection(self.connection_name)
            else:
                raise ValueError(
                    "EMRServerlessSparkSessionManager requires a connection or connection_name. "
                    "Use sparkutils.init() which resolves the connection automatically."
                )

        # Extract application ID and runtime role from connection props.
        # Consistent with SageMakerStudioDataEngineeringSessions (Livy flow) which reads
        # runtimeRole from sparkEmrProperties for the EMR-S session execution role.
        emr_props = (
            getattr(connection, "_Connection__connection_data", {})
            .get("props", {})
            .get("sparkEmrProperties", {})
        )

        # Extract application ID from computeArn
        # ARN format: arn:aws:emr-serverless:region:account:/applications/{applicationId}
        compute_arn = getattr(connection.data, "compute_arn", None)
        if not compute_arn:
            raise ValueError("Could not resolve compute_arn from the connection.")
        self.application_id = compute_arn.split("/")[-1]
        self.emr_serverless_runtime_role = emr_props.get("runtimeRole", "")
        if not self.emr_serverless_runtime_role:
            logger.warning(
                "runtimeRole not found in sparkEmrProperties, falling back to project IAM role"
            )

        # Extract connection-level spark configs (SparkConfiguration from DataZone connection).
        # Consistent with SageMakerStudioDataEngineeringSessions which reads these via
        # connection_transformer and merges them via _update_spark_configuration_to_connection_default.
        self.connection_spark_configs = {}
        try:
            configurations = getattr(connection, "_Connection__connection_data", {}).get(
                "configurations", []
            )
            if isinstance(configurations, list):
                for config in configurations:
                    if config.get("classification") == "SparkConfiguration":
                        self.connection_spark_configs = config.get("properties", {})
                        break
            if self.connection_spark_configs:
                logger.info(
                    f"Loaded {len(self.connection_spark_configs)} connection-level spark configs"
                )
        except Exception as e:
            logger.warning(f"Error reading connection spark configs: {e}")

        logger.info(
            f"EMR Serverless application_id={self.application_id} from compute_arn={compute_arn}"
        )
        self.resolved_connection_name = getattr(connection, "name", None) or self.connection_name
        logger.debug("Successfully created EMR Serverless client")

    def create(self):
        """
        Create and return a SparkSession connected to EMR Serverless.

        Returns:
            SparkSession: A configured SparkSession object.
        """
        if self._spark_session is not None:
            logger.debug("SparkSession already exists, returning existing session")
            return self._spark_session

        try:
            logger.debug("Creating SparkSession connected to EMR Serverless...")
            # Required for PySpark to use Spark Connect (remote) mode instead of local mode
            os.environ["SPARK_CONNECT_MODE_ENABLED"] = "1"
            self._lazy_init()

            # Get EMR Serverless session and Spark Connect URL
            self.emr_serverless_session_id, spark_endpoint_url, endpoint_response = (
                self._start_emr_serverless_session(self.application_id)
            )

            # Create custom channel builder with gRPC interceptor for auto-refreshing
            # EMR Serverless auth tokens. Seed with initial token to avoid redundant API call.
            custom_channel_builder = CustomChannelBuilder(
                self.emr_serverless_session_id,
                self.application_id,
                spark_endpoint_url,
                self.emr_serverless_client,
                initial_auth_token=endpoint_response.get("authToken"),
                initial_token_expiry=endpoint_response.get("authTokenExpiresAt"),
            )

            # Create SparkSession
            self._spark_session = (
                _SparkSession.builder.channelBuilder(custom_channel_builder)
                .appName("EMRServerlessSparkSession")
                .getOrCreate()
            )

            logger.debug("SparkSession created successfully")
            return self._spark_session

        except Exception as e:
            logger.error(f"Failed to create SparkSession: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Clean up any orphaned EMR Serverless session
            self.stop()
            raise

    def stop(self):
        """Stop the SparkSession and terminate the EMR Serverless session."""
        logger.debug(f"Stopping EMR Serverless spark session {self.emr_serverless_session_id}...")

        # Stop Spark session first (graceful gRPC close)
        if self._spark_session:
            try:
                self._spark_session.stop()
            except Exception as e:
                logger.error(f"Error while stopping Spark session: {e}")
            finally:
                self._spark_session = None

        # Then terminate the server-side session
        if self.emr_serverless_session_id:
            try:
                self._terminate_emr_serverless_session(self.emr_serverless_session_id)
            except Exception as e:
                logger.error(
                    f"Error while terminating EMR Serverless spark session {self.emr_serverless_session_id}: {e}"
                )
            finally:
                self.emr_serverless_session_id = None

        logger.debug("Stopped EMR Serverless spark session")

    def get_session_id(self):
        return self.emr_serverless_session_id

    def _get_execution_role_arn(self):
        """Get the execution role ARN for the EMR Serverless session.

        Uses runtimeRole from the connection's sparkEmrProperties (consistent with the
        Livy flow in SageMakerStudioDataEngineeringSessions). Falls back to the project
        IAM role if runtimeRole is not available.
        """
        if self.emr_serverless_runtime_role:
            return self.emr_serverless_runtime_role
        return self.project.iam_role

    def _get_s3_access_grants_configs(self) -> dict:
        """Get S3 Access Grants spark configs if enabled for the project's tooling environment.

        Consistent with SageMakerStudioDataEngineeringSessions which checks
        enableS3AccessGrantsForTools in the tooling environment's provisionedResources.
        """
        try:
            _utils = InternalUtils()
            domain_id = _utils._get_domain_id()
            default_env = (
                self.project._sagemaker_studio_api.project_api.get_project_default_environment(
                    domain_id, self.project.id
                )
            )
            provisioned_resources = default_env.get("provisionedResources", [])
            s3ag_enabled = any(
                r.get("name") == "enableS3AccessGrantsForTools"
                and r.get("value", "").lower() == "true"
                for r in provisioned_resources
            )
            if s3ag_enabled:
                logger.info("S3 Access Grants enabled for Spark configuration")
                return {
                    "spark.hadoop.fs.s3.s3AccessGrants.enabled": "true",
                    "spark.hadoop.fs.s3.s3AccessGrants.fallbackToIAM": "true",
                }
        except Exception as e:
            logger.warning(f"Failed to check S3 Access Grants status: {e}")
        return {}

    @staticmethod
    def _is_release_at_least(release_label: str, min_release: str) -> bool:
        """Compare EMR release labels. Returns True if release_label >= min_release."""
        try:
            current = [int(x) for x in release_label.split("-", 1)[1].split(".")]
            minimum = [int(x) for x in min_release.split("-", 1)[1].split(".")]
            return current >= minimum
        except (IndexError, ValueError):
            return False

    @staticmethod
    def _user_msg(msg):
        """Print a user-facing progress message (visible in notebook cell output)."""
        print(msg, flush=True)

    def _ensure_application_started(self, application_id, timeout=120, poll_interval=2):
        """Ensure the EMR Serverless application is in STARTED state before creating a session.

        Consistent with SageMakerStudioDataEngineeringSessions (pre_session_creation) which
        checks app state, starts if CREATED/STOPPED, and waits for STARTED.

        Returns the application details dict from get_application (reused for FTA check).
        """
        ready_to_start = ("CREATED", "STOPPED")
        transient = ("STARTING", "STOPPING", "CREATING")
        started = ("STARTED",)

        app_response = self.emr_serverless_client.get_application(applicationId=application_id)
        application = app_response["application"]
        state = application["state"]
        logger.info(f"EMR Serverless application {application_id} state: {state}")

        if state in started:
            self._user_msg(f"EMR Serverless ({application_id}) is started")
            return application

        if state in transient:
            state = self._wait_for_application_state(
                application_id, transient, timeout, poll_interval
            )

        if state in ready_to_start:
            logger.info(f"Starting EMR Serverless application {application_id}")
            self._user_msg(f"Starting EMR Serverless ({application_id})")
            self.emr_serverless_client.start_application(applicationId=application_id)
            state = self._wait_for_application_state(
                application_id, ("STARTING",), timeout, poll_interval
            )

        if state in started:
            logger.info(f"EMR Serverless application {application_id} is started")
            self._user_msg(f"EMR Serverless ({application_id}) is started")
            # Re-fetch to return the up-to-date application dict (used for FTA check).
            return self.emr_serverless_client.get_application(applicationId=application_id)[
                "application"
            ]

        raise RuntimeError(
            f"EMR Serverless application {application_id} in unexpected state: {state}"
        )

    def _wait_for_application_state(
        self, application_id, waiting_states, timeout=120, poll_interval=2
    ):
        """Wait until application exits the given waiting states."""
        start_time = time.time()
        while time.time() - start_time <= timeout:
            state = self.emr_serverless_client.get_application(applicationId=application_id)[
                "application"
            ]["state"]
            if state not in waiting_states:
                return state
            time.sleep(poll_interval)
        raise RuntimeError(
            f"Timed out waiting for application {application_id} to exit {waiting_states} state"
        )

    @staticmethod
    def _is_compatibility_mode_enabled(application) -> bool:
        """Check if the EMR-S application has compatibility mode enabled (LF not natively enabled).

        Consistent with SageMakerStudioDataEngineeringSessions._is_compatibility_mode_enabled.
        Returns True when spark.emr-serverless.lakeformation.enabled is 'false' or absent
        in the application's runtimeConfiguration spark-defaults.
        """
        runtime_config = application.get("runtimeConfiguration", None)
        if runtime_config is None:
            return False
        for config in runtime_config:
            if config.get("classification") == "spark-defaults":
                properties = config.get("properties", None)
                if properties is not None:
                    return (
                        properties.get(
                            "spark.emr-serverless.lakeformation.enabled", "false"
                        ).lower()
                        == "false"
                    )
                return False
        return False

    @staticmethod
    def _is_fta_supported(application) -> bool:
        """Check if FTA (Full Table Access via LakeFormation) is supported for this application.

        Consistent with SageMakerStudioDataEngineeringSessions._is_fta_supported.
        FTA requires compatibility mode (lakeformation.enabled=false on the app)
        AND EMR release label >= emr-7.8.0.
        """
        if not EMRServerlessSparkSessionManager._is_compatibility_mode_enabled(application):
            return False
        release_label = application.get("releaseLabel", "")
        if not release_label:
            return False
        return EMRServerlessSparkSessionManager._is_release_at_least(release_label, "emr-7.8.0")

    @staticmethod
    def _get_compatibility_mode_configs() -> dict:
        """Compatibility mode spark configs applied when FTA is supported.

        Consistent with SageMakerStudioDataEngineeringSessions apply_compatibility_mode_configs.
        """
        return {
            "spark.hadoop.fs.s3.credentialsResolverClass": "com.amazonaws.glue.accesscontrol.AWSLakeFormationCredentialResolver",
            "spark.hadoop.fs.s3.useDirectoryHeaderAsFolderObject": "true",
            "spark.hadoop.fs.s3.folderObject.autoAction.disabled": "true",
            "spark.sql.catalog.createDirectoryAfterTable.enabled": "true",
            "spark.sql.catalog.dropDirectoryBeforeTable.enabled": "true",
            "spark.sql.catalog.spark_catalog.glue.lakeformation-enabled": "true",
            "spark.sql.catalog.skipLocationValidationOnCreateTable.enabled": "true",
        }

    @sync_with_metrics("_start_emr_serverless_session")
    def _start_emr_serverless_session(self, application_id):
        """Start EMR Serverless session and get Spark Connect URL."""
        try:
            logger.debug(f"Starting EMR Serverless session for application: {application_id}")

            # Ensure application is started; reuse response for FTA check (no extra API call)
            application = self._ensure_application_started(application_id)

            user_id, account_id = self._get_user_id_account_id()
            spark_configs = generate_spark_configs(account_id)

            # Conditionally apply compatibility mode (FTA) configs — consistent with sessions package.
            # generate_spark_configs includes these unconditionally (shared with Athena), but for EMR-S
            # we follow the sessions package pattern: only apply when FTA is supported.
            if self._is_fta_supported(application):
                logger.info("FTA supported — applying compatibility mode configs")
                spark_configs.update(self._get_compatibility_mode_configs())
            else:
                # Remove compat configs that generate_spark_configs set unconditionally
                for key in self._get_compatibility_mode_configs():
                    spark_configs.pop(key, None)
                logger.info("FTA not supported — compatibility mode configs removed")
            # Merge connection-level spark configs on top of defaults (connection overrides defaults)
            if self.connection_spark_configs:
                spark_configs.update(self.connection_spark_configs)
            # S3 Access Grants — consistent with sessions package (emr_on_serverless_session.py).
            # No version check needed: Spark Connect sessions require EMR versions that already support S3AG.
            spark_configs.update(self._get_s3_access_grants_configs())

            client_token = str(uuid.uuid4())

            self._user_msg(f"Create session for connection: {self.resolved_connection_name}")
            start_session_response = self.emr_serverless_client.start_session(
                applicationId=application_id,
                executionRoleArn=self._get_execution_role_arn(),
                configurationOverrides={
                    "runtimeConfiguration": [
                        {"classification": "spark-defaults", "properties": spark_configs}
                    ]
                },
                idleTimeoutMinutes=15,
                clientToken=client_token,
                tags={
                    "AmazonDataZoneSessionOwner": user_id,
                    "AmazonDataZoneProject": self.project.id,
                },
            )
            session_id = start_session_response["sessionId"]
            self.emr_serverless_session_id = (
                session_id  # assign early so stop() can clean up on failure
            )
            logger.debug(f"EMR Serverless session started: {session_id}")

            self._wait_for_emr_serverless_session(application_id, session_id)

            logger.debug("Getting session endpoint URL and auth token...")
            get_session_endpoint_response = self.emr_serverless_client.get_session_endpoint(
                applicationId=application_id, sessionId=session_id
            )

            spark_connect_url = self._construct_spark_endpoint_url(get_session_endpoint_response)
            logger.debug("Successfully constructed Spark connect URL")
            self._user_msg(f"Session created for connection: {self.resolved_connection_name}.")
            self._user_msg(f"Compute details - Application Id: {application_id}")

            return session_id, spark_connect_url, get_session_endpoint_response

        except Exception as e:
            logger.error(f"Failed to create EMR Serverless Spark session: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def _construct_spark_endpoint_url(self, get_session_endpoint_response) -> str:
        endpoint_url = get_session_endpoint_response["endpoint"]
        auth_token = get_session_endpoint_response["authToken"]
        if endpoint_url.startswith("https://"):
            endpoint_url = endpoint_url.replace("https://", "sc://", 1)

        return f"{endpoint_url}:443/;use_ssl=true;x-aws-proxy-port=15002;x-aws-force-h2=true;x-aws-proxy-auth={auth_token}"

    def _wait_for_emr_serverless_session(
        self, application_id, session_id, timeout=120, poll_interval=2
    ):
        """Wait until EMR Serverless session is ready or timeout expires.

        EMR-S session states: SUBMITTED -> QUEUED -> STARTING -> STARTED/IDLE/BUSY.
        Terminal states: FAILED, TERMINATING, TERMINATED.
        """
        logger.debug(f"Waiting for EMR Serverless session {session_id} to be ready...")
        start_time = time.time()
        last_state = None

        while True:
            try:
                response = self.emr_serverless_client.get_session(
                    applicationId=application_id, sessionId=session_id
                )
                state = response["session"]["state"]
                time_delta = time.time() - start_time

                if state != last_state:
                    logger.debug(f"Session {session_id} state: {state}, elapsed: {time_delta:.1f}s")
                    last_state = state

                if state in ("STARTED", "IDLE", "BUSY"):
                    logger.debug(f"Session {session_id} is ready.")
                    return True
                elif state in ("FAILED", "TERMINATED", "TERMINATING"):
                    reason = response["session"].get("stateDetails", "Unknown")
                    error_msg = f"Session {session_id} failed with state {state}. Reason: {reason}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
                elif time_delta > timeout:
                    error_msg = (
                        f"Session {session_id} was not ready within the session start timeout."
                    )
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)

                time.sleep(poll_interval)
            except RuntimeError:
                raise
            except Exception as e:
                logger.error(f"Error checking session {session_id} status: {e}")
                raise

    def _terminate_emr_serverless_session(self, session_id):
        """Terminate an EMR Serverless session."""
        try:
            response = self.emr_serverless_client.terminate_session(
                applicationId=self.application_id, sessionId=session_id
            )
            logger.debug(f"Terminated session {session_id}")
            return response
        except Exception as e:
            logger.error(f"Error terminating session: {e}")
            raise
