"""``BaseMediaGeneration`` — shared scaffolding for every (provider, modality)
media-generation class.

Every provider-specific image/video class subclasses this. Codifies what
``GoogleVideoGeneration`` does ad-hoc — drift hazard if 8+ classes copy it.

Subclass hooks:
    - ``provider``: provider name string for telemetry
    - ``modality``: "image" | "video"
    - ``starting_message``: user-facing "Starting <x>..." info message
    - ``_build_kwargs(unified_config, profile)``: STRUCTURAL request assembly
      (prompt extraction, media-ref conversion, SDK object nesting). Every
      scalar PARAM comes from the catalog rules via
      ``self._outbound_params(profile.controls, unified_config, ...)`` — the DB
      (ai.api.rules + ai.offering.override, seeded by _ai_029) is the single
      source of param translation for media families (B2-media flip).
    - ``_call_provider(kwargs)``: the SDK invocation (sync; base wraps in executor)
    - ``_poll_if_long_running(raw)``: default no-op; video subclasses override
    - ``_extract_assets(raw)``: pull bytes/URLs out of the provider response
    - ``_classify_error(exc)``: provider-specific error classifier
    - ``_telemetry_url(unified_config, kwargs)``: URL used for outbound capture
"""

from __future__ import annotations

import asyncio
import dataclasses
import inspect
import traceback
from abc import ABC, abstractmethod
from collections.abc import Coroutine
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from matrx_utils import vcprint

if TYPE_CHECKING:
    from matrx_ai.catalog.models import ResolvedCallProfile

from matrx_ai.config import (
    ProviderCharge,
    TokenUsage,
    UnifiedConfig,
    UnifiedResponse,
    serialize_provider_usage,
)
from matrx_ai.config.media_config import ImageContent, VideoContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.providers.outbound_capture import (
    emit_explicit_context_analysis,
    stamp_call_meta,
)

# Synthetic billing baseline — one billable "unit" = 1_000_000 synthetic
# output_tokens. Matches the convention in
# packages/matrx-ai/matrx_ai/config/usage_config.py::SYNTHETIC_USAGE_BASES so
# that ``output_price`` on a pricing tier reads as $/unit (or $/MP, $/sec)
# directly when divided by 1M in TokenUsage.calculate_cost.
_BILLING_UNIT_SCALE = 1_000_000


@dataclass
class GeneratedAsset:
    """One asset returned by a media-generation call.

    Exactly one of ``data`` / ``url`` is set. ``url`` means the provider gave
    us a URL we still need to fetch (Replicate, Together) or a Files-API
    handle that needs ``client.files.download(...)`` first. ``data`` means
    the bytes are inline (gpt-image-* base64, Imagen, Gemini-image).
    """

    data: bytes | None = None
    url: str | None = None
    mime_type: str = ""
    # Provider-specific extras forwarded to the unified content block's metadata.
    metadata: dict[str, Any] | None = None


class MinorImageBlockedError(PermissionError):
    """Raised to REFUSE image generation for a minor when the chosen provider
    cannot GUARANTEE an enforced NSFW/adult-content safety filter.

    Arman's ruling (2026-08-17): allow image generation for minors WITH an
    enforced provider safe-setting, but BLOCK generation if that filtering
    cannot be guaranteed. Raised BEFORE the paid provider call, so nothing is
    billed. Rides the streaming error path (not an HTTPException): it carries a
    NON-retryable ``RetryableError`` on ``.error_info`` — the exact shape the
    orchestrator's failure handler reads (``getattr(e, "error_info", None)``) so
    the refusal is surfaced verbatim to the client and never retried.
    """

    error_type_str = "minor_image_generation_blocked"

    def __init__(self, provider: str, model: str | None) -> None:
        message = (
            f"Image generation refused for a minor: provider {provider!r} "
            f"(model={model}) cannot guarantee an enforced content-safety filter."
        )
        super().__init__(message)
        from matrx_ai.providers.errors import RetryableError

        self.error_info = RetryableError(
            error_type=self.error_type_str,
            message=message,
            status_code=403,
            is_retryable=False,
            user_message=(
                "Image generation with this model isn't available for younger "
                "users. Please try a different image style or model."
            ),
        )


