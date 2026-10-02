# Copyright (c) 2025 LiveKit, Inc. All rights reserved.
# Proprietary and confidential.

from __future__ import annotations

import numpy as np
from livekit import rtc

from ._ffi import (  # type: ignore[import-not-found]
    Credentials,
    FilterError,
    VivaMode,
    KrispVivaFilter,
    KrispVivaFilterSettings,
    NativeInt16BufferMut,
    StreamInfo,
)
from .log import logger

__all__ = ["VivaMode", "KrispVivaFilterFrameProcessor"]


class KrispVivaFilterFrameProcessor(rtc.FrameProcessor[rtc.AudioFrame]):
    """Krisp Viva noise filter as a LiveKit FrameProcessor.

    Construction is cheap; the underlying SDK is initialized on the first
    frame after credentials arrive (so the blocking authorize HTTP call runs
    on the audio thread, not on the room task that delivers credentials).
    """

    def __init__(
        self,
        *,
        mode: VivaMode | None = VivaMode.VOICE_ISOLATION,
        noise_suppression_level: float = 90.0,
        frame_duration_ms: int | None = 10,
        sample_rate: int | None = 16_000,
    ) -> None:
        self._mode = mode
        self._level = float(noise_suppression_level)
        self._frame_duration_ms = frame_duration_ms
        self._enabled = True

        self._filter: KrispVivaFilter | None = None
        self._info: StreamInfo | None = None
        self._credentials: Credentials | None = None
        self._effective_rate: int | None = sample_rate
        self._warned_channels = False

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @property
    def noise_suppression_level(self) -> float:
        return self._level

    @noise_suppression_level.setter
    def noise_suppression_level(self, value: float) -> None:
        clamped = max(0.0, min(100.0, float(value)))
        self._level = clamped
        if self._filter is not None:
            self._filter.set_noise_suppression_level(clamped)

    def _on_stream_info_updated(
        self,
        *,
        room_name: str,
        participant_identity: str,
        publication_sid: str,
    ) -> None:
        self._info = StreamInfo(
            room_id="",
            room_name=room_name,
            participant_identity=participant_identity,
            participant_id="",
            track_id=publication_sid,
        )
        if self._filter is not None:
            self._filter.update_stream_info(self._info)

    def _on_credentials_updated(self, *, token: str, url: str) -> None:
        self._credentials = Credentials(token=token, url=url)
        if self._filter is not None:
            try:
                self._filter.update_credentials(self._credentials)
            except FilterError as e:
                logger.error("Krisp credential rotation failed: %s", e)

    def _process(self, frame: rtc.AudioFrame) -> rtc.AudioFrame:
        if not self._enabled:
            return frame
        if self._credentials is None:
            return frame
        if frame.num_channels != 1:
            # Krisp NC expects mono. Multi-channel support would require
            # processing each channel independently. Pass through untouched.
            if not self._warned_channels:
                logger.warning(
                    "Krisp filter not applied: expected mono audio but got %d "
                    "channels; frames are passed through unprocessed.",
                    frame.num_channels,
                )
                self._warned_channels = True
            return frame

        if self._filter is None or self._effective_rate != frame.sample_rate:
            try:
                self._filter = KrispVivaFilter(
                    KrispVivaFilterSettings(
                        mode=self._mode,
                        sample_rate=frame.sample_rate,
                        frame_duration_ms=self._frame_duration_ms,
                        noise_suppression_level=self._level,
                        credentials=self._credentials,
                    )
                )
                self._effective_rate = frame.sample_rate
                if self._info is not None and self._filter is not None:
                    self._filter.update_stream_info(self._info)
            except FilterError as e:
                logger.error("Krisp filter init failed: %s", e)
                self._filter = None
                return frame

        in_arr = np.frombuffer(frame.data, dtype=np.int16)
        out_arr = np.empty_like(in_arr)
        in_buf = NativeInt16BufferMut(ptr=in_arr.ctypes.data, len=len(in_arr))
        out_buf = NativeInt16BufferMut(ptr=out_arr.ctypes.data, len=len(out_arr))
        try:
            self._filter.process(in_buf, out_buf)
        except FilterError as e:
            logger.error("Krisp processing failed: %s", e)
            return frame

        return rtc.AudioFrame(
            data=out_arr.tobytes(),
            sample_rate=frame.sample_rate,
            num_channels=frame.num_channels,
            samples_per_channel=frame.samples_per_channel,
            userdata=frame.userdata,
        )

    def _close(self) -> None:
        if self._filter is not None:
            self._filter.close_session()
        self._effective_rate = None
        self._info = None
