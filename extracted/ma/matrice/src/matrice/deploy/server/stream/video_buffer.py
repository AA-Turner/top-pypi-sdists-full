"""Video buffering utilities for stream processing."""

import asyncio
import logging
import base64
import tempfile
import os
import cv2
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from collections import defaultdict, deque


def base64_frames_to_video_bytes_cv2(base64_frames, fps=10, output_format='mp4'):
    """
    Convert base64-encoded JPEG frames to a video using OpenCV,
    and return the video bytes by writing to a temp file.
    """
    if not base64_frames:
        raise ValueError("No frames provided")

    # Decode the first frame to get size
    first_frame = base64.b64decode(base64_frames[0])
    img = cv2.imdecode(np.frombuffer(first_frame, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode first frame")

    height, width = img.shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    out = cv2.VideoWriter(tmp_path, fourcc, fps, (width, height))

    for b64_frame in base64_frames:
        jpg_bytes = base64.b64decode(b64_frame)
        frame = cv2.imdecode(np.frombuffer(jpg_bytes, np.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Could not decode frame")
        out.write(frame)

    out.release()

    with open(tmp_path, "rb") as f:
        video_bytes = f.read()

    os.remove(tmp_path)
    return video_bytes


class FrameBuffer:
    """Buffer for collecting frames into video chunks."""
    
    def __init__(self, stream_key: str, buffer_config: Dict[str, Any]):
        """Initialize frame buffer for a specific stream.
        
        Args:
            stream_key: Unique identifier for the stream
            buffer_config: Configuration for buffering (fps, duration, etc.)
        """
        self.stream_key = stream_key
        self.fps = buffer_config.get("fps", 10)
        self.chunk_duration = buffer_config.get("chunk_duration_seconds", 5.0)
        self.max_frames = int(self.fps * self.chunk_duration)
        self.timeout_seconds = buffer_config.get("timeout_seconds", 10.0)
        
        # Buffer state
        self.frames: List[str] = []  # Base64 encoded frames
        self.metadata_list: List[Dict] = []  # Associated metadata for each frame
        self.first_frame_time = None
        self.last_frame_time = None
        
        self.logger = logging.getLogger(f"{__name__}.{stream_key}")
    
    def add_frame(self, base64_frame: str, metadata: Dict[str, Any]) -> bool:
        """Add a frame to the buffer.
        
        Args:
            base64_frame: Base64 encoded frame data
            metadata: Frame metadata
            
        Returns:
            True if buffer is ready for processing, False otherwise
        """
        current_time = datetime.now(timezone.utc)
        
        if not self.frames:
            self.first_frame_time = current_time
        
        self.frames.append(base64_frame)
        self.metadata_list.append(metadata)
        self.last_frame_time = current_time
        
        # Check if buffer is ready
        return self.is_ready()
    
    def is_ready(self) -> bool:
        """Check if buffer is ready for processing."""
        if not self.frames:
            return False
        
        # Check frame count
        if len(self.frames) >= self.max_frames:
            return True
        
        # Check timeout
        if self.first_frame_time:
            elapsed = (datetime.now(timezone.utc) - self.first_frame_time).total_seconds()
            if elapsed >= self.timeout_seconds:
                return True
        
        return False
    
    def is_expired(self, max_idle_time: float = 30.0) -> bool:
        """Check if buffer has been idle too long."""
        if not self.last_frame_time:
            return False
        
        elapsed = (datetime.now(timezone.utc) - self.last_frame_time).total_seconds()
        return elapsed > max_idle_time
    
    def create_video_chunk(self) -> Optional[Dict[str, Any]]:
        """Create a video chunk from buffered frames.
        
        Returns:
            Dictionary containing video data and metadata, or None if failed
        """
        if not self.frames:
            self.logger.debug(f"No frames available to create chunk for stream {self.stream_key}")
            return None
        
        if len(self.frames) < 2:
            self.logger.warning(f"Only {len(self.frames)} frame(s) available for stream {self.stream_key}, creating single frame chunk")
        
        try:
            # Validate frames before processing
            valid_frames = []
            for i, frame in enumerate(self.frames):
                try:
                    # Test decode first frame to validate
                    test_decode = base64.b64decode(frame)
                    if len(test_decode) > 0:
                        valid_frames.append(frame)
                    else:
                        self.logger.warning(f"Empty frame data at index {i} for stream {self.stream_key}")
                except Exception as frame_exc:
                    self.logger.warning(f"Invalid frame at index {i} for stream {self.stream_key}: {str(frame_exc)}")
            
            if not valid_frames:
                self.logger.error(f"No valid frames found for stream {self.stream_key}")
                return None
            
            if len(valid_frames) != len(self.frames):
                self.logger.warning(f"Using {len(valid_frames)}/{len(self.frames)} valid frames for stream {self.stream_key}")
            
            # Convert frames to video
            video_bytes = base64_frames_to_video_bytes_cv2(
                valid_frames, 
                fps=self.fps, 
                output_format='mp4'
            )
            
            if not video_bytes:
                self.logger.error(f"Video conversion resulted in empty data for stream {self.stream_key}")
                return None
            
            # Combine metadata
            combined_metadata = self._combine_metadata()
            combined_metadata['valid_frame_count'] = len(valid_frames)
            combined_metadata['original_frame_count'] = len(self.frames)
            
            # Create video chunk message
            chunk_data = {
                "video_data": video_bytes,
                "metadata": combined_metadata,
                "frame_count": len(valid_frames),
                "duration_seconds": len(valid_frames) / self.fps,
                "fps": self.fps,
                "stream_key": self.stream_key,
                "chunk_created_time": datetime.now(timezone.utc),
                "video_size_bytes": len(video_bytes),
            }
            
            self.logger.debug(
                f"Created video chunk for stream {self.stream_key}: "
                f"{len(valid_frames)} frames, {len(video_bytes)} bytes, "
                f"{chunk_data['duration_seconds']:.2f}s"
            )
            
            return chunk_data
            
        except Exception as exc:
            self.logger.error(
                f"Failed to create video chunk for stream {self.stream_key}: {str(exc)}",
                exc_info=True
            )
            return None
    
    def _combine_metadata(self) -> Dict[str, Any]:
        """Combine metadata from all frames in the buffer."""
        if not self.metadata_list:
            return {}
        
        # Use first frame's metadata as base
        combined = self.metadata_list[0].copy()
        
        # Update with chunk-specific information
        combined.update({
            "is_video_chunk": True,
            "chunk_duration_seconds": len(self.frames) / self.fps,
            "chunk_frames": len(self.frames),
            "start_frame": self.metadata_list[0].get("start_frame", 0),
            "end_frame": self.metadata_list[-1].get("end_frame", len(self.frames) - 1),
            "original_frame_count": len(self.frames),
        })
        
        return combined
    
    def clear(self):
        """Clear the buffer."""
        self.frames.clear()
        self.metadata_list.clear()
        self.first_frame_time = None
        self.last_frame_time = None


class VideoBufferManager:
    """Manages multiple frame buffers for different streams."""
    
    def __init__(
        self,
        default_fps: int = 10,
        default_chunk_duration: float = 5.0,
        default_timeout: float = 10.0,
        max_idle_time: float = 30.0,
        cleanup_interval: float = 60.0,
    ):
        """Initialize video buffer manager.
        
        Args:
            default_fps: Default FPS for video chunks
            default_chunk_duration: Default chunk duration in seconds
            default_timeout: Default timeout for buffering in seconds
            max_idle_time: Maximum idle time before buffer cleanup
            cleanup_interval: Interval for cleanup tasks
        """
        self.default_fps = default_fps
        self.default_chunk_duration = default_chunk_duration
        self.default_timeout = default_timeout
        self.max_idle_time = max_idle_time
        self.cleanup_interval = cleanup_interval
        
        # Stream buffers indexed by stream key
        self.buffers: Dict[str, FrameBuffer] = {}
        
        # Manager state
        self.is_running = False
        self._cleanup_task: Optional[asyncio.Task] = None
        
        # Metrics
        self.frames_buffered = 0
        self.chunks_created = 0
        self.buffers_created = 0
        self.buffers_cleaned = 0
        
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start the buffer manager."""
        if self.is_running:
            return
        
        self.is_running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        self.logger.info("Video buffer manager started")
    
    async def stop(self):
        """Stop the buffer manager."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Process any remaining buffers
        await self._process_all_ready_buffers()
        
        self.logger.info("Video buffer manager stopped")
    
    async def add_frame(
        self, 
        stream_key: str, 
        base64_frame: str, 
        metadata: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Add a frame to the appropriate buffer.
        
        Args:
            stream_key: Stream identifier
            base64_frame: Base64 encoded frame data
            metadata: Frame metadata
            
        Returns:
            Video chunk data if buffer is ready, None otherwise
        """
        if not self.is_running:
            self.logger.debug("Buffer manager not running, ignoring frame")
            return None
        
        if not stream_key:
            self.logger.error("Empty stream key provided, cannot buffer frame")
            return None
        
        if not base64_frame:
            self.logger.error(f"Empty frame data provided for stream {stream_key}")
            return None
        
        try:
            # Validate frame data
            try:
                test_decode = base64.b64decode(base64_frame)
                if len(test_decode) == 0:
                    self.logger.error(f"Frame data is empty after decoding for stream {stream_key}")
                    return None
            except Exception as decode_exc:
                self.logger.error(f"Invalid base64 frame data for stream {stream_key}: {str(decode_exc)}")
                return None
            
            # Get or create buffer for stream
            if stream_key not in self.buffers:
                try:
                    buffer_config = self._create_buffer_config(metadata)
                    self.buffers[stream_key] = FrameBuffer(stream_key, buffer_config)
                    self.buffers_created += 1
                    self.logger.debug(f"Created new buffer for stream: {stream_key}")
                except Exception as buffer_exc:
                    self.logger.error(f"Failed to create buffer for stream {stream_key}: {str(buffer_exc)}")
                    return None
            
            buffer = self.buffers[stream_key]
            
            # Add frame to buffer
            try:
                is_ready = buffer.add_frame(base64_frame, metadata)
                self.frames_buffered += 1
                
                # If buffer is ready, create video chunk
                if is_ready:
                    return await self._process_buffer(stream_key)
                
            except Exception as add_exc:
                self.logger.error(f"Failed to add frame to buffer for stream {stream_key}: {str(add_exc)}")
                return None
        
        except Exception as exc:
            self.logger.error(
                f"Unexpected error adding frame to buffer for stream {stream_key}: {str(exc)}",
                exc_info=True
            )
        
        return None
    
    def _create_buffer_config(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create buffer configuration from metadata."""
        return {
            "fps": metadata.get("fps", self.default_fps),
            "chunk_duration_seconds": metadata.get("chunk_duration_seconds", self.default_chunk_duration),
            "timeout_seconds": self.default_timeout,
        }
    
    async def _process_buffer(self, stream_key: str) -> Optional[Dict[str, Any]]:
        """Process a ready buffer and create video chunk."""
        if stream_key not in self.buffers:
            return None
        
        buffer = self.buffers[stream_key]
        
        try:
            chunk_data = buffer.create_video_chunk()
            if chunk_data:
                self.chunks_created += 1
                self.logger.debug(
                    f"Created video chunk for stream {stream_key}: "
                    f"{chunk_data['frame_count']} frames, "
                    f"{chunk_data['duration_seconds']:.2f}s"
                )
            
            # Clear buffer after processing
            buffer.clear()
            return chunk_data
            
        except Exception as exc:
            self.logger.error(f"Error processing buffer for stream {stream_key}: {str(exc)}")
            buffer.clear()  # Clear on error
            return None
    
    async def _process_all_ready_buffers(self) -> List[Dict[str, Any]]:
        """Process all ready buffers and return video chunks."""
        chunks = []
        
        for stream_key, buffer in list(self.buffers.items()):
            if buffer.is_ready():
                chunk = await self._process_buffer(stream_key)
                if chunk:
                    chunks.append(chunk)
        
        return chunks
    
    async def _cleanup_loop(self):
        """Background cleanup loop."""
        while self.is_running:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_expired_buffers()
                await self._process_timeout_buffers()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                self.logger.error(f"Error in cleanup loop: {str(exc)}")
    
    async def _cleanup_expired_buffers(self):
        """Remove expired buffers."""
        expired_keys = []
        
        for stream_key, buffer in self.buffers.items():
            if buffer.is_expired(self.max_idle_time):
                expired_keys.append(stream_key)
        
        for key in expired_keys:
            self.logger.debug(f"Cleaning up expired buffer for stream: {key}")
            del self.buffers[key]
            self.buffers_cleaned += 1
    
    async def _process_timeout_buffers(self):
        """Process buffers that have timed out."""
        timeout_keys = []
        
        for stream_key, buffer in self.buffers.items():
            if buffer.frames and buffer.is_ready():
                timeout_keys.append(stream_key)
        
        for key in timeout_keys:
            await self._process_buffer(key)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get buffer manager metrics."""
        active_buffers = len(self.buffers)
        total_buffered_frames = sum(len(buf.frames) for buf in self.buffers.values())
        
        return {
            "is_running": self.is_running,
            "active_buffers": active_buffers,
            "total_buffered_frames": total_buffered_frames,
            "frames_buffered": self.frames_buffered,
            "chunks_created": self.chunks_created,
            "buffers_created": self.buffers_created,
            "buffers_cleaned": self.buffers_cleaned,
            "buffer_details": {
                stream_key: {
                    "frame_count": len(buffer.frames),
                    "first_frame_time": buffer.first_frame_time.isoformat() if buffer.first_frame_time else None,
                    "last_frame_time": buffer.last_frame_time.isoformat() if buffer.last_frame_time else None,
                    "is_ready": buffer.is_ready(),
                    "is_expired": buffer.is_expired(self.max_idle_time),
                }
                for stream_key, buffer in self.buffers.items()
            }
        }
    
    def reset_metrics(self):
        """Reset metrics."""
        self.frames_buffered = 0
        self.chunks_created = 0
        self.buffers_created = 0
        self.buffers_cleaned = 0