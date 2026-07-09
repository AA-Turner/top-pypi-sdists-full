"""
Multimodal AI Red Teaming attacks.

Probes multimodal models (vision, audio) with transformed inputs.
"""

from __future__ import annotations

import contextlib
import typing as t

from dreadnode.core.transforms import Transform
from dreadnode.generators.message import (
    ContentAudioInput,
    ContentImageUrl,
    ContentText,
    ContentVideoUrl,
    Message,
)
from dreadnode.optimization import Study
from dreadnode.optimization.stopping import score_value
from dreadnode.samplers import GridSampler

if t.TYPE_CHECKING:
    from dreadnode.core.scorer import Scorer
    from dreadnode.core.task import Task
    from dreadnode.core.types import Audio, Image, Video

OBJECTIVE_SCORE_KEY = "objective"


def _build_message(
    prompt: str,
    image: Image | None = None,
    audio: Audio | None = None,
    video: Video | None = None,
) -> Message:
    """Build a multimodal Message from components."""
    import io

    content: list[t.Any] = [prompt]

    if image is not None:
        buffer = io.BytesIO()
        image.to_pil().save(buffer, format="PNG")
        content.append(ContentImageUrl.from_bytes(buffer.getvalue(), mimetype="image/png"))

    if audio is not None:
        audio_bytes, metadata = audio.to_serializable()
        content.append(
            ContentAudioInput.from_bytes(audio_bytes, format=metadata.get("extension", "mp3"))
        )

    if video is not None:
        video_bytes, metadata = video.to_serializable()
        ext = metadata.get("extension", "mp4")
        content.append(
            ContentVideoUrl.from_bytes(
                video_bytes, mimetype=f"video/{ext}", filename=f"video.{ext}"
            )
        )

    return Message(role="user", content=content)


async def _apply_transforms(
    prompt: str,
    image: Image | None,
    audio: Audio | None,
    video: Video | None,
    transforms: list[Transform[t.Any, t.Any]],
) -> tuple[str, Image | None, Audio | None, Video | None, dict[str, str]]:
    """
    Apply transforms based on their modality attribute.

    Returns the transformed inputs plus a map of modality -> last-applied transform name,
    used to tag provenance on the resulting message parts.
    """
    applied: dict[str, str] = {}
    for transform in transforms:
        modality = transform.modality
        name = getattr(transform, "name", None) or "transform"

        if modality == "image":
            if image is not None:
                image = await transform(image)
                applied["image"] = name
        elif modality == "audio":
            if audio is not None:
                audio = await transform(audio)
                applied["audio"] = name
        elif modality == "video":
            if video is not None:
                video = await transform(video)
                applied["video"] = name
        else:
            # Default to text transform (modality is "text" or None)
            prompt = await transform(prompt)
            applied["text"] = name

    return prompt, image, audio, video, applied


