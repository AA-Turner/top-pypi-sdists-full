"""Actionable error catalog (spec §8). Every error renders problem+cause+fix; the
fix names the command to run when there is one.

Server `failed`-status payloads are rendered VERBATIM (master contract) via
from_payload(); the catalog covers client-side conditions.
"""

from __future__ import annotations

import platform
from dataclasses import dataclass
from pathlib import Path

from dreamscale import __version__
from dreamscale.config import config_path
from dreamscale.model_names import public_model

COMMAND_LOGIN = "dreamscale login"
COMMAND_LOGOUT = "dreamscale auth logout"
COMMAND_WHOAMI = "dreamscale auth whoami"
COMMAND_QUICKSTART = "dreamscale robots so101 setup"
COMMAND_DOCTOR = "dreamscale doctor"
# Points at the server-filtered list instead of naming models, so unreleased ones stay hidden.
SEE_MODELS = "See the models your organization can run: dreamscale models list"
COMMAND_SIM = (
    "dreamscale sim libero --model molmoact2-libero --task-suite libero_spatial --task-id 0"
)
COMMAND_CALIBRATE = "dreamscale robots so101 calibrate"
COMMAND_HOME = "dreamscale robots so101 home"
COMMAND_RELEASE = "dreamscale robots so101 release"
INSTALL_SIM = f'uv pip install "dreamscale[sim]=={__version__}"'
INSTALL_SO101 = f'uv pip install "dreamscale[so101]=={__version__}"'
# The one place that says how to get credits. There is no self-serve top-up today; when a
# page exists, only this constant changes.
CREDITS_FIX = "Email team@dreamscalelabs.com to add credits"
# The server's 426 carries a generic pip hint; the SDK renders the command for how it was
# installed instead (uv tool, a project venv, or pip).
SDK_UPGRADE_REQUIRED = "sdk_upgrade_required"


@dataclass(frozen=True)
class ErrorInfo:
    code: str
    problem: str
    cause: str
    fix: str

    def render(self) -> str:
        return f"✗ {self.problem}\n  cause: {self.cause}\n  fix:   {self.fix}"


class DreamscaleError(Exception):
    """Base of every SDK error: ``.code`` names the problem, ``.fix`` the next step."""

    def __init__(self, info: ErrorInfo) -> None:
        super().__init__(info.problem)
        self.info = info

    @property
    def code(self) -> str:
        return self.info.code

    @property
    def fix(self) -> str:
        return self.info.fix

    def render(self) -> str:
        return self.info.render()


# The pre-rename name (stage-b: keep): `except DropbearError` still catches every SDK error.
DropbearError = DreamscaleError  # stage-b: keep


class CapacityError(DreamscaleError):
    """No server for this request right now: the pool is full or queued out, or your
    organization already runs its share of robots (``shared_session_limit``)."""


# The public name for the same condition.
NoCapacityError = CapacityError


class AuthError(DreamscaleError):
    """No usable API key: not signed in, or the key was rejected."""


class CreditsError(DreamscaleError):
    """The organization is out of credits."""


class ObservationError(DreamscaleError, ValueError, TypeError):
    """An observation does not match the model's contract. Raised before any network call;
    also a ``ValueError``/``TypeError`` so older handlers keep working."""


class ServerError(DreamscaleError):
    """The control plane answered with an unexpected HTTP status (``.status``)."""

    status: int = 0


class SessionExpiredError(DreamscaleError):
    pass


class ConnectionLostError(DreamscaleError):
    pass


class DeploymentInUseError(DreamscaleError):
    """A π0.5 deployment on a dedicated server (not autoscaling) serves one robot at a time,
    and another session holds it (``.session_id`` when the server names it)."""

    session_id: str | None = None


# Server and catalog codes that users branch on, mapped to their typed subclass.
_TYPED_CODES: dict[str, type[DreamscaleError]] = {
    "capacity_exhausted": CapacityError,
    "shared_session_limit": CapacityError,
    "deployment_capacity_unavailable": CapacityError,
    "insufficient_credits": CreditsError,
    "quota_exhausted": CreditsError,
    "invalid_api_key": AuthError,
    "not_configured": AuthError,
    "session_expired": SessionExpiredError,
    "connection_lost": ConnectionLostError,
    "deployment_in_use": DeploymentInUseError,
    "typed_observation_required": ObservationError,
}


