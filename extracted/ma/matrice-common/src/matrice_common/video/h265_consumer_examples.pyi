"""Auto-generated stub for module: h265_consumer_examples."""
from typing import Any, Callable, Optional

from .h265_video_processor import H265FrameDecoder, H265StreamDecoder, decode_frame_h265

# Constants
logger: Any

# Functions
def example_frame_consumer() -> Any:
    """
    Example of consuming frame-wise H.265.
    """
    ...
def example_stream_consumer() -> Any:
    """
    Example of consuming continuous H.265 stream.
    """
    ...

# Classes
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

