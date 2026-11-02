"""A units base whose deployments run one robot preset (DSL-353 P20, docs/plans/
2026-10-30-family-registries.md §6.6): the export fixes its cameras, widths, chunk and rate, and
its RTC is off or trained with a prefix cap. Its CLI hooks (`deployments create`, the robot
line, Detect's lines, `deployments rtc`) are this module's, from the facts its transport module
declares; its sessions' contract is ``dreamscale.policy.preset_deployment``'s.

A base declares one ``PresetUnits`` and passes ``hooks()`` to its ``DeployBase``; what it does
beyond them (a `dreamscale run` runner, aliases, its own Detect lines) stays in its module.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dreamscale.deploy_bases import cli, cmd


@dataclass(frozen=True)
class PresetUnits:
    """One robot preset's units base, as its transport module declares it."""

    name: str  # its base: the model its deployments serve
    label: str  # what its refusals call it
    source_format: str
    preset: str
    preset_label: str  # how its rows and Detect name the robot ("Bimanual YAM")
    # Each camera: the key the robot sends it under, and the checkpoint camera it fills.
    cameras: tuple[tuple[str, str], ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    action_hz: float
    action_space: str
    joint_unit: str | None
    gripper_unit: str | None
    gripper_indices: tuple[int, ...]
    # Trained RTC's contract, and the most prefix rows a request carries (None: RTC off).
    rtc_contract: str | None = None
    max_trained_rtc_delay: int = 0
    # Its robot line's name (default: label), how prose names its robot (default: its
    # preset's label), and what a user deploys.
    title: str | None = None
    robot: str | None = None
    noun: str = "export"
    # Detect's lines where the base prints its own (default: ``found_lines``).
    describe_found: Callable[[dict], list[str]] | None = None

    @property
    def trained(self) -> bool:
        return self.rtc_contract is not None

    @property
    def joints(self) -> bool:
        return self.action_space == "absolute_joint_position"

    def hooks(self) -> dict[str, Any]:
        """Its ``DeployBase`` fields."""
        return {
            "robot_line": self.robot_line, "shows_rtc": self.trained,
            "set_rtc": self.set_rtc if self.trained else None, "detects_as_base": True,
            "found_lines": self.describe_found or self.found_lines, "create": self.create,
        }

    # --- rows ---------------------------------------------------------------------------------

    def robot_line(self, checkpoint: dict) -> str:
        """`<title> · <robot> · 25 of 50 actions at 30 Hz · RTC trained (…)`."""
        spec = checkpoint.get("embodiment") or {}
        executed = spec.get("executed_actions")
        parts = [self.title or self.label, self.preset_label,
                 f"{executed or self.action_horizon} of {self.action_horizon} actions at "
                 f"{cmd._hz(self.action_hz)} Hz"]
        if self.trained and checkpoint.get("rtc_method") and (
                checkpoint.get("status") != "building"):
            parts.append(f"RTC {cmd.prefix_rtc(checkpoint)}")
        return " · ".join(parts)

    def found_lines(self, found: dict) -> list[str]:
        """What Detect read: which export, its robot and its RTC."""
        checkpoint = found.get("checkpoint") or {}
        step = checkpoint.get("step")
        actions = (f"{self.action_dim} joint targets" if self.joints
                   else f"{self.action_dim}-value {self.action_space} actions")
        cameras = ", ".join(feature.replace("_", " ") for _, feature in self.cameras)
        lines = [
            f"{self.noun.capitalize()}: {checkpoint.get('path')}"
            + (f" (step {step:,})" if isinstance(step, int) else ""),
            f"Robot: {self.preset_label} ({actions}; cameras {cameras}; "
            f"{cmd._hz(self.action_hz)} Hz)",
        ]
        if self.trained:
            trained = (found.get("rtc") or {}).get("trained_max_delay") or 0
            lines.append(f"RTC: trained (prefix up to {trained})" if trained
                         else "RTC: off (not trained)")
        return lines

    # --- `deployments create` -----------------------------------------------------------------

    def run_add(self, *, repo: str, revision=None, name=None, hf_token=None, path=None,
                executed=None, rtc=None, rtc_prefix=None, region="auto", wait=True,
                keep_warm=None, slug=None, region_fallback=None, client_factory=None,
                print_fn=print, sleep=time.sleep):
        """Read an export (a Hub repo or a local folder), pin the resolved commit, and deploy
        it on the preset's robot."""
        if client_factory is None:
            from dreamscale.control import ControlPlaneClient

            client_factory = ControlPlaneClient
        region = cmd._check_region(client_factory, self.name, self.label, region,
                                   print_fn=print_fn)
        if self.trained:
            if rtc not in (None, "off", "trained"):
                raise cmd._invalid(f"{self.label} runs RTC off or trained",
                                   "use --rtc off or --rtc trained")
            if rtc_prefix is not None and rtc == "off":
                raise cmd._invalid("--rtc-prefix goes with trained RTC",
                                   "omit --rtc-prefix, or --rtc off")
        elif rtc not in (None, "off") or rtc_prefix is not None:
            raise cmd._invalid(f"{self.label} runs RTC off", "omit --rtc and --rtc-prefix")
        folder = cmd._local_source(repo, self.name)
        if folder and (revision is not None or hf_token is not None):
            raise cmd._invalid(
                f"a local {self.noun} has no Hub revision or token",
                "omit --revision and --hf-token",
            )
        token = cmd.hugging_face.token(hf_token) if folder is None else None
        if folder:
            found = cmd._inspect_local(client_factory, folder, print_fn, path=path,
                                       base=self.name)
        else:
            _, found = cmd._inspect_with_status(
                client_factory, repo, revision, token, print_fn, base=self.name, path=path,
            )
        if found.get("source_format") != self.source_format:
            article = "an" if self.label[:1].lower() in "aeiou" else "a"
            raise cmd._invalid(f"the server did not read {article} {self.label} {self.noun}",
                               "update the SDK and retry")
        for line in (self.describe_found or self.found_lines)(found):
            print_fn(line)
        if self.trained:
            trained = (found.get("rtc") or {}).get("trained_max_delay") or 0
            method = rtc or ("trained" if rtc_prefix is not None else None)
            if method == "trained" and not trained:
                raise cmd._invalid(
                    f"this {self.noun} records no prefix training, so it can't run trained "
                    "RTC", "omit --rtc (it runs RTC off)",
                )
        else:
            method = "off"
        embodiment: dict = {"preset": self.preset}
        if executed is not None:
            embodiment["executed_actions"] = executed
        source = found.get("request") or {}
        local = {}
        if folder:
            local = {
                "upload_id": cmd._upload_checkpoint(
                    client_factory, folder, found, print_fn, base_model=self.name
                ),
                "source_format": self.source_format, "shown": str(Path(repo).expanduser()),
            }
            repo, name = None, name or folder.label
        else:
            repo, revision = source["repo"], source["revision"]
        return cmd.run_add(
            repo=repo, model=self.name, revision=revision, name=name, hf_token=token,
            embodiment=embodiment, region=region, wait=wait,
            client_factory=client_factory, print_fn=print_fn, sleep=sleep,
            keep_warm=keep_warm, slug=slug,
            source_path=source.get("source_path") or (found.get("source") or {}).get("path", ""),
            rtc_method=method, rtc_max_delay=rtc_prefix, region_fallback=region_fallback, **local,
        )

    def create(self, *, repo, given, preset, camera, hz, path, executed, steps, joint_unit, rtc,
               rtc_prefix, revision, name, hf_token, region, wait, keep_warm, slug,
               region_fallback=None) -> None:
        """`deployments create --base <its name>`: the options its robot leaves open."""
        allowed = ("path", "executed", "rtc") if self.trained else ("path", "executed")
        unsupported = {key: value for key, value in given.items() if key not in allowed}
        if preset not in (None, self.preset) or camera or hz is not None or (
            steps is not None or joint_unit is not None
            or (not self.trained and rtc_prefix is not None)
            or any(value is not None for value in unsupported.values())
        ):
            options = ("--path, --executed, --rtc and --rtc-prefix" if self.trained
                       else "--path and --executed")
            raise cli.typer.BadParameter(
                f"{self.label} runs the {self.robot or self.preset_label} (its cameras, widths "
                f"and rate are fixed); pass only {options}."
            )
        result = {}
        cli._run(
            lambda **kwargs: result.update(self.run_add(**kwargs)),
            repo=repo, revision=revision, name=name, hf_token=hf_token, path=path,
            executed=executed, rtc=rtc, rtc_prefix=rtc_prefix, region=region or cmd.AUTO_REGION,
            wait=wait, keep_warm=keep_warm, slug=slug, region_fallback=region_fallback,
        )
        if result.get("status") == "failed":
            raise cli.typer.Exit(code=1)

    # --- `deployments rtc` --------------------------------------------------------------------

    def set_rtc(self, row, checkpoint_id, method, max_delay, client_factory, print_fn) -> dict:
        return cmd._set_prefix_rtc(row, checkpoint_id, method, max_delay, client_factory,
                                   print_fn, label=self.label)
