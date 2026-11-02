"""help route registration (abstract_flask ``register_categories`` convention).

The console Help panel (``/llm/help/*``) and the floating Keeper widget
(``/keeper/help/*``) handlers LIVE in ``help_routes.py`` as plain functions
(kwargs in, JSON-able out); this module only states the URL tree and registers
it. Dict nesting is the path, a ``<param>`` / ``<int:tid>`` key is a path
parameter that reaches the handler as the same-named kwarg, the ``""`` key is a
node's own index route, and a LIST of ``spec`` leaves on one key puts several
method-specific views on one URL.

Every ``/llm/help/*`` route is ``spec(..., response="native")`` so its bare JSON
shape and status code are served verbatim (the console reads ``{sessions:[…]}``,
``{records:[…]}``, 201/400/404/409/503 …, not ``{result:{…}}``). The SSE stream
view returns a Flask ``Response`` which passes through unchanged. The two Keeper
widget routes are plain callable leaves (GET+POST, ``{"result": …}``), their
shape before the lift.
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories, spec

from hugpy_core.help.help_routes import (
    help_session_delete,
    help_session_get,
    help_session_send,
    help_session_stop,
    help_session_stream,
    help_sessions_list,
    help_sessions_start,
    help_ticket_act,
    keeper_ask,
    keeper_report,
    tickets_list,
)

help_bp, logger = get_bp("help_bp", __name__)


def _native(view, methods):
    return spec(view, methods, response="native")


ALL_CATEGORIES = {
    "keeper": {"help": {"ask": keeper_ask, "report": keeper_report}},
    "llm": {
        "help": {
            "sessions": {
                "": [                                            # /llm/help/sessions
                    _native(help_sessions_list, "GET"),
                    _native(help_sessions_start, "POST"),
                ],
                "<sid>": {
                    "": [                                        # /llm/help/sessions/<sid>
                        _native(help_session_get, "GET"),
                        _native(help_session_delete, "DELETE"),
                    ],
                    "messages": _native(help_session_send, "POST"),   # …/<sid>/messages
                    "stop": _native(help_session_stop, "POST"),       # …/<sid>/stop
                    "stream": _native(help_session_stream, "GET"),    # …/<sid>/stream (SSE)
                },
            },
            "tickets": {
                "": _native(tickets_list, "GET"),                # /llm/help/tickets
                "<int:tid>": {
                    "act": _native(help_ticket_act, "POST"),     # …/<int:tid>/act
                },
            },
        },
    },
}
register_categories(help_bp, ALL_CATEGORIES)
