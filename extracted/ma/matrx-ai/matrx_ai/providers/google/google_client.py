from dotenv import load_dotenv
from google import genai

from matrx_ai.providers.keys import resolve_api_key

load_dotenv()

# Keyed on the RESOLVED KEY VALUE so a host-side key rotation takes effect on
# the next request without a process restart. Dual-name resolution preserves
# the historical GEMINI_API_KEY / GOOGLE_API_KEY behavior.
_clients: dict[str, genai.Client] = {}


def google_client() -> genai.Client:
    """Un-memoized constructor (legacy call sites build a throwaway client)."""
    return genai.Client(
        api_key=resolve_api_key("GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_AI_STUDIO")
    )


def get_google_client() -> genai.Client:
    api_key = resolve_api_key(
        "GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_AI_STUDIO", required=True
    )
    client = _clients.get(api_key)
    if client is None:
        client = genai.Client(api_key=api_key)
        _clients.clear()
        _clients[api_key] = client
    return client
