"""Static values and every environment-variable NAME the router reads (declared once)."""
from __future__ import annotations

# environment variable names
ENV_HOME = "HUGPY_ROUTER_HOME"                       # the router's store directory
ENV_BOXES = "HUGPY_ROUTER_BOXES"                     # path of the boxes file (JSON)
ENV_KEY = "HUGPY_ROUTER_KEY"                         # the router's own admin key (hpk_box_…)
ENV_REQUIRE_KEY = "HUGPY_ROUTER_REQUIRE_KEY"         # never | outside (default) | always
ENV_TRUSTED_NETS = "HUGPY_ROUTER_TRUSTED_NETS"
ENV_TRUSTED_PROXIES = "HUGPY_ROUTER_TRUSTED_PROXIES"
ENV_STORE_MODE = "HUGPY_ROUTER_STORE_MODE"           # private (default) | group
ENV_HOST = "HUGPY_ROUTER_HOST"
ENV_PORT = "HUGPY_ROUTER_PORT"

# store
STORE_SUBDIR = "router"                              # under the per-OS data dir
STORE_FILENAME = "router.sqlite3"
BOXES_FILENAME = "boxes.json"                        # under the per-OS config dir /router

# central's queue above the boxes (the wrapper's admission names, same defaults)
ENV_QUEUE_POLICY = "HUGPY_QUEUE_POLICY"
ENV_QUEUE_BYPASS_MAX = "HUGPY_QUEUE_BYPASS_MAX"
ENV_QUEUE_MAX_WAIT_S = "HUGPY_QUEUE_MAX_WAIT_S"
QUEUE_POLICY_DEFAULT = "eta"
QUEUE_BYPASS_MAX_DEFAULT = 3
QUEUE_MAX_WAIT_DEFAULT_S = 120

# routing
WAIT_S = 30                                          # long-poll window per box link
OFFLINE_AFTER_S = 90                                 # no answer from a box this long -> offline
CONNECT_TIMEOUT_S = 10
FIRST_BYTE_TIMEOUT_S = 900                           # a cold load may take minutes before the first byte

# wrapper errors that are a REFUSAL of the call before the first byte (the box could
# not serve it now). With central's allocation known before placement a refusal is a
# recorded fact against that allocation (operator 2026-10-14) — never a bounce.
REFUSAL_TYPES = ("load_error", "insufficient_resources", "profile_materializing", "not_found_error")

# OpenAI routes the router proxies (POST); GET /v1/models is the union of the boxes' catalogs
PROXY_ROUTES = (
    "/v1/chat/completions", "/v1/completions", "/v1/embeddings",
    "/v1/audio/transcriptions", "/v1/audio/translations", "/v1/audio/speech",
    "/v1/images/generations", "/v1/images/edits", "/v1/images/variations",
    "/v1/videos/generations", "/v1/summarize", "/v1/keywords",
)
