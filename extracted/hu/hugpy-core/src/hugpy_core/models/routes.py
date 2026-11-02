"""models route registration (abstract_flask ``register_categories`` convention).

The console DATABASE RELAY views and the per-(model, worker) / per-worker writes
live in ``modeldb.py`` as plain functions (kwargs in — query + form + JSON body +
path params, merged by the registrar with URL identity winning — JSON-able out);
the model-rows SSE lives in ``modelrows.py``. This module only states the URL
tree and registers it onto one blueprint (``models_bp``); the parent wires the
bare-vs-/api dual mount.

Dict nesting is the path. The write handlers answer BOTH forms with the SAME
function: the body form (``/models/database/workers/knobs`` with ``{key, wid,
...}`` in the body, a plain GET+POST ``{"result": ...}`` leaf) and the path form
(``/models/database/<key>/workers/<wid>/knobs``, a ``spec`` POST leaf that serves
the answer BARE — ``response="native"`` — as the console reads it today); the
registrar feeds ``<key>``/``<wid>`` as the same-named kwargs, merged with the
body. ``models_database`` and ``model_discover`` are re-exported from here (name
in this module's namespace) for the web guest-access and delete call sites.
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec

from hugpy_core.models import modeldb, modelrows
from hugpy_core.models.modeldb import (
    model_discover,
    models_database,
    pair_activate,
    pair_assigned,
    pair_knobs,
    pair_pinned,
    worker_activation_report,
    worker_config,
    worker_limits,
    worker_moe,
)
from hugpy_core.models.modelsdb import MODELSDB_CATEGORIES

models_bp, logger = get_bp("models_bp", __name__)


def _post(view):
    """POST-only leaf serving a BARE answer (the console contract for the path
    form of a write)."""
    return spec(view, "POST", response="native")


ALL_CATEGORIES = {
    "models": {
        "database": {
            "": models_database,                 # /models/database (GET+POST)
            "discover": model_discover,          # /models/database/discover
            "workers": {                         # body form: {key, wid, ...}
                "knobs": pair_knobs,             # /models/database/workers/knobs
                "assigned": pair_assigned,       # /models/database/workers/assigned
                "pinned": pair_pinned,           # /models/database/workers/pinned
                "activate": pair_activate,       # /models/database/workers/activate
            },
            "<key>": {                           # path form: identifiers in the URL
                "workers": {
                    "<wid>": {
                        "knobs": _post(pair_knobs),        # /models/database/<key>/workers/<wid>/knobs
                        "assigned": _post(pair_assigned),  # .../assigned
                        "pinned": _post(pair_pinned),      # .../pinned
                        "activate": _post(pair_activate),  # .../activate
                    },
                },
            },
        },
    },
    "fleet": {
        "workers": {
            "activation": worker_activation_report,  # body form /fleet/workers/activation
            "limits": worker_limits,                 # /fleet/workers/limits
            "config": worker_config,                 # /fleet/workers/config
            "moe": worker_moe,                       # /fleet/workers/moe
            "<wid>": {                               # path form: /fleet/workers/<wid>/*
                "activation": _post(worker_activation_report),
                "limits": _post(worker_limits),
                "config": _post(worker_config),
                "moe": _post(worker_moe),
            },
        },
    },
    "llm": {
        "models": {
            "rows": {
                "stream": modelrows.model_rows_stream,  # /llm/models/rows/stream (SSE)
            },
        },
    },
    # Fleet models database (models-db-v1): per-worker projection of each
    # Wrapper's own models DB, mirrored by intake/models_db.py.
    **MODELSDB_CATEGORIES,                       # /modelsdb/*
}
register_categories(models_bp, ALL_CATEGORIES)
