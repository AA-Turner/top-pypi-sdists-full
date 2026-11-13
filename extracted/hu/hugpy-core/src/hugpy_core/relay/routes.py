"""relay route registration (abstract_flask ``register_categories`` convention).

The task relay is a PROXY: each ``/v1/...`` task route forwards the request
(JSON or multipart, body and answer untouched) to the box that holds ``model``.
The proxy work lives in ``taskrelay.py`` (``_relay`` + ``TASK_ROUTES``); here each
route becomes a view registered via the convention. The views keep the proxy
shape — they read ``request`` directly and return the box's ``Response`` passed
through — so the body/headers/query are forwarded verbatim.
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec

from hugpy_core.relay.taskrelay import _relay

relay_bp, logger = get_bp("relay_bp", __name__)


def _proxy(route: str):
    """A view for one task route: ignore the pruned kwargs, forward the live
    request to the box, and pass its Response straight back."""
    def view(**_ignored):
        return _relay(route)
    view.__name__ = "relay" + route.replace("/", "_")
    view.__doc__ = f"proxy POST {route} to the box holding `model`"
    # A proxy returns Flask Responses, including binary artifacts and non-200
    # worker errors. The default tool envelope tries to JSON-encode the Response.
    return spec(view, "GET,POST", inputs="path", response="native")


ALL_CATEGORIES = {
    "v1": {
        "embeddings": _proxy("/v1/embeddings"),          # /v1/embeddings
        "summarize":  _proxy("/v1/summarize"),           # /v1/summarize
        "keywords":   _proxy("/v1/keywords"),            # /v1/keywords
        "audio": {
            "transcriptions": _proxy("/v1/audio/transcriptions"),  # /v1/audio/transcriptions
            "translations":   _proxy("/v1/audio/translations"),    # /v1/audio/translations
            "speech":         _proxy("/v1/audio/speech"),          # /v1/audio/speech
        },
        "images": {
            "generations": _proxy("/v1/images/generations"),  # /v1/images/generations
            "edits":       _proxy("/v1/images/edits"),         # /v1/images/edits
        },
        "videos": {
            "generations": _proxy("/v1/videos/generations"),  # /v1/videos/generations
            "upscale": _proxy("/v1/videos/upscale"),
            "interpolate": _proxy("/v1/videos/interpolate"),
            "track": _proxy("/v1/videos/track"),
        },
        "meshes": {
            "generations": _proxy("/v1/meshes/generations"),  # /v1/meshes/generations
        },
    },
}
register_categories(relay_bp, ALL_CATEGORIES)
