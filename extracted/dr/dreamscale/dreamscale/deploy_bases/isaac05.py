"""Isaac 0.5 deployments in the SDK: a preset (or the repo's own adapter, or the robot's shapes)
on the base weights, RTC chosen per run. Its legacy path (the create, Detect and embodiment
code in ``checkpoints_cmd``) stays until DSL-348 moves it onto units."""

from __future__ import annotations

from dreamscale.deploy_bases import Base, DeployBase, cmd

# Build steps in order, with the intake phases each covers.
BUILD_STEPS = (
    ("Finding the repo", ("building", "resolving")),
    ("Checking architecture", ("checking_architecture",)),
    ("Downloading", ("downloading",)),
    ("Converting", ("converting",)),
    ("Saving", ("sealing", "built")),
    # Intake reports its final phase a moment before the row's status flips.
    ("Testing on a server", ("qualifying", "ready", "failed")),
)
# Measured builds took 11–18 minutes (2026-10-09 to 2026-10-12, dev and prod).
TYPICAL_BUILD = "usually about 15 min"
CLI = Base({"bimanual_yam": "Bimanual YAM", "so101": "SO-101"}, BUILD_STEPS, TYPICAL_BUILD)


def robot_line(checkpoint: dict) -> str:
    return cmd.embodiment_line(checkpoint.get("embodiment"))


def runner(embodiment, checkpoint_id, row, model):
    """The caller's model (or else the deployment's own): Isaac 0.5 serves per robot."""
    if model is not None:
        raise cmd._invalid(
            f"{checkpoint_id} is an Isaac 0.5 deployment, not π0.5",
            f"run it with --model perceptron-isaac05-{embodiment.name}, or without --model",
        )
    return row.get("model")


# The base model before a session opens: a deployment's embodiment sets the rate, chunk and
# widths (the session's resolved contract carries them).
PREVIEW_CONTRACT = {
    "action_hz": 30.0,
    "chunk_size": 30,
    "action_space": "absolute_joint_position",
    "hold_behavior": "current_position",
    "task_prepare_timeout_s": 300.0,
}
BASE = DeployBase(
    family="isaac05", name="isaac0.5", label="Isaac 0.5", cli=CLI,
    aliases=("isaac05", "perceptron-isaac05"), robot_line=robot_line, runner=runner,
    rtc_refusal_fix="choose RTC per run with `dreamscale run … --rtc`",
    preview_contract=PREVIEW_CONTRACT,
)
