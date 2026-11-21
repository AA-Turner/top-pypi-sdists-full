"""SDK adapter for the original per-robot Isaac 0.5 deployments."""

from dreamscale_core.families import ISAAC05

from dreamscale.deploy_bases import Base, DeployBase, cmd

# The original CLI also accepted the lower-case model label without spaces.
CLI_ALIAS = ISAAC05.label.lower().replace(" ", "")

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
TYPICAL_BUILD = "usually about 15 min"
CLI = Base({"bimanual_yam": "Bimanual YAM", "so101": "SO-101"},
                  BUILD_STEPS, TYPICAL_BUILD)


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
    family="isaac05", name="perceptron-isaac05", label="Isaac 0.5", cli=CLI,
    aliases=("isaac05", CLI_ALIAS), robot_line=robot_line, runner=runner, claims_model=True,
    row_models=("perceptron-isaac05-yam", "perceptron-isaac05-so101"),
    rtc_refusal_fix="choose RTC per run with `dreamscale run … --rtc`",
    preview_contract=PREVIEW_CONTRACT,
)
