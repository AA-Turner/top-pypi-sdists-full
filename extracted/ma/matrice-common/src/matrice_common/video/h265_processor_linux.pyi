"""Auto-generated stub for module: h265_processor_linux."""
from typing import Any, Optional

# Constants
logger: Any

# Classes
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

