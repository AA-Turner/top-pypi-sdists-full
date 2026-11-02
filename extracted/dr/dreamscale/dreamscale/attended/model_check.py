"""Passive cloud checks for running a model on a robot: no session, no tokens, no motion."""

from __future__ import annotations

import asyncio

import httpx
from dreamscale_transport.llm import MODELS as LLM_MODELS
from dreamscale_transport.llm import SessionRequest

from dreamscale import errors
from dreamscale.config import API_KEY_ENV, LEGACY_API_KEY_ENV, env_with_legacy
from dreamscale.config import load_config as load_auth_config
from dreamscale.control import ControlPlaneClient
from dreamscale.doctor import CheckResult
from dreamscale.model_names import public_model
from dreamscale.policy.config import OptimizationConfig

# Placement probes that must name a provider for the model to have candidates.
_PROBE_OPTIONS = {"perceptron-isaac05-yam": {"provider": "modal"}}


def supported_models(embodiment) -> tuple[str, ...]:
    return (*embodiment.policy_models, *(LLM_MODELS if embodiment.llm_profile else ()))


def local_checks(embodiment, model) -> list[CheckResult]:
    """The SDK can run model on this robot; raises ValueError when it cannot."""
    if model not in supported_models(embodiment):
        raise ValueError(
            f"{public_model(model)} doesn't run on {embodiment.label}. {errors.SEE_MODELS}"
        )
    if model not in LLM_MODELS:
        return []
    profile = embodiment.load(embodiment.llm_profile)()
    SessionRequest(model=model, profile=profile, instruction="Readiness check")
    return [CheckResult(
        "local LLM compatibility", "pass",
        f"{public_model(model)}: medium effort, standard speed and {embodiment.label} tool profile "
        "supported by this SDK",
    )]


async def cloud_checks(
    embodiment, model, *, auth_config=None, control_factory=ControlPlaneClient,
) -> list[CheckResult]:
    """Authentication, and for a policy its placement metadata; never creates a session."""
    is_llm = model in LLM_MODELS
    name = "account authentication" if is_llm else "auth/model access"
    command = f"dreamscale doctor {embodiment.name}"
    auth = auth_config or load_auth_config()
    api_key = env_with_legacy(API_KEY_ENV, LEGACY_API_KEY_ENV) or auth.api_key
    if not api_key:
        results = [CheckResult(name, "fail", "Run dreamscale login.")]
    else:
        control = control_factory(auth.control_plane_url, api_key)
        try:
            async with asyncio.timeout(20):
                await control.status()
                if not is_llm:
                    await control.probe_candidates(
                        model, optimization_config=OptimizationConfig(rtc="auto"),
                        **_PROBE_OPTIONS.get(model, {}),
                    )
            results = [CheckResult(
                name,
                "pass",
                "Saved account or environment API key authenticated; no session created"
                if is_llm else
                f"{public_model(model)}: HTTP status and placement metadata checked; "
                "no session created",
            )]
        except (TimeoutError, httpx.TimeoutException):
            results = [CheckResult(
                name, "fail",
                f"Cloud access timed out. Check the internet connection and rerun {command}.",
            )]
        except Exception as exc:
            results = [CheckResult(name, "fail", str(exc))]
        finally:
            await control.close()
    if is_llm:
        results.append(CheckResult(
            "LLM model admission", "skip",
            f"Organization access and gateway readiness are checked by dreamscale run "
            f"{embodiment.name} --model {public_model(model)} before arming; this passive check "
            "does not verify them.",
        ))
    return results


async def deployment_checks(
    embodiment, ref, runs_on, *, auth_config=None, control_factory=ControlPlaneClient,
) -> list[CheckResult]:
    """Your deployment ``ref`` exists, is ready, and is built on a base ``runs_on(base, ref)``
    accepts for this robot; never creates a session."""
    from dreamscale.checkpoints_cmd import run_base

    name = "deployment"
    command = f"dreamscale doctor {embodiment.name} --model {ref}"
    auth = auth_config or load_auth_config()
    api_key = env_with_legacy(API_KEY_ENV, LEGACY_API_KEY_ENV) or auth.api_key
    if not api_key:
        return [CheckResult(name, "fail", "Run dreamscale login.")]
    control = control_factory(auth.control_plane_url, api_key)
    try:
        async with asyncio.timeout(20):
            row = await control.get_checkpoint(ref)
    except (TimeoutError, httpx.TimeoutException):
        return [CheckResult(
            name, "fail",
            f"Cloud access timed out. Check the internet connection and rerun {command}.",
        )]
    except errors.DreamscaleError as exc:
        return [CheckResult(
            name, "fail",
            f"{ref}: {exc.info.problem}. `dreamscale deployments list` shows yours.",
        )]
    except Exception as exc:
        return [CheckResult(name, "fail", str(exc))]
    finally:
        await control.close()
    status, base = row.get("status"), run_base(row)
    if not base or not runs_on(base, ref):
        return [CheckResult(
            name, "fail",
            f"{ref} is a {public_model(base or row.get('model') or '?')} deployment, which "
            f"doesn't run on {embodiment.label}.",
        )]
    if status == "building":
        return [CheckResult(name, "warn", f"{ref} is still building; run it once it's ready.")]
    if status != "ready":
        return [CheckResult(
            name, "fail",
            f"{ref} is {status}. `dreamscale deployments show {ref}` says why.",
        )]
    return [CheckResult(
        name, "pass",
        f"{ref}: {public_model(base)} deployment, ready; no session created",
    )]
