"""`dreamscale robots openarm setup`: write the rig file from the recording the model was
trained on, or from the operator's answers.

Only reads Anvil's control stack. A LeRobot dataset's meta/info.json names its joints and
cameras, which is everything the rig file holds; without one, setup asks.
"""

from __future__ import annotations

import json
import time
from dataclasses import replace
from pathlib import Path

from .franka_setup import _choose
from .openarm_config import (
    ARMS,
    CAMERAS,
    DEFAULT_CONFIG_PATH,
    DEFAULT_URL,
    JOINTS,
    load_config,
    save_config,
)
from .openarm_stack import AnvilStack, StackError

# π0.5 reads at most three views.
MAX_MODEL_CAMERAS = 3
_ARM_CHOICES = (("left", "right"), ("left",), ("right",), ("right", "left"))
_ARM_TEXT = ("Both arms, left first", "Left arm only", "Right arm only",
             "Both arms, right first")
_PLACE_TEXT = (
    "Gripper first, then joint 1 to joint 7 (Anvil's converter)",
    "Joint 1 to joint 7, then the gripper",
)
_PLACES = ("first", "last")
# Which views a model usually reads for the arms it drives.
_DEFAULT_CAMERAS = {
    ("left",): ("waist", "chest", "wrist_l"),
    ("right",): ("waist", "chest", "wrist_r"),
}
_BOTH_CAMERAS = ("waist", "wrist_l", "wrist_r")


def _names(feature) -> list[str]:
    """A LeRobot feature's value names, flat (some datasets nest them under one key)."""
    names = feature.get("names") if isinstance(feature, dict) else None
    if isinstance(names, dict):
        names = next((v for v in names.values() if isinstance(v, list)), None)
    return [str(name) for name in names] if isinstance(names, list) else []


def layout_from_info(info: dict) -> dict:
    """The rig file's arms, gripper place and cameras, read from a recording's
    meta/info.json. Raises ValueError naming what doesn't fit an OpenARM recording."""
    features = info.get("features") if isinstance(info, dict) else None
    if not isinstance(features, dict):
        raise ValueError("That file has no features: choose a dataset's meta/info.json.")
    names = _names(features.get("action")) or _names(features.get("observation.state"))
    if not names or len(names) % (JOINTS + 1):
        raise ValueError(
            f"Its action has {len(names)} named values; an OpenARM's has eight per arm."
        )
    arms, places = [], set()
    for start in range(0, len(names), JOINTS + 1):
        block = [name.lower() for name in names[start:start + JOINTS + 1]]
        sides = {
            side for side in ARMS
            if all(side in name or f"_{side[0]}_" in f"_{name}" for name in block)
        }
        fingers = [i for i, name in enumerate(block) if "finger" in name or "gripper" in name]
        joints = [name for i, name in enumerate(block) if i not in fingers]
        ordered = all(f"joint{i}" in name.replace("_", "") for i, name in enumerate(joints, 1))
        if len(sides) != 1 or fingers not in ([0], [JOINTS]) or not ordered:
            raise ValueError(
                "Its joints aren't whole arms of joint 1 to joint 7 with the gripper first or "
                f"last: {', '.join(block)}."
            )
        arms.append(sides.pop())
        places.add("first" if fingers == [0] else "last")
    if len(set(arms)) != len(arms) or len(places) != 1:
        raise ValueError("Its arms repeat, or place their grippers differently.")
    cameras = [
        key.removeprefix("observation.images.") for key in features
        if key.startswith("observation.images.")
    ]
    unknown = [camera for camera in cameras if camera not in CAMERAS]
    if unknown:
        raise ValueError(
            f"Its cameras include {', '.join(unknown)}; an Anvil cell's are "
            f"{', '.join(CAMERAS)}."
        )
    return {
        "arms": tuple(arms), "gripper": places.pop(),
        "cameras": tuple(camera for camera in CAMERAS if camera in cameras),
    }


def read_stack(url, *, stack_factory=AnvilStack, wait_s=2.0) -> dict:
    """What the stack reports, read-only: the arms it publishes and the cameras it lists."""
    stack = stack_factory(url)
    try:
        stack.open()
    except StackError as exc:
        return {"error": str(exc)}
    try:
        deadline = time.monotonic() + wait_s
        while not stack.arms_present() and time.monotonic() < deadline:
            time.sleep(0.05)
        # Each arm's joints may arrive in their own message: let the second one land.
        time.sleep(0.3)
        return {"arms": stack.arms_present(), "cameras": stack.cameras_present()}
    finally:
        stack.close()


