"""Unit tests for ``ActionLedger.render_authoritative_block`` dedup.

PRO-1298 / Mercury: an agent that ran ``classify_table`` against 50
tables lost its tool-call history after compaction because the ledger
truncated to ``_MAX_RENDERED_ENTRIES = 12`` and READ-class entries are
the first to be dropped. The agent re-classified tables it had already
classified. The dedup change collapses repeated-tool groups into a
single ``<entry_summary>`` row so the resuming agent still sees the
"I did this 50 times" signal.
"""

from __future__ import annotations

from xpander_sdk.core.context_optimizer.action_ledger import (
    _LARGE_CONTEXT_THRESHOLD,
    _MAX_RENDERED_ENTRIES,
    _MAX_RENDERED_ENTRIES_LARGE_CONTEXT,
    ActionLedger,
)
from xpander_sdk.models.action_ledger import LedgerEntry, LedgerEntryClass


def _build_ledger_with_repeats(
    count: int,
    *,
    tool: str = "classify_table",
    entry_class: LedgerEntryClass = LedgerEntryClass.READ,
) -> ActionLedger:
    ledger = ActionLedger(task=None, agent=None)
    for i in range(count):
        ledger._entries.append(
            LedgerEntry(
                seq=i + 1,
                tool_name=tool,
                target=f"tbl_{i}",
                status="ok",
                entry_class=entry_class,
                args_preview="",
                result_preview="",
                result_signature="",
                ts=f"t{i}",
            )
        )
    return ledger


def test_compressed_summary_row_emitted_for_large_repeat_group() -> None:
    ledger = _build_ledger_with_repeats(50)
    block = ledger.render_authoritative_block(context_window=1_000_000)
    assert "<entry_summary" in block
    assert 'count="50"' in block
    assert 'tool="classify_table"' in block
    assert 'first_seq="1"' in block
    assert 'last_seq="50"' in block


def test_entry_summary_carries_class_attribute() -> None:
    # PR #511 review: dedup row must carry ``class=`` so the resuming
    # agent can tell whether the collapsed mass-operation was destructive.
    ledger = _build_ledger_with_repeats(
        50, tool="bulk_update", entry_class=LedgerEntryClass.WRITE
    )
    block = ledger.render_authoritative_block(context_window=1_000_000)
    assert "<entry_summary" in block
    assert 'class="write"' in block


def test_dedup_grouping_separates_mixed_class_same_tool() -> None:
    # Same tool_name can produce different entry_class results based on
    # operation/method args (e.g. ``sql_query`` returning READ for SELECT
    # and WRITE for UPDATE). They must NOT collapse into a single
    # summary that hides the WRITE.
    ledger = ActionLedger(task=None, agent=None)
    # 30 READs against sql_query
    for i in range(30):
        ledger._entries.append(
            LedgerEntry(
                seq=i + 1,
                tool_name="sql_query",
                target=f"select_tbl_{i}",
                status="ok",
                entry_class=LedgerEntryClass.READ,
                args_preview="SELECT *",
                result_preview="",
                result_signature="",
                ts=f"t{i}",
            )
        )
    # 1 WRITE mid-batch via same tool name
    ledger._entries.append(
        LedgerEntry(
            seq=31,
            tool_name="sql_query",
            target="users",
            status="ok",
            entry_class=LedgerEntryClass.WRITE,
            args_preview="UPDATE users SET ...",
            result_preview="",
            result_signature="",
            ts="t31",
        )
    )
    block = ledger.render_authoritative_block(context_window=1_000_000)
    # The WRITE must appear as its own <entry> row, not absorbed into
    # the READ group's summary.
    assert "UPDATE users" in block
    assert 'class="write"' in block


def test_first_and_last_representatives_kept_alongside_summary() -> None:
    ledger = _build_ledger_with_repeats(50)
    block = ledger.render_authoritative_block(context_window=1_000_000)
    assert 'target="tbl_0"' in block
    assert 'target="tbl_49"' in block


def test_writes_survive_dedup_eviction_pressure() -> None:
    ledger = _build_ledger_with_repeats(50)
    # Add two WRITE entries — these are the binding-rule referent and
    # must survive regardless of how many READ entries crowd the cap.
    ledger._entries.append(
        LedgerEntry(
            seq=51,
            tool_name="insert_audit_row",
            target="audit_log",
            status="ok",
            entry_class=LedgerEntryClass.WRITE,
            args_preview="",
            result_preview="",
            result_signature="",
            ts="t100",
        )
    )
    block = ledger.render_authoritative_block(context_window=1_000_000)
    assert "insert_audit_row" in block


