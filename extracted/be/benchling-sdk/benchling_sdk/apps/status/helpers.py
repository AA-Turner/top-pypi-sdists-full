from __future__ import annotations

from benchling_sdk.apps.status.types import ReferencedSessionLinkType


def ref(reference: ReferencedSessionLinkType) -> str:
    """
    Ref.

    Helper method for easily serializing a referenced object into a string embeddable in AppSessionMessageCreate
    content.

    Example:
        dna_sequence = benchling.dna_sequences.get_by_id("seq_1234")
        AppSessionMessageCreate(f"This is my DNA sequence {ref(dna_sequence)} for analysis")

    """
    return ref_by_id(reference.id)


def ref_by_id(reference_id: str) -> str:
    """
    Ref by ID.

    Helper method for serializing a reference to an object into a string embeddable in
    AppSessionMessageCreate content via the reference object's id. This is helpful when clients
    don't already have access to the referenced object.

    Example:
        dna_sequence_id: str = "seq_asQya4lk"
        AppSessionMessageCreate(f"This is my DNA sequence {ref_by_id(dna_sequence_id)} for analysis")

    """
    assert reference_id, "reference_id cannot be empty or None"
    return _encode_id(reference_id)


def _encode_id(id: str) -> str:
    """Not sure {} are possible in Benchling IDs, but the spec says we're escaping."""
    escaped_id = id.replace("{", "\\{").replace("}", "\\}")
    return f"{{id:{escaped_id}}}"
