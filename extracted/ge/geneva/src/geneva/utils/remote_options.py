# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Carrying surplus tuning knobs across the remote (``db://``) dispatch.

A namespace request declares only the knobs that existed when its schema was
generated, and the generated model defaults to pydantic's ``extra="ignore"``.
So a knob added to ``backfill()`` or ``refresh()`` works locally and silently
disappears remotely, with no error on either side. What follows decides which
knobs may ride along as surplus keys, and builds a request model that keeps
them.
"""

from __future__ import annotations

import logging
from functools import cache
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

_LOG = logging.getLogger(__name__)

# Kwargs that never cross the wire, by name. Client-side objects the driver
# has no use for, and identity the transport already carries.
#
# Deliberately a denylist: a new tuning knob should reach the remote driver by
# being added to ``backfill()``, without a second edit here. An allowlist would
# make a forgotten entry silently drop the knob -- reintroducing exactly the
# bug this mechanism fixes, and doing it every time Geneva grows an argument.
NON_FORWARDABLE_REMOTE_KWARGS = frozenset(
    {
        # Transport vocabulary: these select *what* the operation acts on, so
        # they must never arrive through a channel meant to tune *how* it runs
        # -- including on a request whose schema happens not to declare them.
        "branch",
        "namespace",
        "version",
        # Names the server owns and rejects outright (400, not a silent drop):
        # BACKFILL_RESERVED_KEYS / REFRESH_RESERVED_KEYS and ENVELOPE_KEYS in
        # phalanx's rest/table/geneva_options.rs.
        "col_name",
        "column_name",
        "id",
        "identity",
        "job_id",
        "udf",
        # Client-side objects the driver has no use for.
        "checkpoint",
        "checkpoint_store",
        "column",
        "columns",
        "error_store",
        "job_tracker",
        "packager",
        "storage_options",
        "table",
        "table_name",
    }
)

# Mirrors phalanx's geneva_options limits, so a value it would reject with a
# 400 is kept local instead of failing the whole dispatch.
MAX_OPTION_NAME_LEN = 64
MAX_OPTION_VALUE_LEN = 1024


def server_accepts_option_name(name: str) -> bool:
    """Whether phalanx's ``validate_key`` would accept this key.

    Its rule: non-empty, at most 64 chars, first character an ASCII lowercase
    letter, remainder ASCII lowercase / digits / underscore. Notably a leading
    underscore fails -- which is why Geneva's experimental ``_``-prefixed
    knobs cannot travel this way at all.
    """
    return (
        bool(name)
        and len(name) <= MAX_OPTION_NAME_LEN
        and name[0].isascii()
        and name[0].islower()
        and name[0].isalpha()
        and all(c.isascii() and (c.islower() or c.isdigit() or c == "_") for c in name)
    )


def forwardable_remote_options(
    kwargs: dict[str, Any], *, reserved: Iterable[str]
) -> dict[str, Any]:
    """Tuning knobs safe to forward verbatim to the remote driver.

    The server captures unknown scalar keys and splats them into the driver's
    corresponding call, so forwarding them from here is what makes a knob work
    remotely without a namespace schema bump -- and, deliberately, without an
    edit to any list in this file.

    What is held back:

    ``reserved`` is what the *transport* owns -- every field the request model
    declares, plus everything already being sent. This is not a naming policy
    but a correctness one: extras bind to a declared field if one exists, so
    without it a caller could route the operation elsewhere (``branch``)
    through a channel meant only for tuning.

    ``NON_FORWARDABLE_REMOTE_KWARGS`` names what a knob must not be: a
    client-side object, transport vocabulary, or a name the server reserves.
    Credentials are not on it because they are not backfill arguments -- they
    belong to ``connect()`` -- and the one that does arrive here,
    ``storage_options``, is denied by name and is not a scalar besides.

    The name and value checks mirror phalanx's ``sanitize_geneva_options``,
    because it answers a bad key with a 400 for the *whole request*, not by
    dropping that key. Failing a backfill over a tuning knob would be worse
    than the silent drop this exists to fix, so anything it would reject stays
    local. One consequence worth knowing: its keys must begin with an ASCII
    lowercase letter, so Geneva's experimental ``_``-prefixed knobs (e.g.
    ``_skip_planner_filter_count``) cannot cross this channel at all -- they
    stay local, and reaching one remotely means renaming it without the
    underscore.
    """
    off_limits = set(reserved)
    options: dict[str, Any] = {}
    for name, value in kwargs.items():
        if value is None or name in off_limits:
            continue
        if name in NON_FORWARDABLE_REMOTE_KWARGS:
            continue
        if not server_accepts_option_name(name):
            continue
        if not isinstance(value, str | int | float | bool):
            continue
        if isinstance(value, str) and len(value) > MAX_OPTION_VALUE_LEN:
            continue
        options[name] = value
    return options


@cache
def request_model_with_options(request_cls: type[Any]) -> type[Any]:
    """A request model that keeps keys its schema doesn't declare.

    The generated model drops unknown keys at construction, so extras have to
    be opted into for them to reach the serialized body at all.
    """
    from pydantic import ConfigDict

    return type(
        f"{request_cls.__name__}WithOptions",
        (request_cls,),
        {
            "model_config": ConfigDict(
                **{**dict(request_cls.model_config), "extra": "allow"}
            )
        },
    )


def build_remote_request(
    request_cls: type[Any],
    request_kwargs: dict[str, Any],
    kwargs: dict[str, Any],
    *,
    op: str,
) -> Any:
    """Build a namespace request, carrying surplus caller knobs as extras.

    ``request_kwargs`` is what the dispatcher assembled from declared fields;
    anything else the caller tuned rides along instead of being dropped on the
    floor. Falls back to the plain generated model when there is nothing
    surplus to carry, so the unchanged case stays unchanged.
    """
    options = forwardable_remote_options(
        kwargs, reserved=set(request_kwargs) | set(request_cls.model_fields)
    )
    if not options:
        return request_cls(**request_kwargs)

    _LOG.debug("Forwarding %s options to the remote driver: %s", op, sorted(options))
    return request_model_with_options(request_cls)(**request_kwargs, **options)
