"""Config cache: ~/.dreamscale/config.toml (binding schema in the master plan).

Atomic writes (temp file + os.replace) with 0600 perms — the file holds the
API key and integration keys. DREAMSCALE_HOME overrides the directory (used by tests).

Installs from before the rename keep working in place: when ~/.dreamscale does
not exist, an existing ~/.dropbear is used as is (never copied), and the legacy
DROPBEAR_HOME / DROPBEAR_API_KEY variables are read after the new names.
"""

from __future__ import annotations

import os
import tempfile
import tomllib
import warnings
from dataclasses import dataclass, field, replace
from pathlib import Path

import tomli_w

from dreamscale.constants import (
    DASHBOARD_URLS,
    DEFAULT_CONTROL_PLANE_URL,
    LEGACY_CONTROL_PLANE_URLS,
)

HOME_ENV = "DREAMSCALE_HOME"
LEGACY_HOME_ENV = "DROPBEAR_HOME"
API_KEY_ENV = "DREAMSCALE_API_KEY"
LEGACY_API_KEY_ENV = "DROPBEAR_API_KEY"
DEFAULT_HOME = "~/.dreamscale"
LEGACY_HOME = "~/.dropbear"
DEFAULT_CALIBRATION_PATH = f"{DEFAULT_HOME}/calibration/so101.json"
LEGACY_CALIBRATION_PATH = f"{LEGACY_HOME}/calibration/so101.json"
# "nearest" is "auto" by its older name; config.toml keeps writing it so older SDKs sharing
# this file still read a region they accept.
DEFAULT_REGION = "nearest"

_warned: set[str] = set()


def env_with_legacy(name: str, legacy: str) -> str | None:
    """Read ``name``, then the pre-rename ``legacy`` variable with a one-time notice."""
    value = os.environ.get(name)
    if value:
        return value
    value = os.environ.get(legacy)
    if not value:
        return None
    if legacy not in _warned:
        _warned.add(legacy)
        warnings.warn(
            f"{legacy} is deprecated; set {name} instead.", FutureWarning, stacklevel=3
        )
    return value


def legacy_home_in_use() -> Path | None:
    """The pre-rename ~/.dropbear, when it is used in place of ~/.dreamscale."""
    home = Path(DEFAULT_HOME).expanduser()
    legacy = Path(LEGACY_HOME).expanduser()
    return legacy if not home.exists() and legacy.is_dir() else None


def dreamscale_home() -> Path:
    """Resolve the SDK directory: env override, ~/.dreamscale, or a legacy ~/.dropbear."""
    override = env_with_legacy(HOME_ENV, LEGACY_HOME_ENV)
    if override:
        return Path(override).expanduser()
    return legacy_home_in_use() or Path(DEFAULT_HOME).expanduser()


# Pre-rename name, kept for callers of the public config module.
dropbear_home = dreamscale_home


def default_calibration_path() -> str:
    return LEGACY_CALIBRATION_PATH if legacy_home_in_use() else DEFAULT_CALIBRATION_PATH


def config_path() -> Path:
    return dreamscale_home() / "config.toml"


@dataclass
class Config:
    api_key: str | None = None
    control_plane_url: str = DEFAULT_CONTROL_PLANE_URL
    preferred_region: str = DEFAULT_REGION
    robot_port: str | None = None
    calibration_path: str = field(default_factory=default_calibration_path)
    camera_index: int | None = None
    wrist_camera_index: int | None = None
    # SO-101 rest pose from `dreamscale robots so101 home --set`: JOINT_NAMES order,
    # calibrated degrees (gripper 0-100).
    home_position: list[float] | None = None
    # Third-party platform credentials by integration, e.g. {"hud": {"api_key": "..."}},
    # from `dreamscale integrations <name> setup`.
    integrations: dict[str, dict[str, str]] = field(default_factory=dict)
    # [camera_codec]: this robot's codec device (internal rollout; dreamscale.camera_codec).
    camera_codec: dict[str, object] = field(default_factory=dict)
    # Where ``api_key`` came from: "DREAMSCALE_API_KEY", "login" (config.toml), or None.
    api_key_source: str | None = field(default=None, repr=False, compare=False)


def load_config() -> Config:
    """The saved config, with the API key from $DREAMSCALE_API_KEY when it is set.

    Once SO-101's rig file (~/.config/dreamscale/so101.json) exists, its port,
    calibration path and home pose replace config.toml's legacy [robot] keys, and its
    cameras replace [camera]: camera_index and wrist_camera_index then read None.

    Key precedence, like other API clients: an explicit ``api_key=`` (callers apply it),
    then $DREAMSCALE_API_KEY, then `dreamscale login`'s saved key. The pre-rename
    $DROPBEAR_API_KEY is deliberately not read here: a stale one must not override a login.
    """
    return _with_rig_file(load_legacy_robot(env_key=_environment_api_key()))