class BaseMediaGeneration(ABC):
    provider: str = ""
    modality: Literal["image", "video"] = "image"
    starting_message: str = "Starting media generation..."
    # Child content-safety (WP13): can this provider ENFORCE an NSFW/adult
    # filter for a minor's image generation? Default False → a minor's image
    # request is REFUSED before the paid call unless the provider affirmatively
    # opts in AND tightens its safety params in ``_apply_minor_image_overrides``.
    # Video/audio subclasses are never affected — enforcement is scoped to
    # ``modality == "image"``.
    supports_minor_safe_image: bool = False

    async def _await_paid_completion(
        self,
        operation: Coroutine[Any, Any, UnifiedResponse],
    ) -> UnifiedResponse:
        task = asyncio.create_task(
            operation,
            name=f"paid_media:{self.provider}:{self.modality}",
        )
        cancellation: asyncio.CancelledError | None = None
        while True:
            try:
                response = await asyncio.shield(task)
                break
            except asyncio.CancelledError as exc:
                if task.done():
                    return task.result()
                cancellation = cancellation or exc
                vcprint(
                    f"[{self.provider} {self.modality}] Cancellation deferred — "
                    "the paid provider operation will finish and persist before "
                    "cancellation propagates.",
                    color="red",
                )

        if cancellation is not None:
            try:
                from matrx_ai.providers.errors import (
                    attach_billed_usage,
                    attach_completed_response,
                )

                attach_billed_usage(cancellation, response.usage)
                attach_completed_response(cancellation, response)
            except Exception as exc:
                vcprint(
                    f"[{self.provider} {self.modality}] Failed to attach the completed "
                    f"response to deferred cancellation: {exc}",
                    color="red",
                )
            raise cancellation
        return response

    @property
    def _content_class(self) -> type[ImageContent] | type[VideoContent]:
        return ImageContent if self.modality == "image" else VideoContent

    @property
    def _event_payload_type(self) -> str:
        return "image_output" if self.modality == "image" else "video_output"

    @abstractmethod
    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: ResolvedCallProfile
    ) -> dict[str, Any]:
        """Assemble the provider SDK kwargs: structural parts in code, scalar
        params from ``profile.controls`` (the offering's CompiledControlsMap)."""

    def _apply_minor_image_overrides(
        self, kwargs: dict[str, Any], unified_config: UnifiedConfig, profile: Any
    ) -> None:
        """Tighten this provider's safety params to the strictest setting for a
        minor, mutating ``kwargs`` in place. Default no-op — a provider that
        sets ``supports_minor_safe_image = True`` MUST override this. Operates
        only on the local ``kwargs`` (provider instances are cached
        process-wide, so instance state would race). May raise
        ``MinorImageBlockedError`` if it cannot guarantee the filter for this
        specific request; the caller also converts any other failure to a block.
        """

    def _enforce_minor_image_safety(
        self, kwargs: dict[str, Any], unified_config: UnifiedConfig, profile: Any
    ) -> None:
        """Enforce the NSFW/adult filter for a minor's IMAGE generation (WP13).

        Reads the ONE ``ctx.is_minor`` flag (resolved once at the AI funnel).
        No-op for adults, guests, and every non-image modality. For a minor:
        refuse outright when the provider can't enforce a filter
        (``supports_minor_safe_image = False``), otherwise apply the provider's
        strict overrides — and if THAT can't be guaranteed, refuse (never let an
        unfiltered image reach a minor).
        """
        if self.modality != "image":
            return
        try:
            from matrx_ai.context.app_context import get_app_context

            is_minor = bool(getattr(get_app_context(), "is_minor", False))
        except Exception:  # noqa: BLE001 — no context ⇒ not a minor request
            is_minor = False
        if not is_minor:
            return
        if not self.supports_minor_safe_image:
            raise MinorImageBlockedError(self.provider, unified_config.model)
        try:
            self._apply_minor_image_overrides(kwargs, unified_config, profile)
        except MinorImageBlockedError:
            raise
        except Exception as exc:  # noqa: BLE001 — can't guarantee the filter ⇒ block
            vcprint(
                f"[{self.provider} image] minor safety override failed "
                f"({type(exc).__name__}: {exc}) — BLOCKING generation for the minor "
                f"(cannot guarantee a content-safety filter).",
                color="red",
            )
            raise MinorImageBlockedError(self.provider, unified_config.model) from exc
        vcprint(
            f"[{self.provider} image] minor content-safety filter ENFORCED "
            f"(model={unified_config.model}).",
            color="cyan",
        )

    @staticmethod
    def _outbound_params(
        controls: Any,
        unified_config: UnifiedConfig,
        *,
        context: dict[str, Any] | None = None,
        extra_canonical: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Canonical config -> provider params through the catalog rules.

        ``extra_canonical`` carries builder-derived canonical values (message-
        tagged negative_prompt, structural media URLs the rules gate per model);
        ``context`` carries the outbound context flags (operation="generate" |
        "edit", has_image_input=bool). Adjustments are voiced loudly.

        The DECLARED-KEYS GATE (shared with the chat seam — one canonical
        implementation in ``outbound_params.drop_foreign_canonical_keys``)
        runs AFTER the extra_canonical merge: a canonical key not declared by
        this offering's compiled rules (e.g. ``verbosity``, a gpt-5 text
        control, riding on a config pointed at a FLUX offering) is DROPPED
        loudly instead of leaking into the provider body via PASSTHROUGH_RULE
        — the crown-jewel guarantee (any model's params at any other model →
        valid body) holds on the media seam too. Builder-derived extras are
        declared structural rules per family (_ai_029), so the gate never
        touches them."""
        from matrx_ai.catalog.canonicalize import canonical_settings_from_config
        from matrx_ai.providers.outbound_params import drop_foreign_canonical_keys

        canonical = canonical_settings_from_config(unified_config)
        if extra_canonical:
            for key, value in extra_canonical.items():
                if value is not None:
                    canonical[key] = value
        drop_foreign_canonical_keys(
            canonical, controls, model=getattr(unified_config, "model", "?")
        )
        params, adjustments = controls.outbound(canonical, context=context or {})
        for adjustment in adjustments:
            vcprint(f"[media controls] {adjustment.reason}", color="yellow")
        # Same law as the chat seam: an unexpected drop reaches the user as a
        # warning (aspect_ratio / resolution / output_format live here).
        from matrx_ai.providers.outbound_params import warn_client_about_dropped_settings

        warn_client_about_dropped_settings(
            adjustments, model=getattr(unified_config, "model", "?")
        )
        return params

    @abstractmethod
    def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        """Invoke the provider SDK synchronously. Base wraps this in run_in_executor."""

    def _poll_if_long_running(self, raw: Any) -> Any:
        """Override for video classes. Default: synchronous, no polling needed."""
        return raw

    @abstractmethod
    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        """Pull GeneratedAsset items out of the raw provider response."""

    @abstractmethod
    def _classify_error(self, exc: Exception) -> Any:
        """Translate provider exception to a uniform error_info shape with
        attributes ``error_type``, ``message``, ``user_message``."""

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        """URL passed to ``emit_explicit_context_analysis`` for outbound capture.

        Subclasses can override for endpoint-specific URLs; default is empty
        string (telemetry still fires with the model id stamped via
        ``stamp_call_meta``).
        """
        return ""

    async def _persist_asset(
        self,
        asset: GeneratedAsset,
        *,
        prompt: str | None = None,
        model: str | None = None,
        extra_metadata: dict[str, Any] | None = None,
    ):
        """Persist via the canonical envelope path.

        Returns a :class:`MediaPersistResult` carrying ``file_id`` plus
        every URL flavour. Subclasses no longer need to handle URL minting
        — the central ``SyncEngine.build_urls_for_record_async`` populates
        ``url`` (CDN if public, authenticated route otherwise),
        ``cdn_url``, and ``download_url`` (attachment) — all durable.

        ``prompt`` is the user's natural-language description; flows
        through to:
          - filename: ``sunset-rocky-mountains-a1b2c3d4.jpg`` instead of
            a UUID, via ``naming.slugify_prompt``.
          - metadata: persisted on the cld_files row so audit / search
            / reviewer UIs can show "what made this".

        ``extra_metadata`` is shallow-merged into the cld_files metadata
        JSONB alongside the default {source, mime_type, model, provider,
        feature} keys. Used by execute() to stamp the canonical
        MediaGenerationMetadata under ``metadata.generation``.
        """
        from matrx_ai.media import save_media_envelope_async

        if asset.data is None and asset.url is None:
            raise RuntimeError("GeneratedAsset has neither data nor url")

        # If only URL is set and the provider expects an explicit fetch+save
        # (Replicate, Together), subclass should fetch bytes in
        # _extract_assets and put them in `data`. Otherwise we pass the URL
        # straight through to save_media_envelope_async, which fetches and persists.
        source = asset.data if asset.data is not None else asset.url
        feature = {
            "image": "ai_images",
            "video": "ai_video",
            "audio": "ai_audio",
        }.get(self.modality, "ai_images")
        envelope = await save_media_envelope_async(
            content=source,
            mime_type=asset.mime_type or self._default_mime(),
            prompt=prompt,
            model=model,
            provider=self.provider,
            feature=feature,
            extra_metadata=extra_metadata,
        )
        if not envelope.file_id:
            raise RuntimeError("save_media_envelope_async returned a result without file_id")
        return envelope

    # ------------------------------------------------------------------
    # Generation metadata hook — override per provider for richer mapping
    # ------------------------------------------------------------------

    def _map_generation_metadata(
        self,
        *,
        raw: Any,
        asset: GeneratedAsset,
        asset_index: int,
        request_kwargs: dict[str, Any],
        unified_config: UnifiedConfig,
        prompt: str | None,
        n_returned: int,
        duration_ms: int | None,
        cost_usd: float | None,
    ):
        """Build the canonical MediaGenerationMetadata for one persisted asset.

        Default implementation returns :func:`build_default_metadata`
        with the minimum-viable fields (provider, model, prompt,
        n_returned, duration_ms, cost_usd). Per-provider subclasses
        override to pull richer fields out of the raw SDK response —
        see :mod:`matrx_ai.media.generation_metadata` for the existing
        OpenAI / Google Imagen / Together Flux mappers.

        Stamped at ``cld_files.metadata.generation`` so the FE can drive
        a "Regenerate with same settings" UX or surface revised prompts.

        Mappers MUST NOT raise — return a best-effort metadata so a
        mapper bug never blocks the generation response.
        """
        from matrx_ai.media.generation_metadata import build_default_metadata

        kind = {
            "image": "image",
            "video": "video",
            "audio": "audio",
        }.get(self.modality, "image")
        return build_default_metadata(
            kind=kind,
            provider=self.provider,
            model=unified_config.model or "",
            prompt=prompt,
            n_returned=n_returned,
            duration_ms=duration_ms,
            cost_usd=cost_usd,
        )

    def _default_mime(self) -> str:
        return "image/png" if self.modality == "image" else "video/mp4"

    @staticmethod
    async def _maybe_await(fn: Any, *args: Any) -> Any:
        """Call ``fn(*args)``: await if coroutine, otherwise run in executor.

        Lets subclasses define their hooks as either sync (Google's
        google-genai is sync) or async (AsyncOpenAI is async-first) without
        the base class caring which. Sync hooks run in the default executor
        so they never block the event loop.
        """
        if inspect.iscoroutinefunction(fn):
            return await fn(*args)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, fn, *args)

    def _build_content_block(self, envelope, asset: GeneratedAsset) -> ImageContent | VideoContent:
        """Build the FE-visible content block carrying the FULL MediaRef envelope.

        ``envelope`` is either a :class:`MediaPersistResult` (preferred —
        new path) or a bare URL string (legacy path, for callers we
        haven't migrated). When given a string we lose the file_id and
        the FE can't re-resolve on expiry, so the envelope path is the
        target everywhere.
        """
        from matrx_ai.media import MediaPersistResult

        cls = self._content_class
        kwargs: dict[str, Any] = {}
        if isinstance(envelope, MediaPersistResult):
            kwargs["file_id"] = envelope.file_id
            kwargs["url"] = envelope.url
            kwargs["mime_type"] = envelope.mime_type or asset.mime_type or self._default_mime()
            # No file_uri=storage_uri: the native s3:// location is server-only
            # and only leaks to the FE via the persisted media part. The content
            # resolves for providers via file_id/url; identify by file_id.
            kwargs["file_size"] = envelope.size_bytes
            # Phase 3b: thread probed dimensions through to the content
            # class so cx_message storage carries them straight from
            # AI-gen response without a follow-up GET.
            if envelope.width is not None and "width" in {f.name for f in dataclasses.fields(cls)}:
                kwargs["width"] = envelope.width
            if envelope.height is not None and "height" in {
                f.name for f in dataclasses.fields(cls)
            }:
                kwargs["height"] = envelope.height
            if envelope.duration_ms is not None and "duration_ms" in {
                f.name for f in dataclasses.fields(cls)
            }:
                kwargs["duration_ms"] = envelope.duration_ms
        else:
            kwargs["url"] = envelope
            kwargs["mime_type"] = asset.mime_type or self._default_mime()
        if asset.metadata:
            kwargs["metadata"] = asset.metadata
        return cls(**kwargs)

    # ------------------------------------------------------------------
    # Usage / billing — overridable per subclass
    # ------------------------------------------------------------------

    def _billing_input_tokens(
        self,
        unified_config: UnifiedConfig,
        kwargs: dict[str, Any],
        raw: Any,
        assets: list[GeneratedAsset],
    ) -> int:
        """Real input tokens reported by the provider (gpt-image-* exposes this).

        Default 0 — most image / video providers don't report token-style
        input usage. Subclasses with a usage object on ``raw`` should
        override to return e.g. ``raw.usage.input_tokens``.
        """
        return 0

    def _billing_output_tokens(
        self,
        unified_config: UnifiedConfig,
        kwargs: dict[str, Any],
        raw: Any,
        assets: list[GeneratedAsset],
    ) -> int:
        """Synthetic output_tokens for cost calculation.

        Default: ``len(assets) * 1_000_000`` — correct for tiers with
        ``usage_basis="image_output"`` (per-image) and
        ``usage_basis="video_unit_output"`` (per-clip).

        Subclasses billed by megapixel or by second should override:
          - ``megapixel_output``: return ``int(total_megapixels * 1_000_000)``
          - ``video_second_output``: return ``int(total_seconds * 1_000_000)``

        Subclasses with **real** token billing (gpt-image-* charges by tokens
        when used through the Responses API) should return the real
        ``raw.usage.output_tokens`` directly.
        """
        return max(1, len(assets)) * _BILLING_UNIT_SCALE

    def _provider_usage(self, raw: Any) -> tuple[int, int, int] | None:
        """Real ``(input_tokens, output_tokens, cached_input_tokens)`` reported
        by the provider, or ``None`` when the provider bills by a synthetic unit
        (per-image / per-second / per-megapixel) and reports no token usage.

        Override in subclasses whose API returns a usage object — gpt-image-*
        (``raw.usage``), Gemini image-native (``raw.usage_metadata``). When the
        model's pricing tier carries no ``usage_basis`` (raw $/1M-token billing),
        this real usage is what gets billed; the synthetic per-asset count is
        NEVER applied to a token-priced tier (that overcharges by ~1,000,000×).
        """
        return None

    def _provider_billing_components(self, raw: Any) -> dict[str, int]:
        """Normalized modality-specific usage units for component pricing."""
        return {}

    def _provider_raw_usage(self, raw: Any) -> dict[str, Any] | None:
        """Preserve provider usage evidence without serializing media payloads."""
        usage = getattr(raw, "usage", None) or getattr(raw, "usage_metadata", None)
        return serialize_provider_usage(usage) if usage is not None else None

    def _provider_charge(self, raw: Any) -> ProviderCharge | None:
        """Exact provider-reported monetary charge, when the API exposes one."""
        return None

    def _resolve_pricing_basis(
        self, model_name: str, offering_id: str = ""
    ) -> tuple[bool, str | None]:
        """``(pricing_known, usage_basis)`` for ``model_name`` — the single basis
        resolver in usage_config, keyed on this provider's api."""
        from matrx_ai.config.usage_config import resolve_usage_basis

        return resolve_usage_basis(model_name, self.provider, offering_id)

    def _synthetic_units(
        self,
        usage_basis: str,
        unified_config: UnifiedConfig,
        kwargs: dict[str, Any],
        raw: Any,
        assets: list[GeneratedAsset],
        synthetic_input: int,
        synthetic_output: int,
    ) -> tuple[int, int, int]:
        """Billable (input, output, cached) tokens for a synthetic-basis tier.

        Most bases are per-asset (the ``synthetic_*`` defaults). The two
        ``computed`` bases derive the count from the generated media so the price
        actually applies per unit instead of per call:
          - ``megapixel_output`` → output_tokens = total output pixels (w×h×n).
          - ``video_second_output`` → output_tokens = total seconds × 1M.
        If the dimension/duration signal is missing we SCREAM and fall back to the
        per-asset count (best effort) rather than $0 — never silently under-bill.
        """
        if usage_basis == "megapixel_output":
            pixels = self._total_output_pixels(kwargs, assets)
            if pixels > 0:
                return (0, pixels, 0)
            self._scream_missing_unit(unified_config, usage_basis, "image dimensions (width×height)")
            return (0, synthetic_output, 0)
        if usage_basis == "video_second_output":
            seconds = self._total_output_seconds(unified_config, kwargs, raw, assets)
            if seconds > 0:
                return (0, int(seconds * _BILLING_UNIT_SCALE), 0)
            self._scream_missing_unit(unified_config, usage_basis, "duration_seconds")
            return (0, synthetic_output, 0)
        if usage_basis in ("character_input", "audio_second_input"):
            # Input-billed synthetic bases — media generators don't normally use
            # these (TTS/transcription do, off this path), but stay correct.
            return (synthetic_input, 0, 0)
        # image_output, video_unit_output, minute → flat per-asset count.
        return (synthetic_input, synthetic_output, 0)

    @staticmethod
    def _total_output_pixels(kwargs: dict[str, Any], assets: list[GeneratedAsset]) -> int:
        """Total output pixels across all assets (width×height×n), from request
        kwargs. Handles int width/height or a ``"WxH"`` size string. 0 if unknown."""
        w = kwargs.get("width")
        h = kwargs.get("height")
        size = kwargs.get("size")
        if (not w or not h) and isinstance(size, str) and "x" in size.lower():
            try:
                sw, sh = size.lower().split("x")[:2]
                w, h = int(sw), int(sh)
            except Exception:
                w = h = None
        try:
            w_i, h_i = int(w), int(h)
        except (TypeError, ValueError):
            return 0
        if w_i <= 0 or h_i <= 0:
            return 0
        return w_i * h_i * max(1, len(assets))

    @staticmethod
    def _total_output_seconds(
        unified_config: UnifiedConfig,
        kwargs: dict[str, Any],
        raw: Any,
        assets: list[GeneratedAsset],
    ) -> float:
        """Total output seconds across all assets — prefers the canonical
        ``duration_seconds`` on the config, then request kwargs, then a duration
        on the provider response. 0.0 if unknown."""
        secs: Any = getattr(unified_config, "duration_seconds", None)
        if not secs:
            for k in ("duration_seconds", "duration", "seconds"):
                if kwargs.get(k):
                    secs = kwargs[k]
                    break
        if not secs:
            provider_config = kwargs.get("config")
            for k in ("duration_seconds", "duration", "seconds"):
                value = getattr(provider_config, k, None)
                if value:
                    secs = value
                    break
        if not secs:
            vid = getattr(raw, "video", None)
            secs = getattr(vid, "duration", None) if vid is not None else None
        try:
            secs_f = float(secs)
        except (TypeError, ValueError):
            return 0.0
        if secs_f <= 0:
            return 0.0
        return secs_f * max(1, len(assets))

    def _scream_missing_unit(self, unified_config: UnifiedConfig, usage_basis: str, needed: str) -> None:
        from matrx_ai.config.usage_config import _warn_billing_once

        _warn_billing_once(
            unified_config.model or "",
            self.provider,
            f"{self.modality} tier uses usage_basis={usage_basis!r} but {needed} "
            f"was not available at billing time",
            f"fell back to per-asset billing (under-bills multi-unit output). Ensure "
            f"{needed} is set on the request/response for {type(self).__name__}.",
        )

    @staticmethod
    def _safe_int(fn: Any, default: int) -> int:
        try:
            return max(0, int(fn()))
        except Exception:
            return default

    def _billing_response_id(self, raw: Any) -> str:
        for attr in ("id", "response_id", "request_id"):
            v = getattr(raw, attr, None)
            if v:
                return str(v)
        return ""

    def _build_usage(
        self,
        unified_config: UnifiedConfig,
        kwargs: dict[str, Any],
        raw: Any,
        assets: list[GeneratedAsset],
        *,
        offering_id: str = "",
        model_name: str = "",
    ) -> TokenUsage:
        """Build the TokenUsage stamped onto UnifiedResponse — basis-aware.

        The billing basis is driven by the model's pricing tier ``usage_basis``:
          - synthetic basis (image_output / megapixel_output / video_*_output) →
            bill the synthetic per-asset / per-unit count (``_billing_*_tokens``);
            ``output_price`` reads as $/unit.
          - no basis (raw $/1M-token billing) → bill the REAL provider usage
            (``_provider_usage``). Feeding the synthetic 1M-per-asset count into a
            token-priced tier multiplies the per-1M-token price by 1M — a
            ~1,000,000× overcharge — so we NEVER do that.

        Always returns a TokenUsage so ``model`` flows through CompletedRequest
        even when cost can't be computed (cost column simply resolves to None/0).
        Requires the pricing lookup to be warm (callers run ``ensure_pricing_lookup``
        first); a cold cache degrades to the synthetic count and defers cost.
        """
        from matrx_ai.config.usage_config import SYNTHETIC_USAGE_BASES

        model = model_name or unified_config.matrx_model_name or unified_config.model or ""
        routed_offering_id = offering_id or unified_config.routing_offering_id or ""
        pricing_known, usage_basis = self._resolve_pricing_basis(model, routed_offering_id)

        real_usage: tuple[int, int, int] | None
        try:
            real_usage = self._provider_usage(raw)
        except Exception:
            real_usage = None

        synthetic_input = self._safe_int(
            lambda: self._billing_input_tokens(unified_config, kwargs, raw, assets), 0
        )
        synthetic_output = self._safe_int(
            lambda: self._billing_output_tokens(unified_config, kwargs, raw, assets),
            max(1, len(assets)) * _BILLING_UNIT_SCALE,
        )

        if usage_basis in SYNTHETIC_USAGE_BASES:
            # Per-unit billing — compute the unit count that matches the price.
            # image_output / video_unit_output → per asset; megapixel_output →
            # real pixels; video_second_output → real seconds (the "computed"
            # bases that the flat per-asset default silently under-billed).
            input_tokens, output_tokens, cached_tokens = self._synthetic_units(
                usage_basis, unified_config, kwargs, raw, assets, synthetic_input, synthetic_output
            )
            billing_kind = f"synthetic:{usage_basis}"
        elif real_usage is not None:
            # Raw token billing ($/1M tokens) with real provider usage —
            # gpt-image-*, Gemini image-native.
            input_tokens, output_tokens, cached_tokens = real_usage
            billing_kind = "provider_tokens"
        elif not pricing_known:
            # Pricing not loaded (cold cache / ad-hoc script) — basis unknown.
            # Record the synthetic count; calculate_cost defers/None until the
            # lookup warms. Normal request flow warms pricing before this runs,
            # so this is the last-resort fallback only.
            input_tokens, output_tokens, cached_tokens = synthetic_input, synthetic_output, 0
            billing_kind = "synthetic_unpriced"
        else:
            # usage_basis is None (raw $/1M-token billing) but the provider
            # reported no usage. Billing the synthetic 1M sentinel here would
            # overcharge ~1,000,000×. Refuse: record zero billable tokens (cost
            # remains unknown, not a fortune or false zero) and SCREAM so it
            # gets fixed.
            input_tokens, output_tokens, cached_tokens = 0, 0, 0
            billing_kind = "uncomputable_no_basis_no_usage"
            from matrx_ai.config.usage_config import _warn_billing_once

            _warn_billing_once(
                model,
                self.provider,
                f"{self.modality} tier is token-priced (no usage_basis) but the "
                f"provider returned no token usage",
                f"cost left unknown to avoid a ~1,000,000× overcharge (the synthetic "
                f"1M-unit-per-asset count must NEVER hit a token-priced tier). "
                f"Fix: add a usage_basis to this model's pricing tier "
                f"(per-image/second/megapixel), OR override _provider_usage() on "
                f"{type(self).__name__} to surface real provider tokens.",
            )

        input_tokens = max(0, int(input_tokens))
        output_tokens = max(0, int(output_tokens))
        cached_tokens = max(0, int(cached_tokens))

        metadata: dict[str, Any] = {
            "modality": self.modality,
            "asset_count": len(assets),
            "billing_kind": billing_kind,
        }
        if billing_kind == "uncomputable_no_basis_no_usage":
            metadata["cost_reconciliation"] = "unknown_missing_provider_usage"
        billing_components = self._provider_billing_components(raw)
        if any(name.startswith("unallocated.") for name in billing_components):
            metadata["cost_reconciliation"] = "unknown_component_allocation"
        # Best-effort dimensional / duration breadcrumbs — used by
        # downstream telemetry & UI even when not folded into cost.
        if self.modality == "image":
            w = kwargs.get("width") or kwargs.get("size")
            h = kwargs.get("height")
            if w:
                metadata["width"] = w
            if h:
                metadata["height"] = h
        else:
            secs = kwargs.get("duration_seconds") or kwargs.get("duration") or kwargs.get("seconds")
            if secs is not None:
                metadata["duration_seconds"] = secs

        return TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_tokens,
            matrx_model_name=model,
            provider_model_name=model,
            api=self.provider,
            response_id=self._billing_response_id(raw),
            offering_id=routed_offering_id,
            metadata=metadata,
            raw_usage=self._provider_raw_usage(raw),
            billing_components=billing_components,
            provider_charge=self._provider_charge(raw),
        )

    async def _emit_asset_event(self, emitter: Any, envelope, mime_type: str) -> None:
        """Emit the provider-asset event as a canonical MediaBlockData.

        Same UnifiedMediaBlock shape persisted to ``cx_message.content``
        so the live stream and the post-stream re-fetch carry identical
        info — the FE renders both through one component off durable URLs.
        """
        from matrx_connect.context.data_types import MediaBlockData
        from matrx_connect.context.media_block import (
            cloud_file_to_media_block,
            external_url_to_media_block,
        )

        from matrx_ai.media import MediaPersistResult

        kind = "image" if self.modality == "image" else "video"

        if isinstance(envelope, MediaPersistResult):
            # Build a synthetic cld_files-shaped dict from the persist
            # envelope so cloud_file_to_media_block can produce a
            # canonical block without a follow-up DB read.
            synthetic_metadata: dict[str, Any] = {}
            if envelope.page_count is not None:
                synthetic_metadata["page_count"] = envelope.page_count
            synthetic_record = {
                "id": envelope.file_id,
                "storage_uri": envelope.storage_uri,
                "file_path": envelope.file_path,
                "file_name": envelope.file_name,
                "mime_type": envelope.mime_type or mime_type,
                "size_bytes": envelope.size_bytes,
                "visibility": envelope.visibility,
                # Phase 3b — surface probed intrinsics on the synthetic
                # record so the stream's UnifiedMediaBlock carries them
                # (cloud_file_to_media_block reads width/height/duration_ms
                # from the record + page_count from metadata).
                "width": envelope.width,
                "height": envelope.height,
                "duration_ms": envelope.duration_ms,
                "metadata": synthetic_metadata,
            }
            url_set = {
                "url": envelope.url,
                "cdn_url": envelope.cdn_url,
                "download_url": envelope.download_url,
            }
            # Phase 1c: for video kind, look up the poster_url variant
            # that was rendered alongside SOCIAL_BASELINE during
            # persistence so VideoBlock.poster_url is populated for
            # inline HTML5 <video poster=...> rendering. Single extra
            # DB query + URL mint — guarded to the video kind so the
            # much more common image emission path stays unchanged.
            kind_variant_urls: dict[str, str] = {}
            if kind == "video":
                try:
                    from matrx_ai.media.media_persistence import AIMediaHandler

                    fm = AIMediaHandler.get_instance()._get_cloud_fm()
                    catalog = await fm.sync_engine.variants.list_existing_async(synthetic_record)
                    poster_row = catalog.get("poster_url")
                    if poster_row:
                        poster_urls = await fm.sync_engine.build_urls_for_record_async(poster_row)
                        if poster_urls.get("url"):
                            kind_variant_urls["poster_url"] = poster_urls["url"]
                except Exception:
                    # Non-fatal — the block still ships without poster_url
                    # and the FE falls back to a static placeholder.
                    pass
            block = cloud_file_to_media_block(
                synthetic_record,
                url_set=url_set,
                kind_override=kind,
                kind_variant_urls=kind_variant_urls or None,
            )
        else:
            # Legacy string-only path (kept for back-compat with any caller
            # that still hands us a URL directly). Treated as external.
            block = external_url_to_media_block(
                envelope,
                kind=kind,
                mime_type=mime_type,
            )

        await emitter.send_data(MediaBlockData(block=block))

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        return await self._await_paid_completion(
            self._execute_to_completion(unified_config, profile, debug)
        )

    async def _execute_to_completion(
        self,
        unified_config: UnifiedConfig,
        profile: ResolvedCallProfile,
        debug: bool = False,
    ) -> UnifiedResponse:
        from matrx_connect.context.events import InfoPayload

        from matrx_ai.context.app_context import get_app_context

        emitter = get_app_context().emitter

        kwargs = self._build_kwargs(unified_config, profile)
        # Child content-safety (WP13): enforce the NSFW/adult filter for a
        # minor's image request BEFORE the paid call (raises to refuse if the
        # filter can't be guaranteed — nothing is billed).
        self._enforce_minor_image_safety(kwargs, unified_config, profile)
        if debug:
            vcprint(kwargs, f"[{self.provider} {self.modality}] kwargs", color="blue")

        stamp_call_meta(
            provider=self.provider,
            model=unified_config.model,
            is_streaming=False,
        )

        # Once the paid provider call returns, NEVER ask the executor to retry
        # the whole execute() — a second ``async_run`` / generate creates another
        # billed prediction. Persist/upload failures after that point are local
        # defects and must surface as non-retryable.
        paid_provider_call_completed = False
        try:
            # Outbound capture for telemetry — best-effort.
            try:
                safe_kwargs = {
                    k: v
                    for k, v in kwargs.items()
                    if isinstance(v, str | int | float | bool | type(None) | dict | list)
                }
                await emit_explicit_context_analysis(
                    provider=self.provider,
                    method="POST",
                    url=self._telemetry_url(unified_config, kwargs),
                    headers={"Content-Type": "application/json"},
                    body=safe_kwargs,
                    is_streaming=False,
                    model=unified_config.model,
                )
            except Exception:
                pass

            if emitter:
                await emitter.send_info(
                    InfoPayload(
                        code=f"{self.modality}_generating",
                        system_message=self.starting_message,
                        user_message=self.starting_message,
                    )
                )

            initial = await self._maybe_await(self._call_provider, kwargs)
            paid_provider_call_completed = True
            raw = await self._maybe_await(self._poll_if_long_running, initial)

            assets = await self._maybe_await(self._extract_assets, raw)
            if not assets:
                raise RuntimeError(
                    f"{self.provider} {self.modality} generation returned no assets."
                )

            # Fetch-if-not-fetched: load the DB pricing lookup BEFORE building
            # usage so the basis-aware billing in _build_usage (and the cost
            # calc) both see a warm cache — a cold cache can't masquerade as
            # "pricing not found". See usage_config.ensure_pricing_lookup.
            try:
                from matrx_ai.config.usage_config import ensure_pricing_lookup

                await ensure_pricing_lookup()
            except Exception:
                pass

            # Build TokenUsage now (before persistence) so per-asset cost
            # can be folded into each ImageContent / VideoContent block's
            # metadata for direct FE consumption next to the rendered asset.
            usage = self._build_usage(
                unified_config,
                kwargs,
                raw,
                assets,
                offering_id=profile.offering_id,
                model_name=profile.model_name,
            )
            try:
                total_cost = usage.calculate_cost()
            except Exception:
                total_cost = None
            per_asset_cost = (
                round(total_cost / len(assets), 6) if total_cost is not None and assets else None
            )

            # Extract the user's prompt for descriptive filenames + audit
            # metadata. The last user-role message text is the canonical
            # "what the user asked for" — image/video generation requests
            # almost always have exactly one user message carrying the prompt.
            prompt_text = _extract_prompt(unified_config)

            content_blocks: list[ImageContent | VideoContent] = []
            for asset_index, asset in enumerate(assets):
                # Build the canonical generation metadata record BEFORE
                # persistence so it's stamped into cld_files.metadata.generation
                # in the same write — the FE's "Regenerate with same settings"
                # UX and revised-prompt display read this typed shape.
                # Mapper errors fall back to the default metadata silently.
                try:
                    gen_meta = self._map_generation_metadata(
                        raw=raw,
                        asset=asset,
                        asset_index=asset_index,
                        request_kwargs=kwargs,
                        unified_config=unified_config,
                        prompt=prompt_text,
                        n_returned=len(assets),
                        duration_ms=None,  # populated by per-provider mappers when known
                        cost_usd=per_asset_cost,
                    )
                    gen_meta_dict = gen_meta.model_dump(exclude_none=True)
                except Exception:
                    vcprint(
                        f"[{self.provider} {self.modality}] _map_generation_metadata "
                        "failed; persisting without generation metadata",
                        color="yellow",
                    )
                    gen_meta_dict = None

                envelope = await self._persist_asset(
                    asset,
                    prompt=prompt_text,
                    model=unified_config.model,
                    extra_metadata={"generation": gen_meta_dict} if gen_meta_dict else None,
                )
                vcprint(
                    f"[{self.provider} {self.modality}] Saved to cld_files: "
                    f"file_id={envelope.file_id} url={envelope.url}",
                    color="green",
                )

                # Stamp model + per-asset cost onto the asset's metadata so
                # the content block carries it. FE renders "Made with X — $Y"
                # directly off the block; analytics also see it on cx_message.
                asset.metadata = dict(asset.metadata or {})
                asset.metadata.setdefault("model", unified_config.model)
                asset.metadata.setdefault("provider", self.provider)
                if per_asset_cost is not None:
                    asset.metadata.setdefault("cost", per_asset_cost)
                if gen_meta_dict:
                    # Also surface the generation block on the content block
                    # itself so the cx_message.content[] item carries the
                    # parsed metadata for in-conversation rendering without a
                    # follow-up GET /assets/{file_id}.
                    asset.metadata.setdefault("generation", gen_meta_dict)

                block = self._build_content_block(envelope, asset)
                content_blocks.append(block)

                if emitter:
                    await self._emit_asset_event(
                        emitter,
                        envelope,
                        block.mime_type or self._default_mime(),
                    )

            messages = [UnifiedMessage(role="assistant", content=content_blocks)]
            return UnifiedResponse(messages=messages, usage=usage)

        except Exception as exc:
            vcprint(exc, f"[{self.provider} {self.modality}] Error", color="red")
            traceback.print_exc()

            error_info = self._classify_error(exc)
            if paid_provider_call_completed:
                error_info = _non_retryable_after_paid_call(
                    error_info,
                    exc,
                    provider=self.provider,
                    modality=self.modality,
                )

            if emitter and error_info is not None:
                await emitter.send_error(
                    error_type=getattr(error_info, "error_type", "unknown_error"),
                    message=getattr(error_info, "message", str(exc)),
                    user_message=getattr(error_info, "user_message", "Media generation failed."),
                )

            if error_info is not None:
                exc.error_info = error_info  # type: ignore[attr-defined]
            raise


