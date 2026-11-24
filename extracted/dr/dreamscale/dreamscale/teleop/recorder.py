"""Cold-start teleop demo recording session (``dreamscale record <robot>``).

Uses the exact same ``ControlArbiter`` (with ``policy=None``) and Wave 2A's
``CaptureManager`` / ``SpoolEpisode`` pipeline so recorded human demos land in
the exact same LeRobot v3.0 format and cloud dataset ingest path without ever
opening a cloud inference session.
"""

from __future__ import annotations

import asyncio
import contextlib
import signal
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dreamscale.capture import CaptureManager, EpisodeSummary

from .arbiter import ArbiterSummary, ControlArbiter
from .devices import TeleopDevice


@dataclass(frozen=True)
class RecordedEpisodeResult:
    arbiter: ArbiterSummary
    spool: EpisodeSummary


async def record_teleop_episodes(
    *,
    rig: Any,
    teleop: TeleopDevice,
    capture: CaptureManager,
    robot_id: str,
    task: str,
    episodes: int = 1,
    max_actions: int | None = None,
    fps: float = 30.0,
    blend_steps: int = 5,
    max_transition_delta: float | None = None,
    pace: bool = True,
    on_episode_start: Callable[[int], Any] | None = None,
    on_episode_done: Callable[[int, RecordedEpisodeResult], Any] | None = None,
    print_fn: Callable[[str], None] = print,
    install_sigint: bool = False,
) -> list[RecordedEpisodeResult]:
    """Record ``episodes`` cold-start human demonstrations using ``ControlArbiter(policy=None)``."""
    results: list[RecordedEpisodeResult] = []
    active_arbiter: ControlArbiter | None = None
    stop_all = False

    loop = asyncio.get_running_loop()
    old_sigint = None
    if install_sigint:
        def _handle_sigint() -> None:
            nonlocal stop_all
            if active_arbiter is not None:
                active_arbiter.request_stop()
            else:
                stop_all = True

        old_sigint = signal.getsignal(signal.SIGINT)
        with contextlib.suppress(NotImplementedError, ValueError):
            loop.add_signal_handler(signal.SIGINT, _handle_sigint)

    try:
        teleop.open()
        for ep_num in range(1, max(1, int(episodes)) + 1):
            if stop_all:
                break
            if on_episode_start is not None:
                proceed = on_episode_start(ep_num)
                if proceed is False:
                    break
            print_fn(
                f"Episode {ep_num}/{episodes}: recording teleop ({teleop.name}). Ctrl+C stops."
            )
            spool_ep = capture.start_episode(
                task=task,
                fps=fps,
                robot_id=robot_id,
                default_source_kind="teleop",
                metadata={"teleop_device": teleop.name, "teleop_kind": teleop.kind},
            )
            arbiter = ControlArbiter(
                rig=rig,
                teleop=teleop,
                policy=None,
                fps=fps,
                blend_steps=blend_steps,
                max_transition_delta=max_transition_delta,
                spool_episode=spool_ep,
                print_fn=print_fn,
                pace=pace,
            )
            active_arbiter = arbiter
            rig.enable_dispatch()
            aborted = False
            try:
                arbiter_summary = await arbiter.run_episode(
                    instruction=task,
                    max_actions=max_actions,
                )
            except BaseException:
                aborted = True
                raise
            finally:
                active_arbiter = None
                with contextlib.suppress(Exception):
                    rig.block_dispatch()
                with contextlib.suppress(Exception):
                    rig.stop()
                spool_summary = await asyncio.to_thread(
                    capture.finish_episode,
                    spool_ep,
                    outcome="aborted" if aborted else "success",
                )
            rec = RecordedEpisodeResult(arbiter=arbiter_summary, spool=spool_summary)
            results.append(rec)
            if spool_summary.status == "ready":
                print_fn(
                    f"Episode {ep_num} spooled ({spool_summary.frame_count} frames); "
                    "uploading in background."
                )
            else:
                print_fn(
                    f"Episode {ep_num} saved locally ({spool_summary.frame_count} frames): "
                    f"{spool_summary.directory}"
                )
            if on_episode_done is not None:
                on_episode_done(ep_num, rec)
    finally:
        if install_sigint and old_sigint is not None:
            with contextlib.suppress(NotImplementedError, ValueError):
                loop.remove_signal_handler(signal.SIGINT)
                signal.signal(signal.SIGINT, old_sigint)
        with contextlib.suppress(Exception):
            teleop.close()
    return results


def run_robot_record(
    *,
    embodiment_name: str,
    teleop: TeleopDevice,
    task: str,
    dataset_ref: str | None = None,
    record_dir: Path | None = None,
    episodes: int = 1,
    max_actions: int | None = None,
    fps: float = 30.0,
    config_path: Path | None = None,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    rig_factory: Callable[[], Any] | None = None,
) -> list[RecordedEpisodeResult]:
    """Open the robot rig + teleop device + CaptureManager and record demos (no cloud policy)."""
    from dreamscale.config import load_config as load_sdk_config

    sdk_cfg = load_sdk_config()
    capture = CaptureManager(
        spool_root=record_dir,
        dataset_ref=dataset_ref,
        api_url=sdk_cfg.control_plane_url if sdk_cfg.api_key else None,
        api_key=sdk_cfg.api_key,
        keep_local=record_dir is not None,
        print_fn=print_fn,
    )

    if rig_factory is None:
        emb = embodiment_name.strip().lower()
        if emb == "yam":
            from dreamscale.hardware.yam_can import resolve_arms
            from dreamscale.hardware.yam_config import DEFAULT_CONFIG_PATH, load_config
            from dreamscale.hardware.yam_rig import YamRig

            raw_cfg = load_config(config_path or DEFAULT_CONFIG_PATH).validate(complete=True)
            cfg = resolve_arms(raw_cfg)
            rig = YamRig(cfg)
        elif emb == "so101":
            from dreamscale.hardware.so101_rig import So101Rig
            from dreamscale.so101_runner import _default_robot_factory, rig_cameras

            cam_cfg = rig_cameras(_default_robot_factory, "pi0.5")
            rig = So101Rig(
                _default_robot_factory,
                calibration_path=sdk_cfg.calibration_path,
                camera_config=cam_cfg,
                print_fn=print_fn,
            )
        else:
            raise ValueError(
                f"Cold-start teleop recording is currently supported on yam and so101, "
                f"not '{embodiment_name}'."
            )
    else:
        rig = rig_factory()

    print_fn(
        f"Connecting {embodiment_name.upper()} for teleop recording ({teleop.name}). "
        "No cloud inference session will be started."
    )
    rig.open(attended=True)
    try:
        def _prompt_start(ep_num: int) -> bool:
            if ep_num == 1 and episodes == 1:
                return True
            ans = input_fn(
                f"Ready for episode {ep_num}/{episodes} — press Enter to start (q to quit): "
            ).strip().lower()
            return ans not in {"q", "quit", "exit"}

        return asyncio.run(
            record_teleop_episodes(
                rig=rig,
                teleop=teleop,
                capture=capture,
                robot_id=embodiment_name.strip().lower(),
                task=task,
                episodes=episodes,
                max_actions=max_actions,
                fps=fps,
                on_episode_start=_prompt_start if episodes > 1 else None,
                print_fn=print_fn,
                install_sigint=True,
            )
        )
    finally:
        with contextlib.suppress(Exception):
            rig.close()
        capture.close(drain_timeout_s=15.0)
