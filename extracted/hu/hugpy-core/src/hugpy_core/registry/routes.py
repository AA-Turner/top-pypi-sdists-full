"""registry route registration under the abstract_flask ``register_categories``
convention.

Consolidates the console's worker-control surface and the LIVE window onto ONE
blueprint, ``registry_bp``. The handlers LIVE in their natural modules as plain
functions (kwargs in, JSON-able out): ``worker_controls.py`` (the Compute-page
worker controls + the ``*_path`` console-URL status adapters) and ``live.py``
(the LIVE window). This module only states the URL tree and registers it.

Dict nesting is the path; the ``""`` key is a node's own index route; a
``<worker_id>`` / ``<key>`` / ``<wid>`` / ``<job_id>`` key is a path parameter
that reaches the handler as the same-named kwarg. The shipped console places the
worker/model id in the PATH and reads a BARE JSON body with a meaningful HTTP
status, so those path forms are ``spec(..., response="native")`` leaves whose
inputs are merged with the body (URL identity wins) — one kwargs handler serves
both the convention body form and the console's path form. The ``operator``
kwarg convention (default ``console``) stays.
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec

from hugpy_core.registry import registry  # re-exported for call sites that patch registry.routes.registry
from hugpy_core.registry import worker_controls as wc
from hugpy_core.registry import model_browser
from hugpy_core.registry.live import live_page, live_stream

registry_bp, logger = get_bp("registry_bp", __name__)

# The wrapper-update handler is reached both through the tree and directly as
# ``registry.routes.workers_update`` by the update API tests; keep the name here.
workers_update = wc.workers_update


def _native(view, method, endpoint):
    """A console path-form leaf: exact method, bare body, status from the handler."""
    return spec(view, method, response="native", endpoint=endpoint, strict_slashes=True)


ALL_CATEGORIES = {
    "fleet": {
        "central": {"browse-drives": _native(model_browser.browse_central_drives, "GET", "central_browse_drives")},
        "workers": {
            # ── convention body forms (worker_id in query/body; {"result": ...}) ──
            "remove":           wc.workers_remove,            # -> /fleet/workers/remove
            "reconnect":        wc.workers_reconnect,         # -> /fleet/workers/reconnect
            "pool":             wc.workers_set_pool,          # -> /fleet/workers/pool
            "update":           wc.workers_update,            # -> /fleet/workers/update
            "central-address":  wc.central_address,           # -> /fleet/workers/central-address
            "load":             wc.workers_load,              # -> /fleet/workers/load
            "unload":           wc.workers_unload,            # -> /fleet/workers/unload
            "evict":            wc.workers_evict,             # -> /fleet/workers/evict
            "free-ram":         wc.workers_free_ram,          # -> /fleet/workers/free-ram
            "restart":          wc.workers_restart,           # -> /fleet/workers/restart
            "reap":             wc.workers_reap,              # -> /fleet/workers/reap
            "remove-model":     wc.workers_remove_model,      # -> /fleet/workers/remove-model
            "reap-approve":     wc.workers_reap_approve,      # -> /fleet/workers/reap-approve
            "alloc-all":        wc.workers_alloc_all,         # -> /fleet/workers/alloc-all
            "bnb":              wc.workers_bnb,               # -> /fleet/workers/bnb
            "wildcard":         wc.workers_wildcard,          # -> /fleet/workers/wildcard
            "fit-preview":      wc.workers_fit_preview,       # -> /fleet/workers/fit-preview
            "calibrate":        wc.workers_calibrate,         # -> /fleet/workers/calibrate
            "calibrate-status": wc.workers_calibrate_status,  # -> /fleet/workers/calibrate-status
            "designations": {
                "prune": wc.workers_prune_designations,       # -> /fleet/workers/designations/prune
            },
            # ── console path forms (worker_id in the URL; bare body + status) ──
            "<worker_id>": {
                "processes": _native(model_browser.processes, "GET", "worker_processes"),
                "terminate-process": _native(model_browser.terminate_process, "POST", "worker_terminate_process"),
                "browse-drives": _native(model_browser.browse_drives, "GET", "worker_browse_drives"),
                "model-browser": {
                    "catalog": _native(model_browser.catalog, "GET", "worker_browser_catalog"),
                    "pair": _native(model_browser.pair, "GET", "worker_browser_pair"),
                    "limits": [_native(model_browser.limits, "GET", "worker_browser_limits"),
                               _native(model_browser.set_limits, "POST", "worker_browser_set_limits")],
                    "report": _native(model_browser.report, "GET", "worker_browser_report"),
                    "preview": _native(model_browser.preview, "POST", "worker_browser_preview"),
                },
                "": _native(wc.remove_path, "DELETE", "worker_remove_path"),
                "reconnect": _native(wc.reconnect_path, "POST", "worker_reconnect_path"),
                "pool": _native(wc.pool_path, "POST", "worker_pool_path"),
                "load": _native(wc.load_path, "POST", "worker_load_path"),
                "reap": _native(wc.reap_path, "POST", "worker_reap_path"),
                "reap-approve": _native(wc.reap_approve_path, "GET", "worker_reap_approve_path"),
                "fit-preview": _native(wc.workers_fit_preview, "GET", "worker_fit_preview_path"),
                "wildcard":    _native(wc.wildcard_path, "POST", "worker_wildcard_path"),
                "unload":      _native(wc.unload_path, "POST", "worker_unload_path"),
                "evict":       _native(wc.evict_path, "POST", "worker_evict_path"),
                "free-ram":    _native(wc.free_ram_path, "POST", "worker_free_ram_path"),
                "restart":     _native(wc.restart_path, "POST", "worker_restart_path"),
                "update":      _native(wc.update_path, "POST", "worker_update_path"),
                "bnb":         _native(wc.bnb_path, "POST", "worker_bnb_path"),
                "calibrate": {
                    "":          _native(wc.calibrate_path, "POST", "worker_calibrate_unavailable_path"),  # 501 NotInThisBuild, as shipped
                    "<job_id>":  _native(wc.workers_calibrate_status, "GET", "worker_calibrate_status_path"),
                },
            },
        },
    },
    "llm": {
        "slots": {
            "":       wc.llm_slots,                            # -> /llm/slots
            "load":   wc.slots_load,                           # -> /llm/slots/load
            "unload": wc.slots_unload,                         # -> /llm/slots/unload
        },
        # /llm/enroll-tokens is served by web/console_routes (enroll_tokens → []);
        # this registry copy was a shadowed NotInThisBuild stub and was removed.
        "enroll-tokens-revoke": wc.enroll_tokens_revoke,   # -> /llm/enroll-tokens-revoke
        "models": {
            "workers": {
                "block":   wc.model_worker_block,              # -> /llm/models/workers/block
                "unblock": wc.model_worker_unblock,            # -> /llm/models/workers/unblock
            },
            "<key>": {
                "workers": {
                    "<wid>": {
                        "block":   _native(wc.model_worker_block, "POST", "model_worker_block_path"),
                        "unblock": _native(wc.model_worker_unblock, "POST", "model_worker_unblock_path"),
                    },
                },
            },
        },
    },
    "live": {
        "stream": live_stream,                            # -> /live/stream
        "page":   live_page,                              # -> /live/page   (was GET /live)
    },
}

register_categories(registry_bp, ALL_CATEGORIES)