def _typed(info: ErrorInfo) -> DreamscaleError:
    cls = _TYPED_CODES.get(info.code)
    if cls is None and ("capacity" in info.code.lower() or "capacity" in info.cause.lower()):
        cls = CapacityError
    return (cls or DreamscaleError)(info)


def from_payload(payload: dict) -> DreamscaleError:
    err = payload.get("error", payload) or {}
    info = ErrorInfo(
        code=str(err.get("code", "unknown")),
        problem=str(err.get("problem", "the request failed")),
        cause=str(err.get("cause", "unknown")),
        fix=str(err.get("fix", "retry")),
    )
    if info.code == SDK_UPGRADE_REQUIRED:
        info = ErrorInfo(info.code, info.problem, info.cause, _sdk_upgrade_fix())
    return _typed(info)


def _sdk_upgrade_fix() -> str:
    """The upgrade command for how this SDK was installed (same rule as update_check)."""
    import os
    import sys

    if "uv/tools/" in sys.prefix.replace("\\", "/"):
        from dreamscale.update_check import _exact_pin_reinstall

        command = _exact_pin_reinstall() or "uv tool upgrade dreamscale"
    elif sys.prefix != sys.base_prefix or "VIRTUAL_ENV" in os.environ:
        command = "uv add dreamscale@latest"
    else:
        command = "pip install -U dreamscale"
    return f"upgrade with `{command}` and rerun"


def server_error(
    *,
    status: int,
    request_id: str | None = None,
    server_code: str | None = None,
    detail: str | None = None,
) -> ServerError:
    cause = f"the control plane answered HTTP {status}"
    if server_code:
        cause += f" ({server_code}{': ' + detail if detail else ''})"
    if request_id:
        cause += f" (request id {request_id})"
    err = ServerError(
        ErrorInfo(
            code="server_error",
            problem=f"Dreamscale returned an error (HTTP {status})",
            cause=cause,
            fix="try again in a minute; if it keeps happening, email team@dreamscalelabs.com"
            + (f" with request id {request_id}" if request_id else ""),
        )
    )
    err.status = int(status)
    return err


def observation_error(field: str, given: str, expected: str) -> ObservationError:
    """``field`` is ``given``; expected ``expected``. The one shape for every observation
    check, so a message always names the field, what was passed and what the model wants."""
    return ObservationError(
        ErrorInfo(
            code="invalid_observation",
            problem=f"`{field}` is {given}; expected {expected}",
            cause="the observation does not match the model's contract",
            fix=f"build `{field}` as {expected} before calling the policy",
        )
    )


def _serial_fix(system: str) -> str:
    if system == "Linux":
        return (
            "add yourself to the dialout group: `sudo usermod -aG dialout $USER`, "
            "then log out and back in"
        )
    if system == "Darwin":
        return (
            "close any app holding the port; if the device never appears, install the "
            "CH340/CP210x USB-serial driver and re-plug the arm"
        )
    return "close any app holding the COM port and check the driver in Device Manager"


def _then_rerun(fix: str, command: str | None) -> str:
    return f"{fix}, then rerun `{command}`" if command else fix


def _display_path(path) -> str:
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)


def _default_base_names() -> dict[str, str]:
    """The default deployment base's label and `--base` name."""
    from dreamscale import deploy_bases

    base = deploy_bases.default()
    return {"base_label": base.label, "base_flag": base.listed_as}


