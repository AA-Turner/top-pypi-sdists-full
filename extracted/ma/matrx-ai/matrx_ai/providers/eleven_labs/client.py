from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from matrx_ai.providers.keys import resolve_api_key

load_dotenv()

# Keyed on the RESOLVED KEY VALUE so a host-side key rotation takes effect on
# the next request without a process restart. Previously this module built the
# client AT IMPORT TIME with a raw os.getenv — both problems fixed here.
_clients: dict[str, ElevenLabs] = {}


def get_elevenlabs_client() -> ElevenLabs:
    api_key = resolve_api_key("ELEVENLABS_API_KEY", required=True)
    client = _clients.get(api_key)
    if client is None:
        client = ElevenLabs(api_key=api_key)
        _clients.clear()
        _clients[api_key] = client
    return client
