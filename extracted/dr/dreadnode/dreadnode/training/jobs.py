"""Sandbox-facing job payloads, entrypoints, and result contracts for training."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import os
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Protocol, Self

import httpx
import numpy as np
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from dreadnode import Dreadnode
from dreadnode.agents import Agent
from dreadnode.agents.tools import Toolset, tool_method
from dreadnode.generators.generator import GeneratedMessage, GenerateParams, Generator, Usage
from dreadnode.generators.message import Message
from dreadnode.tools.task import finish_task, give_up_on_task
from dreadnode.training.etl import (
    OpenAIConversation,
    RLPromptRow,
    load_conversations_from_worlds_dataset,
    load_prompt_rows_from_dataset,
    load_rl_prompt_rows_from_worlds_dataset,
)
from dreadnode.training.etl.sft import (
    SFTConversation,
    load_openai_conversations_from_dataset,
    load_sft_conversations_from_dataset,
)
from dreadnode.training.recipes import (
    RewardPromptRow,
    RewardRecipeRegistry,
    RewardTaskDefinition,
)
from dreadnode.training.rollouts.worlds import (
    build_worlds_reward_shaper_from_config,
    run_worlds_agent_rollout,
)
from dreadnode.training.tinker import (
    TinkerSFTConfig,
    TinkerSFTTrainer,
    load_from_conversations,
    load_from_messages,
)
from dreadnode.training.tinker.rl import (
    TinkerRLConfig,
    TinkerRLRolloutGroup,
    train_tinker_rl,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from dreadnode.training.tinker.trainer import TrainingState


TrainingJobBackend = Literal["tinker", "ray"]
TrainingJobTrainerType = Literal["sft", "rl"]
TrainingJobStatus = Literal["completed", "failed", "cancelled"]


class TrainingCapabilityPayload(BaseModel):
    """Capability metadata resolved by the API control plane."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    version: str
    runtime_digest: str | None = None
    manifest: dict[str, Any]
    file_manifest: list[dict[str, Any]]
    artifact_s3_prefix: str
    entry_prompt: str | None = None


class TrainingDatasetPayload(BaseModel):
    """Dataset metadata resolved by the API control plane."""

    model_config = ConfigDict(extra="forbid")

    id: str
    reference: str
    name: str
    version: str
    format: str
    row_count: int | None = None
    splits: dict[str, Any] | None = None
    artifacts: dict[str, Any]
    summary: str | None = None


class TrainingTaskPayload(BaseModel):
    """Task metadata resolved by the API control plane."""

    model_config = ConfigDict(extra="forbid")

    id: str
    reference: str
    name: str
    version: str
    instruction: str | None = None
    ports: dict[str, Any] | None = None
    verification: dict[str, Any] | None = None
    solution: dict[str, Any] | None = None
    sandbox_provider: str
    s3_key: str


class TrainingWorldPayload(BaseModel):
    """Worlds backend metadata resolved by the API control plane."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str | None = None
    manifest_backend_id: str | None = None
    server_url: str
    auth_token: str | None = None
    artifact_refs: dict[str, Any] = Field(default_factory=dict)
    stats: dict[str, Any] = Field(default_factory=dict)


class BaseTrainingJobPayload(BaseModel):
    """Common payload fields for hosted training execution."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["2026-03-18"] = "2026-03-18"
    job_id: str
    organization_id: str
    workspace_id: str
    created_by: str | None = None
    name: str | None = None
    backend: TrainingJobBackend
    trainer_type: TrainingJobTrainerType
    algorithm: str | None = None
    model: str
    project_ref: str | None = None
    run_ref: str | None = None
    tags: list[str] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)


class TinkerSFTJobPayload(BaseTrainingJobPayload):
    """Resolved payload for a Tinker SFT sandbox job."""

    backend: Literal["tinker"] = "tinker"
    trainer_type: Literal["sft"] = "sft"
    capability: TrainingCapabilityPayload
    dataset: TrainingDatasetPayload | None = None
    trajectory_datasets: list[TrainingDatasetPayload] = Field(default_factory=list)
    eval_dataset: TrainingDatasetPayload | None = None


class TinkerRLJobPayload(BaseTrainingJobPayload):
    """Resolved payload for a Tinker RL sandbox job."""

    backend: Literal["tinker"] = "tinker"
    trainer_type: Literal["rl"] = "rl"
    capability: TrainingCapabilityPayload
    task: TrainingTaskPayload | None = None
    world: TrainingWorldPayload | None = None
    prompt_dataset: TrainingDatasetPayload | None = None
    trajectory_datasets: list[TrainingDatasetPayload] = Field(default_factory=list)
    eval_dataset: TrainingDatasetPayload | None = None
    reward_recipe: dict[str, Any] | None = None
    eval_interval: int | None = None
    eval_max_rollouts: int | None = None


_WORLDS_AGENT_SYSTEM_PROMPT = (
    "You are an expert penetration tester operating in a simulated Active Directory "
    "environment. Explore the network, enumerate resources, obtain credentials, and "
    "escalate privileges toward the stated goal. Execute commands methodically, use "
    "tool results to inform the next step, and finish the task when you have reached "
    "the goal or cannot make further progress."
)


class _WorldsHTTPToolset(Toolset):
    """Minimal HTTP toolset for interacting with a live Worlds backend."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    server_url: str
    auth_token: str | None = None

    _client: httpx.AsyncClient | None = PrivateAttr(default=None)
    _principal_id: str | None = PrivateAttr(default=None)
    _host_id: str | None = PrivateAttr(default=None)
    _domain: str | None = PrivateAttr(default=None)
    _known_creds: list[str] = PrivateAttr(default_factory=list)
    _compromised_hosts: list[str] = PrivateAttr(default_factory=list)

    async def __aenter__(self) -> Self:
        if self._client is None:
            headers = (
                {"Authorization": f"Bearer {self.auth_token}"}
                if self.auth_token is not None
                else None
            )
            self._client = httpx.AsyncClient(
                base_url=self.server_url,
                timeout=30.0,
                headers=headers,
            )
        return self

    async def __aexit__(self, *args: object) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @tool_method(variants=["all"])
    async def list_commands(self) -> dict[str, Any]:
        """List the commands available in the Worlds environment."""

        client = self._require_client()
        response = await client.get("/commands")
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, dict):
            return payload
        return {"commands": []}

    @tool_method(variants=["all"])
    async def run_command(self, command: str) -> dict[str, Any]:
        """Execute a shell-like command against the Worlds backend."""

        client = self._require_client()
        request_body = {
            "command": command,
            "principal_id": self._principal_id,
            "host_id": self._host_id,
            "domain": self._domain,
            "known_creds": list(self._known_creds),
            "compromised_hosts": list(self._compromised_hosts),
        }
        response = await client.post("/run", json=request_body)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict):
            raise TypeError("Worlds backend returned a non-object run response")

        context_updates = result.get("context_updates")
        if isinstance(context_updates, dict):
            principal_id = context_updates.get("principal_id")
            host_id = context_updates.get("host_id")
            domain = context_updates.get("domain")
            compromised_host = context_updates.get("compromised_host")
            acquired_cred = context_updates.get("acquired_cred")
            if isinstance(principal_id, str):
                self._principal_id = principal_id
            if isinstance(host_id, str):
                self._host_id = host_id
            if isinstance(domain, str):
                self._domain = domain
            if (
                isinstance(compromised_host, str)
                and compromised_host not in self._compromised_hosts
            ):
                self._compromised_hosts.append(compromised_host)
            if isinstance(acquired_cred, str) and acquired_cred not in self._known_creds:
                self._known_creds.append(acquired_cred)

        return {
            "stdout": result.get("stdout", ""),
            "stderr": result.get("stderr", ""),
            "exit_code": result.get("exit_code", 0),
            "events": result.get("events", []),
            "context_updates": context_updates or {},
        }

    @tool_method(variants=["all"])
    async def get_context(self) -> dict[str, Any]:
        """Return the current mutable rollout context."""

        return {
            "principal_id": self._principal_id,
            "host_id": self._host_id,
            "domain": self._domain,
            "known_creds": list(self._known_creds),
            "compromised_hosts": list(self._compromised_hosts),
        }

    def _require_client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Worlds HTTP client has not been initialized")
        return self._client


class _TinkerSamplingGenerator(Generator):
    """Generator adapter that drives DN Agents from a Tinker sampling client."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    sampling_client: Any = Field(exclude=True)
    tokenizer: Any = Field(exclude=True)

    async def supports_function_calling(self) -> bool | None:
        return False

    def _generate_single_message(
        self,
        *,
        message_batch: list[Message],
        batch_params: GenerateParams,
    ) -> GeneratedMessage | BaseException:
        try:
            prompt_text = _render_prompt_text(
                tokenizer=self.tokenizer,
                messages=[
                    message.model_dump(exclude_none=True, mode="json") for message in message_batch
                ],
            )
            prompt_tokens = self.tokenizer.encode(
                prompt_text,
                add_special_tokens=True,
            )
            tinker = _get_tinker_module()
            sampling_params = _build_sampling_params(
                tinker=tinker,
                params=batch_params,
            )
            sample_response = self.sampling_client.sample(
                prompt=tinker.types.ModelInput.from_ints(tokens=prompt_tokens),
                sampling_params=sampling_params,
                num_samples=1,
            ).result()
            sequence = _extract_first_sequence(sample_response)
            completion_tokens = list(getattr(sequence, "tokens", []))
            completion_text = self.tokenizer.decode(completion_tokens)
            usage = Usage(
                input_tokens=len(prompt_tokens),
                output_tokens=len(completion_tokens),
                total_tokens=len(prompt_tokens) + len(completion_tokens),
            )
            return GeneratedMessage(
                message=Message(role="assistant", content=completion_text),
                stop_reason=_stop_reason_from_sampling_response(sample_response),
                usage=usage,
                extra={"raw_generated_text": completion_text},
            )
        except Exception as exc:
            return exc

    async def generate_messages(
        self,
        messages: Sequence[Sequence[Message]],
        params: Sequence[GenerateParams],
    ) -> Sequence[GeneratedMessage | BaseException]:
        results: list[GeneratedMessage | BaseException] = []
        for message_batch, batch_params in zip(messages, params, strict=False):
            results.append(
                self._generate_single_message(
                    message_batch=list(message_batch),
                    batch_params=batch_params,
                )
            )
        return results


TrainingJobPayload = TinkerSFTJobPayload | TinkerRLJobPayload


