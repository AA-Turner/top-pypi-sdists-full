"""Google image generation — handles BOTH dedicated Imagen 4 endpoint and
Gemini 3.1 native multimodal image generation through the same provider class.

Branching is on the provider model id (the dialect fact — _ai_029 seeds the
matching per-offering rule set off the same split):
  - ``imagen-*``: ``client.models.generate_images(...)`` for Imagen 4
    (text-only, dedicated endpoint, single-call sync).
  - everything else (gemini-*-image): ``client.models.generate_content(...,
    response_modalities=["TEXT","IMAGE"])`` for Gemini native image
    generation (multimodal, supports image+text inputs and edits).

Both return ``UnifiedResponse(messages=[UnifiedMessage(role="assistant",
content=[ImageContent(...)])])`` with the canonical file URL on each
``ImageContent``.
"""

from __future__ import annotations

from typing import Any

from google import genai
from matrx_utils import vcprint

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)
from matrx_ai.providers.keys import keyed_provider_client

from .translator import GoogleTranslator


class GoogleImageGeneration(BaseMediaGeneration):
    provider = "google"
    modality = "image"
    starting_message = "Generating image..."
    # Imagen (safety_filter_level/person_generation) and Gemini-native
    # (safety_settings) both accept an enforceable strict posture for minors (WP13).
    supports_minor_safe_image = True

    client = keyed_provider_client(
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_AI_STUDIO",
        factory=lambda api_key: genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1beta"},
        ),
    )

    def __init__(self):
        self.translator = GoogleTranslator()
        # Dialect for the in-flight call — set in _build_kwargs so
        # _call_provider can dispatch to the right SDK method.
        self._is_imagen_call: bool = False

    @staticmethod
    def _is_imagen(unified_config: UnifiedConfig) -> bool:
        """Imagen models ride the dedicated ``generate_images`` endpoint; every
        other google_image offering (gemini-*-image) is native multimodal
        ``generate_content``. The provider model id IS the dialect fact — the
        matching offering.override (imagen vs native rule set, _ai_029) is
        seeded off the same split."""
        return (unified_config.model or "").startswith("imagen")

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        """Structural SDK-object nesting; every scalar param (counts, aspect
        gates, image_size tiers, output mime, the fixed safety/rai posture)
        comes from the catalog rules — translator_key ``google_image``, per
        dialect via offering.override (_ai_029)."""
        from google.genai import types

        self._is_imagen_call = self._is_imagen(unified_config)
        prompt = self.translator._extract_prompt(unified_config)
        params = self._outbound_params(profile.controls, unified_config)

        if self._is_imagen_call:
            # The two fixed-posture params are string consts in the DB — coerce
            # to the SDK enums the GenerateImagesConfig fields expect.
            if "safety_filter_level" in params:
                params["safety_filter_level"] = types.SafetyFilterLevel(
                    params["safety_filter_level"]
                )
            if "person_generation" in params:
                params["person_generation"] = types.PersonGeneration(params["person_generation"])
            return {
                "model": unified_config.model,
                "prompt": prompt,
                "config": types.GenerateImagesConfig(**params),
            }

        if params.get("image_size") == "0.5K":
            replacement = (
                "512"
                if (unified_config.model or "").startswith("gemini-3.1-flash-image")
                else "1K"
            )
            vcprint(
                "[google image] Retired image_size '0.5K' reached the provider "
                f"boundary; sending the model-supported equivalent '{replacement}'. "
                "Fix the catalog rule that emitted the retired alias.",
                color="red",
            )
            params["image_size"] = replacement

        # Native (generate_content with image modality): prompt + input images
        # are structural; the flat params (aspect_ratio / image_size) nest
        # under ImageConfig.
        from matrx_ai.providers.google.translator import _LOWEST_SAFETY_SETTINGS

        contents_parts: list[Any] = [prompt] if prompt else []
        for ref in self.translator._iter_image_refs(unified_config):
            part = self.translator._mediaref_to_genai_image(ref)
            if part is not None:
                contents_parts.append(part)

        gen_config_kwargs: dict[str, Any] = {
            "response_modalities": ["TEXT", "IMAGE"],
            "safety_settings": list(_LOWEST_SAFETY_SETTINGS),
        }
        if params:
            gen_config_kwargs["image_config"] = types.ImageConfig(**params)

        return {
            "model": unified_config.model,
            "contents": contents_parts or [prompt],
            "config": types.GenerateContentConfig(**gen_config_kwargs),
        }

    def _apply_minor_image_overrides(
        self, kwargs: dict[str, Any], unified_config: UnifiedConfig, profile: Any
    ) -> None:
        # Tighten the adjustable safety posture to its strictest for a minor,
        # mutating the already-built SDK config in place. Recompute the dialect
        # from unified_config (never the racy self._is_imagen_call instance flag,
        # since provider instances are cached process-wide).
        from google.genai import types

        from matrx_ai.providers.google.translator import _STRICT_MINOR_SAFETY_SETTINGS

        config = kwargs.get("config")
        if config is None:
            raise ValueError("google image kwargs missing 'config' for minor safety override")
        if self._is_imagen(unified_config):
            # Imagen: strictest filter + never generate images of children.
            config.safety_filter_level = types.SafetyFilterLevel.BLOCK_LOW_AND_ABOVE
            config.person_generation = types.PersonGeneration.ALLOW_ADULT
        else:
            # Gemini-native generate_content: replace the lowest-posture
            # safety_settings with the strict minor set.
            config.safety_settings = list(_STRICT_MINOR_SAFETY_SETTINGS)

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        model = kwargs.get("model") or unified_config.model or "unknown"
        method = "generateImages" if self._is_imagen_call else "generateContent"
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:{method}"

    def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        if self._is_imagen_call:
            return self.client.models.generate_images(**kwargs)
        return self.client.models.generate_content(**kwargs)

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        if self._is_imagen_call:
            return self._extract_imagen_assets(raw)
        return self._extract_native_assets(raw)

    @staticmethod
    def _extract_imagen_assets(raw: Any) -> list[GeneratedAsset]:
        assets: list[GeneratedAsset] = []
        for gi in getattr(raw, "generated_images", None) or []:
            image = getattr(gi, "image", None)
            if image is None:
                continue
            data = getattr(image, "image_bytes", None)
            mime = getattr(image, "mime_type", None) or "image/png"
            metadata: dict[str, Any] = {}
            rai_reason = getattr(gi, "rai_filtered_reason", None)
            if rai_reason:
                metadata["rai_filtered_reason"] = rai_reason
            if data:
                assets.append(GeneratedAsset(data=data, mime_type=mime, metadata=metadata or None))
        return assets

    @staticmethod
    def _extract_native_assets(raw: Any) -> list[GeneratedAsset]:
        assets: list[GeneratedAsset] = []
        candidates = getattr(raw, "candidates", None) or []
        for cand in candidates:
            content = getattr(cand, "content", None)
            if content is None:
                continue
            for part in getattr(content, "parts", None) or []:
                inline = getattr(part, "inline_data", None)
                if inline is None:
                    continue
                data = getattr(inline, "data", None)
                mime = getattr(inline, "mime_type", None) or "image/png"
                if not data:
                    continue
                # `data` may already be raw bytes (newer SDK) or a base64 str
                # (older versions). Normalise to bytes.
                if isinstance(data, str):
                    import base64

                    try:
                        data = base64.b64decode(data)
                    except Exception:
                        continue
                metadata: dict[str, Any] = {}
                if getattr(part, "thought", False):
                    metadata["thought"] = True
                ts = getattr(part, "thought_signature", None)
                if ts:
                    # thought_signature is raw binary — base64 it so it is
                    # JSON/JSONB-safe (never raw bytes, never NUL bytes) for the
                    # live-stream path and any consumer downstream.
                    if isinstance(ts, bytes):
                        import base64

                        metadata["thought_signature"] = base64.b64encode(ts).decode("ascii")
                        metadata["thought_signature_encoding"] = "base64"
                    else:
                        metadata["thought_signature"] = ts
                assets.append(GeneratedAsset(data=data, mime_type=mime, metadata=metadata or None))
        return assets

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_google_error

        return classify_google_error(exc)

    def _provider_usage(self, raw: Any) -> tuple[int, int, int] | None:
        """Imagen (``generate_images``) bills per-image — the pricing tier
        carries ``usage_basis="image_output"`` and no token usage is reported, so
        return None (the base class uses the synthetic per-image count).

        Gemini image-native (``generate_content``) is token-priced ($/1M, no
        usage_basis) and reports real usage on ``raw.usage_metadata``; surface it
        so the basis-aware base class bills real tokens instead of treating
        ``output_price`` as a flat $/image. Mirrors ``TokenUsage.from_gemini``.
        """
        if self._is_imagen_call:
            return None
        um = getattr(raw, "usage_metadata", None)
        if um is None:
            return None
        prompt_tokens = getattr(um, "prompt_token_count", None)
        candidates_tokens = getattr(um, "candidates_token_count", None)
        if prompt_tokens is None and candidates_tokens is None:
            return None
        cached = int(getattr(um, "cached_content_token_count", 0) or 0)
        return (int(prompt_tokens or 0), int(candidates_tokens or 0), cached)

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
        """Phase 2 — Google Imagen / Gemini image canonical metadata mapper.
        Surfaces safetyAttributes as ``safety_flagged`` + ``provider_extras.safety``.
        """
        from matrx_ai.media.generation_metadata import (
            build_default_metadata,
            map_google_imagen_response,
        )

        try:
            # Imagen response shape varies (generated_images vs predictions
            # vs candidates) per API; walk a few common paths to find the
            # per-asset item. Fall back to the asset's own metadata.
            candidates = (
                getattr(raw, "generated_images", None)
                or getattr(raw, "predictions", None)
                or getattr(raw, "candidates", None)
                or []
            )
            item = candidates[asset_index] if asset_index < len(candidates) else None
            if item is None:
                raise IndexError("no per-asset item")
            return map_google_imagen_response(
                raw=raw,
                item=item,
                request_kwargs=request_kwargs,
                prompt=prompt or "",
                model=unified_config.model or "",
                n_returned=n_returned,
                duration_ms=duration_ms,
                cost_usd=cost_usd,
            )
        except Exception:
            return build_default_metadata(
                kind="image",
                provider="google",
                model=unified_config.model or "",
                prompt=prompt,
                n_returned=n_returned,
                duration_ms=duration_ms,
                cost_usd=cost_usd,
            )
