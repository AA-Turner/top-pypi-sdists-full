"""
Multimodal AI Red Teaming attacks.

Probes multimodal models (vision, audio) with transformed inputs.
"""

from __future__ import annotations

import typing as t
from pathlib import Path

from dreadnode.core.transforms import Transform
from dreadnode.generators.message import ContentAudioInput, ContentImageUrl, Message
from dreadnode.optimization import Study
from dreadnode.optimization.stopping import score_value
from dreadnode.samplers import GridSampler

if t.TYPE_CHECKING:
    from dreadnode.core.scorer import Scorer
    from dreadnode.core.task import Task
    from dreadnode.core.types import Audio, Image

OBJECTIVE_SCORE_KEY = "objective"


def _build_message(
    prompt: str,
    image: Image | None = None,
    audio: Audio | None = None,
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

    return Message(role="user", content=content)


async def _apply_transforms(
    prompt: str,
    image: Image | None,
    audio: Audio | None,
    transforms: list[Transform[t.Any, t.Any]],
) -> tuple[str, Image | None, Audio | None]:
    """Apply transforms based on their modality attribute."""
    for transform in transforms:
        modality = transform.modality

        if modality == "image":
            if image is not None:
                image = await transform(image)
        elif modality == "audio":
            if audio is not None:
                audio = await transform(audio)
        else:
            # Default to text transform (modality is "text", "video", or None)
            prompt = await transform(prompt)

    return prompt, image, audio


def multimodal_attack(
    goal: str,
    target: Task[..., str],
    scorer: Scorer[str],
    *,
    image: Image | None = None,
    audio: Audio | None = None,
    transforms: list[t.Any] | None = None,
    n_iterations: int = 1,
    early_stopping_score: float | None = 0.8,
    name: str = "multimodal_attack",
    airt_assessment_id: str | None = None,
    airt_goal_category: str | None = None,
    airt_target_model: str | None = None,
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
        scorer: Scorer to evaluate target responses (e.g., jailbreak success).
        image: Optional image to include.
        audio: Optional audio to include.
        transforms: Transforms to apply (auto-detected by modality: image/audio/text).
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

    # Simple sampler for iterations
    sampler = GridSampler({"iteration": list(range(n_iterations))})

    async def objective(params: dict[str, t.Any]) -> dict[str, float]:
        """Apply transforms, call target, score response."""
        iteration = params["iteration"]

        # Apply transforms based on type
        transformed_goal, transformed_image, transformed_audio = await _apply_transforms(
            goal, image, audio, fitted_transforms
        )

        # Build message and call target
        message = _build_message(transformed_goal, transformed_image, transformed_audio)
        span = await target.run(message)
        response = span.output

        # Store sample in trial for tracking (include multimodal content for display)
        trial = current_trial.get()
        if trial is not None:
            sample_input: dict[str, t.Any] = {
                "iteration": iteration,
                "goal": transformed_goal,
            }
            # Include transformed image/audio for console display
            if transformed_image is not None:
                sample_input["image"] = transformed_image
            if transformed_audio is not None:
                sample_input["audio"] = transformed_audio
            # Store original paths for clickable links in console
            if image is not None:
                src = getattr(image, "_source_metadata", {}).get("source-path")
                if src:
                    sample_input["image_path"] = src
            if audio is not None:
                audio_data = getattr(audio, "_data", None)
                if isinstance(audio_data, (str, Path)) and Path(audio_data).exists():
                    sample_input["audio_path"] = str(audio_data)

            sample = Sample(
                input=sample_input,
                output=response,
                index=iteration,
            )
            trial.evaluation_result = EvalResult(samples=[sample])

        # Score the response
        score_result = await scorer.score(response)
        return {OBJECTIVE_SCORE_KEY: score_result.value}

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
        airt_category=airt_category,
        airt_sub_category=airt_sub_category,
        airt_attack_name=name,
        airt_goal=goal,
    )

    if early_stopping_score is not None:
        attack = attack.add_stop_condition(
            score_value(OBJECTIVE_SCORE_KEY, gte=early_stopping_score)
        )

    return attack