class TrainingJobResult(BaseModel):
    """Structured result written back by sandboxed training execution."""

    model_config = ConfigDict(extra="forbid")

    status: TrainingJobStatus
    metrics: dict[str, Any] = Field(default_factory=dict)
    artifacts: dict[str, Any] = Field(default_factory=dict)
    external_job_id: str | None = None
    error: str | None = None


def _build_configured_dreadnode() -> Dreadnode:
    """Return a configured Dreadnode client from sandbox environment variables."""

    return Dreadnode().configure(
        server=os.environ["DREADNODE_SERVER"],
        api_key=os.environ["DREADNODE_API_KEY"],
        organization=os.environ["DREADNODE_ORGANIZATION"],
        workspace=os.environ["DREADNODE_WORKSPACE"],
        project=os.environ.get("DREADNODE_PROJECT") or None,
    )


def _build_tinker_sft_config(payload: TinkerSFTJobPayload) -> TinkerSFTConfig:
    """Build a Tinker SFT config from a sandbox job payload."""

    allowed_keys = {field.name for field in fields(TinkerSFTConfig)}
    config = {
        key: value
        for key, value in payload.config.items()
        if key in allowed_keys and value is not None
    }
    config["base_model"] = payload.model
    return TinkerSFTConfig(**config)


def _get_tinker_module() -> Any:
    """Return the installed Tinker runtime module."""

    try:
        return importlib.import_module("tinker")
    except ModuleNotFoundError as exc:
        raise RuntimeError("Tinker is not installed in the training environment") from exc


def _get_positive_int(
    config: dict[str, Any],
    key: str,
    *,
    default: int,
) -> int:
    value = config.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return default
    return value


def _get_positive_float(
    config: dict[str, Any],
    key: str,
    *,
    default: float,
) -> float:
    value = config.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int | float) or value <= 0:
        return default
    return float(value)


def _get_non_negative_float(
    config: dict[str, Any],
    key: str,
    *,
    default: float,
) -> float:
    value = config.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int | float) or value < 0:
        return default
    return float(value)


def _get_optional_string(config: dict[str, Any], key: str) -> str | None:
    value = config.get(key)
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _get_string_list(config: dict[str, Any], key: str) -> list[str]:
    value = config.get(key)
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def _messages_from_conversations(
    conversations: list[SFTConversation],
) -> list[list[dict[str, str]]]:
    """Extract normalized message lists from ETL conversation records."""

    return [conversation.messages for conversation in conversations]


def _build_sft_metrics(
    *,
    state: TrainingState,
    train_examples: int,
    gradient_accumulation_steps: int,
    learning_rate: float,
    eval_examples: int,
    eval_loss: float | None,
) -> dict[str, Any]:
    """Build hosted-job-friendly summary metrics and history from Tinker training state."""

    losses = [float(loss) for loss in getattr(state, "losses", [])]
    examples_seen = int(getattr(state, "total_sequences_processed", 0))
    metrics: dict[str, Any] = {
        # ``train/steps`` is the optimizer-step count actually run — the *step
        # budget* (derived from ``epochs``, or an explicit ``steps`` cap), NOT
        # ``epochs x batches``. The user-facing pass/coverage view lives in
        # ``train/epochs_completed`` and ``train/num_sequences_processed``
        # (examples seen). The UI labels these distinctly.
        "train/steps": int(getattr(state, "step", len(losses))),
        "train/num_examples": train_examples,
        "train/num_sequences_processed": examples_seen,
        "train/num_tokens_processed": int(getattr(state, "total_tokens_processed", 0)),
        "train/gradient_accumulation_steps": gradient_accumulation_steps,
    }
    if train_examples > 0:
        # Full passes over the data. Fractional when an explicit ``steps`` cap
        # stops training partway through an epoch.
        metrics["train/epochs_completed"] = round(examples_seen / train_examples, 3)
    if losses:
        history_steps = list(range(1, len(losses) + 1))
        metrics.update(
            {
                "steps": history_steps,
                # Namespaced per-step series — discovered by the UI under
                # docs/metrics_contract.md. ``train_loss`` and
                # ``learning_rate`` (no slash) stay as back-compat aliases
                # until MC Phase 3 drops them.
                "train/loss": list(losses),
                "train_loss": losses,
                "train/loss_last": losses[-1],
                "train/loss_mean": float(sum(losses) / len(losses)),
                "train/loss_best": min(losses),
            }
        )
        if learning_rate > 0:
            lr_series = [learning_rate] * len(losses)
            metrics["train/learning_rate"] = lr_series
            metrics["learning_rate"] = lr_series
        # NB: we intentionally do *not* emit a per-step ``val_loss`` series.
        # Tinker evaluates once, at the end of training, so the only honest
        # shapes are the scalar ``eval/loss`` and the single-point
        # ``eval/loss_history`` series on the ``eval/steps`` axis (both written
        # below). The legacy ``val_loss = [None, ..., eval_loss]`` form padded
        # every step but the last with ``None``, which rendered as a gap-riddled
        # chart line (ENG-6522). Per docs/metrics_contract.md: emit eval loss on
        # the ``eval/steps`` axis, not padded with ``None``.
    if eval_examples > 0:
        metrics["eval/num_examples"] = eval_examples
    if eval_loss is not None:
        # Scalar — existing callers/tests depend on this being a float.
        metrics["eval/loss"] = float(eval_loss)
        # Per MC P1: also emit the array form on ``eval/steps`` axis so the
        # UI can chart eval loss against the same step axis training uses.
        # Naming avoids clashing with the scalar key above; MC P3 will pick
        # whichever shape survives (likely the array).
        if losses:
            metrics["eval/steps"] = [len(losses)]
            metrics["eval/loss_history"] = [float(eval_loss)]
    return metrics


def _select_prompt_batch(
    *,
    prompt_rows: list[RLPromptRow],
    step: int,
    batch_size: int,
) -> list[RLPromptRow]:
    if batch_size >= len(prompt_rows):
        return prompt_rows
    start = ((step - 1) * batch_size) % len(prompt_rows)
    batch = prompt_rows[start : start + batch_size]
    if len(batch) == batch_size:
        return batch
    remainder = batch_size - len(batch)
    return batch + prompt_rows[:remainder]


