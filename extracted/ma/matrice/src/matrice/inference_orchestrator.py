"""
Customer Onboarding Automation - Inference Orchestrator

Focus: Service Orchestration (Inference Only).
Assumes Project, Location, and cluster name are already provisioned by Backend CLI.

WORKFLOW:
1. Parse Config (JSON/CSV) & Load Credentials
2. Authenticate Session
3. Camera Synchronization (Idempotent Registration to existing Location)
4. Inference Pipeline Orchestration (Create/Update -> Start)
5. Health Monitoring (300s total timeout with 30s polling interval)
"""

import csv
import json
import logging
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, Final, List, Optional, Tuple, TypedDict

from dotenv import load_dotenv

# --- DEPENDENCY LOADING ---
try:
    from matrice_common.session import Session

    from matrice.camera_management import CameraManagement
    from matrice.inference_pipeline_management import InferencePipelineManagement
    from matrice.streaming_automation import StreamingAutomation
except ImportError:
    # Fallback for local development structure - go up to project root
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from matrice_common.session import Session

    from matrice.camera_management import CameraManagement
    from matrice.inference_pipeline_management import InferencePipelineManagement
    from matrice.streaming_automation import StreamingAutomation


class DeploymentResults(TypedDict):
    """Type definition for deployment results structure."""

    camera_ids: List[str]
    pipeline_id: Optional[str]
    errors: List[str]
    success: bool


# Type aliases for better readability
CameraConfig = Dict[str, Any]
PipelineConfig = Dict[str, Any]

# Valid protocol types for camera streams (API requires explicit type for path routing)
VALID_PROTOCOL_TYPES: Final[Tuple[str, ...]] = ("RTSP", "IP", "FILE")


