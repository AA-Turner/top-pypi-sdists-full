"""Main client for KugelAudio SDK."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import threading
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from urllib.parse import urljoin, urlparse

import httpx
from pathlib import Path

if TYPE_CHECKING:
    from kugelaudio.streaming import (
        MultiContextSession,
        StreamingSession,
        StreamingSessionSync,
    )
from kugelaudio.exceptions import (
    AuthenticationError,
    ConnectionError as KugelAudioConnectionError,
    InsufficientCreditsError,
    KugelAudioError,
    RateLimitError,
    ValidationError,
    classify_http_response,
    classify_ws_close,
    classify_ws_frame,
    classify_ws_handshake_error,
    ws_handshake_error_types,
)
from kugelaudio.models import (
    AudioChunk,
    AudioResponse,
    GenerateRequest,
    Model,
    StreamConfig,
    Voice,
    VoiceDetail,
    VoiceListResponse,
    VoiceReference,
    WordTimestamp,
)

logger = logging.getLogger(__name__)

_language_warning_lock = threading.Lock()
_language_warning_logged = False


def _warn_if_no_language(language: Optional[str], normalize: bool = True) -> None:
    """Log a one-time warning when normalization is enabled without an explicit language."""
    global _language_warning_logged
    if language is None and normalize and not _language_warning_logged:
        with _language_warning_lock:
            if not _language_warning_logged:
                _language_warning_logged = True
                logger.warning(
                    "No 'language' set with normalization enabled — the server will "
                    "auto-detect the language, adding ~60-150 ms to TTFA. Set language "
                    "(e.g., language='en') for optimal latency."
                )


# Default API endpoints
# By default, TTS WebSocket connects to the same URL as the API
# (the backend proxies WebSocket requests to the TTS server)
DEFAULT_API_URL = "https://api.kugelaudio.com"
DEFAULT_TTS_URL = None  # If None, uses api_url

# Region-to-URL mapping for multi-region deployments
REGION_URLS = {
    "eu": "https://api.kugelaudio.com",
    "us": "https://us-api.kugelaudio.com",
    "global": "https://global-api.kugelaudio.com",
}

# Prefixes that can be prepended to API keys to select a region
_REGION_PREFIXES = ("eu-", "us-", "global-")


def _parse_api_key(api_key: str) -> tuple[str, Optional[str]]:
    """Strip a region prefix from an API key.

    Returns:
        (clean_key, detected_region) — detected_region is None when no prefix is present.
    """
    for prefix in _REGION_PREFIXES:
        if api_key.startswith(prefix):
            return api_key[len(prefix):], prefix.rstrip("-")
    return api_key, None


class ModelsResource:
    """Resource for listing available TTS models."""

    def __init__(self, client: KugelAudio):
        self._client = client

    def list(self) -> List[Model]:
        """List available TTS models.

        Returns:
            List of available models
        """
        response = self._client._request("GET", "/v1/models")
        return [Model.from_dict(m) for m in response.get("models", [])]


class VoicesResource:
    """Resource for managing voices."""

    def __init__(self, client: KugelAudio):
        self._client = client

    def list(
        self,
        language: Optional[str] = None,
        include_public: bool = True,
        limit: int = 20,
        offset: int = 0,
    ) -> VoiceListResponse:
        """List available voices.

        Args:
            language: Filter by language code (e.g., 'en', 'de')
            include_public: Include public voices
            limit: Maximum number of voices to return (max 100)
            offset: Number of voices to skip for pagination

        Returns:
            Paginated voice list response
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if language:
            params["language"] = language
        if include_public:
            params["include_public"] = "true"

        response = self._client._request("GET", "/v1/voices", params=params)
        return VoiceListResponse.from_dict(response)

    def get(self, voice_id: int) -> VoiceDetail:
        """Get a specific voice by ID.

        Args:
            voice_id: Voice ID

        Returns:
            Detailed voice information
        """
        response = self._client._request("GET", f"/v1/voices/{voice_id}")
        return VoiceDetail.from_dict(response)

    def create(
        self,
        name: str,
        sex: str,
        *,
        description: str = "",
        category: str = "conversational",
        age: str = "middle_age",
        quality: str = "mid",
        supported_languages: Optional[List[str]] = None,
        is_public: bool = False,
        sample_text: str = "",
        reference_files: Optional[List[Union[str, Path]]] = None,
    ) -> VoiceDetail:
        """Create a new voice.

        Args:
            name: Voice name
            sex: Voice sex ('male' or 'female')
            description: Human-readable description
            category: Voice category (e.g., 'conversational', 'narration')
            age: Voice age ('young', 'middle_age', 'old')
            quality: Voice quality ('low', 'mid', 'high')
            supported_languages: List of language codes (default: ['en'])
            is_public: Whether the voice should be public
            sample_text: Text used for automatic sample generation
            reference_files: Optional list of reference audio file paths to upload

        Returns:
            Created voice details
        """
        metadata: Dict[str, Any] = {
            "name": name,
            "sex": sex,
            "description": description,
            "category": category,
            "age": age,
            "quality": quality,
            "supported_languages": supported_languages or ["en"],
            "is_public": is_public,
            "sample_text": sample_text,
        }

        files_list: List[Tuple[str, Tuple[Optional[str], Any, str]]] = [
            ("metadata", (None, json.dumps(metadata), "application/json")),
        ]
        opened_files: List[IO[bytes]] = []
        try:
            if reference_files:
                for fpath in reference_files:
                    p = Path(fpath)
                    fh = open(p, "rb")
                    opened_files.append(fh)
                    files_list.append(("files", (p.name, fh, "audio/wav")))

            response = self._client._request_multipart(
                "POST", "/v1/voices", files=files_list
            )
        finally:
            for fh in opened_files:
                fh.close()

        return VoiceDetail.from_dict(response)

    def update(
        self,
        voice_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        age: Optional[str] = None,
        sex: Optional[str] = None,
        quality: Optional[str] = None,
        supported_languages: Optional[List[str]] = None,
        is_public: Optional[bool] = None,
        sample_text: Optional[str] = None,
    ) -> VoiceDetail:
        """Update an existing voice.

        Only provided fields will be updated. Pass None to leave a field unchanged.

        Args:
            voice_id: Voice ID to update
            name: New voice name
            description: New description
            category: New category
            age: New age
            sex: New sex
            quality: New quality
            supported_languages: New list of language codes
            is_public: New public visibility
            sample_text: New sample text

        Returns:
            Updated voice details
        """
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if category is not None:
            payload["category"] = category
        if age is not None:
            payload["age"] = age
        if sex is not None:
            payload["sex"] = sex
        if quality is not None:
            payload["quality"] = quality
        if supported_languages is not None:
            payload["supported_languages"] = supported_languages
        if is_public is not None:
            payload["is_public"] = is_public
        if sample_text is not None:
            payload["sample_text"] = sample_text

        response = self._client._request(
            "PATCH", f"/v1/voices/{voice_id}", json_data=payload
        )
        return VoiceDetail.from_dict(response)

    def delete(self, voice_id: int) -> None:
        """Delete a voice.

        Args:
            voice_id: Voice ID to delete
        """
        self._client._request("DELETE", f"/v1/voices/{voice_id}")

    # -- Reference management --

    def list_references(self, voice_id: int) -> List[VoiceReference]:
        """List reference audio files for a voice.

        Args:
            voice_id: Voice ID

        Returns:
            List of voice references
        """
        response = self._client._request(
            "GET", f"/v1/voices/{voice_id}/references"
        )
        return [VoiceReference.from_dict(r) for r in response.get("references", [])]

    def add_reference(
        self,
        voice_id: int,
        file: Union[str, Path],
        *,
        reference_text: str = "",
    ) -> VoiceReference:
        """Upload a reference audio file to a voice.

        Args:
            voice_id: Voice ID
            file: Path to the reference audio file
            reference_text: Transcript of the reference audio

        Returns:
            Created reference metadata
        """
        p = Path(file)
        fh = open(p, "rb")
        try:
            files_list: List[Tuple[str, Tuple[Optional[str], Any, str]]] = [
                ("file", (p.name, fh, "audio/wav")),
            ]
            if reference_text:
                files_list.append(
                    ("reference_text", (None, reference_text, "text/plain")),
                )

            response = self._client._request_multipart(
                "POST", f"/v1/voices/{voice_id}/references", files=files_list
            )
        finally:
            fh.close()

        return VoiceReference.from_dict(response)

    def delete_reference(self, voice_id: int, reference_id: int) -> None:
        """Delete a reference audio file from a voice.

        Args:
            voice_id: Voice ID
            reference_id: Reference ID to delete
        """
        self._client._request(
            "DELETE", f"/v1/voices/{voice_id}/references/{reference_id}"
        )

    # -- Publishing --

    def publish(self, voice_id: int) -> VoiceDetail:
        """Request publication of a voice.

        Sets the voice as public and marks it as pending verification.
        An admin must verify the voice before it appears in public listings.

        Args:
            voice_id: Voice ID

        Returns:
            Updated voice details
        """
        response = self._client._request(
            "POST", f"/v1/voices/{voice_id}/publish"
        )
        return VoiceDetail.from_dict(response)

    # -- Sample generation --

    def generate_sample(self, voice_id: int) -> VoiceDetail:
        """Trigger sample audio generation for a voice.

        Uses the voice's sample_text (or a default) to generate a preview sample.

        Args:
            voice_id: Voice ID

        Returns:
            Updated voice details with sample_url
        """
        response = self._client._request(
            "POST", f"/v1/voices/{voice_id}/generate-sample"
        )
        return VoiceDetail.from_dict(response)


