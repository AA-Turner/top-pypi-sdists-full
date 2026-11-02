"""RoboEval task families, without importing the simulator.

Instructions are the task strings rho-roboeval was trained with
(microsoft/roboeval-data-for-rho). Variants are upstream's environment classes,
static first. Horizons are 20 Hz steps, about twice the 95th-percentile demo.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoboEvalFamily:
    module: str
    variants: tuple[str, ...]
    instruction: str
    horizon: int


FAMILIES = {
    "lift_pot": RoboEvalFamily(
        "lift_pot",
        ("LiftPot", "LiftPotPosition", "LiftPotOrientation", "LiftPotPositionAndOrientation"),
        "Grip the kitchen pot by its handles and raise it above the table.", 300),
    "stack_two_blocks": RoboEvalFamily(
        "manipulation",
        ("StackTwoBlocks", "StackTwoBlocksPosition", "StackTwoBlocksOrientation",
         "StackTwoBlocksPositionAndOrientation"),
        "Manipulate two cubes placed on the table so that they are stacked.", 300),
    "cube_handover": RoboEvalFamily(
        "manipulation",
        ("CubeHandover", "CubeHandoverPosition", "CubeHandoverOrientation",
         "CubeHandoverPositionAndOrientation", "VerticalCubeHandover"),
        "Pass a cube between the robot's two arms.", 400),
    "pick_single_book_from_table": RoboEvalFamily(
        "stack_books",
        ("PickSingleBookFromTable", "PickSingleBookFromTablePosition",
         "PickSingleBookFromTableOrientation", "PickSingleBookFromTablePositionAndOrientation"),
        "Grip the target book on the table and lift it up.", 300),
    "stack_single_book_shelf": RoboEvalFamily(
        "stack_books",
        ("StackSingleBookShelf", "StackSingleBookShelfPosition",
         "StackSingleBookShelfPositionAndOrientation"),
        "Pick up the book from the table and place it in contact with one of the shelves.", 450),
    "pack_box": RoboEvalFamily(
        "pack_objects",
        ("PackBox", "PackBoxPosition", "PackBoxOrientation", "PackBoxPositionAndOrientation"),
        "Have each arm interact with the two-flap packing box and close both flaps until the "
        "opening is fully covered.", 450),
    # Upstream's DragOverAndLiftTray variant is broken (its preset has no BreakfastTray).
    "lift_tray": RoboEvalFamily(
        "lift_tray",
        ("LiftTray", "LiftTrayPosition", "LiftTrayOrientation", "LiftTrayPositionAndOrientation"),
        "Grasp the breakfast tray with the two grippers and lift it clear of the source table.",
        300),
    "rotate_valve": RoboEvalFamily(
        "rotate_utility_objects",
        ("RotateValve", "RotateValvePosition", "RotateValvePositionAndOrientation"),
        "Rotate each valve counterclockwise.", 400),
}


def resolve_variant(family: str, task_id: str | int) -> str:
    """Return the environment class for a family and a variant index or name."""
    if family not in FAMILIES:
        raise ValueError(f"RoboEval --task-suite must be one of {', '.join(FAMILIES)}.")
    variants = FAMILIES[family].variants
    value = str(task_id)
    if value in variants:
        return value
    if value.isdecimal() and int(value) < len(variants):
        return variants[int(value)]
    raise ValueError(f"Unknown {family} variant {value!r}. Use "
                     f"0–{len(variants) - 1} or one of {', '.join(variants)}.")
