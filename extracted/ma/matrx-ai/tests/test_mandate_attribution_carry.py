"""Every run built for a mandate carries the mandate onto its OWN records.

Three seams, each tested against the real function (no doubles of the code under test):

* ``executor._carry_mandate_attribution`` — a held code call (mandate resolved, agent
  built, plain ``run_agent``) puts the key on the child context, not the parent's;
* ``conversation_gate._with_mandate_attribution`` — the new conversation row carries the
  context's ``mandate_key`` (a nested / workflow run shares its parent's request);
* ``mandates.stamp_mandate_attribution`` — a NamedAgent mandate run gets its own request
  record (``independent_request``), like ``run_mandate``.

Planted proof: make ``_carry_mandate_attribution`` return early, ``_with_mandate_attribution``
return ``metadata`` unchanged, or drop the ``independent_request`` line — the matching test
goes red.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from pydantic import BaseModel

from matrx_ai.agents.executor import _carry_mandate_attribution
from matrx_ai.agents.named import NamedAgent
from matrx_ai.db.conversation_gate import _with_mandate_attribution
from matrx_ai.mandates import stamp_mandate_attribution


def test_held_call_agent_carries_its_mandate_over_the_parents() -> None:
    agent = SimpleNamespace(matrx_mandate_key="knowledge.document_verifier", request_metadata={})
    child = {"mandate_key": "chat.default_new_chat", "mandate_attribution": "sole_holder"}
    _carry_mandate_attribution(agent, child)
    assert child == {"mandate_key": "knowledge.document_verifier"}
    assert agent.request_metadata == {"mandate_key": "knowledge.document_verifier"}


def test_named_agent_request_metadata_key_is_carried() -> None:
    agent = SimpleNamespace(request_metadata={"mandate_key": "rag.pdf_page_cleaner"})
    child: dict[str, Any] = {}
    _carry_mandate_attribution(agent, child)
    assert child["mandate_key"] == "rag.pdf_page_cleaner"


def test_agent_without_mandate_changes_nothing_and_never_raises() -> None:
    child = {"mandate_key": "parent.key"}
    _carry_mandate_attribution(SimpleNamespace(), child)
    assert child == {"mandate_key": "parent.key"}

    class _Boom:
        @property
        def request_metadata(self) -> Any:
            raise RuntimeError("boom")

    _carry_mandate_attribution(_Boom(), child)  # loud, never raises
    assert child == {"mandate_key": "parent.key"}


def test_new_conversation_row_carries_the_runs_mandate() -> None:
    ctx = SimpleNamespace(metadata={"mandate_key": "masterwork.rulebook_auditor",
                                    "mandate_attribution": "sole_holder", "other": 1})
    assert _with_mandate_attribution({}, ctx) == {
        "mandate_key": "masterwork.rulebook_auditor",
        "mandate_attribution": "sole_holder",
    }
    # An explicit row key wins; no context / no key leaves the row as it was.
    assert _with_mandate_attribution({"mandate_key": "x.y"}, ctx) == {"mandate_key": "x.y"}
    assert _with_mandate_attribution({}, None) == {}
    assert _with_mandate_attribution({"a": 1}, SimpleNamespace(metadata={})) == {"a": 1}
    assert _with_mandate_attribution({}, SimpleNamespace(metadata="not a dict")) == {}


class _Cleaner(NamedAgent):
    name = "rag_pdf_page_cleaner"
    mandate_key = "rag.pdf_page_cleaner"

    class Inputs(BaseModel):
        raw_text: str


def test_named_mandate_run_is_stamped_with_its_mandate() -> None:
    # Its own request record needs no flag: every child agent run owns its turn.
    kwargs: dict[str, Any] = {"source_feature": "rag", "request_metadata": {"rag_job": "p"}}
    stamp_mandate_attribution(kwargs, "rag.pdf_page_cleaner", _Cleaner)
    assert "independent_request" not in kwargs
    assert kwargs["source_feature"] == "mandate:rag.pdf_page_cleaner"
    assert kwargs["request_metadata"]["mandate_key"] == "rag.pdf_page_cleaner"
