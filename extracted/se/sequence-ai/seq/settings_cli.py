"""
`seq policy settings` / `seq policy set` and seq.policy_settings / seq.policy_set: a deployment's settings, read and
changed without a redeploy.

In one sentence: each key is read as sequence-base's one table holds it (contract.settings: `parse` for a command line's
KEY=VALUE, `check` for a value from Python) → one PATCH /v1/deployments/{name}/settings changes them, all or none → the
answer says each key before and after and when it takes effect, which this says back; GET says every setting, where its
value comes from and how far its last change has reached.

    seq.policy_set("kitchen_user", {"min_workers": 1, "max_wait_for_batch": 1.7, "params.num_steps_user": 8})
"""
from __future__ import annotations

from typing import Any, Callable

from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest

from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None


_TAKES = {"gateway": "now", "workers": "each running worker within a minute",
          "new_workers": "workers started from now on",
          "episodes": "each running worker within a minute, for the episodes begun after it",
          "new_version": "a new version, which takes over once its check passes"}


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def policy_settings(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Every setting of the deployment `name`: its value, what its code says, where the value comes from, its last
    change and by whom, and how far a change its workers read has reached."""
    out = _call("GET", f"/v1/deployments/{segment(name)}/settings", base_url)
    if echo is not None:
        _show(out, echo)
    return out


def policy_set(name: str, changes: dict, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Change settings of the deployment `name` at once, all of them or none: {key: value}, None putting a key back to
    what the code says. A machine key (gpu, weights, cpu, memory, replica_start) builds a new version, which takes over
    once its check passes."""
    from sequence_base.contract.settings import check

    try:
        body: dict = {"changes": {k: check(k, v) for k, v in changes.items()}}
    except ValueError as exc:
        raise InvalidRequest(str(exc)) from None
    out = _call("PATCH", f"/v1/deployments/{segment(name)}/settings", base_url, body)
    for c in out.get("changed") or []:
        _say(echo, f"{c['key']}: {_shown(c.get('before'))} → {_shown(c.get('after'))} - {_TAKES.get(c['reads'], '')}")
    if not out.get("changed"):
        _say(echo, f"{name}: nothing changed")
    if out.get("version"):
        _say(echo, f"v{out['version']} builds with it: `seq policy status {name}` follows it")
    if out.get("notice"):

        _say(echo, out["notice"])
        if body["changes"].get("capture") == "on":
            _say(echo, "hint: seq account set --storage-limit <GB>")
    if out.get("signing_secret"):
        _say(echo, f"alerts' signing secret (shown once): {out['signing_secret']} - each alert's X-Seq-Signature is "
                   "sha256=HMAC(secret, body)")
    return out


def parse_pairs(pairs: list[str]) -> dict:
    """`seq policy set NAME key=value ...` as {key: value}, each value read as its key holds it (contract.settings
    parse): an empty value puts the key back to what the code says."""
    from sequence_base.contract.settings import parse

    out = {}
    for pair in pairs:
        key, eq, text = pair.partition("=")
        if not eq or not key.strip():
            raise InvalidRequest(f"write each change as KEY=VALUE, e.g. min_workers=1; got {pair!r}")
        try:
            out[key.strip()] = parse(key.strip(), text)
        except ValueError as exc:
            raise InvalidRequest(str(exc)) from None
    return out


def _shown(v: Any) -> str:
    if v is None:
        return "-"
    if isinstance(v, list):
        return ",".join(str(x) for x in v) or "-"
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _show(out: dict, echo) -> None:
    echo(f"{out['deployment']} settings (rev {out.get('rev', 0)})")
    rows = out.get("settings") or []
    width = max((len(r["key"]) for r in rows), default=10)
    for r in rows:
        note = []
        if r.get("source") == "set" and r.get("code") is not None and r.get("code") != r.get("value"):
            note.append(f"code says {_shown(r['code'])}")
        applied = r.get("applied")
        if applied and applied.get("of"):
            note.append(f"{applied['workers']} of {applied['of']} workers have it")
        if r.get("version"):
            note.append(f"v{r['version']} builds with another")
        if r.get("changed_at"):
            note.append(f"changed {r['changed_at']}" + (f" by {r['changed_by']}" if r.get("changed_by") else ""))
        echo(f"  {r['key']:<{width}}  {_shown(r.get('value')):<14} {r.get('source', ''):<8} {'; '.join(note)}".rstrip())
