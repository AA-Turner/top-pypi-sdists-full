from dotenv import load_dotenv
from groq import AsyncGroq

from matrx_ai.providers.keys import resolve_api_key

load_dotenv()

# Keyed on the RESOLVED KEY VALUE so a host-side key rotation takes effect on
# the next request (a new key builds a new SDK client) without a process
# restart. One live key at a time — a rotation drops the stale client.
_clients: dict[str, AsyncGroq] = {}


def get_groq_client() -> AsyncGroq:
    api_key = resolve_api_key("GROQ_API_KEY", required=True)
    client = _clients.get(api_key)
    if client is None:
        client = AsyncGroq(api_key=api_key)
        _clients.clear()
        _clients[api_key] = client
    return client
