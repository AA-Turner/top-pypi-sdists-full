"""Attended entry point. Model/options/access are resolved before motor arming."""

from decimal import Decimal
from uuid import uuid4

from dreamscale_transport.llm import SessionRequest

from dreamscale.config import API_KEY_ENV, LEGACY_API_KEY_ENV, dreamscale_home, env_with_legacy
from dreamscale.config import load_config as account_config
from dreamscale.embodiments import YAM
from dreamscale.hardware.yam_can import discover_can_interfaces, resolve_arms
from dreamscale.hardware.yam_config import DEFAULT_CONFIG_PATH, load_config
from dreamscale.hardware.yam_rig import YamRig
from dreamscale.hardware.yam_runner import check_can
from dreamscale.model_names import resolve_llm_model

from .attended import run_attended_llm
from .client import Gateway
from .yam import YamAdapter, native_adapter, profile


def run_yam_llm(
    *,
    model,
    instruction,
    config_path=None,
    effort="medium",
    speed="standard",
    max_cost=None,
    max_joint_step=0.15,
    max_joint_velocity=1.0,
    input_fn=input,
    print_fn=print,
):
    request = SessionRequest(
        request_id=str(uuid4()),
        model=resolve_llm_model(model),
        profile=profile(),
        instruction=instruction or "",
        effort=effort,
        speed=speed,
        max_cost=Decimal(str(max_cost)) if max_cost is not None else None,
    )
    config = resolve_arms(
        load_config(config_path or DEFAULT_CONFIG_PATH).validate(complete=True)
    )
    native = native_adapter(config)
    account = account_config()
    key = env_with_legacy(API_KEY_ENV, LEGACY_API_KEY_ENV) or account.api_key
    if not key:
        raise ValueError("Run dreamscale login before starting a managed LLM task.")
    # The policy runs' preflight: refuses a bad bus; the CLI keeps its lines in the log.
    check_can(config, print_fn=print_fn, discover_can=discover_can_interfaces)

    def make_adapter(rig):
        adapter = YamAdapter(rig, native, owns_rig=False)
        adapter.bind()
        return adapter

    return run_attended_llm(
        request=request,
        embodiment=YAM,
        make_gateway=lambda: Gateway(account.control_plane_url, key),
        make_rig=lambda: YamRig(
            config, max_joint_step=max_joint_step, max_joint_velocity=max_joint_velocity
        ),
        make_adapter=make_adapter,
        journal_dir=dreamscale_home() / "llm-runs",
        input_fn=input_fn,
        print_fn=print_fn,
    )
