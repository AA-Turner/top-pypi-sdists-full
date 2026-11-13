"""
"""
import os
import time
import warnings
from datetime import timedelta
from typing import Any

import httpx
from typing_extensions import assert_never

from ..config import Config
from . import config
from . import context
from . import default_gpu_size
from . import utils
from .api import APIClient
from .api import GPUSize
from .api import AuthLevel
from .api import QuotaInfos
from .api import ScheduleResponse
from .context import ZeroGPUContext
from .errors import ZeroGPUClientError
from .errors import ZeroGPUIllegalDuration
from .errors import ZeroGPUPendingCreditsExceeded
from .errors import ZeroGPUQueueTimeout
from .errors import ZeroGPUQuotaExceeded


TOKEN_HEADER = 'X-IP-Token'
GRADIO_UI_HEADER = ('x-gradio-user', "app")
DEFAULT_SCHEDULE_DURATION = 60
PRO_QUOTA_MINUTES = 40  # TODO: Dynamic value from Spaces API

UNUSED_MESSAGE = "GPU device not used"
NO_GPU_MESSAGE_REGULAR = "No GPU was available"
NO_GPU_MESSAGE_INQUEUE = "No GPU was available after 60s"
EXAMPLES_RETRY_MESSAGE = "Try re-running outside of examples if it happened after clicking one"

SIGNUP_ON_HF_TXT = "Create a free account"
SIGNUP_ON_HF_URL = "https://huggingface.co/join"
SUBSCRIBE_TO_PRO_TXT = "Subscribe to Pro"
SUBSCRIBE_TO_PRO_URL = "https://huggingface.co/subscribe/pro?from=ZeroGPU"
TOKENS_SETTINGS_URL = "https://huggingface.co/settings/tokens"
ADD_CREDITS_URL = "https://huggingface.co/settings/billing?add-credits=true"


def api_client():
    assert Config.zero_device_api_url is not None
    httpx_client = httpx.Client(base_url=Config.zero_device_api_url, timeout=60, verify=False)
    return APIClient(httpx_client)


def startup_report():
    retries, max_retries = 0, 2
    client = api_client()
    while (status := client.startup_report()) is httpx.codes.NOT_FOUND: # pragma: no cover
        time.sleep(1)
        if (retries := retries + 1) > max_retries:
            raise RuntimeError("Error while initializing ZeroGPU: NotFound")
    if status is not httpx.codes.OK: # pragma: no cover
        raise RuntimeError("Error while initializing ZeroGPU: Unknown")


def _is_api_call(ctx: ZeroGPUContext) -> bool: # pragma: no cover
    name, value = GRADIO_UI_HEADER
    return ctx.headers.get(name) != value


def _toast_action(
    auth: AuthLevel | None,
    unlogged_desc: str,
    logged_desc: str,
    ending: str,
) -> str: # pragma: no cover
    html = ""
    link = SIGNUP_ON_HF_URL if auth is None else SUBSCRIBE_TO_PRO_URL
    text = SIGNUP_ON_HF_TXT if auth is None else SUBSCRIBE_TO_PRO_TXT
    desc = unlogged_desc if auth is None else logged_desc
    desc += f" {ending}."
    style = ";".join([
        "white-space: nowrap",
        "text-underline-offset: 2px",
        "color: var(--body-text-color)",
    ])
    html += f'<a style="{style}" href="{link}">'
    html += text
    html += '</a>'
    html += f" {desc}"
    return html


def get_duration_seconds(
    duration: timedelta | None,
    gpu_size: GPUSize | None,
):
    zerogpu_config = config.get_config()
    gpu_size = gpu_size if gpu_size is not None else default_gpu_size()
    duration_seconds = duration.seconds if duration is not None else DEFAULT_SCHEDULE_DURATION
    if gpu_size != 'xlarge':
        duration_seconds *= zerogpu_config['duration_factor']
    return duration_seconds


