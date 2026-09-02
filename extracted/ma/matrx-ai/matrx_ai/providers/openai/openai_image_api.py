"""OpenAI image generation — gpt-image-2, gpt-image-1.5, gpt-image-1-mini.

Two endpoints:
  - ``client.images.generate(...)`` for text-to-image
  - ``client.images.edit(...)`` for image editing (single or multi-input + mask)

Plus optional partial-image streaming via ``partial_images=N`` + ``stream=True``.
Each partial costs +100 image-output tokens.

Routing: any image input (settings-level or role-tagged in the user message)
promotes the call to ``images.edit``; otherwise ``images.generate``.
"""

from __future__ import annotations

import base64
from typing import Any

from openai import AsyncOpenAI

from matrx_ai.config import UnifiedConfig, UnifiedResponse
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import (
    UnifiedMessage,
    iter_images_by_role,
    pick_image_by_role,
)
from matrx_ai.providers.base_media import (
    BaseMediaGeneration,
    GeneratedAsset,
)
from matrx_ai.providers.keys import keyed_provider_client
from matrx_ai.providers.outbound_capture import make_capture_http_client

from .translator import OpenAITranslator


class OpenAIImageGeneration(BaseMediaGeneration):
    provider = "openai"
    modality = "image"
    starting_message = "Generating image..."
    # gpt-image-* accept a `moderation` knob and carry OpenAI's built-in content
    # policy, so a minor's image request can be enforced-safe (WP13).
    supports_minor_safe_image = True

    client = keyed_provider_client(
        "OPENAI_API_KEY",
        factory=lambda api_key: AsyncOpenAI(
            api_key=api_key,
            http_client=make_capture_http_client(),
        ),
    )

    def __init__(self):
        self.translator = OpenAITranslator()

    @staticmethod
    def _is_edit(unified_config: UnifiedConfig) -> bool:
        # Any image input — settings-level or role-tagged in the user message —
        # promotes the call to the images.edit endpoint.
        if unified_config.image_input or unified_config.image_inputs:
            return True
        if pick_image_by_role(unified_config.messages, "start_image") is not None:
            return True
        if pick_image_by_role(unified_config.messages, None) is not None:
            return True
        if pick_image_by_role(unified_config.messages, "mask") is not None:
            return True
        for _ in iter_images_by_role(unified_config.messages, "reference"):
            return True
        return False

    def _build_kwargs(
        self, unified_config: UnifiedConfig, profile: Any
    ) -> dict[str, Any]:
        """Structural assembly for both endpoints; scalar params come from the
        catalog rules (translator_key ``openai_image`` — _ai_029) with the
        ``operation`` context deciding the generate-only knobs (size default,
        moderation, background)."""
        is_edit = self._is_edit(unified_config)
        prompt = self.translator._extract_prompt(unified_config)
        params = self._outbound_params(
            profile.controls,
            unified_config,
            context={"operation": "edit" if is_edit else "generate"},
        )
        kwargs: dict[str, Any] = {
            "model": unified_config.model,
            "prompt": prompt,
            **params,
        }
        if not is_edit:
            return kwargs

        # Edit endpoint — multipart image inputs. Collect in stable order:
        # user-message-tagged images (start_image first, then references, then
        # any un-tagged image), fall back to settings image_input/image_inputs.
        kwargs["_is_edit"] = True
        inputs: list[Any] = []
        start = pick_image_by_role(unified_config.messages, "start_image")
        if start is None:
            start = pick_image_by_role(unified_config.messages, None)
        if start is not None:
            inputs.append(start)
        for ref in iter_images_by_role(unified_config.messages, "reference"):
            inputs.append(ref)
        if not inputs:
            if unified_config.image_input is not None:
                inputs.append(unified_config.image_input)
            for ref in unified_config.image_inputs or []:
                inputs.append(ref)
        if not inputs:
            raise ValueError("openai image edit called with no image_input/image_inputs")

        image_files = [self.translator._mediaref_to_file_tuple(r) for r in inputs if r is not None]
        image_files = [f for f in image_files if f is not None]
        if not image_files:
            raise ValueError("All image inputs failed to resolve to bytes.")
        kwargs["image"] = image_files if len(image_files) > 1 else image_files[0]

        # Mask for inpainting. Role-tagged user-message mask wins.
        mask_ref = pick_image_by_role(unified_config.messages, "mask") or unified_config.mask
        if mask_ref is not None:
            mask_file = self.translator._mediaref_to_file_tuple(mask_ref)
            if mask_file is not None:
                kwargs["mask"] = mask_file
        return kwargs

    def _apply_minor_image_overrides(
        self, kwargs: dict[str, Any], unified_config: UnifiedConfig, profile: Any
    ) -> None:
        # Force the strictest OpenAI moderation for a minor. Only the generate
        # endpoint accepts `moderation`; the edit endpoint doesn't take the
        # param (it would 400), and gpt-image edits still carry OpenAI's built-in
        # policy. `_is_edit` is stamped into kwargs by _build_kwargs.
        if not kwargs.get("_is_edit"):
            kwargs["moderation"] = "auto"

    def _telemetry_url(self, unified_config: UnifiedConfig, kwargs: dict[str, Any]) -> str:
        if self._is_edit(unified_config):
            return "https://api.openai.com/v1/images/edits"
        return "https://api.openai.com/v1/images/generations"

    async def _call_provider(self, kwargs: dict[str, Any]) -> Any:
        if self._is_edit_kwargs(kwargs):
            return await self.client.images.edit(**kwargs)
        return await self.client.images.generate(**kwargs)

    @staticmethod
    def _is_edit_kwargs(kwargs: dict[str, Any]) -> bool:
        # The translator stamps an internal flag on edit kwargs so we know
        # which client method to call; pop it before forwarding.
        return bool(kwargs.pop("_is_edit", False))

    def _extract_assets(self, raw: Any) -> list[GeneratedAsset]:
        """Walk the ImagesResponse `data` array — gpt-image-* always emits
        ``b64_json``. We surface usage + revised_prompt under metadata."""
        assets: list[GeneratedAsset] = []
        data = getattr(raw, "data", None) or []
        usage = getattr(raw, "usage", None)
        for item in data:
            b64 = getattr(item, "b64_json", None)
            if not b64:
                # Fallback for any URL-returning model variant.
                url = getattr(item, "url", None)
                if not url:
                    continue
                metadata = self._asset_metadata(item, usage)
                assets.append(
                    GeneratedAsset(url=url, mime_type=self._guess_mime(item), metadata=metadata)
                )
                continue
            try:
                data_bytes = base64.b64decode(b64)
            except Exception:
                continue
            metadata = self._asset_metadata(item, usage)
            assets.append(
                GeneratedAsset(
                    data=data_bytes,
                    mime_type=self._guess_mime(item),
                    metadata=metadata,
                )
            )
        return assets

    @staticmethod
    def _guess_mime(item: Any) -> str:
        # OpenAI gpt-image-* return the format chosen by `output_format`,
        # but the response item doesn't echo it back. Default png.
        return "image/png"

    @staticmethod
    def _asset_metadata(item: Any, usage: Any) -> dict[str, Any]:
        meta: dict[str, Any] = {}
        revised = getattr(item, "revised_prompt", None)
        if revised:
            meta["revised_prompt"] = revised
        if usage is not None:
            try:
                # gpt-image-* usage shape: input_tokens, output_tokens,
                # input_tokens_details {text_tokens, image_tokens},
                # output_tokens_details {image_tokens}.
                meta["usage"] = {
                    "input_tokens": getattr(usage, "input_tokens", None),
                    "output_tokens": getattr(usage, "output_tokens", None),
                }
            except Exception:
                pass
        return meta

    def _classify_error(self, exc: Exception) -> Any:
        from matrx_ai.providers.errors import classify_openai_error

        return classify_openai_error(exc)

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
        """Phase 2 — pull the OpenAI gpt-image-* per-asset metadata into
        canonical MediaGenerationMetadata. Includes ``revised_prompt``,
        normalised quality, requested/returned sizes, and the response id.
        """
        from matrx_ai.media.generation_metadata import (
            build_default_metadata,
            map_openai_image_response,
        )

        try:
            data = getattr(raw, "data", None) or []
            item = data[asset_index] if asset_index < len(data) else None
            if item is None:
                raise IndexError("no per-asset item")
            return map_openai_image_response(
                raw=raw, item=item, request_kwargs=request_kwargs,
                prompt=prompt or "",
                model=unified_config.model or "",
                n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )
        except Exception:
            return build_default_metadata(
                kind="image", provider="openai",
                model=unified_config.model or "",
                prompt=prompt, n_returned=n_returned,
                duration_ms=duration_ms, cost_usd=cost_usd,
            )

    def _provider_usage(self, raw: Any) -> tuple[int, int, int] | None:
        """gpt-image-* bill by REAL tokens ($/1M, no usage_basis on the tier) —
        surface ``raw.usage`` so the basis-aware base class bills the truth
        instead of the synthetic per-image unit (which read ``output_price`` as a
        flat $/image and overcharged ~1,000,000×).

        Usage shape: ``input_tokens``, ``output_tokens``,
        ``input_tokens_details {text_tokens, image_tokens, cached_tokens?}``.
        Mirrors ``TokenUsage.from_openai`` — split cached out of the input so it
        bills at the cached rate.
        """
        usage = getattr(raw, "usage", None)
        if usage is None:
            return None
        input_tokens = getattr(usage, "input_tokens", None)
        output_tokens = getattr(usage, "output_tokens", None)
        if input_tokens is None and output_tokens is None:
            return None
        details = getattr(usage, "input_tokens_details", None)
        cached = int(getattr(details, "cached_tokens", 0) or 0) if details is not None else 0
        inp = int(input_tokens or 0)
        out = int(output_tokens or 0)
        return (max(0, inp - cached), out, cached)

    def _provider_billing_components(self, raw: Any) -> dict[str, int]:
        usage = getattr(raw, "usage", None)
        if usage is None:
            return {}
        input_details = getattr(usage, "input_tokens_details", None)
        output_details = getattr(usage, "output_tokens_details", None)
        text = int(getattr(input_details, "text_tokens", 0) or 0)
        image = int(getattr(input_details, "image_tokens", 0) or 0)
        cached = int(getattr(input_details, "cached_tokens", 0) or 0)
        total_input = int(getattr(usage, "input_tokens", 0) or 0)
        output_image = int(
            getattr(output_details, "image_tokens", 0)
            or getattr(usage, "output_tokens", 0)
            or 0
        )
        components: dict[str, int] = {"output.image": output_image}
        unallocated_input = max(0, total_input - text - image)
        if unallocated_input:
            components["unallocated.input"] = unallocated_input
        if cached == 0:
            components.update({"input.text": text, "input.image": image})
        elif image == 0:
            components.update(
                {"input.text": max(0, text - cached), "cached_input.text": cached}
            )
        elif text == 0:
            components.update(
                {"input.image": max(0, image - cached), "cached_input.image": cached}
            )
        else:
            # OpenAI reports a combined cached count here, not how much belonged
            # to text versus image. Those components have different prices, so
            # an exact cost is impossible and must remain explicitly unknown.
            components["unallocated.cached_input"] = cached
        return components

    # ------------------------------------------------------------------
    # Streaming override — partial images via SSE
    # ------------------------------------------------------------------

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: Any,
        debug: bool = False,
    ) -> UnifiedResponse:
        # Default to the base class flow when partial-image streaming isn't
        # requested. The base class handles emitter, persistence, error
        # classification, etc. Setting partial_images > 0 implicitly opts
        # the user into the streaming path.
        if not unified_config.partial_images or unified_config.partial_images <= 0:
            return await super().execute(unified_config, profile, debug)

        return await self._await_paid_completion(
            self._execute_streaming(unified_config, profile, debug)
        )

    async def _execute_streaming(
        self,
        unified_config: UnifiedConfig,
        profile: Any,
        debug: bool = False,
    ) -> UnifiedResponse:
        # Streaming partials path. Drives the emitter ourselves; final
        # result is still wrapped in a UnifiedResponse with ImageContent.
        from matrx_connect.context.data_types import MediaBlockData
        from matrx_connect.context.events import InfoPayload
        from matrx_connect.context.media_block import (
            cloud_file_to_media_block,
            streaming_partial_image_block,
        )
        from matrx_utils import vcprint

        from matrx_ai.context.app_context import get_app_context
        from matrx_ai.providers.outbound_capture import stamp_call_meta

        emitter = get_app_context().emitter
        kwargs = self._build_kwargs(unified_config, profile)
        # Force streaming flags on.
        kwargs["stream"] = True
        if not kwargs.get("partial_images"):
            kwargs["partial_images"] = unified_config.partial_images or 2

        if debug:
            vcprint(kwargs, "[openai image stream] kwargs", color="blue")

        stamp_call_meta(
            provider="openai",
            model=unified_config.model,
            is_streaming=True,
        )

        if emitter:
            await emitter.send_info(
                InfoPayload(
                    code="image_generating",
                    system_message=self.starting_message,
                    user_message=self.starting_message,
                )
            )

        partial_count = 0
        final_b64: str | None = None
        revised_prompt: str | None = None
        final_event: Any = None
        try:
            if self._is_edit_kwargs(kwargs):
                stream = await self.client.images.edit(**kwargs)
            else:
                stream = await self.client.images.generate(**kwargs)

            # The stream response is an async iterator of typed events.
            async for event in stream:
                evt_type = getattr(event, "type", "") or ""
                if evt_type.endswith("partial_image"):
                    b64 = getattr(event, "b64_json", None)
                    if b64 and emitter:
                        partial_count += 1
                        await emitter.send_data(
                            MediaBlockData(
                                block=streaming_partial_image_block(
                                    base64=b64,
                                    progress=min(0.99, partial_count / 4.0),
                                    mime_type="image/png",
                                )
                            )
                        )
                elif evt_type.endswith("completed"):
                    final_b64 = getattr(event, "b64_json", None) or final_b64
                    revised_prompt = getattr(event, "revised_prompt", None) or revised_prompt
                    # The completed event carries the real ``usage`` block —
                    # keep it so _build_usage bills real tokens (not the
                    # synthetic per-image unit) on this streaming path too.
                    final_event = event

            if not final_b64:
                raise RuntimeError("OpenAI image streaming completed without final image.")

            data = base64.b64decode(final_b64)
            from matrx_ai.media import save_media_envelope_async

            metadata: dict[str, Any] = {}
            if revised_prompt:
                metadata["revised_prompt"] = revised_prompt

            # Build TokenUsage for the streaming path so model + cost flow
            # into CompletedRequest just like the non-streaming branch. Warm
            # pricing first so the basis-aware billing in _build_usage resolves;
            # pass the completed event as ``raw`` so _provider_usage sees the
            # real token usage.
            asset = GeneratedAsset(data=data, mime_type="image/png")
            try:
                from matrx_ai.config.usage_config import ensure_pricing_lookup

                await ensure_pricing_lookup()
            except Exception:
                pass
            usage = self._build_usage(
                unified_config,
                kwargs,
                final_event,
                [asset],
                offering_id=profile.offering_id,
                model_name=profile.model_name,
            )
            try:
                cost = usage.calculate_cost()
            except Exception:
                cost = None
            metadata["model"] = unified_config.model
            metadata["provider"] = self.provider
            if cost is not None:
                metadata["cost"] = round(cost, 6)

            # Persist via the canonical envelope helper — returns file_id +
            # every URL flavour so we can emit a canonical MediaBlockData
            # event with durable URLs populated.
            persisted = await save_media_envelope_async(
                content=data,
                mime_type="image/png",
                prompt=revised_prompt,
                model=unified_config.model,
                provider=self.provider,
                feature="ai_images",
                extra_metadata=metadata,
            )
            block = ImageContent(
                url=persisted.url,
                file_id=persisted.file_id,
                mime_type="image/png",
                metadata=metadata,
            )

            if emitter:
                # Build a synthetic cld_files-shaped dict from the persist
                # envelope so cloud_file_to_media_block can produce a
                # canonical ImageBlock without a follow-up DB read.
                synthetic_record = {
                    "id": persisted.file_id,
                    "storage_uri": persisted.storage_uri,
                    "file_path": persisted.file_path,
                    "file_name": persisted.file_name,
                    "mime_type": persisted.mime_type,
                    "size_bytes": persisted.size_bytes,
                    "visibility": persisted.visibility,
                    "metadata": metadata,
                }
                url_set = {
                    "url": persisted.url,
                    "cdn_url": persisted.cdn_url,
                    "download_url": persisted.download_url,
                }
                await emitter.send_data(
                    MediaBlockData(
                        block=cloud_file_to_media_block(
                            synthetic_record, url_set=url_set, kind_override="image",
                        )
                    )
                )

            messages = [UnifiedMessage(role="assistant", content=[block])]
            return UnifiedResponse(messages=messages, usage=usage)

        except Exception as exc:
            error_info = self._classify_error(exc)
            if emitter and error_info is not None:
                await emitter.send_error(
                    error_type=getattr(error_info, "error_type", "unknown_error"),
                    message=getattr(error_info, "message", str(exc)),
                    user_message=getattr(error_info, "user_message", "Image generation failed."),
                )
            if error_info is not None:
                exc.error_info = error_info  # type: ignore[attr-defined]
            raise
