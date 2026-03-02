"""
H.265 encoder/decoder optimized for Linux using persistent subprocesses.

This implementation uses non-blocking I/O and proper frame synchronization
that works well on Linux but may have issues on Windows.
"""
import subprocess
import threading
import queue
import logging
import time
import numpy as np
from typing import Optional
import select
import os

logger = logging.getLogger(__name__)


class H265PersistentFrameEncoder:
    """H.265 encoder using persistent FFmpeg subprocess (Linux optimized).

    This implementation maintains a single FFmpeg process across multiple frames,
    significantly reducing overhead compared to per-frame subprocess creation.

    Performance: ~10-20x faster than per-frame approach for consecutive frames.

    Note: Optimized for Linux. On Windows, use H265FrameEncoder instead.
    """

    def __init__(self, preset: str = "ultrafast", quality: int = 23, use_hardware: bool = False):
        """Initialize persistent H.265 frame encoder.

        Args:
            preset: FFmpeg encoding preset (ultrafast, fast, medium, slow)
            quality: CRF quality (0-51, lower=better quality)
            use_hardware: Use hardware acceleration if available
        """
        self.preset = preset
        self.quality = quality
        self.use_hardware = use_hardware
        self.process: Optional[subprocess.Popen] = None
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self._lock = threading.Lock()
        self._stop_flag = False
        self._reader_thread: Optional[threading.Thread] = None
        self._output_queue: queue.Queue = queue.Queue(maxsize=10)
        self._frames_written = 0
        self._frames_read = 0

    def _start_process(self, width: int, height: int) -> bool:
        """Start persistent FFmpeg encoding process."""
        with self._lock:
            # Already running with correct dimensions
            if self.process and self.width == width and self.height == height:
                return True

            # Stop existing process if dimensions changed
            if self.process:
                self._stop_process_internal()

            try:
                self.width = width
                self.height = height

                # Build FFmpeg command - segment format for clear frame boundaries
                cmd = [
                    "ffmpeg",
                    "-loglevel", "error",  # Reduce stderr noise
                    "-f", "rawvideo",
                    "-pix_fmt", "bgr24",
                    "-s", f"{width}x{height}",
                    "-r", "30",
                    "-i", "-",
                    "-c:v", "libx265" if not self.use_hardware else "hevc_nvenc",
                    "-preset", self.preset,
                    "-x265-params", "keyint=1:min-keyint=1:scenecut=0",  # Force keyframes
                    "-crf", str(self.quality),
                    "-f", "segment",  # Use segment muxer for frame boundaries
                    "-segment_format", "hevc",
                    "-segment_time", "0.001",  # Very short segments = per frame
                    "-reset_timestamps", "1",
                    "-segment_list", "pipe:1",  # Send segment info to stdout
                    "-segment_list_type", "flat",
                    "pipe:1"  # Send data to stdout
                ]

                # Start persistent process
                self.process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0  # Unbuffered
                )

                # Set stdout to non-blocking mode (Linux only)
                try:
                    import fcntl  # type: ignore[import-not-found]
                    flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)  # type: ignore[arg-type]
                    fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)  # type: ignore[arg-type]
                except (ImportError, OSError) as e:
                    logger.warning(f"Could not set non-blocking I/O: {e}")

                # Start background reader thread
                self._stop_flag = False
                self._frames_written = 0
                self._frames_read = 0
                self._reader_thread = threading.Thread(target=self._read_output, daemon=True)
                self._reader_thread.start()

                logger.info(f"Started persistent H.265 encoder: {width}x{height}")
                return True

            except Exception as e:
                logger.error(f"Failed to start H.265 encoder: {e}")
                self._stop_process_internal()
                return False

    def _stop_process_internal(self):
        """Internal method to stop the encoding process."""
        if self.process:
            self._stop_flag = True
            try:
                if self.process.stdin:
                    self.process.stdin.close()
                if self.process.stdout:
                    self.process.stdout.close()
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                try:
                    self.process.kill()
                except:
                    pass
            self.process = None

        # Wait for reader thread
        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=1)
        self._reader_thread = None

        # Clear queue
        while not self._output_queue.empty():
            try:
                self._output_queue.get_nowait()
            except queue.Empty:
                break

    def _read_output(self):
        """Background thread to read encoded frames using select() for non-blocking I/O."""
        buffer = bytearray()

        while not self._stop_flag and self.process:
            try:
                # Use select to check if data is available (Linux)
                try:
                    ready, _, _ = select.select([self.process.stdout], [], [], 0.1)
                except (ValueError, OSError):
                    break

                if ready:
                    # Data available - read it
                    try:
                        chunk = self.process.stdout.read(8192)
                        if chunk:
                            buffer.extend(chunk)
                    except (IOError, OSError):
                        pass

                # Check if we have pending frames to extract
                while self._frames_read < self._frames_written:
                    # Look for frame boundary (VPS/SPS NAL units mark frame start)
                    boundary = self._find_frame_boundary(buffer)

                    if boundary > 0:
                        # Extract complete frame
                        frame_data = bytes(buffer[:boundary])
                        buffer = buffer[boundary:]

                        try:
                            self._output_queue.put(frame_data, timeout=1)
                            self._frames_read += 1
                        except queue.Full:
                            logger.warning("Output queue full, dropping frame")
                            self._frames_read += 1
                    else:
                        # Need more data
                        break

                # If we have a partial frame and all frames are read, flush it
                if self._frames_read < self._frames_written and len(buffer) > 100:
                    # Wait a bit to see if more data arrives
                    time.sleep(0.05)
                    if self._frames_read < self._frames_written:
                        # Still pending, flush buffer as last frame
                        try:
                            self._output_queue.put(bytes(buffer), timeout=1)
                            self._frames_read += 1
                            buffer.clear()
                        except queue.Full:
                            logger.warning("Output queue full")
                            self._frames_read += 1
                            buffer.clear()

            except Exception as e:
                if not self._stop_flag:
                    logger.error(f"Error in read thread: {e}")
                break

    def _find_frame_boundary(self, data: bytearray) -> int:
        """Find the start of the next frame (second VPS/SPS NAL unit)."""
        found_first = False
        i = 0

        while i < len(data) - 6:
            # Look for NAL start code
            if data[i:i+4] == b'\x00\x00\x00\x01':
                nal_type = (data[i+4] >> 1) & 0x3F
                if nal_type in (32, 33):  # VPS or SPS
                    if found_first:
                        return i  # Second frame start found
                    found_first = True
                i += 4
            elif data[i:i+3] == b'\x00\x00\x01':
                nal_type = (data[i+3] >> 1) & 0x3F
                if nal_type in (32, 33):  # VPS or SPS
                    if found_first:
                        return i  # Second frame start found
                    found_first = True
                i += 3
            else:
                i += 1

        return -1

    def encode_frame(self, frame: np.ndarray, timeout: float = 5.0) -> Optional[bytes]:
        """Encode single frame to H.265 bytes using persistent process.

        Args:
            frame: OpenCV frame (BGR format)
            timeout: Max time to wait for encoded frame (seconds)

        Returns:
            H.265 encoded frame bytes or None if failed
        """
        try:
            height, width = frame.shape[:2]

            # Start or restart process if needed
            if not self._start_process(width, height):
                return None

            if not self.process or not self.process.stdin:
                return None

            # Write frame to stdin
            try:
                frame_bytes = frame.tobytes()
                self.process.stdin.write(frame_bytes)
                self.process.stdin.flush()

                with self._lock:
                    self._frames_written += 1

            except (BrokenPipeError, OSError) as e:
                logger.warning(f"Pipe broken, restarting: {e}")
                self._stop_process_internal()
                if not self._start_process(width, height):
                    return None
                # Retry
                self.process.stdin.write(frame_bytes)
                self.process.stdin.flush()
                with self._lock:
                    self._frames_written += 1

            # Wait for encoded frame from queue
            try:
                encoded_frame = self._output_queue.get(timeout=timeout)
                return encoded_frame
            except queue.Empty:
                logger.error(f"Timeout waiting for encoded frame after {timeout}s")
                return None

        except Exception as e:
            logger.error(f"Frame encoding error: {e}")
            return None

    def close(self):
        """Close the encoder and cleanup resources."""
        with self._lock:
            self._stop_process_internal()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.close()
        except:
            pass


