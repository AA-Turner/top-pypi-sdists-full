from typing import Dict, Optional, Union
import base64
import logging
import cv2
import threading
import time
import tempfile
import os
from datetime import datetime, timezone
from matrice.deploy.utils.kafka_utils import MatriceKafkaDeployment


class ClientStreamUtils:
    def __init__(
        self,
        session,
        deployment_id: str,
        consumer_group_id: str = None,
        consumer_group_instance_id: str = None,
    ):
        """Initialize ClientStreamUtils.

        Args:
            session: Session object for making RPC calls
            deployment_id: ID of the deployment
            consumer_group_id: Kafka consumer group ID
            consumer_group_instance_id: Unique consumer group instance ID to prevent rebalancing
        """
        self.streaming_threads = []
        self.session = session
        self.deployment_id = deployment_id
        self.kafka_deployment = MatriceKafkaDeployment(
            self.session,
            self.deployment_id,
            "client",
            consumer_group_id,
            consumer_group_instance_id,
        )
        self.stream_support = self.kafka_deployment.setup_success
        self.input_order = {}  # Dictionary to track input counter for each stream key
        self._stop_streaming = False
        self.video_start_times = {}  # Track video start times for timestamp calculation

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
    ) -> cv2.VideoCapture:
        """Set up video capture with proper configuration."""
        stream_type = "unknown"
        # Handle different input types
        if isinstance(input, int) or (isinstance(input, str) and input.isdigit()):
            cap = cv2.VideoCapture(int(input) if isinstance(input, str) else input)
            logging.info(f"Opening webcam device: {input}")
            stream_type = "camera"
        else:
            cap = cv2.VideoCapture(input)
            logging.info(f"Opening video source: {input}")
            stream_type = "video_file"

        if not cap.isOpened():
            logging.error(f"Failed to open video source: {input}")
            raise RuntimeError(f"Failed to open video source: {input}")

        # Set properties for cameras
        if isinstance(input, int) or (isinstance(input, str) and input.isdigit()):
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffering for real-time
            if width is not None:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            if height is not None:
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        return cap, stream_type

    def _get_video_properties(self, cap: cv2.VideoCapture) -> Dict:
        """Get video properties including original FPS."""
        properties = {
            "original_fps": float(round(cap.get(cv2.CAP_PROP_FPS),2)),
            "frame_count": cap.get(cv2.CAP_PROP_FRAME_COUNT),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }
        return properties

    def _get_high_precision_timestamp(self) -> str:
        """Get high precision timestamp with microsecond granularity."""
        return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

    def _calculate_video_timestamp(self, stream_key: str, frame_number: int, fps: float) -> str:
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
        self, input: Union[str, int], cap: cv2.VideoCapture, retry_count: int, max_retries: int,
        width: Optional[int], height: Optional[int]
    ) -> tuple[cv2.VideoCapture, int]:
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
                # For video files, we've reached the end
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

    def _get_input_filename(self, input: Union[str, int]) -> Optional[str]:
        """Extract filename from input path."""
        if isinstance(input, str) and not input.isdigit():
            return os.path.basename(input)
        return None

    def start_stream(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> bool:
        """Start a stream input to the Kafka stream."""
        if not self._check_stream_support():
            return False
        
        if not self._validate_stream_params(fps, quality, width, height):
            return False
            
        try:
            self._stream_inputs(input, fps, stream_key, quality, width, height)
            return True
        except Exception as exc:
            logging.error("Failed to start streaming thread: %s", str(exc))
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
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> bool:
        """Add a stream input to the Kafka stream."""
        if not self._check_stream_support():
            return False
        
        if not self._validate_stream_params(fps, quality, width, height):
            return False
            
        try:
            thread = threading.Thread(
                target=self._stream_inputs,
                args=(input, fps, stream_key, quality, width, height),
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
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Stream inputs from a video source to Kafka."""
        quality = max(1, min(100, quality))
        cap = None
        
        try:
            cap, stream_type = self._setup_video_capture(input, width, height)
            # Get video properties including original FPS
            video_props = self._get_video_properties(cap)
            original_fps = video_props["original_fps"]

            actual_width = video_props["width"]
            actual_height = video_props["height"]
            # Override with specified dimensions if provided
            if width is not None:
                actual_width = width
            if height is not None:
                actual_height = height

            retry_count = 0
            max_retries = 3
            consecutive_failures = 0
            max_consecutive_failures = 10
            frame_interval = 1.0 / fps
            frame_counter = 0

            while not self._stop_streaming:
                start_time = time.time()
                ret, frame = cap.read()

                if not ret:
                    retry_count += 1
                    consecutive_failures += 1
                    logging.warning(f"Failed to read frame, retry {retry_count}/{max_retries}")

                    if consecutive_failures >= max_consecutive_failures:
                        logging.error("Too many consecutive failures, stopping stream")
                        break

                    try:
                        cap, retry_count = self._handle_frame_read_failure(
                            input, cap, retry_count, max_retries, width, height
                        )
                    except (RuntimeError, StopIteration):
                        break
                    continue

                # Reset counters on successful frame read
                retry_count = 0
                consecutive_failures = 0
                frame_counter += 1

                # Resize frame if needed
                frame = self._resize_frame_if_needed(frame, width, height)

                # Encode frame
                try:
                    encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
                    _, buffer = cv2.imencode(".jpg", frame, encode_params)
                except Exception as encode_exc:
                    logging.warning(f"Failed to encode frame with quality {quality}, using default: {encode_exc}")
                    try:
                        _, buffer = cv2.imencode(".jpg", frame)
                    except Exception as fallback_exc:
                        logging.error(f"Failed to encode frame even with default settings: {fallback_exc}")
                        continue

                # Calculate video timestamp for this frame
                video_timestamp = self._calculate_video_timestamp(
                    stream_key or "default", frame_counter, original_fps
                )
                video_format = self._get_input_filename(input)
                if isinstance(video_format, str) and '.' in video_format:
                    video_format = '.'+video_format.split('.')[-1].lower()
                else:
                    video_format = '..mp4'
                
                # Prepare enhanced metadata for this frame
                frame_metadata = {
                    "fps": fps,
                    "original_fps": original_fps,  # For live streams, original FPS is the same as processing FPS
                    "frame_sample_rate": 1.0,  # For individual frames, sample rate is 1:1
                    "stream_time": self._get_high_precision_timestamp(),  # Use high precision timestamp
                    "video_timestamp": video_timestamp,  # Added video timestamp
                    "video_file": self._get_input_filename(input),
                    "camera_id": input if isinstance(input, int) or (isinstance(input, str) and input.isdigit()) else None,
                    "location_info": None,  # Can be enhanced later
                    "start_frame": frame_counter,
                    "end_frame": frame_counter,
                    "quality": quality,
                    "width": actual_width,
                    "height": actual_height,
                    "is_video_chunk": False,  # Flag to indicate this is a single frame
                    "chunk_duration_seconds": 1.0 / fps,  # Duration of single frame
                    "video_properties": video_props,
                    "video_format": video_format,
                    "stream_type": stream_type,  # Added stream type
                }
                
                if not self.produce_request(buffer.tobytes(), stream_key, metadata=frame_metadata):
                    logging.warning("Failed to produce frame to Kafka stream")

                # Maintain desired FPS
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

    def stop_streaming(self) -> None:
        """Stop all streaming threads."""
        self._stop_streaming = True
        for thread in self.streaming_threads:
            if thread.is_alive():
                thread.join(timeout=2.0)
        self.streaming_threads = []
        self._stop_streaming = False
        logging.info("All streaming threads stopped")

    def produce_request(
        self, input: bytes, stream_key: Optional[str] = None, timeout: float = 60.0, metadata: Optional[Dict] = None
    ) -> bool:
        """Add a message to the Kafka stream."""
        if not input:
            logging.error("Input cannot be empty")
            return False
            
        try:
            # Get input counter if not provided in metadata
            if metadata is None:
                metadata = {}
            
            # Enhanced metadata for the new output format
            enhanced_metadata = {
                "stream_info": {
                    "fps": metadata.get("fps", 30),
                    "original_fps": metadata.get("original_fps", metadata.get("fps", 30)),  # Added original FPS
                    "frame_sample_rate": metadata.get("frame_sample_rate", 1.0),  # Added frame sample rate
                    "stream_time": metadata.get("stream_time", self._get_high_precision_timestamp()),  # Use high precision timestamp
                    "video_timestamp": metadata.get("video_timestamp", 0.0),  # Added video timestamp
                    "input_settings": {
                        "video_file": metadata.get("video_file"),
                        "camera_id": metadata.get("camera_id"),
                        "location_info": metadata.get("location_info"),
                        "start_frame": metadata.get("start_frame"),
                        "end_frame": metadata.get("end_frame"),
                        "quality": metadata.get("quality"),
                        "width": metadata.get("width"),
                        "height": metadata.get("height"),
                        "stream_key": stream_key,
                        "is_video_chunk": metadata.get("is_video_chunk", False),  # Added video chunk flag
                        "chunk_duration_seconds": metadata.get("chunk_duration_seconds", 0.0),  # Added chunk duration
                        "video_format": metadata.get("video_format"),  # Added video format
                        "video_properties": metadata.get("video_properties", {}),  # Added video properties
                        "stream_type": metadata.get("stream_type"),  # Added stream type
                    }
                },
                **metadata  # Include any additional metadata
            }
            
            message = {
                "input": base64.b64encode(input).decode("utf-8"),
                "input_order": self._get_next_input_order(stream_key),
                "stream_key": stream_key,
                "metadata": enhanced_metadata
            }
            self.kafka_deployment.produce_message(
                message, timeout=timeout, key=stream_key
            )
            return True
        except Exception as exc:
            logging.error("Failed to add request to Kafka stream: %s", str(exc))
            return False

    def consume_result(self, timeout: float = 60.0) -> Optional[Dict]:
        """Consume the Kafka stream result."""
        try:
            return self.kafka_deployment.consume_message(timeout)
        except Exception as exc:
            logging.error("Failed to consume Kafka stream result: %s", str(exc))
            return None

    async def async_produce_request(
        self, input: bytes, stream_key: Optional[str] = None, timeout: float = 60.0, metadata: Optional[Dict] = None
    ) -> bool:
        """Add a message to the Kafka stream asynchronously."""
        if not input:
            logging.error("Input cannot be empty")
            return False
            
        try:
            # Get input counter if not provided in metadata
            if metadata is None:
                metadata = {}

            # Enhanced metadata for the new output format
            enhanced_metadata = {
                "stream_info": {
                    "fps": metadata.get("fps", 30),
                    "original_fps": metadata.get("original_fps", metadata.get("fps", 30)),  # Added original FPS
                    "frame_sample_rate": metadata.get("frame_sample_rate", 1.0),  # Added frame sample rate
                    "stream_time": metadata.get("stream_time", self._get_high_precision_timestamp()),  # Use high precision timestamp
                    "video_timestamp": metadata.get("video_timestamp", 0.0),  # Added video timestamp
                    "input_settings": {
                        "video_file": metadata.get("video_file"),
                        "camera_id": metadata.get("camera_id"),
                        "location_info": metadata.get("location_info"),
                        "start_frame": metadata.get("start_frame"),
                        "end_frame": metadata.get("end_frame"),
                        "quality": metadata.get("quality"),
                        "width": metadata.get("width"),
                        "height": metadata.get("height"),
                        "stream_key": stream_key,
                        "is_video_chunk": metadata.get("is_video_chunk", False),  # Added video chunk flag
                        "chunk_duration_seconds": metadata.get("chunk_duration_seconds", 0.0),  # Added chunk duration
                        "video_format": metadata.get("video_format"),  # Added video format
                        "video_properties": metadata.get("video_properties", {}),  # Added video properties
                        "stream_type": metadata.get("stream_type"),  # Added stream type
                    }
                },
                **metadata  # Include any additional metadata
            }

            message = {
                "input": base64.b64encode(input).decode("utf-8"),
                "input_order": self._get_next_input_order(stream_key),
                "stream_key": stream_key,
                "metadata": enhanced_metadata
            }
            await self.kafka_deployment.async_produce_message(
                message, timeout=timeout, key=stream_key
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
        video_format: str = "mp4"
    ) -> bool:
        """Start a video stream sending video chunks instead of individual frames."""
        if not self._check_stream_support():
            return False
        
        if not self._validate_stream_params(fps, quality, width, height):
            return False
            
        # Additional validation for video-specific parameters
        if video_duration is not None and video_duration <= 0:
            logging.error("Video duration must be positive")
            return False
        if max_frames is not None and max_frames <= 0:
            logging.error("Max frames must be positive")
            return False
        if video_format not in ['mp4', 'avi', 'webm']:
            logging.error("Video format must be one of: mp4, avi, webm")
            return False
            
        try:
            self._stream_video_chunks(
                input, fps, stream_key, quality, width, height,
                video_duration, max_frames, video_format
            )
            return True
        except Exception as exc:
            logging.error("Failed to start video streaming thread: %s", str(exc))
            return False
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt, stopping video streaming")
            self.stop_streaming()
            return False

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
        video_format: str = "mp4"
    ) -> bool:
        """Start a background video stream sending video chunks instead of individual frames."""
        if not self._check_stream_support():
            return False
        
        if not self._validate_stream_params(fps, quality, width, height):
            return False
            
        # Additional validation for video-specific parameters
        if video_duration is not None and video_duration <= 0:
            logging.error("Video duration must be positive")
            return False
        if max_frames is not None and max_frames <= 0:
            logging.error("Max frames must be positive")
            return False
        if video_format not in ['mp4', 'avi', 'webm']:
            logging.error("Video format must be one of: mp4, avi, webm")
            return False
            
        try:
            thread = threading.Thread(
                target=self._stream_video_chunks,
                args=(input, fps, stream_key, quality, width, height,
                      video_duration, max_frames, video_format),
                daemon=True,
            )
            self.streaming_threads.append(thread)
            thread.start()
            return True
        except Exception as exc:
            logging.error("Failed to start video streaming thread: %s", str(exc))
            return False

    def _stream_video_chunks(
        self,
        input: Union[str, int],
        fps: int = 10,
        stream_key: Optional[str] = None,
        quality: int = 95,
        width: Optional[int] = None,
        height: Optional[int] = None,
        video_duration: Optional[float] = None,
        max_frames: Optional[int] = None,
        video_format: str = "mp4"
    ) -> None:
        """Stream video chunks from a video source to Kafka."""
        quality = max(1, min(100, quality))
        cap = None
        
        try:
            cap, stream_type = self._setup_video_capture(input, width, height)
            
            # Get video properties including original FPS
            video_props = self._get_video_properties(cap)
            original_fps = video_props["original_fps"]
            
            # Get actual frame dimensions
            actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Override with specified dimensions if provided
            if width is not None:
                actual_width = width
            if height is not None:
                actual_height = height

            # Set up video codec
            fourcc_map = {
                'mp4': cv2.VideoWriter_fourcc(*'mp4v'),
                'avi': cv2.VideoWriter_fourcc(*'XVID'),
                'webm': cv2.VideoWriter_fourcc(*'VP80')
            }
            fourcc = fourcc_map.get(video_format, cv2.VideoWriter_fourcc(*'mp4v'))

            # Calculate chunk limits
            if video_duration is not None:
                chunk_frames = int(fps * video_duration)
            elif max_frames is not None:
                chunk_frames = max_frames
            else:
                chunk_frames = int(fps * 5.0)  # Default to 5 seconds

            # Calculate frame sample rate (how many original frames per processed frame)
            frame_sample_rate = original_fps / fps if original_fps > 0 else 1.0

            retry_count = 0
            max_retries = 3
            chunk_count = 0
            consecutive_failures = 0
            max_consecutive_failures = 5
            global_frame_counter = 0

            
            while not self._stop_streaming:
                temp_path = None
                out = None
                try:
                    # Create temporary file for video chunk
                    with tempfile.NamedTemporaryFile(suffix=f'.{video_format}', delete=False) as temp_file:
                        temp_path = temp_file.name

                    # Create video writer
                    out = cv2.VideoWriter(temp_path, fourcc, fps, (actual_width, actual_height))
                    
                    if not out.isOpened():
                        logging.error(f"Failed to open video writer for {temp_path}")
                        consecutive_failures += 1
                        if consecutive_failures >= max_consecutive_failures:
                            logging.error("Too many consecutive video writer failures, stopping")
                            break
                        continue

                    consecutive_failures = 0
                    frames_in_chunk = 0
                    chunk_start_time = time.time()
                    chunk_start_frame = global_frame_counter + 1

                    # Collect frames for this chunk
                    while frames_in_chunk < chunk_frames and not self._stop_streaming:
                        frame_start_time = time.time()
                        ret, frame = cap.read()

                        if not ret:
                            retry_count += 1
                            logging.warning(f"Failed to read frame, retry {retry_count}/{max_retries}")

                            try:
                                cap, retry_count = self._handle_frame_read_failure(
                                    input, cap, retry_count, max_retries, width, height
                                )
                            except (RuntimeError, StopIteration):
                                break
                            continue

                        retry_count = 0
                        global_frame_counter += 1
                        frame = self._resize_frame_if_needed(frame, width, height)
                        out.write(frame)
                        frames_in_chunk += 1

                        # Maintain frame rate
                        frame_interval = 1.0 / fps
                        processing_time = time.time() - frame_start_time
                        sleep_time = max(0, frame_interval - processing_time)
                        if sleep_time > 0:
                            time.sleep(sleep_time)

                    # Finalize video chunk
                    if out is not None:
                        out.release()
                        out = None

                    if frames_in_chunk > 0:
                        # Send video chunk to Kafka
                        try:
                            with open(temp_path, 'rb') as video_file:
                                video_bytes = video_file.read()

                            chunk_count += 1
                            chunk_end_frame = chunk_start_frame + frames_in_chunk - 1
                            
                            # Calculate video timestamp from start
                            video_timestamp = self._calculate_video_timestamp(
                                stream_key or "default", chunk_start_frame, original_fps
                            )
                            
                            video_format = self._get_input_filename(input)
                            if isinstance(video_format, str) and '.' in video_format:
                                video_format = '.'+video_format.split('.')[-1].lower()
                            else:
                                video_format = '.mp4'

                            # Enhanced metadata with all requested information
                            success = self.produce_request(
                                video_bytes, stream_key, 
                                metadata={
                                    "chunk_id": chunk_count,
                                    "frames_count": frames_in_chunk,
                                    "duration": time.time() - chunk_start_time,
                                    "video_format": video_format,
                                    "fps": fps,
                                    "original_fps": original_fps,  # Added original video FPS
                                    "frame_sample_rate": frame_sample_rate,  # Added frame sample rate
                                    "width": actual_width,
                                    "height": actual_height,
                                    "quality": quality,
                                    "video_file": self._get_input_filename(input),
                                    "camera_id": input if isinstance(input, int) or (isinstance(input, str) and input.isdigit()) else None,
                                    "start_frame": chunk_start_frame,
                                    "end_frame": chunk_end_frame,
                                    "video_timestamp": video_timestamp,  # Added video timestamp from start
                                    "stream_time": self._get_high_precision_timestamp(),  # Increased granularity
                                    "is_video_chunk": True,  # Flag to indicate this is a video chunk
                                    "chunk_duration_seconds": chunk_frames / fps,  # Duration of this chunk
                                    "video_properties": video_props,  # Include all video properties
                                    "stream_type": stream_type,  # Added stream type
                                }
                            )
                            
                            if success:
                                logging.debug(f"Successfully sent video chunk {chunk_count} with {frames_in_chunk} frames (frames {chunk_start_frame}-{chunk_end_frame}) at video timestamp {video_timestamp:.3f}s")
                            else:
                                logging.warning(f"Failed to produce video chunk {chunk_count} to Kafka stream")

                        except Exception as e:
                            logging.error(f"Error reading video chunk file: {str(e)}")

                except Exception as chunk_exc:
                    logging.error(f"Error processing video chunk: {chunk_exc}")
                    consecutive_failures += 1
                    if consecutive_failures >= max_consecutive_failures:
                        logging.error("Too many consecutive chunk processing failures, stopping")
                        break
                finally:
                    # Clean up resources
                    if out is not None:
                        try:
                            out.release()
                        except Exception as e:
                            logging.warning(f"Error releasing video writer: {e}")
                    
                    if temp_path and os.path.exists(temp_path):
                        try:
                            os.unlink(temp_path)
                        except Exception as e:
                            logging.warning(f"Failed to delete temporary file {temp_path}: {str(e)}")

                if retry_count >= max_retries:
                    break

        except Exception as exc:
            logging.error(f"Error in video streaming thread: {str(exc)}")
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt, stopping video streaming")
        finally:
            if cap is not None:
                cap.release()
                logging.info(f"Released video source: {input}")
            
            # Clean up stream session
            if stream_key in self.video_start_times:
                del self.video_start_times[stream_key]