def _log_multimodal_parts(
    *,
    original_goal: str,
    transformed_goal: str,
    original_image: Image | None,
    transformed_image: Image | None,
    original_audio: Audio | None,
    transformed_audio: Audio | None,
    original_video: Video | None,
    transformed_video: Video | None,
    applied_transforms: dict[str, str],
    response: t.Any,
) -> None:
    """Emit candidate/response message parts + input_modality onto the trial span.

    Logs the **original** authored input parts (variant=``original``) followed by
    the **transformed** parts (variant=``adversarial``, tagged with the transform)
    for whichever modalities were actually transformed. This lets the UI render a
    clean Original → Transformed → Response message instead of only the final
    adversarial input. A modality that wasn't transformed appears once (original).
    """
    import json

    from dreadnode.tracing.constants import (
        AIRT_ATTRIBUTE_CANDIDATE_PARTS,
        AIRT_ATTRIBUTE_INPUT_MODALITY,
        AIRT_ATTRIBUTE_RESPONSE_PARTS,
    )
    from dreadnode.tracing.span import current_task_span

    from . import message_parts as mp

    span = current_task_span.get()
    if span is None:
        return

    try:
        # Original authored input (one part per present modality).
        candidate_parts: list[dict[str, t.Any]] = [mp.text_part(original_goal, variant="original")]
        if original_image is not None:
            candidate_parts.append(
                mp.image_part(
                    span, original_image, variant="original", filename="original_image.png"
                )
            )
        if original_audio is not None:
            candidate_parts.append(
                mp.audio_part(span, original_audio, variant="original", filename="original_audio")
            )
        if original_video is not None:
            candidate_parts.append(
                mp.video_part(span, original_video, variant="original", filename="original_video")
            )

        # Transformed (adversarial) input — only for modalities actually transformed.
        if "text" in applied_transforms:
            candidate_parts.append(
                mp.text_part(
                    transformed_goal,
                    variant="adversarial",
                    transform=applied_transforms["text"],
                )
            )
        if "image" in applied_transforms and transformed_image is not None:
            candidate_parts.append(
                mp.image_part(
                    span,
                    transformed_image,
                    transform=applied_transforms["image"],
                    variant="adversarial",
                    filename="transformed_image.png",
                )
            )
        if "audio" in applied_transforms and transformed_audio is not None:
            candidate_parts.append(
                mp.audio_part(
                    span,
                    transformed_audio,
                    transform=applied_transforms["audio"],
                    variant="adversarial",
                    filename="transformed_audio",
                )
            )
        if "video" in applied_transforms and transformed_video is not None:
            candidate_parts.append(
                mp.video_part(
                    span,
                    transformed_video,
                    transform=applied_transforms["video"],
                    variant="adversarial",
                    filename="transformed_video",
                )
            )

        response_parts = mp.response_to_parts(span, response)

        span.set_attribute(AIRT_ATTRIBUTE_CANDIDATE_PARTS, json.dumps(candidate_parts))
        span.set_attribute(AIRT_ATTRIBUTE_RESPONSE_PARTS, json.dumps(response_parts))
        span.set_attribute(AIRT_ATTRIBUTE_INPUT_MODALITY, mp.modality_from_parts(candidate_parts))
    except Exception:
        # Never fail a trial because part-logging failed — the text attributes still carry
        # the attack content for analytics.
        from loguru import logger

        logger.debug("Failed to log multimodal message parts", exc_info=True)


def _extract_response_modalities(response: t.Any) -> dict[str, t.Any]:
    """Decode a target response into per-modality scorable values.

    Returns a dict keyed by modality (``"text"``/``"image"``/``"audio"``/``"video"``).
    Text is a single concatenated string; media modalities are decoded into native
    SDK media objects (``Image``/``Audio``/``Video``) so a modality-specific scorer
    receives the type it expects. A str response yields ``{"text": <str>}`` — the
    exact value the single-scorer path scored before, keeping text-out behaviour
    (and every other attack that never emits media) unchanged.
    """
    from dreadnode.core.types import Audio, Image, Video

    out: dict[str, t.Any] = {}
    texts: list[str] = []

    def _walk(value: t.Any) -> None:
        if value is None:
            return
        if isinstance(value, str):
            if value:
                texts.append(value)
        elif isinstance(value, ContentText):
            if value.text:
                texts.append(value.text)
        elif isinstance(value, ContentImageUrl):
            with contextlib.suppress(Exception):
                out["image"] = Image(value.to_bytes())
        elif isinstance(value, ContentAudioInput):
            fmt = getattr(value.input_audio, "format", "wav") or "wav"
            with contextlib.suppress(Exception):
                out["audio"] = Audio(value.to_bytes(), format=fmt)
        elif isinstance(value, ContentVideoUrl):
            with contextlib.suppress(Exception):
                import base64

                data = base64.b64decode(value.file.file_data.split(",", 1)[-1])
                ext = (value.file.mimetype or "video/mp4").split("/")[-1]
                out["video"] = Video(data, format=ext)
        elif isinstance(value, Image):
            out["image"] = value
        elif isinstance(value, Audio):
            out["audio"] = value
        elif isinstance(value, Video):
            out["video"] = value
        elif isinstance(value, (list, tuple)):
            for item in value:
                _walk(item)
        elif isinstance(value, dict):
            for key in ("content", "content_parts", "parts", "text"):
                if key in value:
                    _walk(value[key])
                    break
        else:
            content = getattr(value, "content_parts", None) or getattr(value, "content", None)
            if content is not None and not isinstance(content, str):
                _walk(content)

    _walk(response)
    if texts:
        out["text"] = "\n".join(texts)
    return out


