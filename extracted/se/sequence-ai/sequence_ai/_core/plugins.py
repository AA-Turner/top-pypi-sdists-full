"""
The open sequence-ai's few doors for a package that adds to it - sequence-cloud, GS's own client for its platform: its
commands on `seq`, its names on `seq.*` and `sequence_ai.*`, connect() by a deployment's name, and a `seq login`
sign-in. Each door is a group of entry points, read once, the first that loads answering; with none installed the open
package is all there is, and a name of the platform's says how to get it.

    seq.commands       a module with register(ap, sub), split(argv), json_ok(args), prepare(args), dispatch(args) and
                       report(exc, command): its `seq` subcommands (seq/cli.py, seq/cli_parser.py)
    seq.api            a module whose __all__ are its names on `seq` (seq.deploy, seq.benchmark, ...)
    sequence_ai.api    a module whose __all__ are its names on `sequence_ai` (sequence_ai.models, ...), with
                       by_name(name, *more, **options) for connect() by a name - the connection after it the open
                       Policy - and follow(token, url, base_url) for a rented GPU's allow list
    sequence_ai.signin a module with login_for(base), auth_of(login) and is_login(value)



"""
from __future__ import annotations

import functools
from importlib import metadata
from typing import Any


INSTALL = 'pip install sequence-cloud --extra-index-url "https://$SEQUENCES_API_KEY@api.generalsequences.com/simple"'


@functools.lru_cache(maxsize=None)
def loaded(group: str) -> tuple[Any, ...]:
    """Every entry point of `group` loaded, in their names' order; one that does not load is said once and passed by."""
    out = []
    for ep in sorted(_points(group), key=lambda e: e.name):
        try:
            out.append(ep.load())
        except Exception as exc:
            from .warn import warn

            warn(f"{ep.value} did not load ({type(exc).__name__}: {exc}); sequence-ai goes on without it")
    return tuple(out)


def _points(group: str) -> tuple[Any, ...]:
    """The entry points of `group` on every Python the package runs on: 3.10 and later select them by group; 3.9's
    entry_points() takes no group and answers a dict of every group's, read here by its name.
    
"""
    every = metadata.entry_points()
    return tuple(every.select(group=group)) if hasattr(every, "select") else tuple(every.get(group, ()))


def first(group: str) -> Any | None:
    """The first of `group` that loaded, or None with none installed."""
    got = loaded(group)
    return got[0] if got else None


def needs_cloud(what: str) -> str:
    """The sentence a name of the platform's says with sequence-cloud not installed."""
    return f"{what} is part of sequence-cloud, GS's client for its platform: {INSTALL}"
