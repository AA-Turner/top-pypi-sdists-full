"""Auto-generated stub for module: h265_video_processor."""
from typing import Any, Optional

# Constants
logger: Any

# Functions
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

