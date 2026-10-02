"""A Sources entry is truthful or absent — never wrong (W-37).

PB-04 (2026-10-01, conversation 548c09c9…): the reply's Sources list cited the
customs PDF's page-3 fact as "p.1" and credited facts to sources that do not
contain them — the CSV's crate tag to the PDF, the building manager to an
unrelated note — and titled notes "note". The citations below are the real
ones from that reply, trimmed.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

from matrx_ai.config import TextContent
from matrx_ai.config.citations import citable_wire_blocks_from_output, citation_supports_claim
from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
from matrx_ai.tools.implementations.rag import _citable_blocks_for_hits

PDF_TEXT = (
    "Move 4472 — International customs packet\nCompass Route Relocation Advisors — Page 1 of 4 "
    "— Cover\nShipper: Ilves household goods consignment (split load with Move 4471).\n\n"
    "Broker assignment\nCompass Route Relocation Advisors — Page 3 of 4\nThe customs broker of "
    "record for this consignment is Aduanas Rivera Morales, Nuevo Laredo office.\n"
    "Customs broker file: CB-60417"
)
ROUTING_NOTE = (
    "Move 4471 — routing\n\n# Move 4471 — routing\n\nClient: Delgado family, Alameda → "
    "international.\nCarrier: Pacific Crest Van Lines, tractor 214.\nRouting line: (pending)"
)
WAREHOUSE_NOTE = (
    "Oakland warehouse — customer pickup desk\n\nItems held for Move 4472 are staged in "
    "warehouse unit W-318 until the delivery truck is loaded."
)
RULES_TAIL = (
    "Final provision. Every moving company must deliver a certificate of insurance before the "
    "move date. The certificate must name, as additional insured, exactly: Larchmont Tower "
    "Owners Association of Oakland."
)


def _cite(index: int, title: str, source: str, cited_text: str) -> dict:
    return {
        "type": "search_result_location",
        "search_result_index": index,
        "title": title,
        "source": source,
        "cited_text": cited_text,
        "start_block_index": 0,
        "end_block_index": 1,
    }


PDF_P1 = "matrx://file/b9eb9293?page=1"

# (answer span, its citation, should the citation survive)
PB04 = [
    ('"Upright piano, Yamaha U1",CT-2286,Living,3-person, crated',
     _cite(1, "cld_file — page 1", PDF_P1, PDF_TEXT), False),
    ("ask the front desk to page the building manager, Desmond Achterberg",
     _cite(0, "note", "matrx://unknown", ROUTING_NOTE), False),
    ("Every moving company must deliver a certificate of insurance before the move date. The "
     "certificate must name, as additional insured, exactly: Larchmont Tower Owners Association "
     "of Oakland.", _cite(18, "rules.txt — page 10", "matrx://file/ec92460c?page=10", RULES_TAIL), True),
    ("Items held for Move 4472 are staged in warehouse unit W-318 until the delivery truck is loaded.",
     _cite(4, "note", "matrx://unknown", WAREHOUSE_NOTE), True),
    ("the customs broker of record for this consignment is Aduanas Rivera Morales, Nuevo Laredo "
     "office. Customs broker file: CB-60417", _cite(1, "cld_file — page 1", PDF_P1, PDF_TEXT), True),
]


def test_stored_citations_keep_only_the_ones_whose_source_holds_the_claim() -> None:
    for claim, citation, survives in PB04:
        block = TextContent.from_anthropic({"type": "text", "text": claim, "citations": [citation]})
        kept = block.metadata.get("citations") or []
        assert bool(kept) is survives, f"{claim[:50]!r} → {citation['title']}"


def test_a_paraphrase_that_keeps_the_code_and_words_is_still_grounded() -> None:
    assert citation_supports_claim("The broker file number is CB-60417.", PDF_TEXT)
    assert not citation_supports_claim("The broker file number is CB-60418.", PDF_TEXT)
    assert citation_supports_claim("", PDF_TEXT) and citation_supports_claim("x", None)


def test_live_citations_are_sent_only_for_the_claim_they_support() -> None:
    sent: list = []

    class _Emitter:
        async def send_citation(self, payload):
            sent.append(payload)

        async def send_chunk(self, text):
            pass

        async def send_reasoning_state(self, state):
            pass

    chat = AnthropicChat.__new__(AnthropicChat)
    chat.debug = False
    emitter = _Emitter()

    async def run() -> None:
        for index, (claim, citation, _) in enumerate(PB04):
            await chat._handle_event(
                SimpleNamespace(type="content_block_delta", index=index,
                                delta=SimpleNamespace(type="citations_delta", citation=citation)),
                emitter,
            )
            assert sent == [] or all(p.block_index < index for p in sent)  # held until stop
            await chat._handle_event(
                SimpleNamespace(type="content_block_delta", index=index,
                                delta=SimpleNamespace(type="text_delta", text=claim)),
                emitter,
            )
            await chat._handle_event(SimpleNamespace(type="content_block_stop", index=index), emitter)

    asyncio.run(run())
    assert [p.block_index for p in sent] == [i for i, (_, _, ok) in enumerate(PB04) if ok]


def test_a_passage_spanning_pages_claims_no_single_page_and_notes_carry_their_title() -> None:
    hits = [
        {"source_kind": "cld_file", "source_id": "b9eb9293", "snippet": PDF_TEXT,
         "page_numbers": [1, 2, 3, 4], "metadata": {"source": {"title": None}},
         "processed_document_id": "8f0e4285"},
        {"source_kind": "cld_file", "source_id": "ec92460c", "snippet": RULES_TAIL,
         "page_numbers": [10], "metadata": {"file_name": "larchmont-tower-move-in-rules.txt"}},
        {"source_kind": "note", "source_id": "74b926db", "snippet": WAREHOUSE_NOTE,
         "page_numbers": [], "metadata": {"source": {"title": "Oakland warehouse — customer pickup desk"}}},
    ]
    blocks = [b for b in _citable_blocks_for_hits(hits) if getattr(b, "type", "") == "search_result"]
    pdf, rules, note = blocks
    assert pdf.page is None and pdf.title.endswith("pages 1–4")
    assert "page=" not in pdf.to_anthropic()["source"]
    assert rules.page == 10 and rules.title == "larchmont-tower-move-in-rules.txt — page 10"
    assert note.title == "Oakland warehouse — customer pickup desk"

    # The resend path (rebuilt from the stored tool output) says the same.
    wire = citable_wire_blocks_from_output("knowledge_search", {"hits": hits})
    assert wire is not None
    titles = [b["title"] for b in wire[:3]]
    assert titles[0].endswith("pages 1–4") and "page=" not in wire[0]["source"]
    assert titles[2] == "Oakland warehouse — customer pickup desk"


def test_grounding_keeps_true_paraphrases_and_reformatted_numbers() -> None:
    # Review 2026-10-01: the first check dropped all of these correct citations.
    true_pairs = [
        ("Delivery window is Oct 14 06:00–09:00.", "Deliveries: October 14, 06:00-09:00."),
        ("Oct 14 06:00–09:00", "14 October, 6:00 to 9:00"),
        ("$1,250.00", "$1250"),
        ("14th", "October 14"),
        ("5kg", "5 kg"),
        ("Inspections happen weekly at the depot", "The depot is inspected every week"),
        ("倉庫ユニットはW-318です", "倉庫ユニットW-318に保管"),
    ]
    for claim, source in true_pairs:
        assert citation_supports_claim(claim, source), claim
    # ... and still refuses the wrong source, in any script.
    assert not citation_supports_claim("倉庫の住所は東京です 318", "大阪の事務所 318")


def test_a_span_citing_two_sources_keeps_each_that_holds_its_part() -> None:
    from matrx_ai.config.citations import grounded_citations

    claim = "Crate tag is C-114; building manager is Dana Ortiz."
    citations = [
        {"kind": "search_result", "provider": "anthropic", "title": "inventory.csv", "cited_text": "Crate tag: C-114"},
        {"kind": "search_result", "provider": "anthropic", "title": "contact note", "cited_text": "Building manager: Dana Ortiz"},
        {"kind": "search_result", "provider": "anthropic", "title": "routing note", "cited_text": ROUTING_NOTE},
    ]
    assert [c["title"] for c in grounded_citations(claim, citations)] == ["inventory.csv", "contact note"]
