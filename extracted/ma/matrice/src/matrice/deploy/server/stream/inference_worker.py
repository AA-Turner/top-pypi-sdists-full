"""Inference worker for hybrid stream processing architecture."""

import asyncio
import logging
import base64
import cv2
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from matrice.deploy.server.inference.inference_interface import InferenceInterface
from matrice.deploy.server.stream.video_buffer import VideoBufferManager
from matrice.deploy.optimize.frame_comparators import SSIMComparator
from matrice.deploy.optimize.cache_manager import CacheManager
from matrice.deploy.optimize.transmission import ServerTransmissionHandler


class InferenceWorker:
    """Inference worker that processes messages from input queue and adds results to output queue."""
    
    def __init__(
        self,
        worker_id: str,
        inference_interface: InferenceInterface,
        input_queue,  # inference input queue wrapper
        output_queue,  # post processing queue wrapper
        process_timeout: float = 180.0,
        enable_video_buffering: bool = True,
        ssim_threshold: float = 0.95,
        cache_size: int = 100
    ):
        """Initialize inference worker.
        
        Args:
            worker_id: Unique identifier for this worker
            inference_interface: Inference interface to use for inference
            input_queue: Queue to get messages from
            output_queue: Queue to put results into
            process_timeout: Timeout for inference processing
            enable_video_buffering: Whether to enable video buffering
            ssim_threshold: SSIM threshold for frame similarity (default: 0.95)
            cache_size: Maximum number of cached results per stream
        """
        self.worker_id = worker_id
        self.inference_interface = inference_interface
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.process_timeout = process_timeout
        self.enable_video_buffering = enable_video_buffering
        
        # Initialize simple video buffer manager for basic buffering
        self.video_buffer_manager = None
        if enable_video_buffering:
            self.video_buffer_manager = VideoBufferManager()
        
        # Initialize SSIM-based caching and transmission handler
        self.ssim_comparator = SSIMComparator(threshold=ssim_threshold)
        self.cache_manager = CacheManager(max_cache_size=cache_size)
        self.frame_cache = {}  # stream_key -> last_frame for SSIM comparison
        self.last_inference_results = {}  # stream_key -> last_inference_result for similar frame reuse
        self.txh = ServerTransmissionHandler(ssim_threshold=ssim_threshold)
        
        # Worker state
        self.is_running = False
        self.is_active = True
        self._stop_event = asyncio.Event()
        self._processing_task: Optional[asyncio.Task] = None
        
        # Metrics
        self.messages_processed = 0
        self.messages_failed = 0
        self.messages_output = 0
        self.messages_dropped_output = 0
        self.total_inference_time = 0.0
        self.last_inference_time = None
        self.frames_buffered = 0
        self.video_chunks_created = 0
        self.video_chunks_processed = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.global_counter = 0
        
        self.logger = logging.getLogger(f"{__name__}.{worker_id}")
        self.logger.info(f"Initialized InferenceWorker: {worker_id} (video_buffering={enable_video_buffering}, ssim_threshold={ssim_threshold})")
    
    async def start(self) -> None:
        """Start the inference worker."""
        if self.is_running:
            self.logger.warning(f"Inference worker {self.worker_id} is already running")
            return
        
        self.is_running = True
        self.is_active = True
        self._stop_event.clear()
        
        # Start video buffer manager if enabled
        if self.video_buffer_manager:
            await self.video_buffer_manager.start()
        
        # Start the processing loop
        self._processing_task = asyncio.create_task(self._processing_loop())
        
        self.logger.info(f"Started InferenceWorker: {self.worker_id}")
    
    async def stop(self) -> None:
        """Stop the inference worker."""
        if not self.is_running:
            return
        
        self.logger.info(f"Stopping InferenceWorker: {self.worker_id}")
        
        self.is_running = False
        self.is_active = False
        self._stop_event.set()
        
        # Stop video buffer manager if enabled
        if self.video_buffer_manager:
            await self.video_buffer_manager.stop()
        
        # Cancel and wait for processing task
        if self._processing_task and not self._processing_task.done():
            self._processing_task.cancel()
            try:
                await asyncio.wait_for(self._processing_task, timeout=5.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception as exc:
                self.logger.error(f"Error stopping inference worker {self.worker_id}: {str(exc)}")
        
        self.logger.info(f"Stopped InferenceWorker: {self.worker_id}")
    
    async def _processing_loop(self) -> None:
        """Main processing loop for inference."""
        retry_delay = 1.0
        max_retry_delay = 10.0
        consecutive_errors = 0
        loop_count = 0
        
        while self.is_running and not self._stop_event.is_set():
            try:
                loop_count += 1
                # Log worker state periodically
                if loop_count % 100 == 1:
                    self.logger.debug(
                        f"Inference worker {self.worker_id} active (loop #{loop_count}) - "
                        f"in_q: {self.input_queue.qsize()}, out_q: {self.output_queue.qsize()}, "
                        f"processed: {self.messages_processed}, errors: {consecutive_errors}"
                    )
                
                try:
                    priority, message = await self.input_queue.get()
                except asyncio.TimeoutError:
                    # Log periodically when no messages available
                    if loop_count % 50 == 1:
                        self.logger.debug(
                            f"Inference worker {self.worker_id} waiting - no messages in input queue (size: {self.input_queue.qsize()})"
                        )
                    await asyncio.sleep(0.05)
                    continue
                try:
                    # Debug: summarize incoming message
                    try:
                        msg_key = message.get("message_key")
                        strategy = message.get("transmission_strategy") or message.get("stream_info", {}).get("transmission_strategy")
                        input_hash = message.get("input_hash")
                        content = message.get("input_content")
                        content_len = len(content) if content is not None else 0
                        self.logger.debug(
                            f"Recv msg key={msg_key} strat={strategy} hash={'set' if input_hash else 'none'} bytes={content_len} in_q={self.input_queue.qsize()} out_q={self.output_queue.qsize()}"
                        )
                    except Exception:
                        pass
                    action, cached_data = await self._should_process_immediately(message)
                    self.logger.debug(
                        f"Decision for key={message.get('message_key')}: action={action} cached={'yes' if cached_data is not None else 'no'}"
                    )
                    if action == "cached":
                        await self._handle_cached_result(message, cached_data)
                    elif action == "similar":
                        await self._handle_similar_frame(message)
                    elif action == "buffer":
                        await self._process_buffered_message(message)
                    elif action == "process_difference":
                        await self._process_difference_message(message)
                    else:
                        await self._process_single_inference_with_caching(message)
                    retry_delay = 1.0
                    consecutive_errors = 0
                except Exception as exc:
                    self.logger.error(
                        f"Error processing message in inference worker {self.worker_id}: {str(exc)}"
                    )
                    consecutive_errors += 1
            
            except asyncio.CancelledError:
                break
            except Exception as exc:
                consecutive_errors += 1
                self.logger.error(
                    f"Error in inference loop for worker {self.worker_id} (error #{consecutive_errors}): {str(exc)}"
                )
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, max_retry_delay)
                
                # If too many consecutive errors, pause longer
                if consecutive_errors >= 5:
                    self.logger.error(f"Too many consecutive errors in inference worker {self.worker_id}, pausing...")
                    await asyncio.sleep(max_retry_delay)
                    consecutive_errors = 0
        
        self.logger.debug(f"Processing loop ended for inference worker {self.worker_id}")
    
    async def _handle_cached_result(self, message: Dict[str, Any], cached_result: Dict[str, Any]) -> None:
        """Handle cached inference result."""
        try:
            self.logger.debug(
                f"Using cached MODEL result for key={message.get('message_key')} ref_hash={message.get('stream_info', {}).get('reference_input_hash') or message.get('input_hash')}"
            )
            # Recompute post-processing on top of cached MODEL result only
            stream_key = message.get("message_key")
            # Create stream_info with input_settings for frame number extraction (match old structure)
            input_stream = message.get("input_stream", {})
            stream_info = {
                "input_settings": {
                    "start_frame": input_stream.get("start_frame"),
                    "end_frame": input_stream.get("end_frame"),
                    "stream_unit": input_stream.get("stream_unit"),
                    "input_order": input_stream.get("input_order"),
                    "original_fps": input_stream.get("original_fps", 31),
                },
                "camera_location": message.get("stream_info", {}).get("camera_location", "Unknown Location"),
                "stream_time": input_stream.get("stream_info", {}).get("stream_time",""),
            }
            camera_info = message.get("camera_info")
            input_content = message.get("input_content")  # May be empty for skip

            # If no input content (e.g., skip), try to use the last cached frame as input for PP
            if (not input_content) and stream_key in self.frame_cache:
                try:
                    encode_params = [cv2.IMWRITE_JPEG_QUALITY, 95]
                    _, buf = cv2.imencode(".jpg", self.frame_cache[stream_key], encode_params)
                    input_content = buf.tobytes()
                except Exception:
                    input_content = None
            # TODO: Enable sending the the past frame it will used cached frame and no new input

            # Support caches that might store either the raw dict or a wrapper
            model_result = (
                cached_result.get("model_result")
                if isinstance(cached_result, dict) and "model_result" in cached_result
                else cached_result
            )

            # Store result for similar frame reuse
            stream_key = message.get("message_key")
            if stream_key:
                self.last_inference_results[stream_key] = model_result
            
            # Create result message with only model result (no post-processing)
            result_message = self._create_result_message(message, model_result)
            
            # Add to output queue
            try:
                await self.output_queue.put((result_message["global_counter"], result_message))
                self.messages_output += 1
                self.logger.debug(
                    f"Emitted cached inference result for key={message.get('message_key')} out_q={self.output_queue.qsize()}"
                )
            except asyncio.QueueFull:
                self.messages_dropped_output += 1
                self.logger.warning(f"Dropped cached result from inference worker {self.worker_id} - output queue full")
            except Exception as put_exc:
                self.messages_dropped_output += 1
                self.logger.error(f"Failed to put cached result to output queue in worker {self.worker_id}: {str(put_exc)}")
            
            self.messages_processed += 1
            
        except Exception as exc:
            self.logger.error(f"Error handling cached result in worker {self.worker_id}: {str(exc)}")
    
    async def _handle_similar_frame(self, message: Dict[str, Any]) -> None:
        """Handle similar frame by reusing last cached result."""
        try:
            stream_key = message.get("message_key", "default")
            self.logger.debug(f"Handling similar frame for stream {stream_key}")
            
            # Try to get the last cached result for this stream
            # First check if we have a cached result in the cache_manager
            input_hash = message.get("input_hash")
            cached_result = None
            
            if input_hash:
                cached_result = self.cache_manager.get_cached_result(input_hash, stream_key)
            
            # If no cached result found, try to get the most recent result from the last inference results
            if not cached_result:
                cached_result = self.last_inference_results.get(stream_key)
            
            # If still no result, create a simple placeholder result
            if not cached_result:
                self.logger.warning(f"No cached result available for similar frame in stream {stream_key}, using placeholder")
                cached_result = {
                    "predictions": [],
                    "confidence": 0.0,
                    "metadata": {"similarity_reuse": True, "timestamp": datetime.now(timezone.utc).isoformat()}
                }
            
            # Create result message with the cached/placeholder result
            result_message = self._create_result_message(message, cached_result)
            
            # Add similarity metadata
            result_message["similarity_reuse"] = True
            result_message["processing_type"] = "similar_frame_reuse"
            
            # Add to output queue
            try:
                await self.output_queue.put((result_message["global_counter"], result_message))
                self.messages_output += 1
                self.logger.debug(
                    f"Emitted similar frame result for key={stream_key} out_q={self.output_queue.qsize()}"
                )
            except asyncio.QueueFull:
                self.messages_dropped_output += 1
                self.logger.warning(f"Dropped similar frame result from inference worker {self.worker_id} - output queue full")
            except Exception as put_exc:
                self.messages_dropped_output += 1
                self.logger.error(f"Failed to put similar frame result to output queue in worker {self.worker_id}: {str(put_exc)}")
            
            self.messages_processed += 1
            
        except Exception as exc:
            self.logger.error(f"Error handling similar frame in worker {self.worker_id}: {str(exc)}")
    
    async def _process_single_inference_with_caching(self, message: Dict[str, Any]) -> None:
        """Process single inference and cache the result."""
        try:
            # Update frame cache for SSIM comparison
            await self._update_frame_cache(message)
            
            # Perform inference
            start_time = asyncio.get_event_loop().time()
            
            input_content = message.get("input_content")
            # Create stream_info with input_settings for frame number extraction (match old structure)
            input_stream = message.get("input_stream", {})
            stream_info = {
                "input_settings": {
                    "start_frame": input_stream.get("start_frame"),
                    "end_frame": input_stream.get("end_frame"),
                    "stream_unit": input_stream.get("stream_unit"),
                    "input_order": input_stream.get("input_order"),
                    "original_fps": input_stream.get("original_fps", 31),
                },
                "camera_location": message.get("stream_info", {}).get("camera_location", "Unknown Location"),
                "stream_time": input_stream.get("stream_info", {}).get("stream_time",""),
            }
            camera_info = message.get("camera_info")
            input_hash = message.get("input_hash")
            message_key = message.get("message_key")
            self.logger.debug(
                f"Starting inference key={message_key} hash={'set' if input_hash else 'none'} bytes={len(input_content) if input_content is not None else 0} apply_pp=False"
            )
            
            # Only perform model inference, no post-processing
            model_result, _ = await asyncio.wait_for(
                self.inference_interface.inference(
                    input_content,
                    apply_post_processing=False,
                    stream_key=message_key,
                    stream_info=stream_info,
                    camera_info=camera_info,
                    input_hash=input_hash,
                ),
                timeout=self.process_timeout
            )
            
            # Cache MODEL result only if we have input_hash
            if input_hash:
                cache_data = {
                    "model_result": model_result,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                self.cache_manager.set_cached_result(input_hash, cache_data, message_key)
                self.cache_misses += 1
                self.logger.debug(
                    f"Cached model result for key={message_key} hash={input_hash}"
                )
            
            # Store result for similar frame reuse
            self.last_inference_results[message_key] = model_result
            
            # Create result message with only model result
            result_message = self._create_result_message(message, model_result)
            
            # Add to output queue
            try:
                await self.output_queue.put((result_message["global_counter"], result_message))
                self.messages_output += 1
                self.logger.debug(
                    f"Emitted inference result for key={message_key} out_q={self.output_queue.qsize()}"
                )
            except asyncio.QueueFull:
                self.messages_dropped_output += 1
                self.logger.warning(f"Dropped output message from inference worker {self.worker_id} - output queue full")
            except Exception as put_exc:
                self.messages_dropped_output += 1
                self.logger.error(f"Failed to put output message to queue in worker {self.worker_id}: {str(put_exc)}")
            
            # Update metrics
            inference_time = asyncio.get_event_loop().time() - start_time
            self.total_inference_time += inference_time
            self.messages_processed += 1
            self.last_inference_time = datetime.now(timezone.utc)
            self.logger.debug(
                f"Inference done key={message_key} time_ms={int(inference_time*1000)}"
            )
            
        except asyncio.TimeoutError:
            self.logger.error(f"Inference timeout in worker {self.worker_id}")
        except Exception as exc:
            self.logger.error(f"Inference error in worker {self.worker_id}: {str(exc)}")
    
    async def _update_frame_cache(self, message: Dict[str, Any]) -> None:
        """Update frame cache for SSIM comparison."""
        try:
            stream_key = message.get("message_key", "default")
            input_content = message.get("input_content")
            
            if not input_content:
                return
            
            # Decode frame
            if isinstance(input_content, bytes):
                frame_bytes = input_content
            else:
                frame_bytes = base64.b64decode(input_content)
            
            frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                self.frame_cache[stream_key] = frame
                try:
                    self.logger.debug(
                        f"Updated frame cache for key={stream_key} shape={tuple(frame.shape)}"
                    )
                except Exception:
                    pass
                
        except Exception as exc:
            self.logger.error(f"Error updating frame cache for stream {stream_key}: {str(exc)}")
    
    async def _process_difference_message(self, message: Dict[str, Any]) -> None:
        """Process a message containing frame difference data."""
        try:
            try:
                reconstructed_content, effective_hash = self.txh.reconstruct_from_difference(
                    message, self.frame_cache
                )
            except Exception as exc:
                self.logger.debug(
                    f"Difference reconstruction failed for key={message.get('message_key')} err={str(exc)}"
                )
                return

            reconstructed_message = message.copy()
            reconstructed_message["input_content"] = reconstructed_content
            if effective_hash:
                reconstructed_message["input_hash"] = effective_hash
            
            # Process the reconstructed frame
            await self._process_single_inference_with_caching(reconstructed_message)
            
            self.logger.debug(
                f"Processed difference data for key={message.get('message_key', 'default')} hash={effective_hash} bytes={len(reconstructed_content) if reconstructed_content is not None else 0}"
            )
            
        except Exception as exc:
            self.logger.error(f"Error processing difference message in worker {self.worker_id}: {str(exc)}")
    
    async def _should_process_immediately(self, message: Dict[str, Any]) -> tuple:
        """Check if message should be processed immediately (check cache first, then decide buffering)."""
        stream_key = message.get("message_key", "default")
        input_hash = message.get("input_hash")
        
        action, cached = self.txh.decide_action(message, self.cache_manager, self.frame_cache)
        if action == "cached":
            self.cache_hits += 1
            return action, cached
        
        # If not cached but we have full frame hash, reuse
        if action == "process" and input_hash:
            cached_result = self.cache_manager.get_cached_result(input_hash, stream_key)
            if cached_result:
                self.cache_hits += 1
                return "cached", cached_result
        
        # TODO: Enable this after testing and hanlding async and optimal threshold
        # if action == "process" and await self._is_similar_to_cached_frame(message):
        #     return "similar", None
        
        if await self._should_buffer_message(message):
            return "buffer", None
        
        return action, None
    
    async def _is_similar_to_cached_frame(self, message: Dict[str, Any]) -> bool:
        """Check if current frame is similar to cached frame using SSIM."""
        try:
            stream_key = message.get("message_key", "default")
            input_content = message.get("input_content")
            
            if not input_content or stream_key not in self.frame_cache:
                return False
            
            # Decode current frame
            if isinstance(input_content, bytes):
                frame_bytes = input_content
            else:
                frame_bytes = base64.b64decode(input_content)
            
            current_frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
            if current_frame is None:
                return False
            
            # Compare with cached frame
            cached_frame = self.frame_cache[stream_key]
            is_similar, similarity_score = self.ssim_comparator.compare(cached_frame, current_frame, stream_key)
            
            self.logger.debug(f"SSIM similarity for stream {stream_key}: {similarity_score:.3f}, similar: {is_similar}")
            return is_similar
            
        except Exception as exc:
            self.logger.error(f"Error checking frame similarity for stream {stream_key}: {str(exc)}")
            return False
    
    async def _should_buffer_message(self, message: Dict[str, Any]) -> bool:
        """Check if message should be buffered for video chunking (simplified)."""
        if not self.video_buffer_manager or not self.enable_video_buffering:
            return False
        
        # Don't buffer skip or difference messages - they need special handling
        transmission_strategy = message.get("transmission_strategy", "full")
        if transmission_strategy in ("skip", "difference"):
            return False
        
        # Only buffer messages with actual frame content
        input_content = message.get("input_content")
        if not input_content:
            return False
        
        # Get buffering config from message metadata
        stream_info = message.get("stream_info", {})
        input_settings = stream_info.get("input_settings", {})
        
        # Simple logic: buffer if FPS is reasonable and stream unit is frame
        input_stream = message.get("input_stream", {})
        stream_unit = input_stream.get("stream_unit", "frame")
        fps = input_settings.get("original_fps", 0)
        
        decision = stream_unit != "frame"
        if decision:
            self.logger.debug(
                f"Buffering eligible key={message.get('message_key')} fps={fps}"
            )
        return decision
    
    async def _process_buffered_message(self, message: Dict[str, Any]) -> None:
        """Process a message that should be buffered for video chunking."""
        try:
            # Extract frame data and metadata
            input_content = message.get("input_content")
            if not input_content:
                self.logger.warning(f"No input content in buffered message from worker {self.worker_id}")
                return
            
            # Convert bytes to base64 if needed
            if isinstance(input_content, bytes):
                base64_frame = base64.b64encode(input_content).decode('utf-8')
            else:
                base64_frame = input_content
            
            # Extract metadata for buffering - get config from message data
            stream_key = message.get("message_key", "default")
            stream_info = message.get("stream_info", {})
            input_settings = stream_info.get("input_settings", {})
            
            # Create simple buffer config from message metadata
            buffer_metadata = {
                "fps": input_settings.get("original_fps", 10),
                "chunk_duration_seconds": stream_info.get("chunk_duration_seconds", 5.0),
                "timeout_seconds": stream_info.get("timeout_seconds", 10.0),
            }
            self.logger.debug(
                f"Add frame to buffer key={stream_key} cfg={{fps:{buffer_metadata['fps']},dur:{buffer_metadata['chunk_duration_seconds']}}}"
            )
            
            # Add frame to buffer
            video_chunk = await self.video_buffer_manager.add_frame(
                stream_key=stream_key,
                base64_frame=base64_frame,
                metadata=buffer_metadata
            )
            
            self.frames_buffered += 1
            
            # If video chunk was created, process it
            if video_chunk:
                self.logger.debug(
                    f"Video chunk ready key={stream_key} frames={video_chunk.get('frame_count')} bytes={len(video_chunk.get('video_data') or b'')}"
                )
                await self._process_video_chunk(video_chunk, message)
                
        except Exception as exc:
            self.logger.error(f"Error processing buffered message in worker {self.worker_id}: {str(exc)}")
    
    async def _process_video_chunk(self, video_chunk: Dict[str, Any], original_message: Dict[str, Any]) -> None:
        """Process a video chunk for inference."""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Extract video data
            video_data = video_chunk.get("video_data")
            chunk_metadata = video_chunk.get("metadata", {})
            self.logger.debug(
                f"Starting video-chunk inference key={original_message.get('message_key')} frames={video_chunk.get('frame_count')} dur={video_chunk.get('duration_seconds')}s"
            )
            
            # Build stream_info in the expected structure using chunk metadata
            stream_info = {
                "input_settings": {
                    "start_frame": chunk_metadata.get("start_frame"),
                    "end_frame": chunk_metadata.get("end_frame"),
                    "stream_unit": "segment",
                    "input_order": chunk_metadata.get("input_order"),
                    "original_fps": chunk_metadata.get("fps", 31),
                },
                "camera_location": original_message.get("stream_info", {}).get("camera_location", "Unknown Location"),
                "stream_time": original_message.get("stream_info", {}).get("stream_time",""),
            }

            # Perform inference on video chunk (no post-processing)
            model_result, _ = await asyncio.wait_for(
                self.inference_interface.inference(
                    video_data,
                    apply_post_processing=False,
                    stream_key=original_message.get("message_key"),
                    stream_info=stream_info,
                    camera_info=original_message.get("camera_info"),
                    input_hash=original_message.get("input_hash"),
                ),
                timeout=self.process_timeout
            )
            
            # Create result message for video chunk (only model result)
            result_message = self._create_video_chunk_result_message(
                video_chunk, original_message, model_result
            )
            
            # Add to output queue
            try:
                await self.output_queue.put((result_message["global_counter"], result_message))
                self.messages_output += 1
                self.video_chunks_processed += 1
                self.logger.debug(
                    f"Emitted video-chunk result key={original_message.get('message_key')} out_q={self.output_queue.qsize()}"
                )
            except asyncio.QueueFull:
                self.messages_dropped_output += 1
                self.logger.warning(f"Dropped video chunk output from inference worker {self.worker_id} - output queue full")
            except Exception as put_exc:
                self.messages_dropped_output += 1
                self.logger.error(f"Failed to put video chunk output to queue in worker {self.worker_id}: {str(put_exc)}")
            
            # Update metrics
            inference_time = asyncio.get_event_loop().time() - start_time
            self.total_inference_time += inference_time
            self.messages_processed += 1
            self.last_inference_time = datetime.now(timezone.utc)
            self.logger.debug(
                f"Video-chunk inference done key={original_message.get('message_key')} time_ms={int(inference_time*1000)}"
            )
            
        except asyncio.TimeoutError:
            self.logger.error(f"Video chunk inference timeout in worker {self.worker_id}")
        except Exception as exc:
            self.logger.error(f"Video chunk inference error in worker {self.worker_id}: {str(exc)}")
    
    def _create_result_message(
        self,
        original_message: Dict[str, Any],
        model_result: Any,
    ) -> Dict[str, Any]:
        """Create a result message from inference results."""
        self.global_counter += 1
        return {
            "message_key": original_message.get("message_key"),
            "input_stream": original_message.get("input_stream"),
            "camera_info": original_message.get("camera_info"),
            "model_result": model_result,
            "inference_timestamp": datetime.now(timezone.utc),
            "inference_worker_id": self.worker_id,
            "original_timestamp": original_message.get("timestamp"),
            "consumer_worker_id": original_message.get("consumer_worker_id"),
            "stream_info": original_message.get("stream_info"),
            "input_content": original_message.get("input_content"),
            "input_hash": original_message.get("input_hash"), # self.global_counter fallback
            "global_counter": original_message.get("global_counter", self.global_counter),
        }

    def _create_video_chunk_result_message(
        self,
        video_chunk: Dict[str, Any],
        original_message: Dict[str, Any],
        model_result: Any,
    ) -> Dict[str, Any]:
        """Create a result message for a video chunk."""
        # Create modified input stream to reflect video chunk
        input_stream = original_message.get("input_stream", {}).copy()
        input_stream.update({
            "stream_unit": "segment",
            "frame_count": video_chunk.get("frame_count", 1),
            "start_frame": 0,
            "end_frame": video_chunk.get("frame_count", 1) - 1,
        })
        
        return {
            "message_key": original_message.get("message_key"),
            "input_stream": input_stream,
            "camera_info": original_message.get("camera_info"),
            "model_result": model_result,
            "inference_timestamp": datetime.now(timezone.utc),
            "inference_worker_id": self.worker_id,
            "original_timestamp": original_message.get("timestamp"),
            "consumer_worker_id": original_message.get("consumer_worker_id"),
            "stream_info": original_message.get("stream_info"),
            "input_content": original_message.get("input_content"),
            "input_hash": original_message.get("input_hash"),
            "video_chunk_info": {
                "frame_count": video_chunk.get("frame_count"),
                "duration_seconds": video_chunk.get("duration_seconds"),
                "fps": video_chunk.get("fps"),
                "chunk_created_time": video_chunk.get("chunk_created_time"),
            }
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get worker metrics."""
        avg_inference_time = 0.0
        if self.messages_processed > 0:
            avg_inference_time = self.total_inference_time / self.messages_processed
        
        # Calculate cache hit rate
        total_cache_requests = self.cache_hits + self.cache_misses
        cache_hit_rate = (self.cache_hits / total_cache_requests) if total_cache_requests > 0 else 0.0
        
        metrics = {
            "worker_id": self.worker_id,
            "is_running": self.is_running,
            "is_active": self.is_active,
            "messages_processed": self.messages_processed,
            "messages_failed": self.messages_failed,
            "messages_output": self.messages_output,
            "messages_dropped_output": self.messages_dropped_output,
            "avg_inference_time": avg_inference_time,
            "total_inference_time": self.total_inference_time,
            "last_inference_time": self.last_inference_time.isoformat() if self.last_inference_time else None,
            "input_queue_size": self.input_queue.qsize(),
            "output_queue_size": self.output_queue.qsize(),
            "frames_buffered": self.frames_buffered,
            "video_chunks_created": self.video_chunks_created,
            "video_chunks_processed": self.video_chunks_processed,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": cache_hit_rate,
            "cached_streams": len(self.frame_cache),
        }
        
        # Add video buffer metrics if available
        if self.video_buffer_manager:
            metrics["video_buffer_metrics"] = self.video_buffer_manager.get_metrics()
        
        return metrics
    
    def reset_metrics(self) -> None:
        """Reset worker metrics."""
        self.messages_processed = 0
        self.messages_failed = 0
        self.messages_output = 0
        self.messages_dropped_output = 0
        self.total_inference_time = 0.0
        self.last_inference_time = None
        self.frames_buffered = 0
        self.video_chunks_created = 0
        self.video_chunks_processed = 0
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Clear frame cache and last inference results
        self.frame_cache.clear()
        self.last_inference_results.clear()
        
        # Reset video buffer metrics if available
        if self.video_buffer_manager:
            self.video_buffer_manager.reset_metrics()