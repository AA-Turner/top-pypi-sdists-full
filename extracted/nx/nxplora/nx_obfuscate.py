"""
nx_obfuscate.py — Runtime decoder for obfuscated constants.
Nothing sensitive is stored as plain text in the package.
All constants are base64 encoded and decoded at runtime only.
"""

import base64


def _d(s: str) -> str:
    """Decode a base64-encoded constant."""
    return base64.b64decode(s.encode()).decode()


P = {
    "primary":    _d("bnZpZGlh"),         # legacy "primary" alias — now tertiary fallback
    "fallback":   _d("ZGVlcGluZnJh"),     # the secondary provider — secondary fallback as of 0.3.96
    "fireworks":  _d("ZmlyZXdvcmtz"),     # the primary provider — PRIMARY provider as of 0.3.96
    "openrouter": _d("b3BlbnJvdXRlcg=="),
    "openai":     _d("b3BlbmFp"),
    # Native raw-price providers (0.4+): direct Alibaba DashScope (Qwen) + DeepSeek. When their key is set they
    # LEAD their tier (Qwen = heavy/coding/long-turn, DeepSeek = flash chat + deep reasoning); the fireworks →
    # deepinfra → legacy chain stays the resilience fallback. No key ⇒ they never engage (zero behavior change).
    "dashscope":  _d("ZGFzaHNjb3Bl"),
    "deepseek":   _d("ZGVlcHNlZWs="),
}

CFG = {
    "prefer_primary": _d("cHJlZmVyX252aWRpYQ=="),
}

ENV = {
    "fireworks_api_key":   _d("RklSRVdPUktTX0FQSV9LRVk="),       # primary provider API-key env var
    "fireworks_keychain":  _d("ZmlyZXdvcmtzLWtleQ=="),           # primary provider keychain name
    "fallback_api_key":    _d("REVFUElORlJBX0FQSV9LRVk="),       # secondary provider API-key env var
    "deepinfra_keychain":  _d("ZGVlcGluZnJhLWtleQ=="),           # secondary provider keychain name
    "keychain_prefix":     _d("bnZpZGlhLWtleS0="),               # legacy pool keychain prefix
    "nvidia_key_env":      _d("TlZJRElBX0tFWV8="),               # legacy pool env-var prefix
    "openrouter_api_key":  _d("T1BFTlJPVVRFUl9BUElfS0VZ"),
    "openai_api_key":      _d("T1BFTkFJX0FQSV9LRVk="),
    "dashscope_api_key":   _d("REFTSFNDT1BFX0FQSV9LRVk="),        # native Qwen (DashScope) API-key env var
    "deepseek_api_key":    _d("REVFUFNFRUtfQVBJX0tFWQ=="),        # native DeepSeek API-key env var
}

AUTH = {
    "base": _d("aHR0cHM6Ly9hcGkubmV4cGxvcmEuYWk="),
    "device_code": _d("L2FwaS9vYXV0aC9kZXZpY2UvY29kZQ=="),
    "token": _d("L2FwaS9vYXV0aC90b2tlbg=="),
    "refresh": _d("L2FwaS9vYXV0aC9yZWZyZXNo"),
    "chat": _d("L2FwaS9nYXRld2F5"),
    "activate": _d("aHR0cHM6Ly9uZXhwbG9yYS5haS9hY3RpdmF0ZQ=="),
    "client_id": _d("bngtY2xp"),
}