async def _score_multimodal_response(
    response: t.Any,
    *,
    text_scorer: Scorer[t.Any],
    response_scorers: dict[str, Scorer[t.Any]] | None,
) -> tuple[float, dict[str, float], str | None]:
    """Score each response modality and aggregate the trial score by MAX.

    Red-teaming aggregation is worst-case: if *any* output modality bypasses
    safety, the attack succeeded, so the objective score is the maximum across
    modalities. Per-modality scores are returned for display, and the winning
    (max) modality's rationale is surfaced as the judge reasoning.

    Backward compatible: with no ``response_scorers`` and a plain text (str)
    response, this scores exactly the same string with ``text_scorer`` as the
    prior single-``scorer.score(response)`` path did — text-out attacks and
    non-multimodal attacks are unaffected. Media modalities with no configured
    scorer are simply skipped (they can't be judged without a media scorer).
    """
    scorers: dict[str, Scorer[t.Any]] = dict(response_scorers or {})
    scorers.setdefault("text", text_scorer)

    modalities = _extract_response_modalities(response)
    per_modality: dict[str, float] = {}
    reasons: dict[str, str] = {}
    for modality, value in modalities.items():
        scorer = scorers.get(modality)
        if scorer is None:
            continue
        metric = await scorer.score(value)
        per_modality[modality] = float(metric.value)
        reason = (getattr(metric, "attributes", None) or {}).get("reason")
        if reason:
            reasons[modality] = str(reason)

    if not per_modality:
        # Nothing decoded (or no applicable scorer) — score the raw response so a
        # degenerate/unknown output shape still yields a metric.
        metric = await text_scorer.score(response)
        reason = (getattr(metric, "attributes", None) or {}).get("reason")
        value = float(metric.value)
        return value, {"text": value}, (str(reason) if reason else None)

    winning = max(per_modality, key=per_modality.__getitem__)
    return per_modality[winning], per_modality, reasons.get(winning)