def _choose_cameras(default, available, *, input_fn, print_fn):
    names = ", ".join(available)
    while True:
        reply = input_fn(
            f"Cameras the model reads, up to {MAX_MODEL_CAMERAS} of {names} "
            f"[{', '.join(default)}]: "
        ).strip()
        chosen = tuple(part.strip() for part in reply.replace(",", " ").split()) or default
        if (
            0 < len(chosen) <= MAX_MODEL_CAMERAS and len(set(chosen)) == len(chosen)
            and set(chosen) <= set(CAMERAS)
        ):
            return tuple(camera for camera in CAMERAS if camera in chosen)
        print_fn(f"Name one to {MAX_MODEL_CAMERAS} of {', '.join(CAMERAS)}.")


def run_openarm_setup(
    config_path=DEFAULT_CONFIG_PATH,
    *,
    stack=read_stack,
    input_fn=input,
    print_fn=print,
):
    config_path = Path(config_path)
    config = load_config(config_path)
    print_fn("OpenARM setup. Nothing moves; Anvil's control stack is only read.")
    url = input_fn(f"Control stack address [{config.url or DEFAULT_URL}]: ").strip() or config.url
    config = replace(config, url=url).validate()
    seen = stack(url)
    if "error" in seen:
        print_fn(f"Couldn't read the stack: {seen['error']}")
    else:
        arms, cameras = seen.get("arms") or (), seen.get("cameras")
        print_fn(f"The stack reports: {' and '.join(arms) or 'no'} arm"
                 + ("" if cameras is None else f"; cameras {', '.join(cameras) or 'none'}"))

    layout = None
    while layout is None:
        path = input_fn(
            "Path to the meta/info.json of the dataset your model was trained on "
            "[Enter to answer by hand]: "
        ).strip()
        if not path:
            break
        try:
            layout = layout_from_info(json.loads(Path(path).expanduser().read_text()))
        except (OSError, ValueError) as exc:
            print_fn(f"Couldn't use that file: {exc}")
    if layout is None:
        saved = tuple(config.arms) or tuple(seen.get("arms") or ()) or _ARM_CHOICES[0]
        arms = _ARM_CHOICES[_choose(
            "Arms the model drives, in its order:", list(_ARM_TEXT),
            default=_ARM_CHOICES.index(saved) + 1 if saved in _ARM_CHOICES else 1,
            input_fn=input_fn, print_fn=print_fn,
        ) - 1]
        place = _PLACES[_choose(
            "Each arm's eight values, in the model's order:", list(_PLACE_TEXT),
            default=_PLACES.index(config.gripper) + 1, input_fn=input_fn, print_fn=print_fn,
        ) - 1]
        default = tuple(config.cameras) or _DEFAULT_CAMERAS.get(arms, _BOTH_CAMERAS)
        layout = {
            "arms": arms, "gripper": place,
            "cameras": _choose_cameras(
                default, seen.get("cameras") or CAMERAS, input_fn=input_fn, print_fn=print_fn,
            ),
        }
    if len(layout["cameras"]) > MAX_MODEL_CAMERAS:
        raise ValueError(
            f"That recording has {len(layout['cameras'])} cameras; a model reads up to "
            f"{MAX_MODEL_CAMERAS}. Answer by hand and name the ones it was trained on."
        )
    home = config.home_pose
    if home is not None and tuple(layout["arms"]) != tuple(config.arms):
        print_fn("The arms changed, so the saved home pose is cleared.")
        home = None
    config = replace(config, home_pose=home, **layout).validate(complete=True)
    place = "before" if config.gripper == "first" else "after"
    print_fn(
        f"Arms: {', '.join(config.arms)} · gripper {place} the joints · cameras: "
        f"{', '.join(config.cameras)}"
    )
    missing = [arm for arm in config.arms if "error" not in seen and arm not in seen["arms"]]
    if missing:
        print_fn(f"The stack reports no {' or '.join(missing)} arm right now.")
    save_config(config, config_path)
    print_fn(f"Saved {config_path}. Next: dreamscale doctor openarm")
    return config
