"""Attended persistent hardware session with short, cancellable cloud tasks.

Robot-neutral: an embodiment descriptor (dreamscale.embodiments) says how to label
and print its actions, and a rig (dreamscale.hardware.rig.Rig) owns its hardware.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import select
import signal
import sys
import uuid
from dataclasses import asdict
from pathlib import Path

from dreamscale.codec_feed import start_camera_feed
from dreamscale.hardware.rig import RigFault
from dreamscale.policy.deployment import (
    follows_session_contract as _follows_deployment_session,
)
from dreamscale.policy.deployment import (
    non_joint_run_error,
    waits_for_each_chunk,
)
from dreamscale.policy.remote import aconnect
from dreamscale.policy.runtime.action_smoothing import resolve_action_smoothing
from dreamscale.policy.runtime.action_space import AbsoluteJointPosition, action_space_for
from dreamscale.policy.runtime.contract import (
    deployment_preview_contract,
    follows_server_contract,
    runtime_contract_for_model,
)
from dreamscale.policy.runtime.rtc import DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID
from dreamscale.policy.types import RunContext, RunStrategy
from dreamscale.region_probe import (
    validate_provider_selection,
    validate_region,
    validate_speed_selection,
)

from .lifecycle import AttendedLifecycle, safe_printer
from .sync import run_sync, validate_mode

RTC_VALUES = ("auto", "on", "off", "inference_time", "train_time")
RTC_VALUES_MESSAGE = "rtc must be auto, on, off, inference_time, or train_time."
# Shown when a π0.5 deployment session runs test-time RTC (dynamic_full_horizon_v1).
TEST_TIME_RTC_NOTE = "RTC: test-time (test-time RTC adds latency)."
# Sync runs each chunk to the end before asking for the next, so chunks never overlap.
SYNC_RTC_NOTE = "RTC: not used in sync mode (each chunk runs to the end)."
# A deployment whose robot waits for each chunk (InternW0-Δ) runs in sync mode, whatever --mode.
WAIT_SYNC_NOTE = "Mode: sync (this deployment waits for each chunk and runs it to the end)."
WAIT_SMOOTHING_MESSAGE = (
    "This deployment runs each chunk to the end (sync), so smoothing options don't apply."
)
WAIT_MODE_MESSAGE = (
    "This deployment waits for each chunk and runs it to the end; run it with --mode sync."
)


def default_mode(model):
    """The mode a run takes when none is asked for: the model's own (its contract's
    ``default_mode``: Praxis-1 runs each chunk to its end, as upstream does), else async."""
    try:
        return model_contract(model).default_mode
    except ValueError:  # a model only its server describes: replanning, as before
        return "async"


def task_mode(model, mode, strategy):
    """The mode a task runs in, checked: sync for a base whose robot waits for each chunk,
    as its sessions require; otherwise the requested one ("auto": the model's own)."""
    if mode == "auto":
        mode = "sync" if waits_for_each_chunk(model) else default_mode(model)
    validate_mode(mode, RunStrategy())
    if not waits_for_each_chunk(model):
        validate_mode(mode, strategy)
        return mode
    try:
        validate_mode("sync", strategy)
    except ValueError:
        raise ValueError(WAIT_SMOOTHING_MESSAGE) from None
    return "sync"


async def _close_quietly(policy):
    """Close a session the runner refuses; the refusal is the error to report."""
    try:
        async with asyncio.timeout(30):
            await policy.close()
    except Exception:  # noqa: BLE001 - the refusal is the error to report
        pass


def follows_session_contract(model):
    """A run whose rate and chunk its session supplies: a robot deployment's, or a model this
    SDK has no contract for (one released after it), which runs its server's (F13)."""
    return _follows_deployment_session(model) or follows_server_contract(model)


def model_contract(model):
    """The model's own runtime contract; before a session opens, a robot deployment's (π0.5,
    ABC-VLA) is joint targets held in place, and the session's contract replaces it."""
    if follows_session_contract(model):
        return deployment_preview_contract()
    return runtime_contract_for_model(model)


def _session_strategy(model, contract, **options):
    """The run strategy: the model's own rate and chunk, or, for a robot deployment, none,
    so the run follows the session's (the rate the deployment was trained at). The chunk is the
    rows an answer may hold, not the rows a robot executes of it (``execution_horizon``): a
    loop runs the executed rows and never queues the rest (DSL-424)."""
    if follows_session_contract(model):
        return RunStrategy(**options)
    return RunStrategy(action_hz=contract.action_hz, chunk_size=contract.chunk_size, **options)


def task_instructions(instruction):
    """None, one stripped instruction, or a list of them: tasks run in turn, then exit."""
    if instruction is None:
        return None
    many = not isinstance(instruction, str)
    items = list(instruction) if many else [instruction]
    if not items or any(not isinstance(i, str) or not i.strip() for i in items):
        raise ValueError("Enter a nonempty task instruction.")
    items = [i.strip() for i in items]
    return items if many else items[0]


def validate_run_options(
    model, *, label, mode, region, provider, speed, keep_warm, rtc, context, max_actions,
    trace_dir, trace_images, action_smoothing="auto", smoothing_new_weight=None,
    smoothing_correction_steps=None, smoothing_reference_speed=None,
):
    """Check every robot-neutral option before any hardware opens; returns the strategy."""
    contract = model_contract(model)
    strategy = _session_strategy(
        model,
        contract,
        action_smoothing=action_smoothing,
        smoothing_new_weight=smoothing_new_weight,
        smoothing_correction_steps=smoothing_correction_steps,
        smoothing_reference_speed=smoothing_reference_speed,
    )
    task_mode(model, mode, strategy)
    if trace_images and trace_dir is None:
        raise ValueError("--trace-images requires --trace-dir")
    validate_provider_selection(model, provider, region)
    # auto, available, or any region id: the control plane checks it (GET /v1/regions).
    validate_region(region)
    validate_speed_selection(model, speed, provider, region)
    if type(keep_warm) is not int or not 0 <= keep_warm <= 3600:
        raise ValueError("keep_warm must be 0–3600 seconds.")
    if rtc not in RTC_VALUES:
        raise ValueError(RTC_VALUES_MESSAGE)
    if context not in {"auto", "on", "off"}:
        raise ValueError("context must be auto, on, or off.")
    if max_actions is not None and (type(max_actions) is not int or not 1 <= max_actions <= 18000):
        raise ValueError("max_actions must be None or 1–18000.")
    return contract, strategy


class AttendedTaskRunner:
    """Hardware remains open until the caller explicitly closes the rig.

    preview obtains predictions without dispatch. execute always starts a new
    cloud task on the retained session and observes again, never replaying a
    previewed chunk. stop() closes an idle retained session too. Callbacks
    can be overridden; custom callbacks must be bounded and cooperate with
    cancellation. The built-in rig callbacks are process bounded.

    end_effector_adapter optionally converts the policy's action space into the
    rig's joints (bind/on_conversion); its caller supplies the matching observe
    and execution_contract.
    """

    def __init__(
        self,
        rig,
        *,
        embodiment,
        model,
        connect=aconnect,
        mode="auto",
        keep_warm=300,
        region="available",
        provider=None,
        speed=None,
        rtc="auto",
        checkpoint=None,
        context="auto",
        observe=None,
        act=None,
        read_hold_action=None,
        end_effector_adapter=None,
        execution_contract=None,
        strategy=None,
        trace_dir=None,
        trace_images=False,
        hud=None,
        recorder=None,
        print_fn=print,
        lifecycle=None,
        while_compute_starts=None,
    ):
        if type(keep_warm) is not int or not 0 <= keep_warm <= 3600:
            raise ValueError("keep_warm must be 0–3600 seconds.")
        self.embodiment = embodiment
        self.model = model
        validate_provider_selection(model, provider, region)
        validate_region(region)
        region = validate_speed_selection(model, speed, provider, region)
        self.region, self.provider, self.speed = region, provider, speed
        if rtc not in RTC_VALUES:
            raise ValueError(RTC_VALUES_MESSAGE)
        # "auto" takes the model's server-side default (on for Isaac 0.5, off elsewhere).
        self.rtc, self.checkpoint = rtc, checkpoint
        if context not in {"auto", "on", "off"}:
            raise ValueError("context must be auto, on, or off.")
        # Observation history (Isaac 0.5): "auto" follows the checkpoint's own window.
        self.context = context
        self.rig, self.connect, self.keep_warm = rig, connect, keep_warm
        self.end_effector_adapter = end_effector_adapter
        self.observe = observe or rig.observe
        contract = execution_contract or model_contract(model)
        self.execution_contract = contract
        # Rigs take absolute joint positions; a model acting in another space (DROID's
        # joint velocities) is converted here, against the measured pose.
        self.action_space = (
            AbsoluteJointPosition() if end_effector_adapter is not None
            else action_space_for(contract)
        )
        rig_act = act or rig.act
        rig_hold = read_hold_action or rig.read_hold_action
        if self.action_space.identity:
            self.act, self.read_hold_action = rig_act, rig_hold
        else:
            space = self.action_space

            def converted_act(action, ctx=None):
                return rig_act(space.to_rig(action, rig.read_hold_action(ctx)), ctx)

            def converted_hold(ctx=None):
                return space.hold(rig_hold(ctx))

            self.act, self.read_hold_action = converted_act, converted_hold
        self.strategy = strategy or (
            RunStrategy() if follows_session_contract(model) else RunStrategy(
                action_hz=contract.action_hz, chunk_size=contract.chunk_size,
            )
        )
        self.mode = task_mode(model, mode, self.strategy)
        resolve_action_smoothing(self.strategy, contract)
        if trace_images and trace_dir is None:
            raise ValueError("trace_images requires trace_dir")
        self.trace_dir, self.trace_images = trace_dir, trace_images
        if hud is not None and recorder is not None:
            raise ValueError("Record on HUD or with another recorder, not both.")
        # A task recorder: HudJob, or anything with its start/finish shape.
        self.hud = recorder if recorder is not None else hud
        # The last executed task's recording, awaiting the operator's grade.
        self.hud_episode = None
        self.print_fn = safe_printer(print_fn)
        self._operation = None
        self._cancel_requested = False
        self._preview_instruction = None
        self._preview_observation = None
        self._policy_progress = None
        self._calibration = None
        self._fresh_compute = False
        self.policy = None
        # Runs while a task's compute starts, cancelled once it's ready (YAM: what the arms
        # a previous run left holding are doing meanwhile, yam_hold.watch_resident_holds).
        self.while_compute_starts = while_compute_starts
        self.lifecycle = lifecycle or AttendedLifecycle(
            rig, print_fn=self.print_fn, arms=_arms_word(embodiment),
        )

    @property
    def active(self):
        return self.lifecycle.homing or (
            self._operation is not None and not self._operation.done()
        )

    def request_stop(self):
        self.lifecycle.request_stop()
        if self._operation is not None and not self._cancel_requested:
            self._cancel_requested = True
            self._operation.cancel()

    async def stop(self):
        self.request_stop()
        await self.lifecycle.wait_for_home()
        if self._operation is not None:
            await asyncio.gather(self._operation, return_exceptions=True)
        self._preview_instruction = None
        try:
            # Stopped before the robot connected (while compute started): nothing to hold.
            holds = self.lifecycle.stop_and_hold() if self.lifecycle.ready else {}
        finally:
            cleanup_error = await self._close_policy()
        if cleanup_error is not None:
            raise cleanup_error
        return holds

    async def _close_policy(self):
        await self._cancel_background_calibration()
        self._fresh_compute = False
        policy, self.policy = self.policy, None
        if policy is None:
            return None
        try:
            async with asyncio.timeout(30):
                await policy.close()
            self.print_fn(
                "Cloud task closed"
                + (f"; reserved for {self.keep_warm}s." if self.keep_warm else "; stopped.")
            )
        except BaseException as exc:
            self.print_fn(f"Cloud cleanup unconfirmed: {exc}. Check dreamscale sessions list.")
            return exc
        return None

    async def return_home(self):
        """Return after a task or before disconnect; never retry an interrupted ramp."""
        if self.active:
            raise RuntimeError("Stop the active task before returning home.")
        self._preview_instruction = None
        self._cancel_requested = False
        return await self.lifecycle.return_home()

    async def _operate(self, instruction, *, max_actions=None, preview=False):
        if self.active:
            raise RuntimeError("Stop the active task before starting another.")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError("Enter a task instruction.")
        self._cancel_requested = False
        self._operation = asyncio.create_task(self._work(instruction, max_actions, preview=preview))
        try:
            return await self._operation
        finally:
            self._operation = None

    async def _work(self, instruction, max_actions, *, preview):
        trace = None
        episode = None
        failure = None
        conversion_count, adjustment_notified = 0, False

        def record_conversion(report):
            nonlocal conversion_count, adjustment_notified
            value = dict(
                schema_version=2, model=self.model,
                calibration_id=self.end_effector_adapter.calibration_id,
                observation_id=report.observation_id, chunk_id=report.chunk_id,
                accepted=report.accepted, error=report.error,
                adjustments=report.adjustment_count,
                max_position_error_m=max((p.position_error_m for p in report.poses), default=0.),
                max_rotation_error_rad=max(
                    (p.rotation_error_rad for p in report.poses), default=0.,
                ),
                approximation=(
                    dict(
                        asdict(self.end_effector_adapter.pose_approximation),
                        mode=self.end_effector_adapter.pose_approximation.mode,
                    )
                    if self.end_effector_adapter.pose_approximation is not None else None
                ),
            )
            # Bound normal recording volume; every rejection retains its exact
            # attempted poses even after detailed successful receipts are capped.
            if conversion_count < 32 or not report.accepted:
                value["poses"] = [asdict(pose) for pose in report.poses]
            conversion_count += 1
            self.print_fn("Cartesian conversion: " + json.dumps(value, allow_nan=False))
            if report.accepted and report.adjustment_count and not adjustment_notified:
                budget = self.end_effector_adapter.pose_approximation
                caps = []
                if budget.max_position_error_m is not None:
                    caps.append(f"position ≤{budget.max_position_error_m * 1000:g} mm")
                if budget.max_rotation_error_rad is not None:
                    caps.append(f"rotation ≤{budget.max_rotation_error_rad:g} rad")
                limits = ", ".join(caps) if caps else "joint limits; no pose-error cap"
                self.print_fn(
                    f"Using IK approximations with {limits}; adjustments recorded."
                )
                adjustment_notified = True

        previous_state_hook = getattr(self.rig, "on_state", None)
        try:
            if preview:
                if not self._fresh_compute:
                    # Called without start_compute: a fresh session, still before any motion.
                    await self._start_compute()
                self._fresh_compute = False
                # Network calibration needs no motion: it runs while the arms home.
                await self.start_calibration(instruction)
                home_offset = await self.lifecycle.startup_home()
                if self._cancel_requested:
                    raise asyncio.CancelledError
                if self.lifecycle.has_home:
                    offset_note = (
                        "" if home_offset is None
                        else f"; largest measured arm offset {home_offset:.4f} "
                        f"{self.embodiment.unit}"
                    )
                    self.print_fn(f"Homing ramp complete{offset_note}.")
                self.print_fn("Checking the first prediction…")
                await self._finish_background_calibration()
            if not preview and self.trace_dir is not None:
                from dreamscale.trace import TraceRecorder

                recorded = self._recorded_contract()
                trace = TraceRecorder(
                    Path(self.trace_dir) / uuid.uuid4().hex,
                    images=self.trace_images,
                    strategy=self.strategy,
                    model=self.model,
                    **({"contract": recorded} if recorded is not None else {}),
                    # Velocity models declare no joint layout; views use the robot's.
                    layout=self.embodiment.trace_layout(recorded or model_contract(self.model)),
                    execution_mode=self.mode,
                    camera_roles=self.embodiment.camera_roles,
                )
                self.print_fn(f"Recording: {trace.path}")

                def record_state(state):
                    if previous_state_hook is not None:
                        previous_state_hook(state)
                    trace.measured(
                        list(state.position),
                        velocities=None if state.velocity is None else list(state.velocity),
                        capture_unix_s=state.capture_unix_s,
                    )

                self.rig.on_state = record_state
            if self.policy is None:
                self.policy = await self._connect_policy(self.print_fn)
                if self.end_effector_adapter is not None:
                    self.policy = self.end_effector_adapter.bind(self.policy, self.rig)
            if self.end_effector_adapter is not None:
                self.policy.on_conversion = record_conversion
            if self._cancel_requested:
                raise asyncio.CancelledError
            if preview:
                if getattr(self.policy, "requires_task_preparation", False):
                    await self.policy.prepare(instruction=instruction)
                context = RunContext(
                    action_index=0,
                    observation_id=0,
                    actions_remaining=0,
                    stalled=False,
                    elapsed_s=0.0,
                )
                observation = self.observe(context)
                if inspect.isawaitable(observation):
                    observation = await observation
                chunk = await self.policy.predict(observation, instruction=instruction)
                self._preview_observation = observation
                if self._cancel_requested:
                    raise asyncio.CancelledError
                if not chunk.actions:
                    raise RigFault("Model returned no predictions; execution is blocked.")
                self._record_prediction(observation, chunk, instruction)
                for index, action in enumerate(self.preview_actions(chunk.actions), start=1):
                    # Check data and angle saturation, without projecting future
                    # commands against today's measured pose or velocity budget.
                    try:
                        self.rig.validate_action(action, check_step=False, saturate=True)
                    except RigFault as exc:
                        raise RigFault(f"Initial prediction action {index}: {exc}") from exc
                return chunk
            await self._finish_background_calibration()
            if self.hud is not None:
                episode = self.hud_episode = await self.hud.start(
                    instruction,
                    frames=self.rig.latest_frames,
                    joints=list(self.embodiment.joints),
                    fps=self.action_hz,
                    metadata=self._hud_metadata(max_actions),
                )
                record_state = self.rig.on_state

                def record_episode_state(state):
                    if record_state is not None:
                        record_state(state)
                    episode.measured(list(state.position))

                self.rig.on_state = record_episode_state
            hooks = episode.hooks() if episode is not None else None
            if trace is not None:
                hooks = trace.hooks(hooks)
            self.lifecycle.task_started()
            self.rig.enable_dispatch()
            dispatched = False

            def act(action, ctx=None):
                # The preview already consumed the session's one "Inference started."
                # notice, so the first accepted action is what marks the task running.
                nonlocal dispatched
                result = self.act(action, ctx)
                if not dispatched:
                    dispatched = True
                    self.print_fn("Executing model actions.")
                return result

            # A camera codec that codes frames as they arrive gets each new frame now, not when
            # the observation is taken (t16_latency_v1 LP); None for every other session.
            feed = start_camera_feed(self.rig, self.policy)
            try:
                if self.mode == "sync":
                    return await run_sync(
                        policy=self.policy, instruction=instruction, observe=self.observe,
                        act=act, strategy=self.strategy, max_actions=max_actions,
                        hooks=hooks,
                        execution_contract=(self.execution_contract
                                            if self.end_effector_adapter is not None else None),
                    )
                return await self.policy.run(
                    instruction=instruction,
                    observe=self.observe,
                    act=act,
                    read_hold_action=self.read_hold_action,
                    max_actions=max_actions,
                    strategy=self.strategy,
                    **({"hooks": hooks} if hooks is not None else {}),
                )
            finally:
                if feed is not None:
                    feed.stop()
        except BaseException as exc:
            failure = exc
            raise
        finally:
            cleanup_error = None
            holds = {}
            try:
                holds = self.lifecycle.stop_and_hold()
            except BaseException as exc:
                cleanup_error = exc
                self.print_fn("Measured-pose hold unconfirmed. Use hardware E-stop.")
            for arm, held in holds.items():
                self.print_fn(
                    f"{arm.title()}: measured-pose hold commanded."
                    if held
                    else f"{arm.title()}: hold UNCONFIRMED. Use hardware E-stop and reconnect."
                )
            if preview and failure is None and (not holds or not all(holds.values())):
                cleanup_error = cleanup_error or RigFault(
                    "Prediction check ended without confirmed holds; session closed."
                )
            keep_session = (
                preview and failure is None and cleanup_error is None
                and not self._cancel_requested and not self.rig.faulted
            )
            if episode is not None:
                await asyncio.to_thread(episode.stop_recording, failure)
            if trace is not None or episode is not None:
                self.rig.on_state = previous_state_hook
            if not keep_session:
                close_error = await self._close_policy()
                cleanup_error = cleanup_error or close_error
            if trace is not None:
                try:
                    status = trace.close(
                        cleanup={
                            "holds": holds,
                            "error_type": type(cleanup_error).__name__ if cleanup_error else None,
                        }
                    )
                    self.print_fn(
                        f"Recording saved: {trace.path}; dropped {status['events_dropped']} events."
                    )
                    if status["writer_error"] or not status["writer_finished"]:
                        self.print_fn("Recording is incomplete; inspect status.json.")
                except Exception as exc:
                    self.print_fn(f"Recording finalization failed: {type(exc).__name__}.")
            if cleanup_error is not None and failure is None:
                raise cleanup_error

    def _recorded_contract(self):
        """The contract a recording describes: the end-effector adapter's, a robot
        deployment's session (its own widths and rate; the base model has none), or None
        for the model's own."""
        if self.end_effector_adapter is not None:
            return self.execution_contract
        if follows_session_contract(self.model):
            return getattr(self.policy, "runtime_contract", None)
        return None

    def _hud_metadata(self, max_actions):
        from dreamscale import __version__

        metadata = getattr(self.rig, "metadata", None)
        return {
            "dreamscale_version": __version__,
            "model": self.model,
            "robot": self.embodiment.label,
            "session_id": getattr(self.policy, "session_id", None),
            "mode": self.mode,
            "rtc": self.rtc,
            "context": self.context,
            "checkpoint": self.checkpoint,
            "region": self.region,
            "provider": self.provider,
            "speed": self.speed,
            "max_actions": max_actions,
            "keep_warm": self.keep_warm,
            "action_hz": self.action_hz,
            "action_smoothing": getattr(self.strategy, "action_smoothing", None),
            "rig": metadata() if callable(metadata) else None,
        }

    @property
    def action_hz(self):
        """The rate tasks run at: the strategy's, else the connected session's."""
        return (
            self.strategy.action_hz
            or getattr(self.policy, "action_hz", None)
            or self.execution_contract.action_hz
        )

    async def _connect_policy(self, on_progress):
        policy = await self.connect(
            self.model,
            region=self.region,
            **({"provider": self.provider} if self.provider is not None else {}),
            **({"speed": self.speed} if self.speed == "fast" else {}),
            rtc=self.rtc,
            **({"checkpoint": self.checkpoint} if self.checkpoint is not None else {}),
            **({"context": self.context} if self.context != "auto" else {}),
            # A robot deployment runs at the rate it was trained at, which the session says.
            control_hz=(
                None if follows_session_contract(self.model)
                else runtime_contract_for_model(self.model).action_hz
            ),
            keep_warm=self.keep_warm,
            on_progress=on_progress,
        )
        contract = getattr(policy, "runtime_contract", None)
        # An end-effector adapter turns the session's actions into the rig's joints and holds
        # them: its execution contract, not the session's, governs the run.
        converted = self.end_effector_adapter is not None
        if not converted and getattr(contract, "action_space", None) == "model_defined":
            # A π0.5 deployment whose actions aren't joint targets (the CLI refuses it
            # before connecting, where it can read the deployment): Python only.
            deployment = getattr(policy, "deployment", None)
            await _close_quietly(policy)
            raise non_joint_run_error(
                self.checkpoint or getattr(deployment, "id", "this deployment"),
                getattr(deployment, "state_dim", None),
                getattr(deployment, "action_dim", None),
            )
        if not converted and getattr(contract, "hold_behavior", None) == "wait":
            # Its robot waits for each chunk: only sync runs a chunk from its first action
            # (async holds while the clock runs and skips what the wait covered).
            if self.mode != "sync":
                await _close_quietly(policy)
                raise ValueError(WAIT_MODE_MESSAGE)
            on_progress(WAIT_SYNC_NOTE)
        config = getattr(policy, "resolved_optimization_config", None)
        rtc_on = _follows_deployment_session(self.model) and getattr(config, "rtc", None) == "on"
        if rtc_on and self.mode == "sync":
            on_progress(SYNC_RTC_NOTE)
        elif (
            rtc_on
            and getattr(config, "rtc_contract", None) == DYNAMIC_FULL_HORIZON_RTC_CONTRACT_ID
        ):
            on_progress(TEST_TIME_RTC_NOTE)
        return policy

    def _record_prediction(self, observation, chunk, instruction):
        if self.trace_dir is None:
            return
        directory = Path(self.trace_dir).expanduser() / uuid.uuid4().hex
        try:
            directory.mkdir(parents=True)
            record = {
                "model": self.model,
                "instruction": instruction,
                "dispatched": False,
                # A deployment's own observation (dreamscale.robot) names its pose ``state``.
                "observation": {"hold_action": list(
                    getattr(observation, "hold_action", None) or observation.state
                )},
                "actions": [[float(v) for v in action] for action in chunk.actions],
                "limits": self.rig.action_limits(),
            }
            (directory / "prediction.json").write_text(json.dumps(record, indent=2) + "\n")
            if self.trace_images:
                from PIL import Image

                from dreamscale.trace import observation_frame

                for role in self.embodiment.camera_roles:
                    # A role the model doesn't read has no frame (a one-exterior Franka model).
                    frame = observation_frame(observation, role)
                    if frame is not None:
                        Image.fromarray(frame).save(directory / f"{role}.png")
            self.print_fn(f"Initial prediction recorded: {directory}")
        except Exception as exc:
            self.print_fn(f"Initial prediction recording failed: {type(exc).__name__}.")

    def preview_actions(self, actions):
        """A chunk as rig commands from the measured pose, for checks and display."""
        if self.action_space.identity:
            return list(actions)  # positions need no measured pose to preview
        return self.action_space.preview(actions, self.rig.read_hold_action(None))

    async def preview(self, instruction):
        self._preview_instruction = None
        chunk = await self._operate(instruction, preview=True)
        self._preview_instruction = instruction
        return chunk

    async def start_compute(self, instruction):
        """Start this task's cloud session before anything moves (the last task's closes).

        With the robot already connected, network calibration starts too, so it runs while
        the operator confirms.
        """
        if self.active:
            raise RuntimeError("Stop the active task before starting another.")
        if not isinstance(instruction, str) or not instruction.strip():
            raise ValueError("Enter a task instruction.")
        self._preview_instruction = None
        self._cancel_requested = False
        self._operation = asyncio.create_task(self._start_compute())
        try:
            await self._operation
        finally:
            self._operation = None
        self._fresh_compute = True  # this task's session: preview uses it
        if self.lifecycle.ready:
            await self.start_calibration(instruction)

    async def _start_compute(self):
        cleanup_error = await self._close_policy()
        if cleanup_error is not None:
            raise cleanup_error
        self.print_fn("Starting compute… Ctrl+C cancels.")
        progress = self._policy_progress = _HeldProgress(self.print_fn)
        progress.release()
        # Only while nothing of this run drives the robot: once it's connected, it's ours.
        watch = (
            asyncio.create_task(self.while_compute_starts(self.print_fn))
            if self.while_compute_starts is not None and not self.lifecycle.ready
            else None
        )
        try:
            policy = await self._connect_policy(progress)
        finally:
            if watch is not None:
                watch.cancel()
                await asyncio.gather(watch, return_exceptions=True)
        if self.end_effector_adapter is not None:
            policy = self.end_effector_adapter.bind(policy, self.rig)
        self.policy = policy

    async def start_calibration(self, instruction):
        """Measure network timing in the background; the arms hold still meanwhile."""
        if (
            self._calibration is not None
            or self.policy is None
            or getattr(self.policy, "_calibrate", None) is None
            or self.end_effector_adapter is not None
            or self._policy_progress is None
            or getattr(
                getattr(self.policy, "resolved_optimization_config", None), "calibration", None
            ) == "off"
        ):
            return  # nothing to measure here: no observation is taken
        context = RunContext(
            action_index=0, observation_id=0, actions_remaining=0, stalled=False, elapsed_s=0.0,
        )
        observation = self.observe(context)
        if inspect.isawaitable(observation):
            observation = await observation
        self._preview_observation = observation
        self._calibrate_in_background(instruction)

    def hold_progress(self):
        """Keep session messages from breaking a prompt (printed by release_progress)."""
        if self._policy_progress is not None:
            self._policy_progress.hold()

    def release_progress(self):
        if self._policy_progress is not None:
            self._policy_progress.release()

    def discard_progress(self):
        if self._policy_progress is not None:
            self._policy_progress.discard()

    def _calibrate_in_background(self, instruction):
        """Measure network timing while the operator reviews the prediction.

        The arms hold still and nothing is dispatched; execution awaits whatever
        remains. Calibration messages are held so they don't break the prompt.
        """
        calibrate = getattr(self.policy, "_calibrate", None)
        if (
            calibrate is None
            or self.end_effector_adapter is not None
            or self._preview_observation is None
            or self._policy_progress is None
        ):
            return
        self._calibration = asyncio.create_task(
            calibrate(self._preview_observation, instruction=instruction)
        )

    async def _finish_background_calibration(self):
        calibration, self._calibration = self._calibration, None
        self._preview_observation = None
        if self._policy_progress is not None:
            self._policy_progress.release()
        if calibration is not None:
            # A failed attempt is not fatal: the run loop calibrates again.
            await asyncio.gather(calibration, return_exceptions=True)

    async def _cancel_background_calibration(self):
        calibration, self._calibration = self._calibration, None
        self._preview_observation = None
        if calibration is not None:
            calibration.cancel()
            await asyncio.gather(calibration, return_exceptions=True)
            if self._policy_progress is not None:
                self._policy_progress.discard()

    async def execute(self, instruction, *, max_actions=None):
        if max_actions is not None and (
            type(max_actions) is not int or not 1 <= max_actions <= 18000
        ):
            raise ValueError("max_actions must be None or 1–18000.")
        if self._preview_instruction != instruction:
            raise RuntimeError("Obtain a non-dispatched prediction for this instruction first.")
        self._preview_instruction = None
        return await self._operate(instruction, max_actions=max_actions)


def _motion_warning(runner, instruction, max_actions, *, connect):
    """The one confirmation before anything moves: what will move, and for how long."""
    arms = _arms_word(runner.embodiment)
    steps = ("connect, " if connect is not None else "") + (
        "home, then " if runner.lifecycle.has_home else ""
    )
    limit = ""
    if max_actions is not None:
        hz = _task_hz(runner)
        limit = f" for up to {max_actions} actions ({max_actions / hz:g}s at {hz:g} Hz)"
    return (
        f"{arms.title()} will move: {steps}run \"{instruction}\"{limit}. "
        "Clear the workspace; keep E-stop ready."
    )


def _task_hz(runner):
    """The rate a task runs at, once the preview has connected the session."""
    rate = getattr(runner, "action_hz", None)
    if isinstance(rate, int | float):
        return rate
    return runner.strategy.action_hz or runner.execution_contract.action_hz


def _arms_word(embodiment):
    return "arms" if len(embodiment.arms) > 1 else "arm"


class _PromptStopped(Exception):
    pass


class _HeldProgress:
    """Queue progress until release(), then print it and everything after it."""

    def __init__(self, print_fn):
        self._print, self._held = print_fn, []

    def __call__(self, message):
        if self._held is None:
            self._print(message)
        else:
            self._held.append(message)

    def hold(self):
        if self._held is None:
            self._held = []

    def release(self):
        held, self._held = self._held, None
        for message in held or ():
            self._print(message)

    def discard(self):
        self._held = None


async def _terminal_line(prompt, *, interrupted, print_fn=print):
    """Poll canonical stdin, with no executor or blocked input thread to leak."""
    print_fn(prompt)
    while True:
        if interrupted.is_set():
            interrupted.clear()
            raise _PromptStopped
        if select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if not line:
                raise EOFError
            return line.strip()
        await asyncio.sleep(0.05)


async def _grade_hud(runner, read_line, print_fn):
    """Grade the last task while the arms hold its final pose; Ctrl+C or Enter skips."""
    episode, runner.hud_episode = getattr(runner, "hud_episode", None), None
    if episode is None:
        return
    from dreamscale.integrations.hud_recorder import GRADE_PROMPT, parse_grade

    grade = None
    prompt = getattr(episode, "grade_prompt", GRADE_PROMPT)
    try:
        while True:
            answer = await read_line(prompt)
            if not answer:
                break
            grade = parse_grade(answer)
            if grade is not None:
                break
            print_fn("Enter y, n, or a score from 0 to 1.")
    except (_PromptStopped, EOFError):
        grade = None
    finally:
        await episode.finish(grade)


async def _abandon_hud(runner):
    episode, runner.hud_episode = getattr(runner, "hud_episode", None), None
    if episode is not None:
        await episode.finish()


async def interactive_tasks(
    runner,
    *,
    instruction=None,
    max_actions=None,
    read_line=None,
    print_fn=print,
    open_rig=None,
):
    """Returns 'exit' or 'reconnect'; caller owns explicit hardware teardown.

    `instruction` runs one task then exits; a list runs each in turn, then exits. Each
    task starts its compute first, then asks once before anything moves. ``open_rig()``
    connects the robot (its first motion) after the first confirm; None means the rig is
    already connected.
    """
    queued = [instruction] if isinstance(instruction, str) else list(instruction or ())
    pending_instruction = queued.pop(0) if queued else None
    single_task = pending_instruction is not None
    interrupted = asyncio.Event()
    loop = asyncio.get_running_loop()
    embodiment = runner.embodiment
    holding = f"{_arms_word(embodiment)} holding"

    def interrupt():
        if runner.active:
            runner.request_stop()
        else:
            interrupted.set()

    old_handler = signal.getsignal(signal.SIGINT)
    loop.add_signal_handler(signal.SIGINT, interrupt)
    if read_line is None:

        async def read_line(prompt):
            return await _terminal_line(prompt, interrupted=interrupted, print_fn=print_fn)

    try:
        while True:
            try:
                if pending_instruction is None:
                    instruction = await read_line(
                        "Instruction (Ctrl+C to disconnect):"
                    )
                else:
                    instruction, pending_instruction = pending_instruction, None
                    print_fn(f"Instruction: {instruction}")
                if instruction.lower() in {"cancel", "exit", "reconnect"}:
                    return "exit" if instruction.lower() == "cancel" else instruction.lower()
                if not instruction:
                    continue
                # Compute first: nothing moves until it is ready and the operator agrees.
                await runner.start_compute(instruction)
                print_fn(_motion_warning(runner, instruction, max_actions, connect=open_rig))
                runner.hold_progress()
                confirmed = False
                try:
                    while True:
                        choice = await read_line("Enter to start · Ctrl+C to cancel:")
                        if choice.lower() in {"cancel", "exit", "reconnect"}:
                            return "exit" if choice.lower() == "cancel" else choice.lower()
                        if not choice:
                            confirmed = True
                            break
                        print_fn("Enter to start · Ctrl+C to cancel.")
                finally:
                    # Held session messages print once the task goes ahead; a cancelled
                    # task drops them.
                    runner.release_progress() if confirmed else runner.discard_progress()
                if open_rig is not None:
                    print_fn("Connecting robot…")
                    await asyncio.to_thread(open_rig)
                    open_rig = None
                    if interrupted.is_set():  # Ctrl+C while connecting: stop before homing
                        return "exit"
                chunk = await runner.preview(instruction)
                for line in embodiment.preview_lines(
                    runner.preview_actions(chunk.actions), runner.rig.read_hold_action(),
                ):
                    print_fn(line)
                print_fn(
                    "Executing with current observations. Ctrl+C stops, homes and disconnects."
                )
                result = await runner.execute(instruction, max_actions=max_actions)
                print_fn(f"Stopped after {result.actions} steps · {holding}.")
                await _grade_hud(runner, read_line, print_fn)
                if not await runner.return_home():
                    return "exit"
                if queued:
                    pending_instruction = queued.pop(0)
                elif single_task:
                    return "exit"
            except _PromptStopped:
                return "exit"
            except asyncio.CancelledError:
                await runner.stop()
                if runner.rig.faulted:
                    print_fn("Hardware hold unconfirmed: disconnecting. Use the hardware E-stop.")
                    return "exit"
                await _grade_hud(runner, read_line, print_fn)
                await runner.return_home()
                return "exit"
            except EOFError:
                return "exit"
            except Exception as exc:
                print_fn(f"Task stopped: {exc}")
                if runner.rig.faulted:
                    print_fn(
                        "Hardware fault: disconnecting. "
                        "Resolve the reported issue before reconnecting."
                    )
                    return "exit"
                await _grade_hud(runner, read_line, print_fn)
                if not await runner.return_home():
                    return "exit"
                if queued:
                    pending_instruction = queued.pop(0)
                elif single_task:
                    return "exit"
    finally:
        try:
            try:
                await runner.stop()
            finally:
                try:
                    await _abandon_hud(runner)
                finally:
                    await runner.return_home()
        finally:
            loop.remove_signal_handler(signal.SIGINT)
            signal.signal(signal.SIGINT, old_handler)


def run_attended(
    *,
    embodiment,
    make_rig,
    make_runner,
    instruction=None,
    max_actions=None,
    input_fn=input,
    print_fn=print,
    preflight=None,
    read_line=None,
):
    """Confirm, connect the rig, run tasks until exit; reconnect on request.

    preflight() prints and checks what the operator confirms before motors arm.
    make_rig() returns an unopened rig; make_runner(rig, lifecycle) returns the
    AttendedTaskRunner for one connection.
    """
    arms = _arms_word(embodiment)
    if read_line is None and input_fn is not input:
        # A caller's own prompt reader (tests, embedding); the terminal one stays
        # signal-aware otherwise.
        async def read_line(prompt):
            return input_fn(f"{prompt} ").strip()

    while True:
        if preflight is not None:
            preflight()
        rig = make_rig()
        lifecycle = AttendedLifecycle(rig, print_fn=print_fn, ready=False, arms=arms)

        def open_rig(rig=rig, lifecycle=lifecycle):
            # Bounded: startup unwinds every constructor before closing each controller
            # that connected. The task loop calls it after its confirm (the first motion).
            rig.open(attended=True)
            lifecycle.opened()

        try:
            runner = make_runner(rig, lifecycle)
            outcome = asyncio.run(
                interactive_tasks(
                    runner,
                    instruction=instruction,
                    max_actions=max_actions,
                    print_fn=print_fn,
                    open_rig=open_rig,
                    **({"read_line": read_line} if read_line is not None else {}),
                )
            )
            instruction = None
        finally:
            connected = lifecycle.ready
            if connected:
                print_fn("Disconnecting local hardware…")
            lifecycle.close()
            held = getattr(rig, "held_on_close", {})
            if held and all(held.values()):
                print_fn(embodiment.held_message())
            elif connected:
                print_fn("Disconnected.")
        if outcome != "reconnect":
            return