def catalog(code: str, **kwargs) -> DreamscaleError:
    dashboard = "https://app.dreamscalelabs.com"
    system = kwargs.get("system") or platform.system()
    eta_s = kwargs.get("eta_s")
    eta = f" (~{eta_s}s)" if eta_s else " (startup time varies)"
    model = kwargs.get("model", "that model")
    # deployment_required: the deployments-only base the session named (default: the default
    # deployment base, read from the registry only when it is needed).
    if code == "deployment_required" and not {"base_label", "base_flag"} <= kwargs.keys():
        kwargs = {**_default_base_names(), **kwargs}
    base_label = kwargs.get("base_label")
    base_flag = kwargs.get("base_flag")
    hint = kwargs.get("hint", "see the Models page for live models")
    port = kwargs.get("port", "the configured port")
    index = kwargs.get("index", "the configured index")
    remediation = kwargs.get(
        "remediation",
        "switch networks (a phone hotspot works) — corporate/uni Wi-Fi often drops UDP",
    )
    detail = kwargs.get("detail", "")
    retry_command = kwargs.get("retry_command")
    python_version = kwargs.get("python_version", platform.python_version())
    label = kwargs.get("label", "hardware")
    command = kwargs.get("command", INSTALL_SO101)
    supported = kwargs.get("supported", "a different Python version")
    kind = kwargs.get("kind", "train_time")
    keys_page = f"{dashboard}/dashboard/keys"
    key_source = kwargs.get("key_source")
    session_id = kwargs.get("session_id")
    run_id = kwargs.get("run_id", "with that ID")
    # history_required: what the call left out, and what to pass instead.
    missing = kwargs.get("missing", "its action history")
    wanted = kwargs.get("wanted", "action_history (the actions the robot executed)")
    # typed_observation_required: the robot helper (dreamscale.<helper>) the model reads.
    helper = kwargs.get("helper", "<robot>")

    infos: dict[str, ErrorInfo] = {
        "not_configured": ErrorInfo(
            code="not_configured",
            problem="Dreamscale is not set up on this machine yet",
            cause=f"{_display_path(config_path())} has no API key and DREAMSCALE_API_KEY "
            "is not set",
            fix=f"sign in once with `{COMMAND_LOGIN}`; on a machine without a browser, set "
            f"DREAMSCALE_API_KEY to a key from {keys_page}",
        ),
        "python_version_unsupported": ErrorInfo(
            code="python_version_unsupported",
            problem=f"Python {python_version} is not supported",
            cause="this Dreamscale alpha supports Python 3.11 through 3.14",
            fix=f"use a Python version in the supported range `>=3.11,<3.15`, then rerun "
            f"`{COMMAND_DOCTOR}`",
        ),
        "dependency_pin_mismatch": ErrorInfo(
            code="dependency_pin_mismatch",
            problem="an installed dependency does not match dreamscale's tested pin",
            cause=detail or "the SO-101 environment drifted from Dreamscale's tested pins",
            fix=f"run `{COMMAND_QUICKSTART}`; it reinstalls the tested versions",
        ),
        "so101_not_installed": ErrorInfo(
            code="so101_not_installed",
            problem="SO-101 support is not installed",
            cause="the lean Dreamscale base install does not include LeRobot or Feetech drivers",
            fix=f"run `{COMMAND_QUICKSTART}`; it installs SO-101 support first",
        ),
        "so101_not_set_up": ErrorInfo(
            code="so101_not_set_up",
            problem="this SO-101 is not set up",
            cause="its serial port and side and wrist cameras are not saved yet",
            fix=f"choose the port and both cameras with `{COMMAND_QUICKSTART}`",
        ),
        "so101_home_not_set": ErrorInfo(
            code="so101_home_not_set",
            problem="no SO-101 home pose is saved",
            cause=detail or "home moves the arm to a pose you record once",
            fix="pose the arm by hand where it can rest with motors off, and save it with "
            f"`{COMMAND_HOME} --set`",
        ),
        "so101_home_not_reached": ErrorInfo(
            code="so101_home_not_reached",
            problem="the SO-101 stopped short of its home pose",
            cause=detail or "a joint is blocked or carrying a load",
            fix="the arm is still holding its pose; support it, then release the motors with "
            f"`{COMMAND_RELEASE}`",
        ),
        "so101_wrist_seam": ErrorInfo(
            code="so101_wrist_seam",
            problem="homing would spin the wrist the long way round",
            cause=detail or "the wrist and its home are on opposite sides of the ±180° seam",
            fix=(f"turn the wrist by hand to its home angle and rerun `{COMMAND_HOME}`, or set "
                 f"a home with the wrist nearer its middle (`{COMMAND_HOME} --set`)"),
        ),
        "so101_servo_runaway": ErrorInfo(
            code="so101_servo_runaway",
            problem=f"the {detail or 'SO-101'} servo drives away from its target",
            cause="its position control latched a fault that a mode reset did not clear",
            fix=_then_rerun(
                "that motor is limp and the others are holding; support the arm, then "
                "switch the arm's power off for a few seconds and back on",
                retry_command,
            ),
        ),
        "extra_install_failed": ErrorInfo(
            code="extra_install_failed",
            problem=f"could not install {label} support",
            cause=detail or "the package installer exited with an error",
            fix=_then_rerun(f"install it yourself with `{command}`", retry_command),
        ),
        "extra_python_unsupported": ErrorInfo(
            code="extra_python_unsupported",
            problem=f"{label} support does not run on Python {python_version}",
            cause=f"its drivers support {supported}",
            fix=_then_rerun(
                f"install Dreamscale with a supported Python: `{command}`", retry_command
            ),
        ),
        "udp_blocked": ErrorInfo(
            code="udp_blocked",
            problem="outbound UDP to the server is blocked",
            cause="the data plane runs QUIC over UDP and this network drops it",
            fix=_then_rerun(remediation, COMMAND_DOCTOR),
        ),
        "data_plane_unreachable": ErrorInfo(
            code="data_plane_unreachable",
            problem="the server's data plane did not respond",
            cause="the primary QUIC/UDP data plane could not be reached",
            fix=_then_rerun(remediation, COMMAND_DOCTOR),
        ),
        "relay_unavailable": ErrorInfo(
            code="relay_unavailable",
            problem="TCP fallback is not available for this session",
            cause=detail or "the relay service is disabled or the assigned worker is not connected",
            fix="try again in a few minutes, or require QUIC only from a UDP-capable network",
        ),
        "worker_starting": ErrorInfo(
            code="worker_starting",
            problem=f"the server is still starting{eta}",
            cause="servers stop when idle and start on demand",
            fix="nothing to do — this command waits and shows progress",
        ),
        "start_failed": ErrorInfo(
            code="start_failed",
            problem="the server failed to start",
            cause=detail or "instance start or model load did not complete in time",
            fix="retry in a few minutes",
        ),
        "invalid_api_key": ErrorInfo(
            code="invalid_api_key",
            problem=(
                "the API key in DREAMSCALE_API_KEY was rejected"
                if key_source == "DREAMSCALE_API_KEY"
                else "your API key was rejected"
            ),
            cause=(
                "the key belongs to an organization you are no longer in"
                if kwargs.get("other_organization")
                else "the key is invalid or has been revoked"
            ),
            fix=(
                f"set DREAMSCALE_API_KEY to a current key from {keys_page}, or unset it to use "
                f"your `{COMMAND_LOGIN}`"
                if key_source == "DREAMSCALE_API_KEY"
                else f"sign in again with `{COMMAND_LOGIN}` to create a fresh local key"
            ),
        ),
        "cli_login_expired": ErrorInfo(
            code="cli_login_expired",
            problem="browser login expired",
            cause="the CLI approval link was not completed in time",
            fix=f"run `{COMMAND_LOGIN}` again and approve the new browser prompt",
        ),
        "cli_login_failed": ErrorInfo(
            code="cli_login_failed",
            problem="browser login failed",
            cause=detail or "the CLI auth request could not be completed",
            fix=f"rerun `{COMMAND_LOGIN}`, or create an API key at {keys_page} "
            f"and save it with `{COMMAND_LOGIN} --api-key`",
        ),
        "cli_login_start_failed": ErrorInfo(
            code="cli_login_start_failed",
            problem="browser login could not start",
            cause=detail or "the CLI could not create a browser approval request",
            fix=_then_rerun("check this machine's internet connection", COMMAND_LOGIN),
        ),
        "cli_login_poll_failed": ErrorInfo(
            code="cli_login_poll_failed",
            problem="browser login lost its connection while waiting",
            cause=detail or "the CLI could not retrieve the browser approval",
            fix=_then_rerun("check this machine's internet connection", COMMAND_LOGIN),
        ),
        "cli_logout_failed": ErrorInfo(
            code="cli_logout_failed",
            problem="sign-out could not reach Dreamscale",
            cause=detail or "the login key could not be revoked, so it is still saved",
            fix=_then_rerun("check this machine's internet connection", COMMAND_LOGOUT),
        ),
        "cli_whoami_failed": ErrorInfo(
            code="cli_whoami_failed",
            problem="could not look up your account",
            cause=detail or "the login service could not be reached",
            fix=_then_rerun("check this machine's internet connection", COMMAND_WHOAMI),
        ),
        "cli_login_protocol_failed": ErrorInfo(
            code="cli_login_protocol_failed",
            problem="browser login received an invalid response",
            cause=detail or "the login service response did not match the SDK contract",
            fix=_then_rerun("upgrade Dreamscale if an update is available", COMMAND_LOGIN),
        ),
        "unknown_model": ErrorInfo(
            code="unknown_model",
            problem=f"{public_model(model)} is not a live model",
            cause="the model id is unknown or not yet serving",
            fix=f"{hint} ({dashboard}/dashboard/models)",
        ),
        "rate_limited": ErrorInfo(
            code="rate_limited",
            problem="too many session creates — slowed down for a minute",
            cause="session creation is rate-limited per user (abuse guard)",
            fix="wait ~1 minute; reuse one session per run instead of re-creating",
        ),
        "invalid_region": ErrorInfo(
            code="invalid_region",
            problem=f"{kwargs.get('region', 'that region')} is not a supported Dreamscale region",
            cause="the region isn't live, or this model isn't offered there",
            fix=f"use one of: {kwargs.get('allowed', 'auto, available')}",
        ),
        "calibration_mismatch": ErrorInfo(
            code="calibration_mismatch",
            problem="the arm calibration file is missing or in the wrong format",
            cause=detail or (
                "lerobot 0.6.1 expects the v3.0 calibration format; a v2.1 file (or none) "
                "was found"
            ),
            fix=f"recalibrate with `{COMMAND_CALIBRATE}` — it takes ~2 minutes, guided",
        ),
        "camera_pair_not_configured": ErrorInfo(
            code="camera_pair_not_configured",
            problem="the side and wrist cameras are not both configured",
            cause="molmoact2-so101 needs two camera streams: side_cam and wrist_cam",
            fix=f"run `{COMMAND_QUICKSTART}` and pick both cameras with preview",
        ),
        "camera_missing": ErrorInfo(
            code="camera_missing",
            problem=f"no camera found at index {index}",
            cause="the webcam is unplugged or the index changed",
            fix=f"plug the camera in, or re-pick it with preview: `{COMMAND_QUICKSTART}`",
        ),
        "camera_busy": ErrorInfo(
            code="camera_busy",
            problem=f"the camera at index {index} is busy",
            cause="another app (Zoom, a browser tab, OBS) is holding the camera",
            fix=_then_rerun("quit the other app", retry_command),
        ),
        "robot_port_not_found": ErrorInfo(
            code="robot_port_not_found",
            problem=f"no robot found at {port}",
            cause="the arm is unplugged, off, or enumerated on a different port",
            fix="check the USB cable and the arm's power supply, or re-detect the port with "
            f"`{COMMAND_QUICKSTART}`",
        ),
        "serial_permission_denied": ErrorInfo(
            code="serial_permission_denied",
            problem=f"permission denied opening {port}",
            cause="your OS user cannot open the serial device",
            fix=_then_rerun(_serial_fix(system), retry_command),
        ),
        "connection_lost": ErrorInfo(
            code="connection_lost",
            problem="arm frozen safely — connection lost",
            cause=(
                "no fresh actions arrived before the startup wait expired, or the live "
                "action stream stopped; stale buffered actions older than 1.0s are "
                "discarded and the arm holds position (this freeze is deliberate)"
            ),
            fix="reconnecting automatically…",
        ),
        "cert_fingerprint_mismatch": ErrorInfo(
            code="cert_fingerprint_mismatch",
            problem="worker TLS fingerprint mismatch — connection refused",
            cause=(
                "the worker presented a certificate that does not match the fingerprint "
                "issued for this session; this can indicate interception"
            ),
            fix=f"do not reconnect on this network; report this at {dashboard} and rotate "
            "your API key",
        ),
        "deployments_unavailable": ErrorInfo(
            code="deployments_unavailable",
            problem="this Dreamscale server does not have deployments yet",
            cause="the control plane predates deployments",
            fix=f"create the deployment at {dashboard}/dashboard/deployments, or retry later",
        ),
        "deployment_region_unavailable": ErrorInfo(
            code="deployment_region_unavailable",
            problem="this Dreamscale server can only create deployments in us-west",
            cause="the control plane predates deployment regions",
            fix="create it in us-west (the default) without --region, or retry later",
        ),
        "deployment_keep_warm_unavailable": ErrorInfo(
            code="deployment_keep_warm_unavailable",
            problem="this Dreamscale server cannot keep deployments warm yet",
            cause="the control plane predates deployment keep-warm",
            fix="retry later, or pass keep_warm= to connect() for this session only",
        ),
        "region_fallback_unavailable": ErrorInfo(
            code="region_fallback_unavailable",
            problem="this Dreamscale server can't set a deployment's region fallback yet",
            cause="the control plane predates region fallback",
            fix="leave --region-fallback/--no-region-fallback out for now, or retry later",
        ),
        "deployment_rename_unavailable": ErrorInfo(
            code="deployment_rename_unavailable",
            problem="this Dreamscale server cannot rename deployments yet",
            cause="the control plane predates renaming deployments",
            fix="retry later",
        ),
        "pi05_deployments_unavailable": ErrorInfo(
            code="pi05_deployments_unavailable",
            problem="π0.5 deployments are not available on this Dreamscale server yet",
            cause="the control plane predates π0.5 deployments, or does not run them for "
            "your organization yet",
            fix="retry later, or email team@dreamscalelabs.com to turn them on",
        ),
        "local_folders_unavailable": ErrorInfo(
            code="local_folders_unavailable",
            problem="deploying a local folder is not available on this Dreamscale server yet",
            cause="the control plane predates local folders, or doesn't offer them here",
            fix="push the checkpoint to Hugging Face and deploy hf://owner/name, or retry later",
        ),
        "deployment_required": ErrorInfo(
            code="deployment_required",
            problem=f"{base_label} runs your own fine-tune: name its deployment",
            cause=f"the {base_label} base has no shared weights to run on their own",
            fix='pass deployment="ckpt_…" (see `dreamscale deployments list`), or create one '
            f"with `dreamscale deployments create hf://owner/repo --base {base_flag}`",
        ),
        "deployment_in_use": ErrorInfo(
            code="deployment_in_use",
            problem=detail or "this deployment is already running a robot",
            cause="this deployment serves one robot at a time",
            fix=(
                f"stop that session with `dreamscale sessions stop {session_id}`, then "
                "connect again"
                if session_id
                else "stop the other session (`dreamscale sessions list`, then "
                "`dreamscale sessions stop <id>`), then connect again"
            ),
        ),
        SDK_UPGRADE_REQUIRED: ErrorInfo(
            code=SDK_UPGRADE_REQUIRED,
            problem=f"{public_model(model)} needs a newer Dreamscale SDK",
            cause=f"this SDK ({__version__}) can't run what the server requires for this session",
            fix=_sdk_upgrade_fix() if code == SDK_UPGRADE_REQUIRED else "",
        ),
        "training_unavailable": ErrorInfo(
            code="training_unavailable",
            problem="Training isn't available for your organization",
            cause="this Dreamscale server doesn't run training runs for your organization",
            fix="email team@dreamscalelabs.com to ask for access",
        ),
        "datasets_unavailable": ErrorInfo(
            code="datasets_unavailable",
            problem="Datasets aren't available yet",
            cause="this Dreamscale server doesn't keep datasets yet",
            fix="try again in a few minutes; if it keeps failing, email team@dreamscalelabs.com",
        ),
        "upload_dataset_first": ErrorInfo(
            code="upload_dataset_first",
            problem="dreamscale train takes --dataset and --base, and a folder must be uploaded "
            "first",
            cause=f"{kwargs.get('folder', 'that')} is a folder here; a run reads a dataset kept "
            "on Dreamscale, or on Hugging Face",
            fix=f"dreamscale datasets upload {kwargs.get('folder', './folder')}, then dreamscale "
            f"train --dataset {kwargs.get('name', 'NAME')} --base BASE",
        ),
        "base_required": ErrorInfo(
            code="base_required",
            problem="choose a base model with --base",
            cause="a run has no default base",
            fix=f"--base {kwargs.get('bases') or 'BASE'} (what your organization can start "
            "from), or one of your runs (tr_…)",
        ),
        "dataset_required": ErrorInfo(
            code="dataset_required",
            problem="name the dataset to train on with --dataset",
            cause="a run reads a dataset kept on Dreamscale, or on Hugging Face",
            fix="--dataset towels (dreamscale datasets list shows yours) or "
            "--dataset hf://owner/name",
        ),
        "training_run_not_found": ErrorInfo(
            code="training_run_not_found",
            problem=f"no training run {run_id} in your organization",
            cause="the ID is mistyped, belongs to another organization, or training isn't "
            "available for your organization",
            fix="see your runs with `dreamscale train list`",
        ),
        "training_credits_required": ErrorInfo(
            code="training_credits_required",
            problem=detail or "your balance is too low to start training",
            cause="credits are taken as a run trains, and it needs about ten minutes' worth to "
            "start; nothing was charged",
            fix=(kwargs.get("amount_fix") or "add credits").rstrip(". ")
            + f" at {dashboard}/dashboard/usage, then rerun the same command",
        ),
        "train_not_installed": ErrorInfo(
            code="train_not_installed",
            problem="reading a local dataset needs pyarrow",
            cause="the lean Dreamscale install doesn't read Parquet files",
            fix=f'install it with `uv pip install "dreamscale[train]=={__version__}"` (or '
            "`pip install`), then retry",
        ),
        "rtc_kind_unavailable": ErrorInfo(
            code="rtc_kind_unavailable",
            problem=f"this Dreamscale server cannot run --rtc {kind} yet",
            cause="the control plane predates choosing train_time or inference_time RTC",
            fix="rerun with --rtc on (the model's own RTC) or --rtc auto, or retry later",
        ),
        "hugging_face_connect_unavailable": ErrorInfo(
            code="hugging_face_connect_unavailable",
            problem="this Dreamscale server can't keep a Hugging Face token yet",
            cause="the control plane predates connecting Hugging Face",
            fix="pass --hf-token (or set HF_TOKEN) when you deploy or train from a private repo",
        ),
        "models_unavailable": ErrorInfo(
            code="models_unavailable",
            problem="this Dreamscale server cannot list models yet",
            cause="the control plane predates the models list",
            fix=f"see the models your organization can run at {dashboard}/dashboard/models",
        ),
        "session_expired": ErrorInfo(
            code="session_expired",
            problem="this session has expired or was closed",
            cause="the 60s lease lapsed (no polls/heartbeats) or the key was revoked",
            fix="start a fresh session — it is one command",
        ),
        "sim_not_installed": ErrorInfo(
            code="sim_not_installed",
            problem="the simulation extra is not installed",
            cause="the sim command needs MuJoCo, robosuite, and LIBERO support packages",
            fix=f"install the matching simulator extra: `{INSTALL_SIM}`",
        ),
        "insufficient_credits": ErrorInfo(
            code="insufficient_credits",
            problem="you are out of credits",
            cause="your prepaid balance reached zero",
            fix=CREDITS_FIX,
        ),
        "committed_actions_unsupported": ErrorInfo(
            code="committed_actions_unsupported",
            problem=f"{public_model(model)} doesn't start chunks with committed actions",
            cause=f"its real-time chunking is {kind}; committed_actions needs RTC that takes "
            "them (policy.contract.max_prefix_rows above 0)",
            fix=(
                "call predict() without committed_actions, or turn the deployment's RTC on: "
                "dreamscale deployments rtc <deployment> test-time (π0.5), or trained for a "
                "checkpoint trained with RTC"
                if kwargs.get("deployment")
                else "call predict() without committed_actions, or connect with rtc=\"on\" "
                "where the model trained with RTC (policy.contract.rtc \"train_time\")"
            ),
        ),
        "history_required": ErrorInfo(
            code="history_required",
            problem=f"{public_model(model)} reads the robot's recent history",
            cause=f"predict() was called without {missing}",
            fix=f"pass {wanted}, oldest first (policy.contract says how many; [] at an "
            "episode's start, which the SDK pads), or use next_action(), which keeps them for "
            "you",
        ),
        "typed_observation_required": ErrorInfo(
            code="typed_observation_required",
            problem=f"{public_model(model)} can't read a dreamscale.robot observation",
            cause=f"it reads a dreamscale.{helper} observation (its robot's cameras and typed "
            "state); dreamscale.robot sends one plain state vector, for deployments and LeRobot "
            "checkpoints",
            fix=f"build it with dreamscale.{helper}.observation(...)",
        ),
        "past_observations_unsupported": ErrorInfo(
            code="past_observations_unsupported",
            problem=f"predict() can't send {public_model(model)}'s history",
            cause="it also reads the first frame of the episode, which past_observations "
            "(the ticks just before this one) doesn't carry",
            fix="call predict() without past_observations, or use next_action(), which keeps "
            "the episode's frames for you",
        ),
        "forked_policy": ErrorInfo(
            code="forked_policy",
            problem="this policy was created in another process",
            cause="a connected policy holds a live session and event loop that do not "
            "survive fork()",
            fix="create the policy inside the worker process (call dreamscale.connect() "
            "there)",
        ),
        "policy_closed": ErrorInfo(
            code="policy_closed",
            problem="this policy is closed",
            cause=detail or "close() was called, or the connection failed and was not "
            "reopened",
            fix="call dreamscale.connect() again for a new session",
        ),
        "action_timeout": ErrorInfo(
            code="action_timeout",
            problem=f"no action arrived within {detail or 'the timeout'}",
            cause="the model did not answer in time, or the connection could not be "
            "restored",
            fix="check your network and the Models page, then call dreamscale.connect() "
            "again",
        ),
        "gpu_unreachable": ErrorInfo(
            code="gpu_unreachable",
            problem="could not reach a server for this session",
            cause=detail or "three attempts to open a session failed in a row",
            fix="check your network and `dreamscale models list`, then try again",
        ),
        "reconnect_failed": ErrorInfo(
            code="reconnect_failed",
            problem="the connection to the server was lost and could not be restored",
            cause=detail or "three reconnect attempts failed in a row",
            fix="check your network, then call dreamscale.connect() again",
        ),
        "idle_timeout": ErrorInfo(
            code="idle_timeout",
            problem="the session ended after being idle",
            cause="no inference ran before the idle timeout, so the session auto-terminated",
            fix="call connect again to start a fresh session",
        ),
    }
    # The pre-rename code (SDK 0.1.0a80-a95) for the same condition.
    infos["endpoints_unavailable"] = infos["deployments_unavailable"]
    info = infos[code]
    if code == "deployment_in_use":
        error = DeploymentInUseError(info)
        error.session_id = session_id
        return error
    if code == "start_failed":
        if "capacity" in (detail or "").lower():
            return CapacityError(info)
        return DreamscaleError(info)
    return _typed(info)
