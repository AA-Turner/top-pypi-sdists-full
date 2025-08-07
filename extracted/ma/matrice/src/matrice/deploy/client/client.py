"""Module providing client functionality."""

import time
import logging
from typing import Optional, Dict, Union
from matrice.deploy.client.client_utils import ClientUtils
from matrice.deploy.client.client_stream_utils import ClientStreamUtils


class MatriceDeployClient:
    """Client for interacting with Matrice model deployments.

    This client provides both synchronous and asynchronous methods for making
    predictions and streaming video data to deployed models.

    Example:
        Basic usage:
        ```python
        from matrice import Session
        from matrice.deploy.client import MatriceDeployClient

        session = Session(account_number="...", access_key="...", secret_key="...")
        client = MatriceDeployClient(
            session=session,
            deployment_id="your_deployment_id",
            auth_key="your_auth_key"
        )

        # Check if client is healthy
        if client.is_healthy():
            # Make a prediction
            result = client.get_prediction(input_path="image.jpg")
            print(result)

        # Clean up resources
        client.close()
        ```

    Streaming example:
        ```python
        # Start streaming frames from webcam
        success = client.start_stream(input=0, fps=30, quality=80)
        if success:
            # Consume results
            while True:
                result = client.consume_result(timeout=10.0)
                if result:
                    print(f"Received result: {result}")
                else:
                    break

        # Stop streaming
        client.stop_streaming()
        ```

    Video streaming example:
        ```python
        # Start streaming video chunks from webcam (5 second chunks)
        success = client.start_video_stream(
            input=0,
            fps=30,
            video_duration=5.0,  # 5 second chunks
            video_format="mp4"
        )

        # Or stream video with frame count limit (150 frames per chunk)
        success = client.start_video_stream(
            input=0,
            fps=30,
            max_frames=150,  # 150 frames per chunk
            video_format="mp4"
        )

        if success:
            # Consume video results
            while True:
                result = client.consume_result(timeout=30.0)
                if result:
                    print(f"Received video result: {result}")
                else:
                    break

        # Stop streaming
        client.stop_streaming()
        ```
    """

    def __init__(
        self,
        session,
        deployment_id: str,
        auth_key: str = None,
        create_deployment_config: Dict = None,
        consumer_group_id: str = None,
        consumer_group_instance_id: str = None,
    ):
        """Initialize MatriceDeployClient.

        Args:
            session: Session object for making RPC calls
            deployment_id: ID of the deployment
            auth_key: Authentication key
            create_deployment_config: Deployment configuration
            consumer_group_id: Kafka consumer group ID
            consumer_group_instance_id: Unique consumer group instance ID to prevent rebalancing

        Raises:
            ValueError: If required parameters are missing or invalid
            RuntimeError: If deployment info cannot be retrieved
        """
        # Validate required parameters
        if not session:
            raise ValueError("Session is required")
        if not deployment_id or not isinstance(deployment_id, str):
            raise ValueError("deployment_id must be a non-empty string")

        logging.debug(
            "Initializing MatriceDeployClient for deployment %s",
            deployment_id,
        )
        self.session = session
        self.rpc = self.session.rpc
        self.deployment_id = deployment_id
        self.auth_key = auth_key
        self.index_to_category = {}
        self.last_refresh_time = time.time()
        self.create_deployment_config = create_deployment_config

        if not self.deployment_id:
            logging.warning(
                "Deployment ID is not provided, use create_deployment to create a new deployment if config is provided"
            )
            return

        # Initialize utilities first
        self.client_utils = ClientUtils()
        self.client_stream_utils = ClientStreamUtils(
            self.session,
            self.deployment_id,
            consumer_group_id,
            consumer_group_instance_id,
        )

        # Get deployment info and initialize instance variables
        try:
            self.deployment_info = self.get_deployment_info()
            self.model_id = self.deployment_info["model_id"]
            self.model_type = self.deployment_info["model_type"]
            self.instances_info = self.deployment_info["instances_info"]
            self.server_type = self.deployment_info["server_type"]
            self.connection_protocol = self.deployment_info["connection_protocol"]

            # Initialize client utils with instances info
            if self.instances_info:
                self.client_utils.refresh_instances_info(self.instances_info)
            else:
                logging.warning(
                    "No running instances found for deployment %s", deployment_id
                )

        except Exception as exc:
            logging.error("Failed to initialize MatriceDeployClient: %s", str(exc))
            raise RuntimeError(f"Failed to initialize client: {str(exc)}")

        if not self.auth_key:
            logging.warning(
                "No auth key provided, it must be passed in the get_prediction and get_prediction_async methods or use create_auth_key_if_not_exists to create one"
            )

    def create_deployment(
        self,
        deployment_name,
        model_id="",
        gpu_required=True,
        auto_scale=False,
        auto_shutdown=True,
        shutdown_threshold=5,
        compute_alias="",
        model_type="trained",
        deployment_type="regular",
        checkpoint_type="pretrained",
        checkpoint_value="",
        checkpoint_dataset="COCO",
        runtime_framework="Pytorch",
        server_type="fastapi",
        deployment_params={},
        model_input="image",
        model_output="classification",
        suggested_classes=[],
        model_family="",
        model_key="",
        is_kafka_enabled=False,
        is_optimized=False,
        instance_range=[1, 1],
        custom_schedule=False,
        schedule_deployment=[],
        post_processing_config=None,
        create_deployment_config: Dict = {},
        wait_for_deployment: bool = True,
        max_wait_time: int = 1200,
    ):
        from matrice.projects import Projects

        projects = Projects(self.session)
        if not create_deployment_config:
            create_deployment_config = self.create_deployment_config or {}
        deployment_id = projects._create_deployment(
            deployment_name=deployment_name,
            model_id=model_id,
            gpu_required=gpu_required,
            auto_scale=auto_scale,
            auto_shutdown=auto_shutdown,
            shutdown_threshold=shutdown_threshold,
            compute_alias=compute_alias,
            model_type=model_type,
            deployment_type=deployment_type,
            checkpoint_type=checkpoint_type,
            checkpoint_value=checkpoint_value,
            checkpoint_dataset=checkpoint_dataset,
            runtime_framework=runtime_framework,
            server_type=server_type,
            deployment_params=deployment_params,
            model_input=model_input,
            model_output=model_output,
            suggested_classes=suggested_classes,
            model_family=model_family,
            model_key=model_key,
            is_kafka_enabled=is_kafka_enabled,
            is_optimized=is_optimized,
            instance_range=instance_range,
            custom_schedule=custom_schedule,
            schedule_deployment=schedule_deployment,
            post_processing_config=post_processing_config,
            create_deployment_config=create_deployment_config,
            return_id_only=True,
        )
        if wait_for_deployment:
            self.wait_for_deployment(max_wait_time)
        self.__init__(
            session=self.session,
            deployment_id=deployment_id,
        )
        return deployment_id

    def wait_for_deployment(self, timeout=1200):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if self.is_healthy():
                    logging.info("Deployment is ready for streaming")
                    return True

                logging.debug("Deployment not ready yet, waiting...")
                time.sleep(10)

            except Exception as e:
                logging.debug(f"Deployment check failed: {e}")
                time.sleep(10)

        logging.error(f"Deployment not ready after {timeout} seconds")
        return False

    def create_auth_key_if_not_exists(self, expiry_days: int = 30) -> str:
        """Create an authentication key if one doesn't exist.

        Args:
            expiry_days: Number of days until the key expires

        Returns:
            str: The created authentication key

        Raises:
            ValueError: If expiry_days is invalid
            RuntimeError: If key creation fails
        """
        if not isinstance(expiry_days, int) or expiry_days <= 0:
            raise ValueError("expiry_days must be a positive integer")

        try:
            resp = self.rpc.post(
                path=f"/v1/inference/add_auth_key/{self.deployment_id}",
                payload={"expiryDays": expiry_days, "authType": "external"},
            )
            if resp.get("success"):
                self.auth_key = resp["data"]["key"]
                return self.auth_key
            else:
                raise RuntimeError(f"Failed to create auth key: {resp}")
        except Exception as exc:
            logging.error(f"Failed to create auth key: {str(exc)}")
            raise RuntimeError(f"Failed to create auth key: {str(exc)}")

    def get_deployment_info(self) -> Dict:
        """Get deployment information.

        Returns:
            Dict containing deployment information

        Raises:
            RuntimeError: If deployment info cannot be retrieved
        """
        try:
            response = self.rpc.get(
                f"/v1/inference/get_deployment_without_auth_key/{self.deployment_id}"
            )
            if not response.get("success"):
                raise RuntimeError(f"Failed to get deployment info: {response}")

            deployment_info = response["data"]
            model_id = deployment_info["_idModel"]
            model_type = deployment_info["modelType"]
            running_instances = deployment_info["runningInstances"]
            instances_info = [
                {
                    "ip_address": instance["ipAddress"],
                    "port": instance["port"],
                    "instance_id": instance["modelDeployInstanceId"],
                }
                for instance in running_instances
                if instance.get("deployed", False)
            ]
            server_type = deployment_info.get("serverType", "fastapi")
            connection_protocol = "grpc" if "grpc" in server_type.lower() else "rest"
            logging.debug(
                "Successfully fetched deployment info. Found %s running instances",
                len(instances_info),
            )
            return {
                "model_id": model_id,
                "model_type": model_type,
                "instances_info": instances_info,
                "server_type": server_type,
                "connection_protocol": connection_protocol,
            }
        except Exception as exc:
            logging.error(f"Failed to get deployment info: {str(exc)}")
            raise RuntimeError(f"Failed to get deployment info: {str(exc)}")

    def refresh_instances_info(self, force: bool = False):
        """Refresh instances information from the deployment.

        Args:
            force: Whether to force refresh regardless of time elapsed
        """
        current_time = time.time()
        if not force and (current_time - self.last_refresh_time) < 60:  # 5 minutes
            logging.debug("Skipping refresh, last refresh was recent")
            return

        try:
            self.deployment_info = self.get_deployment_info()
            self.instances_info = self.deployment_info["instances_info"]

            if self.instances_info:
                self.client_utils.refresh_instances_info(self.instances_info)
                self.last_refresh_time = current_time
                logging.debug("Successfully refreshed instances info")
            else:
                logging.warning("No running instances found during refresh")
        except Exception as exc:
            logging.error(f"Failed to refresh instances info: {str(exc)}")

    def get_index_to_category(self) -> Dict:
        """Get index to category mapping.

        Returns:
            Dict mapping indices to category names

        Raises:
            RuntimeError: If category mapping cannot be retrieved
        """
        try:
            logging.debug(
                "Getting index to category mapping for model %s",
                self.model_id,
            )
            if self.model_type == "trained":
                url = f"/v1/model/model_train/{self.model_id}"
            elif self.model_type == "exported":
                url = f"/v1/model/get_model_train_by_export_id?exportId={self.model_id}"
            else:
                error_msg = f"Unsupported model type for index to category mapping: {self.model_type}"
                logging.warning(error_msg)
                return {}
            response = self.rpc.get(url)
            if not response.get("data"):
                error_msg = "No data returned from model train endpoint for index to category mapping"
                logging.error(error_msg)
                raise RuntimeError(error_msg)
            model_train_doc = response["data"]
            self.index_to_category = model_train_doc.get("indexToCat", {})
            logging.debug(
                "Successfully fetched index to category mapping with %d categories",
                len(self.index_to_category),
            )
            return self.index_to_category
        except Exception as exc:
            logging.error(f"Failed to get index to category mapping: {str(exc)}")
            # Return empty mapping instead of raising
            self.index_to_category = {}
            return self.index_to_category

    def get_prediction(
        self,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
        auth_key: Optional[str] = None,
        apply_post_processing: bool = False,
    ) -> Union[Dict, str]:
        """Get prediction from the deployed model.

        Args:
            input_path: Path to input file
            input_bytes: Input data as bytes
            input_url: URL to input data
            extra_params: Additional parameters for the prediction
            auth_key: Authentication key (uses instance auth_key if not provided)
            apply_post_processing: Whether to apply post-processing

        Returns:
            Prediction result from the model

        Raises:
            ValueError: If no input is provided or auth key is missing
            Exception: If prediction request fails
        """
        # Use provided auth_key or fall back to instance auth_key
        effective_auth_key = auth_key or self.auth_key

        # Refresh instances if needed
        self.refresh_instances_info()

        return self.client_utils.inference(
            input_path=input_path,
            input_bytes=input_bytes,
            input_url=input_url,
            extra_params=extra_params,
            auth_key=effective_auth_key,
            apply_post_processing=apply_post_processing,
        )

    async def get_prediction_async(
        self,
        input_path: Optional[str] = None,
        input_bytes: Optional[bytes] = None,
        input_url: Optional[str] = None,
        extra_params: Optional[Dict] = None,
        auth_key: Optional[str] = None,
        apply_post_processing: bool = False,
    ) -> Union[Dict, str]:
        """Get prediction from the deployed model asynchronously.

        Args:
            input_path: Path to input file
            input_bytes: Input data as bytes
            input_url: URL to input data
            extra_params: Additional parameters for the prediction
            auth_key: Authentication key (uses instance auth_key if not provided)
            apply_post_processing: Whether to apply post-processing

        Returns:
            Prediction result from the model

        Raises:
            ValueError: If no input is provided or auth key is missing
            Exception: If prediction request fails
        """
        # Use provided auth_key or fall back to instance auth_key
        effective_auth_key = auth_key or self.auth_key

        # Refresh instances if needed
        self.refresh_instances_info()

        return await self.client_utils.async_inference(
            input_path=input_path,
            input_bytes=input_bytes,
            input_url=input_url,
            extra_params=extra_params,
            auth_key=effective_auth_key,
            apply_post_processing=apply_post_processing,
        )

    def start_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> bool:
        """Start a streaming session (blocking).

        Args:
            input: Video source (camera index, file path, or URL)
            fps: Frames per second to stream
            stream_key: Unique identifier for the stream
            quality: JPEG compression quality (1-100)
            width: Target frame width
            height: Target frame height

        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        if not self.client_stream_utils.stream_support:
            logging.error("Streaming not supported for this deployment")
            return False

        return self.client_stream_utils.start_stream(
            input=input,
            fps=fps,
            stream_key=stream_key,
            stream_group_key=stream_group_key,
            quality=quality,
            width=width,
            height=height,
        )

    def start_background_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> bool:
        """Start a background streaming session.

        Args:
            input: Video source (camera index, file path, or URL)
            fps: Frames per second to stream
            stream_key: Unique identifier for the stream
            quality: JPEG compression quality (1-100)
            width: Target frame width
            height: Target frame height

        Returns:
            bool: True if streaming started successfully, False otherwise
        """
        if not self.client_stream_utils.stream_support:
            logging.error("Streaming not supported for this deployment")
            return False

        return self.client_stream_utils.start_background_stream(
            input=input,
            fps=fps,
            stream_key=stream_key,
            stream_group_key=stream_group_key,
            quality=quality,
            width=width,
            height=height,
        )

    def stop_streaming(self) -> None:
        """Stop all streaming sessions."""
        self.client_stream_utils.stop_streaming()

    def consume_result(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume a result from the streaming session.

        Args:
            timeout: Maximum time to wait for a result in seconds

        Returns:
            Result dictionary if available, None if timeout
        """
        return self.client_stream_utils.consume_result(timeout=timeout)

    async def consume_result_async(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume a result from the streaming session asynchronously.

        Args:
            timeout: Maximum time to wait for a result in seconds

        Returns:
            Result dictionary if available, None if timeout
        """
        return await self.client_stream_utils.async_consume_result(timeout=timeout)

    async def close_stream(self) -> None:
        """Close streaming connections asynchronously."""
        await self.client_stream_utils.close()

    def is_healthy(self) -> bool:
        """Check if the deployment is healthy and ready to serve requests.

        Returns:
            bool: True if deployment is healthy, False otherwise
        """
        try:
            # Try to get deployment info as a health check
            self.refresh_instances_info(force=True)
            return len(self.instances_info) > 0
        except Exception as exc:
            logging.error(f"Health check failed: {str(exc)}")
            return False

    def get_status(self) -> Dict:
        """Get comprehensive status information about the client and deployment.

        Returns:
            Dict containing status information
        """
        try:
            self.refresh_instances_info(force=True)

            status = {
                "deployment_id": self.deployment_id,
                "model_id": self.model_id,
                "model_type": self.model_type,
                "server_type": self.server_type,
                "connection_protocol": self.connection_protocol,
                "running_instances": len(self.instances_info),
                "stream_support": self.client_stream_utils.stream_support,
                "has_auth_key": bool(self.auth_key),
                "healthy": len(self.instances_info) > 0,
                "last_refresh": self.last_refresh_time,
            }

            return status
        except Exception as exc:
            logging.error(f"Failed to get status: {str(exc)}")
            return {
                "deployment_id": self.deployment_id,
                "error": str(exc),
                "healthy": False,
            }

    def close(self) -> None:
        """Close all client connections and clean up resources.

        This method should be called when you're done using the client
        to properly clean up HTTP connections and other resources.
        """
        errors = []

        # Close HTTP clients
        try:
            self.client_utils.close()
        except Exception as exc:
            error_msg = f"Error closing client utils: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        # Stop streaming if active
        try:
            self.stop_streaming()
        except Exception as exc:
            error_msg = f"Error stopping streaming: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        if errors:
            error_summary = "; ".join(errors)
            logging.warning("Some errors occurred during cleanup: %s", error_summary)
        else:
            logging.debug("Client cleanup completed successfully")

    async def aclose(self) -> None:
        """Close all client connections asynchronously and clean up resources.

        This method should be called when you're done using the client
        to properly clean up HTTP connections and other resources.
        """
        errors = []

        # Close HTTP clients
        try:
            await self.client_utils.aclose()
        except Exception as exc:
            error_msg = f"Error closing client utils: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        # Close streaming connections
        try:
            await self.close_stream()
        except Exception as exc:
            error_msg = f"Error closing streaming connections: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        if errors:
            error_summary = "; ".join(errors)
            logging.warning(
                "Some errors occurred during async cleanup: %s", error_summary
            )
        else:
            logging.debug("Async client cleanup completed successfully")

    def start_video_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
        video_duration: Optional[float] = None,
        max_frames: Optional[int] = None,
        video_format: str = "mp4",
    ) -> bool:
        """Start a video streaming session (blocking) that sends video chunks.

        Args:
            input: Video source (camera index, file path, or URL)
            fps: Frames per second to capture and encode
            stream_key: Unique identifier for the stream
            quality: Video compression quality (1-100)
            width: Target frame width
            height: Target frame height
            video_duration: Duration of each video chunk in seconds (optional)
            max_frames: Maximum number of frames per video chunk (optional)
            video_format: Video format for encoding ('mp4', 'avi', 'webm')

        Returns:
            bool: True if streaming started successfully, False otherwise

        Note:
            Either video_duration or max_frames should be specified to control chunk size.
            If neither is provided, defaults to 5 second chunks.
        """
        if not self.client_stream_utils.stream_support:
            logging.error("Streaming not supported for this deployment")
            return False

        return self.client_stream_utils.start_video_stream(
            input=input,
            fps=fps,
            stream_key=stream_key,
            quality=quality,
            width=width,
            height=height,
            video_duration=video_duration,
            max_frames=max_frames,
            video_format=video_format,
        )

    def start_background_video_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
        video_duration: Optional[float] = None,
        max_frames: Optional[int] = None,
        video_format: str = "mp4",
    ) -> bool:
        """Start a background video streaming session that sends video chunks.

        Args:
            input: Video source (camera index, file path, or URL)
            fps: Frames per second to capture and encode
            stream_key: Unique identifier for the stream
            quality: Video compression quality (1-100)
            width: Target frame width
            height: Target frame height
            video_duration: Duration of each video chunk in seconds (optional)
            max_frames: Maximum number of frames per video chunk (optional)
            video_format: Video format for encoding ('mp4', 'avi', 'webm')

        Returns:
            bool: True if streaming started successfully, False otherwise

        Note:
            Either video_duration or max_frames should be specified to control chunk size.
            If neither is provided, defaults to 5 second chunks.
        """
        if not self.client_stream_utils.stream_support:
            logging.error("Streaming not supported for this deployment")
            return False

        return self.client_stream_utils.start_background_video_stream(
            input=input,
            fps=fps,
            stream_key=stream_key,
            quality=quality,
            width=width,
            height=height,
            video_duration=video_duration,
            max_frames=max_frames,
            video_format=video_format,
        )
