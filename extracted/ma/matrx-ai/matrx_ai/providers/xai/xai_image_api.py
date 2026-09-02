"""xAI grok-imagine image generation — gen, edit (single + multi-image).

Uses ``xai_sdk.AsyncClient.image`` because the OpenAI-compatible endpoint
doesn't cover edits cleanly. Supported via ``image.sample`` (n=1) and
``image.sample_batch`` (n>1):

- text-to-image: prompt + model, no image_url
- image edit (single): prompt + image_url
- image edit (multi, max 3 sources): prompt + image_urls=[u1, u2, u3]

Routing: any image input (settings-level or role-tagged) promotes the call to
the edit endpoint; otherwise text-to-image.
"""

from __future__ import annotations

import base64
from typing import Any

import xai_sdk

from matrx_ai.config import ProviderCharge, UnifiedConfig
from matrx_ai.config.message_config import (
    iter_images_by_role,
    pick_image_by_role,
    pick_text_by_role,
)
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)
from matrx_ai.providers.keys import keyed_provider_client


class XAIImageModerationError(RuntimeError):
    """Raised when xAI returns a response with no usable image because the
    request was blocked by moderation. Non-retryable: a retry will produce
    the exact same refusal and bill the account again."""


class XAIImageGeneration(BaseMediaGeneration):
    provider = "xai"
    modality = "image"
    starting_message = "Generating image (Grok)..."
    # xAI exposes no settable safety level (only after-the-fact moderation
    # detection), so we can't GUARANTEE a strict filter for a minor →
    # supports_minor_safe_image stays False (base default): a minor's Grok image
    # request is REFUSED before the paid call (WP13).

    def _provider_charge(self, raw: Any) -> ProviderCharge | None:
        from matrx_ai.providers.xai.translator import provider_charge_from_xai_usage

        usage = getattr(raw, "usage", None)
        return provider_charge_from_xai_usage(usage) if usage is not None else None

    # Built lazily on first ACCESS (grpc.aio needs a running event loop, so
    # never at import/__init__ time) and memoized on the RESOLVED KEY VALUE —
    # a host-side key rotation builds a fresh SDK client on the next request.
    client = keyed_provider_client(
        "XAI_API_KEY",
        factory=lambda api_key: xai_sdk.AsyncClient(api_key=api_key),
    )

    @staticmethod
    def _is_edit(unified_config: UnifiedConfig) -> bool:
        # Any image input — settings-level or role-tagged in the user message —
        # promotes the call to the edit endpoint.
        if unified_config.image_input or unified_config.image_inputs:
            return True
        if pick_image_by_role(unified_config.messages, "start_image") is not None:
            return True
        if pick_image_by_role(unified_config.messages, None) is not None:
            return True
        for _ in iter_images_by_role(unified_config.messages, "reference"):
            return True
        return False

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        prompt = self._extract_prompt(unified_config)
        # image_format const ("base64"), aspect_ratio derivation and the
        # 1k/2k resolution tiering are catalog rules (translator_key
        # ``xai_image`` — _ai_029).
        params = self._outbound_params(profile.controls, unified_config)
        kwargs: dict[str, Any] = {
            "prompt": prompt,
            "model": unified_config.model,
            **params,
        }

        # Image input(s) for edit ops — xai-sdk wants URLs, not bytes.
        # Prefer user-message-tagged images (start_image, reference, or first
        # un-tagged image), fall back to settings-level image_input/image_inputs.
        if self._is_edit(unified_config):
            inputs: list[str] = []
            start = (
                pick_image_by_role(unified_config.messages, "start_image")
                or pick_image_by_role(unified_config.messages, None)
            )
            if start is not None:
                u = self._mediaref_url(start)
                if u:
                    inputs.append(u)
            for ref in iter_images_by_role(unified_config.messages, "reference"):
                u = self._mediaref_url(ref)
                if u:
                    inputs.append(u)
            if not inputs:
                if unified_config.image_input is not None:
                    u = self._mediaref_url(unified_config.image_input)
                    if u:
                        inputs.append(u)
                for ref in unified_config.image_inputs or []:
                    u = self._mediaref_url(ref)
                    if u:
                        inputs.append(u)
            inputs = inputs[:3]  # xAI multi-image edit: max 3 sources
            if not inputs:
                raise ValueError(
                    "xai_image_edit needs image_input/image_inputs with a "
                    "resolved URL or fetchable bytes"
                )
            if len(inputs) == 1:
                kwargs["image_url"] = inputs[0]
            else:
                kwargs["image_urls"] = inputs
        return kwargs

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        if self._is_edit(unified_config):
            return "https://api.x.ai/v1/images/edits"
        return "https://api.x.ai/v1/images/generations"

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        """xai-sdk's ImageResponse: ``base64`` str or ``url`` str on the underlying proto.

        ``BaseImageResponse.base64`` / ``.url`` are Python properties that
        **raise ValueError** when their proto field is empty (and a different
        ValueError when ``respect_moderation`` is False). ``getattr(..., default)``
        does NOT swallow ValueError, so reading those properties directly is
        unsafe. Read the raw proto fields off ``_image`` instead — they're plain
        strings that are empty when unset, no exceptions.

        sample_batch returns a sequence; sample returns one item.
        """
        items = raw if isinstance(raw, (list, tuple)) else [raw]
        assets: list[GeneratedAsset] = []
        moderation_blocked = False
        for item in items:
            proto = getattr(item, "_image", None)
            if proto is None:
                continue
            respect_moderation = bool(getattr(proto, "respect_moderation", True))
            b64 = getattr(proto, "base64", "") or ""
            url = getattr(proto, "url", "") or ""
            # xAI doesn't return a mime_type on the proto; default per format.
            mime = "image/jpeg"
            if not b64 and not url:
                if not respect_moderation:
                    moderation_blocked = True
                continue
            if b64:
                # SDK may emit either raw base64 or a "data:<mime>;base64,<...>" URI.
                payload = b64.split("base64,", 1)[-1]
                try:
                    data = base64.b64decode(payload)
                except Exception:
                    continue
                assets.append(GeneratedAsset(data=data, mime_type=mime))
            else:
                assets.append(GeneratedAsset(url=url, mime_type=mime))
        if not assets and moderation_blocked:
            raise XAIImageModerationError(
                "xAI Grok-imagine refused to generate the image because it "
                "did not respect moderation rules."
            )
        return assets

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import RetryableError, classify_xai_error

        if isinstance(exc, XAIImageModerationError):
            return RetryableError(
                error_type="content_filtered",
                message=str(exc),
                is_retryable=False,
                user_message=(
                    "xAI Grok-imagine refused to generate this image because it "
                    "violates content policy. Adjust the prompt and try again."
                ),
            )

        # Defense-in-depth: any time the SDK's raising properties leak through
        # (e.g. someone reintroduces ``item.url`` access), classify as a
        # provider-side malformed-response — non-retryable, since retrying
        # bills the account again for the same failure.
        msg = str(exc)
        if isinstance(exc, ValueError) and (
            "Image was not returned via URL" in msg
            or "Image was not returned via base64" in msg
            or "did not respect moderation rules" in msg
        ):
            is_moderation = "moderation" in msg
            return RetryableError(
                error_type="content_filtered" if is_moderation else "provider_response_invalid",
                message=msg,
                is_retryable=False,
                user_message=(
                    "xAI Grok-imagine refused to generate this image because it "
                    "violates content policy. Adjust the prompt and try again."
                    if is_moderation
                    else "xAI returned an image response without usable content. "
                    "This will not improve on retry; the request was not produced."
                ),
            )

        return classify_xai_error(exc)

    @staticmethod
    def _extract_prompt(config: UnifiedConfig) -> str:
        return pick_text_by_role(config.messages, None) or ""

    @staticmethod
    def _mediaref_url(ref: Any) -> str | None:
        if ref is None:
            return None
        url = (
            getattr(ref, "resolved_url", None)
            or getattr(ref, "url", None)
            or (ref.get("resolved_url") or ref.get("url") if isinstance(ref, dict) else None)
        )
        if url:
            return url
        # If only base64_data is present, build a data URI.
        b64 = getattr(ref, "base64_data", None) or (
            ref.get("base64_data") if isinstance(ref, dict) else None
        )
        mime = (
            getattr(ref, "mime_type", None)
            or (ref.get("mime_type") if isinstance(ref, dict) else None)
            or "image/png"
        )
        if b64:
            return f"data:{mime};base64,{b64}"
        return None

    # Override execute() to use _build_kwargs_with_n (so we know n at call site)
    async def execute(self, unified_config, profile, debug=False):
        # Stash n on self so _call_provider can read it; the base class
        # passes only the kwargs dict, which we don't want to pollute with
        # a private field. n is STRUCTURAL for xai — it rides the
        # sample_batch positional args, never the request kwargs.
        self._pending_n = max(1, min(unified_config.count or 1, 10))
        return await super().execute(unified_config, profile, debug)

    def _map_generation_metadata(
        self,
        *,
        raw: Any,
        asset,
        asset_index: int,
        request_kwargs: dict[str, Any],
        unified_config,
        prompt,
        n_returned: int,
        duration_ms,
        cost_usd,
    ):
        """Phase 2b — xAI grok-imagine canonical metadata mapper.
        Surfaces ``revised_prompt`` (grok rewrites prompts the way
        OpenAI does) and width/height when the SDK populates them."""
        from matrx_ai.media.generation_metadata import (
            build_default_metadata,
            map_xai_image_response,
        )

        try:
            # xAI response: raw is the sample response object; iterate
            # over .images / .data when sample_batch was used, else raw
            # itself is the single item.
            items = (
                getattr(raw, "images", None)
                or getattr(raw, "data", None)
                or [raw]
            )
            item = items[asset_index] if asset_index < len(items) else items[0]
            return map_xai_image_response(
                raw=raw, item=item, request_kwargs=request_kwargs,
                prompt=prompt or "",
                model=unified_config.model or "",
                n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )
        except Exception:
            return build_default_metadata(
                kind="image", provider="xai",
                model=unified_config.model or "",
                prompt=prompt, n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:  # type: ignore[no-redef]
        n = getattr(self, "_pending_n", 1)
        prompt = kwargs.pop("prompt")
        model = kwargs.pop("model")
        if n > 1:
            return await self.client.image.sample_batch(prompt, model, n, **kwargs)
        return await self.client.image.sample(prompt, model, **kwargs)
