"""Step a label-prompted deployment through a task on two xArm 7s, freezing the idle arm.

A model trained on labelled phases (one instruction per phase, each moving one arm) runs one
label at a time: Enter starts the next label, `b` goes back one, `q` stops. Whichever arm
the label doesn't move is held where it was when the label started, whatever the model says
for it.

Run: python -m dreamscale.examples.xarm7_labels <account>/<slug> labels.json [first label]
labels.json lists the task's labels in order, each with the arm it moves ("fore" or "aft"):

    [["pick up the cup", "fore"], ["hold the lid open", "aft"]]

It uses the rig file `dreamscale robots xarm7 setup` writes. This is a starting point for your
own runner, not a product command.
"""

from __future__ import annotations

import json
import queue
import sys
import threading
from pathlib import Path

import numpy as np

import dreamscale
from dreamscale.hardware.xarm7_config import ARMS, ROLES, load_config
from dreamscale.hardware.xarm7_rig import XArm7Rig

ARM_SIZE = 8  # seven joints, then the gripper


def frozen(action, hold, active: str) -> tuple[float, ...]:
    """The model's action with every arm but `active` replaced by its held values."""
    out = np.asarray(action, dtype=float).copy()
    for i, arm in enumerate(ARMS):
        if arm != active:
            out[i * ARM_SIZE:(i + 1) * ARM_SIZE] = hold[i * ARM_SIZE:(i + 1) * ARM_SIZE]
    return tuple(out.tolist())


def load_labels(path: str) -> list[tuple[str, str]]:
    """The (label, arm) pairs in a labels file, in task order."""
    labels = json.loads(Path(path).read_text())
    if not isinstance(labels, list) or not labels or not all(
        isinstance(pair, list) and len(pair) == 2 and isinstance(pair[0], str)
        and pair[0].strip() and pair[1] in ARMS for pair in labels
    ):
        sys.exit(f"{path}: expected a list of [label, arm] pairs, arm one of {', '.join(ARMS)}")
    return [(label, arm) for label, arm in labels]


def keys() -> queue.Queue:
    """Lines typed on stdin, as they arrive."""
    lines: queue.Queue = queue.Queue()

    def read():
        for line in sys.stdin:
            lines.put(line.strip().lower())

    threading.Thread(target=read, daemon=True).start()
    return lines


def run(deployment: str, labels: list[tuple[str, str]], *, first: int = 0) -> None:
    config = load_config().validate(complete=True)
    rig = XArm7Rig(config, roles=ROLES, max_joint_step=0.2, max_joint_velocity=0.5)
    typed = keys()
    index = first
    with dreamscale.connect(deployment) as policy:
        rig.open(attended=True)
        try:
            while 0 <= index < len(labels):
                label, active = labels[index]
                print(f"[{index + 1}/{len(labels)}] {label} ({active} arm). "
                      "Enter to start · q to quit")
                if typed.get() == "q":
                    break
                hold = rig.read_hold_action()
                rig.enable_dispatch()
                print("Running. Enter: next label · b: back · q: stop")
                while True:
                    try:
                        key = typed.get_nowait()
                    except queue.Empty:
                        key = None
                    if key is not None:
                        rig.stop()
                        index += -1 if key == "b" else 1
                        if key == "q":
                            index = len(labels)
                        break
                    action = policy.next_action(rig.observe(None), label)
                    rig.act(frozen(action, hold, active))
        finally:
            rig.stop()
            rig.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python -m dreamscale.examples.xarm7_labels <account>/<slug> labels.json"
                 " [first label]")
    run(sys.argv[1], load_labels(sys.argv[2]),
        first=int(sys.argv[3]) - 1 if len(sys.argv) > 3 else 0)
