"""
Benchmarking module for streaming infrastructure load testing.

This module provides automated load testing capabilities by incrementally
adding cameras to a streaming pipeline and collecting performance metrics.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(r"C:\Users\Adminstrator\Desktop\Matrice\release\py_matrice\py_common\src")

from matrice.streaming_automation import StreamingAutomation


class StreamingBenchmarking:
    """
    Automated load testing for streaming infrastructure.

    Incrementally adds cameras to a pipeline and collects performance metrics
    from streaming gateway and inference pipeline.

    Attributes
    ----------
    video_path : str
        Path to video file for camera simulation
    compute_alias : str
        Compute resource identifier
    app_name : str
        Application name for inference
    min_cameras : int
        Minimum cameras to start with
    max_cameras : int
        Maximum cameras to add
    interval_minutes : float
        Minutes between adding cameras
    step_size : int
        Number of cameras to add at each interval
    metrics_interval_minutes : float
        Minutes between collecting metrics
    output_file : str
        Path to JSON output file

    Examples
    --------
    >>> benchmark = StreamingBenchmarking(
    ...     video_path="/path/to/video.mp4",
    ...     compute_alias="benchmark-device",
    ...     app_name="People Counting",
    ...     account_number="ACC123",
    ...     access_key="key",
    ...     secret_key="secret",
    ...     project_id="proj_id",
    ...     min_cameras=1,
    ...     max_cameras=20,
    ...     interval_minutes=5.0,
    ...     step_size=2,
    ...     metrics_interval_minutes=0.5,
    ...     camera_batch_size=10,
    ...     pipeline_batch_size=10,
    ...     auto_start=True
    ... )
    >>> benchmark.initialize_setup()
    >>> benchmark.start_benchmark(duration_minutes=30)
    >>> benchmark.stop_benchmark()
    >>> benchmark.export_results()
    """

    def __init__(
        self,
        video_path: str,
        compute_alias: str,
        app_name: str,
        account_number: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        min_cameras: int = 1,
        max_cameras: int = 20,
        interval_minutes: float = 5.0,
        step_size: int = 1,
        metrics_interval_minutes: float = 0.5,
        output_file: str = "benchmark_results.json",
        fps: int = 10,
        width: int = 640,
        height: int = 480,
        video_quality: int = 80,
        aspect_ratio: str = "16:9",
        state_file: Optional[str] = None,
        auto_resume: bool = True,
        camera_batch_size: int = 10,
        pipeline_batch_size: int = 10,
        auto_start: bool = True,
        facial_recognition_server_id: Optional[str] = None,
        lpr_server_id: Optional[str] = None,
        cluster_name: Optional[str] = None,
        lan_id: str = "",
        runtime_framework: str = "Triton",
    ):
        """
        Initialize streaming benchmarking.

        Parameters
        ----------
        video_path : str
            Path to video file for camera simulation
        compute_alias : str
            Compute resource identifier
        app_name : str
            Application name for inference
        account_number : str
            Matrice account number
        access_key : str, optional
            API access key
        secret_key : str, optional
            API secret key
        project_id : str, optional
            Project ID
        project_name : str, optional
            Project name
        min_cameras : int, optional
            Minimum cameras to start with (default: 1)
        max_cameras : int, optional
            Maximum cameras to add (default: 20)
        interval_minutes : float, optional
            Minutes between adding cameras (default: 5.0)
        step_size : int, optional
            Number of cameras to add at each interval (default: 1)
        metrics_interval_minutes : float, optional
            Minutes between collecting metrics (default: 0.5)
        output_file : str, optional
            JSON output file path (default: "benchmark_results.json")
        fps : int, optional
            Frames per second for camera streams (default: 10)
        width : int, optional
            Video width in pixels (default: 640)
        height : int, optional
            Video height in pixels (default: 480)
        video_quality : int, optional
            Video quality 0-100 (default: 80)
        aspect_ratio : str, optional
            Video aspect ratio (default: "16:9")
        state_file : str, optional
            Path to state file for crash recovery. If None, uses output_file.
        auto_resume : bool, optional
            Automatically resume from state file if it exists (default: True)
        camera_batch_size : int, optional
            Number of cameras to create in each batch (default: 10)
        pipeline_batch_size : int, optional
            Number of cameras to add to pipeline in each batch (default: 10)
        auto_start : bool, optional
            Automatically start streaming gateway and inference pipeline after creation (default: True)
        facial_recognition_server_id : str, optional
            Facial recognition server ID (required for FR applications like "Face Recognition")
        lpr_server_id : str, optional
            LPR server ID (required for LPR applications like "License Plate Recognition")
        cluster_name : str, optional
            Cluster name for deployment (e.g., "thor2"). If None, uses compute_alias.
        runtime_framework : str, optional
            Runtime framework (default: "Triton")
        """
        self.video_path = video_path
        self.compute_alias = compute_alias
        self.app_name = app_name
        self.min_cameras = min_cameras
        self.facial_recognition_server_id = facial_recognition_server_id
        self.lpr_server_id = lpr_server_id
        self.cluster_name = cluster_name or compute_alias  # Default to compute_alias if not provided
        self.runtime_framework = runtime_framework
        self.max_cameras = max_cameras
        self.interval_minutes = interval_minutes
        self.step_size = step_size
        self.metrics_interval_minutes = metrics_interval_minutes
        self.output_file = output_file
        self.state_file = state_file or output_file
        self.auto_resume = auto_resume
        self.camera_batch_size = camera_batch_size
        self.pipeline_batch_size = pipeline_batch_size
        self.auto_start = auto_start

        # Initialize logger
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.fps = fps
        self.width = width
        self.height = height
        self.video_quality = video_quality
        self.aspect_ratio = aspect_ratio

        # Initialize automation
        self.automation = StreamingAutomation(
            account_number=account_number,
            access_key=access_key,
            secret_key=secret_key,
            project_id=project_id,
            project_name=project_name,
        )

        # Benchmark state
        self.is_running: bool = False
        # Type annotations for time tracking (helps mypy)
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

        # Setup IDs - Resource IDs are optional until created
        self.lan_id: str = lan_id
        self.gateway_id: Optional[str] = None  # Auto-populated from camera creation response
        self.pipeline_id: Optional[str] = None
        self.camera_ids: List[str] = []  # Explicit type for mypy
        self.application_id: Optional[str] = None

        # Metrics storage
        self.metrics_timeline: List[Dict[str, Any]] = []
        self.experiment_id: str = str(uuid.uuid4())
        self.experiment_start_time: Optional[datetime] = None
        self.camera_addition_history: List[Dict[str, Any]] = []  # Track when cameras were added
        self._log_file_initialized: bool = False  # Track if log file header has been written

        # Threading
        self._benchmark_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.RLock()

        # State persistence
        self._last_state_save_time: Optional[datetime] = None
        self._state_save_interval_seconds: int = 60  # Save state every minute

        # Try to load state if auto_resume is enabled
        if self.auto_resume and os.path.exists(self.state_file):
            try:
                self.logger.info(f"Found existing state file: {self.state_file}")
                self.logger.info("Attempting to resume from saved state...")
                self.load_state()
            except Exception as e:
                self.logger.warning(f"Failed to load state from {self.state_file}: {str(e)}")
                self.logger.info("Starting with fresh state")

    def initialize_setup(self) -> Dict[str, Any]:
        """
        Initialize the streaming infrastructure with one camera.

        Creates initial cameras and pipeline. Cameras are assigned to a LAN
        and cluster; the backend auto-assigns the streaming gateway.

        Returns
        -------
        dict
            Setup results with all created resource IDs

        Raises
        ------
        Exception
            If setup fails at any step
        """
        self.logger.info("=" * 60)
        self.logger.info("INITIALIZING BENCHMARKING SETUP")
        self.logger.info("=" * 60)

        try:
            # Generate unique names
            unique_id = str(uuid.uuid4())[:8]
            # Sanitize names for use in pipeline/camera names (remove spaces, special chars)
            sanitized_app_name = self.app_name.replace(" ", "-").replace("_", "-").lower()
            sanitized_compute_alias = self.compute_alias.replace(" ", "-").replace("_", "-").lower()
            sanitized_cluster_name = self.cluster_name.replace(" ", "-").replace("_", "-").lower()

            pipeline_name = f"benchmark-pipeline-{sanitized_compute_alias}-{sanitized_cluster_name}-{sanitized_app_name}-{self.max_cameras}-{unique_id}"
            self.logger.info(f"Generated unique benchmark ID: {unique_id}")

            # Get application ID
            self.logger.info(f"[1/4] Finding application: {self.app_name}")
            try:
                app, error = self.automation.find_application_by_name(self.app_name)
                if error:
                    raise Exception(f"Failed to find application '{self.app_name}': {error}")
                # Ensure app is not None before accessing
                if not app:
                    raise Exception(f"Application '{self.app_name}' not found")
                self.application_id = app.get("_id")
                if not self.application_id:
                    raise Exception(f"Application found but no ID returned: {app}")
                self.logger.info(f"Found application ID: {self.application_id}")
            except Exception as e:
                self.logger.error(f"Failed to find application '{self.app_name}': {str(e)}", exc_info=True)
                raise

            # Create initial cameras (min_cameras) in batches
            self.logger.info(
                f"[2/4] Creating {self.min_cameras} initial camera(s) with video: {Path(self.video_path).name}"
            )
            try:
                # Get video path once (handles upload and caching)
                video_path_to_use = self._get_video_path_for_cameras()

                # Create cameras in batches
                initial_camera_ids: List[str] = []
                camera_number = 1

                while camera_number <= self.min_cameras:
                    # Determine batch size for this iteration
                    batch_size = min(self.camera_batch_size, self.min_cameras - camera_number + 1)

                    # Build camera payloads for this batch
                    camera_payloads = []
                    for i in range(batch_size):
                        camera_payload = self._build_camera_payload(
                            camera_number=camera_number, video_path_to_use=video_path_to_use
                        )
                        camera_payloads.append(camera_payload)
                        camera_number += 1

                    # Create cameras in this batch
                    self.logger.info(
                        f"[Batch Creation] Creating batch of {len(camera_payloads)} camera(s) ({len(initial_camera_ids) + len(camera_payloads)}/{self.min_cameras} total)..."
                    )
                    created_cameras, error = self.automation.create_cameras(camera_payloads)

                    if error:
                        raise Exception(f"Batch camera creation returned error: {error}")

                    if not created_cameras:
                        raise Exception("Camera creation succeeded but no cameras returned")

                    # Extract camera IDs and auto-assigned gateway ID from this batch
                    for cam in created_cameras:
                        camera_id = cam.get("_id") or cam.get("id")
                        if camera_id:
                            initial_camera_ids.append(camera_id)
                            self.camera_ids.append(camera_id)
                            self.logger.info(f"Created camera: {camera_id}")
                        # Capture auto-assigned gateway ID from first camera
                        if not self.gateway_id and cam.get("streamingGatewayId"):
                            self.gateway_id = cam["streamingGatewayId"]
                            self.logger.info(f"Auto-assigned gateway: {self.gateway_id}")

                if len(initial_camera_ids) != self.min_cameras:
                    self.logger.warning(f"Expected {self.min_cameras} cameras but got {len(initial_camera_ids)}")

            except Exception as e:
                self.logger.error(f"Failed to create initial cameras: {str(e)}", exc_info=True)
                raise

            # Create pipeline with initial cameras in batches
            self.logger.info(f"[3/4] Creating inference pipeline: {pipeline_name}")
            try:
                # Add cameras to pipeline in batches
                if initial_camera_ids:
                    # Create pipeline with first batch
                    first_batch_size = min(self.pipeline_batch_size, len(initial_camera_ids))
                    pipeline_cameras = [
                        {"cameraId": cam_id, "applications": [{"_idApplication": self.application_id}]}
                        for cam_id in initial_camera_ids[:first_batch_size]
                    ]

                    # Safely get project_id from session; raise if missing
                    project_id_value: Optional[str] = cast(
                        Optional[str], getattr(self.automation.session, "project_id", None)
                    )
                    if not project_id_value:
                        raise Exception("Session missing project_id")
                    self.pipeline_id, error = self.automation.create_inference_pipeline(
                        name=pipeline_name,
                        project_id=project_id_value,
                        cameras=pipeline_cameras,
                        description=f"Benchmarking pipeline {unique_id}",
                        facial_recognition_server_id=self.facial_recognition_server_id,
                        lpr_server_id=self.lpr_server_id,
                        cluster_name=self.cluster_name,
                        runtime_framework=self.runtime_framework,
                    )
                    if error:
                        raise Exception(f"API returned error: {error}")
                    if not self.pipeline_id:
                        raise Exception("Pipeline creation succeeded but no ID returned")
                    self.logger.info(f"Created pipeline: {self.pipeline_id} with {len(pipeline_cameras)} camera(s)")

                    # Add remaining cameras in batches
                    remaining_cameras = initial_camera_ids[first_batch_size:]
                    if remaining_cameras:
                        for i in range(0, len(remaining_cameras), self.pipeline_batch_size):
                            batch = remaining_cameras[i : i + self.pipeline_batch_size]
                            batch_payload = [
                                {"cameraId": cam_id, "applications": [{"_idApplication": self.application_id}]}
                                for cam_id in batch
                            ]
                            self.logger.info(f"Adding batch of {len(batch_payload)} camera(s) to pipeline...")
                            result, error = self.automation.add_cameras_and_applications_to_pipeline(
                                pipeline_id=self.pipeline_id, cameras=batch_payload, compute_alias=self.compute_alias
                            )
                            if error:
                                self.logger.warning(f"Failed to add batch to pipeline: {error}")
                            else:
                                self.logger.info(f"Added {len(batch_payload)} camera(s) to pipeline")
                else:
                    # Create empty pipeline if no cameras
                    # Safely get project_id from session; raise if missing
                    project_id_value = cast(Optional[str], getattr(self.automation.session, "project_id", None))
                    if not project_id_value:
                        raise Exception("Session missing project_id")
                    self.pipeline_id, error = self.automation.create_inference_pipeline(
                        name=pipeline_name,
                        project_id=project_id_value,
                        cameras=[],
                        description=f"Benchmarking pipeline {unique_id}",
                        facial_recognition_server_id=self.facial_recognition_server_id,
                        lpr_server_id=self.lpr_server_id,
                        cluster_name=self.cluster_name,
                        runtime_framework=self.runtime_framework,
                    )
                    if error:
                        raise Exception(f"API returned error: {error}")
                    if not self.pipeline_id:
                        raise Exception("Pipeline creation succeeded but no ID returned")
                    self.logger.info(f"Created empty pipeline: {self.pipeline_id}")
            except Exception as e:
                self.logger.error(f"Failed to create pipeline: {str(e)}", exc_info=True)
                raise

            # Start pipeline (if auto_start is enabled)
            if self.auto_start:
                self.logger.info("[4/4] Starting inference pipeline...")
                try:
                    # Assert pipeline_id is set before use (helps mypy)
                    assert self.pipeline_id is not None, "pipeline_id not set"
                    success, error = self.automation.start_inference_pipeline(
                        self.pipeline_id,
                        self.compute_alias,
                        cluster_name=self.cluster_name,
                    )
                    if error:
                        self.logger.warning(f"Failed to start pipeline: {error}")
                    else:
                        self.logger.info("Pipeline started")
                except Exception as e:
                    self.logger.warning(f"Exception while starting pipeline: {str(e)}", exc_info=True)
            else:
                self.logger.info("[4/4] Skipping pipeline start (auto_start=False)")

            self.logger.info("\n" + "=" * 60)
            self.logger.info("SETUP COMPLETE - Ready to start benchmarking")
            self.logger.info("=" * 60)

            return {
                "pipeline_id": self.pipeline_id,
                "initial_camera_ids": initial_camera_ids,
                "application_id": self.application_id,
                "total_initial_cameras": len(initial_camera_ids),
                "lan_id": self.lan_id,
                "cluster_name": self.cluster_name,
            }
        except Exception as e:
            self.logger.error(f"Setup initialization failed: {str(e)}", exc_info=True)
            raise

    def _get_video_path_for_cameras(self) -> str:
        """
        Get the video path to use for cameras (handles upload and caching).

        Returns
        -------
        str
            Video path (S3 URL or original URL/path)
        """
        # Check if it's a URL (starts with http:// or https://)
        if self.video_path.startswith(("http://", "https://")):
            # Already a URL, use it directly
            self.logger.debug(f"Using video URL: {self.video_path}")
            return self.video_path
        elif Path(self.video_path).exists():
            # Local file path - upload if needed (will use cache if already uploaded)
            abs_path = str(Path(self.video_path).resolve())

            # Check if already cached
            if abs_path in self.automation._video_upload_cache:
                cached_url = self.automation._video_upload_cache[abs_path]
                self.logger.debug(f"Using cached S3 URL for video: {abs_path}")
                return cached_url
            else:
                # Upload the video (upload_video will cache it)
                self.logger.info(f"Uploading video file: {Path(self.video_path).name}")
                file_name = f"benchmark-video-{str(uuid.uuid4())[:8]}.mp4"
                s3_url, error = self.automation.upload_video(self.video_path, file_name)
                if error or not s3_url:
                    raise Exception(f"Failed to upload video: {error or 'empty URL returned'}")
                self.logger.info(f"Video uploaded to S3: {s3_url}")
                return s3_url
        else:
            # File doesn't exist and it's not a URL - treat as URL anyway
            # (might be a URL that doesn't start with http/https, or a remote path)
            self.logger.warning(f"Video path not found locally, treating as URL: {self.video_path}")
            return self.video_path

    def _build_camera_payload(self, camera_number: int, video_path_to_use: str) -> Dict[str, Any]:
        """
        Build a camera payload dictionary for batch creation.

        Parameters
        ----------
        camera_number : int
            Sequential camera number
        video_path_to_use : str
            Video path (S3 URL or original URL/path) to use

        Returns
        -------
        dict
            Camera payload dictionary
        """
        # Generate unique ID for this camera
        unique_camera_id = str(uuid.uuid4())[:8]
        # Sanitize names for use in camera names (remove spaces, special chars)
        sanitized_app_name = self.app_name.replace(" ", "-").replace("_", "-").lower()
        sanitized_compute_alias = self.compute_alias.replace(" ", "-").replace("_", "-").lower()
        sanitized_cluster_name = self.cluster_name.replace(" ", "-").replace("_", "-").lower()
        camera_name = f"benchmark-camera-{sanitized_compute_alias}-{sanitized_cluster_name}-{sanitized_app_name}-{self.max_cameras}-{camera_number}-{unique_camera_id}"
        return {
            "accountNumber": self.automation.account_number,
            "lanId": self.lan_id,
            "clusterName": self.cluster_name,
            "cameraName": camera_name,
            "protocolType": "FILE",
            "simulationVideoPath": video_path_to_use,
            "customStreamSettings": {
                "width": self.width,
                "height": self.height,
                "streamingFPS": self.fps,
                "aspectRatio": self.aspect_ratio,
                "videoQuality": self.video_quality,
            },
        }

    def _create_camera_internal(self, camera_number: int) -> tuple:
        """
        Internal method to create a single camera (kept for backward compatibility).
        For batch operations, use add_cameras() instead.

        Parameters
        ----------
        camera_number : int
            Sequential camera number

        Returns
        -------
        tuple
            (camera_id, error_message)
        """
        try:
            video_path_to_use = self._get_video_path_for_cameras()
            camera_payload = self._build_camera_payload(camera_number, video_path_to_use)

            created_cameras, error = self.automation.create_cameras([camera_payload])
            if error:
                return None, error

            if not created_cameras:
                return None, "No camera created"

            camera_id = created_cameras[0].get("_id") or created_cameras[0].get("id")
            return camera_id, None
        except Exception as e:
            return None, str(e)

    def get_camera_output_topics(self, camera_id: str) -> List[Dict[str, Any]]:
        """
        Get output topics for a camera.

        Parameters
        ----------
        camera_id : str
            Camera ID

        Returns
        -------
        list
            List of camera output topics. Returns empty list on error.
        """
        try:
            endpoint = f"/v1/inference/get_camera_output_topics_by_camera_id/{camera_id}"
            response = self.automation.session.rpc.get(endpoint, timeout=300)

            if not response.get("success"):
                self.logger.warning(f"Failed to get camera output topics: {response.get('message', 'Unknown error')}")
                return []

            data = response.get("data", [])
            if not isinstance(data, list):
                return []
            return data
        except Exception as e:
            self.logger.warning(f"Exception fetching camera output topics: {str(e)}")
            return []

    def get_camera_input_topic(self, camera_id: str) -> Dict[str, Any]:
        """
        Get input topic for a camera.

        Parameters
        ----------
        camera_id : str
            Camera ID

        Returns
        -------
        dict
            Camera input topic information
        """
        try:
            endpoint = f"/v1/inference/get_camera_input_topic_by_camera_id/{camera_id}"
            response = self.automation.session.rpc.get(endpoint, timeout=300)

            if not response.get("success"):
                return {"error": f"API error: {response.get('message', 'Unknown error')}"}

            return response.get("data", {})
        except Exception as e:
            return {"error": f"Exception fetching camera input topic: {str(e)}"}

    def get_topics_by_streaming_gateway(self, streaming_id: str, server_id: str) -> Dict[str, Any]:
        """
        Get topics by streaming gateway and server ID.

        Parameters
        ----------
        streaming_id : str
            Streaming gateway ID
        server_id : str
            Server ID

        Returns
        -------
        dict
            Topics information
        """
        try:
            endpoint = f"/v1/inference/get_topics_by_streaming_id_and_server_id/{streaming_id}/{server_id}"
            response = self.automation.session.rpc.get(endpoint, timeout=300)

            if not response.get("success"):
                return {"error": f"API error: {response.get('message', 'Unknown error')}"}

            return response.get("data", {})
        except Exception as e:
            return {"error": f"Exception fetching topics by streaming gateway: {str(e)}"}

    def add_camera(self) -> Optional[str]:
        """
        Add one more camera to the existing pipeline.

        Creates a new camera with the same video and adds it to the pipeline
        with the same application using the proper API.

        Returns
        -------
        str or None
            Camera ID if successful, None if failed

        Raises
        ------
        Exception
            If pipeline not initialized or camera creation fails
        """
        if not self.pipeline_id:
            raise Exception("Pipeline not initialized. Call initialize_setup() first.")

        with self._lock:
            camera_number = len(self.camera_ids) + 1

            if camera_number > self.max_cameras:
                print(f"\nMaximum camera limit ({self.max_cameras}) reached. Stopping camera addition.")
                return None

            print(f"\n{'=' * 60}")
            print(f"ADDING CAMERA #{camera_number}")
            print(f"{'=' * 60}")

            # Create camera
            print(f"[1/3] Creating camera #{camera_number}...")
            new_camera_id, error = self._create_camera_internal(camera_number)
            if error:
                print(f"Failed to create camera: {error}")
                return None
            print(f"Created camera: {new_camera_id}")

            # Add camera to pipeline using the proper API
            print("[2/3] Adding camera to pipeline...")
            cameras_payload = [{"cameraId": new_camera_id, "applications": [{"_idApplication": self.application_id}]}]

            result, error = self.automation.add_cameras_and_applications_to_pipeline(
                pipeline_id=self.pipeline_id, cameras=cameras_payload, compute_alias=self.compute_alias
            )

            if error:
                print(f"Failed to add camera to pipeline: {error}")
                return None
            print("Camera added to pipeline")

            # Store camera ID
            self.camera_ids.append(new_camera_id)

            # Track camera addition in history
            addition_record = {
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "cameras_added": 1,
                "camera_ids": [new_camera_id],
                "total_cameras": len(self.camera_ids),
            }

            with self._lock:
                self.camera_addition_history.append(addition_record)

            # Append camera addition as log entry
            self._append_log_entry("camera_addition", addition_record)

            print(f"Total cameras: {len(self.camera_ids)}")
            print(f"{'=' * 60}\n")

            return new_camera_id

    def add_cameras(self) -> List[str]:
        """
        Add multiple cameras to the existing pipeline based on step_size.

        Creates new cameras with the same video and adds them to the pipeline
        with the same application using the proper API.

        Returns
        -------
        list of str
            List of camera IDs successfully added. Empty list if failed or max reached.

        Raises
        ------
        Exception
            If pipeline not initialized
        """
        if not self.pipeline_id:
            error_msg = "Pipeline not initialized. Call initialize_setup() first."
            self.logger.error(error_msg)
            raise Exception(error_msg)

        try:
            with self._lock:
                current_count = len(self.camera_ids)

                # Calculate how many cameras we can add
                remaining_slots = self.max_cameras - current_count
                if remaining_slots <= 0:
                    self.logger.warning(f"Maximum camera limit ({self.max_cameras}) reached. Stopping camera addition.")
                    return []

                cameras_to_add = min(self.step_size, remaining_slots)

                self.logger.info("=" * 60)
                self.logger.info(f"ADDING {cameras_to_add} CAMERA(S) (Step size: {self.step_size})")
                self.logger.info("=" * 60)

                # Get video path once (handles upload and caching)
                try:
                    video_path_to_use = self._get_video_path_for_cameras()
                except Exception as e:
                    self.logger.error(f"Failed to prepare video path: {str(e)}", exc_info=True)
                    return []

                # Create cameras in batches
                created_camera_ids: List[str] = []
                camera_number = current_count + 1

                while camera_number <= current_count + cameras_to_add:
                    # Determine batch size for this iteration
                    batch_size = min(self.camera_batch_size, (current_count + cameras_to_add) - camera_number + 1)

                    # Build camera payloads for this batch
                    camera_payloads = []
                    for i in range(batch_size):
                        camera_payload = self._build_camera_payload(camera_number, video_path_to_use)
                        camera_payloads.append(camera_payload)
                        camera_number += 1

                    # Create cameras in this batch
                    self.logger.info(
                        f"[Batch Creation] Creating batch of {len(camera_payloads)} camera(s) ({len(created_camera_ids) + len(camera_payloads)}/{cameras_to_add} total)..."
                    )
                    created_cameras, error = self.automation.create_cameras(camera_payloads)

                    if error:
                        self.logger.error(f"Failed to create cameras in batch: {error}")
                        return []

                    if not created_cameras:
                        self.logger.error("No cameras were created in this batch")
                        return []

                    # Extract camera IDs from this batch
                    batch_camera_ids = []
                    for cam in created_cameras:
                        camera_id = cam.get("_id") or cam.get("id")
                        if camera_id:
                            batch_camera_ids.append(camera_id)
                            created_camera_ids.append(camera_id)
                            self.logger.info(f"Created camera: {camera_id}")

                    if not batch_camera_ids:
                        self.logger.error("No valid camera IDs returned from batch creation")
                        return []

                if not created_camera_ids:
                    self.logger.error("No cameras were created")
                    return []

                # Add cameras to pipeline in batches
                try:
                    for i in range(0, len(created_camera_ids), self.pipeline_batch_size):
                        batch = created_camera_ids[i : i + self.pipeline_batch_size]
                        cameras_payload = [
                            {"cameraId": cam_id, "applications": [{"_idApplication": self.application_id}]}
                            for cam_id in batch
                        ]

                        self.logger.info(
                            f"[Adding to pipeline] Adding batch of {len(cameras_payload)} camera(s) to pipeline ({i + len(cameras_payload)}/{len(created_camera_ids)} total)..."
                        )
                        result, error = self.automation.add_cameras_and_applications_to_pipeline(
                            pipeline_id=self.pipeline_id, cameras=cameras_payload, compute_alias=self.compute_alias
                        )

                        if error:
                            raise Exception(f"API returned error: {error}")
                        self.logger.info(f"Added {len(cameras_payload)} camera(s) to pipeline")

                    self.logger.info(f"All {len(created_camera_ids)} cameras added to pipeline")
                except Exception as e:
                    self.logger.error(f"Failed to add cameras to pipeline: {str(e)}", exc_info=True)
                    # Clean up created cameras if pipeline addition fails
                    self.logger.warning("Note: Cameras were created but not added to pipeline")
                    return []

                # Store all camera IDs
                self.camera_ids.extend(created_camera_ids)

                # Track camera addition in history
                addition_record = {
                    "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                    "cameras_added": len(created_camera_ids),
                    "camera_ids": created_camera_ids,
                    "total_cameras": len(self.camera_ids),
                }

                with self._lock:
                    self.camera_addition_history.append(addition_record)

                # Append camera addition as log entry
                self._append_log_entry("camera_addition", addition_record)

                self.logger.info(
                    f"Total cameras: {len(self.camera_ids)} (Added {len(created_camera_ids)} in this step)"
                )
                self.logger.info("=" * 60)

                # Save state after camera addition
                try:
                    self.save_state()
                except Exception as e:
                    self.logger.warning(f"Failed to save state after camera addition: {str(e)}")

                return created_camera_ids
        except Exception as e:
            self.logger.error(f"Unexpected error in add_cameras: {str(e)}", exc_info=True)
            raise

    def collect_metrics(self) -> Dict[str, Any]:
        """
        Collect current metrics from gateway and pipeline.

        Returns
        -------
        dict
            Current metrics snapshot
        """
        try:
            timestamp = datetime.now(timezone.utc).isoformat() + "Z"
            camera_count = len(self.camera_ids)

            # Collect real metrics from APIs with error handling
            try:
                gateway_metrics = self._get_real_gateway_metrics()
            except Exception as e:
                self.logger.warning(f"Failed to collect gateway metrics: {str(e)}")
                gateway_metrics = {"error": f"Exception: {str(e)}"}

            try:
                pipeline_metrics = self._get_real_pipeline_metrics()
            except Exception as e:
                self.logger.warning(f"Failed to collect pipeline metrics: {str(e)}")
                pipeline_metrics = {"error": f"Exception: {str(e)}"}

            metrics_entry = {
                "timestamp": timestamp,
                "camera_count": camera_count,
                "gateway_metrics": gateway_metrics,
                "pipeline_metrics": pipeline_metrics,
            }

            with self._lock:
                self.metrics_timeline.append(metrics_entry)

            # Append metrics as log entry
            self._append_log_entry("metric_collection", metrics_entry)

            # Save state after metrics collection (less frequently, every 5th collection)
            if len(self.metrics_timeline) % 5 == 0:
                try:
                    self.save_state()
                except Exception as e:
                    self.logger.warning(f"Failed to save state after metrics collection: {str(e)}")

            return metrics_entry
        except Exception as e:
            self.logger.error(f"Unexpected error in collect_metrics: {str(e)}", exc_info=True)
            # Return a minimal metrics entry even on error
            return {
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "camera_count": len(self.camera_ids),
                "gateway_metrics": {"error": f"Collection failed: {str(e)}"},
                "pipeline_metrics": {"error": f"Collection failed: {str(e)}"},
            }

    def _get_real_gateway_metrics(self) -> Dict[str, Any]:
        """
        Fetch real streaming gateway metrics from API.

        Returns
        -------
        dict
            Gateway metrics including camera readings and gateway sending stats
        """
        try:
            # Call streaming gateway metrics API
            endpoint = f"/v1/monitoring/streaming_gateway_metrics/{self.gateway_id}/latest?limit=1"
            response = self.automation.session.rpc.get(endpoint, timeout=300)

            if not response.get("success"):
                return {"error": f"API error: {response.get('message', 'Unknown error')}"}

            data = response.get("data", [])
            if not data:
                return {"error": "No metrics data available"}

            # Extract metrics from first data point
            metrics_data = data[0]
            # According to tt.py, the field is "per_camera_metrics", not "metrics"
            camera_metrics = metrics_data.get("per_camera_metrics", [])

            # Aggregate metrics across all cameras
            result = {
                "timestamp": metrics_data.get("timestamp"),
                "granularity": metrics_data.get("granularity"),
                "bucket_start": metrics_data.get("bucket_start"),
                "camera_count": len(camera_metrics),
                "cameras": [],
            }

            # Collect per-camera metrics
            for cam in camera_metrics:
                camera_reading = cam.get("camera_reading", {})
                gateway_sending = cam.get("gateway_sending", {})

                cam_data = {
                    "camera_id": cam.get("camera_id"),
                    "camera_reading": {
                        "throughput_fps": camera_reading.get("throughput", {}).get("avg", 0),
                        "latency_ms": camera_reading.get("latency", {}).get("avg", 0),
                    },
                    "gateway_sending": {
                        "throughput_fps": gateway_sending.get("throughput", {}).get("avg", 0),
                        "latency_ms": gateway_sending.get("latency", {}).get("avg", 0),
                    },
                }
                result["cameras"].append(cam_data)

            # Calculate aggregated stats
            if camera_metrics:
                avg_camera_throughput = sum(
                    cam.get("camera_reading", {}).get("throughput", {}).get("avg", 0) for cam in camera_metrics
                ) / len(camera_metrics)

                avg_camera_latency = sum(
                    cam.get("camera_reading", {}).get("latency", {}).get("avg", 0) for cam in camera_metrics
                ) / len(camera_metrics)

                avg_gateway_throughput = sum(
                    cam.get("gateway_sending", {}).get("throughput", {}).get("avg", 0) for cam in camera_metrics
                ) / len(camera_metrics)

                avg_gateway_latency = sum(
                    cam.get("gateway_sending", {}).get("latency", {}).get("avg", 0) for cam in camera_metrics
                ) / len(camera_metrics)

                result["aggregated"] = {
                    "avg_camera_throughput_fps": round(avg_camera_throughput, 2),
                    "avg_camera_latency_ms": round(avg_camera_latency, 2),
                    "avg_gateway_throughput_fps": round(avg_gateway_throughput, 2),
                    "avg_gateway_latency_ms": round(avg_gateway_latency, 2),
                }

            return result

        except Exception as e:
            return {"error": f"Exception fetching gateway metrics: {str(e)}"}

    def _get_real_pipeline_metrics(self) -> Dict[str, Any]:
        """
        Fetch real app deployment metrics from API.

        Returns
        -------
        dict
            Pipeline/application deployment metrics
        """
        try:
            # Check if we have any cameras
            if not self.camera_ids:
                return {"error": "No cameras available to fetch metrics"}

            # Get app deployment ID from camera output topics (following tt.py pattern)
            output_topics = self.get_camera_output_topics(self.camera_ids[0])

            if not output_topics:
                return {"error": "No output topics found for camera"}

            # Extract appDeploymentId from first output topic (like tt.py: data[0]["appDeploymentId"])
            app_deploy_id = output_topics[0].get("appDeploymentId")

            if not app_deploy_id:
                return {"error": "No app deployment ID found in output topics"}

            # Call app deployment metrics API
            metrics_endpoint = f"/v1/monitoring/app_deployment_metrics/{app_deploy_id}/latest?limit=1"
            response = self.automation.session.rpc.get(metrics_endpoint, timeout=300)

            if not response.get("success"):
                return {"error": f"API error: {response.get('message', 'Unknown error')}"}

            data = response.get("data", [])
            if not data:
                return {"error": "No metrics data available"}

            # Extract metrics from first data point
            metrics_data = data[0]

            result = {
                "timestamp": metrics_data.get("timestamp"),
                "granularity": metrics_data.get("granularity"),
                "bucket_start": metrics_data.get("bucket_start"),
                "consumer": {
                    "throughput_avg": metrics_data.get("consumer_throughput", {}).get("avg", -1),
                    "latency_avg_ms": metrics_data.get("consumer_latency", {}).get("avg", -1),
                },
                "inference": {
                    "throughput_avg": metrics_data.get("inference_throughput", {}).get("avg", 0),
                    "latency_avg_ms": metrics_data.get("inference_latency", {}).get("avg", -1),
                },
                "post_processing": {
                    "throughput_avg": metrics_data.get("post_processing_throughput", {}).get("avg", 0),
                    "latency_avg_ms": metrics_data.get("post_processing_latency", {}).get("avg", -1),
                },
                "producer": {
                    "throughput_avg": metrics_data.get("producer_throughput", {}).get("avg", 0),
                    "latency_avg_ms": metrics_data.get("producer_latency", {}).get("avg", -1),
                },
                "count": metrics_data.get("count", 0),
            }

            return result

        except Exception as e:
            return {"error": f"Exception fetching pipeline metrics: {str(e)}"}

    def _benchmark_loop(self, duration_minutes: Optional[float] = None):
        """
        Internal benchmark loop that runs in a separate thread.

        Parameters
        ----------
        duration_minutes : float, optional
            Maximum duration to run. If None, runs indefinitely.
        """
        try:
            # Calculate end_time based on original start_time if resuming
            end_time = None
            if duration_minutes:
                if self.start_time:
                    # Use original start_time to calculate end_time (for resuming)
                    end_time = self.start_time + timedelta(minutes=duration_minutes)
                else:
                    # Fresh start
                    end_time = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)

            # Separate intervals for cameras and metrics
            camera_interval_seconds = self.interval_minutes * 60
            metrics_interval_seconds = self.metrics_interval_minutes * 60

            # Calculate next camera addition time
            # If resuming, base it on last camera addition, otherwise start from now
            now = datetime.now(timezone.utc)
            if self.camera_addition_history:
                # Resume: calculate next time based on last addition
                last_addition = self.camera_addition_history[-1]
                last_addition_time = datetime.fromisoformat(
                    last_addition.get("timestamp", now.isoformat()).replace("Z", "+00:00")
                ).replace(tzinfo=None)
                # Next addition should be at last_addition_time + interval
                next_camera_time = last_addition_time + timedelta(seconds=camera_interval_seconds)
                # If that time has already passed, schedule for immediate addition
                if next_camera_time < now:
                    next_camera_time = now + timedelta(seconds=min(camera_interval_seconds, 30))
            else:
                # Fresh start: schedule first addition after interval
                next_camera_time = now + timedelta(seconds=camera_interval_seconds)

            # Calculate next metrics collection time
            # If resuming, base it on last metrics collection, otherwise start from now
            if self.metrics_timeline:
                # Resume: calculate next time based on last metrics collection
                last_metrics = self.metrics_timeline[-1]
                last_metrics_time = datetime.fromisoformat(
                    last_metrics.get("timestamp", now.isoformat()).replace("Z", "+00:00")
                ).replace(tzinfo=None)
                # Next collection should be at last_metrics_time + interval
                next_metrics_time = last_metrics_time + timedelta(seconds=metrics_interval_seconds)
                # If that time has already passed, schedule for immediate collection
                if next_metrics_time < now:
                    next_metrics_time = now + timedelta(seconds=min(metrics_interval_seconds, 10))
            else:
                # Fresh start: schedule first collection after interval
                next_metrics_time = now + timedelta(seconds=metrics_interval_seconds)

            self.logger.info("=" * 60)
            if self.camera_addition_history or self.metrics_timeline:
                self.logger.info("BENCHMARK RESUMED")
                self.logger.info(f"  Resuming from {len(self.camera_addition_history)} camera addition(s)")
                self.logger.info(f"  Resuming from {len(self.metrics_timeline)} metric collection(s)")
            else:
                self.logger.info("BENCHMARK STARTED")
            self.logger.info("=" * 60)
            self.logger.info("Configuration:")
            self.logger.info(f"  Starting cameras: {len(self.camera_ids)}")
            self.logger.info(f"  Min cameras: {self.min_cameras}")
            self.logger.info(f"  Max cameras: {self.max_cameras}")
            self.logger.info(f"  Step size: {self.step_size} camera(s) per interval")
            self.logger.info(f"  Camera addition interval: {self.interval_minutes} minutes")
            self.logger.info(f"  Metrics collection interval: {self.metrics_interval_minutes} minutes")
            self.logger.info(f"  Duration: {duration_minutes if duration_minutes else 'Unlimited'} minutes")
            if end_time:
                remaining_minutes = (end_time - now).total_seconds() / 60
                self.logger.info(f"  Remaining duration: {remaining_minutes:.1f} minutes")
            self.logger.info(f"  Output file: {self.output_file}")
            self.logger.info("=" * 60)

            # Collect initial metrics
            try:
                self.logger.info("Collecting initial metrics...")
                initial_metrics = self.collect_metrics()
                self.logger.info(f"Initial metrics collected: {initial_metrics.get('camera_count', 0)} cameras")
            except Exception as e:
                self.logger.warning(f"Failed to collect initial metrics: {str(e)}", exc_info=True)

            consecutive_errors = 0
            max_consecutive_errors = 5

            while not self._stop_event.is_set():
                try:
                    now = datetime.now(timezone.utc)

                    # Periodic state saving
                    if (
                        self._last_state_save_time is None
                        or (now - self._last_state_save_time).total_seconds() >= self._state_save_interval_seconds
                    ):
                        try:
                            self.save_state()
                            self.logger.debug("State saved periodically")
                        except Exception as e:
                            self.logger.warning(f"Failed to save state periodically: {str(e)}")

                    # Check duration limit
                    if end_time and now >= end_time:
                        self.logger.info("Duration limit reached. Stopping benchmark...")
                        break

                    # Check if time to add cameras
                    should_stop_cameras = False
                    if now >= next_camera_time:
                        try:
                            self.logger.info(f"Time to add cameras (interval: {self.interval_minutes} min)")
                            new_camera_ids = self.add_cameras()
                            if not new_camera_ids:
                                # Max cameras reached or failed
                                self.logger.info("No more cameras to add. Stopping benchmark...")
                                should_stop_cameras = True
                            else:
                                consecutive_errors = 0  # Reset error counter on success
                                self.logger.info(f"Next camera addition scheduled in {self.interval_minutes} minutes")
                        except Exception as e:
                            consecutive_errors += 1
                            self.logger.error(
                                f"Error adding cameras (attempt {consecutive_errors}/{max_consecutive_errors}): {str(e)}",
                                exc_info=True,
                            )
                            if consecutive_errors >= max_consecutive_errors:
                                self.logger.error(
                                    f"Too many consecutive errors ({consecutive_errors}). Stopping benchmark."
                                )
                                should_stop_cameras = True
                        # Always schedule next camera addition at the configured interval
                        next_camera_time = now + timedelta(seconds=camera_interval_seconds)
                    if should_stop_cameras:
                        break

                    # Check if time to collect metrics
                    should_stop_metrics = False
                    if now >= next_metrics_time:
                        try:
                            self.logger.debug(f"Collecting metrics (interval: {self.metrics_interval_minutes} min)")
                            metrics = self.collect_metrics()

                            # Display metrics summary
                            gw = metrics.get("gateway_metrics", {})
                            pl = metrics.get("pipeline_metrics", {})
                            camera_count = metrics.get("camera_count", 0)

                            if "aggregated" in gw:
                                # Real metrics available
                                agg = gw["aggregated"]
                                inf = pl.get("inference", {})
                                self.logger.info(
                                    f"Metrics: Cameras={camera_count}, "
                                    f"Camera FPS={agg.get('avg_camera_throughput_fps', 0):.1f}, "
                                    f"Gateway FPS={agg.get('avg_gateway_throughput_fps', 0):.1f}, "
                                    f"Inference Throughput={inf.get('throughput_avg', 0):.2f}"
                                )
                            elif "error" in gw or "error" in pl:
                                # Error case
                                gw_error = gw.get("error", "N/A")
                                pl_error = pl.get("error", "N/A")
                                self.logger.warning(
                                    f"Metrics (with errors): Cameras={camera_count}, "
                                    f"GW Error={gw_error}, PL Error={pl_error}"
                                )
                            else:
                                self.logger.info(f"Metrics collected: Cameras={camera_count}")

                            consecutive_errors = 0  # Reset error counter on success
                        except Exception as e:
                            consecutive_errors += 1
                            self.logger.error(
                                f"Error collecting metrics (attempt {consecutive_errors}/{max_consecutive_errors}): {str(e)}",
                                exc_info=True,
                            )
                            if consecutive_errors >= max_consecutive_errors:
                                self.logger.error(
                                    f"Too many consecutive errors ({consecutive_errors}). Stopping benchmark."
                                )
                                should_stop_metrics = True
                        # Always schedule next metrics collection at the configured interval
                        next_metrics_time = now + timedelta(seconds=metrics_interval_seconds)
                    if should_stop_metrics:
                        break

                    # Sleep briefly to avoid busy waiting
                    time.sleep(1)

                except KeyboardInterrupt:
                    self.logger.warning("Keyboard interrupt received in benchmark loop")
                    raise
                except Exception as e:
                    self.logger.error(f"Unexpected error in benchmark loop: {str(e)}", exc_info=True)
                    consecutive_errors += 1
                    if consecutive_errors >= max_consecutive_errors:
                        self.logger.error(f"Too many consecutive errors ({consecutive_errors}). Stopping benchmark.")
                        break
                    time.sleep(5)  # Wait before retrying

        except KeyboardInterrupt:
            self.logger.warning("Benchmark loop interrupted by user")
            raise
        except Exception as e:
            self.logger.error(f"Fatal error in benchmark loop: {str(e)}", exc_info=True)
            raise
        finally:
            # Save state before exiting (even on crash)
            try:
                self.save_state()
                self.logger.info("State saved before benchmark loop exit")
            except Exception as e:
                self.logger.warning(f"Failed to save state in finally block: {str(e)}")
            self.logger.info("Benchmark loop ended")

    def start_benchmark(self, duration_minutes: Optional[float] = None, resume: Optional[bool] = None):
        """
        Start the benchmarking process.

        Begins adding cameras at specified intervals and collecting metrics.
        Runs in a background thread.

        Parameters
        ----------
        duration_minutes : float, optional
            Maximum duration to run. If None, runs until stop_benchmark() is called.
        resume : bool, optional
            Force resume from state if True, force new start if False.
            If None, uses auto_resume setting from __init__.

        Raises
        ------
        Exception
            If benchmark already running or setup not initialized
        """
        if self.is_running:
            error_msg = "Benchmark already running"
            self.logger.error(error_msg)
            raise Exception(error_msg)

        # Check if we should resume from state
        should_resume = resume if resume is not None else self.auto_resume
        if should_resume and os.path.exists(self.state_file):
            try:
                self.logger.info("Resuming from saved state...")
                resume_result = self.resume_from_state()
                self.logger.info(
                    "Resume successful: status=%s cameras=%s metrics=%s",
                    resume_result.get("status"),
                    resume_result.get("cameras_restored"),
                    resume_result.get("metrics_restored"),
                )
                # Reset is_running flag since we're restarting
                self.is_running = False
                # If resuming, preserve existing start_time and experiment_start_time
                # They should already be loaded from state
            except Exception as e:
                self.logger.warning(f"Failed to resume from state: {str(e)}")
                self.logger.info("Starting fresh benchmark instead...")
                # Reset to fresh start
                self.start_time = datetime.now(timezone.utc)
                self.experiment_start_time = self.start_time

        if not self.pipeline_id:
            error_msg = "Setup not initialized. Call initialize_setup() first."
            self.logger.error(error_msg)
            raise Exception(error_msg)

        try:
            self.is_running = True
            if not self.start_time:
                self.start_time = datetime.now(timezone.utc)
            if not self.experiment_start_time:
                self.experiment_start_time = self.start_time
            self._stop_event.clear()

            # Initialize log file with header
            self._initialize_log_file()

            # Log experiment start (only if not resuming)
            if not (should_resume and os.path.exists(self.state_file)):
                self._append_log_entry(
                    "experiment_start",
                    {
                        "start_time": self.start_time.isoformat() + "Z",
                        "duration_minutes": duration_minutes,
                    },
                )

            # Save initial state
            self.save_state()

            self.logger.info("Starting benchmark thread...")
            # Start benchmark thread
            self._benchmark_thread = threading.Thread(
                target=self._benchmark_loop, args=(duration_minutes,), daemon=True
            )
            self._benchmark_thread.start()
            self.logger.info("Benchmark thread started")

            try:
                # Wait for thread to complete
                self._benchmark_thread.join()
            except KeyboardInterrupt:
                self.logger.warning("Keyboard interrupt received...")
                self.stop_benchmark()
        except Exception as e:
            self.logger.error(f"Error starting benchmark: {str(e)}", exc_info=True)
            self.is_running = False
            raise

    def stop_benchmark(self):
        """
        Stop the benchmarking process gracefully.

        Signals the benchmark thread to stop and waits for completion.
        """
        if not self.is_running:
            self.logger.warning("Benchmark not running")
            return

        try:
            self.logger.info("=" * 60)
            self.logger.info("STOPPING BENCHMARK")
            self.logger.info("=" * 60)

            self._stop_event.set()

            # Wait for thread to finish
            if self._benchmark_thread and self._benchmark_thread.is_alive():
                self.logger.info("Waiting for benchmark thread to finish...")
                self._benchmark_thread.join(timeout=5)
                if self._benchmark_thread.is_alive():
                    self.logger.warning("Benchmark thread did not finish within timeout")

            self.is_running = False
            self.end_time = datetime.now(timezone.utc)

            duration_minutes = (self.end_time - self.start_time).total_seconds() / 60 if self.start_time else 0

            # Log experiment end
            self._append_log_entry(
                "experiment_end",
                {
                    "end_time": self.end_time.isoformat() + "Z",
                    "duration_minutes": round(duration_minutes, 2),
                    "total_cameras": len(self.camera_ids),
                    "metrics_collected": len(self.metrics_timeline),
                },
            )

            # Save final state
            try:
                self.save_state()
                self.logger.info("Final state saved")
            except Exception as e:
                self.logger.warning(f"Failed to save final state: {str(e)}")

            self.logger.info("Benchmark stopped")
            self.logger.info(f"  Total cameras: {len(self.camera_ids)}")
            self.logger.info(f"  Duration: {duration_minutes:.1f} minutes")
            self.logger.info(f"  Metrics collected: {len(self.metrics_timeline)} snapshots")
            self.logger.info(f"  Results saved to: {self.output_file}")
            self.logger.info(f"  State saved to: {self.state_file}")
            self.logger.info("=" * 60)
        except Exception as e:
            self.logger.error(f"Error stopping benchmark: {str(e)}", exc_info=True)
            self.is_running = False
            raise

    def _initialize_log_file(self):
        """
        Initialize the JSON log file with experiment header information.
        This is called once at the start of the benchmark.
        If resuming, preserves existing log entries.
        """
        try:
            if self._log_file_initialized:
                return

            # Check if log file already exists (from previous run)
            existing_logs = []
            if os.path.exists(self.output_file):
                try:
                    with open(self.output_file, "r") as f:
                        existing_data = json.load(f)
                        existing_logs = existing_data.get("logs", [])
                        self.logger.info(f"Found existing log file with {len(existing_logs)} entries. Preserving them.")
                except Exception as e:
                    self.logger.warning(f"Failed to read existing log file: {str(e)}")

            header = {
                "experiment_info": {
                    "experiment_id": self.experiment_id,
                    "experiment_start_time": (
                        self.experiment_start_time.isoformat() + "Z" if self.experiment_start_time else None
                    ),
                    "status": "running",
                },
                "benchmark_config": {
                    "video_path": self.video_path,
                    "video_settings": {
                        "streamingFPS": self.fps,
                        "width": self.width,
                        "height": self.height,
                        "video_quality": self.video_quality,
                        "aspect_ratio": self.aspect_ratio,
                    },
                    "compute_alias": self.compute_alias,
                    "app_name": self.app_name,
                    "min_cameras": self.min_cameras,
                    "max_cameras": self.max_cameras,
                    "interval_minutes": self.interval_minutes,
                    "step_size": self.step_size,
                    "metrics_interval_minutes": self.metrics_interval_minutes,
                    "camera_batch_size": self.camera_batch_size,
                    "pipeline_batch_size": self.pipeline_batch_size,
                    "auto_start": self.auto_start,
                    "facial_recognition_server_id": self.facial_recognition_server_id,
                    "lpr_server_id": self.lpr_server_id,
                    "cluster_name": self.cluster_name,
                    "runtime_framework": self.runtime_framework,
                },
                "setup_ids": {
                    "gateway_id": self.gateway_id,
                    "lan_id": self.lan_id,
                    "cluster_name": self.cluster_name,
                    "pipeline_id": self.pipeline_id,
                    "application_id": self.application_id,
                    "camera_ids": self.camera_ids,
                    "total_cameras": len(self.camera_ids),
                },
                "logs": existing_logs,  # Preserve existing logs when resuming
            }

            # Write initial file
            with open(self.output_file, "w") as f:
                json.dump(header, f, indent=2)

            self._log_file_initialized = True
            self.logger.info(f"Initialized log file: {self.output_file}")

        except Exception as e:
            self.logger.warning(f"Failed to initialize log file: {str(e)}")

    def _append_log_entry(self, event_type: str, event_data: Dict[str, Any]):
        """
        Append a new log entry to the JSON file.

        Parameters
        ----------
        event_type : str
            Type of event (e.g., 'metric_collection', 'camera_addition', 'experiment_end')
        event_data : dict
            Data for this event
        """
        try:
            # Read existing file
            if os.path.exists(self.output_file):
                with open(self.output_file, "r") as f:
                    data = json.load(f)
            else:
                # File doesn't exist, initialize it first
                self._initialize_log_file()
                with open(self.output_file, "r") as f:
                    data = json.load(f)

            # Create log entry
            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                "event_type": event_type,
                "event_data": event_data,
            }

            # Append to logs array
            if "logs" not in data:
                data["logs"] = []
            data["logs"].append(log_entry)

            # Update experiment info if needed
            if "experiment_info" in data:
                if event_type == "experiment_end":
                    data["experiment_info"]["status"] = "completed"
                    data["experiment_info"]["experiment_end_time"] = log_entry["timestamp"]
                    if self.experiment_start_time:
                        end_time = datetime.now(timezone.utc)
                        duration = (end_time - self.experiment_start_time).total_seconds() / 60
                        data["experiment_info"]["experiment_duration_minutes"] = round(duration, 2)

            # Update setup_ids if cameras were added
            if event_type == "camera_addition" and "setup_ids" in data:
                data["setup_ids"]["camera_ids"] = self.camera_ids
                data["setup_ids"]["total_cameras"] = len(self.camera_ids)

            # Write back atomically
            temp_file = self.output_file + ".tmp"
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=2)

            # Atomic rename
            if os.path.exists(self.output_file):
                os.replace(temp_file, self.output_file)
            else:
                os.rename(temp_file, self.output_file)

        except Exception as e:
            self.logger.warning(f"Failed to append log entry: {str(e)}")

    def _build_results_structure(self) -> Dict[str, Any]:
        """
        Build the complete results structure with all experiment information.

        Returns
        -------
        dict
            Complete results structure with all experiment info
        """
        # Calculate summary statistics
        summary = self._calculate_summary()

        # Build comprehensive experiment info
        experiment_info = {
            "experiment_id": self.experiment_id,
            "experiment_start_time": (
                self.experiment_start_time.isoformat() + "Z" if self.experiment_start_time else None
            ),
            "experiment_end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
            "experiment_duration_minutes": (
                round((self.end_time - self.experiment_start_time).total_seconds() / 60, 2)
                if self.experiment_start_time and self.end_time
                else None
            ),
            "status": "running" if self.is_running else ("completed" if self.end_time else "not_started"),
        }

        # Build results structure
        results = {
            "experiment_info": experiment_info,
            "benchmark_config": {
                "video_path": self.video_path,
                "video_settings": {
                    "streamingFPS": self.fps,
                    "width": self.width,
                    "height": self.height,
                    "video_quality": self.video_quality,
                    "aspect_ratio": self.aspect_ratio,
                },
                "compute_alias": self.compute_alias,
                "app_name": self.app_name,
                "min_cameras": self.min_cameras,
                "max_cameras": self.max_cameras,
                "interval_minutes": self.interval_minutes,
                "step_size": self.step_size,
                "metrics_interval_minutes": self.metrics_interval_minutes,
                "start_time": self.start_time.isoformat() + "Z" if self.start_time else None,
                "end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
                "facial_recognition_server_id": self.facial_recognition_server_id,
                "lpr_server_id": self.lpr_server_id,
                "cluster_name": self.cluster_name,
                "runtime_framework": self.runtime_framework,
            },
            "setup_ids": {
                "gateway_id": self.gateway_id,
                "lan_id": self.lan_id,
                "cluster_name": self.cluster_name,
                "pipeline_id": self.pipeline_id,
                "application_id": self.application_id,
                "camera_ids": self.camera_ids,
                "total_cameras": len(self.camera_ids),
            },
            "camera_addition_history": self.camera_addition_history,
            "metrics_timeline": self.metrics_timeline,
            "summary": summary,
        }

        return results

    def export_results(self, file_path: Optional[str] = None) -> str:
        """
        Export benchmark results to JSON file with summary.

        Reads the existing log file and adds a summary section.

        Parameters
        ----------
        file_path : str, optional
            Output file path. Uses default output_file if not specified.

        Returns
        -------
        str
            Path to exported file
        """
        if file_path is None:
            file_path = self.output_file

        # Read existing log file
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                results = json.load(f)
        else:
            # File doesn't exist, build from current state
            results = {"experiment_info": {}, "benchmark_config": {}, "setup_ids": {}, "logs": []}

        # Calculate and add summary
        summary = self._calculate_summary()
        results["summary"] = summary

        # Write back to file
        with open(file_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"{'=' * 60}")
        print("RESULTS EXPORTED")
        print(f"{'=' * 60}")
        print(f"File: {file_path}")
        if os.path.exists(file_path):
            print(f"Size: {Path(file_path).stat().st_size / 1024:.1f} KB")
            if "logs" in results:
                print(f"Total log entries: {len(results['logs'])}")
        print(f"{'=' * 60}\n")

        return file_path

    def _extract_camera_additions_from_logs(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract camera addition history from log entries.

        Parameters
        ----------
        logs : list
            List of log entries

        Returns
        -------
        list
            List of camera addition records
        """
        additions = []
        for log_entry in logs:
            if log_entry.get("event_type") == "camera_addition":
                additions.append(log_entry.get("event_data", {}))
        return additions

    def _extract_metrics_from_logs(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract metrics timeline from log entries.

        Parameters
        ----------
        logs : list
            List of log entries

        Returns
        -------
        list
            List of metrics entries
        """
        metrics = []
        for log_entry in logs:
            if log_entry.get("event_type") == "metric_collection":
                metrics.append(log_entry.get("event_data", {}))
        return metrics

    def save_state(self) -> bool:
        """
        Save current benchmark state to file for crash recovery.

        Returns
        -------
        bool
            True if state was saved successfully, False otherwise
        """
        try:
            state = {
                "version": "1.0",
                "saved_at": datetime.now(timezone.utc).isoformat() + "Z",
                "experiment_id": self.experiment_id,
                "experiment_start_time": (
                    self.experiment_start_time.isoformat() + "Z" if self.experiment_start_time else None
                ),
                "start_time": self.start_time.isoformat() + "Z" if self.start_time else None,
                "end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
                "is_running": self.is_running,
                "setup_ids": {
                    "gateway_id": self.gateway_id,
                    "lan_id": self.lan_id,
                    "cluster_name": self.cluster_name,
                    "pipeline_id": self.pipeline_id,
                    "application_id": self.application_id,
                    "camera_ids": self.camera_ids,
                },
                "benchmark_config": {
                    "video_path": self.video_path,
                    "video_settings": {
                        "streamingFPS": self.fps,
                        "width": self.width,
                        "height": self.height,
                        "video_quality": self.video_quality,
                        "aspect_ratio": self.aspect_ratio,
                    },
                    "compute_alias": self.compute_alias,
                    "app_name": self.app_name,
                    "min_cameras": self.min_cameras,
                    "max_cameras": self.max_cameras,
                    "interval_minutes": self.interval_minutes,
                    "step_size": self.step_size,
                    "metrics_interval_minutes": self.metrics_interval_minutes,
                    "camera_batch_size": self.camera_batch_size,
                    "pipeline_batch_size": self.pipeline_batch_size,
                    "auto_start": self.auto_start,
                    "facial_recognition_server_id": self.facial_recognition_server_id,
                    "lpr_server_id": self.lpr_server_id,
                    "cluster_name": self.cluster_name,
                    "runtime_framework": self.runtime_framework,
                },
                "camera_addition_history": self.camera_addition_history,
                "metrics_timeline": self.metrics_timeline,
            }

            # Write state file atomically
            temp_file = self.state_file + ".tmp"
            with open(temp_file, "w") as f:
                json.dump(state, f, indent=2)

            if os.path.exists(self.state_file):
                os.replace(temp_file, self.state_file)
            else:
                os.rename(temp_file, self.state_file)

            self._last_state_save_time = datetime.now(timezone.utc)
            return True

        except Exception as e:
            self.logger.warning(f"Failed to save state: {str(e)}")
            return False

    def load_state(self) -> bool:
        """
        Load benchmark state from file.

        Returns
        -------
        bool
            True if state was loaded successfully, False otherwise

        Raises
        ------
        Exception
            If state file is invalid or corrupted
        """
        if not os.path.exists(self.state_file):
            self.logger.warning(f"State file not found: {self.state_file}")
            return False

        try:
            with open(self.state_file, "r") as f:
                data = json.load(f)

            # Validate structure
            if not isinstance(data, dict):
                raise ValueError("State file is not a valid JSON object")

            # Check if this is a state file (has "version" key) or log file format
            if "version" in data:
                # This is a state file format
                state = data
            elif "experiment_info" in data and "setup_ids" in data:
                # This is a log file format, extract state from it
                state = {
                    "experiment_id": data.get("experiment_info", {}).get("experiment_id"),
                    "experiment_start_time": data.get("experiment_info", {}).get("experiment_start_time"),
                    "start_time": data.get("benchmark_config", {}).get("start_time"),
                    "end_time": data.get("benchmark_config", {}).get("end_time"),
                    "setup_ids": data.get("setup_ids", {}),
                    "camera_addition_history": self._extract_camera_additions_from_logs(data.get("logs", [])),
                    "metrics_timeline": self._extract_metrics_from_logs(data.get("logs", [])),
                }
            else:
                raise ValueError("Unknown file format")

            # Restore experiment ID and timestamps
            if state.get("experiment_id"):
                self.experiment_id = state["experiment_id"]

            if state.get("experiment_start_time"):
                self.experiment_start_time = datetime.fromisoformat(
                    state["experiment_start_time"].replace("Z", "+00:00")
                ).replace(tzinfo=None)

            if state.get("start_time"):
                self.start_time = datetime.fromisoformat(state["start_time"].replace("Z", "+00:00")).replace(
                    tzinfo=None
                )

            if state.get("end_time"):
                self.end_time = datetime.fromisoformat(state["end_time"].replace("Z", "+00:00")).replace(tzinfo=None)

            # Restore setup IDs
            if state.get("setup_ids"):
                setup_ids = state["setup_ids"]
                self.gateway_id = setup_ids.get("gateway_id")
                if setup_ids.get("lan_id"):
                    self.lan_id = setup_ids["lan_id"]
                if setup_ids.get("cluster_name"):
                    self.cluster_name = setup_ids["cluster_name"]
                self.pipeline_id = setup_ids.get("pipeline_id")
                self.application_id = setup_ids.get("application_id")
                self.camera_ids = setup_ids.get("camera_ids", [])

            # Restore benchmark config (including server IDs)
            if state.get("benchmark_config"):
                benchmark_config = state["benchmark_config"]
                self.facial_recognition_server_id = benchmark_config.get("facial_recognition_server_id")
                self.lpr_server_id = benchmark_config.get("lpr_server_id")
                if benchmark_config.get("cluster_name"):
                    self.cluster_name = benchmark_config.get("cluster_name")
                if benchmark_config.get("runtime_framework"):
                    self.runtime_framework = benchmark_config.get("runtime_framework")

            # Restore history and metrics
            if state.get("camera_addition_history"):
                self.camera_addition_history = state["camera_addition_history"]

            if state.get("metrics_timeline"):
                self.metrics_timeline = state["metrics_timeline"]

            # Reset is_running flag since we're loading from a saved state (process was interrupted)
            if state.get("is_running"):
                self.logger.info("Previous benchmark was running. Resetting is_running flag.")
                self.is_running = False

            # Mark log file as initialized if we have logs
            if self.metrics_timeline or self.camera_addition_history:
                self._log_file_initialized = True

            self.logger.info("State loaded successfully")
            self.logger.info("  Experiment ID: %s", str(self.experiment_id).replace("\n", "").replace("\r", ""))
            self.logger.info("  Cameras: %d", len(self.camera_ids))
            self.logger.info("  Metrics collected: %d", len(self.metrics_timeline))
            self.logger.info("  Camera additions: %d", len(self.camera_addition_history))

            return True

        except Exception as e:
            self.logger.error(f"Failed to load state: {str(e)}", exc_info=True)
            raise

    def resume_from_state(self) -> Dict[str, Any]:
        """
        Resume benchmark from saved state.

        Validates that all required resources (gateway, pipeline, etc.) still exist
        and are accessible before resuming.

        Returns
        -------
        dict
            Resume status with information about what was restored

        Raises
        ------
        Exception
            If state cannot be loaded or resources are invalid
        """
        if not os.path.exists(self.state_file):
            raise Exception(f"State file not found: {self.state_file}")

        self.logger.info("=" * 60)
        self.logger.info("RESUMING BENCHMARK FROM SAVED STATE")
        self.logger.info("=" * 60)

        # Load state
        if not self.load_state():
            raise Exception("Failed to load state")

        # Validate that required resources exist
        validation_results = {
            "gateway_valid": False,
            "pipeline_valid": False,
            "application_valid": False,
            "cameras_valid": False,
        }

        # Validate gateway
        if self.gateway_id:
            try:
                endpoint = f"/v1/streaming-gateways/{self.gateway_id}"
                response = self.automation.session.rpc.get(endpoint, timeout=300)
                validation_results["gateway_valid"] = response.get("success", False)
                if not validation_results["gateway_valid"]:
                    self.logger.warning(f"Gateway {self.gateway_id} not found or invalid")
            except Exception as e:
                self.logger.warning(f"Failed to validate gateway: {str(e)}")

        # Validate pipeline
        if self.pipeline_id:
            try:
                validation_results["pipeline_valid"] = True
                if not validation_results["pipeline_valid"]:
                    self.logger.warning(f"Pipeline {self.pipeline_id} not found or invalid")
            except Exception as e:
                self.logger.warning(f"Failed to validate pipeline: {str(e)}")

        # Validate application
        if self.application_id:
            try:
                app, error = self.automation.find_application_by_name(self.app_name)
                if not error and app is not None and app.get("_id") == self.application_id:
                    validation_results["application_valid"] = True
                else:
                    self.logger.warning(f"Application {self.application_id} not found or invalid")
            except Exception as e:
                self.logger.warning(f"Failed to validate application: {str(e)}")

        # Validate cameras (check at least some exist)
        if self.camera_ids:
            try:
                # Check first camera as sample
                if len(self.camera_ids) > 0:
                    endpoint = f"/v1/cameras/{self.camera_ids[0]}"
                    response = self.automation.session.rpc.get(endpoint, timeout=300)
                    validation_results["cameras_valid"] = response.get("success", False)
            except Exception as e:
                self.logger.warning(f"Failed to validate cameras: {str(e)}")

        # Log validation results
        self.logger.info("Resource validation:")
        for resource, valid in validation_results.items():
            status = "✓" if valid else "✗"
            self.logger.info(f"  {status} {resource}")

        # Warn if critical resources are missing
        if not validation_results["pipeline_valid"]:
            self.logger.error("Pipeline is invalid. Cannot resume benchmark.")
            raise Exception("Pipeline validation failed. Cannot resume.")

        if not validation_results["gateway_valid"]:
            self.logger.error("Gateway is invalid. Cannot resume benchmark.")
            raise Exception("Gateway validation failed. Cannot resume.")

        self.logger.info("=" * 60)
        self.logger.info("STATE RESTORED - Ready to resume benchmarking")
        self.logger.info("=" * 60)

        return {
            "status": "resumed",
            "experiment_id": self.experiment_id,
            "cameras_restored": len(self.camera_ids),
            "metrics_restored": len(self.metrics_timeline),
            "validation": validation_results,
        }

    def _calculate_summary(self) -> Dict[str, Any]:
        """
        Calculate summary statistics from collected metrics.

        Returns
        -------
        dict
            Summary statistics
        """
        if not self.metrics_timeline:
            return {}

        # Extract values for statistics with explicit types
        camera_throughputs: List[float] = []
        camera_latencies: List[float] = []
        gateway_throughputs: List[float] = []
        gateway_latencies: List[float] = []
        inference_throughputs: List[float] = []
        inference_latencies: List[float] = []
        post_processing_throughputs: List[float] = []
        post_processing_latencies: List[float] = []

        for entry in self.metrics_timeline:
            gw = entry.get("gateway_metrics", {})
            pl = entry.get("pipeline_metrics", {})

            # Gateway metrics
            if "aggregated" in gw:
                agg = gw["aggregated"]
                if "avg_camera_throughput_fps" in agg:
                    camera_throughputs.append(agg["avg_camera_throughput_fps"])
                if "avg_camera_latency_ms" in agg:
                    camera_latencies.append(agg["avg_camera_latency_ms"])
                if "avg_gateway_throughput_fps" in agg:
                    gateway_throughputs.append(agg["avg_gateway_throughput_fps"])
                if "avg_gateway_latency_ms" in agg:
                    gateway_latencies.append(agg["avg_gateway_latency_ms"])

            # Pipeline metrics
            if "inference" in pl:
                inf = pl["inference"]
                if "throughput_avg" in inf and inf["throughput_avg"] >= 0:
                    inference_throughputs.append(inf["throughput_avg"])
                if "latency_avg_ms" in inf and inf["latency_avg_ms"] >= 0:
                    inference_latencies.append(inf["latency_avg_ms"])

            if "post_processing" in pl:
                pp = pl["post_processing"]
                if "throughput_avg" in pp and pp["throughput_avg"] >= 0:
                    post_processing_throughputs.append(pp["throughput_avg"])
                if "latency_avg_ms" in pp and pp["latency_avg_ms"] >= 0:
                    post_processing_latencies.append(pp["latency_avg_ms"])

        # Explicitly type summary as Dict[str, Any] to allow heterogeneous values
        summary: Dict[str, Any] = {
            "total_cameras_added": len(self.camera_ids),
            "total_duration_minutes": (
                round((self.end_time - self.start_time).total_seconds() / 60, 2)
                if self.start_time and self.end_time
                else 0
            ),
            "metrics_snapshots_collected": len(self.metrics_timeline),
        }

        # Gateway statistics
        if camera_throughputs:
            summary["camera_throughput_fps_stats"] = {
                "average": round(sum(camera_throughputs) / len(camera_throughputs), 2),
                "min": round(min(camera_throughputs), 2),
                "max": round(max(camera_throughputs), 2),
            }

        if camera_latencies:
            summary["camera_latency_ms_stats"] = {
                "average": round(sum(camera_latencies) / len(camera_latencies), 2),
                "min": round(min(camera_latencies), 2),
                "max": round(max(camera_latencies), 2),
            }

        if gateway_throughputs:
            summary["gateway_throughput_fps_stats"] = {
                "average": round(sum(gateway_throughputs) / len(gateway_throughputs), 2),
                "min": round(min(gateway_throughputs), 2),
                "max": round(max(gateway_throughputs), 2),
            }

        if gateway_latencies:
            summary["gateway_latency_ms_stats"] = {
                "average": round(sum(gateway_latencies) / len(gateway_latencies), 2),
                "min": round(min(gateway_latencies), 2),
                "max": round(max(gateway_latencies), 2),
            }

        # Pipeline statistics
        if inference_throughputs:
            summary["inference_throughput_stats"] = {
                "average": round(sum(inference_throughputs) / len(inference_throughputs), 2),
                "min": round(min(inference_throughputs), 2),
                "max": round(max(inference_throughputs), 2),
            }

        if inference_latencies:
            summary["inference_latency_ms_stats"] = {
                "average": round(sum(inference_latencies) / len(inference_latencies), 2),
                "min": round(min(inference_latencies), 2),
                "max": round(max(inference_latencies), 2),
            }

        if post_processing_throughputs:
            summary["post_processing_throughput_stats"] = {
                "average": round(sum(post_processing_throughputs) / len(post_processing_throughputs), 2),
                "min": round(min(post_processing_throughputs), 2),
                "max": round(max(post_processing_throughputs), 2),
            }

        if post_processing_latencies:
            summary["post_processing_latency_ms_stats"] = {
                "average": round(sum(post_processing_latencies) / len(post_processing_latencies), 2),
                "min": round(min(post_processing_latencies), 2),
                "max": round(max(post_processing_latencies), 2),
            }

        return summary


if __name__ == "__main__":
    # Example usage
    import logging
    import os

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.FileHandler("benchmark.log"), logging.StreamHandler()],
        force=True,
    )

    # Load credentials from environment variables (never hardcode secrets)
    ACCOUNT_NUMBER = os.environ.get("MATRICE_ACCOUNT_NUMBER", "")
    ACCESS_KEY = os.environ.get("MATRICE_ACCESS_KEY_ID", "")
    SECRET_KEY = os.environ.get("MATRICE_SECRET_ACCESS_KEY", "")  # nosec B105
    PROJECT_ID = os.environ.get("MATRICE_PROJECT_ID", "")
    COMPUTE_ALIAS = os.environ.get("MATRICE_COMPUTE_ALIAS", "h100")
    cluster_name = os.environ.get("MATRICE_CLUSTER_NAME", "H100")
    # VIDEO_PATH = r"C:\Users\Adminstrator\Desktop\Matrice\release\py_matrice\iStock-2111071610.mp4"
    VIDEO_PATH = "https://s3.us-west-2.amazonaws.com/prod.application.predictions/09bfee3f1331a4210d4fbenchmark-video-1-43a2b3ab.mp4"  # ppl
    # VIDEO_PATH = "https://s3.us-west-2.amazonaws.com/prod.application.predictions/f3c918348127d24c9a16camera-video-1766600473947.mp4" # fr
    # VIDEO_PATH = r"C:\Users\Adminstrator\Desktop\Matrice\release\py_matrice\Entry4_MediaDemo2 (2).mp4"
    APP_NAME = "People Counting"  # "People Counting" "Face Recognition"
    # S = Session("9782886768719887307619115")
    # print(S.rpc.get("/v1/inference/get_camerastream_by_acc_number/9782886768719887307619115?projectId=68ff94e551fb982bb3508c82"))
    # # Initialize benchmarking
    benchmark = StreamingBenchmarking(
        video_path=VIDEO_PATH,
        compute_alias=COMPUTE_ALIAS,
        app_name=APP_NAME,
        account_number=ACCOUNT_NUMBER,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        project_id=PROJECT_ID,
        min_cameras=1000,
        max_cameras=1000,  # Fixed: was 200, should be 2000
        interval_minutes=2,
        step_size=250,
        metrics_interval_minutes=0.5,
        output_file="benchmark_results.json",
        state_file="benchmark_state.json",
        auto_resume=True,
        camera_batch_size=100,
        pipeline_batch_size=100,
        auto_start=False,
        # facial_recognition_server_id="694c2cbbc060108fe7514d38", # "694c4612c060108fe7514d6c"
        cluster_name=cluster_name,
        runtime_framework="Pytorch",
    )

    # pipeline_cameras = [
    #         {
    #             "cameraId": cam_id,
    #             "applications": [{"_idApplication": app_id}]
    #         }
    #         for cam_id in cams
    #     ]

    # pipeline_id, error = benchmark.automation.create_inference_pipeline(
    #     name="Benchmarking pipeline",
    #     project_id=benchmark.automation.session.project_id,
    #     cameras=pipeline_cameras,
    #     description="Benchmarking pipeline",
    # )
    # print(f"Pipeline created: {pipeline_id}")
    # print(f"Error: {error}")

    print("\n--- Example: Benchmarking Setup ---")
    # Initialize the setup (creates gateway, location, camera group, initial cameras, and pipeline)
    setup_results = benchmark.initialize_setup()
    print(f"Setup complete: {setup_results}")

    # Start benchmarking (adds cameras incrementally and collects metrics)
    print("\n--- Starting Benchmark ---")
    try:
        benchmark.start_benchmark(duration_minutes=60)  # Run for 60 minutes
    except KeyboardInterrupt:
        print("\n--- Stopping Benchmark ---")
        benchmark.stop_benchmark()

    # Export results
    print("\n--- Exporting Results ---")
    results_file = benchmark.export_results()
    print(f"Results exported to: {results_file}")
