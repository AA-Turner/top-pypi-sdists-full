"""The dataclasses-API inventory is a ratchet, and an honest one.

`dataclasses.replace()`, `.fields()` and `.asdict()` stop working the moment a
contract type becomes a pydantic model (CUTOVER failure mode 4) — they raise,
they do not degrade. PLAN.md carried "35 call sites" as an estimate.

Measured: **7 confirmed, 5 suspected, 14 unrelated.** Migration work is 7–12
sites, not 35.

The range is deliberate. Two earlier versions of the scanner each produced a
single confident number and each was wrong in a different direction: name hints
missed `asdict(self)` inside `ImageContent`, and closure resolution then missed
`asdict(usage_obj)` and `replace(original_request.config)`, whose types are not
in the source at all. Static analysis cannot settle those, so the tool reports
three buckets instead of pretending.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))

import dataclass_api_inventory as inv  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2] / "matrx_ai"


def _buckets():
    sites = inv.scan(ROOT)
    return (
        [s for s in sites if s["bucket"] == "CONFIRMED"],
        [s for s in sites if s["bucket"] == "SUSPECTED"],
        [s for s in sites if s["bucket"] == "OTHER"],
    )


def test_the_inventory_is_a_ratchet_that_only_goes_down():
    confirmed, suspected, _ = _buckets()
    total = len(confirmed) + len(suspected)
    assert total <= 12, (
        f"{total} contract-or-suspected dataclasses-API sites; the ceiling is 12 and it only "
        "goes DOWN. A new one is a site that will raise at flip."
    )


def test_grep_would_have_been_useless_here():
    """Recorded because it justifies the tool existing. Raw greps report 113
    `replace(` and 66 `fields(` — `str.replace` and `model_fields` dominate. The
    AST walk resolves how `dataclasses` was imported per module and counts only
    real calls."""
    confirmed, suspected, other = _buckets()
    assert len(confirmed) + len(suspected) + len(other) < 40


def test_self_and_cls_resolve_to_their_enclosing_class():
    """The miss that the first classifier had: `asdict(self)` inside
    `ImageContent` is a contract site and reads as nothing by name."""
    confirmed, _, _ = _buckets()
    media = [s for s in confirmed if "media_config.py" in s["file"] and s["arg"] == "self"]
    assert len(media) >= 4, "self no longer resolves to the enclosing contract class"


def test_suspected_is_reported_rather_than_folded_into_either_side():
    """A tool that collapsed this bucket would state a number that is wrong in
    one direction or the other. Its existence is the honest part."""
    _, suspected, _ = _buckets()
    assert suspected, "the suspected bucket vanished — did the classifier start guessing again?"
    args = {s["arg"] for s in suspected}
    assert any("usage_obj" in a or "config_data" in a or "provider_charge" in a for a in args)