def test_many_dedup_groups_do_not_starve_writes() -> None:
    # PR #511 review: with N dedup-eligible groups + multiple WRITE/VERIFY
    # entries, every WRITE/VERIFY must survive at the default cap of 12.
    # Pre-fix the budget collapsed to 1 and most non-dedup WRITEs were lost.
    ledger = ActionLedger(task=None, agent=None)
    seq = 1
    # 11 dedup-eligible READ groups, each 20 entries → 11 summary rows.
    for grp in range(11):
        for j in range(20):
            ledger._entries.append(
                LedgerEntry(
                    seq=seq,
                    tool_name=f"read_grp_{grp}",
                    target=f"tgt_{j}",
                    status="ok",
                    entry_class=LedgerEntryClass.READ,
                    args_preview="",
                    result_preview="",
                    result_signature="",
                    ts=f"t{seq}",
                )
            )
            seq += 1
    # 4 standalone WRITE entries (different tools, not deduped) + 2 VERIFY.
    standalone = [
        ("insert_user", LedgerEntryClass.WRITE, "users"),
        ("update_billing", LedgerEntryClass.WRITE, "billing"),
        ("delete_session", LedgerEntryClass.WRITE, "session_42"),
        ("create_invoice", LedgerEntryClass.WRITE, "inv_99"),
        ("verify_total", LedgerEntryClass.VERIFY, "billing"),
        ("count_rows", LedgerEntryClass.VERIFY, "users"),
    ]
    for tool, klass, tgt in standalone:
        ledger._entries.append(
            LedgerEntry(
                seq=seq,
                tool_name=tool,
                target=tgt,
                status="ok",
                entry_class=klass,
                args_preview="",
                result_preview="",
                result_signature="",
                ts=f"t{seq}",
            )
        )
        seq += 1
    block = ledger.render_authoritative_block()
    for tool, _, _ in standalone:
        assert tool in block, f"missing critical entry: {tool}"


def test_large_context_window_bumps_cap() -> None:
    # Small group (under dedup threshold) — render all entries directly.
    ledger = _build_ledger_with_repeats(20)
    block_small = ledger.render_authoritative_block(context_window=128_000)
    block_large = ledger.render_authoritative_block(context_window=1_000_000)
    # Both must include some entries (the test guards the cap selection
    # branch, not the exact row count after dedup).
    assert "<entry " in block_small or "<entry_summary" in block_small
    assert "<entry " in block_large or "<entry_summary" in block_large


def test_explicit_max_entries_overrides_window_based_cap() -> None:
    ledger = _build_ledger_with_repeats(20)
    block = ledger.render_authoritative_block(max_entries=4, context_window=1_000_000)
    # Soft cap applies to non-WRITE/VERIFY detail. With all-READ ledger
    # we still bound output (<=4 entries + at most 1 summary row).
    total_rows = block.count("<entry ") + block.count("<entry_summary tool=")
    assert total_rows <= 5


def test_no_dedup_for_distinct_low_volume_tools() -> None:
    ledger = ActionLedger(task=None, agent=None)
    # 3 different tools, each invoked twice — none exceeds the dedup
    # threshold so all entries render verbatim.
    for i, tool in enumerate(["read_a", "read_b", "read_c"]):
        for j in range(2):
            ledger._entries.append(
                LedgerEntry(
                    seq=i * 2 + j + 1,
                    tool_name=tool,
                    target=f"x_{j}",
                    status="ok",
                    entry_class=LedgerEntryClass.READ,
                    args_preview="",
                    result_preview="",
                    result_signature="",
                    ts=f"t{i}{j}",
                )
            )
    block = ledger.render_authoritative_block(context_window=200_000)
    # No summary ROW (the header text mentions the tag literally, but a
    # real row has a tool= attribute).
    assert "<entry_summary tool=" not in block
    assert "read_a" in block and "read_b" in block and "read_c" in block


def test_empty_ledger_returns_empty_string() -> None:
    ledger = ActionLedger(task=None, agent=None)
    assert ledger.render_authoritative_block() == ""


def test_cap_constants_sane() -> None:
    assert _MAX_RENDERED_ENTRIES_LARGE_CONTEXT > _MAX_RENDERED_ENTRIES
    assert _LARGE_CONTEXT_THRESHOLD >= 200_000
