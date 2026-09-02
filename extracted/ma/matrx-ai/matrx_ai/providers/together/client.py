from dotenv import load_dotenv
from together import AsyncTogether

from matrx_ai.providers.keys import resolve_api_key

load_dotenv()

# Keyed on the RESOLVED KEY VALUE so a host-side key rotation takes effect on
# the next request (a new key builds a new SDK client) without a process
# restart. One live key at a time — a rotation drops the stale client.
_clients: dict[str, AsyncTogether] = {}


def get_together_client() -> AsyncTogether:
    api_key = resolve_api_key("TOGETHER_API_KEY", required=True)
    client = _clients.get(api_key)
    if client is None:
        client = AsyncTogether(api_key=api_key)
        _clients.clear()
        _clients[api_key] = client
    return client
