"""Stub file for video directory."""
from typing import Any, Callable, Optional

from .h265_processor import H265FrameEncoder, H265FrameDecoder
from .h265_processor_linux import H265PersistentFrameEncoder, H265PersistentFrameDecoder
from .h265_video_processor import H265FrameDecoder, H265StreamDecoder, decode_frame_h265

# Constants
IS_LINUX: Any = ...  # From h265_auto
logger: Any = ...  # From h265_auto
logger: Any = ...  # From h265_consumer_examples
logger: Any = ...  # From h265_processor
logger: Any = ...  # From h265_processor_linux
logger: Any = ...  # From h265_video_processor

# Functions
# From h265_consumer_examples
def example_frame_consumer() -> Any:
    """
    Example of consuming frame-wise H.265.
    """
    ...

# From h265_consumer_examples
def example_stream_consumer() -> Any:
    """
    Example of consuming continuous H.265 stream.
    """
    ...

# From h265_processor
def decode_frame_h265(h265_data: Any, width: int, height: int) -> Optional[Any.Any]:
    """
    Quick utility to decode H.265 frame.
    """
    ...

# From h265_processor
def encode_frame_h265(frame: Any.Any, quality: int = 23) -> Optional[Any]:
    """
    Quick utility to encode a frame to H.265.
    """
    ...

# From h265_video_processor
def decode_frame_h265(h265_data: Any, width: int, height: int, use_hardware: bool = False) -> Optional[Any.Any]:
    """
    Quick function to decode H.265 frame data.
    
        Args:
            h265_data: H.265 encoded bytes
            width: Frame width
            height: Frame height
            use_hardware: Use hardware acceleration if available
    
        Returns:
            OpenCV frame (BGR format) or None
    """
    ...

# From h265_video_processor
def encode_frame_h265(frame: Any.Any, quality: int = 23, use_hardware: bool = False) -> Optional[Any]:
    """
    Quick function to encode a single frame to H.265.
    
        Args:
            frame: OpenCV frame (BGR format)
            quality: CRF quality (0-51, lower=better)
            use_hardware: Use hardware acceleration if available
    
        Returns:
            H.265 encoded bytes or None
    """
    ...

# Classes
# From h265_consumer_examples
class H265FrameConsumer:
    # Consumer for frame-wise H.265 encoded messages (compatible with existing downstream).

    def __init__(self: Any, redis_host: str = 'localhost', redis_port: int = 6379, redis_db: int = 0, use_hardware: bool = False) -> None:
        """
        Initialize frame-wise H.265 consumer.
        
                Args:
                    redis_host: Redis server host
                    redis_port: Redis server port
                    redis_db: Redis database number
                    use_hardware: Use hardware decoding if available
        """
        ...

    def consume_frames(self: Any, channel: str, frame_callback: Callable[[Any.Any, dict], None], width: int, height: int) -> Any:
        """
        Consume H.265 frames from Redis channel.
        
                Args:
                    channel: Redis channel name
                    frame_callback: Callback function(frame, metadata)
                    width: Expected frame width
                    height: Expected frame height
        """
        ...


# From h265_consumer_examples
class H265StreamConsumer:
    # Consumer for continuous H.265 stream chunks (optimal compression).

    def __init__(self: Any, redis_host: str = 'localhost', redis_port: int = 6379, redis_db: int = 0, width: int = 640, height: int = 480, use_hardware: bool = False) -> None:
        """
        Initialize stream-wise H.265 consumer.
        
                Args:
                    redis_host: Redis server host
                    redis_port: Redis server port
                    redis_db: Redis database number
                    width: Expected frame width
                    height: Expected frame height
                    use_hardware: Use hardware decoding if available
        """
        ...

    def get_frame(self: Any, timeout: float = 0.1) -> Optional[Any.Any]:
        """
        Get next decoded frame.
        
                Args:
                    timeout: Timeout in seconds
        
                Returns:
                    OpenCV frame (BGR format) or None
        """
        ...

    def get_frames(self: Any) -> Any[Any.Any, None, None]:
        """
        Generator that yields decoded frames.
        """
        ...

    def start_consuming(self: Any, channel: str) -> bool:
        """
        Start consuming H.265 stream chunks from Redis channel.
        
                Args:
                    channel: Redis channel name
        
                Returns:
                    True if started successfully
        """
        ...

    def stop_consuming(self: Any) -> Any:
        """
        Stop consuming H.265 stream chunks.
        """
        ...


