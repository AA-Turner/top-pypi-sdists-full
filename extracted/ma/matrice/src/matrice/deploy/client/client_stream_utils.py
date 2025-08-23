import base64
import logging
import cv2
import threading
import time
import hashlib
import numpy as np
from datetime import datetime, timezone
from typing import Dict, Optional, Union, Tuple, Any
from matrice.deploy.stream.kafka_stream import MatriceKafkaDeployment
from matrice.deploy.optimize.transmission import ClientTransmissionHandler


class ClientStreamUtils:
    def __init__(
        self,
        session,
        service_id: str,
        consumer_group_id: str = None,
        consumer_group_instance_id: str = None,
        threshold_a: float = 0.95,
        threshold_b: float = 0.85,
        enable_intelligent_transmission: bool = False,
    ):
        """Initialize ClientStreamUtils.

        Args:
            session: Session object for making RPC calls
            service_id: ID of the deployment
            consumer_group_id: Kafka consumer group ID
            consumer_group_instance_id: Unique consumer group instance ID to prevent rebalancing
            threshold_a: High similarity threshold for skipping transmission (default: 0.95)
            threshold_b: Medium similarity threshold for difference transmission (default: 0.85)
            enable_intelligent_transmission: Whether to enable intelligent frame transmission
        """
        self.streaming_threads = []
        self.session = session
        self.service_id = service_id
        self.kafka_deployment = MatriceKafkaDeployment(
            self.session,
            self.service_id,
            "client",
            consumer_group_id,
            consumer_group_instance_id,
        )
        self.stream_support = self.kafka_deployment.setup_success
        self.input_order = {}  # Dictionary to track input counter for each stream key
        self._stop_streaming = False
        self.video_start_times = {}  # Track video start times for timestamp calculation

        # Intelligent transmission components
        self.enable_intelligent_transmission = enable_intelligent_transmission
        self.threshold_a = threshold_a
        self.threshold_b = threshold_b
        self.txh = ClientTransmissionHandler(
            threshold_a=threshold_a, threshold_b=threshold_b
        )

        # Transmission statistics
        self.frames_sent = 0
        self.frames_skipped = 0
        self.frames_diff_sent = 0
        self.bytes_saved = 0

    def _determine_transmission_strategy(
        self, frame: np.ndarray, stream_key: str
    ) -> Tuple[str, Dict]:
        if not self.enable_intelligent_transmission:
            self.txh.frame_cache[stream_key] = frame.copy()
            return "full", {"reason": "intelligent_disabled"}
        return self.txh.decide_transmission(frame, stream_key)

    def _validate_stream_params(
        self, fps: int, quality: int, width: Optional[int], height: Optional[int]
    ) -> bool:
        """Validate common streaming parameters."""
        if fps <= 0:
            logging.error("FPS must be positive")
            return False
        if quality < 1 or quality > 100:
            logging.error("Quality must be between 1 and 100")
            return False
        if width is not None and width <= 0:
            logging.error("Width must be positive")
            return False
        if height is not None and height <= 0:
            logging.error("Height must be positive")
            return False
        return True

    def _check_stream_support(self) -> bool:
        """Check if streaming is supported."""
        if not self.stream_support:
            logging.error(
                "Kafka stream support not available, Please check if Kafka is enabled in the deployment and reinitialize the client"
            )
            return False
        return True

    def _setup_video_capture(
        self, input: Union[str, int], width: Optional[int], height: Optional[int]
    ) -> Tuple[cv2.VideoCapture, str]:
        """Set up video capture with proper configuration."""
        stream_type = "unknown"
        # Handle different input types
        if isinstance(input, int) or (isinstance(input, str) and input.isdigit()):
            cap = cv2.VideoCapture(int(input) if isinstance(input, str) else input)
            logging.info(f"Opening webcam device: {input}")
            stream_type = "camera"
        elif isinstance(input, str) and input.startswith("rtsp"):
            cap = cv2.VideoCapture(input)
            logging.info(f"Opening RTSP stream: {input}")
            stream_type = "rtsp"
        elif isinstance(input, str) and input.startswith("http"):
            cap = cv2.VideoCapture(input)
            logging.info(f"Opening HTTP stream: {input}")
            stream_type = "http"
        else:
            cap = cv2.VideoCapture(input)
            logging.info(f"Opening video source: {input}")
            stream_type = "video_file"

        if not cap.isOpened():
            logging.error(f"Failed to open video source: {input}")
            raise RuntimeError(f"Failed to open video source: {input}")

        # Set properties for cameras and RTSP streams
        if isinstance(input, int) or (isinstance(input, str) and input.isdigit()):
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffering for real-time
            if width is not None:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            if height is not None:
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        elif isinstance(input, str) and input.startswith("rtsp"):
            # For RTSP streams, set minimal buffer to prevent frame accumulation
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        return cap, stream_type

    def _get_video_properties(self, cap: cv2.VideoCapture) -> Dict:
        """Get video properties from capture object."""
        return {
            "original_fps": float(round(cap.get(cv2.CAP_PROP_FPS), 2)),
            "frame_count": cap.get(cv2.CAP_PROP_FRAME_COUNT),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }

    def _get_high_precision_timestamp(self) -> str:
        """Get high precision timestamp with microsecond granularity."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    def _calculate_video_timestamp(
        self, stream_key: str, frame_number: int, fps: float
    ) -> str:
        """Calculate video timestamp from start of video.

        The timestamp is returned in human-readable ``HH:MM:SS:mmm`` format
        where *mmm* represents milliseconds.  This makes it easier to locate
        frames in recordings that are longer than 60 seconds.
        """
        # Lazily initialise the start-time dictionary to keep backward
        # compatibility even though it is no longer used for formatting.
        if stream_key not in self.video_start_times:
            self.video_start_times[stream_key] = time.time()

        # Calculate the elapsed time in seconds since the beginning of the
        # video based solely on frame number and FPS.
        total_seconds = frame_number / fps if fps else 0.0

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int(round((total_seconds - int(total_seconds)) * 1000))

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

    def _handle_frame_read_failure(
        self,
        input: Union[str, int],
        cap: cv2.VideoCapture,
        retry_count: int,
        max_retries: int,
        width: Optional[int],
        height: Optional[int],
        simulate_video_file_stream: bool = False,
    ) -> Tuple[cv2.VideoCapture, int]:
        """Handle frame read failures with retry logic."""
        if retry_count >= max_retries:
            if isinstance(input, int) or (isinstance(input, str) and input.isdigit()):
                # For cameras, try to reopen
                logging.info("Attempting to reopen camera...")
                cap.release()
                time.sleep(1)  # Give camera time to reset
                cap = cv2.VideoCapture(int(input) if isinstance(input, str) else input)
                if not cap.isOpened():
                    raise RuntimeError("Failed to reopen camera")
                # Reapply resolution settings
                if width is not None:
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                if height is not None:
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                return cap, 0  # Reset retry count
            else:
                # For video files, check if we should restart or stop
                if simulate_video_file_stream:
                    logging.info(
                        f"End of video file reached, restarting from beginning: {input}"
                    )
                    cap.release()
                    time.sleep(10)  # Brief pause before reopening
                    cap = cv2.VideoCapture(input)
                    if not cap.isOpened():
                        raise RuntimeError(f"Failed to reopen video file: {input}")
                    return cap, 0  # Reset retry count
                else:
                    # Normal behavior - end of stream
                    logging.info(f"End of stream reached for input: {input}")
                    raise StopIteration("End of stream reached")

        time.sleep(0.1)  # Short delay before retry
        return cap, retry_count

    def _resize_frame_if_needed(
        self, frame, width: Optional[int], height: Optional[int]
    ):
        """Resize frame if dimensions are specified and different from current."""
        if width is not None or height is not None:
            current_height, current_width = frame.shape[:2]
            target_width = width if width is not None else current_width
            target_height = height if height is not None else current_height

            if target_width != current_width or target_height != current_height:
                frame = cv2.resize(frame, (target_width, target_height))
        return frame

    def _get_next_input_order(self, stream_key: Optional[str]) -> int:
        """Get the next input order for a given stream key."""
        key = stream_key if stream_key is not None else "default"
        if key not in self.input_order:
            self.input_order[key] = 0
        self.input_order[key] += 1
        return self.input_order[key]

    def _get_video_format(self, input: Union[str, int]) -> str:
        """Get video format extension from input."""
        if isinstance(input, str) and "." in input:
            return "." + input.split("?")[0].split(".")[-1].lower()
        return ".mp4"

    def _calculate_frame_skip(self, original_fps: float, target_fps: int) -> int:
        """Calculate how many frames to skip for RTSP streams to achieve target FPS."""
        if original_fps <= 0 or target_fps <= 0:
            return 1

        frame_skip = max(1, int(original_fps / target_fps))
        logging.info(
            f"Original FPS: {original_fps}, Target FPS: {target_fps}, Frame skip: {frame_skip}"
        )
        return frame_skip

    # Removed: metadata building is centralized in ClientTransmissionHandler

    def start_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
        simulate_video_file_stream: bool = False,
        is_video_chunk: bool = False,
        chunk_duration_seconds: Optional[float] = None,
        chunk_frames: Optional[int] = None,
        camera_location: Optional[str] = None,
    ) -> bool:
        """Start a stream input to the Kafka stream in the current thread.
        
        Args:
            input: Video input source (camera index, file path, or URL)
            fps: Target frames per second
            stream_key: Unique identifier for this stream
            stream_group_key: Group identifier for this stream
            quality: JPEG compression quality (1-100)
            width: Target frame width (optional)
            height: Target frame height (optional)
            simulate_video_file_stream: Whether to simulate video file as stream
            is_video_chunk: Whether to send video chunks instead of frames
            chunk_duration_seconds: Duration of video chunks in seconds
            chunk_frames: Maximum number of frames per chunk
            camera_location: Physical location of the camera (e.g., "Building A, Floor 2, Room 205")
        """
        if not self._check_stream_support():
            return False

        if not self._validate_stream_params(fps, quality, width, height):
            return False

        try:
            self._stream_inputs(
                input=input,
                fps=fps,
                stream_key=stream_key,
                stream_group_key=stream_group_key,
                quality=quality,
                width=width,
                height=height,
                simulate_video_file_stream=simulate_video_file_stream,
                is_video_chunk=is_video_chunk,
                chunk_duration_seconds=chunk_duration_seconds,
                chunk_frames=chunk_frames,
                camera_location=camera_location,
            )
            return True
        except Exception as exc:
            logging.error("Failed to start streaming: %s", str(exc))
            return False
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt, stopping streaming")
            self.stop_streaming()
            return False

    def start_background_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
        simulate_video_file_stream: bool = False,
        is_video_chunk: bool = False,
        chunk_duration_seconds: Optional[float] = None,
        chunk_frames: Optional[int] = None,
        camera_location: Optional[str] = None,
    ) -> bool:
        """Start a stream input to the Kafka stream in a background thread.
        
        Args:
            input: Video input source (camera index, file path, or URL)
            fps: Target frames per second
            stream_key: Unique identifier for this stream
            stream_group_key: Group identifier for this stream
            quality: JPEG compression quality (1-100)
            width: Target frame width (optional)
            height: Target frame height (optional)
            simulate_video_file_stream: Whether to simulate video file as stream
            is_video_chunk: Whether to send video chunks instead of frames
            chunk_duration_seconds: Duration of video chunks in seconds
            chunk_frames: Maximum number of frames per chunk
            camera_location: Physical location of the camera (e.g., "Building A, Floor 2, Room 205")
        """
        if not self._check_stream_support():
            return False

        if not self._validate_stream_params(fps, quality, width, height):
            return False

        try:
            thread = threading.Thread(
                target=self._stream_inputs,
                args=(
                    input,
                    fps,
                    stream_key,
                    stream_group_key,
                    quality,
                    width,
                    height,
                    simulate_video_file_stream,
                    is_video_chunk,
                    chunk_duration_seconds,
                    chunk_frames,
                    camera_location,
                ),
                daemon=True,
            )
            self.streaming_threads.append(thread)
            thread.start()
            return True
        except Exception as exc:
            logging.error("Failed to start streaming thread: %s", str(exc))
            return False

    def _stream_inputs(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
        simulate_video_file_stream: bool = False,
        is_video_chunk: bool = False,
        chunk_duration_seconds: Optional[float] = None,
        chunk_frames: Optional[int] = None,
        camera_location: Optional[str] = None,
    ) -> None:
        """Stream inputs from a video source to Kafka."""
        quality = max(1, min(100, quality))
        cap = None

        try:
            cap, stream_type = self._setup_video_capture(input, width, height)
            # Get video properties including original FPS
            video_props = self._get_video_properties(cap)

            actual_width = video_props["width"]
            actual_height = video_props["height"]
            # Override with specified dimensions if provided
            if width is not None:
                actual_width = width
            if height is not None:
                actual_height = height

            # Calculate frame skip for RTSP streams to handle high FPS sources
            frame_skip = 1
            is_rtsp_stream = isinstance(input, str) and input.startswith("rtsp")
            if is_rtsp_stream and video_props["original_fps"] > fps:
                frame_skip = self._calculate_frame_skip(
                    video_props["original_fps"], fps
                )

            retry_count = 0
            max_retries = 3
            consecutive_failures = 0
            max_consecutive_failures = 10
            frame_counter = 0
            processed_frame_counter = 0

            while not self._stop_streaming:
                start_time = time.time()
                ret, frame = cap.read()

                if not ret:
                    retry_count += 1
                    consecutive_failures += 1
                    logging.warning(
                        f"Failed to read frame, retry {retry_count}/{max_retries}"
                    )

                    if consecutive_failures >= max_consecutive_failures:
                        logging.error("Too many consecutive failures, stopping stream")
                        break

                    try:
                        cap, retry_count = self._handle_frame_read_failure(
                            input,
                            cap,
                            retry_count,
                            max_retries,
                            width,
                            height,
                            simulate_video_file_stream,
                        )
                    except (RuntimeError, StopIteration):
                        break
                    continue

                # Reset counters on successful frame read
                retry_count = 0
                consecutive_failures = 0
                frame_counter += 1

                # For RTSP streams, use frame skipping instead of time delays
                if is_rtsp_stream:
                    # Process only every Nth frame to achieve target FPS
                    if frame_counter % frame_skip != 0:
                        continue
                    processed_frame_counter += 1
                else:
                    processed_frame_counter = frame_counter

                # Resize frame if needed
                frame = self._resize_frame_if_needed(frame, width, height)

                # Prepare payload and metadata via transmission handler
                try:
                    input_bytes, frame_metadata, strategy = (
                        self.txh.prepare_transmission(
                            frame,
                            stream_key=stream_key or "default",
                            input_source=input,
                            video_props=video_props,
                            fps=fps,
                            quality=quality,
                            actual_width=actual_width,
                            actual_height=actual_height,
                            stream_type=stream_type,
                            frame_counter=processed_frame_counter,
                            is_video_chunk=is_video_chunk,
                            chunk_duration_seconds=chunk_duration_seconds,
                            chunk_frames=chunk_frames,
                            camera_location=camera_location,
                        )
                    )
                except Exception as exc:
                    logging.error(f"Transmission preparation failed: {exc}")
                    continue

                # Update simple counters
                if strategy == "skip":
                    self.frames_skipped += 1
                elif strategy == "difference":
                    self.frames_diff_sent += 1

                # Produce
                if self.produce_request(
                    input_bytes,
                    stream_key,
                    stream_group_key,
                    metadata=frame_metadata,
                ):
                    if strategy == "full":
                        self.frames_sent += 1
                else:
                    logging.warning("Failed to produce to Kafka stream")

                # For non-RTSP streams, maintain desired FPS with time delays
                if not is_rtsp_stream:
                    frame_interval = 1.0 / fps
                    processing_time = time.time() - start_time
                    sleep_time = max(0, frame_interval - processing_time)
                    if sleep_time > 0:
                        time.sleep(sleep_time)

        except Exception as exc:
            logging.error(f"Error in streaming thread: {str(exc)}")
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt, stopping streaming")
        finally:
            if cap is not None:
                cap.release()
                logging.info(f"Released video source: {input}")

    def _construct_input_stream(
        self,
        input_data: bytes,
        metadata: Dict = {},
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
    ) -> Dict:
        """Construct the input stream dictionary."""
        if not input_data and (metadata or {}).get("transmission_strategy") != "skip":
            logging.error("Input data cannot be empty (except for skip strategy)")
            return {}

        stream_info = {
            "broker": self.kafka_deployment.bootstrap_server,
            "topic": self.kafka_deployment.request_topic,
            "stream_time": self._get_high_precision_timestamp(),
        }

        input_stream = {
            "ip_key_name": self.service_id,
            "stream_info": stream_info,
            "feed_type": (
                "disk" if metadata.get("stream_type") == "video_file" else "camera"
            ),
            "original_fps": metadata.get("original_fps", metadata.get("fps", 30.0)),
            "stream_fps": metadata.get("fps", 30.0),
            "stream_unit": (
                "segment" if metadata.get("is_video_chunk", False) else "frame"
            ),
            "input_order": self._get_next_input_order(stream_key),
            "frame_count": (
                1
                if not metadata.get("is_video_chunk", False)
                else int(
                    metadata.get("chunk_duration_seconds", 1.0)
                    * metadata.get("fps", 30)
                )
            ),
            "start_frame": metadata.get("start_frame"),
            "end_frame": metadata.get("end_frame"),
            "video_codec": "h264",
            "bw_opt_alg": None,
            "original_resolution": {
                "width": metadata.get("width", 1024),
                "height": metadata.get("height", 1080),
            },
            "stream_resolution": {
                "width": metadata.get("width", 1024),
                "height": metadata.get("height", 1080),
            },
            "camera_info": {
                "camera_name": stream_key,
                "camera_group": stream_group_key,
                "location": metadata.get("camera_location", "Unknown Location")
                },
            "latency_stats": {
                "last_read_time_sec": "TODO",
                "last_write_time_sec": "TODO",
                "last_process_time_sec": "TODO",
            },
            "content": (
                base64.b64encode(input_data).decode("utf-8") if input_data else ""
            ),
            "input_hash": (
                hashlib.md5(input_data, usedforsecurity=False).hexdigest()
                if input_data
                else None
            ),
        }
        # Pass through selected metadata fields to server for intelligent transmission/caching
        passthrough_keys = {
            "transmission_strategy",
            "similarity_score",
            "skip_reason",
            "difference_metadata",
            "video_timestamp",
            "video_properties",
            "frame_sample_rate",
            "is_video_chunk",
            "chunk_duration_seconds",
            "video_format",
            "stream_type",
            "reference_input_hash",
        }
        for k, v in (metadata or {}).items():
            if k in passthrough_keys and v is not None:
                input_stream[k] = v

        return {
            "input_name": f"{input_stream['stream_unit']}_{input_stream['input_order']}",
            "input_unit": input_stream["stream_unit"],
            "input_stream": input_stream,
        }

    def produce_request(
        self,
        input_data: bytes,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        metadata: Optional[Dict] = None,
        timeout: float = 60.0,
    ) -> bool:
        """Simple function to produce a stream request to Kafka."""
        try:
            message = self._construct_input_stream(
                input_data, metadata or {}, stream_key, stream_group_key
            )
            self.kafka_deployment.produce_message(
                message, timeout=timeout, key=stream_key
            )
            return True
        except Exception as exc:
            logging.error("Failed to produce request: %s", str(exc))
            return False

    def consume_result(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume the Kafka stream result."""
        try:
            return self.kafka_deployment.consume_message(timeout)
        except Exception as exc:
            logging.error("Failed to consume Kafka stream result: %s", str(exc))
            return None

    async def async_produce_request(
        self,
        input_data: bytes,
        stream_key: Optional[str] = None,
        stream_group_key: Optional[str] = None,
        metadata: Optional[Dict] = None,
        timeout: float = 60.0,
    ) -> bool:
        """Produce a unified stream request to Kafka asynchronously."""
        try:
            message = self._construct_input_stream(
                input_data, metadata or {}, stream_key, stream_group_key
            )
            await self.kafka_deployment.async_produce_message(
                message=message, timeout=timeout, key=stream_key
            )
            return True
        except Exception as exc:
            logging.error(
                "Failed to add request to Kafka stream asynchronously: %s", str(exc)
            )
            return False

    async def async_consume_result(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume the Kafka stream result asynchronously."""
        try:
            return await self.kafka_deployment.async_consume_message(timeout)
        except Exception as exc:
            logging.error(
                "Failed to consume Kafka stream result asynchronously: %s", str(exc)
            )
            return None

    def stop_streaming(self) -> None:
        """Stop all streaming threads."""
        self._stop_streaming = True
        for thread in self.streaming_threads:
            if thread.is_alive():
                thread.join(timeout=2.0)
        self.streaming_threads = []
        self._stop_streaming = False
        logging.info("All streaming threads stopped")

    def get_transmission_stats(self) -> Dict[str, Any]:
        """Get intelligent transmission statistics.

        Returns:
            Dictionary with transmission statistics
        """
        total_frames = self.frames_sent + self.frames_skipped + self.frames_diff_sent
        skip_rate = (self.frames_skipped / total_frames) if total_frames > 0 else 0.0
        diff_rate = (self.frames_diff_sent / total_frames) if total_frames > 0 else 0.0
        full_rate = (self.frames_sent / total_frames) if total_frames > 0 else 0.0

        return {
            "frames_sent_full": self.frames_sent,
            "frames_skipped": self.frames_skipped,
            "frames_diff_sent": self.frames_diff_sent,
            "total_frames_processed": total_frames,
            "skip_rate": skip_rate,
            "diff_rate": diff_rate,
            "full_rate": full_rate,
            "bytes_saved": self.bytes_saved,
            "intelligent_transmission_enabled": self.enable_intelligent_transmission,
            "threshold_a": self.threshold_a,
            "threshold_b": self.threshold_b,
            "cached_streams": len(self.txh.frame_cache),
        }

    def reset_transmission_stats(self) -> None:
        """Reset transmission statistics."""
        self.frames_sent = 0
        self.frames_skipped = 0
        self.frames_diff_sent = 0
        self.bytes_saved = 0
        # Clear frame cache to prevent memory leaks
        if self.txh:
            self.txh.frame_cache.clear()
            self.txh.last_frame_hashes.clear()
        logging.info("Reset transmission statistics and cleared frame cache")

    async def close(self) -> None:
        """Close all client connections including Kafka stream."""
        errors = []

        # Stop all streaming threads
        try:
            self.stop_streaming()
        except Exception as exc:
            error_msg = f"Error stopping streaming threads: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        # Try to close Kafka connections
        try:
            await self.kafka_deployment.close()
            logging.info("Successfully closed Kafka connections")
        except Exception as exc:
            error_msg = f"Error closing Kafka connections: {str(exc)}"
            logging.error(error_msg)
            errors.append(error_msg)

        # Report all errors if any occurred
        if errors:
            error_summary = "\n".join(errors)
            logging.error("Errors occurred during close: %s", error_summary)