class H265PersistentFrameDecoder:
    """H.265 decoder using persistent FFmpeg subprocess (Linux optimized).

    Maintains a single FFmpeg process for decoding multiple H.265 frames.
    """

    def __init__(self, use_hardware: bool = False):
        """Initialize persistent H.265 frame decoder.

        Args:
            use_hardware: Use hardware decoding if available
        """
        self.use_hardware = use_hardware
        self.process: Optional[subprocess.Popen] = None
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self._lock = threading.Lock()
        self._stop_flag = False
        self._reader_thread: Optional[threading.Thread] = None
        self._output_queue: queue.Queue = queue.Queue(maxsize=10)
        self._frames_written = 0
        self._frames_read = 0

    def _start_process(self, width: int, height: int) -> bool:
        """Start persistent FFmpeg decoding process."""
        with self._lock:
            if self.process and self.width == width and self.height == height:
                return True

            if self.process:
                self._stop_process_internal()

            try:
                self.width = width
                self.height = height

                cmd = [
                    "ffmpeg",
                    "-loglevel", "error",
                    "-f", "hevc",
                    "-i", "-",
                    "-f", "rawvideo",
                    "-pix_fmt", "bgr24",
                    "pipe:1"
                ]

                self.process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0
                )

                # Set non-blocking I/O
                try:
                    import fcntl  # type: ignore[import-not-found]
                    flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)  # type: ignore[arg-type]
                    fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)  # type: ignore[arg-type]
                except (ImportError, OSError):
                    pass

                self._stop_flag = False
                self._frames_written = 0
                self._frames_read = 0
                self._reader_thread = threading.Thread(target=self._read_output, daemon=True)
                self._reader_thread.start()

                logger.info(f"Started persistent H.265 decoder: {width}x{height}")
                return True

            except Exception as e:
                logger.error(f"Failed to start H.265 decoder: {e}")
                self._stop_process_internal()
                return False

    def _stop_process_internal(self):
        """Stop the decoding process."""
        if self.process:
            self._stop_flag = True
            try:
                if self.process.stdin:
                    self.process.stdin.close()
                if self.process.stdout:
                    self.process.stdout.close()
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                try:
                    self.process.kill()
                except:
                    pass
            self.process = None

        if self._reader_thread and self._reader_thread.is_alive():
            self._reader_thread.join(timeout=1)
        self._reader_thread = None

        while not self._output_queue.empty():
            try:
                self._output_queue.get_nowait()
            except queue.Empty:
                break

    def _read_output(self):
        """Background thread to read decoded frames."""
        frame_size = self.width * self.height * 3
        buffer = bytearray()

        while not self._stop_flag and self.process:
            try:
                # Use select for non-blocking read
                try:
                    ready, _, _ = select.select([self.process.stdout], [], [], 0.1)
                except (ValueError, OSError):
                    break

                if ready:
                    try:
                        chunk = self.process.stdout.read(frame_size * 2)
                        if chunk:
                            buffer.extend(chunk)
                    except (IOError, OSError):
                        pass

                # Extract complete frames
                while len(buffer) >= frame_size and self._frames_read < self._frames_written:
                    frame_data = bytes(buffer[:frame_size])
                    buffer = buffer[frame_size:]

                    frame = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = frame.reshape((self.height, self.width, 3))

                    try:
                        self._output_queue.put(frame, timeout=1)
                        self._frames_read += 1
                    except queue.Full:
                        logger.warning("Output queue full")
                        self._frames_read += 1

            except Exception as e:
                if not self._stop_flag:
                    logger.error(f"Error in decoder read thread: {e}")
                break

    def decode_frame(self, h265_data: bytes, width: int, height: int, timeout: float = 5.0) -> Optional[np.ndarray]:
        """Decode H.265 frame using persistent process.

        Args:
            h265_data: H.265 encoded frame bytes
            width: Expected frame width
            height: Expected frame height
            timeout: Max time to wait for decoded frame

        Returns:
            OpenCV frame (BGR format) or None if failed
        """
        try:
            if not self._start_process(width, height):
                return None

            if not self.process or not self.process.stdin:
                return None

            # Write H.265 data to stdin
            try:
                self.process.stdin.write(h265_data)
                self.process.stdin.flush()

                with self._lock:
                    self._frames_written += 1

            except (BrokenPipeError, OSError) as e:
                logger.warning(f"Decoder pipe broken, restarting: {e}")
                self._stop_process_internal()
                if not self._start_process(width, height):
                    return None
                self.process.stdin.write(h265_data)
                self.process.stdin.flush()
                with self._lock:
                    self._frames_written += 1

            # Wait for decoded frame
            try:
                decoded_frame = self._output_queue.get(timeout=timeout)
                return decoded_frame
            except queue.Empty:
                logger.error(f"Timeout waiting for decoded frame after {timeout}s")
                return None

        except Exception as e:
            logger.error(f"Frame decoding error: {e}")
            return None

    def close(self):
        """Close the decoder."""
        with self._lock:
            self._stop_process_internal()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            self.close()
        except:
            pass