def _render_instruction(
    instruction: str | None,
    context: dict[str, str | int | None],
) -> str | None:
    if not instruction:
        return instruction

    def _replacer(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        value = context.get(key)
        if value is None:
            return match.group(0)
        return str(value)

    return re.sub(r"\{\{\s*(\w+)\s*\}\}", _replacer, instruction)


def _render_task_instruction(
    *,
    prompt_row: RLPromptRow,
    task: TrainingTaskPayload | None,
) -> str | None:
    if task is None:
        return None
    if not task.instruction:
        return None
    rendered = _render_instruction(task.instruction, prompt_row.template_context)
    if rendered and "{{" not in rendered:
        return rendered.strip()
    return None


def _build_prompt_messages(
    *,
    prompt_row: RLPromptRow,
    capability_prompt: str | None,
    task_instruction: str | None,
) -> list[dict[str, str]]:
    system_parts = [
        part.strip()
        for part in (capability_prompt, task_instruction)
        if isinstance(part, str) and part.strip()
    ]
    messages: list[dict[str, str]] = []
    if system_parts:
        messages.append({"role": "system", "content": "\n\n".join(system_parts)})
    if prompt_row.messages:
        messages.extend(prompt_row.messages)
        return messages
    if prompt_row.prompt:
        messages.append({"role": "user", "content": prompt_row.prompt})
        return messages
    raise ValueError("Prompt row did not contain prompt text or messages")


def _render_prompt_text(
    *,
    tokenizer: Any,
    messages: list[dict[str, Any]],
) -> str:
    apply_chat_template = getattr(tokenizer, "apply_chat_template", None)
    if callable(apply_chat_template):
        try:
            rendered = apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            if isinstance(rendered, str) and rendered.strip():
                return rendered
        except (AttributeError, TypeError, ValueError):
            pass
    rendered_messages = []
    for message in messages:
        role = message["role"].capitalize()
        content = str(message.get("content", ""))
        tool_calls = message.get("tool_calls")
        if isinstance(tool_calls, list) and tool_calls:
            content = (f"{content}\n" if content else "") + json.dumps(
                {"tool_calls": tool_calls}, sort_keys=True
            )
        rendered_messages.append(f"{role}:\n{content}")
    return "\n\n".join(rendered_messages) + "\n\nAssistant:\n"


def _extract_target_logprobs(
    *,
    logprob_response: Any,
    target_length: int,
) -> list[float]:
    raw_logprobs = getattr(logprob_response, "prompt_logprobs", None)
    if raw_logprobs is None and isinstance(logprob_response, list | tuple):
        raw_logprobs = logprob_response
    if raw_logprobs is None and hasattr(logprob_response, "to_numpy"):
        raw_logprobs = logprob_response
    if raw_logprobs is None:
        wrapped_logprobs = getattr(logprob_response, "logprobs", None)
        if wrapped_logprobs is not None:
            raw_logprobs = wrapped_logprobs
    if raw_logprobs is None:
        loss_fn_outputs = getattr(logprob_response, "loss_fn_outputs", None)
        if isinstance(loss_fn_outputs, list) and loss_fn_outputs:
            first_output = loss_fn_outputs[0]
            if isinstance(first_output, dict):
                raw_logprobs = first_output.get("logprobs")
            else:
                raw_logprobs = getattr(first_output, "logprobs", None)
    if raw_logprobs is None:
        raise RuntimeError("Tinker compute_logprobs response is missing logprobs")
    if hasattr(raw_logprobs, "to_numpy"):
        raw_logprobs = raw_logprobs.to_numpy()
    values = [float(value) for value in raw_logprobs if value is not None]
    if len(values) < target_length:
        raise RuntimeError("Tinker compute_logprobs response was shorter than expected")
    return values[:target_length]


def _build_rl_datum(
    *,
    tinker: Any,
    full_tokens: list[int],
    prompt_token_count: int,
    reward: float,
    target_logprobs: list[float],
) -> Any:
    input_tokens = full_tokens[:-1]
    target_tokens = full_tokens[1:]
    token_rewards = [0.0] * prompt_token_count + [reward] * (len(full_tokens) - prompt_token_count)
    shifted_advantages = token_rewards[1:]
    if len(target_tokens) != len(target_logprobs) or len(target_tokens) != len(shifted_advantages):
        raise RuntimeError("RL datum shapes are inconsistent")
    return tinker.types.Datum(
        model_input=tinker.types.ModelInput.from_ints(tokens=input_tokens),
        loss_fn_inputs={
            "target_tokens": np.asarray(target_tokens, dtype=np.int32),
            "logprobs": np.asarray(target_logprobs, dtype=np.float32),
            "advantages": np.asarray(shifted_advantages, dtype=np.float32),
        },
    )


def _run_rl_eval_pass(
    *,
    sampling_client: Any,
    tokenizer: Any,
    eval_prompt_rows: list[RLPromptRow],
    capability_prompt: str | None,
    task: TrainingTaskPayload | None,
    reward_recipe: dict[str, Any] | None,
    reward_registry: RewardRecipeRegistry,
    reward_task: RewardTaskDefinition | None,
    config: TinkerRLConfig,
    tinker: Any,
    step: int,
    callback: Any,
    eval_max_rollouts: int,
) -> None:
    """Sample the eval prompt set deterministically and push ``eval/*`` series.

    Uses ``temperature=0.0`` (greedy) so the held-out reward signal isn't
    polluted by sampling variance — each step's eval reward reflects the
    current policy's deterministic best guess. Scores via the same recipe
    as training so the train/eval curves are directly comparable.
    """

    if callback is None or not eval_prompt_rows:
        return

    sampled_rows = eval_prompt_rows[:eval_max_rollouts]
    rewards: list[float] = []
    extraction_failed_count = 0

    for prompt_row in sampled_rows:
        task_instruction = _render_task_instruction(prompt_row=prompt_row, task=task)
        prompt_messages = _build_prompt_messages(
            prompt_row=prompt_row,
            capability_prompt=capability_prompt,
            task_instruction=task_instruction,
        )
        prompt_text = _render_prompt_text(tokenizer=tokenizer, messages=prompt_messages)
        prompt_tokens = tokenizer.encode(prompt_text, add_special_tokens=True)
        prompt_input = tinker.types.ModelInput.from_ints(tokens=prompt_tokens)
        sampling_params = tinker.types.SamplingParams(
            max_tokens=config.max_new_tokens,
            temperature=0.0,
            stop=config.stop or None,
        )
        try:
            sample_response = sampling_client.sample(
                prompt=prompt_input,
                sampling_params=sampling_params,
                num_samples=1,
            ).result()
        except Exception:
            # Eval is advisory — a Tinker hiccup mid-step shouldn't kill the
            # training run. Skip this prompt and keep going.
            continue
        if not getattr(sample_response, "sequences", None):
            continue
        completion_text = tokenizer.decode(
            list(sample_response.sequences[0].tokens)
        ).strip()
        result = reward_registry.evaluate(
            reward_recipe=reward_recipe,
            completion=completion_text,
            prompt_row=_build_reward_prompt_row(prompt_row),
            task=reward_task,
        )
        rewards.append(result.reward)
        if result.metrics.get("reward/extraction_failed"):
            extraction_failed_count += 1

    if not rewards:
        return

    metrics: dict[str, float] = {
        "reward": sum(rewards) / len(rewards),
        "reward_max": max(rewards),
        "reward_min": min(rewards),
        "extraction_failed_rate": extraction_failed_count / len(rewards),
    }
    callback.on_evaluation(state=None, metrics=metrics, step=step)


def _build_reward_prompt_row(prompt_row: RLPromptRow) -> RewardPromptRow:
    return RewardPromptRow(
        expected_output=prompt_row.expected_output,
        reward=prompt_row.reward,
        metadata=dict(prompt_row.metadata),
        template_context=dict(prompt_row.template_context),
    )


def _build_reward_task_definition(
    task: TrainingTaskPayload | None,
) -> RewardTaskDefinition | None:
    if task is None:
        return None
    verification = dict(task.verification) if isinstance(task.verification, dict) else None
    return RewardTaskDefinition(reference=task.reference, verification=verification)


def _build_tinker_rl_config(payload: TinkerRLJobPayload) -> TinkerRLConfig:
    """Build a Tinker RL config from a sandbox job payload."""

    config = dict(payload.config)
    return TinkerRLConfig(
        base_model=payload.model,
        algorithm=_get_rl_algorithm(payload.algorithm),
        lora_rank=_get_positive_int(config, "lora_rank", default=16),
        steps=_get_positive_int(config, "steps", default=1),
        num_rollouts=_get_positive_int(config, "num_rollouts", default=8),
        batch_size=_get_positive_int(
            config,
            "batch_size",
            default=min(_get_positive_int(config, "num_rollouts", default=8), 8),
        ),
        learning_rate=_get_positive_float(config, "learning_rate", default=1e-4),
        weight_sync_interval=_get_positive_int(
            config,
            "weight_sync_interval",
            default=1,
        ),
        checkpoint_interval=_get_positive_int(
            config,
            "checkpoint_interval",
            default=max(_get_positive_int(config, "steps", default=1), 1),
        ),
        max_new_tokens=_get_positive_int(config, "max_new_tokens", default=128),
        temperature=_get_non_negative_float(config, "temperature", default=0.0),
        stop=_get_string_list(config, "stop"),
        execution_mode=config.get("execution_mode", "sync"),
        max_steps_off_policy=_get_positive_int(
            config,
            "max_steps_off_policy",
            default=1,
        ),
    )


def _build_sampling_params(*, tinker: Any, params: GenerateParams) -> Any:
    return tinker.types.SamplingParams(
        max_tokens=params.max_tokens or 128,
        temperature=float(params.temperature or 0.0),
        stop=params.stop or None,
    )


def _extract_first_sequence(sample_response: Any) -> Any:
    sequences = getattr(sample_response, "sequences", None)
    if not isinstance(sequences, list) or not sequences:
        raise RuntimeError("Tinker sampling response did not contain any sequences")
    return sequences[0]


def _stop_reason_from_sampling_response(
    sample_response: Any,
) -> Literal["stop", "length", "content_filter", "tool_calls", "unknown"]:
    finish_reason = getattr(sample_response, "finish_reason", None)
    if finish_reason in {
        "stop",
        "length",
        "content_filter",
        "tool_calls",
        "unknown",
    }:
        return finish_reason
    return "unknown"


def _get_rl_algorithm(
    value: str | None,
) -> Literal["importance_sampling", "ppo"]:
    if value == "ppo":
        return "ppo"
    return "importance_sampling"


def _build_worlds_agent_system_prompt(
    capability_prompt: str | None,
) -> str:
    if capability_prompt and capability_prompt.strip():
        return f"{capability_prompt.strip()}\n\n{_WORLDS_AGENT_SYSTEM_PROMPT}"
    return _WORLDS_AGENT_SYSTEM_PROMPT


def _terminal_signal_value(signals: list[dict[str, Any]]) -> float:
    total = 0.0
    for signal in signals:
        value = signal.get("value")
        if isinstance(value, int | float):
            total += float(value)
    return total


def _turn_reward_to_go(
    turns: list[dict[str, Any]],
    *,
    terminal_signals: list[dict[str, Any]],
) -> list[float]:
    """Per-turn cumulative reward-to-go for a rollout.

    Generic: reads ``turn["reward"]`` (float, defaulting to 0) and folds the
    aggregated terminal-signal value onto the last turn. No Worlds-specific
    namespaces; consumed by every recipe that builds Tinker datums from an
    agent rollout.
    """

    rewards: list[float] = []
    for turn in turns:
        value = turn.get("reward")
        rewards.append(float(value) if isinstance(value, int | float) else 0.0)
    if rewards:
        rewards[-1] += _terminal_signal_value(terminal_signals)
    reward_to_go = [0.0] * len(rewards)
    running = 0.0
    for index in range(len(rewards) - 1, -1, -1):
        running += rewards[index]
        reward_to_go[index] = running
    return reward_to_go


# Back-compat alias — kept so anything outside this module referring to the
# old name still resolves. Prefer ``_turn_reward_to_go`` for new callers.
_build_worlds_turn_reward_to_go = _turn_reward_to_go


def _trajectory_to_tinker_datums(
    *,
    rollout_result: Any,
    tokenizer: Any,
    tinker: Any,
    sampling_client: Any,
) -> tuple[list[Any], float]:
    """Convert a :class:`RolloutResult` into Tinker per-turn training datums.

    Consumes the ``message_log`` + ``metadata.turns`` + ``metadata.terminal_signals``
    shape produced by both :class:`AgentRolloutRecorder` (env-agent rollouts)
    and :class:`WorldsEpisodeRecorder` (Worlds RL rollouts). No reward-shaper
    coupling — all shaping is already baked into ``turn["reward"]`` +
    ``terminal_signals[*]["value"]`` by the recorder.

    Returns ``(datums, final_reward)``.
    """
    message_log = rollout_result.message_log
    metadata = rollout_result.metadata if isinstance(rollout_result.metadata, dict) else {}
    raw_turns = metadata.get("turns")
    terminal_signals = metadata.get("terminal_signals")
    if not isinstance(raw_turns, list):
        raw_turns = []
    if not isinstance(terminal_signals, list):
        terminal_signals = []
    reward_to_go = _turn_reward_to_go(
        [turn for turn in raw_turns if isinstance(turn, dict)],
        terminal_signals=[signal for signal in terminal_signals if isinstance(signal, dict)],
    )

    datums: list[Any] = []
    assistant_turn_index = 0
    for message_index, message in enumerate(message_log):
        if message.get("role") != "assistant":
            continue
        if assistant_turn_index >= len(raw_turns):
            break
        turn = raw_turns[assistant_turn_index]
        assistant_turn_index += 1
        if not isinstance(turn, dict):
            continue
        target_text = (
            turn.get("raw_generated_text") or turn.get("generated_text") or message.get("content")
        )
        if not isinstance(target_text, str) or not target_text.strip():
            continue
        prefix_messages = message_log[:message_index]
        prompt_text = _render_prompt_text(
            tokenizer=tokenizer,
            messages=[dict(prefix_message) for prefix_message in prefix_messages],
        )
        prompt_tokens = tokenizer.encode(prompt_text, add_special_tokens=True)
        target_tokens = tokenizer.encode(target_text, add_special_tokens=False)
        full_tokens = prompt_tokens + target_tokens
        if len(full_tokens) < 2:
            continue
        logprob_response = sampling_client.compute_logprobs(
            prompt=tinker.types.ModelInput.from_ints(tokens=full_tokens)
        ).result()
        target_logprobs = _extract_target_logprobs(
            logprob_response=logprob_response,
            target_length=len(full_tokens) - 1,
        )
        reward = reward_to_go[min(assistant_turn_index - 1, len(reward_to_go) - 1)]
        datums.append(
            _build_rl_datum(
                tinker=tinker,
                full_tokens=full_tokens,
                prompt_token_count=len(prompt_tokens),
                reward=reward,
                target_logprobs=target_logprobs,
            )
        )
    return datums, float(getattr(rollout_result, "final_reward", 0.0))


# Back-compat alias for the pre-refactor name. Kept so anything outside this
# module referring to the old name still resolves. Prefer
# ``_trajectory_to_tinker_datums`` for new callers.
_iter_worlds_rollout_datums = _trajectory_to_tinker_datums


async def _run_worlds_rollout(
    *,
    sampling_client: Any,
    tokenizer: Any,
    payload: TinkerRLJobPayload,
    reward_policy: dict[str, Any] | None,
    rollout_index: int,
) -> Any:
    if payload.world is None:
        raise ValueError("Live Worlds rollouts require a resolved world target")
    generator = _TinkerSamplingGenerator(
        model=payload.model,
        params=GenerateParams(),
        sampling_client=sampling_client,
        tokenizer=tokenizer,
    )
    reward_shaper = build_worlds_reward_shaper_from_config(reward_policy)
    goal = _get_optional_string(payload.config, "world_goal") or "Domain Admins"
    metadata = {
        "world_manifest_id": payload.world.id if payload.world is not None else None,
        "rollout_index": rollout_index,
    }
    async with _WorldsHTTPToolset(
        server_url=payload.world.server_url,
        auth_token=payload.world.auth_token,
    ) as toolset:
        agent = Agent(
            name="worlds-training-agent",
            model=generator,
            instructions=_build_worlds_agent_system_prompt(payload.capability.entry_prompt),
            tools=[toolset, finish_task, give_up_on_task],
            tool_mode="json-in-xml",
            max_steps=_get_positive_int(payload.config, "max_turns", default=8),
        )
        return await run_worlds_agent_rollout(
            agent,
            goal,
            reward_shaper=reward_shaper,
            metadata=metadata,
        )


def _generate_worlds_tinker_rl_rollout_group(
    *,
    sampling_client: Any,
    tokenizer: Any,
    generation_step: int,
    model_version: int,
    scheduled_at_training_step: int,
    config: TinkerRLConfig,
    payload: TinkerRLJobPayload,
    tinker: Any,
) -> TinkerRLRolloutGroup:
    datums: list[Any] = []
    rollout_rewards: list[float] = []
    world_reward = payload.config.get("world_reward")
    reward_policy = world_reward if isinstance(world_reward, dict) else None
    target_rollouts = max(1, min(config.num_rollouts, config.batch_size))
    for rollout_index in range(target_rollouts):
        rollout_result = asyncio.run(
            _run_worlds_rollout(
                sampling_client=sampling_client,
                tokenizer=tokenizer,
                payload=payload,
                reward_policy=reward_policy,
                rollout_index=rollout_index,
            )
        )
        rollout_datums, final_reward = _trajectory_to_tinker_datums(
            rollout_result=rollout_result,
            tokenizer=tokenizer,
            tinker=tinker,
            sampling_client=sampling_client,
        )
        if rollout_datums:
            datums.extend(rollout_datums)
            rollout_rewards.append(final_reward)
    return TinkerRLRolloutGroup(
        generation_step=generation_step,
        model_version=model_version,
        scheduled_at_training_step=scheduled_at_training_step,
        datums=datums,
        rewards=rollout_rewards,
    )


def _generate_tinker_rl_rollout_group(
    *,
    sampling_client: Any,
    tokenizer: Any,
    generation_step: int,
    model_version: int,
    scheduled_at_training_step: int,
    config: TinkerRLConfig,
    prompt_rows: list[RLPromptRow],
    capability_prompt: str | None,
    task: TrainingTaskPayload | None,
    reward_recipe: dict[str, Any] | None,
    reward_registry: RewardRecipeRegistry,
    reward_task: RewardTaskDefinition | None,
    tinker: Any,
) -> TinkerRLRolloutGroup:
    """Generate one prompt-group worth of RL datums and rewards."""

    batch_rows = _select_prompt_batch(
        prompt_rows=prompt_rows,
        step=generation_step,
        batch_size=config.batch_size,
    )
    datums: list[Any] = []
    step_rewards: list[float] = []

    for prompt_row in batch_rows:
        task_instruction = _render_task_instruction(
            prompt_row=prompt_row,
            task=task,
        )
        prompt_messages = _build_prompt_messages(
            prompt_row=prompt_row,
            capability_prompt=capability_prompt,
            task_instruction=task_instruction,
        )
        prompt_text = _render_prompt_text(
            tokenizer=tokenizer,
            messages=prompt_messages,
        )
        prompt_tokens = tokenizer.encode(prompt_text, add_special_tokens=True)
        prompt_input = tinker.types.ModelInput.from_ints(tokens=prompt_tokens)
        sampling_params = tinker.types.SamplingParams(
            max_tokens=config.max_new_tokens,
            temperature=config.temperature,
            stop=config.stop or None,
        )
        sample_response = sampling_client.sample(
            prompt=prompt_input,
            sampling_params=sampling_params,
            num_samples=1,
        ).result()
        if not getattr(sample_response, "sequences", None):
            continue

        sequence = sample_response.sequences[0]
        completion_tokens = list(sequence.tokens)
        completion_text = tokenizer.decode(completion_tokens).strip()
        reward_result = reward_registry.evaluate(
            reward_recipe=reward_recipe,
            completion=completion_text,
            prompt_row=_build_reward_prompt_row(prompt_row),
            task=reward_task,
        )
        reward = reward_result.reward
        step_rewards.append(reward)

        full_tokens = prompt_tokens + completion_tokens
        if len(full_tokens) < 2:
            continue
        logprob_response = sampling_client.compute_logprobs(
            prompt=tinker.types.ModelInput.from_ints(tokens=full_tokens)
        ).result()
        target_logprobs = _extract_target_logprobs(
            logprob_response=logprob_response,
            target_length=len(full_tokens) - 1,
        )
        datums.append(
            _build_rl_datum(
                tinker=tinker,
                full_tokens=full_tokens,
                prompt_token_count=len(prompt_tokens),
                reward=reward,
                target_logprobs=target_logprobs,
            )
        )

    return TinkerRLRolloutGroup(
        generation_step=generation_step,
        model_version=model_version,
        scheduled_at_training_step=scheduled_at_training_step,
        datums=datums,
        rewards=step_rewards,
    )


def _build_sandbox_api_client() -> Any:
    """Construct an ApiClient inside the training sandbox from injected env vars.

    The ``DREADNODE_*`` env vars are populated by
    ``SandboxService.create_training_sandbox`` → ``build_sdk_env_vars``. The
    minted key is scoped to ``TRAINING_AGENT_ALLOWED_SCOPES`` which includes
    ``environments:read/write/execute`` — enough for the orchestration below.
    """

    from dreadnode.app.api.client import ApiClient

    return ApiClient(
        os.environ["DREADNODE_SERVER"],
        api_key=os.environ["DREADNODE_API_KEY"],
        default_org=os.environ.get("DREADNODE_ORGANIZATION"),
    )


def _load_capability_for_training(
    dn: Dreadnode, payload: TrainingCapabilityPayload
) -> Any:
    """Pull the capability OCI artifact and load it as a ``Capability`` object.

    Mirrors the optimization path's capability loader (``optimization/jobs.py``)
    but written locally so training doesn't import from ``app.optimization.*``.
    Tries the sandbox-scoped OCI name first, then the payload name — OCI
    artifacts are org-scoped and the payload's name may carry a different org
    prefix than the sandbox user's org.

    Returns a :class:`Capability` instance whose ``.tools`` / ``.agents`` are
    ready to feed into ``create_agent()``.
    """

    from dreadnode.capabilities.capability import Capability

    bare_name = payload.name.rsplit("/", 1)[-1]
    sandbox_org = getattr(dn, "organization", None)
    oci_names: list[str] = []
    if isinstance(sandbox_org, str) and sandbox_org:
        oci_names.append(f"{sandbox_org}/{bare_name}")
    if payload.name not in oci_names:
        oci_names.append(payload.name)

    pull_errors: list[str] = []
    for oci_name in oci_names:
        pull_result = dn.pull_package(
            [f"capability://{oci_name}:{payload.version}"]
        )
        if pull_result.success:
            break
        pull_errors.extend(pull_result.errors or [])
    else:
        raise RuntimeError(
            f"Unable to pull capability {payload.name}:{payload.version} — "
            + "; ".join(pull_errors or ["unknown OCI error"])
        )

    capability_refs: list[Any] = []
    pull_config = getattr(pull_result, "config", None)
    if isinstance(pull_config, dict):
        capability_manifest = pull_config.get("capability_manifest")
        if isinstance(capability_manifest, dict):
            manifest_name = capability_manifest.get("name")
            if isinstance(manifest_name, str) and manifest_name:
                capability_refs.append(manifest_name)
    for candidate in (
        getattr(pull_result, "dest", None),
        bare_name,
        payload.name,
    ):
        if candidate is not None and candidate not in capability_refs:
            capability_refs.append(candidate)

    last_error: Exception | None = None
    for ref in capability_refs:
        try:
            return Capability(ref, storage=dn.storage)
        except FileNotFoundError as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    raise FileNotFoundError(
        f"Capability not found after pull: {payload.name}:{payload.version}; "
        f"tried refs {capability_refs}"
    )


def _prompt_row_env_inputs(row: RLPromptRow) -> dict[str, Any] | None:
    """Pull per-rollout ``TaskEnvironment`` inputs from a prompt row.

    Mirrors GEPA's ``CapabilityEnvAdapter`` convention
    (``optimization/adapters/env.py:40-46``) — dataset rows carrying
    ``row["inputs"]`` have their inputs threaded into env provisioning for
    template substitution. Missing / malformed → ``None`` → env falls back to
    task defaults.

    We peek into ``metadata`` first (more specific) then fall back to the row
    body so dataset authors can attach inputs either way.
    """

    metadata = getattr(row, "metadata", None)
    if isinstance(metadata, dict):
        inputs = metadata.get("env_inputs") or metadata.get("inputs")
        if isinstance(inputs, dict):
            return dict(inputs)
    row_inputs = getattr(row, "inputs", None)
    return dict(row_inputs) if isinstance(row_inputs, dict) else None


def _select_env_recipe_name(reward_recipe: dict[str, Any] | None) -> str | None:
    """Return the env-backed recipe name if ``reward_recipe`` names one.

    Keeps dispatch logic in one place; returns ``None`` for every non-env
    recipe (including ``None`` input) so callers can keep the existing flow.
    """

    if not isinstance(reward_recipe, dict):
        return None
    name = reward_recipe.get("name")
    if not isinstance(name, str):
        return None
    if name in {"task_env_verifier_v1", "task_env_agent_v1"}:
        return name
    return None


def _env_recipe_params(reward_recipe: dict[str, Any] | None) -> dict[str, Any]:
    if isinstance(reward_recipe, dict):
        params = reward_recipe.get("params")
        if isinstance(params, dict):
            return dict(params)
    return {}


def _generate_env_single_shot_rollout_group(
    *,
    sampling_client: Any,
    tokenizer: Any,
    generation_step: int,
    model_version: int,
    scheduled_at_training_step: int,
    config: TinkerRLConfig,
    prompt_rows: list[RLPromptRow],
    capability_prompt: str | None,
    task: TrainingTaskPayload,
    reward_recipe_params: dict[str, Any],
    tinker: Any,
) -> TinkerRLRolloutGroup:
    """Single-shot env-backed rollout group (``task_env_verifier_v1``).

    For each prompt in the step batch: provision a :class:`TaskEnvironment`,
    render the task instruction, sample one completion from the policy,
    verify against the env using the task's ``verification`` config, build
    one Tinker datum. No agent, no tool loop.
    """

    from dreadnode.core import TaskEnvironment
    from dreadnode.training.env_rollouts import (
        batched_environments,
        verify_env_state,
    )

    if task is None:
        raise ValueError("task_env_verifier_v1 requires a task_ref on the RL job")
    if not prompt_rows:
        raise ValueError("task_env_verifier_v1 requires a prompt dataset")

    batch_rows = _select_prompt_batch(
        prompt_rows=prompt_rows,
        step=generation_step,
        batch_size=config.batch_size,
    )
    if not batch_rows:
        return TinkerRLRolloutGroup(
            generation_step=generation_step,
            model_version=model_version,
            scheduled_at_training_step=scheduled_at_training_step,
            datums=[],
            rewards=[],
        )

    max_concurrent = int(reward_recipe_params.get("max_concurrent_rollouts", 8))
    env_timeout_sec = int(reward_recipe_params.get("env_timeout_sec", 300))
    reward_if_true = float(reward_recipe_params.get("reward_if_true", 1.0))
    reward_if_false = float(reward_recipe_params.get("reward_if_false", 0.0))

    api_client = _build_sandbox_api_client()
    org = os.environ["DREADNODE_ORGANIZATION"]
    workspace = os.environ["DREADNODE_WORKSPACE"]

    envs = [
        TaskEnvironment(
            api_client=api_client,
            org=org,
            workspace=workspace,
            task_ref=task.reference,
            inputs=_prompt_row_env_inputs(row),
            timeout_sec=env_timeout_sec,
        )
        for row in batch_rows
    ]

    async def _run() -> tuple[list[Any], list[float]]:
        datums: list[Any] = []
        rewards: list[float] = []
        async with batched_environments(
            envs, max_concurrent_setup=max_concurrent
        ) as live_envs:
            for env, prompt_row in zip(envs, batch_rows, strict=True):
                if env not in live_envs:
                    # Setup failed — skip, don't try to grade.
                    continue
                goal = env.render_instruction() or _render_task_instruction(
                    prompt_row=prompt_row, task=task
                )
                messages = _build_prompt_messages(
                    prompt_row=prompt_row,
                    capability_prompt=capability_prompt,
                    task_instruction=goal,
                )
                prompt_text = _render_prompt_text(
                    tokenizer=tokenizer, messages=messages
                )
                prompt_tokens = tokenizer.encode(prompt_text, add_special_tokens=True)
                sample_response = sampling_client.sample(
                    prompt=tinker.types.ModelInput.from_ints(tokens=prompt_tokens),
                    sampling_params=tinker.types.SamplingParams(
                        max_tokens=config.max_new_tokens,
                        temperature=config.temperature,
                        stop=config.stop or None,
                    ),
                    num_samples=1,
                ).result()
                if not getattr(sample_response, "sequences", None):
                    continue
                sequence = sample_response.sequences[0]
                completion_tokens = list(sequence.tokens)

                verification = env.task_verification or (task.verification or None)
                try:
                    result = await verify_env_state(
                        env,
                        trajectory=None,
                        verification=verification,
                    )
                except ValueError as exc:
                    logger.warning(
                        "Verification misconfigured for env rollout (env_id={}): {}",
                        env.id,
                        exc,
                    )
                    continue

                reward = reward_if_true if result.passed else reward_if_false
                rewards.append(reward)

                full_tokens = prompt_tokens + completion_tokens
                if len(full_tokens) < 2:
                    continue
                logprob_response = sampling_client.compute_logprobs(
                    prompt=tinker.types.ModelInput.from_ints(tokens=full_tokens)
                ).result()
                target_logprobs = _extract_target_logprobs(
                    logprob_response=logprob_response,
                    target_length=len(full_tokens) - 1,
                )
                datums.append(
                    _build_rl_datum(
                        tinker=tinker,
                        full_tokens=full_tokens,
                        prompt_token_count=len(prompt_tokens),
                        reward=reward,
                        target_logprobs=target_logprobs,
                    )
                )
        return datums, rewards

    datums, rewards = asyncio.run(_run())
    return TinkerRLRolloutGroup(
        generation_step=generation_step,
        model_version=model_version,
        scheduled_at_training_step=scheduled_at_training_step,
        datums=datums,
        rewards=rewards,
    )


def _generate_env_agent_rollout_group(
    *,
    sampling_client: Any,
    tokenizer: Any,
    generation_step: int,
    model_version: int,
    scheduled_at_training_step: int,
    config: TinkerRLConfig,
    prompt_rows: list[RLPromptRow],
    capability_prompt: str | None,  # unused; we pull the capability directly  # noqa: ARG001
    task: TrainingTaskPayload,
    reward_recipe_params: dict[str, Any],
    tinker: Any,
    capability_payload: TrainingCapabilityPayload,
    dn: Dreadnode,
) -> TinkerRLRolloutGroup:
    """Multi-turn capability-driven env rollout (``task_env_agent_v1``).

    For each prompt row: provision :class:`TaskEnvironment`, render the
    instruction, run an in-process :class:`Agent` built from the job's
    capability with the Tinker sampling client as its LLM, verify the
    env state (via env_flag / env_script / llm_judge), and convert the
    run into Tinker datums using the same per-turn reward-to-go builder
    the Worlds RL path uses.

    The capability is pulled and loaded once per step (reused across
    rollouts) via the same OCI path that optimization uses — no
    ``app.optimization.*`` import; shared upstream only.
    """

    from dreadnode.app.server.app import create_agent
    from dreadnode.core import TaskEnvironment
    from dreadnode.training.env_rollouts import (
        batched_environments,
        verify_env_state,
    )
    from dreadnode.training.rollouts.agent_rollout import run_agent_rollout

    if task is None:
        raise ValueError("task_env_agent_v1 requires a task_ref on the RL job")
    if not prompt_rows:
        raise ValueError("task_env_agent_v1 requires a prompt dataset")

    batch_rows = _select_prompt_batch(
        prompt_rows=prompt_rows,
        step=generation_step,
        batch_size=config.batch_size,
    )
    if not batch_rows:
        return TinkerRLRolloutGroup(
            generation_step=generation_step,
            model_version=model_version,
            scheduled_at_training_step=scheduled_at_training_step,
            datums=[],
            rewards=[],
        )

    max_turns = int(reward_recipe_params.get("max_turns", 20))
    max_concurrent = int(reward_recipe_params.get("max_concurrent_rollouts", 8))
    env_timeout_sec = int(reward_recipe_params.get("env_timeout_sec", 600))
    reward_if_true = float(reward_recipe_params.get("reward_if_true", 1.0))
    reward_if_false = float(reward_recipe_params.get("reward_if_false", 0.0))

    api_client = _build_sandbox_api_client()
    org = os.environ["DREADNODE_ORGANIZATION"]
    workspace = os.environ["DREADNODE_WORKSPACE"]

    # Pull and load the capability once per step. Capabilities are
    # immutable OCI artifacts, so this is safe to reuse across the step's
    # rollouts. Fresh ``create_agent`` call per rollout gives each agent
    # a clean tool state.
    capability = _load_capability_for_training(dn, capability_payload)
    if not capability.agents:
        raise ValueError(
            f"Capability {capability_payload.name!r} does not expose any "
            "agents — cannot run env-backed RL rollouts against it"
        )
    agent_def = capability.agents[0]

    envs = [
        TaskEnvironment(
            api_client=api_client,
            org=org,
            workspace=workspace,
            task_ref=task.reference,
            inputs=_prompt_row_env_inputs(row),
            timeout_sec=env_timeout_sec,
        )
        for row in batch_rows
    ]

    generator = _TinkerSamplingGenerator(
        model=os.environ.get("DREADNODE_TRAINING_POLICY_MODEL", "policy"),
        params=GenerateParams(),
        sampling_client=sampling_client,
        tokenizer=tokenizer,
    )

    async def _run() -> tuple[list[Any], list[float]]:
        datums: list[Any] = []
        rewards: list[float] = []
        async with batched_environments(
            envs, max_concurrent_setup=max_concurrent
        ) as live_envs:
            for env in live_envs:
                goal = env.render_instruction() or ""
                if not goal:
                    logger.warning(
                        "Env {} rendered an empty goal; skipping rollout", env.id
                    )
                    continue

                # Build the agent per rollout so tools + hooks get a
                # fresh slate and a crash on rollout N doesn't bleed
                # state into N+1.
                agent = create_agent(
                    generator,
                    capability=capability,
                    agent_def=agent_def,
                    extra_tools=[*capability.tools, finish_task, give_up_on_task],
                )
                agent.max_steps = max_turns

                try:
                    rollout_result = await run_agent_rollout(
                        agent,
                        goal,
                        metadata={"environment_id": env.id, "task_ref": env.task_ref},
                    )
                except Exception:
                    logger.exception(
                        "Agent rollout crashed for env {}; skipping", env.id
                    )
                    continue

                verification = env.task_verification or (task.verification or None)
                try:
                    verdict = await verify_env_state(
                        env,
                        trajectory=None,  # Env-state methods don't need trajectory
                        verification=verification,
                    )
                except ValueError as exc:
                    logger.warning(
                        "Verification misconfigured for env rollout "
                        "(env_id={}): {}",
                        env.id,
                        exc,
                    )
                    continue

                terminal_reward = reward_if_true if verdict.passed else reward_if_false
                rewards.append(terminal_reward)

                # Inject the terminal reward into rollout metadata so the
                # shared reward-to-go builder picks it up.
                metadata = rollout_result.metadata
                terminal_signals = metadata.get("terminal_signals") or []
                if not isinstance(terminal_signals, list):
                    terminal_signals = []
                terminal_signals = [
                    *terminal_signals,
                    {
                        "source": "task_env_verification",
                        "value": terminal_reward,
                        "method": verdict.metrics.get("method", "unknown"),
                    },
                ]
                metadata["terminal_signals"] = terminal_signals

                rollout_datums, _final_reward = _trajectory_to_tinker_datums(
                    rollout_result=rollout_result,
                    tokenizer=tokenizer,
                    tinker=tinker,
                    sampling_client=sampling_client,
                )
                datums.extend(rollout_datums)

        return datums, rewards

    datums, rewards = asyncio.run(_run())
    return TinkerRLRolloutGroup(
        generation_step=generation_step,
        model_version=model_version,
        scheduled_at_training_step=scheduled_at_training_step,
        datums=datums,
        rewards=rewards,
    )


def run_tinker_sft_job(payload: TinkerSFTJobPayload) -> TrainingJobResult:
    """Execute one hosted Tinker SFT job from a resolved payload."""

    dn = _build_configured_dreadnode()
    pull_packages: list[str] = []
    if payload.dataset is not None:
        pull_packages.append(f"dataset://{payload.dataset.reference.replace('@', ':', 1)}")
    pull_packages.extend(
        f"dataset://{dataset.reference.replace('@', ':', 1)}"
        for dataset in payload.trajectory_datasets
    )
    if payload.eval_dataset is not None:
        pull_packages.append(f"dataset://{payload.eval_dataset.reference.replace('@', ':', 1)}")
    if not pull_packages:
        raise ValueError(
            "Tinker SFT payload did not include any dataset or trajectory dataset references"
        )
    pull_result = dn.pull_package(pull_packages)
    if not pull_result.success:
        raise RuntimeError("; ".join(pull_result.errors) or "Dataset pull failed")

    train_dataset = (
        dn.load_package(f"dataset://{payload.dataset.reference}")
        if payload.dataset is not None
        else None
    )
    trajectory_datasets = [
        dn.load_package(f"dataset://{dataset.reference}") for dataset in payload.trajectory_datasets
    ]
    eval_dataset = (
        dn.load_package(f"dataset://{payload.eval_dataset.reference}")
        if payload.eval_dataset is not None
        else None
    )

    # Collect OpenAI conversations (with tool_calls) from worlds datasets
    openai_conversations: list[OpenAIConversation] = []
    for trajectory_dataset in trajectory_datasets:
        openai_conversations.extend(
            load_conversations_from_worlds_dataset(
                trajectory_dataset,
                system_prompt=payload.capability.entry_prompt,
            )
        )

    # Collect plain SFT conversations from regular datasets. Per-record
    # dispatch: rows with structured tool_calls / tool_call_id (e.g.
    # `dn eval get-transcript` exports) are picked up by the OpenAI loader
    # and routed through the renderer-aware path so the model's native
    # tool-call template is applied at tokenization time. Plain text rows
    # take the existing SFT loader path.
    sft_conversations: list[SFTConversation] = []
    if train_dataset is not None:
        sft_conversations.extend(
            load_sft_conversations_from_dataset(
                train_dataset,
                system_prompt=payload.capability.entry_prompt,
            )
        )
        openai_conversations.extend(
            load_openai_conversations_from_dataset(
                train_dataset,
                system_prompt=payload.capability.entry_prompt,
            )
        )

    if not openai_conversations and not sft_conversations:
        raise ValueError(
            "Training inputs did not produce any usable conversations. "
            "Each dataset row must contain a `messages` list, a Worlds/ATIF "
            "`steps` list with user/agent messages, or a prompt + completion "
            "pair (`prompt`/`input` + `expected_output`/`output`)."
        )

    eval_conversations: list[SFTConversation] = []
    eval_openai_conversations: list[OpenAIConversation] = []
    if eval_dataset is not None:
        eval_conversations = load_sft_conversations_from_dataset(
            eval_dataset,
            system_prompt=payload.capability.entry_prompt,
        )
        eval_openai_conversations = load_openai_conversations_from_dataset(
            eval_dataset,
            system_prompt=payload.capability.entry_prompt,
        )

    config = _build_tinker_sft_config(payload)
    # Only pass callbacks= when the HTTP-push runtime (run_job_by_id) has
    # installed one; the legacy --payload path keeps the older constructor
    # signature intact.
    if _progress_callback_ctx is not None:
        trainer = TinkerSFTTrainer(config, callbacks=[_progress_callback_ctx])
    else:
        trainer = TinkerSFTTrainer(config)

    # Convert worlds trajectories using model-specific renderer
    train_data = load_from_conversations(
        openai_conversations,
        trainer.renderer,
        config.max_sequence_length,
    )

    # Convert plain SFT conversations using legacy path
    if sft_conversations:
        train_data.extend(
            load_from_messages(
                _messages_from_conversations(sft_conversations),
                trainer.tokenizer,
                config.max_sequence_length,
            )
        )

    eval_data = load_from_messages(
        _messages_from_conversations(eval_conversations),
        trainer.tokenizer,
        config.max_sequence_length,
    )
    if eval_openai_conversations:
        eval_data.extend(
            load_from_conversations(
                eval_openai_conversations,
                trainer.renderer,
                config.max_sequence_length,
            )
        )
    state = trainer.train(train_data, eval_data or None, log_to_dreadnode=False)
    eval_loss: float | None = None
    if eval_data:
        eval_loss = trainer.evaluate(
            eval_data,
            step=getattr(state, "total_steps", None) or getattr(state, "step", 0),
            log_to_dreadnode=False,
        )

    return TrainingJobResult(
        status="completed",
        metrics=_build_sft_metrics(
            state=state,
            train_examples=len(train_data),
            gradient_accumulation_steps=config.gradient_accumulation_steps,
            learning_rate=config.learning_rate,
            eval_examples=len(eval_data),
            eval_loss=eval_loss,
        ),
        artifacts={
            "capability": f"{payload.capability.name}@{payload.capability.version}",
            "checkpoints": list(getattr(state, "checkpoints", [])),
            **({"dataset": payload.dataset.reference} if payload.dataset is not None else {}),
            **(
                {
                    "trajectory_datasets": [
                        dataset.reference for dataset in payload.trajectory_datasets
                    ]
                }
                if payload.trajectory_datasets
                else {}
            ),
            **(
                {"eval_dataset": payload.eval_dataset.reference}
                if payload.eval_dataset is not None
                else {}
            ),
        },
    )


def run_tinker_rl_job(payload: TinkerRLJobPayload) -> TrainingJobResult:
    """Execute one hosted Tinker RL job from a resolved payload."""

    dn = _build_configured_dreadnode()
    pull_packages: list[str] = []
    if payload.prompt_dataset is not None:
        pull_packages.append(f"dataset://{payload.prompt_dataset.reference.replace('@', ':', 1)}")
    pull_packages.extend(
        f"dataset://{dataset.reference.replace('@', ':', 1)}"
        for dataset in payload.trajectory_datasets
    )
    if payload.eval_dataset is not None:
        pull_packages.append(
            f"dataset://{payload.eval_dataset.reference.replace('@', ':', 1)}"
        )
    if not pull_packages and payload.world is None:
        raise ValueError(
            "Tinker RL payload did not include prompt datasets, trajectory datasets, or a live Worlds target"
        )
    if pull_packages:
        pull_result = dn.pull_package(pull_packages)
        if not pull_result.success:
            raise RuntimeError("; ".join(pull_result.errors) or "Prompt dataset pull failed")

    prompt_dataset = (
        dn.load_package(f"dataset://{payload.prompt_dataset.reference}")
        if payload.prompt_dataset is not None
        else None
    )
    trajectory_datasets = [
        dn.load_package(f"dataset://{dataset.reference}") for dataset in payload.trajectory_datasets
    ]
    eval_dataset = (
        dn.load_package(f"dataset://{payload.eval_dataset.reference}")
        if payload.eval_dataset is not None
        else None
    )
    tinker = _get_tinker_module()
    rl_config = _build_tinker_rl_config(payload)
    prompt_rows: list[RLPromptRow] = []
    if prompt_dataset is not None:
        prompt_rows.extend(
            load_prompt_rows_from_dataset(
                prompt_dataset,
                split=_get_optional_string(payload.config, "prompt_split"),
                limit=max(rl_config.num_rollouts, rl_config.batch_size),
            )
        )
    for trajectory_dataset in trajectory_datasets:
        prompt_rows.extend(
            load_rl_prompt_rows_from_worlds_dataset(
                trajectory_dataset,
                system_prompt=payload.capability.entry_prompt,
                limit=max(rl_config.num_rollouts, rl_config.batch_size),
            )
        )
    eval_prompt_rows: list[RLPromptRow] = []
    if eval_dataset is not None:
        eval_max_rollouts = payload.eval_max_rollouts or rl_config.batch_size
        eval_prompt_rows.extend(
            load_prompt_rows_from_dataset(
                eval_dataset,
                # Match the eval split's natural shape — gsm8k-test only has
                # ``test``; users with multi-split eval datasets can override.
                split=_get_optional_string(payload.config, "eval_split"),
                limit=eval_max_rollouts,
            )
        )
    if payload.world is None and not prompt_rows:
        raise ValueError("Prompt dataset did not produce any usable prompt rows")

    reward_registry = RewardRecipeRegistry()
    reward_task = _build_reward_task_definition(payload.task)
    reward_recipe = payload.reward_recipe
    if reward_recipe is None and payload.prompt_dataset is None and payload.trajectory_datasets:
        reward_recipe = {"name": "trajectory_imitation_v1"}

    env_recipe_name = _select_env_recipe_name(reward_recipe)
    env_recipe_params = _env_recipe_params(reward_recipe)

    if env_recipe_name is not None:
        if payload.task is None:
            raise ValueError(
                f"{env_recipe_name} requires a task_ref on the RL job"
            )
        if env_recipe_name == "task_env_verifier_v1":
            training_result = train_tinker_rl(
                tinker=tinker,
                config=rl_config,
                job_id=payload.job_id,
                generate_group=lambda **kwargs: _generate_env_single_shot_rollout_group(
                    config=rl_config,
                    prompt_rows=prompt_rows,
                    capability_prompt=payload.capability.entry_prompt,
                    task=payload.task,
                    reward_recipe_params=env_recipe_params,
                    tinker=tinker,
                    **kwargs,
                ),
            )
        else:
            # task_env_agent_v1 — needs the pulled capability + the sandbox
            # ``Dreadnode`` instance to wire capability tool discovery.
            training_result = train_tinker_rl(
                tinker=tinker,
                config=rl_config,
                job_id=payload.job_id,
                generate_group=lambda **kwargs: _generate_env_agent_rollout_group(
                    config=rl_config,
                    prompt_rows=prompt_rows,
                    capability_prompt=payload.capability.entry_prompt,
                    task=payload.task,
                    reward_recipe_params=env_recipe_params,
                    tinker=tinker,
                    capability_payload=payload.capability,
                    dn=dn,
                    **kwargs,
                ),
            )
    elif payload.world is not None:
        training_result = train_tinker_rl(
            tinker=tinker,
            config=rl_config,
            job_id=payload.job_id,
            generate_group=lambda **kwargs: _generate_worlds_tinker_rl_rollout_group(
                config=rl_config,
                payload=payload,
                tinker=tinker,
                **kwargs,
            ),
            callback=_progress_callback_ctx,
        )
    else:
        eval_interval = max(1, payload.eval_interval or 10) if eval_prompt_rows else 0
        eval_max_rollouts = (
            payload.eval_max_rollouts or rl_config.batch_size
            if eval_prompt_rows
            else 0
        )

        def _generate_with_eval(**kwargs: Any) -> TinkerRLRolloutGroup:
            group = _generate_tinker_rl_rollout_group(
                config=rl_config,
                prompt_rows=prompt_rows,
                capability_prompt=payload.capability.entry_prompt,
                task=payload.task,
                reward_recipe=reward_recipe,
                reward_registry=reward_registry,
                reward_task=reward_task,
                tinker=tinker,
                **kwargs,
            )
            # Held-out eval at step boundaries. ``generation_step`` is the
            # 1-indexed step the trainer is about to consume this group for —
            # eval runs *before* the gradient applies, measuring the policy
            # with the current sampling_client (post-(N-1)-updates).
            if eval_prompt_rows and eval_interval > 0:
                generation_step = int(kwargs.get("generation_step", 0))
                if generation_step > 0 and generation_step % eval_interval == 0:
                    _run_rl_eval_pass(
                        sampling_client=kwargs["sampling_client"],
                        tokenizer=kwargs["tokenizer"],
                        eval_prompt_rows=eval_prompt_rows,
                        capability_prompt=payload.capability.entry_prompt,
                        task=payload.task,
                        reward_recipe=reward_recipe,
                        reward_registry=reward_registry,
                        reward_task=reward_task,
                        config=rl_config,
                        tinker=tinker,
                        step=generation_step,
                        callback=_progress_callback_ctx,
                        eval_max_rollouts=eval_max_rollouts,
                    )
            return group

        training_result = train_tinker_rl(
            tinker=tinker,
            config=rl_config,
            job_id=payload.job_id,
            generate_group=_generate_with_eval,
            callback=_progress_callback_ctx,
        )

    return TrainingJobResult(
        status="completed",
        metrics=dict(training_result.metrics),
        artifacts={
            "capability": f"{payload.capability.name}@{payload.capability.version}",
            "execution_mode": rl_config.execution_mode,
            "checkpoints": list(training_result.checkpoints),
            **(
                {"prompt_dataset": payload.prompt_dataset.reference}
                if payload.prompt_dataset is not None
                else {}
            ),
            **(
                {
                    "trajectory_datasets": [
                        dataset.reference for dataset in payload.trajectory_datasets
                    ]
                }
                if payload.trajectory_datasets
                else {}
            ),
            **({"task": payload.task.reference} if payload.task is not None else {}),
            **(
                {
                    "world_manifest_id": payload.world.id,
                    "world_server_url": payload.world.server_url,
                    **(
                        {"world_server_auth_token": payload.world.auth_token}
                        if payload.world.auth_token is not None
                        else {}
                    ),
                }
                if payload.world is not None
                else {}
            ),
        },
    )


def run_training_job(payload: TrainingJobPayload) -> TrainingJobResult:
    """Dispatch a sandbox training payload to the matching SDK runtime."""

    if isinstance(payload, TinkerSFTJobPayload):
        return run_tinker_sft_job(payload)
    if isinstance(payload, TinkerRLJobPayload):
        return run_tinker_rl_job(payload)
    raise ValueError(
        f"Unsupported training payload backend/trainer_type: {payload.backend}/{payload.trainer_type}"
    )


def _run_training_job_with_callback(
    payload: TrainingJobPayload,
    callback: Any,
) -> TrainingJobResult:
    """Dispatch + install a progress-push trainer callback for the SFT path.

    The callback hooks into ``TinkerSFTTrainer``'s per-step / per-eval /
    per-checkpoint notifications to emit step_complete / eval_complete /
    checkpoint_saved events. Module-level ``_progress_callback`` context
    makes it available to the trainer factory inside ``run_tinker_sft_job``
    without changing that function's signature.
    """
    global _progress_callback_ctx
    previous = _progress_callback_ctx
    _progress_callback_ctx = callback
    try:
        return run_training_job(payload)
    finally:
        _progress_callback_ctx = previous


# Module-level context the trainer factory reads to install the progress
# callback. Python is single-threaded per training-run, and the callback is
# set/unset around a single ``asyncio.to_thread`` call in ``run_job_by_id``,
# so a module-level is safe — it's a poor man's contextvar without the
# cross-loop complexity.
_progress_callback_ctx: Any = None


async def _pull_package(dn: Dreadnode, package_ref: str) -> None:
    """Pull a single package by ref, raising on failure.

    Async-safe wrapper around ``dn.pull_package`` (blocking I/O).
    """

    def _pull() -> None:
        result = dn.pull_package([package_ref])
        if not result.success:
            errors = getattr(result, "errors", None) or [f"pull failed: {package_ref}"]
            raise RuntimeError("; ".join(errors))

    await asyncio.to_thread(_pull)


def _read_capability_entry_prompt(
    dn: Dreadnode, *, name: str, version: str
) -> str | None:
    """Locate and read the capability's entry-agent prompt from local storage.

    Mirrors the API's ``MaterializationService.read_capability_entry_prompt``
    lookup: consult the manifest for ``entry_agent``, then read
    ``agents/<entry_agent>.(md|txt)``. Falls back to the first
    ``agents/*.{md,txt}`` file when the manifest doesn't name an entry agent.
    Returns ``None`` if no candidate file exists on disk.
    """
    try:
        raw_manifest = dn.storage.get_manifest("capabilities", name, version)
    except FileNotFoundError:
        return None
    manifest: dict[str, Any]
    try:
        manifest = json.loads(raw_manifest)
    except (json.JSONDecodeError, TypeError):
        return None

    base = dn.storage.package_path("capabilities", name, version)
    entry_agent = manifest.get("entry_agent") if isinstance(manifest, dict) else None

    candidates: list[Path] = []
    if isinstance(entry_agent, str) and entry_agent:
        for suffix in (".md", ".txt"):
            candidate = base / "agents" / f"{entry_agent}{suffix}"
            if candidate.is_file():
                candidates.append(candidate)
    if not candidates:
        agents_dir = base / "agents"
        if agents_dir.is_dir():
            candidates = sorted(
                p for p in agents_dir.iterdir()
                if p.is_file() and p.suffix in (".md", ".txt")
            )

    for path in candidates:
        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue
        # Strip frontmatter like the API does, so downstream prompts don't
        # surface YAML headers as literal system text.
        if content.startswith("---\n"):
            parts = content.split("---", 2)
            if len(parts) == 3:
                content = parts[2].lstrip("\n")
        return content
    return None


def _build_dataset_payload(
    dn: Dreadnode, *, name: str, version: str
) -> TrainingDatasetPayload:
    """Build a ``TrainingDatasetPayload`` from a pulled dataset's manifest."""
    from dreadnode.packaging.manifest import DatasetManifest

    raw_manifest = dn.storage.get_manifest("datasets", name, version)
    manifest = DatasetManifest.model_validate_json(raw_manifest)
    return TrainingDatasetPayload(
        id="",
        reference=f"{name}@{version}",
        name=name,
        version=version,
        format=manifest.format,
        row_count=manifest.row_count,
        splits=manifest.splits,
        artifacts=dict(manifest.artifacts),
        summary=manifest.summary,
    )


async def fetch_and_build_payload(dn: Dreadnode, job_id: str) -> TrainingJobPayload:
    """Assemble a sandbox training payload from a live hosted job row.

    Replacement for the worker's resolver/materialization phase: the sandbox
    receives only the job UUID on argv and pulls its own inputs (capability
    + datasets) via OCI. This mirrors
    ``dreadnode.optimization.jobs.fetch_and_build_payload`` — the payload
    shape stays the legacy one so ``run_training_job`` is unchanged. Phase C
    may collapse the intermediate adapter.

    Phase A scope: SFT only. RL resolution (task / world / reward recipe) is
    materialization-heavy and lands in a follow-up.
    """
    organization = dn.organization
    workspace = dn.workspace
    if not isinstance(organization, str) or not isinstance(workspace, str):
        raise TypeError("Sandbox Dreadnode client is missing org/workspace — cannot fetch job")

    job = await asyncio.to_thread(dn.api.get_training_job, organization, workspace, str(job_id))

    if job.backend != "tinker":
        raise ValueError(f"Unsupported training backend: {job.backend}")
    if job.trainer_type not in {"sft", "rl"}:
        raise ValueError(f"Unsupported trainer_type: {job.trainer_type}")

    def _fully_qualify(ref_name: str) -> str:
        """Prepend the job's org key when the ref doesn't already namespace it.

        Dataset + capability refs in the ``TrainingJobResponse`` carry the
        bare short name (``gsm8k``) — the org prefix (``dreadnode/``) is
        implicit from the job's organization. The OCI registry path, though,
        expects the fully qualified ``<org>/<name>`` form. The worker sandbox's
        ``DREADNODE_ORGANIZATION`` env (= ``dn.organization``) is authoritative.
        """
        if "/" in ref_name:
            return ref_name
        return f"{organization}/{ref_name}"

    capability_name = _fully_qualify(job.capability.name)
    capability_version = job.capability.version
    await _pull_package(dn, f"capability://{capability_name}:{capability_version}")

    class _DatasetRefLike(Protocol):
        name: str
        version: str

    async def _load_dataset_ref(ref: _DatasetRefLike) -> TrainingDatasetPayload:
        full_name = _fully_qualify(ref.name)
        await _pull_package(dn, f"dataset://{full_name}:{ref.version}")
        return await asyncio.to_thread(
            _build_dataset_payload, dn, name=full_name, version=ref.version
        )

    @dataclass(frozen=True)
    class _DatasetRefShim:
        """Typed stand-in for the API ``DatasetRef`` used when we only have
        ``{name, version}`` from a config blob (eval refs, sampled trajectory
        refs) — keeps :func:`_load_dataset_ref` typed without reaching back
        into the API model layer.
        """

        name: str
        version: str

    if job.trainer_type == "sft":
        entry_prompt = _read_capability_entry_prompt(
            dn, name=capability_name, version=capability_version
        )
        capability_payload = TrainingCapabilityPayload(
            id=job.capability.artifact_id or "",
            name=capability_name,
            version=capability_version,
            runtime_digest=job.capability.runtime_digest,
            manifest={},
            file_manifest=[],
            artifact_s3_prefix="",
            entry_prompt=entry_prompt,
        )

        dataset_payload: TrainingDatasetPayload | None = None
        if job.dataset_ref is not None:
            dataset_payload = await _load_dataset_ref(job.dataset_ref)

        trajectory_datasets: list[TrainingDatasetPayload] = []
        for tref in job.trajectory_dataset_refs:
            trajectory_datasets.append(await _load_dataset_ref(tref))

        eval_ref = (job.config or {}).get("eval_dataset_ref")
        eval_dataset_payload: TrainingDatasetPayload | None = None
        if isinstance(eval_ref, dict):
            eval_name = eval_ref.get("name")
            eval_version = eval_ref.get("version")
            if isinstance(eval_name, str) and isinstance(eval_version, str):
                eval_dataset_payload = await _load_dataset_ref(
                    _DatasetRefShim(name=eval_name, version=eval_version)
                )

        return TinkerSFTJobPayload(
            job_id=str(job.id),
            organization_id=str(job.organization_id),
            workspace_id=str(job.workspace_id),
            created_by=str(job.created_by) if getattr(job, "created_by", None) is not None else None,
            name=job.name,
            algorithm=job.algorithm,
            model=job.model,
            project_ref=job.project_ref,
            run_ref=job.run_ref,
            tags=list(job.tags),
            config=dict(job.config or {}),
            capability=capability_payload,
            dataset=dataset_payload,
            trajectory_datasets=trajectory_datasets,
            eval_dataset=eval_dataset_payload,
        )

    # --- RL path ---------------------------------------------------------
    # RL needs bits the SDK can't derive on its own — task metadata,
    # peer-resolved Worlds server URL, pre-sampled trajectory ref — so we
    # fetch them from the dedicated rl-context endpoint.
    rl_context = await asyncio.to_thread(
        dn.api.get_training_job_rl_context,
        organization,
        workspace,
        str(job_id),
    )

    capability_payload = TrainingCapabilityPayload(
        id=job.capability.artifact_id or "",
        name=capability_name,
        version=capability_version,
        runtime_digest=job.capability.runtime_digest,
        manifest={},
        file_manifest=[],
        artifact_s3_prefix="",
        entry_prompt=rl_context.capability_entry_prompt,
    )

    task_payload: TrainingTaskPayload | None = None
    if rl_context.task is not None:
        task_payload = TrainingTaskPayload(
            id=rl_context.task.id,
            reference=rl_context.task.reference,
            name=rl_context.task.name,
            version=rl_context.task.version,
            instruction=rl_context.task.instruction,
            ports=rl_context.task.ports,
            verification=rl_context.task.verification,
            solution=rl_context.task.solution,
            sandbox_provider=rl_context.task.sandbox_provider,
            s3_key=rl_context.task.s3_key,
        )

    world_payload: TrainingWorldPayload | None = None
    if rl_context.world is not None:
        world_payload = TrainingWorldPayload(
            id=rl_context.world.id,
            name=rl_context.world.name,
            manifest_backend_id=rl_context.world.manifest_backend_id,
            server_url=rl_context.world.server_url,
            artifact_refs=dict(rl_context.world.artifact_refs),
            stats=dict(rl_context.world.stats),
        )

    prompt_dataset_payload: TrainingDatasetPayload | None = None
    if job.prompt_dataset_ref is not None:
        prompt_dataset_payload = await _load_dataset_ref(job.prompt_dataset_ref)

    # Eval dataset for periodic held-out scoring during RL training. Pulled
    # via the same OCI path as the training prompt dataset.
    eval_ref = (job.config or {}).get("eval_dataset_ref")
    eval_dataset_payload: TrainingDatasetPayload | None = None
    if isinstance(eval_ref, dict):
        eval_name = eval_ref.get("name")
        eval_version = eval_ref.get("version")
        if isinstance(eval_name, str) and isinstance(eval_version, str):
            eval_dataset_payload = await _load_dataset_ref(
                _DatasetRefShim(name=eval_name, version=eval_version)
            )

    # Merge user-provided trajectory datasets with the worker-pre-sampled one.
    # The sampled ref lands first — matches the legacy worker's behavior of
    # prepending it so the RL trainer sees native-agent demos early.
    trajectory_datasets = []
    if rl_context.sampled_trajectory_dataset_ref:
        # `sampled_trajectory_dataset_ref` is in "name@version" format.
        sampled = rl_context.sampled_trajectory_dataset_ref
        sampled_name, _, sampled_version = sampled.partition("@")
        if sampled_name and sampled_version:
            trajectory_datasets.append(
                await _load_dataset_ref(
                    _DatasetRefShim(name=sampled_name, version=sampled_version)
                )
            )
    for tref in job.trajectory_dataset_refs:
        trajectory_datasets.append(await _load_dataset_ref(tref))

    eval_interval_raw = (job.config or {}).get("eval_interval")
    eval_max_rollouts_raw = (job.config or {}).get("eval_max_rollouts")
    return TinkerRLJobPayload(
        job_id=str(job.id),
        organization_id=str(job.organization_id),
        workspace_id=str(job.workspace_id),
        created_by=str(job.created_by) if getattr(job, "created_by", None) is not None else None,
        name=job.name,
        algorithm=job.algorithm,
        model=job.model,
        project_ref=job.project_ref,
        run_ref=job.run_ref,
        tags=list(job.tags),
        config=dict(job.config or {}),
        capability=capability_payload,
        task=task_payload,
        world=world_payload,
        prompt_dataset=prompt_dataset_payload,
        trajectory_datasets=trajectory_datasets,
        eval_dataset=eval_dataset_payload,
        reward_recipe=rl_context.reward_recipe,
        eval_interval=eval_interval_raw if isinstance(eval_interval_raw, int) else None,
        eval_max_rollouts=eval_max_rollouts_raw if isinstance(eval_max_rollouts_raw, int) else None,
    )


async def run_job_by_id(job_id: str) -> TrainingJobResult:
    """Sandbox entry for HTTP-driven hosted training.

    Pulls the job + capability + datasets itself rather than reading a
    pre-staged payload file. Delegates to the same ``run_training_job``
    dispatcher as the legacy file-IPC path — downstream execution is
    identical. Emits progress events around the run so the API can track
    lifecycle without polling the sandbox:

    - ``training_start`` on entry (advisory, best-effort).
    - ``training_end`` on success, with the final metrics + status as
      artifacts. **Retried** — this is the authoritative close signal.
    - ``training_error`` on any exception, with the error string.
      **Retried** — the controller's ``wait_for_terminal_status`` is the
      fallback if this push is lost, but landing it is still preferable so
      the UI shows a clean failure reason instead of a timeout.
    """

    from dreadnode.app.api.models import TrainingJobProgressUpdateRequest
    from dreadnode.training._progress import (
        ProgressPushCallback,
        push_progress_update,
    )

    dn = _build_configured_dreadnode()
    payload = await fetch_and_build_payload(dn, job_id)

    await push_progress_update(
        dn=dn,
        job_id=job_id,
        request=TrainingJobProgressUpdateRequest(
            event_type="training_start",
            message=f"Training started on {payload.model}",
            data={"trainer_type": payload.trainer_type, "backend": payload.backend},
        ),
    )

    callback = ProgressPushCallback(dn=dn, job_id=job_id)

    def _run_with_callback() -> TrainingJobResult:
        return _run_training_job_with_callback(payload, callback)

    try:
        result = await asyncio.to_thread(_run_with_callback)
    except BaseException as exc:
        await push_progress_update(
            dn=dn,
            job_id=job_id,
            request=TrainingJobProgressUpdateRequest(
                event_type="training_error",
                level="error",
                message=str(exc) or type(exc).__name__,
                error=str(exc) or type(exc).__name__,
            ),
        )
        raise

    if result.status == "completed":
        await push_progress_update(
            dn=dn,
            job_id=job_id,
            request=TrainingJobProgressUpdateRequest(
                event_type="training_end",
                message="Training complete",
                metrics=dict(result.metrics or {}),
                artifacts=dict(result.artifacts or {}),
            ),
        )
    else:
        await push_progress_update(
            dn=dn,
            job_id=job_id,
            request=TrainingJobProgressUpdateRequest(
                event_type="training_error",
                level="error",
                message=result.error or f"Training ended with status={result.status}",
                error=result.error or f"Training ended with status={result.status}",
                metrics=dict(result.metrics or {}),
                artifacts=dict(result.artifacts or {}),
            ),
        )
    return result


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for sandboxed training job execution.

    The sandbox is launched with ``--job-id <uuid>`` and fetches its own
    context over HTTP via :func:`fetch_and_build_payload`, then pushes
    progress + terminal state through ``/training/jobs/{id}/progress``.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--job-id",
        dest="job_id",
        required=True,
        help="Training job UUID — the SDK fetches context over HTTP.",
    )
    args = parser.parse_args(argv)

    try:
        result = asyncio.run(run_job_by_id(args.job_id))
    except (
        FileNotFoundError,
        KeyError,
        NotImplementedError,
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
    ) as exc:  # pragma: no cover - exercised via API orchestration
        # Surface the failure on stderr so the worker's log-tail fallback
        # can report it. Silent exits on a caught exception are miserable
        # to debug — the progress-push ``training_error`` event may also
        # have failed (e.g., if the failure happened before reaching the
        # API call) and stderr is the only remaining signal.
        import sys as _sys
        import traceback as _traceback

        _sys.stderr.write(
            f"[dreadnode.training.jobs] run_job_by_id({args.job_id}) failed:\n"
        )
        _traceback.print_exc()
        _sys.stderr.flush()
        result = TrainingJobResult(status="failed", error=str(exc))
    return 0 if result.status == "completed" else 1


__all__ = [
    "BaseTrainingJobPayload",
    "TinkerRLJobPayload",
    "TinkerSFTJobPayload",
    "TrainingCapabilityPayload",
    "TrainingDatasetPayload",
    "TrainingJobPayload",
    "TrainingJobResult",
    "TrainingTaskPayload",
    "fetch_and_build_payload",
    "main",
    "run_job_by_id",
    "run_tinker_rl_job",
    "run_tinker_sft_job",
    "run_training_job",
]


if __name__ == "__main__":
    raise SystemExit(main())
