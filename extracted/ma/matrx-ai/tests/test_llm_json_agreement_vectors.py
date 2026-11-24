"""FORCING FUNCTION: the server's one LLM-output JSON funnel and the browser's agree.

The server reads a model's JSON through ``matrx_ai.agents.response_parser.extract_json``;
the browser reads the same answer through ``@ai-matrx/content-ir/json-extract``
``extractFirstJson(text, { allowFuzzy: true })`` (the rule the streaming JSON tracker's
``finalize()`` ends on). Python cannot import the TypeScript rule, so the two are held
together by vectors GENERATED from it
(``apps/shared/content-ir-core/__tests__/llm-json-agreement-vectors.json``, never
hand-edited) whose byte-identical copy is ``tests/fixtures/llm_json_agreement_vectors.json``
(the copy-equals-source check is a host contract:
``tests/package_host_contracts/matrx_ai_parity/test_llm_json_vectors_copy_matches_source.py``).
A vector the two sides answer differently on purpose carries ``differs`` with the reason.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_ai.agents.response_parser import extract_json

_PACKAGE_ROOT = Path(__file__).resolve().parents[1]
_FIXTURE = _PACKAGE_ROOT / "tests" / "fixtures" / "llm_json_agreement_vectors.json"

_VECTORS = json.loads(_FIXTURE.read_text(encoding="utf-8"))["vectors"]


@pytest.mark.parametrize("vector", [v for v in _VECTORS if "differs" not in v], ids=lambda v: v["name"])
def test_extract_json_gives_the_browser_answer(vector: dict) -> None:
    got = extract_json(vector["text"])
    # json.dumps compares key order too (a __kind document keeps its order on both sides).
    assert json.dumps(got) == json.dumps(vector["value"])


@pytest.mark.parametrize("vector", [v for v in _VECTORS if "differs" in v], ids=lambda v: v["name"])
def test_a_declared_difference_still_differs(vector: dict) -> None:
    # When the two sides converge, the `differs` note is stale: delete it in the generator.
    assert json.dumps(extract_json(vector["text"])) != json.dumps(vector["value"]), vector["differs"]
