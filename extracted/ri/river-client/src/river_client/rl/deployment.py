"""Temporary dedicated capacity for checkpoint-pinned evaluation."""

from __future__ import annotations

import asyncio
import json
import math
import time
from contextlib import asynccontextmanager
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from river_client.client import _http_error, _optional_sampling_log_masses
from river_client.types import RiverError, Sample

from .checkpoint import fingerprint
from .config import _integer
from .engine import call
from .evaluation import CheckpointSampler


def _request(client, deployment, route, body=None, *, timeout=30):
    request = Request(
        f"{deployment.base_url.rstrip('/')}/{route}",
        data=None if body is None else json.dumps(body).encode(),
        headers={
            **client._http_authorization_headers(),
            "Content-Type": "application/json",
        },
        method="GET" if body is None else "POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except HTTPError as error:
        with error:
            payload = error.read()
        raise _http_error(error.code, payload, "Evaluation sampling") from None


async def _settle(operation):
    """A cancelled blocking mutation must finish before its resources are freed."""
    task = asyncio.create_task(operation)
    cancelled = False
    while not task.done():
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            cancelled = True
    result = task.result()
    if cancelled:
        raise asyncio.CancelledError
    return result


class EvaluationDeployment:
    """Create and delete dedicated workers for each evaluated checkpoint.

    Supply a River client with dedicated-deployment access and exactly one
    capacity group: ``unified_replicas``, or both prefill/decode replica counts.
    Each checkpoint's variants share its deployment. Queued evaluations do not
    hold workers; ``max_concurrent`` bounds the number of live deployments.
    Full-weight export admission limits still apply.
    """

    def __init__(
        self,
        client,
        *,
        unified_replicas=None,
        prefill_replicas=None,
        decode_replicas=None,
        max_concurrent=1,
        export_timeout=3600,
        startup_timeout=1800,
        evaluation_timeout=3600,
        cleanup_timeout=300,
    ):
        unified = unified_replicas is not None
        pd = prefill_replicas is not None and decode_replicas is not None
        if unified == pd or (
            unified and (prefill_replicas is not None or decode_replicas is not None)
        ):
            raise ValueError(
                "supply unified_replicas or both prefill_replicas and decode_replicas"
            )
        self.counts = {
            name: value
            for name, value in {
                "unified_replicas": unified_replicas,
                "prefill_replicas": prefill_replicas,
                "decode_replicas": decode_replicas,
            }.items()
            if value is not None
        }
        for name, value in self.counts.items():
            _integer(value, name, 1)
        _integer(max_concurrent, "max_concurrent", 1)
        for name, value in {
            "export_timeout": export_timeout,
            "startup_timeout": startup_timeout,
            "evaluation_timeout": evaluation_timeout,
            "cleanup_timeout": cleanup_timeout,
        }.items():
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        self.export_timeout = export_timeout
        self.startup_timeout = startup_timeout
        self.evaluation_timeout = evaluation_timeout
        self.cleanup_timeout = cleanup_timeout
        self.client, self.max_concurrent = client, max_concurrent
        self._slots = asyncio.Semaphore(max_concurrent)

    def config_dict(self):
        return {
            **self.counts,
            "max_concurrent": self.max_concurrent,
            **{
                name: getattr(self, name)
                for name in (
                    "export_timeout",
                    "startup_timeout",
                    "evaluation_timeout",
                    "cleanup_timeout",
                )
            },
        }

    async def _create(self, checkpoint, state):
        key = fingerprint(
            {"checkpoint": checkpoint.path, "attempt": state.get("attempt", 0)}
        )
        state["creating"] = True
        deployment = await call(
            self.client.create_deployment,
            checkpoint,
            **self.counts,
            idempotency_key=f"rl-eval-{key}",
        )
        state["id"] = deployment.id
        state.pop("creating", None)
        return deployment

    async def cleanup(self, checkpoint, state):
        # A lost creation response can still own workers. Replay the same
        # idempotency key to recover their identity before deleting them.
        if state.get("creating") and not state.get("id"):
            await _settle(self._create(checkpoint, state))
        if deployment_id := state.get("id"):

            async def delete():
                await call(
                    self.client.delete_deployment,
                    deployment_id,
                    wait=True,
                    wait_timeout=self.cleanup_timeout,
                    idempotency_key=f"rl-eval-delete-{deployment_id}",
                )
                state.pop("id", None)
                state["attempt"] = state.get("attempt", 0) + 1

            try:
                await _settle(delete())
            except Exception as error:
                raise RiverError(
                    f"failed to delete evaluation deployment {deployment_id}; resume to retry cleanup"
                ) from error

    @asynccontextmanager
    async def open(self, checkpoint, state):
        async with self._slots:
            try:
                # Reuse the same key after ambiguous acceptance or process restart.
                # A previously deleted attempt needs a new key, never a new policy.
                while True:
                    if not state.get("id"):
                        await _settle(self._create(checkpoint, state))
                    current = await call(self.client.get_deployment, state["id"])
                    if current.phase != "deleted":
                        break
                    state.pop("id", None)
                    state["attempt"] = state.get("attempt", 0) + 1
                deadline = time.monotonic() + self.startup_timeout
                while not current.is_serving:
                    if current.phase in ("failed", "deleting", "deleted"):
                        raise RiverError(
                            f"evaluation deployment {current.id} is {current.phase}"
                        )
                    if time.monotonic() >= deadline:
                        raise TimeoutError(
                            f"evaluation deployment {current.id} did not become ready"
                        )
                    await asyncio.sleep(min(1, max(0, deadline - time.monotonic())))
                    current = await call(self.client.get_deployment, state["id"])
                if current.checkpoint != checkpoint.path:
                    raise RiverError(
                        "evaluation deployment is bound to a different checkpoint"
                    )
                capabilities = await call(_request, self.client, current, "models")
                if "checkpoint_sampling_v1" not in capabilities.get("features", []):
                    raise RiverError(
                        "evaluation requires serving capability checkpoint_sampling_v1"
                    )
                yield current
            finally:
                await self.cleanup(checkpoint, state)


class DeploymentSampler(CheckpointSampler):
    """Token-ID sampler wrapper bound to one full-weight checkpoint deployment."""

    submit_sampling_batch = None

    def __init__(self, sampler, client, deployment):
        super().__init__(
            sampler.session,
            base_model=sampler.base_model,
            checkpoint=sampler.checkpoint,
            tokenizer=sampler.tokenizer,
        )
        self.client, self.deployment = client, deployment

    def get_server_capabilities(self):
        # The dedicated endpoint was negotiated before constructing this adapter.
        return None

    async def sample(
        self,
        *,
        model_input=None,
        num_samples=1,
        max_tokens=256,
        temperature=1,
        top_p=1,
        top_k=-1,
        stop=None,
        seeds=None,
        timeout=1800,
        return_prompt_token_ids=False,
        return_sampling_log_mass=False,
        **kwargs,
    ):
        if (
            model_input is None
            or num_samples != 1
            or any(value for value in kwargs.values())
        ):
            raise ValueError(
                "deployment evaluation requires model_input and supports one sample per prompt, without routing or top-logprob capture"
            )
        if seeds is not None and len(seeds) != len(model_input):
            raise ValueError("seeds must match the prompt count")
        bodies = []
        for index, chunks in enumerate(model_input):
            if any(chunk["type"] != "text" for chunk in chunks):
                raise ValueError(
                    "deployment checkpoint evaluation currently supports text inputs"
                )
            bodies.append(
                {
                    "input_ids": [
                        token for chunk in chunks for token in chunk["tokens"]
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "stop": stop or [],
                    "seed": seeds[index] if seeds is not None else None,
                    "return_sampling_log_mass": return_sampling_log_mass,
                }
            )

        async def generate(body):
            result = await call(
                _request, self.client, self.deployment, "sample", body, timeout=timeout
            )
            tokens, logprobs = result["token_ids"], result["token_logprobs"]
            if len(tokens) != len(logprobs) or any(value is None for value in logprobs):
                raise RiverError(
                    "evaluation sampling requires exact token IDs and log probabilities"
                )
            return [
                Sample(
                    text=self.tokenizer.decode(tokens),
                    tokens=tokens,
                    logprobs=logprobs,
                    stop_reason=result["stop_reason"],
                    model_step=self.checkpoint.step,
                    policy_version=self.checkpoint.policy_version,
                    prompt_token_ids=body["input_ids"]
                    if return_prompt_token_ids
                    else None,
                    sampling_log_masses=_optional_sampling_log_masses(
                        result, return_sampling_log_mass
                    ),
                )
            ]

        tasks = [asyncio.create_task(generate(body)) for body in bodies]
        try:
            return await asyncio.gather(*tasks)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
