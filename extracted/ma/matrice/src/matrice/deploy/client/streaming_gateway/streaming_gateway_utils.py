from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Optional, Union, List, Tuple
import os
import uuid

from matrice.deploy.utils.post_processing.core.config import (
    BaseConfig as PostProcessingConfig,
    AlertConfig as AlertingConfig,
    TrackingConfig,
    ZoneConfig as CountingConfig
)


class InputType(Enum):
    """Supported input types."""
    AUTO = "auto"
    CAMERA = "camera"
    VIDEO_FILE = "video_file"
    RTSP_STREAM = "rtsp_stream"
    HTTP_STREAM = "http_stream"
    HTTP_VIDEO_FILE = "http_video_file"


class ModelInputType(Enum):
    """Supported model input types."""

    FRAMES = "frames"  # Send individual frames as images
    VIDEO = "video"  # Send video chunks


class OutputType(Enum):
    """Supported output types."""

    KAFKA = "kafka"
    FILE = "file"
    BOTH = "both"


@dataclass
class InputConfig:
    """Configuration for input sources."""

    source: Union[int, str]  # Camera index, file path, or stream URL
    type: InputType = InputType.AUTO
    fps: int = 10
    quality: int = 100
    width: Optional[int] = 640
    height: Optional[int] = 480
    stream_key: Optional[str] = None
    stream_group_key: Optional[str] = None
    model_input_type: ModelInputType = ModelInputType.FRAMES
    video_duration: Optional[float] = None  # Duration of video chunks in seconds
    max_frames: Optional[int] = None  # Maximum frames per video chunk
    video_format: str = "mp4"  # Video format for encoding
    simulate_video_file_stream: bool = False

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Validate fps
        if self.fps <= 0:
            raise ValueError("FPS must be positive")

        # Validate quality
        if not (1 <= self.quality <= 100):
            raise ValueError("Quality must be between 1 and 100")

        # Validate dimensions
        if self.width is not None and self.width <= 0:
            raise ValueError("Width must be positive")
        if self.height is not None and self.height <= 0:
            raise ValueError("Height must be positive")

        # Validate video parameters
        if self.video_duration is not None and self.video_duration <= 0:
            raise ValueError("Video duration must be positive")
        if self.max_frames is not None and self.max_frames <= 0:
            raise ValueError("Max frames must be positive")
        if self.video_format not in ["mp4", "avi", "webm"]:
            raise ValueError("Video format must be one of: mp4, avi, webm")

        # Validate video mode requirements
        if self.model_input_type == ModelInputType.VIDEO:
            if self.video_duration is None and self.max_frames is None:
                # Set default duration if none specified
                self.video_duration = 5.0

        if self.type == InputType.AUTO:
            if isinstance(self.source, int) or (isinstance(self.source, str) and self.source.isdigit()):
                self.type = InputType.CAMERA
            elif isinstance(self.source, str) and self.source.startswith(("rtsp://")):
                self.type = InputType.RTSP_STREAM
            elif isinstance(self.source, str) and self.source.startswith(("http://", "https://")):
                self.type = InputType.HTTP_STREAM
            elif isinstance(self.source, str) and os.path.exists(self.source):
                self.type = InputType.VIDEO_FILE
            else:
                self.type = InputType.HTTP_VIDEO_FILE

        # Validate source based on type
        if self.type == InputType.CAMERA:
            if not isinstance(self.source, int) and not (
                isinstance(self.source, str) and self.source.isdigit()
            ):
                raise ValueError("Camera source must be an integer or numeric string")
        elif self.type == InputType.VIDEO_FILE:
            if not isinstance(self.source, str):
                raise ValueError("Video file source must be a string path")
            if not os.path.exists(str(self.source)):
                raise ValueError(f"Video file does not exist: {self.source}")
        elif self.type in [InputType.RTSP_STREAM, InputType.HTTP_STREAM]:
            if not isinstance(self.source, str):
                raise ValueError("Stream source must be a URL string")
            if not str(self.source).startswith(("rtsp://", "http://", "https://")):
                raise ValueError("Stream source must be a valid URL")
        elif self.type == InputType.HTTP_VIDEO_FILE:
            if not isinstance(self.source, str):
                raise ValueError("HTTP video file source must be a URL string")
            if not str(self.source).startswith(("http://", "https://")):
                raise ValueError("HTTP video file source must be a valid HTTP/HTTPS URL")
            # Optional: Check if URL looks like a video file
            video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v')
            if not any(str(self.source).lower().endswith(ext) for ext in video_extensions):
                import warnings
                warnings.warn(f"URL does not appear to point to a video file: {self.source}")
        
        # Generate unique stream key if not provided
        if self.stream_key is None:
            if self.type == InputType.CAMERA:
                self.stream_key = f"camera_{self.source}_{uuid.uuid4().hex[:8]}"
            elif self.type == InputType.VIDEO_FILE:
                filename = os.path.splitext(os.path.basename(str(self.source)))[0]
                self.stream_key = f"video_{filename}_{uuid.uuid4().hex[:8]}"
            elif self.type == InputType.RTSP_STREAM:
                self.stream_key = f"rtsp_{uuid.uuid4().hex[:8]}"
            elif self.type == InputType.HTTP_STREAM:
                self.stream_key = f"http_{uuid.uuid4().hex[:8]}"
            elif self.type == InputType.HTTP_VIDEO_FILE:
                self.stream_key = f"http_video_{uuid.uuid4().hex[:8]}"
            else:
                self.stream_key = f"stream_{uuid.uuid4().hex[:8]}"

        if self.stream_group_key is None:
            self.stream_group_key = f"stream_group_{self.stream_key}"

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result["type"] = self.type.value
        result["model_input_type"] = self.model_input_type.value
        return result

    @classmethod
    def from_dict(cls, data: Dict) -> "InputConfig":
        """Create from dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")

        data = data.copy()

        # Convert enum fields
        if "type" in data:
            try:
                data["type"] = InputType(data["type"])
            except ValueError:
                raise ValueError(f"Invalid input type: {data['type']}")

        if "model_input_type" in data:
            try:
                data["model_input_type"] = ModelInputType(data["model_input_type"])
            except ValueError:
                raise ValueError(
                    f"Invalid model input type: {data['model_input_type']}"
                )

        return cls(**data)


@dataclass
class FileOutputConfig:
    """Configuration for file output."""

    directory: str
    filename_pattern: str = "result_{frame_number}_{stream_key}_{timestamp}.json"
    max_files: Optional[int] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.directory:
            raise ValueError("Directory cannot be empty")
        if not self.filename_pattern:
            raise ValueError("Filename pattern cannot be empty")
        if self.max_files is not None and self.max_files <= 0:
            raise ValueError("Max files must be positive")

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "FileOutputConfig":
        """Create from dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
        return cls(**data)


