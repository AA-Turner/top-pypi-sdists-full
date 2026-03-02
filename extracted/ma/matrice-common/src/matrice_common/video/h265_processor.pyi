"""Auto-generated stub for module: h265_processor."""
from typing import Any, Optional

# Constants
logger: Any

# Functions
def decode_frame_h265(h265_data: Any, width: int, height: int) -> Optional[Any.Any]:
    """
    Quick utility to decode H.265 frame.
    """
    ...
def encode_frame_h265(frame: Any.Any, quality: int = 23) -> Optional[Any]:
    """
    Quick utility to encode a frame to H.265.
    """
    ...

# Classes
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

