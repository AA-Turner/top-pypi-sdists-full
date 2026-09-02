"""The code-execution content blocks must survive a storage round-trip.

Found while mapping the content-block family for Phase 1b.2 (the 19 *Content
classes are 19 of the 26 types in the contract closure).

Two things were wrong and they were the same thing twice:

  * to_storage_dict() omitted `metadata` while the field stayed declared, so
    anything set on it vanished on persist; and
  * parse_content() rebuilt these two types with _filter(), which keeps only
    keys whose name matches a dataclass field. That is the precise antipattern
    the long comment in parse_content condemns — it names three production
    incidents in three days from it (citations erased, Anthropic call_id
    erased, Gemini thoughtSignature erased) and states the rule that these
    branches "only normalize wire aliases and delegate" to the ONE
    deserializer. These two were the last canonical-storage types that did not.

LATENT, NOT AN OUTAGE: chat.message holds ZERO code_exec and ZERO code_result
blocks, which is why it was never noticed and why fixing it carries no risk to
existing rows. It mattered now because the pydantic family conversion would
have inherited the gap and pinned it as "correct".

The types also cross a spelling boundary — the dataclass discriminator is
"code_execution" but to_storage_dict writes "code_exec" — so both spellings are
pinned here.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.extra_config import CodeExecutionContent, CodeExecutionResultContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import reconstruct_content


def test_code_execution_metadata_survives_storage():
    original = CodeExecutionContent(
        code="print(1)", language="python", metadata={"trace_id": "t-1"}
    )
    rebuilt = reconstruct_content(original.to_storage_dict())

    assert isinstance(rebuilt, CodeExecutionContent)
    assert rebuilt.code == "print(1)"
    assert rebuilt.language == "python"
    assert rebuilt.metadata == {"trace_id": "t-1"}


def test_code_execution_result_metadata_survives_storage():
    original = CodeExecutionResultContent(
        output="1", outcome="success", metadata={"trace_id": "t-2"}
    )
    rebuilt = reconstruct_content(original.to_storage_dict())

    assert isinstance(rebuilt, CodeExecutionResultContent)
    assert rebuilt.output == "1"
    assert rebuilt.outcome == "success"
    assert rebuilt.metadata == {"trace_id": "t-2"}


def test_empty_metadata_is_still_omitted_from_storage():
    """No new key on the 99% path — the writer stays sparse, as every other
    to_storage_dict in this family is."""
    assert "metadata" not in CodeExecutionContent(code="x").to_storage_dict()
    assert "metadata" not in CodeExecutionResultContent(output="x").to_storage_dict()


@pytest.mark.parametrize(
    "wire_type,cls",
    [
        ("code_execution", CodeExecutionContent),          # the dataclass discriminator
        ("code_exec", CodeExecutionContent),               # what to_storage_dict writes
        ("code_execution_result", CodeExecutionResultContent),
        ("code_result", CodeExecutionResultContent),
    ],
)
def test_parse_content_accepts_both_spellings_and_keeps_metadata(wire_type, cls):
    """parse_content used to _filter these; now it delegates. Both spellings
    must land on the same class with metadata intact."""
    item = {"type": wire_type, "metadata": {"kept": True}}
    if cls is CodeExecutionContent:
        item |= {"code": "print(1)", "language": "python"}
    else:
        item |= {"output": "1", "outcome": "success"}

    parsed = UnifiedMessage.parse_content([item])

    assert len(parsed) == 1
    assert isinstance(parsed[0], cls)
    assert parsed[0].metadata == {"kept": True}


def test_the_filter_antipattern_is_gone_from_these_branches():
    """Forcing function: if someone reintroduces _filter for these types, the
    silent drop comes back and this fails."""
    import inspect

    from matrx_ai.config import message_config

    src = inspect.getsource(message_config.UnifiedMessage.parse_content)
    code_branch = src[src.index("code_execution") :]
    assert "_filter" not in code_branch, "the code-execution branches use _filter again"
