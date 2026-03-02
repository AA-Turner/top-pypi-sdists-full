"""H.265 video encoder and decoder classes for both frame-wise and continuous stream processing."""
import subprocess
import threading
import queue
import logging
import time
from typing import Optional, Tuple, Generator
import numpy as np
import cv2

logger = logging.getLogger(__name__)


class H265FrameEncoder:
    """H.265 encoder for individual frames (compatible with existing downstream)."""
    
    def __init__(
        self, 
        width: int, 
        height: int, 
        quality: int = 23,
        preset: str = "ultrafast",
        use_hardware: bool = False
    ):
        """Initialize frame-wise H.265 encoder.
        
        Args:
            width: Frame width
            height: Frame height
            quality: CRF quality (0-51, lower=better)
            preset: Encoding speed preset
            use_hardware: Use hardware acceleration if available
        """
        self.width = width
        self.height = height
        self.quality = quality
        self.preset = preset
        self.use_hardware = use_hardware
        
    def encode_frame(self, frame: np.ndarray) -> Optional[bytes]:
        """Encode single frame to H.265 bytes.
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            H.265 encoded frame bytes or None if encoding failed
        """
        try:
            # Build FFmpeg command for single frame H.265 encoding
            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24", 
                "-s", f"{self.width}x{self.height}",
                "-i", "-",
                "-c:v", self._get_encoder(),
                "-preset", self.preset,
                "-crf", str(self.quality),
                "-x265-params", "keyint=1",  # Force keyframe for compatibility
                "-f", "hevc",
                "pipe:1"
            ]
            
            # Execute FFmpeg
            process = subprocess.Popen(
                cmd, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Send frame data and get H.265 output
            stdout, stderr = process.communicate(input=frame.tobytes(), timeout=5)
            
            if process.returncode == 0 and stdout:
                return stdout
            else:
                logger.warning(f"Frame encoding failed: {stderr.decode() if stderr else 'Unknown error'}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Frame encoding timeout")
            process.kill()
            return None
        except Exception as e:
            logger.error(f"Frame encoding error: {e}")
            return None
            
    def _get_encoder(self) -> str:
        """Get the appropriate H.265 encoder."""
        if self.use_hardware:
            return "hevc_nvenc"  # NVIDIA GPU
            # Could add: hevc_vaapi, hevc_videotoolbox, etc.
        return "libx265"


class H265StreamEncoder:
    """H.265 encoder for continuous video streams (optimal compression)."""
    
    def __init__(
        self,
        width: int,
        height: int, 
        fps: int,
        quality: int = 23,
        preset: str = "fast",
        use_hardware: bool = False,
        chunk_size: int = 8192
    ):
        """Initialize continuous stream H.265 encoder.
        
        Args:
            width: Frame width
            height: Frame height
            fps: Frames per second
            quality: CRF quality (0-51, lower=better)  
            preset: Encoding speed preset
            use_hardware: Use hardware acceleration if available
            chunk_size: Size of output chunks in bytes
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.quality = quality
        self.preset = preset
        self.use_hardware = use_hardware
        self.chunk_size = chunk_size
        
        # FFmpeg process
        self.process: Optional[subprocess.Popen] = None
        self.output_queue: queue.Queue[bytes] = queue.Queue(maxsize=100)
        self.reader_thread: Optional[threading.Thread] = None
        self.stop_encoding: bool = False
        
    def start(self) -> bool:
        """Start the continuous H.265 encoding process."""
        if self.process:
            return True
            
        try:
            # Build FFmpeg command for continuous stream encoding
            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "-s", f"{self.width}x{self.height}",
                "-r", str(self.fps),
                "-i", "-",
                "-c:v", self._get_encoder(),
                "-preset", self.preset,
                "-crf", str(self.quality),
                "-f", "hevc",
                "pipe:1"
            ]
            
            # Start FFmpeg process
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                bufsize=0  # Unbuffered for real-time streaming
            )
            
            # Start output reader thread
            self.stop_encoding = False
            self.reader_thread = threading.Thread(target=self._read_output, daemon=True)
            self.reader_thread.start()
            
            logger.info(f"Started H.265 stream encoder: {self.width}x{self.height}@{self.fps}fps")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start H.265 stream encoder: {e}")
            self.stop()
            return False
            
    def stop(self):
        """Stop the continuous encoding process."""
        self.stop_encoding = True
        
        if self.process:
            try:
                self.process.stdin.close()
                self.process.stdout.close() 
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None
            
        if self.reader_thread:
            self.reader_thread.join(timeout=2)
            self.reader_thread = None
            
        logger.info("Stopped H.265 stream encoder")
        
    def encode_frame(self, frame: np.ndarray) -> bool:
        """Add frame to continuous encoding stream.
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            True if frame was queued successfully
        """
        if not self.process or not self.process.stdin:
            return False
            
        try:
            self.process.stdin.write(frame.tobytes())
            self.process.stdin.flush()
            return True
        except Exception as e:
            logger.error(f"Failed to encode frame: {e}")
            return False
            
    def get_encoded_chunk(self, timeout: float = 0.1) -> Optional[bytes]:
        """Get next chunk of encoded H.265 data.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            H.265 encoded chunk bytes or None
        """
        try:
            return self.output_queue.get(timeout=timeout)
        except queue.Empty:
            return None
            
    def _read_output(self):
        """Background thread to read FFmpeg output."""
        while not self.stop_encoding and self.process:
            try:
                chunk = self.process.stdout.read(self.chunk_size)
                if chunk:
                    if not self.output_queue.full():
                        self.output_queue.put(chunk)
                    else:
                        logger.warning("Output queue full, dropping H.265 chunk")
                else:
                    break  # End of stream
            except Exception as e:
                logger.error(f"Error reading H.265 output: {e}")
                break
                
    def _get_encoder(self) -> str:
        """Get the appropriate H.265 encoder."""
        if self.use_hardware:
            return "hevc_nvenc"  # NVIDIA GPU
        return "libx265"


class H265FrameDecoder:
    """H.265 decoder for individual frames."""
    
    def __init__(self, use_hardware: bool = False):
        """Initialize frame-wise H.265 decoder.
        
        Args:
            use_hardware: Use hardware acceleration if available
        """
        self.use_hardware = use_hardware
        
    def decode_frame(self, h265_data: bytes) -> Optional[np.ndarray]:
        """Decode H.265 frame to OpenCV frame.
        
        Args:
            h265_data: H.265 encoded frame bytes
            
        Returns:
            OpenCV frame (BGR format) or None if decoding failed
        """
        try:
            # Build FFmpeg command for single frame decoding
            cmd = [
                "ffmpeg", "-y",
                "-f", "hevc",
                "-i", "-", 
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "pipe:1"
            ]
            
            # Execute FFmpeg  
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Send H.265 data and get raw frame
            stdout, stderr = process.communicate(input=h265_data, timeout=5)
            
            if process.returncode == 0 and stdout:
                # Convert raw bytes to OpenCV frame
                # Need to determine frame dimensions - this is a limitation
                # In practice, dimensions should be passed or stored in metadata
                frame_data = np.frombuffer(stdout, dtype=np.uint8)
                # Frame reshape requires known dimensions
                return frame_data  # Return raw data, reshape externally
            else:
                logger.warning(f"Frame decoding failed: {stderr.decode() if stderr else 'Unknown error'}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Frame decoding timeout")
            process.kill()
            return None
        except Exception as e:
            logger.error(f"Frame decoding error: {e}")
            return None


class H265StreamDecoder:
    """H.265 decoder for continuous video streams."""
    
    def __init__(self, width: int, height: int, use_hardware: bool = False):
        """Initialize continuous stream H.265 decoder.
        
        Args:
            width: Expected frame width
            height: Expected frame height
            use_hardware: Use hardware acceleration if available
        """
        self.width = width
        self.height = height
        self.use_hardware = use_hardware
        
        # FFmpeg process
        self.process: Optional[subprocess.Popen] = None
        self.frame_queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=50)
        self.reader_thread: Optional[threading.Thread] = None
        self.stop_decoding: bool = False
        
    def start(self) -> bool:
        """Start the continuous H.265 decoding process."""
        if self.process:
            return True
            
        try:
            # Build FFmpeg command for continuous stream decoding
            cmd = [
                "ffmpeg", "-y",
                "-f", "hevc", 
                "-i", "-",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "pipe:1"
            ]
            
            # Start FFmpeg process
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0  # Unbuffered for real-time streaming
            )
            
            # Start frame reader thread
            self.stop_decoding = False
            self.reader_thread = threading.Thread(target=self._read_frames, daemon=True)
            self.reader_thread.start()
            
            logger.info(f"Started H.265 stream decoder: {self.width}x{self.height}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start H.265 stream decoder: {e}")
            self.stop()
            return False
            
    def stop(self):
        """Stop the continuous decoding process."""
        self.stop_decoding = True
        
        if self.process:
            try:
                self.process.stdin.close()
                self.process.stdout.close()
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None
            
        if self.reader_thread:
            self.reader_thread.join(timeout=2)
            self.reader_thread = None
            
        logger.info("Stopped H.265 stream decoder")
        
    def decode_chunk(self, h265_chunk: bytes) -> bool:
        """Add H.265 chunk to decoding stream.
        
        Args:
            h265_chunk: H.265 encoded chunk bytes
            
        Returns:
            True if chunk was queued successfully
        """
        if not self.process or not self.process.stdin:
            return False
            
        try:
            self.process.stdin.write(h265_chunk)
            self.process.stdin.flush()
            return True
        except Exception as e:
            logger.error(f"Failed to decode chunk: {e}")
            return False
            
    def get_frame(self, timeout: float = 0.1) -> Optional[np.ndarray]:
        """Get next decoded frame.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            OpenCV frame (BGR format) or None
        """
        try:
            return self.frame_queue.get(timeout=timeout)
        except queue.Empty:
            return None
            
    def _read_frames(self):
        """Background thread to read decoded frames."""
        frame_size = self.width * self.height * 3  # BGR
        
        while not self.stop_decoding and self.process:
            try:
                # Read one complete frame
                frame_data = self.process.stdout.read(frame_size)
                if len(frame_data) == frame_size:
                    # Convert to OpenCV frame
                    frame = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = frame.reshape((self.height, self.width, 3))
                    
                    if not self.frame_queue.full():
                        self.frame_queue.put(frame)
                    else:
                        logger.warning("Frame queue full, dropping decoded frame")
                elif len(frame_data) == 0:
                    break  # End of stream
                else:
                    logger.warning(f"Incomplete frame data: {len(frame_data)}/{frame_size}")
            except Exception as e:
                logger.error(f"Error reading decoded frame: {e}")
                break


# Utility functions for easy usage
def encode_frame_h265(frame: np.ndarray, quality: int = 23, use_hardware: bool = False) -> Optional[bytes]:
    """Quick function to encode a single frame to H.265.
    
    Args:
        frame: OpenCV frame (BGR format)
        quality: CRF quality (0-51, lower=better)
        use_hardware: Use hardware acceleration if available
        
    Returns:
        H.265 encoded bytes or None
    """
    height, width = frame.shape[:2]
    encoder = H265FrameEncoder(width, height, quality, use_hardware=use_hardware)
    return encoder.encode_frame(frame)


def decode_frame_h265(h265_data: bytes, width: int, height: int, use_hardware: bool = False) -> Optional[np.ndarray]:
    """Quick function to decode H.265 frame data.
    
    Args:
        h265_data: H.265 encoded bytes
        width: Frame width
        height: Frame height  
        use_hardware: Use hardware acceleration if available
        
    Returns:
        OpenCV frame (BGR format) or None
    """
    decoder = H265FrameDecoder(use_hardware=use_hardware)
    raw_data = decoder.decode_frame(h265_data)
    if raw_data is not None:
        try:
            frame = raw_data.reshape((height, width, 3))
            return frame
        except ValueError:
            logger.error(f"Failed to reshape frame data: expected {height*width*3}, got {len(raw_data)}")
            return None
    return None