# From h265_processor
class H265FrameConsumer:
    # Consumer for frame-wise H.265 from Redis (like your consumer example).

    def __init__(self: Any, redis_host: str = 'localhost', redis_port: int = 6379, redis_db: int = 0) -> None:
        """
        Initialize frame consumer.
        """
        ...

    def consume_frames(self: Any, channel: str, width: int, height: int) -> Any[Any.Any, None, None]:
        """
        Consume H.265 frames from Redis channel.
        
                Args:
                    channel: Redis channel name
                    width: Frame width
                    height: Frame height
        
                Yields:
                    Decoded OpenCV frames
        """
        ...


# From h265_processor
class H265FrameDecoder:
    # H.265 decoder for individual frames.
    #
    #     Note: This implementation creates a new FFmpeg process per frame for maximum
    #     reliability across all platforms. For high-throughput decoding, consider using
    #     H265StreamDecoder instead, which maintains a persistent process.

    def __init__(self: Any, use_hardware: bool = False) -> None:
        """
        Initialize H.265 frame decoder.
        
                Args:
                    use_hardware: Use hardware decoding if available
        """
        ...

    def close(self: Any) -> Any:
        """
        Close the decoder and cleanup resources.
        """
        ...

    def decode_frame(self: Any, h265_data: Any, width: int, height: int, timeout: float = 5.0) -> Optional[Any.Any]:
        """
        Decode H.265 frame to OpenCV frame.
        
                Args:
                    h265_data: H.265 encoded frame bytes
                    width: Expected frame width
                    height: Expected frame height
                    timeout: Max time to wait for decoding (seconds)
        
                Returns:
                    OpenCV frame (BGR format) or None if failed
        """
        ...


# From h265_processor
class H265FrameEncoder:
    # H.265 encoder for individual frames.
    #
    #     Note: This implementation creates a new FFmpeg process per frame for maximum
    #     reliability across all platforms. While this has more overhead than a persistent
    #     subprocess, it guarantees correct frame boundaries and works reliably on Windows.
    #
    #     For high-throughput encoding, consider using H265StreamEncoder instead, which
    #     maintains a persistent process for continuous video streams.

    def __init__(self: Any, preset: str = 'ultrafast', quality: int = 23, use_hardware: bool = False) -> None:
        """
        Initialize H.265 frame encoder.
        
                Args:
                    preset: FFmpeg encoding preset (ultrafast, fast, medium, slow)
                    quality: CRF quality (0-51, lower=better quality)
                    use_hardware: Use hardware acceleration if available
        """
        ...

    def close(self: Any) -> Any:
        """
        Close the encoder and cleanup resources.
        """
        ...

    def encode_frame(self: Any, frame: Any.Any, timeout: float = 5.0) -> Optional[Any]:
        """
        Encode single frame to H.265 bytes.
        
                Args:
                    frame: OpenCV frame (BGR format)
                    timeout: Max time to wait for encoding (seconds)
        
                Returns:
                    H.265 encoded frame bytes or None if failed
        """
        ...


# From h265_processor
class H265StreamConsumer:
    # Consumer for continuous H.265 stream from Redis (like your stream consumer example).

    def __init__(self: Any, width: int, height: int, redis_host: str = 'localhost', redis_port: int = 6379, redis_db: int = 0) -> None:
        """
        Initialize stream consumer.
        """
        ...

    def get_frames(self: Any) -> Any[Any.Any, None, None]:
        """
        Generator that yields decoded frames.
        """
        ...

    def start_consuming(self: Any, channel: str) -> bool:
        """
        Start consuming H.265 stream from Redis.
        
                Args:
                    channel: Redis channel name
        
                Returns:
                    True if started successfully
        """
        ...

    def stop_consuming(self: Any) -> Any:
        """
        Stop consuming.
        """
        ...


