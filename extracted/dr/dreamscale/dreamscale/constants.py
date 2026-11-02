"""Dreamscale SDK constants.

Cross-component values come from dreamscale_transport.constants (single binding
source — docs/plans/2026-06-10-dropbear-mvp-00-master.md) and are re-exported.
SDK-only values are defined below.
"""

from typing import TYPE_CHECKING

from dreamscale_transport import catalog
from dreamscale_transport.constants import (
    CHUNK_SIZE,
    EXEC_HZ,
    HEARTBEAT_S,
    LEASE_TTL_S,
    MAX_STEP_DEG,
    MODEL_BIMANUAL_YAM,
    MODEL_DREAMZERO_DROID,
    MODEL_DREAMZERO_YAM,
    MODEL_DROID,
    MODEL_GROOT_LIBERO,
    MODEL_LIBERO,
    MODEL_SO101,
    OBS_HZ,
    START_TIMEOUT_S,
    UDP_PORT_BIMANUAL_YAM,
    UDP_PORT_DROID,
    UDP_PORT_GROOT,
    UDP_PORT_LIBERO,
    UDP_PORT_SO101,
)

__all__ = [
    "CHUNK_SIZE", "EXEC_HZ", "HEARTBEAT_S", "LEASE_TTL_S", "MAX_STEP_DEG",
    "MODEL_BIMANUAL_YAM", "MODEL_DROID", "MODEL_GROOT_LIBERO", "MODEL_LIBERO",
    "MODEL_DREAMZERO_DROID", "MODEL_DREAMZERO_YAM", "MODEL_SO101", "OBS_HZ", "START_TIMEOUT_S",
    "UDP_PORT_BIMANUAL_YAM",
    "UDP_PORT_DROID", "UDP_PORT_GROOT", "UDP_PORT_LIBERO",
    "UDP_PORT_SO101",
    "DEFAULT_CONTROL_PLANE_URL", "LEGACY_CONTROL_PLANE_URLS", "JOINT_NAMES",
    "CAMERA_KEY_SO101", "CAMERA_KEY_SO101_SIDE", "CAMERA_KEY_SO101_WRIST",
    "CAMERA_KEY_LIBERO_AGENT", "CAMERA_KEY_LIBERO_WRIST",
    "CAMERA_KEY_DROID_EXTERIOR_1", "CAMERA_KEY_DROID_EXTERIOR_2",
    "CAMERA_KEY_DROID_WRIST", "CAMERA_KEY_BIMANUAL_YAM_TOP",
    "CAMERA_KEY_BIMANUAL_YAM_LEFT", "CAMERA_KEY_BIMANUAL_YAM_RIGHT",
    "OBS_FRAME_WIDTH", "OBS_FRAME_HEIGHT", "OBS_JPEG_QUALITY",
    "STALE_ACTION_S", "MAX_PREDICTIONS",
    "POLL_INTERVAL_S", "RESUME_POLL_INITIAL_S",
]

# The SDK's own model-id constants (MolmoAct2 bimanual YAM TT-RTC and the π0.5 train-time-RTC
# checkpoints on SO-101, ARX5 and DROID): each catalog entry names its constant
# (``CatalogModel.constant``); transport exports its SUPPORTED_MODELS' ones, and this module
# reads the rest from the catalog.
_CATALOG_CONSTANTS = {
    entry.constant: entry.id for entry in catalog.CATALOG
    if entry.constant and not entry.in_supported_models
}
__all__ += list(_CATALOG_CONSTANTS)


def __getattr__(name: str) -> str:
    try:
        return _CATALOG_CONSTANTS[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None


def __dir__() -> list[str]:
    return sorted({*globals(), *_CATALOG_CONSTANTS})


if TYPE_CHECKING:  # their names, for type checkers and IDEs (values: the catalog's)
    MODEL_BIMANUAL_YAM_TTRTC: str
    MODEL_PI05_SO101: str
    MODEL_PI05_ARX5: str
    MODEL_PI05_DROID: str

DEFAULT_CONTROL_PLANE_URL = "https://api.dreamscalelabs.com"
LEGACY_CONTROL_PLANE_URLS = (
    "https://api.dropbear.dreamscalelabs.com",
    "https://api.dropbear.dreamtimelabs.ai",
)
# The dashboard of each hosted control plane (config.dashboard_url); a local one has none.
DASHBOARD_URLS = {
    DEFAULT_CONTROL_PLANE_URL: "https://app.dreamscalelabs.com",
    "https://api-dev.dreamscalelabs.com": "https://app-dev.dreamscalelabs.com",
}

# SO-101 motor order (lerobot 0.6.1 SOFollower bus order); index 5 is the gripper.
JOINT_NAMES: tuple[str, ...] = (
    "shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper",
)

# Image keys. SO-101 sends two physical views in observation order: side, wrist.
# ``CAMERA_KEY_SO101`` is kept as a compatibility alias for older code that only
# knew about the side camera. Worker decode is key-agnostic and follows
# observation order, so validation may use the sandbox-serving ids ("image",
# "wrist_image") while SDK wire keeps these fully qualified ids.
CAMERA_KEY_SO101_SIDE = "side_cam"
CAMERA_KEY_SO101_WRIST = "wrist_cam"
CAMERA_KEY_SO101 = CAMERA_KEY_SO101_SIDE
CAMERA_KEY_LIBERO_AGENT = "observation.images.image"
CAMERA_KEY_LIBERO_WRIST = "observation.images.wrist_image"
CAMERA_KEY_DROID_EXTERIOR_1 = "observation.images.exterior_1_left"
CAMERA_KEY_DROID_EXTERIOR_2 = "observation.images.exterior_2_left"
CAMERA_KEY_DROID_WRIST = "observation.images.wrist_left"
CAMERA_KEY_BIMANUAL_YAM_TOP = "observation.images.top"
CAMERA_KEY_BIMANUAL_YAM_LEFT = "observation.images.left"
CAMERA_KEY_BIMANUAL_YAM_RIGHT = "observation.images.right"

# Webcam frames go up at capture resolution (commodity 480p) — the worker resizes.
OBS_FRAME_WIDTH = 640
OBS_FRAME_HEIGHT = 480
OBS_JPEG_QUALITY = 80

# Safety: a buffered action older than this is stale and must never execute
# (freeze-on-disconnect). 1.0 s ≈ 3 chunk periods at CHUNK_SIZE=10 / EXEC_HZ=30.
STALE_ACTION_S = 1.0
# Temporal ensembling keeps this many overlapping chunk predictions.
MAX_PREDICTIONS = 2

# Accepted API key prefixes. Keys are issued as dropbear_sk_ today; accepting the
# new prefix now means switching issuance needs no SDK release.
API_KEY_PREFIXES = ("dreamscale_sk_", "dropbear_sk_")

POLL_INTERVAL_S = 2.0  # GET poll while `starting` (each poll refreshes the lease)
RESUME_POLL_INITIAL_S = 0.05  # first GET after a keep-warm reclaim; doubles to POLL_INTERVAL_S
