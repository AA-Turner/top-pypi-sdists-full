"""Grail phase #2 STEP 2 — the flat→graph mapper (nx_brain_local.flat_to_node / infer_node_type).

Proves a flat CLI memory maps to a valid typed-node body for POST /api/brain/cli-write. Pure + deterministic.
Run: python3 nx/cli/tests/test_brain_mapper.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_brain_local as B


def test_basic_shape():
    n = B.flat_to_node(content="Acme signed the pilot", label="Acme pilot", world="sales", source="crm",
                       metadata={"deal_id": "d1"})
    assert n["nodeType"] in B.VALID_NODE_TYPES
    assert n["label"] == "Acme pilot"
    assert n["payload"]["content"] == "Acme signed the pilot"
    assert n["payload"]["world"] == "sales"
    assert n["payload"]["meta"] == {"deal_id": "d1"}
    assert n["sourceAttribution"]["sourceKind"] == "nx-cli"        # provenance always stamped
    assert n["sourceAttribution"]["world"] == "sales"
    assert n["sourceAttribution"]["source"] == "crm"
    assert "sourceWorld" not in n                                   # left unset → route defaults source_world='cli'


def test_node_type_inference():
    assert B.infer_node_type(label="ICP fit", content="mid-market SaaS") == "concept"          # default
    assert B.infer_node_type(content="pricing tiers", source="https://stripe.com/pricing") == "source"
    assert B.infer_node_type(content="notes", metadata={"url": "x"}) == "source"
    assert B.infer_node_type(content="Should we raise now?") == "returning_question"            # ends with ?
    assert B.infer_node_type(content="We decided to ship the preview first") == "decision"
    # every inference output is a valid M387 node_type
    for probe in ("a", "a?", "we chose x", "http source", ""):
        assert B.infer_node_type(content=probe) in B.VALID_NODE_TYPES


def test_label_derivation_and_truncation():
    # no label → derive from the first content line, capped at 80
    n = B.flat_to_node(content="First line is the label\nsecond line ignored", label="")
    assert n["label"] == "First line is the label"
    long = "x" * 500
    n2 = B.flat_to_node(content=long, label=long)
    assert len(n2["label"]) == 200                                 # label capped at 200
    n3 = B.flat_to_node(content="", label="")
    assert n3["label"] == "note"                                   # empty everything → safe fallback


def test_minimal_and_empty_fields():
    n = B.flat_to_node(content="just content")
    assert n["payload"] == {"content": "just content"}             # no world/meta keys when absent
    assert n["sourceAttribution"] == {"sourceKind": "nx-cli"}      # only sourceKind when no world/source
    n2 = B.flat_to_node(content="", label="titled")
    assert "content" not in n2["payload"]                          # empty content → not stored
    assert n2["nodeType"] in B.VALID_NODE_TYPES


if __name__ == "__main__":
    for name, fn in sorted((n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)):
        fn(); print(f"  ✓ {name}")
    print("ALL FLAT→GRAPH MAPPER PROOFS PASS")