class CustomerOnboardingAutomation:
    """
    Automated inference orchestrator for Matrice AI platform.

    This class provides simplified deployment automation that focuses exclusively
    on inference service orchestration. It assumes that infrastructure components
    (Project, Location, Cluster name) have already been provisioned by the
    Backend CLI setup process.

    Key Features:
    - Idempotent camera registration (checks existing cameras before creating)
    - Automated pipeline deployment with camera-to-application mappings
    - Real-time health monitoring with configurable timeouts
    - Support for both JSON and CSV configuration formats
    - Comprehensive error handling and status reporting

    Workflow:
    1. Parse configuration file and validate required parameters
    2. Authenticate with Matrice AI platform using provided credentials
    3. Synchronize cameras to existing location (idempotent)
    4. Create inference pipeline with camera-application assignments
    5. Start pipeline and monitor health until running state achieved

    Attributes
    ----------
    streaming_automation : StreamingAutomation
        Primary API client for pipeline operations
    camera_management : CameraManagement
        Direct API client for camera operations (authoritative)
    pipeline_management : InferencePipelineManagement
        Direct API client for advanced pipeline-specific operations (monitoring)
    session : Session
        Authenticated session object shared across API clients
    project_id : str
        Target project ID from configuration
    lan_id : str
        Target LAN ID from configuration
    cluster_name : str
        Compute cluster name from configuration
    results : Dict
        Deployment results and status tracking
    """

    def __init__(
        self, account_number: str, access_key: str, secret_key: str, project_id: str, lan_id: str, cluster_name: str
    ):
        """
        Initialize the automation system with deployment context.

        Parameters
        ----------
        account_number : str
            Matrice account number
        access_key : str
            API access key
        secret_key : str
            API secret key
        project_id : str
            Target project ID (already provisioned)
        lan_id : str
            location_id is deprecated, use lan_id instead.
            Target LAN ID (already provisioned)
        cluster_name : str
            Compute cluster alias (already provisioned)
        """
        # Deployment context (provided at initialization)
        self.account_number = account_number
        self.access_key = access_key
        self.secret_key = secret_key
        self.project_id = project_id
        self.lan_id = lan_id
        self.cluster_name = cluster_name

        # API client instances (initialized during session setup)
        self.streaming_automation: Optional[StreamingAutomation] = None
        self.camera_management: Optional[CameraManagement] = None
        self.pipeline_management: Optional[InferencePipelineManagement] = None
        self.session: Optional[Session] = None

        # Results tracking for deployment status and error reporting
        self.results: DeploymentResults = {
            "camera_ids": [],  # List of camera IDs (existing + newly created)
            "pipeline_id": None,  # Created pipeline ID
            "errors": [],  # List of error/warning messages
            "success": False,  # Overall deployment success flag
        }

    def _add_error(self, error_msg: str, print_error: bool = True) -> None:
        """
        Utility method to add error to results and optionally print it.

        Parameters
        ----------
        error_msg : str
            Error message to add
        print_error : bool
            Whether to print the error message to console
        """
        self.results["errors"].append(error_msg)
        if print_error:
            print(f"ERROR: {error_msg}")

    def _print_info(self, message: str, prefix: str = "") -> None:
        """
        Utility method for consistent info logging.

        Parameters
        ----------
        message : str
            Message to print
        prefix : str
            Optional prefix for the message
        """
        if prefix:
            print(f"{prefix}: {message}")
        else:
            print(message)

    def _validate_camera_config(self, cameras_config: List[CameraConfig]) -> bool:
        """
        Validate camera configurations before processing.

        Required fields: name, path, type (RTSP, IP, or FILE).
        The API uses type to route the path: RTSP/IP -> cameraFeedPath, FILE -> simulationVideoPath.

        Parameters
        ----------
        cameras_config : List[CameraConfig]
            List of camera configurations to validate

        Returns
        -------
        bool
            True if all configurations are valid, False otherwise
        """
        if not cameras_config:
            self._add_error("No camera configurations provided")
            return False

        # Required fields: name, path, type (API needs protocolType for path routing)
        required_fields = ["name", "path", "type"]
        for i, cam_config in enumerate(cameras_config):
            # Check required fields are present and non-empty
            for field in required_fields:
                if not cam_config.get(field) or not str(cam_config.get(field)).strip():
                    self._add_error(f"Camera config {i + 1}: Missing required field '{field}'")
                    return False

            # Validate type is one of RTSP, IP, or FILE (API uses this to route cameraFeedPath vs simulationVideoPath)
            protocol_type = str(cam_config["type"]).strip().upper()
            if protocol_type not in VALID_PROTOCOL_TYPES:
                self._add_error(
                    f"Camera '{cam_config.get('name')}': Invalid 'type' '{cam_config.get('type')}'. "
                    f"Must be one of: {', '.join(VALID_PROTOCOL_TYPES)}"
                )
                return False

            # Validate camera name (no special characters that might break API)
            name = cam_config["name"]
            if not name.replace("_", "").replace("-", "").replace(".", "").isalnum():
                self._add_error(
                    f"Camera '{name}': Name contains invalid characters. Use only alphanumeric, underscore, dash, or dot."
                )
                return False

            # Validate path format for RTSP or file paths
            path = cam_config["path"]
            if not (
                path.startswith("rtsp://")
                or path.startswith("rtmps://")
                or path.startswith("http://")
                or path.startswith("https://")
                or Path(path).exists()
            ):
                print(f"WARNING: Camera '{name}': Path '{path}' may be invalid (not RTSP/HTTP URL or existing file)")

        return True

    # --- CONFIGURATION PARSING METHODS ---

    def _load_config(self, config_path: str) -> Tuple[List[CameraConfig], PipelineConfig]:
        """
        Load camera and pipeline configuration from JSON or CSV file.

        For JSON: Extract cameras[] and pipeline{} directly
        For CSV: Load cameras from rows, pipeline config from PIPELINE_CONFIG section

        Parameters
        ----------
        config_path : str
            Path to configuration file (.json or .csv)

        Returns
        -------
        Tuple[List[CameraConfig], PipelineConfig]
            (cameras_list, pipeline_config)
        """
        # Validate input path parameter
        if not config_path or not config_path.strip():
            raise ValueError("Configuration file path cannot be empty or None")

        path = Path(config_path.strip())
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        if path.suffix.lower() == ".json":
            print("Loading JSON configuration")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate that JSON contains an object at root level
            if not isinstance(data, dict):
                raise ValueError("Configuration file must contain a JSON object at root level")

            # Validate and extract cameras configuration
            raw_cameras = data.get("cameras", [])
            if not isinstance(raw_cameras, list):
                raise ValueError("Configuration field 'cameras' must be a list")

            # Enhanced schema validation: Check structure and required fields immediately
            for idx, cam in enumerate(raw_cameras):
                if not isinstance(cam, dict):
                    raise ValueError(f"Configuration field 'cameras[{idx}]' must be an object")

                # Validate required fields are present and non-empty
                if not cam.get("name") or not str(cam.get("name")).strip():
                    raise ValueError(f"Camera config {idx + 1}: Missing or empty required field 'name'")

                if not cam.get("path") or not str(cam.get("path")).strip():
                    raise ValueError(f"Camera config {idx + 1}: Missing or empty required field 'path'")

                # Validate type (required: API needs protocolType for cameraFeedPath vs simulationVideoPath routing)
                if not cam.get("type") or not str(cam.get("type")).strip():
                    raise ValueError(f"Camera config {idx + 1}: Missing or empty required field 'type'")
                protocol_type = str(cam.get("type")).strip().upper()
                if protocol_type not in VALID_PROTOCOL_TYPES:
                    raise ValueError(
                        f"Camera config {idx + 1}: Invalid 'type' '{cam.get('type')}'. "
                        f"Must be one of: {', '.join(VALID_PROTOCOL_TYPES)}"
                    )
                # Normalize type to uppercase for downstream use
                cam["type"] = protocol_type

                # Validate camera name format early
                name = str(cam["name"]).strip()
                if not name.replace("_", "").replace("-", "").replace(".", "").isalnum():
                    raise ValueError(
                        f"Camera '{name}': Invalid name format. Use only alphanumeric, underscore, dash, or dot characters."
                    )

            cameras: List[CameraConfig] = raw_cameras

            # Validate and extract pipeline configuration
            raw_pipeline = data.get("pipeline", {})
            if not isinstance(raw_pipeline, dict):
                raise ValueError("Configuration field 'pipeline' must be an object")
            pipeline_config: PipelineConfig = raw_pipeline
            return cameras, pipeline_config  # Return the cameras and pipeline configuration

        elif path.suffix.lower() == ".csv":
            print("Loading CSV configuration")
            cameras: List[CameraConfig] = []
            pipeline_config: PipelineConfig = {}

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Find pipeline config section if exists
            pipeline_start_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("PIPELINE_CONFIG"):
                    pipeline_start_idx = i
                    break

            # Parse cameras section
            camera_lines = lines[:pipeline_start_idx] if pipeline_start_idx != -1 else lines

            # Remove empty lines and strip whitespace
            camera_lines = [line.strip() for line in camera_lines if line.strip()]

            if camera_lines:
                reader = csv.DictReader(camera_lines)
                for row_num, row in enumerate(reader, start=2):  # Start at 2 for header row
                    # Convert CSV row to camera dict, handle apps field
                    camera: CameraConfig = dict(row)

                    # Enhanced validation: Check required fields and format
                    if not camera.get("name") or not str(camera.get("name")).strip():
                        raise ValueError(f"CSV row {row_num}: 'name' field is required and cannot be empty")

                    if not camera.get("path") or not str(camera.get("path")).strip():
                        raise ValueError(f"CSV row {row_num}: 'path' field is required and cannot be empty")

                    # Validate type (required: API needs protocolType for path routing)
                    if not camera.get("type") or not str(camera.get("type")).strip():
                        raise ValueError(f"CSV row {row_num}: 'type' field is required and cannot be empty")
                    protocol_type_raw = str(camera.get("type")).strip().upper()
                    if protocol_type_raw not in VALID_PROTOCOL_TYPES:
                        raise ValueError(
                            f"CSV row {row_num}: Invalid 'type' '{camera.get('type')}'. "
                            f"Must be one of: {', '.join(VALID_PROTOCOL_TYPES)}"
                        )

                    camera["name"] = str(camera["name"]).strip()
                    camera["path"] = str(camera["path"]).strip()
                    camera["type"] = protocol_type_raw  # Normalize to uppercase for consistency
                    for int_field in ["width", "height", "streamingFPS", "videoQuality"]:
                        if int_field in camera and camera[int_field]:
                            try:
                                camera[int_field] = int(camera[int_field])
                            except (ValueError, TypeError):
                                pass  # Keep original, will hit default in stream_settings
                    # Validate camera name format early (same as JSON validation)
                    name = camera["name"]
                    if not name.replace("_", "").replace("-", "").replace(".", "").isalnum():
                        raise ValueError(
                            f"CSV row {row_num}, Camera '{name}': Invalid name format. Use only alphanumeric, underscore, dash, or dot characters."
                        )

                    # Parse apps field if present
                    if "apps" in camera and isinstance(camera["apps"], str):
                        camera["apps"] = [app.strip() for app in camera["apps"].split(",") if app.strip()]
                    elif "apps" not in camera or not camera["apps"]:
                        camera["apps"] = []

                    cameras.append(camera)

            # Parse pipeline config section if exists
            if pipeline_start_idx != -1 and pipeline_start_idx + 1 < len(lines):
                pipeline_lines = lines[pipeline_start_idx + 1 :]  # Skip the PIPELINE_CONFIG header

                for line in pipeline_lines:
                    line = line.strip()
                    if line and "," in line:
                        # Split only on first comma to handle values that might contain commas
                        key, value = line.split(",", 1)
                        key = key.strip()
                        value = value.strip()

                        # Convert boolean values
                        if value.lower() in ("true", "false"):
                            value = value.lower() == "true"

                        pipeline_config[key] = value

            config_msg = f"Loaded {len(cameras)} cameras"
            if pipeline_config:
                config_msg += f" and pipeline config ({len(pipeline_config)} settings)"
            else:
                config_msg += " (no pipeline config)"
            print(config_msg)

            return cameras, pipeline_config
        else:
            raise ValueError("Configuration file must be .json or .csv format")

    def _initialize_session(self) -> bool:
        """
        Initialize authentication session and management objects.

        Returns
        -------
        bool
            True if initialization successful, False otherwise
        """
        # Validate credentials before attempting authentication
        if not self.account_number or self.account_number.strip() == "":
            self._add_error("Account number is required and cannot be empty")
            return False

        if not self.access_key or self.access_key.strip() == "":
            self._add_error("Access key is required and cannot be empty")
            return False

        if not self.secret_key or self.secret_key.strip() == "":
            self._add_error("Secret key is required and cannot be empty")
            return False

        # Validate required deployment context fields
        if not self.project_id or str(self.project_id).strip() == "":
            self._add_error("Project ID is required and cannot be empty")
            return False

        if not self.lan_id or str(self.lan_id).strip() == "":
            self._add_error("LAN ID is required and cannot be empty")
            return False

        if not self.cluster_name or str(self.cluster_name).strip() == "":
            self._add_error("Cluster name is required and cannot be empty")
            return False

        try:
            # # 1. Initialize the Session object DIRECTLY first
            # print("Creating authenticated session...")

            # self.session = Session(
            #     account_number=self.account_number,
            #     access_key=self.access_key,
            #     secret_key=self.secret_key,
            #     project_id=self.project_id,
            # )

            # if not self.session:
            #     self._add_error("Failed to construct Session object")
            #     return False
            # # 2. Pass the SESSION object to StreamingAutomation
            # print("Initializing StreamingAutomation client...")
            # self.streaming_automation = StreamingAutomation(
            #     session=self.session
            # )

            print("Initializing StreamingAutomation client...")
            # print(f"account_number type: {type(self.account_number)}, value: {self.account_number}")
            # print(f"access_key type: {type(self.access_key)}, value: {self.access_key}")
            # print(f"secret_key type: {type(self.secret_key)}, value: {self.secret_key}")
            # print(f"project_id type: {type(self.project_id)}, value: {self.project_id}")

            # print(f"lan_id type: {type(self.lan_id)}, value: {self.lan_id}")
            # print(f"cluster_name type: {type(self.cluster_name)}, value: {self.cluster_name}")
            # Using keyword arguments (account_number=self.account_number)
            # is the cleanest way to satisfy the SDK's requirements.
            try:
                self.streaming_automation = StreamingAutomation(
                    account_number=self.account_number,  # <--- Correct!
                    access_key=self.access_key,
                    secret_key=self.secret_key,
                    project_id=self.project_id,
                )
            except Exception:
                traceback.print_exc()  # This will show the FULL error chain
                return False
            print("StreamingAutomation created successfully")
            # Now extract the session it created internally
            self.session = self.streaming_automation.session
            print("Session extracted successfully")

            # 3. Initialize other management clients using the same session
            print("Initializing management clients...")
            self.camera_management = CameraManagement(self.session)
            print("CameraManagement created successfully")
            self.pipeline_management = InferencePipelineManagement(self.session)
            print("InferencePipelineManagement created successfully")

            print("Session initialization completed successfully")
            return True

        except Exception as e:
            traceback.print_exc()  # This will show the FULL error chain
            self._add_error(f"Authentication failed: {str(e)}")
            return False

    # --- CORE ORCHESTRATION METHODS ---

    def _sync_cameras(self, cameras_config: List[CameraConfig]) -> Dict[str, str]:
        """
        Registers cameras to the existing Location provided by Backend CLI.

        This method implements idempotent camera creation by:
        1. Validating camera configurations
        2. Fetching all existing cameras from the platform
        3. Building a lookup map by camera name to avoid duplicates
        4. Creating only cameras that don't already exist
        5. Returning a dictionary mapping camera names to their IDs

        Parameters
        ----------
        cameras_config : List[CameraConfig]
            List of camera configurations, each containing:
            - name: Camera name
            - path: RTSP stream URL or file path
            - apps: List of application names to assign

        Returns
        -------
        Dict[str, str]
            Dictionary mapping camera names to their IDs {"camera_name": "camera_id"}
            Preserves the intended mapping regardless of creation order
        """
        # Validate camera configurations first
        if not self._validate_camera_config(cameras_config):
            return {}

        # Dictionary to store camera name -> camera ID mappings
        camera_name_to_id: Dict[str, str] = {}

        # Fetch existing cameras to prevent duplicate creation
        camera_names_raw = [cam.get("name") for cam in cameras_config if cam.get("name")]
        # Deduplicate while preserving order to avoid redundant API calls
        camera_names_to_check = list(dict.fromkeys(camera_names_raw))

        # Build efficient lookup map: camera_name -> camera_id
        existing_camera_map: Dict[str, str] = {}

        try:
            if self.camera_management is None:
                raise RuntimeError("Camera management client not initialized")

            print(f"LOOKUP: Checking for {len(camera_names_to_check)} existing cameras using server-side search...")

            for camera_name in camera_names_to_check:
                data, error, message = self.camera_management.get_camera_streams_with_filters(
                    search=camera_name, limit=10
                )

                if error:
                    print(f"WARNING: Could not search for camera '{camera_name}': {error}")
                    continue

                # Check if we found the exact camera name match
                if data:
                    for cam in data:
                        cam_name = cam.get("cameraName")
                        if cam_name == camera_name:
                            camera_id = cam.get("_id") or cam.get("id")
                            if camera_id:
                                existing_camera_map[camera_name] = str(camera_id)
                                print(f"FOUND: Camera '{camera_name}' exists with ID {camera_id}")
                            break

                if camera_name not in existing_camera_map:
                    print(f"CREATE: Camera '{camera_name}' not found - will be created")

        except Exception as e:
            print(f"WARNING: Exception during camera lookup: {e}")

        # Process each camera configuration
        for cam_config in cameras_config:
            camera_name = cam_config.get("name")  # Config uses 'name' field
            if not camera_name:
                print("ERROR: Camera configuration missing 'name' field")
                continue

            # Check if camera already exists (idempotency)
            if camera_name in existing_camera_map:
                existing_id = existing_camera_map[camera_name]
                print(f"MATCH: Camera '{camera_name}' already exists. Using ID: {existing_id}")
                camera_name_to_id[camera_name] = existing_id
            else:
                print(f"CREATE: Registering new camera '{camera_name}' to Location {self.lan_id}")

                # Prepare camera payload according to CameraManagement API requirements

                # type is required (validated at load time): RTSP/IP use cameraFeedPath, FILE uses simulationVideoPath
                protocol_type = cam_config.get("type", "RTSP")  # Fallback only if validation was bypassed
                camera_url = cam_config.get("path", "")

                # Handle local video file upload if needed
                if protocol_type == "FILE" and camera_url and Path(camera_url).exists():
                    print(f"LOCAL FILE: Uploading {camera_url}...")
                    # Use StreamingAutomation's video upload capability
                    s3_url, upload_error = self.streaming_automation.upload_video(camera_url)
                    if s3_url and not upload_error:
                        camera_url = s3_url
                        print(f"UPLOADED: {s3_url}")
                    else:
                        print(f"UPLOAD FAILED: {upload_error}")
                        self.results["errors"].append(f"Failed to upload video '{camera_url}': {upload_error}")
                        continue

                # Build stream settings only for fields with non-empty values.
                # Omit customStreamSettings entirely when all optional fields are empty;
                # the API applies defaults for missing fields.
                stream_settings: Dict[str, Any] = {}
                for key in ("make", "model", "aspectRatio"):
                    val = cam_config.get(key)
                    if val is not None and str(val).strip():
                        stream_settings[key] = str(val).strip()
                for key in ("width", "height", "streamingFPS", "videoQuality"):
                    val = cam_config.get(key)
                    if val is not None and str(val).strip():
                        try:
                            stream_settings[key] = int(val)
                        except (ValueError, TypeError):
                            pass  # Skip invalid values; API will use defaults

                # Create camera using CameraManagement API directly
                # CameraManagement handles account_number from session automatically
                if self.camera_management is None:
                    print(f"ERROR: Camera management client not available for '{camera_name}'")
                    continue

                camera_payload: Dict[str, Any] = {
                    "lanId": self.lan_id,  # Location ID for gateway assignment
                    "clusterName": self.cluster_name,  # Compute cluster for gateway assignment
                    "cameraName": camera_name,  # API field name
                    "protocolType": protocol_type,
                    "accountNumber": self.account_number,
                }
                if stream_settings:
                    camera_payload["customStreamSettings"] = stream_settings

                # Set appropriate path field based on protocol
                if protocol_type == "FILE":
                    camera_payload["simulationVideoPath"] = camera_url
                else:
                    camera_payload["cameraFeedPath"] = camera_url

                # Create camera - CameraManagement API handles account_number from session
                # Returns 3-tuple: (list_of_cameras, error, message)
                try:
                    new_cameras, error, message = self.camera_management.create_camera_streams_batch([camera_payload])
                except Exception:
                    traceback.print_exc()
                    raise

                if new_cameras and len(new_cameras) > 0:
                    new_camera_id = new_cameras[0].get("_id") or new_cameras[0].get("id")
                    if new_camera_id:
                        new_camera_id_str = str(new_camera_id)
                        print(f"SUCCESS: Camera '{camera_name}' created with ID: {new_camera_id_str}")
                        camera_name_to_id[camera_name] = new_camera_id_str
                        # Update local map for subsequent iterations
                        existing_camera_map[camera_name] = new_camera_id_str
                    else:
                        print(f"ERROR: Camera '{camera_name}' created but no ID returned")
                else:
                    print(f"ERROR: Failed to create camera '{camera_name}': {error}")

        return camera_name_to_id

    def _deploy_pipeline(
        self, pipeline_config: PipelineConfig, camera_name_to_id: Dict[str, str], cameras_config: List[CameraConfig]
    ) -> Optional[str]:
        """
        Creates an inference pipeline with camera-to-application mappings.

        This method implements idempotent pipeline creation by:
        1. Checking if a pipeline with the same name already exists
        2. Creating a new pipeline only if it doesn't exist
        3. Mapping cameras to their assigned applications

        Parameters
        ----------
        pipeline_config : PipelineConfig
            Pipeline configuration containing:
            - name: Pipeline name (required)
            - description: Pipeline description (optional)
            - auto_start: Whether to start pipeline after creation (optional)
        camera_name_to_id : Dict[str, str]
            Dictionary mapping camera names to their IDs from _sync_cameras
        cameras_config : List[CameraConfig]
            Original camera configurations with application assignments

        Returns
        -------
        Optional[str]
            Pipeline ID if successful, None if failed
        """
        pipeline_name = pipeline_config.get("name", f"Auto-Pipeline-{int(time.time())}")

        # Check if pipeline already exists to maintain idempotency
        existing_pipeline_id: Optional[str] = None
        print(f"Checking for existing pipeline: '{pipeline_name}'")
        try:
            if self.streaming_automation is None:
                print("WARNING: Streaming automation client not available")
                return None
            # Use StreamingAutomation for pipeline operations (primary interface)
            existing_pipelines, error = self.streaming_automation.list_inference_pipelines(project_id=self.project_id)

            if error:
                print(f"WARNING: Could not list existing pipelines: {error}")
            elif existing_pipelines:
                # Search for matching pipeline name
                for pipeline in existing_pipelines:
                    if isinstance(pipeline, dict) and pipeline.get("name") == pipeline_name:
                        existing_pipeline_id = pipeline.get("_id") or pipeline.get("id")
                        print(f"MATCH: Pipeline '{pipeline_name}' already exists. ID: {existing_pipeline_id}")
                        break
        except Exception as e:
            print(f"WARNING: Exception checking existing pipelines: {e}")

        # Build camera-to-application mapping (needed for both new and existing pipelines)
        camera_app_mapping: List[Dict[str, Any]] = []
        app_cache: Dict[str, Optional[str]] = {}

        for cam_config in cameras_config:
            camera_name = cam_config.get("name")
            if not camera_name:
                continue

            # Look up camera ID by name to ensure correct mapping
            camera_id = camera_name_to_id.get(camera_name)
            if not camera_id:
                print(f"WARNING: Camera '{camera_name}' was not successfully created, skipping")
                continue

            # Get applications assigned to this specific camera
            apps = cam_config.get("apps", [])
            if apps:
                # Use StreamingAutomation for application lookup (consistent API pattern)
                applications = []
                for app_name in apps:
                    try:
                        if self.streaming_automation is None:
                            print(f"WARNING: Streaming automation client not available for app '{app_name}'")
                            continue

                        # Check cache first
                        if app_name in app_cache:
                            app_id = app_cache[app_name]
                            if app_id:
                                applications.append({"_idApplication": app_id})
                            continue

                        # Lookup application and cache result
                        app, error = self.streaming_automation.find_application_by_name(app_name)
                        print(f"App found: {app}")
                        print(f"App error: {error}")
                        if error or not app:
                            print(f"WARNING: Could not find application '{app_name}': {error}")
                            app_cache[app_name] = None  # Cache negative result
                            continue
                        app_id = app.get("_id") or app.get("id")
                        if app_id:
                            app_cache[app_name] = app_id  # Cache positive result
                            applications.append({"_idApplication": app_id})
                    except Exception as e:
                        print(f"WARNING: Exception finding application '{app_name}': {e}")

                if applications:
                    camera_app_mapping.append({"cameraId": camera_id, "applications": applications})
                    print(
                        f"MAPPED: Camera '{camera_name}' (ID: {camera_id}) -> Apps: {[app['name'] if isinstance(app, dict) else str(app) for app in apps]}"
                    )

        if not camera_app_mapping:
            error_msg = (
                "No applications assigned to cameras. Pipeline creation requires at least one camera with applications."
            )
            print(f"ERROR: {error_msg}")
            self.results["errors"].append(error_msg)
            return None

        # If pipeline already exists, add cameras to it and return
        if existing_pipeline_id:
            print(f"Adding cameras and applications to existing pipeline '{pipeline_name}'...")
            try:
                if self.streaming_automation is None:
                    return None
                result, add_error = self.streaming_automation.add_cameras_and_applications_to_pipeline(
                    pipeline_id=existing_pipeline_id, cameras=camera_app_mapping, compute_alias=""
                )
                if add_error:
                    print(f"WARNING: Failed to add cameras to existing pipeline: {add_error}")
                else:
                    print("SUCCESS: Cameras and applications added to existing pipeline")
                    print(f"Result: {result}")
            except Exception as e:
                print(f"WARNING: Exception adding cameras to existing pipeline: {e}")
            return existing_pipeline_id

        # Pipeline doesn't exist, create new one
        print(f"CREATE: Building new pipeline '{pipeline_name}'")
        try:
            if self.streaming_automation is None:
                error_msg = "Streaming automation client not available for pipeline creation"
                print(f"ERROR: {error_msg}")
                self.results["errors"].append(error_msg)
                return None

            pipeline_id, error = self.streaming_automation.create_inference_pipeline(
                name=pipeline_name,
                project_id=self.project_id,
                cameras=camera_app_mapping,
                description=pipeline_config.get("description", ""),
                access_scale=pipeline_config.get("access_scale", "local"),
                deploy_type=pipeline_config.get("deploy_type", "real_time"),
                server_type=pipeline_config.get("server_type", "fastapi"),
                user_id="",
                cluster_name=self.cluster_name,
                runtime_framework=pipeline_config.get("runtime_framework", "Triton"),
            )

            if error:
                error_msg = f"Pipeline creation failed: {error}"
                print(f"ERROR: {error_msg}")
                self.results["errors"].append(error_msg)
                return None

            print(f"SUCCESS: Pipeline '{pipeline_name}' created with ID: {pipeline_id}")
            print("Adding cameras and applications to pipeline...")
            result, add_error = self.streaming_automation.add_cameras_and_applications_to_pipeline(
                pipeline_id=pipeline_id, cameras=camera_app_mapping, compute_alias=""
            )

            if add_error:
                print(f"WARNING: Failed to add cameras to pipeline: {add_error}")
            else:
                print("SUCCESS: Cameras and applications added to pipeline")
                print(f"Result: {result}")

            return pipeline_id

        except Exception as e:
            error_msg = f"Exception during pipeline creation: {str(e)}"
            print(f"ERROR: {error_msg}")
            self.results["errors"].append(error_msg)
            return None

    def _monitor_health(self, pipeline_id: str) -> bool:
        """
        Starts the inference pipeline and monitors its status until running.

        This method performs the following steps:
        1. Sends start command to the pipeline using the configured cluster_name
        2. Monitors pipeline status with 30-second polling intervals
        3. Returns success when pipeline reaches 'running' state
        4. Returns failure if pipeline enters error state or times out

        Parameters
        ----------
        pipeline_id : str
            ID of the pipeline to start and monitor

        Returns
        -------
        bool
            True if pipeline starts successfully and reaches 'running' state,
            False if pipeline fails to start, enters error state, or times out
        """
        print(f"Starting pipeline {pipeline_id} on cluster: {self.cluster_name}")

        # Start the pipeline using correct API signature
        # The start_inference_pipeline method requires: (pipeline_id, compute_alias, cluster_name)
        try:
            if self.streaming_automation is None:
                error_msg = "Streaming automation client not available for pipeline start"
                print(f"ERROR: {error_msg}")
                self.results["errors"].append(error_msg)
                return False
            success, error = self.streaming_automation.start_inference_pipeline(
                pipeline_id=pipeline_id,
                compute_alias="",  # we send an empty string for compute_alias since the API requires it but we are using cluster_name for assignment
                cluster_name=self.cluster_name,
            )

            if not success:
                error_msg = f"Pipeline start command failed: {error}"
                print(f"ERROR: {error_msg}")
                self.results["errors"].append(error_msg)
                return False

            print("Pipeline start command sent successfully")

        except Exception as e:
            error_msg = f"Exception starting pipeline: {str(e)}"
            print(f"ERROR: {error_msg}")
            self.results["errors"].append(error_msg)
            return False

        # Monitor pipeline status with polling (maximum 300 seconds = 5 minutes)
        print("Monitoring pipeline status (maximum 300 seconds)...")
        max_wait_time: Final[int] = 300  # 5 minutes total timeout
        check_interval: Final[int] = 30  # Check every 30 seconds
        elapsed_time = 0

        # Check this BEFORE the loop starts
        if not self.pipeline_management:
            error_msg = "Pipeline management client not initialized"
            print(f"ERROR: {error_msg}")
            self.results["errors"].append(error_msg)
            return False

        while elapsed_time < max_wait_time:
            current_status = "unknown"  # Default for this iteration

            # Get pipeline status with robust error handling
            try:
                # Wrap API call in specific try-catch for network/API errors
                try:
                    pipeline_data, error, message = self.pipeline_management.get_inference_pipeline_by_id(pipeline_id)
                except Exception as api_error:
                    print(f"WARNING: API call failed (network/server error): {api_error}")
                    print(f"Retrying in {check_interval} seconds...")
                    # Continue to next iteration rather than failing entire deployment
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                    continue

                if error:
                    print(f"WARNING: API Error: {error}")
                    # For API errors, continue polling rather than failing immediately
                    print("Continuing to monitor despite API error...")
                elif pipeline_data:
                    current_status = str(pipeline_data.get("status", "unknown")).lower()
                    # Debug: Show available fields if status field is missing
                    if current_status == "unknown":
                        available_fields = (
                            list(pipeline_data.keys()) if isinstance(pipeline_data, dict) else "not a dict"
                        )
                        print(f"DEBUG: No 'status' field found. Available fields: {available_fields}")

                print(f"Status check: {current_status} (elapsed: {elapsed_time}s)")

                # 1. SUCCESS: Exit and return True
                if current_status in {"running", "active"}:
                    print("SUCCESS: Pipeline is now running!")
                    return True

                # 2. FAILURE: Exit and return False
                failed_statuses = {"failed", "error", "crashed", "stopped"}
                if current_status in failed_statuses:
                    error_msg = f"Pipeline failed to start. Final status: {current_status}"
                    print(f"ERROR: {error_msg}")
                    self.results["errors"].append(error_msg)
                    return False

                # 3. TRANSITIONAL: (starting, created, unknown)
                # Continue monitoring - no explicit handling needed

            except Exception as e:
                print(f"WARNING: Unexpected exception during status check: {e}")
                # Continue monitoring rather than crashing

            # Wait before next status check
            time.sleep(check_interval)
            elapsed_time += check_interval

        # Timeout reached without reaching running state
        warning_msg = f"Pipeline status monitoring timed out after {max_wait_time} seconds"
        print(f"ERROR: {warning_msg}")
        self.results["errors"].append(warning_msg)

        # Treat timeout as failure since running state was not confirmed
        # This ensures deployment failures are not masked by uncertain timeouts
        return False

    def _get_pipeline_config(self, config_data: Dict[str, Any], default_name: str = "Auto-Pipeline") -> PipelineConfig:
        """
        Extract pipeline configuration from config data with validated defaults.

        Parameters
        ----------
        config_data : Dict[str, Any]
            Configuration data that may contain pipeline settings
        default_name : str
            Default pipeline name if not specified

        Returns
        -------
        PipelineConfig
            Pipeline configuration with core settings and validated defaults
        """
        pipeline_config = config_data.get("pipeline", {}) if isinstance(config_data, dict) else {}

        # Define validated defaults for better type safety
        validated_config: PipelineConfig = {
            "name": pipeline_config.get("name", default_name),
            "description": pipeline_config.get("description", "Auto-generated inference pipeline"),
            "runtime_framework": pipeline_config.get("runtime_framework", "Triton"),
            "access_scale": pipeline_config.get("access_scale", "local"),
            "deploy_type": pipeline_config.get("deploy_type", "real_time"),  # Aligned with API default
            "server_type": pipeline_config.get("server_type", "fastapi"),
            "auto_start": pipeline_config.get("auto_start", True),
        }

        return validated_config

    # --- MAIN DEPLOYMENT ORCHESTRATOR ---

    def deploy_cameras_and_pipeline(
        self,
        cameras_config_path: str,
        pipeline_name: str = "Auto-Pipeline",
        pipeline_config: Optional[PipelineConfig] = None,
    ) -> DeploymentResults:
        """
        Main method: Deploy cameras and pipeline from configuration file.

        This method:
        1. Parse camera configuration (JSON/CSV)
        2. Initialize authentication session
        3. Create cameras (idempotent)
        4. Create inference pipeline with camera-app mappings
        5. Start pipeline and monitor health

        Parameters
        ----------
        cameras_config_path : str
            Path to cameras configuration file (JSON or CSV)
        pipeline_name : str, optional
            Name for the inference pipeline (default: "Auto-Pipeline")
        pipeline_config : PipelineConfig, optional
            Detailed pipeline configuration (overrides settings from config file)

        Returns
        -------
        DeploymentResults
            Deployment results with camera_ids, pipeline_id, errors, success status
        """
        print("=" * 60)
        print("MATRICE AI: INFERENCE ORCHESTRATOR")
        print("=" * 60)

        # Pre-flight safety checks
        if not self.account_number or not self.access_key or not self.secret_key:
            self._add_error("Authentication credentials cannot be empty")
            return self.results

        if not self.project_id or not self.lan_id or not self.cluster_name:
            self._add_error("Deployment context (project_id, lan_id, cluster_name) cannot be empty")
            return self.results

        try:
            # Step 1: Load configuration with validation
            if not cameras_config_path or not cameras_config_path.strip():
                raise ValueError("Configuration file path is required")

            print(f"[1/4] Loading configuration: {cameras_config_path}")

            cameras_config, loaded_pipeline_config = self._load_config(cameras_config_path)

            if not cameras_config:
                raise ValueError("No cameras found in configuration")

            print(f"Found {len(cameras_config)} cameras to deploy")

            # Extract pipeline configuration (use provided config or loaded config)
            if pipeline_config is None:
                pipeline_config = self._get_pipeline_config({"pipeline": loaded_pipeline_config}, pipeline_name)
            else:
                # Merge provided config with defaults (provided values override defaults)
                default_config = self._get_pipeline_config({}, pipeline_name)
                pipeline_config = {**default_config, **pipeline_config}

            print(f"Pipeline config: {pipeline_config['name']} ({pipeline_config['runtime_framework']})")

            # Step 2: Initialize API session
            print("[2/4] Initializing session and authenticating...")
            if not self._initialize_session():
                print(f"FAILED: Authentication failed: {self.results['errors']}")
                return self.results

            print("Deployment context:")
            print(f"  - Project ID: {self.project_id}")
            print(f"  - LAN ID: {self.lan_id}")
            print(f"  - Cluster Name: {self.cluster_name}")

            # Step 3: Create cameras
            print("[3/4] Creating cameras...")
            camera_name_to_id = self._sync_cameras(cameras_config)

            # Convert dictionary to list for results tracking
            self.results["camera_ids"] = list(camera_name_to_id.values())

            if not camera_name_to_id:
                print("FAILED: No cameras were successfully created")
                return self.results
            else:
                print(f"SUCCESS: {len(camera_name_to_id)} cameras ready")
                # Show the camera name -> ID mappings for transparency
                for name, cam_id in camera_name_to_id.items():
                    print(f"  - {name}: {cam_id}")

            # Step 4: Create and start pipeline
            print("[4/4] Creating and starting inference pipeline...")
            pipeline_id = self._deploy_pipeline(pipeline_config, camera_name_to_id, cameras_config)

            if not pipeline_id:
                print("FAILED: Pipeline creation failed")
                return self.results

            self.results["pipeline_id"] = pipeline_id

            # Start and monitor pipeline (if auto_start is enabled)
            if pipeline_config.get("auto_start", True):
                print("Starting pipeline and monitoring health...")
                if self._monitor_health(pipeline_id):
                    self.results["success"] = True
                    print("DEPLOYMENT SUCCESSFUL: All services running")
                else:
                    print("DEPLOYMENT PARTIALLY SUCCESSFUL: Pipeline created but failed to start")
            else:
                print("Pipeline created but not started (auto_start=False)")
                self.results["success"] = True

            # Print summary
            print("\nDEPLOYMENT SUMMARY:")
            print(f"  - Cameras created: {len(self.results['camera_ids'])}")
            print(f"  - Pipeline ID: {self.results['pipeline_id']}")
            if self.results["errors"]:
                print(f"  - Issues: {len(self.results['errors'])}")
                for error in self.results["errors"]:
                    print(f"    * {error}")

            return self.results

        except Exception as e:
            traceback.print_exc()
            error_msg = f"Critical deployment exception: {str(e)}"
            print(f"CRITICAL ERROR: {error_msg}")
            self.results["errors"].append(error_msg)
            return self.results


