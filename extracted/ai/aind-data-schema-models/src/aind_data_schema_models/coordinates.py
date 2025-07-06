"""Coordinate enums for data schema"""

from enum import Enum


class Origin(str, Enum):
    """Origin positions for coordinate systems"""

    ORIGIN = "Origin"  # only exists in Atlases / Images
    BREGMA = "Bregma"
    LAMBDA = "Lambda"
    C1 = "C1"  # cervical vertebrae
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    C5 = "C5"
    C6 = "C6"
    C7 = "C7"
    TIP = "Tip"  # of a probe
    FRONT_CENTER = "Front_center"  # front center of a device, e.g. camera
    ARENA_CENTER = "Arena_center"  # center of an arena on the ground surface
    ARENA_FRONT_LEFT = "Arena_front_left"
    ARENA_FRONT_RIGHT = "Arena_front_right"
    ARENA_BACK_LEFT = "Arena_back_left"
    ARENA_BACK_RIGHT = "Arena_back_right"


class AxisName(str, Enum):
    """Axis name"""

    X = "X"
    Y = "Y"
    Z = "Z"
    AP = "AP"
    ML = "ML"
    SI = "SI"
    DEPTH = "Depth"


class Direction(str, Enum):
    """Local and anatomical directions"""

    LR = "Left_to_right"
    RL = "Right_to_left"
    AP = "Anterior_to_posterior"
    PA = "Posterior_to_anterior"
    IS = "Inferior_to_superior"
    SI = "Superior_to_inferior"
    FB = "Front_to_back"
    BF = "Back_to_front"
    UD = "Up_to_down"
    DU = "Down_to_up"
    OTHER = "Other"
    POS = "Positive"
    NEG = "Negative"


class AnatomicalRelative(str, Enum):
    """Relative positions in 3D space"""

    SUPERIOR = "Superior"
    INFERIOR = "Inferior"
    ANTERIOR = "Anterior"
    POSTERIOR = "Posterior"
    LEFT = "Left"
    RIGHT = "Right"
    MEDIAL = "Medial"
    LATERAL = "Lateral"
    ORIGIN = "Origin"  # on the origin
