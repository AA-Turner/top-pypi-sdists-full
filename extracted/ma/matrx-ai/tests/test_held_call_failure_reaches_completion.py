"""A held call that FAILED must reach its mandate's post-run check — not crash it.

``HeldCall.finish(success=False)`` built ``AgentRunResult(error_kind="provider")``,
a value outside ``ErrorKind`` (``"execution" | "parse" | None``). Every held
site's failure path (``run_held_call``, ``run_held_pydantic``, ``run_held_text``
and ~10 host sites) therefore raised a pydantic ValidationError from inside its
``except`` block, masking the provider's real error and never recording the
failure. Found 2026-09-26 converting the cleanup-check bake-off (BYPASS-CENSUS).
"""

from __future__ import annotations

import asyncio

from matrx_ai.mandates import HeldCall


def _held(seen: list) -> HeldCall:
    async def complete(result, variables, spilled):  # noqa: ANN001
        seen.append(result)

    return HeldCall(
        mandate_key="checks.cleanup_bakeoff.answer",
        model="claude-sonnet-5",
        system="s",
        temperature=None,
        max_output_tokens=None,
        turns=[],
        config=None,
        metadata={},
        complete=complete,
    )


def test_a_failed_held_call_reaches_its_completion() -> None:
    seen: list = []
    asyncio.run(_held(seen).finish("", success=False, error="RuntimeError: provider 529"))
    assert len(seen) == 1
    assert seen[0].success is False
    assert seen[0].error == "RuntimeError: provider 529"
    assert seen[0].error_kind == "execution"


def test_a_succeeded_held_call_carries_no_error_kind() -> None:
    seen: list = []
    asyncio.run(_held(seen).finish('{"ok": true}', parsed={"ok": True}))
    assert seen[0].success is True and seen[0].error_kind is None


def test_a_parsed_dict_reaches_the_post_run_check_as_a_dict_not_a_bare_model() -> None:
    """``AgentRunResult.parsed`` is typed as a pydantic model: a dict was coerced into a bare ``BaseModel()`` that cannot
    be dumped or printed, so every held site that parses its own JSON failed its post-run check ("BaseModel cannot be
    instantiated directly", seen on the AI-column fill 2026-10-19)."""
    seen: list = []
    asyncio.run(_held(seen).finish('{"value": "x"}', parsed={"value": "x"}))
    assert seen[0].parsed == {"value": "x"}
    repr(seen[0])  # a bare BaseModel raised here


def test_a_parsed_list_is_kept_too() -> None:
    seen: list = []
    asyncio.run(_held(seen).finish("[1]", parsed=[1]))
    assert seen[0].parsed == [1]