def schedule(
    task_id: int,
    duration: timedelta | None = None,
    gpu_size: GPUSize | None = None,
    _first_attempt: bool = True,
) -> ScheduleResponse:

    ctx = context.get()
    token, payload = _get_token_and_payload(ctx.headers)
    if token is not None and (token_error := payload.get('error')):
        message = f"Falling back to IP-based quotas ({token_error})"
        ctx.warning(
            title="ZeroGPU client warning",
            message=message,
        )

    duration_seconds = get_duration_seconds(duration, gpu_size)

    res, meta = api_client().schedule(
        cgroup_path=utils.self_cgroup_device_path(),
        task_id=task_id,
        token=token,
        token_version=2,
        duration_seconds=round(duration_seconds),
        gpu_size=gpu_size,
    )

    auth = meta.auth

    if isinstance(res, ScheduleResponse):
        return res

    if isinstance(res, QuotaInfos): # pragma: no cover
        requested = round(duration_seconds)
        requested *= 2 if gpu_size == 'xlarge' else 1
        if meta.approve_result == 'pending-overquota-exceeded':
            raise ZeroGPUPendingCreditsExceeded(
                "You have too many ZeroGPU credits allocated to running tasks. "
                "Try again once some of those tasks have completed."
            )
        if res.wait < timedelta(0):
            message = (
                f"The requested GPU duration ({requested}s) "
                f"is larger than the maximum allowed"
            )
            if _is_api_call(ctx):
                if auth is None or auth == 'regular':
                    message += ". "
                    message += (
                        f"Subscribe to Hugging Face PRO to allow GPU tasks up to {PRO_QUOTA_MINUTES} min - "
                        f"{SUBSCRIBE_TO_PRO_URL}"
                    )
            raise ZeroGPUIllegalDuration(message)
        if token is None:
            raise ZeroGPUQuotaExceeded(
                f"Space app has reached its GPU limit. "
                f"{EXAMPLES_RETRY_MESSAGE}"
            )
        else:
            if res.wait == timedelta(0):
                message = "You have exceeded your ZeroGPU runs limit"
            else:
                gpu = "Pro ZeroGPU" if auth == 'pro' else ("free ZeroGPU" if auth == 'regular' else "ZeroGPU")
                message = (
                    f"You have exceeded your {gpu} quota "
                    f"({requested}s requested vs. {res.left}s left). "
                    f"Try again in {res.wait}"
                )
            if _is_api_call(ctx):
                message += ". "
                match auth:
                    case None:
                        message += (
                            f"Authenticate with a Hugging Face token for more quota - "
                            f"{TOKENS_SETTINGS_URL}"
                        )
                    case 'regular':
                        message += (
                            f"Subscribe to Hugging Face PRO to get {PRO_QUOTA_MINUTES} min of ZeroGPU quota a day - "
                            f"{SUBSCRIBE_TO_PRO_URL}"
                        )
                    case 'pro':
                        message += (
                            f"Add credits to keep using ZeroGPU. "
                            f"$1 for 10 minutes of ZeroGPU inference - "
                            f"{ADD_CREDITS_URL}"
                        )
            raise ZeroGPUQuotaExceeded(message)

    if not isinstance(res, httpx.codes): # pragma: no cover
        if meta.queuing_reason in ('node', None):
            ctx.info(
                title="ZeroGPU queue",
                message="Waiting for a GPU to become available",
            )
        elif meta.queuing_reason == 'concurrency':
            ctx.info(
                title="ZeroGPU queue",
                message="Waiting for a GPU slot on this Space",
            )
        else:
            assert_never(meta.queuing_reason)
        while True:
            try:
                event = next(res)
            except StopIteration:
                raise RuntimeError("Unexpected end of stream")
            except httpx.RemoteProtocolError:
                if not _first_attempt:
                    raise RuntimeError("Error while re-trying after queue disconnect")
                return schedule(task_id, duration, _first_attempt=False)
            if event.event == 'ping':
                if ctx.disconnected():
                    res.close()
                    raise RuntimeError("Connection closed by visitor while queueing")
                continue
            if event.event == 'failed':
                if token is None:
                    message = f"{NO_GPU_MESSAGE_INQUEUE}. {EXAMPLES_RETRY_MESSAGE}"
                else:
                    match (_is_api_call(ctx), auth):
                        case (True, None):
                            details = (
                                "Authenticate with a Hugging Face token to get a higher priority in ZeroGPU queues - "
                                f"{TOKENS_SETTINGS_URL}"
                            )
                        case (True, 'regular'):
                            details = (
                                "Subscribe to Hugging Face PRO to get the highest priority in ZeroGPU queues - "
                                f"{SUBSCRIBE_TO_PRO_URL}"
                            )
                        case (False, None | 'regular'):
                            details = _toast_action(
                                auth=auth,
                                unlogged_desc="to get a higher",
                                logged_desc="to get the highest",
                                ending="priority in ZeroGPU queues",
                            )
                        case (_, 'pro'):
                            details = "Retry later"
                    message = f"{NO_GPU_MESSAGE_INQUEUE}. {details}"
                raise ZeroGPUQueueTimeout(message)
            if event.event == 'succeeded':
                assert event.data is not None
                if ctx.disconnected():
                    release(event.data.allowToken)
                    raise RuntimeError("Connection closed by visitor on queue success")
                ctx.success(
                    title="ZeroGPU queue",
                    message="Successfully acquired a GPU",
                )
                return event.data

    if res is httpx.codes.SERVICE_UNAVAILABLE:
        message = NO_GPU_MESSAGE_REGULAR
    elif res is httpx.codes.UNAUTHORIZED: # pragma: no cover
        message = "Expired ZeroGPU proxy token"
    else: # pragma: no cover
        raise RuntimeError(f"ZeroGPU API /schedule error: {res} ({httpx.codes.get_reason_phrase(res)})")

    raise ZeroGPUClientError(message)


def allow(allow_token: str) -> None:
    pid = os.getpid()
    assert pid != 1, "Allowing PID 1 on ZeroGPU will end up killing your Space"
    assert api_client().allow(allow_token=allow_token, pid=pid) is httpx.codes.OK


def release(
    allow_token: str, *,
    fail: bool = False,
    allow_404: bool = False,
) -> None:

    ctx = context.get()
    res = api_client().release(
        allow_token=allow_token,
        fail=fail,
    )

    if res is httpx.codes.NO_CONTENT: # pragma: no cover
        try:
            ctx.warning(
                title="ZeroGPU client warning",
                message=UNUSED_MESSAGE,
            )
        except AttributeError:
            pass
        warnings.warn(UNUSED_MESSAGE, RuntimeWarning)
        return None

    if res is httpx.codes.NOT_FOUND:
        if not allow_404:
            warnings.warn("ZeroGPU API /release warning: 404 Not Found")
        return None

    if httpx.codes.is_success(res):
        return None

    raise RuntimeError(f"ZeroGPU API /release error: {res} ({httpx.codes.get_reason_phrase(res)})") # pragma: no cover


def _get_token_and_payload(headers: dict[str, str]) -> tuple[str | None, dict[str, Any]]:
    if (token := headers.get(TOKEN_HEADER.lower())) is None:
        return None, {}
    try:
        payload = utils.jwt_payload(token)
    except Exception: # pragma: no cover
        warnings.warn("Error while decoding X-IP-Token JWT")
        return token, {}
    return token, payload


def duration_warning():
    context.get().warning(
        title="ZeroGPU duration",
        message="GPU task is exceeding its requested duration and might be aborted",
    )