def _non_retryable_after_paid_call(
    error_info: Any,
    exc: Exception,
    *,
    provider: str,
    modality: str,
) -> Any:
    """Force non-retryable classification once the paid provider call finished.

    Replicate/OpenAI/etc. already billed the generation. Retrying the whole
    media execute() would create a second prediction for a local persist/DB
    failure — the exact loop that burned duplicate Replicate video runs when a
    missing ``history.row_versions`` partition was misread as HTTP 429.
    """
    from matrx_ai.providers.errors import RetryableError

    message = str(exc).strip() or type(exc).__name__
    details: dict[str, object] = {
        "suppressed_retry": True,
        "reason": "paid_provider_call_already_completed",
        "provider": provider,
        "modality": modality,
    }
    if isinstance(error_info, RetryableError):
        if not error_info.is_retryable:
            error_info.details.update(details)
            return error_info
        details.update(error_info.details or {})
        return RetryableError(
            error_type=(
                "post_provider_failure"
                if error_info.error_type in {"rate_limit", "unknown_error", "overloaded"}
                else error_info.error_type
            ),
            message=error_info.message or message,
            status_code=error_info.status_code,
            is_retryable=False,
            user_message=(
                error_info.user_message
                if error_info.error_type
                not in {"rate_limit", "unknown_error", "overloaded"}
                else (
                    f"{modality.title()} generation finished at {provider}, but "
                    "saving the result failed. It has been recorded — please try again."
                )
            ),
            details=details,
        )
    return RetryableError(
        error_type="post_provider_failure",
        message=message,
        is_retryable=False,
        user_message=(
            f"{modality.title()} generation finished at {provider}, but "
            "saving the result failed. It has been recorded — please try again."
        ),
        details=details,
    )


def _extract_prompt(unified_config: UnifiedConfig) -> str | None:
    """Pull the user's natural-language prompt from a media-gen request.

    Last user-role message wins. We concatenate every TextContent item
    in that message so multi-segment user inputs aren't truncated.
    Best-effort — returns None when the config shape doesn't contain
    a clean user prompt (e.g. assistant-only synthetic generations).
    """
    messages = getattr(unified_config, "messages", None) or []
    last_user_text: str | None = None
    for msg in messages:
        role = getattr(msg, "role", None) or (msg.get("role") if isinstance(msg, dict) else None)
        if role != "user":
            continue
        content = getattr(msg, "content", None) or (
            msg.get("content") if isinstance(msg, dict) else None
        )
        if isinstance(content, str):
            last_user_text = content
            continue
        if not isinstance(content, list):
            continue
        parts: list[str] = []
        for item in content:
            text_val: Any = getattr(item, "text", None) or (
                item.get("text") if isinstance(item, dict) else None
            )
            if isinstance(text_val, str) and text_val.strip():
                parts.append(text_val.strip())
        if parts:
            last_user_text = " ".join(parts)
    return last_user_text