# From h265_processor
class H265StreamDecoder:
    # H.265 decoder for continuous byte streams.

    def __init__(self: Any, width: int, height: int, use_hardware: bool = False) -> None:
        """
        Initialize H.265 stream decoder.
        
                Args:
                    width: Expected frame width
                    height: Expected frame height
                    use_hardware: Use hardware decoding if available
        """
        ...

    def decode_bytes(self: Any, h265_chunk: Any) -> bool:
        """
        Add H.265 bytes to decoding stream.
        
                Args:
                    h265_chunk: H.265 encoded bytes
        
                Returns:
                    True if bytes were added successfully
        """
        ...

    def read_frame(self: Any) -> Optional[Any.Any]:
        """
        Read next decoded frame from stream.
        
                Returns:
                    OpenCV frame (BGR format) or None
        """
        ...

    def start(self: Any) -> bool:
        """
        Start the continuous H.265 decoding process.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the decoding process.
        """
        ...


# From h265_processor
class H265StreamEncoder:
    # H.265 encoder for continuous byte streams (like your RTSP → Redis stream example).

    def __init__(self: Any, width: int, height: int, fps: int, preset: str = 'fast', quality: int = 23, use_hardware: bool = False) -> None:
        """
        Initialize H.265 stream encoder.
        
                Args:
                    width: Frame width
                    height: Frame height
                    fps: Frames per second
                    preset: FFmpeg encoding preset
                    quality: CRF quality (0-51, lower=better quality)
                    use_hardware: Use hardware acceleration if available
        """
        ...

    def encode_frame(self: Any, frame: Any.Any) -> bool:
        """
        Add frame to continuous encoding stream.
        
                Args:
                    frame: OpenCV frame (BGR format)
        
                Returns:
                    True if frame was added successfully
        """
        ...

    def read_bytes(self: Any, chunk_size: int = 4096) -> Optional[Any]:
        """
        Read encoded H.265 bytes from the stream.
        
                Args:
                    chunk_size: Size of chunk to read
        
                Returns:
                    H.265 encoded bytes or None
        """
        ...

    def start(self: Any) -> bool:
        """
        Start the continuous H.265 encoding process.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the encoding process.
        """
        ...


# From h265_processor_linux
class H265PersistentFrameDecoder:
    # H.265 decoder using persistent FFmpeg subprocess (Linux optimized).
    #
    #     Maintains a single FFmpeg process for decoding multiple H.265 frames.

    def __init__(self: Any, use_hardware: bool = False) -> None:
        """
        Initialize persistent H.265 frame decoder.
        
                Args:
                    use_hardware: Use hardware decoding if available
        """
        ...

    def close(self: Any) -> Any:
        """
        Close the decoder.
        """
        ...

    def decode_frame(self: Any, h265_data: Any, width: int, height: int, timeout: float = 5.0) -> Optional[Any.Any]:
        """
        Decode H.265 frame using persistent process.
        
                Args:
                    h265_data: H.265 encoded frame bytes
                    width: Expected frame width
                    height: Expected frame height
                    timeout: Max time to wait for decoded frame
        
                Returns:
                    OpenCV frame (BGR format) or None if failed
        """
        ...


# From h265_processor_linux
class H265PersistentFrameEncoder:
    # H.265 encoder using persistent FFmpeg subprocess (Linux optimized).
    #
    #     This implementation maintains a single FFmpeg process across multiple frames,
    #     significantly reducing overhead compared to per-frame subprocess creation.
    #
    #     Performance: ~10-20x faster than per-frame approach for consecutive frames.
    #
    #     Note: Optimized for Linux. On Windows, use H265FrameEncoder instead.

    def __init__(self: Any, preset: str = 'ultrafast', quality: int = 23, use_hardware: bool = False) -> None:
        """
        Initialize persistent H.265 frame encoder.
        
                Args:
                    preset: FFmpeg encoding preset (ultrafast, fast, medium, slow)
                    quality: CRF quality (0-51, lower=better quality)
                    use_hardware: Use hardware acceleration if available
        """
        ...

    def close(self: Any) -> Any:
        """
        Close the encoder and cleanup resources.
        """
        ...

    def encode_frame(self: Any, frame: Any.Any, timeout: float = 5.0) -> Optional[Any]:
        """
        Encode single frame to H.265 bytes using persistent process.
        
                Args:
                    frame: OpenCV frame (BGR format)
                    timeout: Max time to wait for encoded frame (seconds)
        
                Returns:
                    H.265 encoded frame bytes or None if failed
        """
        ...


