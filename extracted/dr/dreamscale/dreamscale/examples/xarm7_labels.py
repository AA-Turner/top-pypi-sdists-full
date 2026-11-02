"""Step a label-prompted deployment through a task on two xArm 7s, freezing the idle arm.

A model trained on labelled phases (one instruction per phase, each moving one arm) runs one
label at a time: Enter starts the next label, `b` goes back one, `q` stops. Whichever arm
the label doesn't move is held where it was when the label started, whatever the model says
for it.

Run: python -m dreamscale.examples.xarm7_labels <account>/<slug>
It uses the rig file `dreamscale robots xarm7 setup` writes. Adapt LABELS and ACTIVE_ARM to
your own task; this is a starting point for your own runner, not a product command.
"""

from __future__ import annotations

import queue
import sys
import threading

import numpy as np

import dreamscale
from dreamscale.hardware.xarm7_config import ARMS, ROLES, load_config
from dreamscale.hardware.xarm7_rig import XArm7Rig

# The wiper-fluid refill: (label, the arm it moves), in task order.
LABELS = (
    ("inspect the wiper fluid cap", "fore"),
    ("move the arm above the wiper fluid cap", "aft"),
    ("align the gripper and pop open the cap", "aft"),
    ("hold the wiper fluid cap open", "aft"),
    ("pick up the funnel from the table", "fore"),
    ("move the funnel above the wiper fluid pipe", "fore"),
    ("seat and release the funnel, then move clear", "fore"),
    ("move to and reach around the bottle", "fore"),
    ("grasp the bottle and position it over the funnel", "fore"),
    ("tip and hold the bottle while pouring", "fore"),
    ("return and release the bottle on the table", "fore"),
    ("move to and grasp the funnel in the pipe", "fore"),
    ("lift the funnel out and return it above the table", "fore"),
    ("set down the funnel and inspect the cap", "fore"),
    ("prepare the gripper and press the cap closed", "aft"),
    ("move clear of the closed cap", "aft"),
)
ARM_SIZE = 8  # seven joints, then the gripper


def frozen(action, hold, active: str) -> tuple[float, ...]:
    """The model's action with every arm but `active` replaced by its held values."""
    out = np.asarray(action, dtype=float).copy()
    for i, arm in enumerate(ARMS):
        if arm != active:
            out[i * ARM_SIZE:(i + 1) * ARM_SIZE] = hold[i * ARM_SIZE:(i + 1) * ARM_SIZE]
    return tuple(out.tolist())


def keys() -> queue.Queue:
    """Lines typed on stdin, as they arrive."""
    lines: queue.Queue = queue.Queue()

    def read():
        for line in sys.stdin:
            lines.put(line.strip().lower())

    threading.Thread(target=read, daemon=True).start()
    return lines


def run(deployment: str, *, first: int = 0) -> None:
    config = load_config().validate(complete=True)
    rig = XArm7Rig(config, roles=ROLES, max_joint_step=0.2, max_joint_velocity=0.5)
    typed = keys()
    index = first
    with dreamscale.connect(deployment) as policy:
        rig.open(attended=True)
        try:
            while 0 <= index < len(LABELS):
                label, active = LABELS[index]
                print(f"[{index + 1}/{len(LABELS)}] {label} ({active} arm). "
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
                            index = len(LABELS)
                        break
                    action = policy.next_action(rig.observe(None), label)
                    rig.act(frozen(action, hold, active))
        finally:
            rig.stop()
            rig.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python -m dreamscale.examples.xarm7_labels <account>/<slug> [first label]")
    run(sys.argv[1], first=int(sys.argv[2]) - 1 if len(sys.argv) > 2 else 0)
