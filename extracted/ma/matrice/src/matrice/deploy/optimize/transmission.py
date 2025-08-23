"""Shared input transmission handlers for client and server.

This module centralizes the logic for determining how frames are transmitted
from the client (full/difference/skip) and how they are handled on the server
side (cache reuse, difference reconstruction, similarity checks).
"""
import base64
import hashlib
import logging
from typing import Any, Dict, Optional, Tuple, Union

import cv2
import numpy as np
from datetime import datetime, timezone

from .frame_comparators import SSIMComparator
from .frame_difference import FrameDifferenceProcessor

logger = logging.getLogger(__name__)


class ClientTransmissionHandler:
    """Client-side transmission handler implementing two-threshold logic.

    Responsibilities:
    - Maintain last frame per stream for SSIM reference
    - Decide strategy: full, difference, or skip
    - Produce difference payload (base64-encoded JPEG) and metadata
    - Track last full-frame input hash for server cache linking
    """

    def __init__(
        self,
        threshold_a: float = 0.95,
        threshold_b: float = 0.85,
    ) -> None:
        self.threshold_a = threshold_a
        self.threshold_b = threshold_b
        self.ssim_comparator = SSIMComparator(threshold=threshold_a)
        self.difference_processor = FrameDifferenceProcessor()

        # Client-side caches
        self.frame_cache: Dict[str, np.ndarray] = {}
        self.last_frame_hashes: Dict[str, str] = {}

    # -----------------------------
    # Strategy Decision
    # -----------------------------
    def decide_transmission( # TODO: Enable this after testing and hanlding async and send the reconstructed frame from the server
        self,
        frame: np.ndarray,
        stream_key: str,
    ) -> Tuple[str, Dict[str, Any]]:
        """Determine transmission strategy for a frame.

        Returns: (strategy, data)
          strategy in {"full", "difference", "skip"}
          data contains similarity and optional diff payload metadata
        """
        try:
            if stream_key not in self.frame_cache:
                self.frame_cache[stream_key] = frame.copy()
                return "full", {"reason": "first_frame", "similarity_score": 0.0}

            ref = self.frame_cache[stream_key]
            # is_similar, score = self.ssim_comparator.compare(ref, frame, stream_key)

            # if score >= self.threshold_a:
            #     return "skip", {"similarity_score": float(score), "reason": "high_similarity"}
            # elif score >= self.threshold_b:
            #     diff_data, diff_meta = self.difference_processor.calculate_frame_difference(ref, frame)
            #     if diff_meta.get("has_changes", False):
            #         return "difference", {
            #             "similarity_score": float(score),
            #             "difference_data": diff_data,
            #             "difference_metadata": diff_meta,
            #             "reason": "medium_similarity",
            #         }
            #     return "skip", {"similarity_score": float(score), "reason": "no_changes"}
            # else:
            #     # Low similarity, update cache immediately
            self.frame_cache[stream_key] = frame.copy()
            return "full", {"similarity_score": 0, "reason": "low_similarity"}
        except Exception as exc:
            logger.warning("Transmission decision error: %s", str(exc))
            # Fallback to full frame to keep pipeline robust
            self.frame_cache[stream_key] = frame.copy()
            return "full", {"reason": "error_fallback", "error": str(exc)}

    def encode_difference(
        self,
        difference_data: np.ndarray,
        difference_metadata: Dict[str, Any],
        quality: int,
    ) -> bytes:
        """Encode difference np.ndarray to raw bytes suitable for transport."""
        encoded_b64 = self.difference_processor.encode_frame_difference(
            difference_data, difference_metadata, compression_quality=quality
        )
        return base64.b64decode(encoded_b64) if encoded_b64 else b""

    def compute_and_store_full_frame_hash(
        self, stream_key: str, full_jpeg_bytes: bytes
    ) -> str:
        """Compute deterministic MD5 (non-security) and store it for reference."""
        try:
            md5 = hashlib.md5(full_jpeg_bytes, usedforsecurity=False).hexdigest()
            self.last_frame_hashes[stream_key] = md5
            return md5
        except Exception:
            return ""

    # -----------------------------
    # High-level orchestration for client
    # -----------------------------
    def _build_stream_metadata(
        self,
        input_source: Union[str, int],
        stream_key: Optional[str],
        video_props: Dict[str, Any],
        fps: int,
        quality: int,
        actual_width: int,
        actual_height: int,
        stream_type: str,
        frame_counter: int,
        is_video_chunk: bool = False,
        chunk_duration_seconds: Optional[float] = None,
        chunk_frames: Optional[int] = None,
        camera_location: Optional[str] = None,
    ) -> Dict[str, Any]:
        original_fps = video_props.get("original_fps", 0)
        frame_sample_rate = original_fps / fps if (original_fps and fps) else 1.0

        def _get_video_format(inp: Union[str, int]) -> str:
            if isinstance(inp, str) and "." in inp:
                return "." + inp.split("?")[0].split(".")[-1].lower()
            return ".mp4"

        def _calc_video_timestamp(frame_num: int, src_fps: float) -> str:
            total_seconds = frame_num / src_fps if src_fps else 0.0
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            milliseconds = int(round((total_seconds - int(total_seconds)) * 1000))
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

        if is_video_chunk and chunk_duration_seconds is not None:
            duration = chunk_duration_seconds
            frame_count = (chunk_frames if chunk_frames is not None else int(duration * fps)) or 1
        else:
            duration = 1.0 / fps if fps else 0.0
            frame_count = 1

        return {
            "fps": fps,
            "original_fps": original_fps,
            "frame_sample_rate": frame_sample_rate,
            "video_timestamp": _calc_video_timestamp(frame_counter, original_fps),
            "start_frame": frame_counter,
            "end_frame": frame_counter + frame_count - 1,
            "quality": quality,
            "width": actual_width,
            "height": actual_height,
            "is_video_chunk": is_video_chunk,
            "chunk_duration_seconds": duration,
            "video_properties": video_props,
            "video_format": _get_video_format(input_source),
            "stream_type": stream_type,
            "camera_location": camera_location or "Unknown Location",
        }

    def prepare_transmission(
        self,
        frame: np.ndarray,
        *,
        stream_key: str,
        input_source: Union[str, int],
        video_props: Dict[str, Any],
        fps: int,
        quality: int,
        actual_width: int,
        actual_height: int,
        stream_type: str,
        frame_counter: int,
        is_video_chunk: bool = False,
        chunk_duration_seconds: Optional[float] = None,
        chunk_frames: Optional[int] = None,
        camera_location: Optional[str] = None,
    ) -> Tuple[bytes, Dict[str, Any], str]:
        """Prepare bytes payload and metadata for transport.

        Returns (input_bytes, metadata, strategy)
        """
        strategy, strategy_data = self.decide_transmission(frame, stream_key)

        metadata = self._build_stream_metadata(
            input_source,
            stream_key,
            video_props,
            fps,
            quality,
            actual_width,
            actual_height,
            stream_type,
            frame_counter,
            is_video_chunk,
            chunk_duration_seconds,
            chunk_frames,
            camera_location,
        )
        metadata["transmission_strategy"] = strategy
        if "similarity_score" in strategy_data:
            metadata["similarity_score"] = strategy_data["similarity_score"]

        ref_key = stream_key or "default"
        if ref_key in self.last_frame_hashes:
            metadata["reference_input_hash"] = self.last_frame_hashes[ref_key]

        if strategy == "skip":
            metadata["skip_reason"] = strategy_data.get("reason", "unknown")
            return b"", metadata, strategy

        if strategy == "difference":
            diff_data = strategy_data.get("difference_data")
            diff_meta = strategy_data.get("difference_metadata", {})
            metadata["difference_metadata"] = diff_meta
            diff_bytes = self.encode_difference(diff_data, diff_meta, quality)
            if not diff_bytes:
                # Fallback to full
                strategy = "full"
                metadata["transmission_strategy"] = strategy
            else:
                return diff_bytes, metadata, strategy

        # Full frame path
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        try:
            _, buffer = cv2.imencode(".jpg", frame, encode_params)
        except Exception:
            _, buffer = cv2.imencode(".jpg", frame)
        full_bytes = buffer.tobytes()
        # Store hash for future reference
        self.compute_and_store_full_frame_hash(stream_key or "default", full_bytes)
        return full_bytes, metadata, "full"


