"""Clean H.265 encoder/decoder classes for frame-wise and byte-wise streaming."""
import cv2
import subprocess
import threading
import queue
import logging
import time
import numpy as np
from typing import Optional, Generator
import redis

logger = logging.getLogger(__name__)


class H265FrameEncoder:
    """H.265 encoder for individual frames.

    Note: This implementation creates a new FFmpeg process per frame for maximum
    reliability across all platforms. While this has more overhead than a persistent
    subprocess, it guarantees correct frame boundaries and works reliably on Windows.

    For high-throughput encoding, consider using H265StreamEncoder instead, which
    maintains a persistent process for continuous video streams.
    """

    def __init__(self, preset: str = "ultrafast", quality: int = 23, use_hardware: bool = False):
        """Initialize H.265 frame encoder.

        Args:
            preset: FFmpeg encoding preset (ultrafast, fast, medium, slow)
            quality: CRF quality (0-51, lower=better quality)
            use_hardware: Use hardware acceleration if available
        """
        self.preset = preset
        self.quality = quality
        self.use_hardware = use_hardware

    def encode_frame(self, frame: np.ndarray, timeout: float = 5.0) -> Optional[bytes]:
        """Encode single frame to H.265 bytes.

        Args:
            frame: OpenCV frame (BGR format)
            timeout: Max time to wait for encoding (seconds)

        Returns:
            H.265 encoded frame bytes or None if failed
        """
        try:
            height, width = frame.shape[:2]

            # Build FFmpeg command for single frame H.265 encoding
            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "-s", f"{width}x{height}",
                "-i", "-",
                "-c:v", "libx265" if not self.use_hardware else "hevc_nvenc",
                "-preset", self.preset,
                "-x265-params", "keyint=1",  # Every frame is keyframe for compatibility
                "-crf", str(self.quality),
                "-f", "hevc",
                "pipe:1"
            ]

            # Execute FFmpeg process
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Send frame data and get H.265 output
            stdout, stderr = process.communicate(input=frame.tobytes(), timeout=timeout)

            if process.returncode == 0 and stdout:
                return stdout
            else:
                logger.error(f"Frame encoding failed: {stderr.decode() if stderr else 'Unknown error'}")
                return None

        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except:
                pass
            logger.error(f"Frame encoding timeout after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"Frame encoding error: {e}")
            return None

    def close(self):
        """Close the encoder and cleanup resources."""
        pass  # Nothing to clean up in per-frame mode

    def __del__(self):
        """Cleanup on deletion."""
        pass

# Remove the rest of the old persistent implementation methods
# The following methods are replaced above:
#   - _start_process
#   - _stop_process_internal
#   - _read_output
#   - _find_frame_boundary
# These are removed since we're using per-frame encoding

if False:  # Placeholder for old code, wrapped in a string to prevent mypyc parsing
    """
    def _start_process(self, width: int, height: int) -> bool:
        \"\"\"Start persistent FFmpeg encoding process.\"\"\"
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

                # Build FFmpeg command - use matroska container for reliable streaming
                # Matroska (mkv) handles frame boundaries properly in streams
                cmd = [
                    "ffmpeg",
                    "-f", "rawvideo",
                    "-pix_fmt", "bgr24",
                    "-s", f"{width}x{height}",
                    "-r", "30",  # Nominal framerate
                    "-i", "-",
                    "-c:v", "libx265" if not self.use_hardware else "hevc_nvenc",
                    "-preset", self.preset,
                    "-x265-params", "keyint=1:min-keyint=1",  # Force every frame as keyframe
                    "-crf", str(self.quality),
                    "-f", "matroska",  # Use matroska container for proper frame boundaries
                    "-flush_packets", "1",
                    "pipe:1"
                ]

                # Start persistent process
                self.process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0  # Unbuffered
                )

                # Start background reader thread
                self._stop_flag = False
                self._pending_frames = 0
                self._reader_thread = threading.Thread(target=self._read_output, daemon=True)
                self._reader_thread.start()

                logger.info(f"Started persistent H.265 frame encoder: {width}x{height}")
                return True

            except Exception as e:
                logger.error(f"Failed to start H.265 frame encoder: {e}")
                self._stop_process_internal()
                return False

    def _stop_process_internal(self):
        \"\"\"Internal method to stop the encoding process (must be called with lock held).\"\"\"
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

        # Wait for reader thread to finish
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
        \"\"\"Background thread to read encoded frames from FFmpeg stdout.\"\"\"
        buffer = bytearray()
        chunk_size = 8192
        last_data_time = time.time()
        frame_timeout = 0.5  # 500ms without new data = frame is complete

        while not self._stop_flag and self.process:
            try:
                if self._pending_frames > 0:
                    # Use read1() for less blocking behavior (reads whatever is available)
                    try:
                        chunk = self.process.stdout.read1(chunk_size)
                    except AttributeError:
                        # Fallback if read1 not available
                        chunk = self.process.stdout.read(min(chunk_size, 1024))

                    if chunk:
                        buffer.extend(chunk)
                        last_data_time = time.time()

                        # Look for start of next frame to identify boundary
                        frame_boundary = self._find_frame_boundary(buffer)

                        if frame_boundary > 0:
                            # Found complete frame - extract it
                            frame_data = bytes(buffer[:frame_boundary])
                            buffer = buffer[frame_boundary:]

                            # Put frame in queue
                            try:
                                self._output_queue.put(frame_data, timeout=1)
                                self._pending_frames -= 1
                            except queue.Full:
                                logger.warning("Output queue full, dropping encoded frame")
                                self._pending_frames -= 1
                    else:
                        # No new data - check if we should flush buffered data
                        time_since_data = time.time() - last_data_time

                        if len(buffer) > 0 and time_since_data > frame_timeout:
                            # Timeout - flush buffer as complete frame
                            try:
                                self._output_queue.put(bytes(buffer), timeout=1)
                                self._pending_frames -= 1
                                buffer.clear()
                                last_data_time = time.time()
                            except queue.Full:
                                logger.warning("Output queue full, dropping frame")
                                self._pending_frames -= 1
                                buffer.clear()
                        else:
                            # Wait briefly before next read
                            time.sleep(0.01)

                        if self._stop_flag:
                            break

                    # Safety: if buffer is too large, flush it
                    if len(buffer) > 2 * 1024 * 1024 and self._pending_frames > 0:
                        logger.warning(f"Buffer size {len(buffer)} exceeds limit, flushing")
                        try:
                            self._output_queue.put(bytes(buffer), timeout=1)
                            self._pending_frames -= 1
                            buffer.clear()
                        except queue.Full:
                            logger.warning("Output queue full, clearing buffer")
                            buffer.clear()
                            self._pending_frames = max(0, self._pending_frames - 1)
                else:
                    # No pending frames, sleep
                    time.sleep(0.01)

            except Exception as e:
                if not self._stop_flag:
                    logger.error(f"Error reading encoded output: {e}")
                break

        # Flush remaining buffer
        if len(buffer) > 0 and self._pending_frames > 0:
            try:
                self._output_queue.put(bytes(buffer), block=False)
                self._pending_frames -= 1
            except:
                pass
    """

    def _find_frame_boundary(self, data: bytearray) -> int:
        """Find the start of the next frame in the H.265 stream.

        Each keyframe starts with VPS/SPS/PPS NAL units. We look for the second occurrence
        of this pattern to identify where the previous frame ends.

        Returns:
            Position of next frame start, or -1 if not found
        """
        found_first_vps = False
        i = 0

        while i < len(data) - 6:
            # Look for NAL unit start code (0x00 0x00 0x00 0x01 or 0x00 0x00 0x01)
            start_code_len = 0
            if data[i:i+4] == b'\x00\x00\x00\x01':
                start_code_len = 4
            elif data[i:i+3] == b'\x00\x00\x01':
                start_code_len = 3

            if start_code_len > 0:
                # Check NAL unit type (bits 1-6 of first byte after start code)
                if i + start_code_len < len(data):
                    nal_header = data[i + start_code_len]
                    nal_type = (nal_header >> 1) & 0x3F

                    # VPS = 32, SPS = 33, PPS = 34 in H.265
                    if nal_type in (32, 33):  # VPS or SPS indicates frame start
                        if found_first_vps:
                            # This is the second frame start - boundary found
                            return i
                        else:
                            found_first_vps = True

                i += start_code_len
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

            # Write frame to encoder stdin
            try:
                with self._lock:
                    frame_bytes = frame.tobytes()
                    self.process.stdin.write(frame_bytes)
                    self.process.stdin.flush()
                    self._pending_frames += 1
            except (BrokenPipeError, OSError) as e:
                logger.warning(f"Encoder pipe broken, restarting: {e}")
                with self._lock:
                    self._stop_process_internal()
                if not self._start_process(width, height):
                    return None
                # Retry write
                with self._lock:
                    self.process.stdin.write(frame_bytes)
                    self.process.stdin.flush()
                    self._pending_frames += 1

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


class H265StreamEncoder:
    """H.265 encoder for continuous byte streams (like your RTSP → Redis stream example)."""
    
    def __init__(self, width: int, height: int, fps: int, preset: str = "fast", quality: int = 23, use_hardware: bool = False):
        """Initialize H.265 stream encoder.
        
        Args:
            width: Frame width
            height: Frame height
            fps: Frames per second
            preset: FFmpeg encoding preset
            quality: CRF quality (0-51, lower=better quality)
            use_hardware: Use hardware acceleration if available
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.preset = preset
        self.quality = quality
        self.use_hardware = use_hardware
        self.process: Optional[subprocess.Popen] = None
        
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
                "-c:v", "libx265" if not self.use_hardware else "hevc_nvenc", 
                "-preset", self.preset,
                "-crf", str(self.quality),
                "-f", "hevc",
                "pipe:1"
            ]
            
            # Start FFmpeg process with pipes
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0  # Unbuffered for real-time
            )
            
            logger.info(f"Started H.265 stream encoder: {self.width}x{self.height}@{self.fps}fps")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start H.265 stream encoder: {e}")
            self.stop()
            return False
            
    def stop(self):
        """Stop the encoding process."""
        if self.process:
            try:
                self.process.stdin.close()
                self.process.stdout.close()
                self.process.terminate()
                self.process.wait(timeout=3)
            except:
                self.process.kill()
            self.process = None
            
    def encode_frame(self, frame: np.ndarray) -> bool:
        """Add frame to continuous encoding stream.
        
        Args:
            frame: OpenCV frame (BGR format)
            
        Returns:
            True if frame was added successfully
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
            
    def read_bytes(self, chunk_size: int = 4096) -> Optional[bytes]:
        """Read encoded H.265 bytes from the stream.
        
        Args:
            chunk_size: Size of chunk to read
            
        Returns:
            H.265 encoded bytes or None
        """
        if not self.process or not self.process.stdout:
            return None
            
        try:
            return self.process.stdout.read(chunk_size)
        except Exception as e:
            logger.error(f"Failed to read H.265 bytes: {e}")
            return None


class H265FrameDecoder:
    """H.265 decoder for individual frames.

    Note: This implementation creates a new FFmpeg process per frame for maximum
    reliability across all platforms. For high-throughput decoding, consider using
    H265StreamDecoder instead, which maintains a persistent process.
    """

    def __init__(self, use_hardware: bool = False):
        """Initialize H.265 frame decoder.

        Args:
            use_hardware: Use hardware decoding if available
        """
        self.use_hardware = use_hardware

    def decode_frame(self, h265_data: bytes, width: int, height: int, timeout: float = 5.0) -> Optional[np.ndarray]:
        """Decode H.265 frame to OpenCV frame.

        Args:
            h265_data: H.265 encoded frame bytes
            width: Expected frame width
            height: Expected frame height
            timeout: Max time to wait for decoding (seconds)

        Returns:
            OpenCV frame (BGR format) or None if failed
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
            stdout, stderr = process.communicate(input=h265_data, timeout=timeout)

            if process.returncode == 0 and stdout:
                # Convert raw bytes to OpenCV frame
                frame_data = np.frombuffer(stdout, dtype=np.uint8)

                # Calculate expected frame size
                expected_size = width * height * 3  # BGR
                if len(frame_data) >= expected_size:
                    frame = frame_data[:expected_size].reshape((height, width, 3))
                    return frame
                else:
                    logger.error(f"Insufficient frame data: {len(frame_data)}/{expected_size}")
                    return None
            else:
                logger.error(f"Frame decoding failed: {stderr.decode() if stderr else 'Unknown error'}")
                return None

        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except:
                pass
            logger.error(f"Frame decoding timeout after {timeout}s")
            return None
        except Exception as e:
            logger.error(f"Frame decoding error: {e}")
            return None

    def close(self):
        """Close the decoder and cleanup resources."""
        pass  # Nothing to clean up in per-frame mode

    def __del__(self):
        """Cleanup on deletion."""
        pass


class H265StreamDecoder:
    """H.265 decoder for continuous byte streams."""
    
    def __init__(self, width: int, height: int, use_hardware: bool = False):
        """Initialize H.265 stream decoder.
        
        Args:
            width: Expected frame width
            height: Expected frame height
            use_hardware: Use hardware decoding if available
        """
        self.width = width
        self.height = height
        self.use_hardware = use_hardware
        self.process: Optional[subprocess.Popen] = None
        
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
                bufsize=0  # Unbuffered for real-time
            )
            
            logger.info(f"Started H.265 stream decoder: {self.width}x{self.height}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start H.265 stream decoder: {e}")
            self.stop()
            return False
            
    def stop(self):
        """Stop the decoding process."""
        if self.process:
            try:
                self.process.stdin.close()
                self.process.stdout.close()
                self.process.terminate()
                self.process.wait(timeout=3)
            except:
                self.process.kill()
            self.process = None
            
    def decode_bytes(self, h265_chunk: bytes) -> bool:
        """Add H.265 bytes to decoding stream.
        
        Args:
            h265_chunk: H.265 encoded bytes
            
        Returns:
            True if bytes were added successfully
        """
        if not self.process or not self.process.stdin:
            return False
            
        try:
            self.process.stdin.write(h265_chunk)
            self.process.stdin.flush()
            return True
        except Exception as e:
            logger.error(f"Failed to decode bytes: {e}")
            return False
            
    def read_frame(self) -> Optional[np.ndarray]:
        """Read next decoded frame from stream.
        
        Returns:
            OpenCV frame (BGR format) or None
        """
        if not self.process or not self.process.stdout:
            return None
            
        try:
            # Read one complete frame
            frame_size = self.width * self.height * 3  # BGR
            frame_data = self.process.stdout.read(frame_size)
            
            if len(frame_data) == frame_size:
                frame = np.frombuffer(frame_data, dtype=np.uint8)
                frame = frame.reshape((self.height, self.width, 3))
                return frame
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to read decoded frame: {e}")
            return None


# Consumer Classes for Redis Integration

class H265FrameConsumer:
    """Consumer for frame-wise H.265 from Redis (like your consumer example)."""
    
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, redis_db: int = 0):
        """Initialize frame consumer."""
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.decoder = H265FrameDecoder()
        
    def consume_frames(self, channel: str, width: int, height: int) -> Generator[np.ndarray, None, None]:
        """Consume H.265 frames from Redis channel.
        
        Args:
            channel: Redis channel name
            width: Frame width
            height: Frame height
            
        Yields:
            Decoded OpenCV frames
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        
        logger.info(f"Consuming H.265 frames from channel: {channel}")
        
        try:
            for message in pubsub.listen():
                if message["type"] != "message":
                    continue
                    
                try:
                    h265_data = message["data"]
                    frame = self.decoder.decode_frame(h265_data, width, height)
                    if frame is not None:
                        yield frame
                except Exception as e:
                    logger.error(f"Frame decode error: {e}")
                    
        finally:
            pubsub.close()


class H265StreamConsumer:
    """Consumer for continuous H.265 stream from Redis (like your stream consumer example)."""
    
    def __init__(self, width: int, height: int, redis_host: str = "localhost", redis_port: int = 6379, redis_db: int = 0):
        """Initialize stream consumer."""
        self.width = width
        self.height = height
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.decoder = H265StreamDecoder(width, height)
        self.frame_queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=30)
        self._stop_consuming = False
        
    def start_consuming(self, channel: str) -> bool:
        """Start consuming H.265 stream from Redis.
        
        Args:
            channel: Redis channel name
            
        Returns:
            True if started successfully
        """
        if not self.decoder.start():
            return False
            
        # Start Redis consumer thread
        self._stop_consuming = False
        self.redis_thread = threading.Thread(target=self._consume_redis_stream, args=(channel,), daemon=True)
        self.frame_reader_thread = threading.Thread(target=self._read_frames, daemon=True)
        
        self.redis_thread.start()
        self.frame_reader_thread.start()
        
        logger.info(f"Started consuming H.265 stream from channel: {channel}")
        return True
        
    def stop_consuming(self):
        """Stop consuming."""
        self._stop_consuming = True
        self.decoder.stop()
        
    def get_frames(self) -> Generator[np.ndarray, None, None]:
        """Generator that yields decoded frames."""
        while not self._stop_consuming:
            try:
                frame = self.frame_queue.get(timeout=0.1)
                yield frame
            except queue.Empty:
                continue
                
    def _consume_redis_stream(self, channel: str):
        """Background thread to consume H.265 chunks from Redis."""
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        
        try:
            for message in pubsub.listen():
                if self._stop_consuming:
                    break
                    
                if message["type"] != "message":
                    continue
                    
                try:
                    h265_chunk = message["data"]
                    self.decoder.decode_bytes(h265_chunk)
                except Exception as e:
                    logger.error(f"Stream decode error: {e}")
        finally:
            pubsub.close()
            
    def _read_frames(self):
        """Background thread to read decoded frames."""
        while not self._stop_consuming:
            try:
                frame = self.decoder.read_frame()
                if frame is not None:
                    if not self.frame_queue.full():
                        self.frame_queue.put(frame)
                    else:
                        # Drop oldest frame
                        try:
                            self.frame_queue.get_nowait()
                            self.frame_queue.put(frame)
                        except queue.Empty:
                            pass
                else:
                    time.sleep(0.001)  # Small delay if no frame
            except Exception as e:
                logger.error(f"Frame read error: {e}")


# Utility functions for easy usage
def encode_frame_h265(frame: np.ndarray, quality: int = 23) -> Optional[bytes]:
    """Quick utility to encode a frame to H.265."""
    encoder = H265FrameEncoder(quality=quality)
    return encoder.encode_frame(frame)


def decode_frame_h265(h265_data: bytes, width: int, height: int) -> Optional[np.ndarray]:
    """Quick utility to decode H.265 frame.""" 
    decoder = H265FrameDecoder()
    return decoder.decode_frame(h265_data, width, height)