URLS = {
    P["fireworks"]:  _d("aHR0cHM6Ly9hcGkuZmlyZXdvcmtzLmFpL2luZmVyZW5jZS92MQ=="),  # the primary provider (primary)
    P["fallback"]:   _d("aHR0cHM6Ly9hcGkuZGVlcGluZnJhLmNvbS92MS9vcGVuYWk="),       # the secondary provider (secondary)
    P["primary"]:    _d("aHR0cHM6Ly9pbnRlZ3JhdGUuYXBpLm52aWRpYS5jb20vdjE="),       # the legacy pooled provider (tertiary)
    P["openrouter"]: _d("aHR0cHM6Ly9vcGVucm91dGVyLmFpL2FwaS92MQ=="),
    P["openai"]:     _d("aHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MQ=="),
    # Native OpenAI-compatible endpoints (the raw-price path). Model ids are env-overridable at the routing layer
    # (NX_QWEN_MODEL_MAX / NX_DEEPSEEK_MODEL_*); the base URLs here are the native defaults.
    P["dashscope"]:  _d("aHR0cHM6Ly9kYXNoc2NvcGUuYWxpeXVuY3MuY29tL2NvbXBhdGlibGUtbW9kZS92MQ=="),
    P["deepseek"]:   _d("aHR0cHM6Ly9hcGkuZGVlcHNlZWsuY29tL3Yx"),
}

# Secondary-provider catalog IDs (case-sensitive). Used when the secondary
# provider is the resolved provider (primary provider key missing).
# Verified live 2026-06-22.
M = {
    "kimi":      _d("bW9vbnNob3RhaS9LaW1pLUsyLjY="),
    "dsv4pro":   _d("ZGVlcHNlZWstYWkvRGVlcFNlZWstVjQtUHJv"),
    "dsv4flash": _d("ZGVlcHNlZWstYWkvRGVlcFNlZWstVjQtRmxhc2g="),
    "glm52":     _d("emFpLW9yZy9HTE0tNS4y"),
    "kimi_code": _d("bW9vbnNob3RhaS9LaW1pLUsyLjctQ29kZQ=="),
    "qwen_code": _d("UXdlbi9Rd2VuMy1Db2Rlci00ODBCLUEzNUItSW5zdHJ1Y3QtVHVyYm8="),  # the code-tier model id (secondary provider) — light coding
    "llama8b":   _d("bWV0YS1sbGFtYS9NZXRhLUxsYW1hLTMuMS04Qi1JbnN0cnVjdA=="),
    # Legacy bench entry — no active tier.
    "nemotron":  _d("bnZpZGlhL2xsYW1hLTMuMy1uZW1vdHJvbi1zdXBlci00OWItdjE="),
}

# Primary-provider catalog IDs (p-notation for versions, verified live against
# /v1/chat/completions 2026-06-22). Primary provider as of 0.3.96.
FW = {
    "fast":      _d("YWNjb3VudHMvZmlyZXdvcmtzL21vZGVscy9kZWVwc2Vlay12NC1mbGFzaA=="),
    "pro":       _d("YWNjb3VudHMvZmlyZXdvcmtzL21vZGVscy9kZWVwc2Vlay12NC1wcm8="),
    "kimi_code": _d("YWNjb3VudHMvZmlyZXdvcmtzL21vZGVscy9raW1pLWsycDctY29kZQ=="),
    "kimi":      _d("YWNjb3VudHMvZmlyZXdvcmtzL21vZGVscy9raW1pLWsycDY="),
    "glm":       _d("YWNjb3VudHMvZmlyZXdvcmtzL21vZGVscy9nbG0tNXAy"),
}

# Aggregator-fallback cross-provider model (council last-resort). Obfuscated so
# no literal provider/model triple appears in shipped source.
OR_FALLBACK = _d("b3BlbmFpL2dwdC00by1taW5p")  # aggregator fallback model id
# Final-fallback model id (last-resort provider in the chain).
OAI_FALLBACK = _d("Z3B0LTRvLW1pbmk=")  # final fallback model id

MR = {
    # Semantic aliases — names stay stable across providers. The TIERS
    # registry in nx_routing.py picks FW or M values based on resolved
    # provider; consumers only see the resolved model string.
    "peer":      M["kimi"],
    "pro":       M["dsv4pro"],
    "fast":      M["dsv4flash"],
    "glm":       M["glm52"],
    "code_kimi": M["kimi_code"],
    "qwen_code": M["qwen_code"],   # the code-tier model id — light-effort coding lane
    "small":     M["llama8b"],
    "coord":     M["nemotron"],   # legacy alias — no active tier
}