class ServerTransmissionHandler:
    """Server-side transmission handler for intelligent input handling.

    Responsibilities:
    - Interpret transmission_strategy from client (skip/difference/full)
    - Resolve cache hits for skip signals
    - Reconstruct frames for difference payloads
    - Perform SSIM similarity checks for optional skipping
    """

    def __init__(self, ssim_threshold: float = 0.95) -> None:
        self.ssim_comparator = SSIMComparator(threshold=ssim_threshold)
        self.diff_processor = FrameDifferenceProcessor()

    def decide_action(
        self,
        message: Dict[str, Any],
        cache_manager,
        frame_cache: Dict[str, np.ndarray],
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Decide how to handle an incoming message.

        Returns (action, payload):
          - ("cached", cached_result)
          - ("similar", None)
          - ("process_difference", None) -> call reconstruct() then process
          - ("process", None)
        """
        stream_key = message.get("message_key", "default")
        input_hash = message.get("input_hash")
        strategy = message.get("transmission_strategy") or message.get("stream_info", {}).get("transmission_strategy", "full")

        # Skip strategy -> cache reuse
        if strategy == "skip":
            reference_hash = (
                message.get("stream_info", {}).get("reference_input_hash")
                or input_hash
            )
            if reference_hash:
                cached = cache_manager.get_cached_result(reference_hash, stream_key)
                if cached is not None:
                    logger.debug(
                        f"decide_action key={stream_key} strat=skip -> cached_hit ref_hash={reference_hash}"
                    )
                    return "cached", cached
            # Fallback: treat as similar to reduce load
            logger.debug(
                f"decide_action key={stream_key} strat=skip -> no_cache -> similar"
            )
            return "similar", None

        # Difference strategy -> reconstruct then process
        if strategy == "difference":
            logger.debug(
                f"decide_action key={stream_key} strat=difference -> reconstruct"
            )
            return "process_difference", None

        # TODO: Enable this after testing and hanlding async and optimal threshold
        # Full (or unknown) -> optionally check SSIM to skip redundant work
        # if self._is_similar_to_cached_frame(message, frame_cache):
        #     logger.debug(
        #         f"decide_action key={stream_key} strat=full -> similar_by_ssim"
        #     )
        #     return "similar", None

        logger.debug(
            f"decide_action key={stream_key} strat={strategy} -> process"
        )
        return "process", None

    def reconstruct_from_difference(
        self,
        message: Dict[str, Any],
        frame_cache: Dict[str, np.ndarray],
    ) -> Tuple[Optional[bytes], Optional[str]]:
        """Reconstruct full frame from difference; returns (jpeg_bytes, effective_hash)."""
        stream_key = message.get("message_key", "default")
        stream_info = message.get("stream_info", {})
        input_content = message.get("input_content")  # raw bytes (decoded)

        if not input_content:
            raise ValueError("No difference data provided")

        if stream_key not in frame_cache:
            raise ValueError("No reference frame available for reconstruction")

        # Decode difference JPEG to ndarray
        diff_frame = cv2.imdecode(np.frombuffer(input_content, np.uint8), cv2.IMREAD_COLOR)
        if diff_frame is None:
            raise ValueError("Failed to decode difference frame")

        reference_frame = frame_cache[stream_key]
        reconstructed = self.diff_processor.reconstruct_frame(reference_frame, diff_frame, stream_info.get("difference_metadata", {}))
        if reconstructed is None or reconstructed.size == 0:
            raise ValueError("Reconstructed frame is invalid")

        # Update cache reference frame
        frame_cache[stream_key] = reconstructed

        # Encode back to JPEG bytes and compute deterministic hash
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 95]
        _, buffer = cv2.imencode(".jpg", reconstructed, encode_params)
        full_bytes = buffer.tobytes()

        try:
            reference_hash = stream_info.get("reference_input_hash")
            effective_hash = reference_hash or hashlib.md5(full_bytes, usedforsecurity=False).hexdigest()
        except Exception:
            effective_hash = None

        return full_bytes, effective_hash

    def update_frame_cache_from_message(
        self, message: Dict[str, Any], frame_cache: Dict[str, np.ndarray]
    ) -> None:
        """If message has image bytes, decode and store for SSIM reference."""
        try:
            stream_key = message.get("message_key", "default")
            content = message.get("input_content")
            if not content:
                return
            frame = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                frame_cache[stream_key] = frame
        except Exception as exc:
            logger.debug("Failed updating frame cache: %s", str(exc))

    def _is_similar_to_cached_frame(
        self, message: Dict[str, Any], frame_cache: Dict[str, np.ndarray]
    ) -> bool:
        try:
            stream_key = message.get("message_key", "default")
            content = message.get("input_content")
            if not content or stream_key not in frame_cache:
                return False
            current = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
            if current is None:
                return False
            cached = frame_cache[stream_key]
            is_similar, _ = self.ssim_comparator.compare(cached, current, stream_key)
            return is_similar
        except Exception:
            return False

    # -----------------------------
    # Kafka message normalization
    # -----------------------------
    def process_input_message(
        self,
        raw_message_value: Dict[str, Any],
        message_key: Optional[str],
        consumer_worker_id: str,
    ) -> Dict[str, Any]:
        """Normalize raw Kafka message 'value' into a processed message structure.

        Handles transmission_strategy: 'skip', 'difference', 'full'.
        Decodes content accordingly and carries through strategy metadata.
        """
        if not isinstance(raw_message_value, dict):
            raise ValueError("Invalid message format: expected dict for 'value'")

        input_stream = raw_message_value.get("input_stream", {})
        if not isinstance(input_stream, dict):
            raise ValueError("Invalid message: 'input_stream' missing or not a dict")

        input_content_b64 = input_stream.get("content")
        input_hash = input_stream.get("input_hash")
        camera_info = input_stream.get("camera_info")

        transmission_strategy = input_stream.get("transmission_strategy", "full")
        similarity_score = input_stream.get("similarity_score", 0.0)

        # Decode content according to strategy
        if transmission_strategy == "skip":
            decoded_content = b""
        elif transmission_strategy == "difference":
            if not input_content_b64:
                raise ValueError("Missing 'content' for difference transmission")
            try:
                decoded_content = base64.b64decode(input_content_b64)
            except Exception as exc:
                raise ValueError(f"Failed to decode base64 difference data: {str(exc)}")
        else:
            if not input_content_b64:
                raise ValueError("Missing 'content' field for full-frame transmission")
            try:
                decoded_content = base64.b64decode(input_content_b64)
            except Exception as exc:
                raise ValueError(f"Failed to decode base64 full frame data: {str(exc)}")

        # Build stream_info with input_settings and strategy details
        stream_info: Dict[str, Any] = {
            "input_settings": {
                "start_frame": input_stream.get("start_frame"),
                "end_frame": input_stream.get("end_frame"),
                "stream_unit": input_stream.get("stream_unit"),
                "input_order": input_stream.get("input_order"),
                "original_fps": input_stream.get("original_fps"),
            },
            "transmission_strategy": transmission_strategy,
            "similarity_score": similarity_score,
            "camera_location": camera_info.get("location") if camera_info else "Unknown Location",
        }

        if transmission_strategy == "skip":
            stream_info["skip_reason"] = input_stream.get("skip_reason", "unknown")
            ref_hash = input_stream.get("reference_input_hash")
            if ref_hash:
                stream_info["reference_input_hash"] = ref_hash
        elif transmission_strategy == "difference":
            stream_info["difference_metadata"] = input_stream.get("difference_metadata", {})
            ref_hash = input_stream.get("reference_input_hash")
            if ref_hash:
                stream_info["reference_input_hash"] = ref_hash

        return {
            "message_key": message_key,
            "input_content": decoded_content,
            "input_stream": input_stream,
            "stream_info": stream_info,
            "camera_info": camera_info,
            "input_hash": input_hash,
            "timestamp": datetime.now(timezone.utc),
            "consumer_worker_id": consumer_worker_id,
            "transmission_strategy": transmission_strategy,
            "similarity_score": similarity_score,
        }