def load_legacy_robot(*, env_key: str | None = None, path: Path | None = None) -> Config:
    """config.toml as written, without SO-101's rig file: the source a first so101.json
    is migrated from."""
    path = path or config_path()
    if env_key is None:
        env_key = _environment_api_key()
    if not path.exists():
        return Config(api_key=env_key, api_key_source=API_KEY_ENV if env_key else None)
    data = tomllib.loads(path.read_text())
    auth = data.get("auth", {})
    api = data.get("api", {})
    robot = data.get("robot", {})
    camera = data.get("camera", {})
    saved_key = auth.get("api_key") or None
    config = Config(
        api_key=env_key or saved_key,
        api_key_source=API_KEY_ENV if env_key else ("login" if saved_key else None),
        control_plane_url=_normalize_control_plane_url(api.get("control_plane_url")),
        preferred_region=api.get("preferred_region") or DEFAULT_REGION,
        robot_port=robot.get("port"),
        calibration_path=robot.get("calibration_path", default_calibration_path()),
        camera_index=camera.get("side_index", camera.get("index")),
        wrist_camera_index=camera.get("wrist_index"),
        home_position=robot.get("home"),
        integrations={
            name: dict(values)
            for name, values in data.get("integrations", {}).items()
            if isinstance(values, dict)
        },
        camera_codec=dict(data.get("camera_codec", {}) or {}),
    )
    return config


def dashboard_url(path: str, control_plane_url: str | None = None) -> str | None:
    """``path`` on the dashboard of the control plane the CLI talks to (the configured one by
    default), or None for one without a known dashboard, such as a local control plane."""
    url = _normalize_control_plane_url(control_plane_url or load_config().control_plane_url)
    origin = DASHBOARD_URLS.get(url)
    return f"{origin}{path}" if origin else None


def _normalize_control_plane_url(value: object) -> str:
    if value is None:
        return DEFAULT_CONTROL_PLANE_URL
    url = str(value).strip().rstrip("/")
    if not url or url in LEGACY_CONTROL_PLANE_URLS:
        return DEFAULT_CONTROL_PLANE_URL
    return url


def _environment_api_key() -> str | None:
    return os.environ.get(API_KEY_ENV, "").strip() or None


def saved_api_key() -> str | None:
    """The key `dreamscale login` saved in config.toml (never $DREAMSCALE_API_KEY)."""
    path = config_path()
    if not path.exists():
        return None
    return tomllib.loads(path.read_text()).get("auth", {}).get("api_key") or None


def _so101_rig_path() -> Path:
    from dreamscale.hardware.rig_file import rig_file_path

    return rig_file_path("so101")


def _with_rig_file(config: Config) -> Config:
    path = _so101_rig_path()
    if not path.exists():
        return config
    from dreamscale.hardware.so101_config import load_config as load_so101

    rig = load_so101(path)
    config.robot_port = rig.port
    if rig.calibration_path is not None:
        config.calibration_path = rig.calibration_path
    config.home_position = list(rig.home_pose) if rig.home_pose is not None else None
    config.camera_index = config.wrist_camera_index = None
    return config


def save_config(config: Config, *, save_api_key: bool = False) -> Path:
    """Write config.toml. A key that came from $DREAMSCALE_API_KEY is never written.

    When ``config.api_key`` is the environment's key, the key already saved by
    `dreamscale login` is kept as it is. ``save_api_key=True`` is for a key the user
    just gave explicitly (`dreamscale login`), which is saved even if it matches.
    """
    data: dict[str, dict[str, object]] = {}
    key = config.api_key
    env_key = _environment_api_key()
    if not save_api_key and env_key is not None and key == env_key:
        key = saved_api_key()
    if key is not None:
        data["auth"] = {"api_key": key}
    data["api"] = {
        "control_plane_url": config.control_plane_url,
        "preferred_region": config.preferred_region or DEFAULT_REGION,
    }
    robot: dict[str, object] = {}
    rig_path = _so101_rig_path()
    if rig_path.exists():
        # The rig file owns SO-101's port, calibration and home; config.toml keeps the
        # account. Cameras are set by setup, never by this Config.
        from dreamscale.hardware.so101_config import load_config as load_so101
        from dreamscale.hardware.so101_config import save_config as save_so101

        rig = load_so101(rig_path)
        rig.port = config.robot_port
        rig.calibration_path = config.calibration_path
        rig.home_pose = (
            tuple(float(v) for v in config.home_position)
            if config.home_position is not None else None
        )
        save_so101(rig, rig_path)
        config = replace(config, robot_port=None, calibration_path=default_calibration_path(),
                         camera_index=None, wrist_camera_index=None, home_position=None)
    if config.robot_port is not None:
        robot["port"] = config.robot_port
    if (
        config.robot_port is not None
        or config.calibration_path != default_calibration_path()
    ):
        robot["calibration_path"] = config.calibration_path
    if config.home_position is not None:
        robot["home"] = [float(value) for value in config.home_position]
    if robot:
        data["robot"] = robot
    camera: dict[str, object] = {}
    if config.camera_index is not None:
        camera["side_index"] = config.camera_index
    if config.wrist_camera_index is not None:
        camera["wrist_index"] = config.wrist_camera_index
    if camera:
        data["camera"] = camera
    integrations = {name: values for name, values in config.integrations.items() if values}
    if integrations:
        data["integrations"] = integrations
    if config.camera_codec:
        data["camera_codec"] = dict(config.camera_codec)
    return _atomic_write_toml(config_path(), data)


def _atomic_write_toml(path: Path, data: dict) -> Path:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".config-", suffix=".toml")
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            tomli_w.dump(data, handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        Path(tmp).unlink(missing_ok=True)
    return path
