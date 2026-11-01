"""HttpOpHandler: deliver http and rejected_http ops, placing an experiment child write at its experiment's project."""

from __future__ import annotations
from .... import errors
from ..ops import _UNPLACED_EXPERIMENT_PATH


def _placed(client, op: dict) -> dict | None:
    """Deliver a journaled experiment child write at the project its experiment is filed
    in NOW (``client._on_experiment``: placed once per client, again on a 404 at a
    remembered project). None for any other op.

    A route-absent server (older than X21) is answered as its own 404, which
    dead-letters like any refusal, not as a capability error the drain would not classify."""
    match = _UNPLACED_EXPERIMENT_PATH.fullmatch(op.get("path") or "")
    if match is None:
        return None
    rest = match.group(2)

    def send(project: str, experiment: str):
        return client.transport.request(
            op["method"],
            f"/v1/projects/{project}/experiments/{experiment}{rest}",
            json_body=op.get("body"),
        )

    try:
        return {"response": client._on_experiment(send, match.group(1))}
    except errors.CapabilityUnavailable as exc:
        if isinstance(exc.__cause__, errors.RosError):
            raise exc.__cause__ from None
        raise