# Native raw-price catalog IDs. Env-overridable at the routing layer (NX_QWEN_MODEL_MAX / NX_DEEPSEEK_MODEL_CHAT /
# NX_DEEPSEEK_MODEL_REASONER). Defaults are current stable native ids: Qwen `qwen-max` (set NX_QWEN_MODEL_MAX=
# qwen3.8-max-preview for the promo tier); DeepSeek `deepseek-chat` (chat/coding) + `deepseek-reasoner` (deep reasoning).
NATIVE = {
    "qwen_max":   _d("cXdlbi1tYXg="),
    "ds_chat":    _d("ZGVlcHNlZWstY2hhdA=="),
    "ds_reason":  _d("ZGVlcHNlZWstcmVhc29uZXI="),
}

SB = {
    "nx_url": _d("aHR0cHM6Ly90aXlvbmN2bWxlcnlqbW9mdGR5YS5zdXBhYmFzZS5jbw=="),
    "anon_key": _d(
        "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKemRYQmhZbUZ6WlNJc0luSmxaaUk2SW5ScGVXOXVZM1p0YkdWeWVXcHRiMlowWkhsaElpd2ljbTlzWlNJNkltRnViMjRpTENKcFlYUWlPakUzT0RFek9ESXlOalVzSW1WNGNDSTZNakE1TmprMU9ESTJOWDAuZjdPT3VFLUUxcld1VTk0Qlk2U1E5a3hDcmxqaVZ2YldvbVYyUjhtN0FSMA=="
    ),
    "rest": _d("L3Jlc3QvdjE="),
    "storage": _d("L3N0b3JhZ2UvdjEvb2JqZWN0"),
    "auth": _d("L2F1dGgvdjE="),
    "functions": _d("L2Z1bmN0aW9ucy92MS8="),
}

BRIDGE = {
    "endpoint": _d("bngtYXV0aC1icmlkZ2U="),
    "nx_url": SB["nx_url"],
}

HUB = {
    "default": _d("aHR0cDovL2xvY2FsaG9zdDozNzM3Mw=="),
    "registry": _d("aHR0cHM6Ly9yYXZpdGVtZXIuZ2l0aHViLmlvL21jcC1yZWdpc3RyeS9yZWdpc3RyeS5qc29u"),
    "servers_api": _d("L2FwaS9zZXJ2ZXJz"),
    "connect": _d("L2FwaS9jb25uZWN0"),
    "disconnect": _d("L2FwaS9kaXNjb25uZWN0"),
    "user_api": _d("L2FwaS91c2VyLw=="),
    "health": _d("L2hlYWx0aA=="),
    "tools_suffix": _d("L3Rvb2xz"),
    "servers_suffix": _d("L3NlcnZlcnM="),
}

ID = {
    "name": _d("Tlg="),
    "builder": _d("TmV4cGxvcmE="),
    "version": _d("MC4xNS4yMjE="),
}

# Freeze the constant tables: any in-process attempt to mutate a model id,
# provider URL, Keychain name, or the version string now raises TypeError
# instead of silently corrupting routing/obfuscation at runtime. (Reads and
# .get() are unaffected.) MR is built from M above, so freeze after.
from types import MappingProxyType as _Frozen  # noqa: E402
P   = _Frozen(P)
CFG = _Frozen(CFG)
ENV = _Frozen(ENV)
AUTH = _Frozen(AUTH)
URLS = _Frozen(URLS)
M   = _Frozen(M)
FW  = _Frozen(FW)
MR  = _Frozen(MR)
SB  = _Frozen(SB)
BRIDGE = _Frozen(BRIDGE)
HUB = _Frozen(HUB)
ID  = _Frozen(ID)