# From h265_video_processor
class H265FrameDecoder:
    # H.265 decoder for individual frames.

    def __init__(self: Any, use_hardware: bool = False) -> None:
        """
        Initialize frame-wise H.265 decoder.
        
                Args:
                    use_hardware: Use hardware acceleration if available
        """
        ...

    def decode_frame(self: Any, h265_data: Any) -> Optional[Any.Any]:
        """
        Decode H.265 frame to OpenCV frame.
        
                Args:
                    h265_data: H.265 encoded frame bytes
        
                Returns:
                    OpenCV frame (BGR format) or None if decoding failed
        """
        ...


# From h265_video_processor
class H265FrameEncoder:
    # H.265 encoder for individual frames (compatible with existing downstream).

    def __init__(self: Any, width: int, height: int, quality: int = 23, preset: str = 'ultrafast', use_hardware: bool = False) -> None:
        """
        Initialize frame-wise H.265 encoder.
        
                Args:
                    width: Frame width
                    height: Frame height
                    quality: CRF quality (0-51, lower=better)
                    preset: Encoding speed preset
                    use_hardware: Use hardware acceleration if available
        """
        ...

    def encode_frame(self: Any, frame: Any.Any) -> Optional[Any]:
        """
        Encode single frame to H.265 bytes.
        
                Args:
                    frame: OpenCV frame (BGR format)
        
                Returns:
                    H.265 encoded frame bytes or None if encoding failed
        """
        ...


# From h265_video_processor
class H265StreamDecoder:
    # H.265 decoder for continuous video streams.

    def __init__(self: Any, width: int, height: int, use_hardware: bool = False) -> None:
        """
        Initialize continuous stream H.265 decoder.
        
                Args:
                    width: Expected frame width
                    height: Expected frame height
                    use_hardware: Use hardware acceleration if available
        """
        ...

    def decode_chunk(self: Any, h265_chunk: Any) -> bool:
        """
        Add H.265 chunk to decoding stream.
        
                Args:
                    h265_chunk: H.265 encoded chunk bytes
        
                Returns:
                    True if chunk was queued successfully
        """
        ...

    def get_frame(self: Any, timeout: float = 0.1) -> Optional[Any.Any]:
        """
        Get next decoded frame.
        
                Args:
                    timeout: Timeout in seconds
        
                Returns:
                    OpenCV frame (BGR format) or None
        """
        ...

    def start(self: Any) -> bool:
        """
        Start the continuous H.265 decoding process.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the continuous decoding process.
        """
        ...


# From h265_video_processor
class H265StreamEncoder:
    # H.265 encoder for continuous video streams (optimal compression).

    def __init__(self: Any, width: int, height: int, fps: int, quality: int = 23, preset: str = 'fast', use_hardware: bool = False, chunk_size: int = 8192) -> None:
        """
        Initialize continuous stream H.265 encoder.
        
                Args:
                    width: Frame width
                    height: Frame height
                    fps: Frames per second
                    quality: CRF quality (0-51, lower=better)
                    preset: Encoding speed preset
                    use_hardware: Use hardware acceleration if available
                    chunk_size: Size of output chunks in bytes
        """
        ...

    def encode_frame(self: Any, frame: Any.Any) -> bool:
        """
        Add frame to continuous encoding stream.
        
                Args:
                    frame: OpenCV frame (BGR format)
        
                Returns:
                    True if frame was queued successfully
        """
        ...

    def get_encoded_chunk(self: Any, timeout: float = 0.1) -> Optional[Any]:
        """
        Get next chunk of encoded H.265 data.
        
                Args:
                    timeout: Timeout in seconds
        
                Returns:
                    H.265 encoded chunk bytes or None
        """
        ...

    def start(self: Any) -> bool:
        """
        Start the continuous H.265 encoding process.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the continuous encoding process.
        """
        ...


from . import h265_auto, h265_consumer_examples, h265_processor, h265_processor_linux, h265_video_processor