class TTSResource:
    """Resource for text-to-speech generation."""

    def __init__(self, client: KugelAudio):
        self._client = client
        self._ws_connection: Optional[Any] = None
        self._ws_lock = asyncio.Lock()
        self._ws_url: Optional[str] = None
        self._keepalive_task: Optional[asyncio.Task[None]] = None

    def generate(
        self,
        text: str,
        model_id: str = "kugel-1-turbo",
        voice_id: Optional[int] = None,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        sample_rate: int = 24000,
        normalize: bool = True,
        language: Optional[str] = None,
        word_timestamps: bool = False,
        speed: float = 1.0,
    ) -> AudioResponse:
        """Generate audio from text (non-streaming).

        This method collects all audio chunks internally and returns
        the complete audio response.

        Args:
            text: Text to synthesize
            model_id: Model to use ('kugel-1-turbo' or 'kugel-1')
            voice_id: Voice ID to use
            cfg_scale: CFG scale for generation
            max_new_tokens: Maximum tokens to generate
            sample_rate: Output sample rate (24000)
            normalize: Enable text normalization (default: True).
                For best performance, specify the ``language`` parameter
                to skip auto-detection (~150 ms).
            language: ISO 639-1 language code for normalization (e.g., 'de', 'en').
                Supported: de, en, fr, es, it, pt, nl, pl, sv, da, no, fi, cs, hu, ro,
                el, uk, bg, tr, vi, ar, hi, zh, ja, ko, sk, sl, hr, sr, ru, he, fa,
                ur, bn, ta, yue, th, id, ms
            word_timestamps: Request word-level timestamps. When enabled,
                ``AudioResponse.word_timestamps`` will be populated with
                per-word timing boundaries.
            speed: Playback speed multiplier (0.8–1.2, default 1.0).
                Uses pitch-preserving WSOLA time-stretching.

        Returns:
            Complete audio response (with ``word_timestamps`` if requested)
        """
        # Use sync wrapper for async streaming
        chunks: List[AudioChunk] = []
        all_stamps: List[WordTimestamp] = []
        final_stats: Dict[str, Any] = {}

        for item in self.stream(
            text=text,
            model_id=model_id,
            voice_id=voice_id,
            cfg_scale=cfg_scale,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            sample_rate=sample_rate,
            normalize=normalize,
            language=language,
            word_timestamps=word_timestamps,
            speed=speed,
        ):
            if isinstance(item, AudioChunk):
                chunks.append(item)
            elif isinstance(item, list):
                all_stamps.extend(item)
            elif isinstance(item, dict) and item.get("final"):
                final_stats = item

        return AudioResponse.from_chunks(chunks, final_stats, all_stamps)

    def stream(
        self,
        text: str,
        model_id: str = "kugel-1-turbo",
        voice_id: Optional[int] = None,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        sample_rate: int = 24000,
        normalize: bool = True,
        language: Optional[str] = None,
        word_timestamps: bool = False,
        speed: float = 1.0,
    ) -> Iterator[Union[AudioChunk, List[WordTimestamp], Dict[str, Any]]]:
        """Stream audio from text via WebSocket.

        Yields audio chunks as they are generated. The final message
        contains stats about the generation.

        Args:
            text: Text to synthesize
            model_id: Model to use ('kugel-1-turbo' or 'kugel-1')
            voice_id: Voice ID to use
            cfg_scale: CFG scale for generation
            max_new_tokens: Maximum tokens to generate
            sample_rate: Output sample rate
            normalize: Enable text normalization (default: True).
                For best performance, specify the ``language`` parameter
                to skip auto-detection (~150 ms).
            language: ISO 639-1 language code for normalization (e.g., 'de', 'en').
                Supported: de, en, fr, es, it, pt, nl, pl, sv, da, no, fi, cs, hu, ro,
                el, uk, bg, tr, vi, ar, hi, zh, ja, ko, sk, sl, hr, sr, ru, he, fa,
                ur, bn, ta, yue, th, id, ms
            word_timestamps: Request word-level timestamps. When enabled, the
                server sends a ``word_timestamps`` message after audio containing
                per-word timing. Yielded as ``list[WordTimestamp]``.
            speed: Playback speed multiplier (0.8–1.2, default 1.0).
                Uses pitch-preserving WSOLA time-stretching.

        Yields:
            AudioChunk for audio data, list[WordTimestamp] for word timestamps,
            dict for final stats
        """
        import queue
        import threading

        # Use a thread-safe queue for true streaming
        result_queue: queue.Queue = queue.Queue()
        exception_holder: List[Exception] = []
        done_sentinel = object()

        async def collect():
            try:
                async for item in self.stream_async(
                    text=text,
                    model_id=model_id,
                    voice_id=voice_id,
                    cfg_scale=cfg_scale,
                    temperature=temperature,
                    max_new_tokens=max_new_tokens,
                    sample_rate=sample_rate,
                    normalize=normalize,
                    language=language,
                    word_timestamps=word_timestamps,
                    speed=speed,
                ):
                    result_queue.put(item)
            except Exception as e:
                exception_holder.append(e)
            finally:
                # Close the WS connection before the loop is destroyed
                # so the next sync call can create a fresh one on its own loop.
                await self._close_ws_connection()
                result_queue.put(done_sentinel)

        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(collect())
            finally:
                loop.close()

        # Reset the asyncio lock so it binds to the new thread's loop
        self._ws_lock = asyncio.Lock()

        # Start async collection in background thread
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()

        # Yield items as they arrive (true streaming)
        while True:
            item = result_queue.get()
            if item is done_sentinel:
                break
            yield item

        # Check for exceptions after streaming completes
        if exception_holder:
            raise exception_holder[0]

    async def _get_ws_connection(self, model_id: str) -> Any:
        """Get or create a WebSocket connection for the given model.

        This implements connection pooling to avoid the ~220ms connect
        overhead on each request.
        """
        try:
            import websockets
        except ImportError:
            raise ImportError(
                "websockets is required for streaming. Install with: pip install websockets"
            )

        # Build WebSocket URL
        ws_url = self._client._tts_url.replace("https://", "wss://").replace(
            "http://", "ws://"
        )
        ws_url = f"{ws_url}/ws/tts?api_key={self._client._api_key}"
        if model_id:
            ws_url += f"&model_id={model_id}"

        async with self._ws_lock:
            # Check if we have a valid connection for this URL
            # websockets uses .state (OPEN = 1) or .closed property
            if self._ws_connection is not None and self._ws_url == ws_url:
                try:
                    # Check if connection is still open
                    is_open = (
                        (
                            hasattr(self._ws_connection, "open")
                            and self._ws_connection.open
                        )
                        or (
                            hasattr(self._ws_connection, "state")
                            and self._ws_connection.state.name == "OPEN"
                        )
                        or (
                            hasattr(self._ws_connection, "closed")
                            and not self._ws_connection.closed
                        )
                    )
                    if is_open:
                        return self._ws_connection
                except Exception:
                    pass

            # Close old connection if URL changed
            if self._ws_connection is not None:
                try:
                    await self._ws_connection.close()
                except Exception:
                    pass
                self._ws_connection = None

            # Create new connection
            self._cancel_keepalive()
            self._ws_connection = await websockets.connect(ws_url, compression=None)
            self._ws_url = ws_url
            if self._client._keepalive_ping_interval is not None:
                self._keepalive_task = asyncio.create_task(
                    self._start_keepalive(self._ws_connection)
                )
            return self._ws_connection

    async def _start_keepalive(self, ws: Any) -> None:
        """Send periodic pings on the pooled connection to prevent idle timeouts."""
        interval = self._client._keepalive_ping_interval
        if interval is None:
            return
        try:
            while True:
                await asyncio.sleep(interval)
                if self._ws_connection is not ws:
                    break
                try:
                    await ws.ping()
                    logger.debug("Keepalive ping sent on pooled WebSocket")
                except Exception as e:
                    logger.debug("Keepalive ping failed (connection may be closed): %s", e)
                    break
        except asyncio.CancelledError:
            pass

    def _cancel_keepalive(self) -> None:
        if self._keepalive_task is not None and not self._keepalive_task.done():
            self._keepalive_task.cancel()
        self._keepalive_task = None

    async def _close_ws_connection(self) -> None:
        """Close the pooled WebSocket connection."""
        async with self._ws_lock:
            self._cancel_keepalive()
            if self._ws_connection is not None:
                try:
                    await self._ws_connection.close()
                except Exception:
                    pass
                self._ws_connection = None
                self._ws_url = None

    async def connect_async(self, model: str = "kugel-1-turbo") -> None:
        """Pre-establish WebSocket connection for faster first request.

        Call this at application startup to eliminate cold start latency
        (~300-600ms) from your first TTS request.

        Args:
            model: Model to connect for ('kugel-1-turbo' or 'kugel-1').
                   The connection is model-specific due to routing.

        Example:
            client = KugelAudio(api_key="...")

            # Pre-connect at startup
            await client.tts.connect_async()

            # First request is now fast (~100ms instead of ~500ms)
            async for chunk in client.tts.stream_async("Hello"):
                ...
        """
        await self._get_ws_connection(model)
        logger.info("WebSocket connection pre-established for model: %s", model)

    def connect(self, model: str = "kugel-1-turbo") -> None:
        """Pre-establish WebSocket connection for faster first request (sync version).

        Call this at application startup to eliminate cold start latency
        (~300-600ms) from your first TTS request.

        Args:
            model: Model to connect for ('kugel-1-turbo' or 'kugel-1').
                   The connection is model-specific due to routing.

        Example:
            client = KugelAudio(api_key="...")

            # Pre-connect at startup
            client.tts.connect()

            # First request is now fast (~100ms instead of ~500ms)
            for chunk in client.tts.stream("Hello"):
                ...
        """
        import threading

        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.connect_async(model))
            finally:
                loop.close()

        thread = threading.Thread(target=run)
        thread.start()
        thread.join()

    def is_connected(self) -> bool:
        """Check if WebSocket connection is established and open.

        Returns:
            True if connected and ready for requests.
        """
        if self._ws_connection is None:
            return False
        try:
            is_open = (
                (hasattr(self._ws_connection, "open") and self._ws_connection.open)
                or (
                    hasattr(self._ws_connection, "state")
                    and self._ws_connection.state.name == "OPEN"
                )
                or (
                    hasattr(self._ws_connection, "closed")
                    and not self._ws_connection.closed
                )
            )
            return is_open
        except Exception:
            return False

    async def stream_async(
        self,
        text: str,
        model_id: str = "kugel-1-turbo",
        voice_id: Optional[int] = None,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        sample_rate: int = 24000,
        reuse_connection: bool = True,
        normalize: bool = True,
        language: Optional[str] = None,
        word_timestamps: bool = False,
        speed: float = 1.0,
    ) -> AsyncIterator[Union[AudioChunk, List[WordTimestamp], Dict[str, Any]]]:
        """Stream audio asynchronously via WebSocket.

        Args:
            text: Text to synthesize
            model_id: Model to use ('kugel-1-turbo' or 'kugel-1')
            voice_id: Voice ID to use
            cfg_scale: CFG scale for generation
            max_new_tokens: Maximum tokens to generate
            sample_rate: Output sample rate
            reuse_connection: If True (default), reuse WebSocket connection
                for faster TTFA (~175ms vs ~390ms). Set to False to always
                create a new connection.
            normalize: Enable text normalization (default: True).
                For best performance, specify the ``language`` parameter
                to skip auto-detection (~150 ms).
            language: ISO 639-1 language code for normalization (e.g., 'de', 'en').
                Supported: de, en, fr, es, it, pt, nl, pl, sv, da, no, fi, cs, hu, ro,
                el, uk, bg, tr, vi, ar, hi, zh, ja, ko, sk, sl, hr, sr, ru, he, fa,
                ur, bn, ta, yue, th, id, ms
            word_timestamps: Request word-level timestamps. When enabled, the
                server sends a ``word_timestamps`` message after audio containing
                per-word timing. Yielded as ``list[WordTimestamp]``.
            speed: Playback speed multiplier (0.8–1.2, default 1.0).
                Uses pitch-preserving WSOLA time-stretching.

        Yields:
            AudioChunk for audio data, list[WordTimestamp] for word timestamps,
            dict for final stats
        """
        try:
            import websockets
        except ImportError:
            raise ImportError(
                "websockets is required for streaming. Install with: pip install websockets"
            )

        _warn_if_no_language(language, normalize)

        request_data = {
            "text": text,
            "model_id": model_id,
            "cfg_scale": cfg_scale,
            "max_new_tokens": max_new_tokens,
            "sample_rate": sample_rate,
            "normalize": normalize,
            "word_timestamps": word_timestamps,
            "speed": speed,
        }
        if voice_id is not None:
            request_data["voice_id"] = voice_id
        if language is not None:
            request_data["language"] = language
        if temperature is not None:
            request_data["temperature"] = temperature

        if reuse_connection:
            # Use connection pooling for faster TTFA
            ws = await self._get_ws_connection(model_id)
            try:
                await ws.send(json.dumps(request_data))

                while True:
                    try:
                        msg = await ws.recv()
                        data = json.loads(msg)

                        if data.get("error"):
                            raise classify_ws_frame(data)

                        if data.get("final"):
                            yield data
                            break

                        if data.get("audio"):
                            yield AudioChunk.from_dict(data)

                        if "word_timestamps" in data:
                            yield [
                                WordTimestamp.from_dict(w)
                                for w in data["word_timestamps"]
                            ]

                    except websockets.exceptions.ConnectionClosed as e:
                        # Connection was closed, clear pool and retry once
                        await self._close_ws_connection()
                        raise classify_ws_close(
                            getattr(e, "code", None), getattr(e, "reason", None)
                        ) from e

            except websockets.exceptions.ConnectionClosed:
                # Connection died, clear it from pool
                await self._close_ws_connection()
                raise

        else:
            # Original behavior: new connection per request
            ws_url = self._client._tts_url.replace("https://", "wss://").replace(
                "http://", "ws://"
            )
            ws_url = f"{ws_url}/ws/tts?api_key={self._client._api_key}"
            if model_id:
                ws_url += f"&model_id={model_id}"

            try:
                async with websockets.connect(ws_url) as ws:
                    await ws.send(json.dumps(request_data))

                    while True:
                        try:
                            msg = await ws.recv()
                            data = json.loads(msg)

                            if data.get("error"):
                                raise classify_ws_frame(data)

                            if data.get("final"):
                                yield data
                                break

                            if data.get("audio"):
                                yield AudioChunk.from_dict(data)

                            if "word_timestamps" in data:
                                yield [
                                    WordTimestamp.from_dict(w)
                                    for w in data["word_timestamps"]
                                ]

                        except websockets.exceptions.ConnectionClosed as e:
                            raise classify_ws_close(
                                getattr(e, "code", None),
                                getattr(e, "reason", None),
                            ) from e

            except ws_handshake_error_types(websockets) as e:
                typed = classify_ws_handshake_error(e)
                if typed is not None:
                    raise typed from e
                raise KugelAudioConnectionError(
                    f"KugelAudio WebSocket handshake failed: {e}."
                ) from e

    def streaming_session(
        self,
        voice_id: Optional[int] = None,
        model_id: Optional[str] = None,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        sample_rate: int = 24000,
        flush_timeout_ms: int = 500,
        normalize: bool = True,
        language: Optional[str] = None,
        word_timestamps: bool = False,
        speed: float = 1.0,
        on_word_timestamps: Optional[Callable[[List[WordTimestamp]], None]] = None,
    ) -> StreamingSession:
        """Create a streaming session for text-in/audio-out streaming.

        Use this when streaming text from an LLM and want audio as soon
        as complete sentences are available.

        Example:
            async with client.tts.streaming_session(voice_id=123) as session:
                async for token in llm_stream:
                    async for chunk in session.send(token):
                        play_audio(chunk)

                async for chunk in session.flush():
                    play_audio(chunk)

        Example with word timestamps:
            async with client.tts.streaming_session(
                voice_id=123, word_timestamps=True,
            ) as session:
                async for chunk in session.send("Hello world."):
                    play_audio(chunk)
                async for chunk in session.flush():
                    play_audio(chunk)

                for ts in session.last_word_timestamps:
                    print(f"{ts.word}: {ts.start_ms}-{ts.end_ms}ms")

        Args:
            voice_id: Voice ID to use
            model_id: Model to use (e.g., "kugel-1-turbo")
            cfg_scale: CFG scale for generation
            max_new_tokens: Maximum tokens per generation
            sample_rate: Output sample rate
            flush_timeout_ms: Auto-flush timeout in milliseconds
            normalize: Enable text normalization
            language: ISO 639-1 language code for normalization
            word_timestamps: Request per-chunk word-level timestamps
            speed: Playback speed multiplier (0.8–1.2, default 1.0).
                Uses pitch-preserving WSOLA time-stretching.
            on_word_timestamps: Callback ``(stamps: list[WordTimestamp]) -> None``
                invoked each time the server sends word timestamps.

        Returns:
            StreamingSession for async use
        """
        from kugelaudio.models import StreamConfig
        from kugelaudio.streaming import StreamingSession

        config = StreamConfig(
            voice_id=voice_id,
            model_id=model_id,
            cfg_scale=cfg_scale,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            sample_rate=sample_rate,
            flush_timeout_ms=flush_timeout_ms,
            normalize=normalize,
            language=language,
            word_timestamps=word_timestamps,
            speed=speed,
        )

        return StreamingSession(
            api_key=self._client._api_key,
            tts_url=self._client._tts_url,
            config=config,
            on_word_timestamps=on_word_timestamps,
        )

    def streaming_session_sync(
        self,
        voice_id: Optional[int] = None,
        model_id: Optional[str] = None,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        sample_rate: int = 24000,
        flush_timeout_ms: int = 500,
        normalize: bool = True,
        language: Optional[str] = None,
        word_timestamps: bool = False,
        speed: float = 1.0,
        on_word_timestamps: Optional[Callable[[List[WordTimestamp]], None]] = None,
    ) -> StreamingSessionSync:
        """Create a synchronous streaming session.

        Example:
            with client.tts.streaming_session_sync(voice_id=123) as session:
                for token in llm_stream:
                    for chunk in session.send(token):
                        play_audio(chunk)

                for chunk in session.flush():
                    play_audio(chunk)

        Args:
            voice_id: Voice ID to use
            model_id: Model to use (e.g., "kugel-1-turbo")
            cfg_scale: CFG scale for generation
            max_new_tokens: Maximum tokens per generation
            sample_rate: Output sample rate
            flush_timeout_ms: Auto-flush timeout in milliseconds
            normalize: Enable text normalization
            language: ISO 639-1 language code for normalization
            word_timestamps: Request per-chunk word-level timestamps
            speed: Playback speed multiplier (0.8–1.2, default 1.0).
                Uses pitch-preserving WSOLA time-stretching.
            on_word_timestamps: Callback ``(stamps: list[WordTimestamp]) -> None``
                invoked each time the server sends word timestamps.

        Returns:
            StreamingSessionSync for sync use
        """
        from kugelaudio.streaming import StreamingSessionSync

        async_session = self.streaming_session(
            voice_id=voice_id,
            model_id=model_id,
            cfg_scale=cfg_scale,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            sample_rate=sample_rate,
            flush_timeout_ms=flush_timeout_ms,
            normalize=normalize,
            language=language,
            word_timestamps=word_timestamps,
            speed=speed,
            on_word_timestamps=on_word_timestamps,
        )

        return StreamingSessionSync(async_session)

    def multi_context_session(
        self,
        default_voice_id: Optional[int] = None,
        model_id: Optional[str] = None,
        sample_rate: int = 24000,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        normalize: bool = True,
        language: Optional[str] = None,
        inactivity_timeout: float = 20.0,
    ) -> MultiContextSession:
        """Create a multi-context session for concurrent TTS streams.

        Allows managing up to 5 independent audio generation contexts
        over a single WebSocket connection. Each context has its own
        text buffer, voice settings, and generation queue.

        Use cases:
        - Multi-speaker conversations with different voices
        - Pre-buffering audio while another stream plays
        - Interleaved audio generation for dynamic conversations

        Args:
            default_voice_id: Default voice ID for new contexts
            model_id: Model to use (e.g., "kugel-1-turbo")
            sample_rate: Output sample rate (default 24000)
            cfg_scale: CFG scale for generation (default 2.0)
            max_new_tokens: Maximum tokens to generate (default 2048)
            normalize: Enable text normalization (default True)
            language: ISO 639-1 language code for normalization (e.g., 'de', 'en').
                If not set and normalize is True, the server auto-detects the
                language, which adds ~60-150 ms to time-to-first-audio.
            inactivity_timeout: Seconds before context auto-closes (default 20.0)

        Returns:
            MultiContextSession for async use

        Example:
            async with client.tts.multi_context_session(language="en") as session:
                # Create contexts with different voices
                await session.create_context("narrator", voice_id=123)
                await session.create_context("character", voice_id=456)

                # Send text to different speakers
                async for chunk in session.send("narrator", "The story begins."):
                    play_audio("narrator", chunk)

                async for chunk in session.send("character", "Hello!"):
                    play_audio("character", chunk)
        """
        from kugelaudio.streaming import MultiContextSession

        return MultiContextSession(
            api_key=self._client._api_key,
            tts_url=self._client._tts_url,
            default_voice_id=default_voice_id,
            model_id=model_id,
            sample_rate=sample_rate,
            cfg_scale=cfg_scale,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            normalize=normalize,
            language=language,
            inactivity_timeout=inactivity_timeout,
        )

    async def generate_async(
        self,
        text: str,
        model_id: str = "kugel-1-turbo",
        voice_id: Optional[int] = None,
        cfg_scale: float = 2.0,
        temperature: Optional[float] = None,
        max_new_tokens: int = 2048,
        sample_rate: int = 24000,
        normalize: bool = True,
        language: Optional[str] = None,
        word_timestamps: bool = False,
        speed: float = 1.0,
    ) -> AudioResponse:
        """Generate audio asynchronously.

        Args:
            text: Text to synthesize
            model_id: Model to use ('kugel-1-turbo' or 'kugel-1')
            voice_id: Voice ID to use
            cfg_scale: CFG scale for generation
            max_new_tokens: Maximum tokens to generate
            sample_rate: Output sample rate
            normalize: Enable text normalization (default: True).
                For best performance, specify the ``language`` parameter
                to skip auto-detection (~150 ms).
            language: ISO 639-1 language code for normalization (e.g., 'de', 'en').
                Supported: de, en, fr, es, it, pt, nl, pl, sv, da, no, fi, cs, hu, ro,
                el, uk, bg, tr, vi, ar, hi, zh, ja, ko, sk, sl, hr, sr, ru, he, fa,
                ur, bn, ta, yue, th, id, ms
            word_timestamps: Request word-level timestamps. When enabled,
                ``AudioResponse.word_timestamps`` will be populated with
                per-word timing boundaries.
            speed: Playback speed multiplier (0.8–1.2, default 1.0).
                Uses pitch-preserving WSOLA time-stretching.

        Returns:
            Complete audio response (with ``word_timestamps`` if requested)
        """
        chunks: List[AudioChunk] = []
        all_stamps: List[WordTimestamp] = []
        final_stats: Dict[str, Any] = {}

        async for item in self.stream_async(
            text=text,
            model_id=model_id,
            voice_id=voice_id,
            cfg_scale=cfg_scale,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            sample_rate=sample_rate,
            normalize=normalize,
            language=language,
            word_timestamps=word_timestamps,
            speed=speed,
        ):
            if isinstance(item, AudioChunk):
                chunks.append(item)
            elif isinstance(item, list):
                all_stamps.extend(item)
            elif isinstance(item, dict) and item.get("final"):
                final_stats = item

        return AudioResponse.from_chunks(chunks, final_stats, all_stamps)


