"""Together speaks the OpenAI wire, so its client IS ``AsyncOpenAI`` at Together's hosts.

We do not depend on the ``together`` SDK: every call we make is plain JSON over
HTTPS, and that SDK caps ``filelock`` below the fixed release (CASA 6.1.1). Its
chat default was the inference host and everything else the API host; both are
kept here so the wire does not change.
"""

from dotenv import load_dotenv
from openai import AsyncOpenAI

from matrx_ai.providers.keys import resolve_api_key

load_dotenv()

TOGETHER_INFERENCE_BASE_URL = "https://api-inference.together.ai/v1"
TOGETHER_API_BASE_URL = "https://api.together.ai/v1"
TOGETHER_VIDEOS_URL = "https://api.together.ai/v2/videos"
#: Image and video calls wait this long; chat rides the capture client's own.
TOGETHER_MEDIA_TIMEOUT_FEATURE = "ai.media_providers"
TOGETHER_MEDIA_TIMEOUT_KEY = "together_media_timeout_seconds"
#: KNOB MIRROR of platform.feature_knob "ai.media_providers" "together_media_timeout_seconds"
TOGETHER_MEDIA_TIMEOUT_MIRROR = 60.0


def together_media_timeout_seconds() -> float:
    """How long a Together image or video call waits, live from the host knob (read when the SDK client is built)."""
    from matrx_ai.knobs import package_knob_number

    return package_knob_number(
        TOGETHER_MEDIA_TIMEOUT_FEATURE, TOGETHER_MEDIA_TIMEOUT_KEY, TOGETHER_MEDIA_TIMEOUT_MIRROR,
        low=5.0, high=600.0,
    )

# Keyed on the RESOLVED KEY VALUE so a host-side key rotation takes effect on
# the next request (a new key builds a new SDK client) without a process
# restart. One live key at a time — a rotation drops the stale client.
_clients: dict[str, AsyncOpenAI] = {}


def get_together_client() -> AsyncOpenAI:
    api_key = resolve_api_key("TOGETHER_API_KEY", required=True)
    client = _clients.get(api_key)
    if client is None:
        client = AsyncOpenAI(api_key=api_key, base_url=TOGETHER_API_BASE_URL)
        _clients.clear()
        _clients[api_key] = client
    return client
