
from typing import Dict, List, Optional, Any
import time
import logging
import asyncio
import base64
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from matrice_common.session import Session
from matrice_inference.server.stream.utils import CameraConfig
from matrice_inference.server.stream.app_event_listener import AppEventListener
from matrice_inference.server.stream.deployment_refresh_listener import DeploymentRefreshListener
from kafka import KafkaProducer


class AppDeployment:
    """Handles app deployment configuration and camera setup for streaming pipeline."""
    
    def __init__(self, session: Session, app_deployment_id: str, deployment_instance_id: Optional[str] = None, connection_timeout: int = 1200, action_id: Optional[str] = None):  # Increased from 300 to 1200
        self.app_deployment_id = app_deployment_id
        self.deployment_instance_id = deployment_instance_id
        self.rpc = session.rpc
        self.session = session
        self.connection_timeout = connection_timeout
        self.action_id = action_id
        self.logger = logging.getLogger(__name__)

        # Event listener for dynamic topic updates (initialized separately)
        self.event_listener: Optional[AppEventListener] = None
        self.refresh_listener: Optional[DeploymentRefreshListener] = None
        self.streaming_pipeline = None  # Reference to pipeline (set externally)
        self.event_loop = None  # Event loop reference for async operations
        self.camera_config_monitor = None  # Reference to monitor (set externally)

        # Heartbeat reporter for sending app deployment status
        self.heartbeat_producer: Optional[KafkaProducer] = None
        self.heartbeat_topic = "app_deployment_heartbeat"
        self.heartbeat_timeout = 5.0
        self._init_heartbeat_producer()

        # Server info cache with 10 minute expiration
        self._server_info_cache: Dict[str, Dict[str, Any]] = {}  # Key: f"{server_type}:{server_id}"
        self._cache_expiration = 600  # 10 minutes in seconds
    
    def get_input_topics(self) -> List[Dict]:
        """Get input topics for the app deployment."""
        try:
            response = self.rpc.get(f"/v1/inference/get_input_topics_by_app_deployment_id/{self.app_deployment_id}")
            if response.get("success", False):
                return response.get("data", [])
            else:
                self.logger.error(f"Failed to get input topics: {response.get('message', 'Unknown error')}")
                return []
        except Exception as e:
            self.logger.error(f"Exception getting input topics: {str(e)}")
            return []
    
    def get_output_topics(self) -> List[Dict]:
        """Get output topics for the app deployment."""
        try:
            response = self.rpc.get(f"/v1/inference/get_output_topics_by_app_deployment_id/{self.app_deployment_id}")
            if response.get("success", False):
                return response.get("data", [])
            else:
                self.logger.error(f"Failed to get output topics: {response.get('message', 'Unknown error')}")
                return []
        except Exception as e:
            self.logger.error(f"Exception getting output topics: {str(e)}")
            return []
    
    def get_camera_configs(self) -> Dict[str, CameraConfig]:
        """
        Get camera configurations for the streaming pipeline.
        
        Returns:
            Dict[str, CameraConfig]: Dictionary mapping camera_id to CameraConfig
        """
        camera_configs = {}
        
        try:
            # Get input and output topics
            input_topics = self.get_input_topics()
            output_topics = self.get_output_topics()
            
            if not input_topics:
                self.logger.warning("No input topics found for app deployment")
                return camera_configs
            
            # Create mapping of camera_id to output topic
            output_topic_map = {}
            for output_topic in output_topics:
                camera_id = output_topic.get("cameraId")
                if camera_id:
                    output_topic_map[camera_id] = output_topic
            
            # Process each input topic to create camera config
            for input_topic in input_topics:
                try:
                    camera_id = input_topic.get("cameraId")
                    if not camera_id:
                        self.logger.warning("Input topic missing camera ID, skipping")
                        continue
                    
                    # Get corresponding output topic
                    output_topic = output_topic_map.get(camera_id)
                    if not output_topic:
                        self.logger.warning(f"No output topic found for camera {camera_id}, skipping")
                        continue
                    
                    # Get connection info for this server
                    server_id = input_topic.get("serverId")
                    server_type = input_topic.get("serverType", "redis").lower()
                    
                    if not server_id:
                        self.logger.warning(f"No server ID found for camera {camera_id}, skipping")
                        continue
                    
                    connection_info = self.get_and_wait_for_connection_info(server_type, server_id)
                    if not connection_info:
                        self.logger.error(f"Could not get connection info for camera {camera_id}, skipping")
                        continue
                    
                    # Create stream config
                    stream_config = connection_info.copy()
                    stream_config["stream_type"] = server_type

                    # Store camera metadata for stream_info reconstruction
                    stream_config["camera_name"] = input_topic.get("cameraName", camera_id)
                    stream_config["camera_group"] = input_topic.get("cameraGroup", camera_id)
                    stream_config["location"] = input_topic.get("locationId", "Unknown Location")

                    # Validate stream_config
                    if not stream_config or "stream_type" not in stream_config:
                        self.logger.error(
                            f"Invalid stream_config for camera {camera_id}: {stream_config}, skipping"
                        )
                        continue
                    
                    # Log the configuration for debugging
                    self.logger.info(
                        f"Created camera config for {camera_id}: "
                        f"stream_type={server_type}, "
                        f"input_topic={input_topic.get('topicName')}, "
                        f"output_topic={output_topic.get('topicName')}, "
                        f"config_keys={list(stream_config.keys())}"
                    )
                    
                    # Create camera config
                    camera_config = CameraConfig(
                        camera_id=camera_id,
                        input_topic=input_topic.get("topicName"),
                        output_topic=output_topic.get("topicName"),
                        stream_config=stream_config,
                        enabled=True
                    )
                    
                    camera_configs[camera_id] = camera_config
                    
                except Exception as e:
                    self.logger.error(f"Error creating config for camera {camera_id}: {str(e)}")
                    continue
            
            self.logger.info(f"Successfully created {len(camera_configs)} camera configurations")
            return camera_configs

        except Exception as e:
            self.logger.error(f"Error getting camera configs: {str(e)}")
            return camera_configs

    async def load_cameras_incrementally(
        self,
        streaming_pipeline=None,
        event_loop=None,
        max_parallel_workers: int = 10
    ) -> Dict[str, Any]:
        """
        Load cameras incrementally and in parallel, adding each to the pipeline as soon as it's ready.

        This method:
        1. Fetches input/output topics
        2. Processes cameras in parallel (up to max_parallel_workers at a time)
        3. Adds each camera to the pipeline as soon as its config is ready
        4. Doesn't wait for all cameras - returns immediately after starting the process

        Args:
            streaming_pipeline: Reference to StreamingPipeline to add cameras to
            event_loop: Event loop for async operations
            max_parallel_workers: Maximum number of cameras to process in parallel

        Returns:
            Dict with summary: {"total_cameras": int, "started_loading": int}
        """
        try:
            # Store references
            if streaming_pipeline:
                self.streaming_pipeline = streaming_pipeline
            if event_loop:
                self.event_loop = event_loop

            # Get input and output topics
            self.logger.info("Fetching input/output topics for incremental camera loading...")
            input_topics = self.get_input_topics()
            output_topics = self.get_output_topics()

            if not input_topics:
                self.logger.warning("No input topics found - pipeline will start with zero cameras")
                return {"total_cameras": 0, "started_loading": 0}

            # Create mapping of camera_id to output topic
            output_topic_map = {
                output_topic.get("cameraId"): output_topic
                for output_topic in output_topics
                if output_topic.get("cameraId")
            }

            # Filter to only cameras that have both input and output topics
            cameras_to_load = []
            for input_topic in input_topics:
                camera_id = input_topic.get("cameraId")
                if camera_id and camera_id in output_topic_map:
                    cameras_to_load.append({
                        "camera_id": camera_id,
                        "input_topic": input_topic,
                        "output_topic": output_topic_map[camera_id]
                    })

            total_cameras = len(cameras_to_load)
            self.logger.info(
                f"Found {total_cameras} cameras ready to load "
                f"(will load in parallel with max {max_parallel_workers} workers)"
            )

            if total_cameras == 0:
                return {"total_cameras": 0, "started_loading": 0}

            # Start loading cameras in background (don't await)
            asyncio.create_task(
                self._load_cameras_parallel(cameras_to_load, max_parallel_workers)
            )

            return {
                "total_cameras": total_cameras,
                "started_loading": total_cameras
            }

        except Exception as e:
            self.logger.error(f"Error starting incremental camera load: {e}", exc_info=True)
            return {"total_cameras": 0, "started_loading": 0, "error": str(e)}

    async def _load_cameras_parallel(
        self,
        cameras_to_load: List[Dict[str, Any]],
        max_parallel_workers: int
    ) -> None:
        """
        Load cameras in parallel using ThreadPoolExecutor.

        Each camera's connection info is fetched in a thread, then added to pipeline.
        """
        total = len(cameras_to_load)
        loaded_count = 0
        failed_count = 0

        self.logger.info(f"Starting parallel camera loading: {total} cameras, {max_parallel_workers} workers")
        start_time = time.time()

        # Use ThreadPoolExecutor for parallel connection info fetching
        with ThreadPoolExecutor(max_workers=max_parallel_workers) as executor:
            # Submit all camera loading tasks
            future_to_camera = {
                executor.submit(
                    self._fetch_camera_config_sync,
                    camera_data["camera_id"],
                    camera_data["input_topic"],
                    camera_data["output_topic"]
                ): camera_data["camera_id"]
                for camera_data in cameras_to_load
            }

            # Process cameras as they complete
            for future in as_completed(future_to_camera):
                camera_id = future_to_camera[future]
                try:
                    camera_config = future.result()

                    if camera_config:
                        # Add to pipeline asynchronously
                        if self.streaming_pipeline:
                            try:
                                success = await self.streaming_pipeline.add_camera_config(camera_config)
                                if success:
                                    loaded_count += 1
                                    elapsed = time.time() - start_time
                                    self.logger.info(
                                        f"✓ Camera {camera_id} added to pipeline "
                                        f"({loaded_count}/{total}, {elapsed:.1f}s elapsed)"
                                    )
                                else:
                                    failed_count += 1
                                    self.logger.error(
                                        f"✗ Failed to add camera {camera_id} to pipeline "
                                        f"({loaded_count + failed_count}/{total})"
                                    )
                            except Exception as e:
                                failed_count += 1
                                self.logger.error(
                                    f"✗ Exception adding camera {camera_id} to pipeline: {e} "
                                    f"({loaded_count + failed_count}/{total})"
                                )
                        else:
                            failed_count += 1
                            self.logger.error(f"No streaming pipeline reference for camera {camera_id}")
                    else:
                        failed_count += 1
                        self.logger.warning(
                            f"✗ Failed to fetch config for camera {camera_id} "
                            f"({loaded_count + failed_count}/{total})"
                        )

                except Exception as e:
                    failed_count += 1
                    self.logger.error(
                        f"✗ Exception processing camera {camera_id}: {e} "
                        f"({loaded_count + failed_count}/{total})",
                        exc_info=True
                    )

        elapsed = time.time() - start_time
        self.logger.info(
            f"Parallel camera loading completed: {loaded_count} succeeded, {failed_count} failed, "
            f"{elapsed:.1f}s total ({elapsed/total:.2f}s per camera avg)"
        )

    def _fetch_camera_config_sync(
        self,
        camera_id: str,
        input_topic: Dict[str, Any],
        output_topic: Dict[str, Any]
    ) -> Optional[CameraConfig]:
        """
        Fetch camera configuration synchronously (for use in ThreadPoolExecutor).

        This method fetches connection info and creates CameraConfig.
        Runs in a thread pool to parallelize blocking I/O.
        """
        try:
            # Get connection info for this server
            server_id = input_topic.get("serverId")
            server_type = input_topic.get("serverType", "redis").lower()

            if not server_id:
                self.logger.warning(f"No server ID found for camera {camera_id}")
                return None

            # Fetch connection info (blocking call, but in thread pool)
            connection_info = self.get_and_wait_for_connection_info(server_type, server_id)
            if not connection_info:
                self.logger.error(f"Could not get connection info for camera {camera_id}")
                return None

            # Create stream config
            stream_config = connection_info.copy()
            stream_config["stream_type"] = server_type

            # Store camera metadata for stream_info reconstruction
            stream_config["camera_name"] = input_topic.get("cameraName", camera_id)
            stream_config["camera_group"] = input_topic.get("cameraGroup", camera_id)
            stream_config["location"] = input_topic.get("locationId", "Unknown Location")

            # Validate stream_config
            if not stream_config or "stream_type" not in stream_config:
                self.logger.error(
                    f"Invalid stream_config for camera {camera_id}: {stream_config}"
                )
                return None

            # Create camera config
            camera_config = CameraConfig(
                camera_id=camera_id,
                input_topic=input_topic.get("topicName"),
                output_topic=output_topic.get("topicName"),
                stream_config=stream_config,
                enabled=True
            )

            return camera_config

        except Exception as e:
            self.logger.error(f"Error fetching config for camera {camera_id}: {e}", exc_info=True)
            return None

    def _get_cached_server_info(self, server_type: str, server_id: str) -> Optional[Dict]:
        """Get server info from cache if available and not expired.
        
        Args:
            server_type: Type of server (kafka/redis)
            server_id: Server ID
            
        Returns:
            Cached connection info if available and valid, None otherwise
        """
        cache_key = f"{server_type}:{server_id}"
        
        if cache_key in self._server_info_cache:
            cached_entry = self._server_info_cache[cache_key]
            cached_time = cached_entry.get('timestamp', 0)
            current_time = time.time()
            
            # Check if cache is still valid (within 10 minutes)
            if current_time - cached_time < self._cache_expiration:
                self.logger.debug(
                    f"Using cached {server_type} server info for {server_id} "
                    f"(age: {current_time - cached_time:.1f}s)"
                )
                return cached_entry.get('data')
            else:
                # Cache expired, remove it
                self.logger.debug(f"Cache expired for {server_type} server {server_id}, will fetch fresh data")
                del self._server_info_cache[cache_key]
        
        return None

    def _cache_server_info(self, server_type: str, server_id: str, connection_info: Dict) -> None:
        """Cache server connection info with timestamp.
        
        Args:
            server_type: Type of server (kafka/redis)
            server_id: Server ID
            connection_info: Connection info to cache
        """
        cache_key = f"{server_type}:{server_id}"
        self._server_info_cache[cache_key] = {
            'timestamp': time.time(),
            'data': connection_info
        }
        self.logger.debug(f"Cached {server_type} server info for {server_id}")

    def get_and_wait_for_connection_info(self, server_type: str, server_id: str) -> Optional[Dict]:
        """Get the connection information for the streaming gateway."""
        # Check cache first
        cached_info = self._get_cached_server_info(server_type, server_id)
        if cached_info:
            return cached_info

        def _get_kafka_connection_info():
            try:
                response = self.rpc.get(f"/v1/actions/get_kafka_server/{server_id}")
                if response.get("success", False):
                    data = response.get("data")
                    if (
                        data
                        and data.get("ipAddress")
                        and data.get("port")
                        and data.get("status") == "running"
                    ):
                        return {
                            'bootstrap_servers': f'{data["ipAddress"]}:{data["port"]}',
                            'sasl_mechanism': 'SCRAM-SHA-256',
                            'sasl_username': os.environ.get("KAFKA_SASL_USERNAME"),
                            'sasl_password': os.environ.get("KAFKA_SASL_PASSWORD"),
                            'security_protocol': 'SASL_PLAINTEXT'
                        }
                    else:
                        self.logger.debug("Kafka connection information is not complete, waiting...")
                        return None
                else:
                    self.logger.debug("Failed to get Kafka connection information: %s", response.get("message", "Unknown error"))
                    return None
            except Exception as exc:
                self.logger.debug("Exception getting Kafka connection info: %s", str(exc))
                return None

        def _get_redis_connection_info():
            # Try API first, fall back to hardcoded config if API fails
            try:
                # Build URL with actionId query parameter if available
                url = f"/v1/actions/redis_servers/{server_id}"
                if self.action_id:
                    url += f"?actionId={self.action_id}"
                response = self.rpc.get(url)
                if response.get("success", False):
                    data = response.get("data")
                    if (
                        data
                        # and data.get("host")
                        and data.get("port")
                        and data.get("status") == "running"
                    ):
                        return {
                            'host': data.get("host") or "localhost",
                            'port': int(data["port"]),
                            'password': data.get("password", ""),  # Empty string for passwordless Redis
                            'username': data.get("username"),       # None if not provided
                            'db': data.get("db", 0),
                            'connection_timeout': 120  # Increased from 30 to 120
                        }
            except Exception as exc:
                self.logger.debug("Exception getting Redis connection info from API: %s", str(exc))

            # Fallback: hardcoded Redis config for local deployment
            self.logger.warning("REDIS API CALL FAILED FOR SERVER ID: %s, USING HARDCODED LOCAL REDIS CONFIG", server_id)
            return {
                'host': 'localhost',
                'port': 6379,
                'password': 'MTc2ODgzMTAyMTcxMDQyNTgwMA==',
                'username': None,
                'db': 0,
                'connection_timeout': 120
            }

        start_time = time.time()
        last_log_time = 0
        
        while True:
            current_time = time.time()
            
            # Get connection info based on server type
            connection_info = None
            if server_type == "kafka":
                connection_info = _get_kafka_connection_info()
            elif server_type == "redis":
                connection_info = _get_redis_connection_info()
            else:
                raise ValueError(f"Unsupported server type: {server_type}")
            
            # If we got valid connection info, cache it and return
            if connection_info:
                self.logger.info("Successfully retrieved %s connection information", server_type)
                self._cache_server_info(server_type, server_id, connection_info)
                return connection_info
            
            # Check timeout
            if current_time - start_time > self.connection_timeout:
                error_msg = f"Timeout waiting for {server_type} connection information after {self.connection_timeout} seconds"
                self.logger.error(error_msg)
                
                # Log the last response for debugging
                try:
                    if server_type == "kafka":
                        response = self.rpc.get(f"/v1/actions/get_kafka_server/{server_id}")
                    else:
                        url = f"/v1/actions/redis_servers/{server_id}"
                        if self.action_id:
                            url += f"?actionId={self.action_id}"
                        response = self.rpc.get(url)
                    self.logger.error("Last response received: %s", response)
                except Exception as exc:
                    self.logger.error("Failed to get last response for debugging: %s", str(exc))
                
                return None  # Return None instead of raising exception to allow graceful handling
            
            # Log waiting message every 10 seconds to avoid spam
            if current_time - last_log_time >= 10:
                elapsed = current_time - start_time
                remaining = self.connection_timeout - elapsed
                self.logger.info("Waiting for %s connection information... (%.1fs elapsed, %.1fs remaining)",
                           server_type, elapsed, remaining)
                last_log_time = current_time

            time.sleep(1)

    def _init_heartbeat_producer(self):
        """Initialize Kafka producer for heartbeats."""
        try:
            # Get Kafka configuration
            response = self.rpc.get("/v1/actions/get_kafka_info")

            if not response or "data" not in response:
                self.logger.error("Failed to get Kafka info for heartbeat reporter")
                return

            data = response.get("data", {})

            # Decode connection info
            ip = base64.b64decode(data["ip"]).decode("utf-8")
            port = base64.b64decode(data["port"]).decode("utf-8")
            bootstrap_servers = f"{ip}:{port}"

            # Create Kafka producer config
            kafka_config = {
                'bootstrap_servers': bootstrap_servers,
                'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
                'key_serializer': lambda k: k.encode('utf-8') if k else None,
                'acks': 1,  # Wait for leader acknowledgment
                'retries': 3,
                'max_in_flight_requests_per_connection': 1,
            }

            # Add SASL authentication if available
            if "username" in data and "password" in data:
                username = base64.b64decode(data["username"]).decode("utf-8")
                password = base64.b64decode(data["password"]).decode("utf-8")

                kafka_config.update({
                    'security_protocol': 'SASL_PLAINTEXT',
                    'sasl_mechanism': 'SCRAM-SHA-256',
                    'sasl_plain_username': username,
                    'sasl_plain_password': password,
                })

            # Create producer
            self.heartbeat_producer = KafkaProducer(**kafka_config)
            self.logger.info(f"Kafka heartbeat producer initialized: {bootstrap_servers}, topic: {self.heartbeat_topic}")

        except Exception as e:
            self.logger.error(f"Failed to initialize Kafka heartbeat producer: {e}", exc_info=True)
            self.heartbeat_producer = None

    def send_heartbeat(self, camera_configs: Dict[str, CameraConfig]) -> bool:
        """
        Send heartbeat to Kafka topic with current camera configurations.

        Args:
            camera_configs: Dictionary of camera_id -> CameraConfig

        Returns:
            True if successful, False otherwise
        """
        if not self.heartbeat_producer:
            self.logger.warning("Kafka heartbeat producer not initialized, cannot send heartbeat")
            return False

        try:
            # Get refresh-managed cameras info for enhanced payload
            refresh_managed_cameras = set()
            if self.camera_config_monitor and hasattr(self.camera_config_monitor, '_refresh_managed_cameras'):
                with self.camera_config_monitor._refresh_lock:
                    refresh_managed_cameras = self.camera_config_monitor._refresh_managed_cameras.copy()

            # Build camera config payload with management type
            cameras = []
            refresh_managed_count = 0
            monitor_managed_count = 0

            for camera_id, config in camera_configs.items():
                is_refresh_managed = camera_id in refresh_managed_cameras
                if is_refresh_managed:
                    refresh_managed_count += 1
                else:
                    monitor_managed_count += 1

                camera_data = {
                    "camera_id": camera_id,
                    "input_topic": config.input_topic,
                    "output_topic": config.output_topic,
                    "stream_type": config.stream_config.get("stream_type", "unknown"),
                    "enabled": config.enabled,
                    "management_type": "refresh" if is_refresh_managed else "monitor/event"
                }
                cameras.append(camera_data)

            # Build heartbeat message with enhanced metadata
            heartbeat = {
                "app_deployment_id": self.app_deployment_id,
                "deployment_instance_id": self.deployment_instance_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "camera_count": len(cameras),
                "refresh_managed_count": refresh_managed_count,
                "monitor_managed_count": monitor_managed_count,
                "cameras": cameras
            }

            # Send to Kafka
            future = self.heartbeat_producer.send(
                self.heartbeat_topic,
                value=heartbeat,
                key=self.app_deployment_id
            )

            # Wait for send to complete with timeout
            future.get(timeout=self.heartbeat_timeout)

            self.logger.debug(
                f"Heartbeat payload: {len(cameras)} cameras "
                f"({refresh_managed_count} refresh-managed, {monitor_managed_count} monitor-managed)"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to send heartbeat to Kafka: {e}", exc_info=True)
            return False

    def close_heartbeat_producer(self):
        """Close Kafka heartbeat producer."""
        if self.heartbeat_producer:
            try:
                self.heartbeat_producer.close(timeout=5)
                self.logger.info("Kafka heartbeat producer closed")
            except Exception as e:
                self.logger.error(f"Error closing Kafka heartbeat producer: {e}")

    def initialize_event_listener(self, streaming_pipeline=None, event_loop=None) -> bool:
        """Initialize and start the app event listener.

        Args:
            streaming_pipeline: Reference to the StreamingPipeline instance for dynamic updates
            event_loop: Event loop for scheduling async tasks (optional, will try to get running loop)

        Returns:
            bool: True if successfully initialized and started
        """
        try:
            if self.event_listener and self.event_listener.is_listening:
                self.logger.warning("Event listener already running")
                return False

            self.streaming_pipeline = streaming_pipeline

            # Get or store event loop
            if event_loop:
                self.event_loop = event_loop
            else:
                try:
                    self.event_loop = asyncio.get_running_loop()
                except RuntimeError:
                    self.logger.warning("No running event loop found, async operations may not work")
                    self.event_loop = None

            # Create event listener
            self.event_listener = AppEventListener(
                session=self.session,
                app_deployment_id=self.app_deployment_id,
                on_topic_added=self._handle_topic_added,
                on_topic_deleted=self._handle_topic_deleted
            )

            # Start listening
            success = self.event_listener.start()
            if success:
                self.logger.info(f"App event listener started for deployment {self.app_deployment_id}")
            else:
                self.logger.error("Failed to start app event listener")

            return success

        except Exception as e:
            self.logger.error(f"Error initializing event listener: {e}")
            return False

    def stop_event_listener(self):
        """Stop the app event listener and close heartbeat producer."""
        if self.event_listener:
            self.event_listener.stop()
            self.event_listener = None
            self.logger.info("App event listener stopped")

        # Close heartbeat producer
        self.close_heartbeat_producer()

    def _handle_topic_added(self, event: Dict[str, Any]):
        """Handle topic added event.

        Args:
            event: Event dict containing topic information
        """
        try:
            topic_type = event.get('topicType')
            topic_data = event.get('data', {})
            camera_id = topic_data.get('cameraId')
            topic_name = topic_data.get('topicName')
            server_type = topic_data.get('serverType')

            self.logger.info(
                f"Topic added event received: {topic_type} topic for camera {camera_id} "
                f"(topic={topic_name}, server={server_type})"
            )

            # Validate required fields
            if not camera_id:
                self.logger.error("Topic added event missing cameraId, ignoring")
                return

            # CRITICAL: If camera is managed by refresh, event listener should NOT interfere
            # Once a camera appears in ANY refresh event, only refresh can modify it
            # This prevents event listener from re-adding cameras that refresh removed
            if self.camera_config_monitor and hasattr(self.camera_config_monitor, '_refresh_managed_cameras'):
                with self.camera_config_monitor._refresh_lock:
                    if camera_id in self.camera_config_monitor._refresh_managed_cameras:
                        total_refresh_managed = len(self.camera_config_monitor._refresh_managed_cameras)
                        self.logger.info(
                            f"⊘ Event Listener: Ignoring topic added for camera {camera_id} - "
                            f"refresh-managed (only refresh can modify, {total_refresh_managed} total refresh-managed cameras)"
                        )
                        return

            # For input topics, wait for corresponding output topic before adding camera
            if topic_type == 'input':
                self.logger.info(
                    f"Input topic added for camera {camera_id}. Will add to pipeline "
                    f"when corresponding output topic is available."
                )
                # Don't refresh yet - wait for output topic
                return

            # For output topics, try to refresh camera config (will succeed if input topic exists)
            if topic_type == 'output':
                # Refresh camera configs to include the new topic
                if not self.streaming_pipeline:
                    self.logger.error("No streaming pipeline reference, cannot add camera")
                    return

                if not self.event_loop:
                    self.logger.error("No event loop reference, cannot schedule async operation")
                    return
                
                if not self.event_loop.is_running():
                    self.logger.error("Event loop is not running, cannot schedule async operation")
                    return

                self.logger.info(f"Output topic added, attempting to add camera {camera_id} to pipeline")
                future = asyncio.run_coroutine_threadsafe(
                    self._refresh_camera_config(camera_id),
                    self.event_loop
                )
                
                # Optional: Add callback to log result
                def log_result(fut):
                    try:
                        fut.result()  # This will raise if the coroutine raised
                    except Exception as e:
                        self.logger.error(f"Failed to refresh camera config: {e}")
                
                future.add_done_callback(log_result)

        except Exception as e:
            self.logger.error(f"Error handling topic added event: {e}", exc_info=True)

    def _handle_topic_deleted(self, event: Dict[str, Any]):
        """Handle topic deleted event.

        Args:
            event: Event dict containing topic information
        """
        try:
            topic_type = event.get('topicType')
            topic_data = event.get('data', {})
            camera_id = topic_data.get('cameraId')
            topic_name = topic_data.get('topicName')

            self.logger.info(
                f"Topic deleted event received: {topic_type} topic for camera {camera_id} "
                f"(topic={topic_name})"
            )

            # Validate required fields
            if not camera_id:
                self.logger.error("Topic deleted event missing cameraId, ignoring")
                return

            # CRITICAL: If camera is managed by refresh, event listener should NOT interfere
            # Once a camera appears in ANY refresh event, only refresh can modify it
            # This prevents event listener from removing cameras that should only be managed by refresh
            if self.camera_config_monitor and hasattr(self.camera_config_monitor, '_refresh_managed_cameras'):
                with self.camera_config_monitor._refresh_lock:
                    if camera_id in self.camera_config_monitor._refresh_managed_cameras:
                        total_refresh_managed = len(self.camera_config_monitor._refresh_managed_cameras)
                        self.logger.info(
                            f"⊘ Event Listener: Ignoring topic deleted for camera {camera_id} - "
                            f"refresh-managed (only refresh can modify, {total_refresh_managed} total refresh-managed cameras)"
                        )
                        return

            # If input topic is deleted, log but don't remove from pipeline
            # (input topics may be shared, and removal should be based on output topic)
            if topic_type == 'input':
                self.logger.info(
                    f"Input topic deleted for camera {camera_id}. "
                    f"Camera will remain in pipeline unless output topic is also deleted."
                )
                return

            # If output topic is deleted, remove camera from pipeline
            if topic_type == 'output':
                if not self.streaming_pipeline:
                    self.logger.error("No streaming pipeline reference, cannot remove camera")
                    return

                if not self.event_loop:
                    self.logger.error("No event loop reference, cannot schedule async operation")
                    return
                
                if not self.event_loop.is_running():
                    self.logger.error("Event loop is not running, cannot schedule async operation")
                    return

                self.logger.info(f"Output topic deleted, removing camera {camera_id} from pipeline")
                future = asyncio.run_coroutine_threadsafe(
                    self._remove_camera_from_pipeline(camera_id),
                    self.event_loop
                )
                
                # Add callback to log result
                def log_result(fut):
                    try:
                        fut.result()  # This will raise if the coroutine raised
                    except Exception as e:
                        self.logger.error(f"Failed to remove camera from pipeline: {e}")
                
                future.add_done_callback(log_result)

        except Exception as e:
            self.logger.error(f"Error handling topic deleted event: {e}", exc_info=True)

    def get_single_camera_config(self, camera_id: str) -> Optional[CameraConfig]:
        """
        Get configuration for a single camera by ID.

        This is more efficient than fetching all cameras when we only need one.

        Args:
            camera_id: ID of camera to fetch

        Returns:
            CameraConfig if found and valid, None otherwise
        """
        try:
            # Get input and output topics
            input_topics = self.get_input_topics()
            output_topics = self.get_output_topics()

            # Find the specific camera's topics
            input_topic = None
            output_topic = None

            for topic in input_topics:
                if topic.get("cameraId") == camera_id:
                    input_topic = topic
                    break

            for topic in output_topics:
                if topic.get("cameraId") == camera_id:
                    output_topic = topic
                    break

            # Validate we have both topics
            if not input_topic:
                self.logger.debug(f"No input topic found for camera {camera_id}")
                return None

            if not output_topic:
                self.logger.debug(f"No output topic found for camera {camera_id}")
                return None

            # Get connection info
            server_id = input_topic.get("serverId")
            server_type = input_topic.get("serverType", "redis").lower()

            if not server_id:
                self.logger.warning(f"No server ID for camera {camera_id}")
                return None

            # Fetch connection info
            connection_info = self.get_and_wait_for_connection_info(server_type, server_id)
            if not connection_info:
                self.logger.error(f"Could not get connection info for camera {camera_id}")
                return None

            # Create stream config
            stream_config = connection_info.copy()
            stream_config["stream_type"] = server_type

            # Store camera metadata for stream_info reconstruction
            stream_config["camera_name"] = input_topic.get("cameraName", camera_id)
            stream_config["camera_group"] = input_topic.get("cameraGroup", camera_id)
            stream_config["location"] = input_topic.get("locationId", "Unknown Location")

            # Validate stream_config
            if not stream_config or "stream_type" not in stream_config:
                self.logger.error(
                    f"Invalid stream_config for camera {camera_id}: {stream_config}"
                )
                return None

            # Create camera config
            camera_config = CameraConfig(
                camera_id=camera_id,
                input_topic=input_topic.get("topicName"),
                output_topic=output_topic.get("topicName"),
                stream_config=stream_config,
                enabled=True
            )

            self.logger.info(
                f"Fetched config for camera {camera_id}: "
                f"stream_type={server_type}, "
                f"input={camera_config.input_topic}, "
                f"output={camera_config.output_topic}"
            )

            return camera_config

        except Exception as e:
            self.logger.error(f"Error getting config for camera {camera_id}: {e}", exc_info=True)
            return None

    async def _refresh_camera_config(self, camera_id: str):
        """Refresh camera configuration and update pipeline.

        Args:
            camera_id: ID of camera to refresh
        """
        try:
            self.logger.info(f"Refreshing camera config for {camera_id}")

            # Get fresh camera config (optimized to fetch only this camera)
            new_config = self.get_single_camera_config(camera_id)

            # Check if camera config was successfully fetched
            if new_config:
                # Update or add camera in pipeline
                if self.streaming_pipeline:
                    success = await self.streaming_pipeline.add_camera_config(new_config)
                    if success:
                        self.logger.info(
                            f"✓ Successfully added/updated camera {camera_id} in pipeline "
                            f"(input={new_config.input_topic}, output={new_config.output_topic})"
                        )
                    else:
                        self.logger.error(f"✗ Failed to add/update camera {camera_id} in pipeline")
                else:
                    self.logger.error("No streaming pipeline available")
            else:
                self.logger.warning(
                    f"Camera {camera_id} config could not be fetched. "
                    f"This may indicate that both input and output topics are not yet available."
                )

        except Exception as e:
            self.logger.error(f"Error refreshing camera config for {camera_id}: {e}", exc_info=True)

    async def _remove_camera_from_pipeline(self, camera_id: str):
        """Remove camera from pipeline.

        Args:
            camera_id: ID of camera to remove
        """
        try:
            self.logger.info(f"Removing camera {camera_id} from pipeline")

            if self.streaming_pipeline:
                success = await self.streaming_pipeline.remove_camera_config(camera_id)
                if success:
                    self.logger.info(f"✓ Successfully removed camera {camera_id} from pipeline")
                else:
                    self.logger.warning(
                        f"✗ Failed to remove camera {camera_id} from pipeline "
                        f"(may have already been removed)"
                    )
            else:
                self.logger.error("No streaming pipeline available")

        except Exception as e:
            self.logger.error(f"Error removing camera {camera_id} from pipeline: {e}", exc_info=True)

    def initialize_refresh_listener(
        self,
        streaming_pipeline=None,
        event_loop=None,
        camera_config_monitor=None
    ) -> bool:
        """Initialize and start the deployment refresh listener.

        Args:
            streaming_pipeline: Reference to the StreamingPipeline instance
            event_loop: Event loop for scheduling async tasks
            camera_config_monitor: Reference to CameraConfigMonitor for notifications

        Returns:
            bool: True if successfully initialized and started
        """
        try:
            if not self.deployment_instance_id:
                self.logger.error("No deployment_instance_id provided, cannot start refresh listener")
                return False

            if self.refresh_listener and self.refresh_listener.is_listening:
                self.logger.warning("Refresh listener already running")
                return False

            self.streaming_pipeline = streaming_pipeline
            self.camera_config_monitor = camera_config_monitor

            # Get or store event loop
            if event_loop:
                self.event_loop = event_loop
            else:
                try:
                    self.event_loop = asyncio.get_running_loop()
                except RuntimeError:
                    self.logger.warning("No running event loop found, async operations may not work")
                    self.event_loop = None

            # Create refresh listener
            self.refresh_listener = DeploymentRefreshListener(
                session=self.session,
                deployment_instance_id=self.deployment_instance_id,
                on_refresh=self._handle_refresh_event
            )

            # Start listening
            success = self.refresh_listener.start()
            if success:
                self.logger.info(
                    f"Deployment refresh listener started for instance {self.deployment_instance_id} "
                    f"(PRIMARY source of truth)"
                )
            else:
                self.logger.error("Failed to start deployment refresh listener")

            return success

        except Exception as e:
            self.logger.error(f"Error initializing refresh listener: {e}", exc_info=True)
            return False

    def stop_refresh_listener(self):
        """Stop the deployment refresh listener."""
        if self.refresh_listener:
            self.refresh_listener.stop()
            self.refresh_listener = None
            self.logger.info("Deployment refresh listener stopped")

    def _handle_refresh_event(self, event: Dict[str, Any]):
        """Handle refresh event containing full camera configuration snapshot.

        This event is sent by the backend when the deployment needs to be
        scaled or rebalanced. The backend distributes camera topics across
        deployment instances based on FPS requirements to ensure even load
        distribution.

        Backend Logic:
        1. Gets total required FPS for all cameras in the app deployment
        2. Gets all running deployment instances
        3. Calculates FPS per instance (total_fps / num_instances)
        4. Sorts output topics by camera FPS (ascending)
        5. Assigns topics to instances to balance FPS load
        6. Sends refresh event to each instance with its assigned topics

        Args:
            event: Refresh event dict with structure:
                {
                    "eventType": "refresh",
                    "streamingGatewayId": "...",  # NOTE: Key name is wrong, this is deployInstanceId
                    "timestamp": "...",
                    "data": [CameraStreamTopicResponse]
                }

                Where each CameraStreamTopicResponse contains:
                {
                    "id": "...",
                    "accountNumber": "...",
                    "cameraId": "...",
                    "streamingGatewayId": "...",
                    "serverId": "...",
                    "serverType": "redis" | "kafka",
                    "appDeploymentId": "...",
                    "topicName": "...",
                    "topicType": "input" | "output",
                    "ipAddress": "...",
                    "port": 123,
                    "consumingAppsDeploymentIds": [...],
                    "cameraFPS": 30,
                    "deployInstanceId": "..."
                }

                NOTE: Backend sends "streamingGatewayId" but the value is actually
                the deployment instance ID. The key name is incorrect in the backend.
        """
        try:
            timestamp = event.get('timestamp', 'unknown')
            streaming_topics = event.get('data', [])

            self.logger.warning(
                f"Refresh event received: timestamp={timestamp}, "
                f"streaming_topics={len(streaming_topics)}"
            )

            # CRITICAL: Validate that streaming_topics is not None and is a list
            if streaming_topics is None:
                self.logger.warning(
                    "Refresh event has None data - treating as empty assignment. "
                    "This will remove all cameras from this instance."
                )
                streaming_topics = []
            
            # Empty refresh event is VALID - it means this instance should handle NO cameras
            # This is intentional during scale-down or rebalancing
            if len(streaming_topics) == 0:
                current_camera_count = len(self.streaming_pipeline.camera_configs) if self.streaming_pipeline else 0
                if current_camera_count > 0:
                    self.logger.warning(
                        f"Refresh event has EMPTY data array - this will remove ALL {current_camera_count} cameras from this instance. "
                        f"This is expected during scale-down or rebalancing."
                    )
                else:
                    self.logger.info("Refresh event has empty data and no cameras currently configured - no action needed")

            # Build camera configs from streaming topics
            new_camera_configs = self._build_camera_configs_from_streaming_topics(streaming_topics)

            self.logger.info(
                f"Built {len(new_camera_configs)} camera configs from refresh event "
                f"(from {len(streaming_topics)} streaming topics)"
            )

            # Validate we have cameras if streaming_topics was not empty
            if len(streaming_topics) > 0 and len(new_camera_configs) == 0:
                self.logger.error(
                    f"Failed to build any camera configs from {len(streaming_topics)} streaming topics - "
                    f"skipping refresh to avoid accidental removal of all cameras"
                )
                return

            # Check event loop availability
            if not self.streaming_pipeline:
                self.logger.error("No streaming pipeline reference, cannot reconcile cameras")
                return

            if not self.event_loop:
                self.logger.error("No event loop reference, cannot schedule async operation")
                return

            # Check event loop state comprehensively
            if self.event_loop.is_closed():
                self.logger.error("Event loop is closed, cannot schedule async operation")
                return

            if not self.event_loop.is_running():
                self.logger.error("Event loop is not running, cannot schedule async operation")
                return

            # Schedule reconciliation on event loop with error handling
            self.logger.warning(f"Scheduling camera reconciliation on event loop...")
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._reconcile_cameras(new_camera_configs, timestamp),
                    self.event_loop
                )
            except RuntimeError as e:
                self.logger.error(f"Failed to schedule reconciliation - event loop may have closed: {e}")
                return

            # Add callback to log result with timeout protection
            def log_result(fut):
                try:
                    # Use timeout to prevent indefinite blocking
                    success = fut.result(timeout=300)  # 5 minute timeout
                    if success:
                        self.logger.info(f"✓ Refresh reconciliation completed successfully")
                    else:
                        self.logger.error(f"✗ Refresh reconciliation failed")
                except TimeoutError:
                    self.logger.error(f"✗ Refresh reconciliation timed out after 300 seconds")
                except Exception as e:
                    self.logger.error(f"✗ Exception during refresh reconciliation: {e}", exc_info=True)

            future.add_done_callback(log_result)

        except Exception as e:
            self.logger.error(
                f"Error handling refresh event: {e}\n"
                f"Event: {event}",
                exc_info=True
            )

    def _build_camera_configs_from_streaming_topics(
        self,
        streaming_topics: List[Dict[str, Any]]
    ) -> Dict[str, CameraConfig]:
        """Build camera configurations from streaming topics data.

        Args:
            streaming_topics: List of StreamingTopics from refresh event

        Returns:
            Dict mapping camera_id to CameraConfig
        """
        camera_configs = {}

        try:
            # Group streaming topics by camera_id
            topics_by_camera = {}
            for topic in streaming_topics:
                camera_id = topic.get('cameraId')
                if not camera_id:
                    self.logger.warning(f"Streaming topic missing cameraId: {topic}")
                    continue

                if camera_id not in topics_by_camera:
                    topics_by_camera[camera_id] = {'input': None, 'output': None}

                topic_type = topic.get('topicType', '').lower()
                topics_by_camera[camera_id][topic_type] = topic

            # Build camera config for each camera
            for camera_id, topics in topics_by_camera.items():
                try:
                    input_topic = topics.get('input')
                    output_topic = topics.get('output')

                    # Validate we have both input and output topics
                    if not input_topic or not output_topic:
                        self.logger.warning(
                            f"Camera {camera_id} missing input or output topic, skipping "
                            f"(input={input_topic is not None}, output={output_topic is not None})"
                        )
                        continue

                    # Get connection info from input topic
                    server_id = input_topic.get('serverId')
                    server_type = input_topic.get('serverType', 'redis').lower()

                    if not server_id:
                        self.logger.warning(f"No server ID for camera {camera_id}, skipping")
                        continue

                    # Validate server type
                    valid_server_types = ['redis', 'kafka']
                    if server_type not in valid_server_types:
                        self.logger.error(
                            f"Invalid server type '{server_type}' for camera {camera_id} "
                            f"(valid types: {valid_server_types}), skipping"
                        )
                        continue

                    # Get connection info (with timeout/wait)
                    try:
                        connection_info = self.get_and_wait_for_connection_info(server_type, server_id)
                    except Exception as e:
                        self.logger.error(
                            f"Exception getting connection info for camera {camera_id}: {e}, skipping",
                            exc_info=True
                        )
                        continue

                    if not connection_info:
                        self.logger.error(f"Could not get connection info for camera {camera_id}, skipping")
                        continue

                    # Create stream config
                    stream_config = connection_info.copy()
                    stream_config["stream_type"] = server_type

                    # Store camera metadata for stream_info reconstruction
                    stream_config["camera_name"] = input_topic.get("cameraName", camera_id)
                    stream_config["camera_group"] = input_topic.get("cameraGroup", camera_id)
                    stream_config["location"] = input_topic.get("locationId", "Unknown Location")

                    # Validate stream_config
                    if not stream_config or "stream_type" not in stream_config:
                        self.logger.error(
                            f"Invalid stream_config for camera {camera_id}: {stream_config}, skipping"
                        )
                        continue

                    # Log the configuration
                    self.logger.info(
                        f"Created camera config for {camera_id}: "
                        f"stream_type={server_type}, "
                        f"input_topic={input_topic.get('topicName')}, "
                        f"output_topic={output_topic.get('topicName')}"
                    )

                    # Create camera config
                    camera_config = CameraConfig(
                        camera_id=camera_id,
                        input_topic=input_topic.get('topicName'),
                        output_topic=output_topic.get('topicName'),
                        stream_config=stream_config,
                        enabled=True
                    )

                    camera_configs[camera_id] = camera_config

                except Exception as e:
                    self.logger.error(f"Error creating config for camera {camera_id}: {e}", exc_info=True)
                    continue

            # Log summary of cameras and total FPS
            if camera_configs:
                camera_ids = list(camera_configs.keys())
                self.logger.info(f"Successfully built camera configs: {', '.join(camera_ids)}")

            return camera_configs

        except Exception as e:
            self.logger.error(f"Error building camera configs from streaming topics: {e}", exc_info=True)
            return {}

    async def _reconcile_cameras(
        self,
        new_camera_configs: Dict[str, CameraConfig],
        event_timestamp: str
    ) -> bool:
        """Reconcile pipeline cameras with new configuration snapshot.

        Performs full replacement: cameras in new_camera_configs become the
        complete set of active cameras.

        Args:
            new_camera_configs: New camera configuration dict (full snapshot)
            event_timestamp: Timestamp from refresh event

        Returns:
            bool: True if reconciliation succeeded
        """
        try:
            # Get current camera IDs
            current_ids = set(self.streaming_pipeline.camera_configs.keys()) if self.streaming_pipeline else set()
            new_ids = set(new_camera_configs.keys())

            # CRITICAL: Capture OLD camera configs BEFORE reconciliation
            # This ensures removed cameras can be marked as refresh-managed
            old_camera_configs = dict(self.streaming_pipeline.camera_configs) if self.streaming_pipeline else {}

            # Determine changes
            to_remove = current_ids - new_ids
            to_add = new_ids - current_ids
            to_maybe_update = new_ids & current_ids

            # Log reconciliation plan
            self.logger.warning(
                f"Refresh reconciliation plan: "
                f"+{len(to_add)} adds, ~{len(to_maybe_update)} potential updates, "
                f"-{len(to_remove)} removes (event_timestamp={event_timestamp})"
            )

            # Execute full reconciliation on pipeline
            if self.streaming_pipeline:
                result = await self.streaming_pipeline.reconcile_camera_configs(new_camera_configs)

                if result.get("success"):
                    self.logger.info(
                        f"✓ Refresh reconciliation completed: {result['total_cameras']} cameras active "
                        f"(+{result['added']}, ~{result['updated']}, -{result['removed']})"
                    )

                    # Notify monitor to update its cache
                    # CRITICAL: Pass BOTH old and new configs so removed cameras can be tracked
                    if self.camera_config_monitor:
                        try:
                            self.camera_config_monitor.notify_refresh_completed(
                                new_camera_configs=new_camera_configs,
                                old_camera_configs=old_camera_configs
                            )
                            self.logger.info("Notified camera config monitor of refresh completion")
                        except Exception as e:
                            self.logger.warning(f"Failed to notify monitor: {e}")

                    return True
                else:
                    errors = result.get('errors', [])
                    self.logger.error(
                        f"✗ Refresh reconciliation failed: {len(errors)} errors\n"
                        f"Errors: {errors}\n"
                        f"Keeping current configuration"
                    )
                    return False
            else:
                self.logger.error("No streaming pipeline available for reconciliation")
                return False

        except Exception as e:
            self.logger.error(
                f"✗ Exception during camera reconciliation: {e}\n"
                f"Event timestamp: {event_timestamp}\n"
                f"New cameras: {len(new_camera_configs)}\n"
                f"Current cameras: {len(current_ids)}\n"
                f"Keeping current configuration",
                exc_info=True
            )
            return False