class KugelAudio:
    """KugelAudio API client.

    Example:
        client = KugelAudio(api_key="your_api_key")

        # List models
        models = client.models.list()

        # List voices
        voices = client.voices.list().voices

        # Generate audio with fast model
        audio = client.tts.generate(
            text="Hello, world!",
            model_id="kugel-1-turbo",
        )
        audio.save("output.wav")

        # Generate audio with premium model
        audio = client.tts.generate(
            text="Hello, world!",
            model_id="kugel-1",
        )
    """

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        tts_url: Optional[str] = None,
        timeout: float = 60.0,
        keepalive_ping_interval: Optional[float] = 20.0,
        region: Optional[str] = None,
    ):
        """Initialize KugelAudio client.

        Args:
            api_key: Your KugelAudio API key. Can be prefixed with ``eu-``, ``us-``,
                or ``global-`` to automatically select the matching region (the prefix
                is stripped before authenticating).
            api_url: API base URL. When set, takes precedence over *region* and any
                key prefix.  (default: determined by region, falling back to
                ``https://api.kugelaudio.com``)
            tts_url: TTS server URL (default: same as api_url, the backend proxies WebSocket)
            timeout: Request timeout in seconds
            keepalive_ping_interval: Seconds between WebSocket ping frames sent on the
                pooled connection to prevent idle timeouts (default: 20.0). Set to None
                to disable keepalive pings.
            region: Deployment region — ``'eu'``, ``'us'``, or ``'global'``. Takes
                precedence over an API-key prefix but not over an explicit *api_url*.

        For fastest performance in async code, use the factory method:
            client = await KugelAudio.create(api_key="...")

        This pre-establishes the WebSocket connection so your first TTS request
        is fast (~100ms instead of ~600ms).
        """
        if not api_key:
            raise ValidationError(
                "KugelAudio API key is missing. Set the KUGELAUDIO_API_KEY "
                "environment variable or pass api_key=... to the client. "
                "Get a key at https://app.kugelaudio.com/settings/api-keys."
            )

        clean_key, detected_region = _parse_api_key(api_key)
        self._api_key = clean_key

        if api_url:
            self._api_url = api_url.rstrip("/")
        else:
            effective_region = region or detected_region or "eu"
            if effective_region not in REGION_URLS:
                raise ValidationError(
                    f"Invalid region '{effective_region}'. "
                    f"Must be one of: {', '.join(REGION_URLS)}"
                )
            self._api_url = REGION_URLS[effective_region]

        # If tts_url not specified, use api_url (backend proxies to TTS server)
        self._tts_url = (tts_url or self._api_url).rstrip("/")
        self._keepalive_ping_interval = keepalive_ping_interval
        self._timeout = timeout

        # Initialize resources
        self.models = ModelsResource(self)
        self.voices = VoicesResource(self)
        self.tts = TTSResource(self)

        from kugelaudio import __version__

        self._http_client = httpx.Client(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {clean_key}",
                "X-API-Key": clean_key,
                "User-Agent": f"kugelaudio-python/{__version__}",
            },
        )

        # Note on auto_connect:
        # - For ASYNC usage: Use `await KugelAudio.create()` to get a pre-connected client
        # - For SYNC usage: Connection pooling doesn't work across calls because each
        #   sync `stream()` call creates its own event loop. The sync API is simpler
        #   but has ~500ms cold start per call. For best sync performance, use the
        #   async API with asyncio.run() or switch to `streaming_session_sync()` which
        #   maintains a persistent connection.

    @classmethod
    async def create(
        cls,
        api_key: str,
        api_url: Optional[str] = None,
        tts_url: Optional[str] = None,
        timeout: float = 60.0,
        model: str = "kugel-1-turbo",
        keepalive_ping_interval: Optional[float] = 20.0,
        region: Optional[str] = None,
    ) -> "KugelAudio":
        """Async factory to create a pre-connected KugelAudio client.

        Use this in async code to get a client that's already connected
        and ready for fast TTS requests.

        Args:
            api_key: Your KugelAudio API key
            api_url: API base URL (default: https://api.kugelaudio.com)
            tts_url: TTS server URL (default: same as api_url)
            timeout: Request timeout in seconds
            model: Model to pre-connect for ('kugel-1-turbo' or 'kugel-1')
            keepalive_ping_interval: Seconds between WebSocket ping frames (default: 20.0).
            region: Deployment region ('eu', 'us', or 'global').

        Returns:
            Pre-connected KugelAudio client

        Example:
            async def main():
                # Client is ready immediately - no cold start on first request
                client = await KugelAudio.create(api_key="...")

                # First request is fast (~100ms)
                async for chunk in client.tts.stream_async("Hello"):
                    ...
        """
        client = cls(
            api_key=api_key,
            api_url=api_url,
            tts_url=tts_url,
            timeout=timeout,
            keepalive_ping_interval=keepalive_ping_interval,
            region=region,
        )
        await client.connect_async(model=model)
        return client

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API.

        Args:
            method: HTTP method
            path: API path
            params: Query parameters
            json_data: JSON body

        Returns:
            Response data

        Raises:
            KugelAudioError: On API error
        """
        url = urljoin(self._api_url + "/", path.lstrip("/"))

        try:
            response = self._http_client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
            )

            if response.status_code >= 400:
                raise classify_http_response(response)

            if response.status_code == 204 or not response.content:
                return {}
            return response.json()

        except httpx.TimeoutException as e:
            raise KugelAudioConnectionError(
                f"Request to {method} {path} timed out after {self._timeout}s."
            ) from e
        except httpx.RequestError as e:
            raise KugelAudioConnectionError(
                f"Could not reach KugelAudio at {url}: {e}. "
                "Check network connectivity."
            ) from e

    def _request_multipart(
        self,
        method: str,
        path: str,
        files: List[Tuple[str, Tuple[Optional[str], Any, str]]],
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make multipart/form-data HTTP request to API.

        Args:
            method: HTTP method
            path: API path
            files: List of (field, (filename, file_obj, content_type)) tuples
            params: Query parameters

        Returns:
            Response data
        """
        url = urljoin(self._api_url + "/", path.lstrip("/"))

        try:
            response = self._http_client.request(
                method=method,
                url=url,
                params=params,
                files=files,
            )

            if response.status_code >= 400:
                raise classify_http_response(response)

            return response.json()

        except httpx.TimeoutException as e:
            raise KugelAudioConnectionError(
                f"Request to {method} {path} timed out after {self._timeout}s."
            ) from e
        except httpx.RequestError as e:
            raise KugelAudioConnectionError(
                f"Could not reach KugelAudio at {url}: {e}. "
                "Check network connectivity."
            ) from e

    def close(self) -> None:
        """Close the client and release resources."""
        self._http_client.close()
        if self.tts._ws_connection is not None:
            try:
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None

                if loop is not None and loop.is_running():
                    loop.create_task(self.tts._close_ws_connection())
                else:
                    _loop = asyncio.new_event_loop()
                    try:
                        _loop.run_until_complete(self.tts._close_ws_connection())
                    finally:
                        _loop.close()
            except Exception:
                pass

    async def aclose(self) -> None:
        """Close the client asynchronously."""
        self._http_client.close()
        if hasattr(self.tts, "_close_ws_connection"):
            await self.tts._close_ws_connection()

    def connect(self, model: str = "kugel-1-turbo") -> None:
        """Pre-establish WebSocket connection for faster first request.

        Call this at application startup to eliminate cold start latency
        (~300-600ms) from your first TTS request.

        Args:
            model: Model to connect for ('kugel-1-turbo' or 'kugel-1').
                   The connection is model-specific due to routing.

        Example:
            client = KugelAudio(api_key="...")

            # Pre-connect at startup
            client.connect()

            # First request is now fast (~100ms instead of ~500ms)
            for chunk in client.tts.stream("Hello"):
                ...
        """
        self.tts.connect(model)

    async def connect_async(self, model: str = "kugel-1-turbo") -> None:
        """Pre-establish WebSocket connection for faster first request (async).

        Call this at application startup to eliminate cold start latency
        (~300-600ms) from your first TTS request.

        Args:
            model: Model to connect for ('kugel-1-turbo' or 'kugel-1').
                   The connection is model-specific due to routing.

        Example:
            client = KugelAudio(api_key="...")

            # Pre-connect at startup
            await client.connect_async()

            # First request is now fast (~100ms instead of ~500ms)
            async for chunk in client.tts.stream_async("Hello"):
                ...
        """
        await self.tts.connect_async(model)

    def is_connected(self) -> bool:
        """Check if WebSocket connection is established and open.

        Returns:
            True if connected and ready for requests.
        """
        return self.tts.is_connected()

    def __enter__(self) -> KugelAudio:
        return self

    def __exit__(self, *args) -> None:
        self.close()
