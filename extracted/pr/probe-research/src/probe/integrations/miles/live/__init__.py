"""Miles' running samples as live samples (front door; DESIGN.md): `LIVE`, this process's tries; the module wraps the
Ray setup hook installs (`wrap_rollout_common`, `wrap_session_tracer`, `install_rid_stamp`, `wrap_rollout_inputs`);
the refusal texts."""

from probe.integrations.miles.live.engines import CURRENT, EngineAborter, RidStamp
from probe.integrations.miles.live.generate import ProbeGenerate, is_live_on, wrap_generate, wrap_rollout_common
from probe.integrations.miles.live.live import (
    AGENT_REFUSAL,
    GENERATE_WATCH_REFUSAL,
    LIVE,
    NOT_STAMPED_REFUSAL,
    LiveRollouts,
    install_rid_stamp,
    wrap_rollout_inputs,
    wrap_session_tracer,
)
from probe.integrations.miles.live.rollout import Rollout
from probe.integrations.miles.live.schedule import RolloutSchedule
from probe.integrations.miles.live.sessions import SessionWatcher, to_turns

__all__ = [
    "AGENT_REFUSAL",
    "CURRENT",
    "GENERATE_WATCH_REFUSAL",
    "LIVE",
    "NOT_STAMPED_REFUSAL",
    "EngineAborter",
    "LiveRollouts",
    "ProbeGenerate",
    "RidStamp",
    "Rollout",
    "RolloutSchedule",
    "SessionWatcher",
    "install_rid_stamp",
    "is_live_on",
    "to_turns",
    "wrap_generate",
    "wrap_rollout_common",
    "wrap_rollout_inputs",
    "wrap_session_tracer",
]