# --- ENTRY POINT ---
if __name__ == "__main__":
    load_dotenv()

    # ===========================================================================
    # HOW CREDENTIALS ARE RESOLVED
    # ===========================================================================
    # This script supports TWO credential sources — automatically detected:
    #
    #   1. CLI ARGS (Production / Backend CLI)
    #      python inference_orchestrator.py <config_file> <project_id> <lan_id>
    #                                        <cluster_name> <account_number>
    #                                        [access_key] [secret_key]
    #
    #      access_key and secret_key are optional as CLI args — if omitted,
    #      they fall back to env vars MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY
    #
    #   2. ENV VARS (Dev / Testing)
    #      Set in .env file or shell. No CLI args needed.
    #      Activate a dev mode below (USE_CSV_CONFIG, USE_JSON_CONFIG, USE_BUILTIN_CONFIG)
    #
    # DETECTION LOGIC:
    #   - If CLI args are present (sys.argv has >= 2 args) → CLI mode (production)
    #   - If no CLI args → Dev mode (env vars + mode flags below)
    # ===========================================================================

    # ---------------------------------------------------------------------------
    # SHARED: Logging setup
    # ---------------------------------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler("inference_orchestrator.log"), logging.StreamHandler()],
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )

    # ===========================================================================
    # CONFIGURATION & CREDENTIAL RESOLUTION
    # ===========================================================================
    # This script handles different deployment environments. Below are the modes for resolving infrastructure IDs and secure credentials.

    # ===========================================================================
    # MODE 1: FULL PRODUCTION (CLI ARGS) - CURRENTLY DISABLED
    # ===========================================================================
    # This block is commented out but kept for reference. It is designed for a
    # strict production environment (e.g., triggered by a backend service) where
    # ALL parameters are passed directly as command-line arguments in a specific order.
    #
    # Expected CLI structure:
    # python inference_orchestrator.py <config_file> <project_id> <lan_id> \
    #                                  <cluster_name> <account_number> \
    #                                  [access_key] [secret_key]
    #
    # if len(sys.argv) >= 6:
    #     print("=== MODE: PRODUCTION (CLI ARGS) ===")
    #
    #     cameras_file   = sys.argv[1]
    #     project_id     = sys.argv[2]
    #     lan_id         = sys.argv[3]
    #     cluster_name   = sys.argv[4]
    #     account_number = sys.argv[5]
    #
    #     # Optional CLI args for keys, falling back to environment variables if omitted
    #     # access_key = sys.argv[6] if len(sys.argv) > 6 else os.environ.get("MATRICE_ACCESS_KEY_ID", "")
    #     # secret_key = sys.argv[7] if len(sys.argv) > 7 else os.environ.get("MATRICE_SECRET_ACCESS_KEY", "")

    # ===========================================================================
    # MODE 2: HYBRID (CLI Config + ENV Credentials) - ACTIVE
    # ===========================================================================
    # This is the current active mode. It expects ONLY the configuration file path
    # to be passed via the CLI (supports .json or .csv). For security and convenience,
    # all other sensitive credentials and infrastructure IDs are extracted securely
    # from system environment variables.
    #
    # Expected CLI structure:
    # python inference_orchestrator.py <cameras_file>
    #
    if len(sys.argv) >= 2:
        print("=== MODE: HYBRID (CLI Config + ENV Credentials) ===")

        # 1. Get the configuration file from the command line argument
        cameras_file = sys.argv[1]

        # 2. Pull all authentication and infrastructure details from environment variables
        account_number = os.environ.get("MATRICE_ACCOUNT_NUMBER")
        access_key = os.environ.get("MATRICE_ACCESS_KEY_ID")
        secret_key = os.environ.get("MATRICE_SECRET_ACCESS_KEY")
        project_id = os.environ.get("MATRICE_PROJECT_ID")
        lan_id = os.environ.get("MATRICE_LAN_ID")
        cluster_name = os.environ.get("MATRICE_CLUSTER_NAME")

        # Validate config file exists before proceeding
        if not Path(cameras_file).exists():
            print(f"\nERROR: Config file not found: {cameras_file}")
            sys.exit(1)

        # Validate credentials are present
        if not access_key or not secret_key:
            print("\nERROR: access_key and secret_key must be provided as CLI args or env vars:")
            print("  CLI  : python inference_orchestrator.py config.json ... acc123 mykey mysecret")
            print("  ENV  : export MATRICE_ACCESS_KEY_ID=mykey && export MATRICE_SECRET_ACCESS_KEY=mysecret")
            sys.exit(1)

        print(f"  Config file  : {cameras_file}")
        print(f"  Project ID   : {project_id}")
        print(f"  LAN ID       : {lan_id}")
        print(f"  Cluster Name : {cluster_name}")
        print(f"  Account      : {account_number}")
        print(f"  Access Key   : {'from CLI' if len(sys.argv) > 6 else 'from env var'}")

        automation = CustomerOnboardingAutomation(
            account_number=account_number,
            access_key=access_key,
            secret_key=secret_key,
            project_id=project_id,
            lan_id=lan_id,
            cluster_name=cluster_name,
        )

        try:
            results = automation.deploy_cameras_and_pipeline(cameras_file)
            print(f"\nResults: {results}")
            sys.exit(0 if results.get("success", False) else 1)
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            sys.exit(1)

    # ===========================================================================
    # DEV / TESTING MODE — ENV VARS
    # ===========================================================================
    # Triggered when no CLI args are passed.
    # Credentials are read from .env file or shell environment variables.
    #
    # Set ONE of the following to True, keep the others False:
    #
    #   USE_CSV_CONFIG     → Run with a CSV config file (e.g. test_config.csv)
    #   USE_JSON_CONFIG    → Run with a JSON config file (e.g. test_config.json)
    #   USE_BUILTIN_CONFIG → Run with hardcoded cameras/pipeline (no file needed)
    # ===========================================================================
    else:
        USE_CSV_CONFIG = True
        USE_JSON_CONFIG = False
        USE_BUILTIN_CONFIG = False

        # Validate env vars before proceeding
        PLACEHOLDER_VALUES = {
            "YOUR_ACCESS_KEY",
            "YOUR_SECRET_KEY",
            "YOUR_ACCOUNT_NUMBER",
            "YOUR_PROJECT_ID",
            "YOUR_LAN_ID",
            "YOUR_CLUSTER_NAME",
            "",
            "null",
            "None",
            "undefined",
        }

        required_env_vars = {
            "MATRICE_ACCESS_KEY_ID": "Access Key ID",
            "MATRICE_SECRET_ACCESS_KEY": "Secret Access Key",  # nosec B105 - label, not a password
            "MATRICE_ACCOUNT_NUMBER": "Account Number",
            "MATRICE_PROJECT_ID": "Project ID",
            "MATRICE_LAN_ID": "LAN ID",
            "MATRICE_CLUSTER_NAME": "Cluster Name",
        }

        missing_vars = []
        placeholder_vars = []

        for var_name, var_desc in required_env_vars.items():
            current_value = os.environ.get(var_name, "")
            if not current_value:
                missing_vars.append(f"{var_name} ({var_desc})")
            elif current_value in PLACEHOLDER_VALUES:
                placeholder_vars.append(f"{var_name} ({var_desc}) = '{current_value}'")

        if missing_vars or placeholder_vars:
            print("CREDENTIAL VALIDATION FAILED")
            if missing_vars:
                print("\nMissing environment variables:")
                for var in missing_vars:
                    print(f"  - {var}")
            if placeholder_vars:
                print("\nPlaceholder values detected:")
                for var in placeholder_vars:
                    print(f"  - {var}")
            print("\nSet these in your .env file or shell:")
            print("  MATRICE_ACCESS_KEY_ID=your_actual_access_key")
            print("  MATRICE_SECRET_ACCESS_KEY=your_actual_secret_key")
            print("  MATRICE_ACCOUNT_NUMBER=your_actual_account_number")
            print("  MATRICE_PROJECT_ID=your_actual_project_id")
            print("  MATRICE_LAN_ID=your_actual_lan_id")
            print("  MATRICE_CLUSTER_NAME=your_actual_cluster_name")
            print("\nABORTING.")
            sys.exit(1)

        # Build automation object from env vars
        automation = CustomerOnboardingAutomation(
            account_number=os.environ.get("MATRICE_ACCOUNT_NUMBER", ""),
            access_key=os.environ.get("MATRICE_ACCESS_KEY_ID", ""),
            secret_key=os.environ.get("MATRICE_SECRET_ACCESS_KEY", ""),
            project_id=os.environ.get("MATRICE_PROJECT_ID", ""),
            lan_id=os.environ.get("MATRICE_LAN_ID", ""),
            cluster_name=os.environ.get("MATRICE_CLUSTER_NAME", ""),
        )

        # -----------------------------------------------------------------------
        # DEV MODE 1: CSV CONFIG FILE
        # -----------------------------------------------------------------------
        # To activate: set USE_CSV_CONFIG = True
        # -----------------------------------------------------------------------
        if USE_CSV_CONFIG:
            CSV_CONFIG_PATH = "sample_cameras_config.csv"  # ← Change as needed
            PIPELINE_NAME = "Production_Inference_Pipeline_CSV"  # ← Change as needed

            print(f"=== MODE: CSV CONFIG FILE ({CSV_CONFIG_PATH}) ===")
            try:
                if not automation._initialize_session():
                    print("FAILED: Authentication failed")
                    sys.exit(1)

                results = automation.deploy_cameras_and_pipeline(
                    cameras_config_path=CSV_CONFIG_PATH, pipeline_name=PIPELINE_NAME
                )
                print(f"\nResults: {results}")
                sys.exit(0 if results.get("success", False) else 1)
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                sys.exit(1)

        # -----------------------------------------------------------------------
        # DEV MODE 2: JSON CONFIG FILE
        # -----------------------------------------------------------------------
        # To activate: set USE_JSON_CONFIG = True
        # -----------------------------------------------------------------------
        elif USE_JSON_CONFIG:
            JSON_CONFIG_PATH = "sample_cameras_config.json"  # ← Change as needed
            PIPELINE_NAME = "Production-Inference-Pipeline"  # ← Change as needed

            print(f"=== MODE: JSON CONFIG FILE ({JSON_CONFIG_PATH}) ===")
            try:
                if not automation._initialize_session():
                    print("FAILED: Authentication failed")
                    sys.exit(1)

                results = automation.deploy_cameras_and_pipeline(
                    cameras_config_path=JSON_CONFIG_PATH, pipeline_name=PIPELINE_NAME
                )
                print(f"\nResults: {results}")
                sys.exit(0 if results.get("success", False) else 1)
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                sys.exit(1)

        # -----------------------------------------------------------------------
        # DEV MODE 3: BUILT-IN HARDCODED CONFIG (no config file needed)
        # -----------------------------------------------------------------------
        # To activate: set USE_BUILTIN_CONFIG = True
        # Edit the cameras list and dev_pipeline_config dict directly below.
        # -----------------------------------------------------------------------
        elif USE_BUILTIN_CONFIG:
            print("=== MODE: BUILT-IN HARDCODED CONFIG ===")

            # Edit camera entries as needed.
            # 'type': 'FILE' for local video, 'RTSP' for live stream.
            # Numeric fields must be integers (not strings).
            cameras = [
                {
                    "name": "Demo_Camera_1",
                    "path": "C:\\Users\\Global\\Downloads\\5325136-hd_1920_1080_30fps.mp4",
                    "type": "FILE",
                    "apps": ["People Counting"],
                    "width": 1280,
                    "height": 720,
                    "streamingFPS": 15,
                    "aspectRatio": "16:9",
                    "videoQuality": 85,
                },
                # ← Add more camera dicts here if needed
            ]

            # Edit pipeline settings as needed.
            # auto_start=False → pipeline created but NOT started (safe for inspection)
            # auto_start=True  → pipeline starts immediately after creation
            dev_pipeline_config = {
                "name": "Demo_Pipeline",
                "description": "Development testing pipeline",
                "runtime_framework": "Triton",
                "access_scale": "local",
                "deploy_type": "real_time",
                "server_type": "fastapi",
                "auto_start": True,  # ← Set False to skip start + health monitoring
            }

            try:
                if not automation._initialize_session():
                    print("FAILED: Authentication failed")
                    sys.exit(1)

                # Step 1: Create / sync cameras
                camera_name_to_id = automation._sync_cameras(cameras)
                automation.results["camera_ids"] = list(camera_name_to_id.values())

                if not camera_name_to_id:
                    print("FAILED: No cameras were created")
                    sys.exit(1)

                # Step 2: Create pipeline
                print(f"\n[BUILTIN] Creating pipeline: {dev_pipeline_config['name']}")
                pipeline_id = automation._deploy_pipeline(dev_pipeline_config, camera_name_to_id, cameras)

                if not pipeline_id:
                    print("FAILED: Pipeline creation failed")
                    sys.exit(1)

                automation.results["pipeline_id"] = pipeline_id
                print(f"Pipeline created: {pipeline_id}")

                # Step 3: Start and monitor (only if auto_start=True)
                if dev_pipeline_config.get("auto_start", False):
                    print("Starting pipeline and monitoring health...")
                    if automation._monitor_health(pipeline_id):
                        automation.results["success"] = True
                        print("\nDEPLOYMENT SUCCESSFUL: Pipeline is running!")
                    else:
                        print("\nDEPLOYMENT FAILED: Pipeline created but failed to start")
                else:
                    # auto_start=False: pipeline exists but is not running.
                    # Inspect in admin console before starting manually.
                    automation.results["success"] = True
                    print("\nPipeline created but NOT started (auto_start=False).")
                    print(f"  → Find pipeline ID {pipeline_id} in the admin console to start manually.")

            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                sys.exit(1)

            print(f"\nResults: {automation.results}")
            sys.exit(0 if automation.results.get("success", False) else 1)

        else:
            print("ERROR: No mode selected. Set one of USE_CSV_CONFIG, USE_JSON_CONFIG, or USE_BUILTIN_CONFIG to True.")
            sys.exit(1)
