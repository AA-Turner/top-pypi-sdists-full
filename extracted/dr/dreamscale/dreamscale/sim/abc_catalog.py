"""ABC's simulator as `dreamscale sim abc`: the pinned source, its tasks and the models.

``abc_sim`` (github.com/amazon-far/abc, Apache-2.0) is the MuJoCo simulator of the ABC
bimanual YAM station. Its action and state are the YAM wire's: left six joints and gripper,
then right, radians and a 0 (closed) to 1 (open) gripper.
"""

from __future__ import annotations

from dataclasses import dataclass

from dreamscale_transport import catalog

REPOSITORY = "amazon-far/abc"
# The commit the ABC-VLA family pins (abc-vla-yam's upstream_revision).
REVISION = "d0832d12651d1b260a652861a14648dc5f3660c7"
# Simulator meshes and textures ship as tarballs listed in the source's
# abc_sim/models/assets_manifest.json (sha256 each), on upstream's public mirror.
ASSETS_MANIFEST = "abc_sim/models/assets_manifest.json"
ASSETS_MIRROR = "https://abc-data.timehorizons.org/sim_assets/"
BASE_PACKAGES = ("i2rt_yam",)

# The station's cameras in the YAM wire's order, and upstream's eval image (height, width).
CAMERAS = ("top", "left", "right")
IMAGE_SIZE = (168, 224)
# One action is 17 physics ticks of 2 ms: 0.034 s, the 30 Hz the station's models run at.
CONTROL_HZ = 30
# Upstream's eval budget: 236 chunks of 15 actions.
HORIZON_STEPS = 236 * 15
# Upstream's eval seed: world N's scene is seed SEED + N.
SEED = 20260511


@dataclass(frozen=True)
class Task:
    """A scored abc_sim task: the asset packages its scene loads beyond the arms, and the
    prompt its episodes carried in the ABC parents' training mixture (the released
    checkpoints' ``sim_prompt_map``), which is not the task's own prompt."""

    packages: tuple[str, ...]
    trained_prompt: str


# The five sim tasks in the ABC parents' training mixture (abc_dit_xl_200k_model.json).
TASKS = {
    "put_plastic_bottles_in_bin": Task(
        ("task_water_bottles",), "sim throw plastic bottles in bin"),
    "sweep_away_paper_scraps_from_table": Task(
        ("brush_flat", "dustpan", "garbage_can", "paper_ball"),
        "sim sweep away paper scraps from the table"),
    "turn_mug_right_side_up": Task(
        ("mug", "tray", "task_mug_flip"), "sim turn mug right side up"),
    "load_plates_into_dish_rack": Task(
        ("task_dishrack",), "sim load plates into tabletop dish rack"),
    "hang_mug_on_mug_rack": Task(
        ("mug", "mug_tree", "task_mug_tree"), "sim hang the mug on the mug rack"),
}
DEFAULT_TASK = "put_plastic_bottles_in_bin"

# The YAM joint models the simulator runs (the catalog's ``client.abc_sim``), those trained on
# abc_sim episodes first: they are prompted as in training. Every other one was trained on
# real camera footage only and gets the task's own prompt; its score here says nothing about
# the real robot.
SIM_TRAINED_MODELS = tuple(
    entry.id for entry in catalog.CATALOG if entry.client.abc_sim == "trained")
MODELS = (*SIM_TRAINED_MODELS,
          *(entry.id for entry in catalog.CATALOG if entry.client.abc_sim == "runs"))


def resolve_task(task: str, episode: str | int) -> int:
    """The episode index of a selection: ``task`` names one of TASKS."""
    if task not in TASKS:
        raise ValueError(f"ABC --task-suite must be one of {', '.join(TASKS)}.")
    try:
        index = int(episode)
    except (TypeError, ValueError) as exc:
        raise ValueError("ABC --task-id must be an episode number, 0 or more.") from exc
    if index < 0:
        raise ValueError("ABC --task-id must be an episode number, 0 or more.")
    return index


def prompt_for(model: str, task: str, task_prompt: str) -> str:
    """What ``model`` is told for ``task``: its training prompt if it trained on the sim."""
    return TASKS[task].trained_prompt if model in SIM_TRAINED_MODELS else task_prompt


def packages_for(task: str) -> tuple[str, ...]:
    return (*BASE_PACKAGES, *TASKS[task].packages)
