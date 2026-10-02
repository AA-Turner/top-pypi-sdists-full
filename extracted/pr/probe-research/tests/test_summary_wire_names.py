"""The headline-scalar map goes out under both wire names.

`summary_metrics` is the field's real name; `summary` is the alias the server
still accepts. Sending one only is unsafe in one direction each: alias-only
means the server can never drop the alias, and new-name-only silently loses the
map against a server older than the rename -- which prod briefly was on
2026-09-21, when a failing post-upgrade hook rolled releases back.
"""

from __future__ import annotations

from conftest import open_run

from probe.sdk.run import _summary_wire


def test_both_names_carry_the_same_map() -> None:
    scalars = {"final_exact_match": 0.336, "n_steps": 934}
    wire = _summary_wire(scalars)
    assert wire == {"summary_metrics": scalars, "summary": scalars}


def test_the_two_names_are_the_same_object_not_a_copy() -> None:
    """Identity, so no caller can mutate one spelling into disagreeing with the
    other and leave the server's choice of alias deciding what got recorded."""
    scalars = {"loss": 1.0}
    wire = _summary_wire(scalars)
    assert wire["summary_metrics"] is wire["summary"]


def test_none_is_carried_through_under_both_names() -> None:
    """Callers gate on `is not None` before building a body; the helper itself
    stays total rather than inventing an empty map."""
    assert _summary_wire(None) == {"summary_metrics": None, "summary": None}


def test_set_status_puts_both_names_on_the_actual_patch(client, app) -> None:
    """The real PATCH body, not a text scan of the source.

    An earlier version of this guard read the module's source for the literal
    `"summary"` and flagged `Run.span()`'s kwargs dict -- a Python parameter
    name that has nothing to do with the wire. What matters is what is POSTED,
    so assert on that.
    """
    run = open_run(client, experiment="wire-names")
    run.set_status("completed", summary_metrics={"final_exact_match": 0.336}, sync=True)

    patches = [
        r for r in app.requests if r.method == "PATCH" and str(r.url).endswith(f"/v1/runs/{run.id}")
    ]
    assert patches, "no terminal PATCH was sent"
    import json as _json

    body = _json.loads(patches[-1].content)
    assert body["summary_metrics"] == {"final_exact_match": 0.336}
    assert body["summary"] == {"final_exact_match": 0.336}