def multimodal_attack(
    goal: str,
    target: Task[..., str],
    scorer: Scorer[str],
    *,
    response_scorers: dict[str, Scorer[t.Any]] | None = None,
    image: Image | None = None,
    audio: Audio | None = None,
    video: Video | None = None,
    transforms: list[t.Any] | None = None,
    n_iterations: int = 1,
    early_stopping_score: float | None = 0.8,
    name: str = "multimodal_attack",
    airt_assessment_id: str | None = None,
    airt_goal_category: str | None = None,
    airt_target_model: str | None = None,
    airt_attacker_model: str | None = None,
    airt_evaluator_model: str | None = None,
    airt_category: str | None = None,
    airt_sub_category: str | None = None,
) -> Study[dict[str, t.Any]]:
    """
    Multimodal red teaming attack with transform support.

    Probes a multimodal model by applying transforms to the input
    (image, audio, text) and evaluating responses.

    Args:
        goal: The text prompt to send to the model (consistent with goat_attack/tap_attack API).
        target: Task that takes a Message and returns a string response.
        scorer: Scorer to evaluate the target's *text* response (e.g., jailbreak
            success). Also used as the default text scorer for multimodal output.
        response_scorers: Optional per-modality scorers for multimodal *output*,
            keyed by ``"text"``/``"image"``/``"audio"``/``"video"``. When a target
            emits more than one modality (e.g. text + a generated image), each part
            is scored by its modality's scorer and the trial's objective score is
            the MAX across them — worst-case aggregation, since any single modality
            bypassing safety counts as a successful jailbreak. Per-modality scores
            are recorded on the trial span for display. Media modalities without a
            configured scorer are skipped. Omit this for text-out targets — behaviour
            is then identical to scoring the text response with ``scorer``.
        image: Optional image to include.
        audio: Optional audio to include.
        video: Optional video to include.
        transforms: Transforms to apply (auto-detected by modality: image/audio/video/text).
        n_iterations: Number of iterations to run.
        early_stopping_score: Stop if this score is reached. None to disable.
        name: Name for the attack study.

    Returns:
        A configured Study instance.

    Example:
        ```python
        from dreadnode.airt import multimodal_attack
        from dreadnode.transforms import image as img_transforms
        from dreadnode.transforms import audio as audio_transforms

        attack = multimodal_attack(
            "Describe what you see and hear",
            target=target,
            scorer=jailbreak_scorer,
            image=Image("photo.png"),
            audio=Audio("question.mp3"),
            transforms=[
                img_transforms.add_gaussian_noise(scale=0.1),
                audio_transforms.add_white_noise(snr_db=15),
            ],
            n_iterations=5,
            max_trials=5,
        )
        result = await attack.run()
        ```
    """
    from dreadnode.evaluations.result import EvalResult
    from dreadnode.evaluations.sample import Sample
    from dreadnode.optimization.study import current_trial

    # Fit transforms
    fitted_transforms = Transform.fit_many(transforms) if transforms else []

    # Names of the configured transforms, recorded at the finding level so the
    # findings table's "Transforms" column matches the per-part `transform`
    # provenance (otherwise the row shows "none" while the media part shows
    # e.g. `add_gaussian_noise`).
    transform_names = [getattr(tf, "name", None) or "transform" for tf in fitted_transforms]

    # Simple sampler for iterations
    sampler = GridSampler({"iteration": list(range(n_iterations))})

    async def objective(params: dict[str, t.Any]) -> dict[str, float]:
        """Apply transforms, call target, score response."""
        iteration = params["iteration"]

        # Apply transforms based on type
        (
            transformed_goal,
            transformed_image,
            transformed_audio,
            transformed_video,
            applied,
        ) = await _apply_transforms(goal, image, audio, video, fitted_transforms)

        # Build message
        message = _build_message(
            transformed_goal, transformed_image, transformed_audio, transformed_video
        )

        # Record the candidate ("attacker prompt") + trace Input as the transformed
        # goal *text* BEFORE calling the target. If the target then fails (e.g. a
        # provider error, so the response is empty), the finding still shows the
        # real prompt instead of the sampler's {"iteration": N} search state.
        # The Study logs `str(sample.input)` as `transformed_prompt`, so a dict
        # input would render as `{'iteration': 0, 'image': Image(...)}`; the
        # transformed media is carried losslessly in the message parts, so the
        # text is all we log here.
        trial = current_trial.get()
        if trial is not None:
            trial.candidate = transformed_goal
            # The trial span's "candidate" input was logged at TrialStart with the
            # sampler's raw search state; replace it with the goal text.
            from dreadnode.tracing.span import current_task_span as _cts

            _trial_span = _cts.get()
            if _trial_span is not None:
                with contextlib.suppress(Exception):
                    _trial_span._inputs = [
                        r for r in _trial_span._inputs if getattr(r, "name", None) != "candidate"
                    ]
                    _trial_span.log_input("candidate", transformed_goal)

        # Call the target. If it errors (auth failure, unreachable model, rate limit,
        # ...), record the error text as the response so the finding shows *why* it
        # failed instead of an opaque "(no response)", then re-raise so the trial is
        # still classified as an error (not a refusal).
        try:
            span = await target.run(message)
            response = span.output
        except Exception as target_exc:
            error_text = f"[target error] {type(target_exc).__name__}: {str(target_exc)[:500]}"
            with contextlib.suppress(Exception):
                _log_multimodal_parts(
                    original_goal=goal,
                    transformed_goal=transformed_goal,
                    original_image=image,
                    transformed_image=transformed_image,
                    original_audio=audio,
                    transformed_audio=transformed_audio,
                    original_video=video,
                    transformed_video=transformed_video,
                    applied_transforms=applied,
                    response=error_text,
                )
            if trial is not None:
                with contextlib.suppress(Exception):
                    trial.evaluation_result = EvalResult(
                        samples=[Sample(input=transformed_goal, output=error_text, index=iteration)]
                    )
            from dreadnode.tracing.span import current_task_span as _err_span_ctx

            _err_span = _err_span_ctx.get()
            if _err_span is not None:
                from dreadnode.tracing.constants import AIRT_ATTRIBUTE_JUDGE_REASONING

                with contextlib.suppress(Exception):
                    _err_span.set_attribute(AIRT_ATTRIBUTE_JUDGE_REASONING, error_text)
            raise

        # Persist the multimodal message parts (input + output) as content-addressed
        # artifacts on the trial span, so findings can render each part in the UI.
        _log_multimodal_parts(
            original_goal=goal,
            transformed_goal=transformed_goal,
            original_image=image,
            transformed_image=transformed_image,
            original_audio=audio,
            transformed_audio=transformed_audio,
            original_video=video,
            transformed_video=transformed_video,
            applied_transforms=applied,
            response=response,
        )

        if trial is not None:
            sample = Sample(
                input=transformed_goal,
                output=response,
                index=iteration,
            )
            trial.evaluation_result = EvalResult(samples=[sample])

        # Score the response. For multimodal *output* (e.g. text + a generated
        # image), each modality is scored by its own scorer and the objective is
        # the MAX — any modality bypassing safety = a successful jailbreak. For a
        # plain text response this reduces to scoring the text with `scorer`, so
        # text-out attacks are unaffected. The winning modality's rationale is
        # persisted so findings show *why* it scored ("Judge Reasoning"); the
        # per-modality breakdown is recorded for display.
        agg_score, modality_scores, reason = await _score_multimodal_response(
            response, text_scorer=scorer, response_scorers=response_scorers
        )
        from dreadnode.tracing.span import current_task_span

        trial_span = current_task_span.get()
        if trial_span is not None:
            if reason:
                from dreadnode.tracing.constants import AIRT_ATTRIBUTE_JUDGE_REASONING

                with contextlib.suppress(Exception):
                    trial_span.set_attribute(AIRT_ATTRIBUTE_JUDGE_REASONING, str(reason))
            if len(modality_scores) > 1:
                import json

                from dreadnode.tracing.constants import AIRT_ATTRIBUTE_MODALITY_SCORES

                with contextlib.suppress(Exception):
                    trial_span.set_attribute(
                        AIRT_ATTRIBUTE_MODALITY_SCORES, json.dumps(modality_scores)
                    )
        return {OBJECTIVE_SCORE_KEY: agg_score}

    attack: Study[dict[str, t.Any]] = Study(
        name=name,
        objective=objective,
        sampler=sampler,
        n_iterations=n_iterations,
        max_trials=n_iterations,
        tags=["airt"],
        airt_assessment_id=airt_assessment_id,
        airt_goal_category=airt_goal_category,
        airt_target_model=airt_target_model,
        airt_attacker_model=airt_attacker_model,
        airt_evaluator_model=airt_evaluator_model,
        airt_category=airt_category,
        airt_sub_category=airt_sub_category,
        airt_attack_name=name,
        airt_goal=goal,
        airt_transforms=transform_names or None,
    )

    if early_stopping_score is not None:
        attack = attack.add_stop_condition(
            score_value(OBJECTIVE_SCORE_KEY, gte=early_stopping_score)
        )

    return attack