@dataclass
class KafkaOutputConfig:
    """Configuration for Kafka output."""

    topic: str
    bootstrap_servers: str
    key_field: str = "stream_key"
    producer_config: Optional[Dict] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.topic:
            raise ValueError("Topic cannot be empty")
        if not self.bootstrap_servers:
            raise ValueError("Bootstrap servers cannot be empty")
        if not self.key_field:
            raise ValueError("Key field cannot be empty")

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "KafkaOutputConfig":
        """Create from dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")
        return cls(**data)


@dataclass
class OutputConfig:
    """Configuration for output destinations."""

    type: OutputType
    file_config: Optional[FileOutputConfig] = None
    kafka_config: Optional[KafkaOutputConfig] = None
    post_processing_config: Optional[PostProcessingConfig] = None
    apply_post_processing: bool = False
    save_original_results: bool = True

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.type in [OutputType.FILE, OutputType.BOTH] and not self.file_config:
            raise ValueError("file_config is required when output type includes FILE")
        if self.type in [OutputType.KAFKA, OutputType.BOTH] and not self.kafka_config:
            raise ValueError("kafka_config is required when output type includes KAFKA")

        # Validate post-processing configuration
        if self.apply_post_processing:
            raise ValueError(
                "Post-processing is not available. Please install the post-processing module."
            )

        if self.apply_post_processing and not self.post_processing_config:
            raise ValueError(
                "post_processing_config is required when apply_post_processing is True"
            )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = {
            "type": self.type.value,
            "file_config": self.file_config.to_dict() if self.file_config else None,
            "kafka_config": self.kafka_config.to_dict() if self.kafka_config else None,
            "apply_post_processing": self.apply_post_processing,
            "save_original_results": self.save_original_results,
        }

        if self.post_processing_config:
            result["post_processing_config"] = self.post_processing_config.to_dict()

        return result

    @classmethod
    def from_dict(cls, data: Dict) -> "OutputConfig":
        """Create from dictionary."""
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary")

        data = data.copy()

        # Convert enum field
        if "type" in data:
            try:
                data["type"] = OutputType(data["type"])
            except ValueError:
                raise ValueError(f"Invalid output type: {data['type']}")

        # Convert nested configs
        if data.get("file_config"):
            data["file_config"] = FileOutputConfig.from_dict(data["file_config"])
        if data.get("kafka_config"):
            data["kafka_config"] = KafkaOutputConfig.from_dict(data["kafka_config"])
        if data.get("post_processing_config"):
            data["post_processing_config"] = PostProcessingConfig.from_dict(
                data["post_processing_config"]
            )

        return cls(**data)


# Convenience functions for creating common configurations
def create_camera_input(
    camera_index: int = 0,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    model_input_type: ModelInputType = ModelInputType.FRAMES,
    video_duration: float = None,
    max_frames: int = None,
    video_format: str = "mp4",
) -> InputConfig:
    """Create a camera input configuration.

    Args:
        camera_index: Camera device index (0 for default camera)
        fps: Frames per second to capture
        quality: Video/image quality (1-100)
        stream_key: Unique identifier for the stream
        width: Frame width in pixels
        height: Frame height in pixels
        model_input_type: FRAMES for individual images, VIDEO for video chunks
        video_duration: Duration of video chunks in seconds (only for VIDEO mode)
        max_frames: Maximum frames per video chunk (only for VIDEO mode)
        video_format: Video format for encoding (mp4, avi, webm)

    Returns:
        InputConfig: Configured input for camera

    Raises:
        ValueError: If parameters are invalid
    """
    if not isinstance(camera_index, int) or camera_index < 0:
        raise ValueError("Camera index must be a non-negative integer")

    return InputConfig(
        type=InputType.CAMERA,
        source=camera_index,
        fps=fps,
        quality=quality,
        width=width,
        height=height,
        stream_key=stream_key or f"camera_{camera_index}",
        model_input_type=model_input_type,
        video_duration=video_duration,
        max_frames=max_frames,
        video_format=video_format,
    )


def create_video_input(
    video_path: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    model_input_type: ModelInputType = ModelInputType.FRAMES,
    video_duration: float = None,
    max_frames: int = None,
    video_format: str = "mp4",
) -> InputConfig:
    """Create a video file input configuration.

    Args:
        video_path: Path to the video file
        fps: Frames per second to process
        quality: Video/image quality (1-100)
        stream_key: Unique identifier for the stream
        width: Frame width in pixels
        height: Frame height in pixels
        model_input_type: FRAMES for individual images, VIDEO for video chunks
        video_duration: Duration of video chunks in seconds (only for VIDEO mode)
        max_frames: Maximum frames per video chunk (only for VIDEO mode)
        video_format: Video format for encoding (mp4, avi, webm)

    Returns:
        InputConfig: Configured input for video file

    Raises:
        ValueError: If parameters are invalid
        FileNotFoundError: If video file doesn't exist
    """
    if not isinstance(video_path, str) or not video_path.strip():
        raise ValueError("Video path must be a non-empty string")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    # Extract filename without extension for default stream key
    filename = os.path.splitext(os.path.basename(video_path))[0]

    return InputConfig(
        type=InputType.VIDEO_FILE,
        source=video_path,
        fps=fps,
        quality=quality,
        width=width,
        height=height,
        stream_key=stream_key or f"video_{filename}",
        model_input_type=model_input_type,
        video_duration=video_duration,
        max_frames=max_frames,
        video_format=video_format,
    )


def create_rtsp_input(
    rtsp_url: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    model_input_type: ModelInputType = ModelInputType.FRAMES,
    video_duration: float = None,
    max_frames: int = None,
    video_format: str = "mp4",
) -> InputConfig:
    """Create an RTSP stream input configuration.

    Args:
        rtsp_url: RTSP stream URL
        fps: Frames per second to capture
        quality: Video/image quality (1-100)
        stream_key: Unique identifier for the stream
        width: Frame width in pixels
        height: Frame height in pixels
        model_input_type: FRAMES for individual images, VIDEO for video chunks
        video_duration: Duration of video chunks in seconds (only for VIDEO mode)
        max_frames: Maximum frames per video chunk (only for VIDEO mode)
        video_format: Video format for encoding (mp4, avi, webm)

    Returns:
        InputConfig: Configured input for RTSP stream

    Raises:
        ValueError: If parameters are invalid
    """
    if not isinstance(rtsp_url, str) or not rtsp_url.strip():
        raise ValueError("RTSP URL must be a non-empty string")

    if not rtsp_url.startswith("rtsp://"):
        raise ValueError("RTSP URL must start with 'rtsp://'")

    return InputConfig(
        type=InputType.RTSP_STREAM,
        source=rtsp_url,
        fps=fps,
        quality=quality,
        width=width,
        height=height,
        stream_key=stream_key or f"rtsp_stream_{rtsp_url}",
        model_input_type=model_input_type,
        video_duration=video_duration,
        max_frames=max_frames,
        video_format=video_format,
    )


def create_http_video_input(
    video_url: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    model_input_type: ModelInputType = ModelInputType.FRAMES,
    video_duration: float = None,
    max_frames: int = None,
    video_format: str = "mp4",
) -> InputConfig:
    """Create an HTTP video file input configuration.

    Args:
        video_url: HTTP/HTTPS video file URL
        fps: Frames per second to process
        quality: Video/image quality (1-100)
        stream_key: Unique identifier for the stream
        width: Frame width in pixels
        height: Frame height in pixels
        model_input_type: FRAMES for individual images, VIDEO for video chunks
        video_duration: Duration of video chunks in seconds (only for VIDEO mode)
        max_frames: Maximum frames per video chunk (only for VIDEO mode)
        video_format: Video format for encoding (mp4, avi, webm)

    Returns:
        InputConfig: Configured input for HTTP video file

    Raises:
        ValueError: If parameters are invalid
    """
    if not isinstance(video_url, str) or not video_url.strip():
        raise ValueError("Video URL must be a non-empty string")

    if not video_url.startswith(("http://", "https://")):
        raise ValueError("Video URL must start with 'http://' or 'https://'")

    # Extract a default stream key from the URL
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(video_url)
        filename = os.path.basename(parsed_url.path)
        if filename:
            filename_base = os.path.splitext(filename)[0]
            default_stream_key = f"http_video_{filename_base}"
        else:
            default_stream_key = f"http_video_{video_url}"
    except Exception:
        default_stream_key = f"http_video_{video_url}"

    return InputConfig(
        type=InputType.HTTP_VIDEO_FILE,
        source=video_url,
        fps=fps,
        quality=quality,
        width=width,
        height=height,
        stream_key=stream_key or default_stream_key,
        model_input_type=model_input_type,
        video_duration=video_duration,
        max_frames=max_frames,
        video_format=video_format,
    )


def create_file_output(
    directory: str,
    filename_pattern: str = None,
    max_files: int = None,
    post_processing_config: PostProcessingConfig = None,
    apply_post_processing: bool = False,
    save_original_results: bool = True,
) -> OutputConfig:
    """Create a file output configuration.

    Args:
        directory: Output directory path
        filename_pattern: Pattern for output filenames
        max_files: Maximum number of files to keep
        post_processing_config: Post-processing configuration (optional)
        apply_post_processing: Whether to apply post-processing (default: False)
        save_original_results: Whether to save original results alongside processed ones (default: True)

    Returns:
        OutputConfig instance for file output
    """
    if filename_pattern is None:
        filename_pattern = "result_{frame_number}_{stream_key}_{timestamp}.json"

    file_config = FileOutputConfig(
        directory=directory, filename_pattern=filename_pattern, max_files=max_files
    )

    return OutputConfig(
        type=OutputType.FILE,
        file_config=file_config,
        post_processing_config=post_processing_config,
        apply_post_processing=apply_post_processing,
        save_original_results=save_original_results,
    )


def create_kafka_output(
    topic: str,
    bootstrap_servers: str,
    key_field: str = "stream_key",
    producer_config: Dict = None,
) -> OutputConfig:
    """Create a Kafka output configuration.

    Args:
        topic: Kafka topic name
        bootstrap_servers: Kafka bootstrap servers
        key_field: Field to use as message key
        producer_config: Additional Kafka producer configuration

    Returns:
        OutputConfig instance for Kafka output
    """
    kafka_config = KafkaOutputConfig(
        topic=topic,
        bootstrap_servers=bootstrap_servers,
        key_field=key_field,
        producer_config=producer_config,
    )

    return OutputConfig(
        type=OutputType.KAFKA,
        kafka_config=kafka_config,
    )


def create_dual_output(
    file_directory: str,
    kafka_topic: str,
    kafka_bootstrap_servers: str,
    filename_pattern: str = None,
    max_files: int = None,
    kafka_key_field: str = "stream_key",
    producer_config: Dict = None,
    post_processing_config: PostProcessingConfig = None,
    apply_post_processing: bool = False,
    save_original_results: bool = True,
) -> OutputConfig:
    """Create a dual output configuration (both file and Kafka).

    Args:
        file_directory: Directory for file output
        kafka_topic: Kafka topic name
        kafka_bootstrap_servers: Kafka bootstrap servers
        filename_pattern: Pattern for output filenames
        max_files: Maximum number of files to keep
        kafka_key_field: Field to use as Kafka message key
        producer_config: Additional Kafka producer configuration

    Returns:
        OutputConfig instance for dual output
    """
    if filename_pattern is None:
        filename_pattern = "result_{frame_number}_{stream_key}_{timestamp}.json"

    file_config = FileOutputConfig(
        directory=file_directory, filename_pattern=filename_pattern, max_files=max_files
    )

    kafka_config = KafkaOutputConfig(
        topic=kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        key_field=kafka_key_field,
        producer_config=producer_config,
    )

    return OutputConfig(
        type=OutputType.BOTH,
        file_config=file_config,
        kafka_config=kafka_config,
        post_processing_config=post_processing_config,
        apply_post_processing=apply_post_processing,
        save_original_results=save_original_results,
    )


# Specialized convenience functions for common use cases
def create_camera_frame_input(
    camera_index: int = 0,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
) -> InputConfig:
    """Create a camera input for frame-based streaming.

    Args:
        camera_index: Camera device index
        fps: Frames per second
        quality: Image quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height

    Returns:
        InputConfig: Camera input configured for frame streaming
    """
    return create_camera_input(
        camera_index=camera_index,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.FRAMES,
    )


def create_camera_video_input(
    camera_index: int = 0,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    video_duration: float = 5.0,
    video_format: str = "mp4",
) -> InputConfig:
    """Create a camera input for video-based streaming with duration limit.

    Args:
        camera_index: Camera device index
        fps: Frames per second
        quality: Video quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height
        video_duration: Duration of video chunks in seconds
        video_format: Video format (mp4, avi, webm)

    Returns:
        InputConfig: Camera input configured for video streaming
    """
    return create_camera_input(
        camera_index=camera_index,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.VIDEO,
        video_duration=video_duration,
        video_format=video_format,
    )


def create_camera_video_input_by_frames(
    camera_index: int = 0,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    max_frames: int = 150,
    video_format: str = "mp4",
) -> InputConfig:
    """Create a camera input for video-based streaming with frame count limit.

    Args:
        camera_index: Camera device index
        fps: Frames per second
        quality: Video quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height
        max_frames: Maximum frames per video chunk
        video_format: Video format (mp4, avi, webm)

    Returns:
        InputConfig: Camera input configured for video streaming
    """
    return create_camera_input(
        camera_index=camera_index,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.VIDEO,
        max_frames=max_frames,
        video_format=video_format,
    )


def create_video_frame_input(
    video_path: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
) -> InputConfig:
    """Create a video file input for frame-based streaming.

    Args:
        video_path: Path to video file
        fps: Frames per second
        quality: Image quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height

    Returns:
        InputConfig: Video input configured for frame streaming
    """
    return create_video_input(
        video_path=video_path,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.FRAMES,
    )


def create_video_video_input(
    video_path: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    video_duration: float = 5.0,
    video_format: str = "mp4",
) -> InputConfig:
    """Create a video file input for video-based streaming with duration limit.

    Args:
        video_path: Path to video file
        fps: Frames per second
        quality: Video quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height
        video_duration: Duration of video chunks in seconds
        video_format: Video format (mp4, avi, webm)

    Returns:
        InputConfig: Video input configured for video streaming
    """
    return create_video_input(
        video_path=video_path,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.VIDEO,
        video_duration=video_duration,
        video_format=video_format,
    )


def create_video_video_input_by_frames(
    video_path: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    max_frames: int = 150,
    video_format: str = "mp4",
) -> InputConfig:
    """Create a video file input for video-based streaming with frame count limit.

    Args:
        video_path: Path to video file
        fps: Frames per second
        quality: Video quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height
        max_frames: Maximum frames per video chunk
        video_format: Video format (mp4, avi, webm)

    Returns:
        InputConfig: Video input configured for video streaming
    """
    return create_video_input(
        video_path=video_path,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.VIDEO,
        max_frames=max_frames,
        video_format=video_format,
    )


def create_http_video_frame_input(
    video_url: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
) -> InputConfig:
    """Create an HTTP video file input for frame-based streaming.

    Args:
        video_url: HTTP/HTTPS video file URL
        fps: Frames per second
        quality: Image quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height

    Returns:
        InputConfig: HTTP video input configured for frame streaming
    """
    return create_http_video_input(
        video_url=video_url,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.FRAMES,
    )


def create_http_video_video_input(
    video_url: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    video_duration: float = 5.0,
    video_format: str = "mp4",
) -> InputConfig:
    """Create an HTTP video file input for video-based streaming with duration limit.

    Args:
        video_url: HTTP/HTTPS video file URL
        fps: Frames per second
        quality: Video quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height
        video_duration: Duration of video chunks in seconds
        video_format: Video format (mp4, avi, webm)

    Returns:
        InputConfig: HTTP video input configured for video streaming
    """
    return create_http_video_input(
        video_url=video_url,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.VIDEO,
        video_duration=video_duration,
        video_format=video_format,
    )


def create_http_video_video_input_by_frames(
    video_url: str,
    fps: int = 30,
    quality: int = 95,
    stream_key: str = None,
    width: int = None,
    height: int = None,
    max_frames: int = 150,
    video_format: str = "mp4",
) -> InputConfig:
    """Create an HTTP video file input for video-based streaming with frame count limit.

    Args:
        video_url: HTTP/HTTPS video file URL
        fps: Frames per second
        quality: Video quality (1-100)
        stream_key: Stream identifier
        width: Frame width
        height: Frame height
        max_frames: Maximum frames per video chunk
        video_format: Video format (mp4, avi, webm)

    Returns:
        InputConfig: HTTP video input configured for video streaming
    """
    return create_http_video_input(
        video_url=video_url,
        fps=fps,
        quality=quality,
        stream_key=stream_key,
        width=width,
        height=height,
        model_input_type=ModelInputType.VIDEO,
        max_frames=max_frames,
        video_format=video_format,
    )


# Post-processing utility functions
def create_detection_post_processing_config(
    confidence_threshold: float = 0.6,
    enable_counting: bool = True,
    enable_alerting: bool = True,
    map_index_to_category: bool = False,
    index_to_category: Dict[int, str] = None,
    category_triggers: List[str] = None,
    count_threshold: int = None,
) -> PostProcessingConfig:
    """Create a post-processing configuration optimized for object detection.

    Args:
        confidence_threshold: Global confidence threshold for filtering detections
        enable_counting: Whether to enable object counting features
        enable_alerting: Whether to enable alerting features
        map_index_to_category: Whether to map category indices to names
        index_to_category: Mapping from category indices to category names
        category_triggers: List of categories that should trigger alerts
        count_threshold: Threshold for triggering count-based alerts

    Returns:
        PostProcessingConfig optimized for detection models
    """

    alerting_config = AlertingConfig(
        enable_alerting=enable_alerting,
        category_threshold={"all": confidence_threshold},
        category_triggers=category_triggers,
    )

    if count_threshold:
        alerting_config.category_count_threshold = {"all": count_threshold}

    return PostProcessingConfig(
        map_index_to_category=map_index_to_category,
        index_to_category=index_to_category,
        alerting=alerting_config,
        counting=CountingConfig(
            enable_counting=enable_counting, identification_keys=["category"]
        ),
    )


def create_tracking_post_processing_config(
    confidence_threshold: float = 0.6,
    enable_tracking: bool = True,
    enable_counting: bool = True,
    enable_alerting: bool = True,
    tracking_zones: Dict[str, List[Tuple[int, int]]] = None,
    crossing_lines: Dict[str, List[Tuple[int, int]]] = None,
    map_index_to_category: bool = False,
    index_to_category: Dict[int, str] = None,
    category_triggers: List[str] = None,
) -> PostProcessingConfig:
    """Create a post-processing configuration optimized for object tracking.

    Args:
        confidence_threshold: Global confidence threshold for filtering detections
        enable_tracking: Whether to enable tracking features
        enable_counting: Whether to enable object counting features
        enable_alerting: Whether to enable alerting features
        tracking_zones: Dictionary of zone names to polygon coordinates
        crossing_lines: Dictionary of line names to line coordinates
        map_index_to_category: Whether to map category indices to names
        index_to_category: Mapping from category indices to category names
        category_triggers: List of categories that should trigger alerts

    Returns:
        PostProcessingConfig optimized for tracking models
    """

    return PostProcessingConfig(
        map_index_to_category=map_index_to_category,
        index_to_category=index_to_category,
        alerting=AlertingConfig(
            enable_alerting=enable_alerting,
            category_threshold={"all": confidence_threshold},
            category_triggers=category_triggers,
        ),
        tracking=TrackingConfig(
            enable_tracking=enable_tracking,
            tracking_zones=tracking_zones,
            crossing_lines=crossing_lines,
        ),
        counting=CountingConfig(
            enable_counting=enable_counting, identification_keys=["track_id"]
        ),
    )


def create_security_post_processing_config(
    person_confidence_threshold: float = 0.8,
    vehicle_confidence_threshold: float = 0.7,
    restricted_zones: Dict[str, List[Tuple[int, int]]] = None,
    entrance_lines: Dict[str, List[Tuple[int, int]]] = None,
    alert_on_person: bool = True,
    max_person_count: int = 5,
) -> PostProcessingConfig:
    """Create a post-processing configuration optimized for security monitoring.

    Args:
        person_confidence_threshold: Confidence threshold for person detection
        vehicle_confidence_threshold: Confidence threshold for vehicle detection
        restricted_zones: Dictionary of restricted zone names to polygon coordinates
        entrance_lines: Dictionary of entrance line names to line coordinates
        alert_on_person: Whether to alert whenever a person is detected
        max_person_count: Maximum allowed person count before triggering alert

    Returns:
        PostProcessingConfig optimized for security monitoring
    """

    category_thresholds = {
        "person": person_confidence_threshold,
        "car": vehicle_confidence_threshold,
        "truck": vehicle_confidence_threshold,
        "all": 0.6,
    }

    category_triggers = ["person"] if alert_on_person else []
    category_count_thresholds = {"person": max_person_count}

    return PostProcessingConfig(
        map_index_to_category=True,
        index_to_category={
            0: "person",
            1: "car",
            2: "truck",
            3: "bus",
            4: "motorcycle",
        },
        alerting=AlertingConfig(
            enable_alerting=True,
            category_threshold=category_thresholds,
            category_count_threshold=category_count_thresholds,
            category_triggers=category_triggers,
        ),
        tracking=TrackingConfig(
            enable_tracking=True,
            tracking_zones=restricted_zones,
            crossing_lines=entrance_lines,
        ),
        counting=CountingConfig(enable_counting=True, identification_keys=["track_id"]),
    )
