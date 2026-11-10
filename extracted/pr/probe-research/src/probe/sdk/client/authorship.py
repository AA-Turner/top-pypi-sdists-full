"""stamp authored_by (declared, else from the environment) into request bodies."""

from __future__ import annotations
from .. import agent_session


def _authored_by(explicit: str | None, *, is_new_run_name: bool = False) -> str | None:
    """The `authored_by` to send: what the caller declared, else the environment.

    ONE RESOLVER, so every door agrees. `None` back means SEND NO KEY -- not
    `"authored_by": null` -- because the server reads an absent field as "this
    client has not been taught to say" and applies its historical inference,
    which is exactly the behaviour every release before this one had.
    """
    if explicit is not None:
        return explicit
    return agent_session.default_authorship(is_new_run_name=is_new_run_name)


def _put_authorship(body: dict, explicit: str | None, *, is_new_run_name: bool = False) -> None:
    """Stamp `authored_by` into a request body, or leave the body untouched."""
    resolved = _authored_by(explicit, is_new_run_name=is_new_run_name)
    if resolved is not None:
        body["authored_by"] = resolved
