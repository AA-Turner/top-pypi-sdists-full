"""The human-answer contract is declared by the node that emits it."""

from matrx_graph.content_ir.sdk import kind_catalog
from matrx_graph.nodes.control.human_input import HumanInputOutput


def test_human_answer_is_discovered_from_its_owning_output_model() -> None:
    """Removing the SDK decorator makes this catalog discovery fail."""
    registration = kind_catalog()["human_answer"]

    assert registration.model is HumanInputOutput
    assert registration.label == "Human Answer"
    assert registration.family == "control_flow"


def test_human_answer_schema_keeps_the_live_open_map_marker_contract() -> None:
    """Dropping this marker would make the publisher refuse the live schema."""
    schema = kind_catalog()["human_answer"].json_schema()

    assert schema["properties"]["extras"]["properties"]["__kind"] == {
        "type": "string",
        "description": "The registered kind this payload is an instance of, when it is one.",
    }
    # A closed sub-object has no identity and declares NO marker (rule 31: never a
    # blank ``const ""``). The compatibility gate accepts removing the live blank.
    assert "__kind" not in schema["$defs"]["DecisionProvenance"]["properties"]
