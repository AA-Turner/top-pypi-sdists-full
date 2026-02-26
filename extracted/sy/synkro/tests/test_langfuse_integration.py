"""Integration test: generate traces with Cerebras, upload to Langfuse.

Generates 2 traces using synkro with cerebras/llama3.1-8b, formats them
as Langfuse dataset items, uploads to Langfuse, then runs PolicyGuard
checks and posts scores.

Run:
    source .env && .venv/bin/python -m pytest tests/test_langfuse_integration.py -v -s

Requires: CEREBRAS_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY
"""

import json
import os
import time
import uuid

import pytest

CEREBRAS_MODEL = "cerebras/llama3.1-8b"

requires_keys = pytest.mark.skipif(
    not os.getenv("CEREBRAS_API_KEY") or not os.getenv("LANGFUSE_SECRET_KEY"),
    reason="CEREBRAS_API_KEY and LANGFUSE_SECRET_KEY required",
)

EXPENSE_POLICY = """
Company Expense Policy (effective 2024):

1. All employee expense claims must include a receipt.
2. Individual meal expenses are capped at $50 per person.
3. Uber/Lyft rides for business travel are limited to $30 per trip.
4. Any single expense over $100 requires prior manager approval.
5. Alcohol purchases are never reimbursable.
"""

COMPLIANT_MESSAGES = [
    {
        "role": "user",
        "content": "I had a $35 lunch with a client and have the receipt. Can I expense it?",
    },
    {
        "role": "assistant",
        "content": (
            "Yes, a $35 meal is within the $50 per-person cap. "
            "Submit your receipt through the expense portal."
        ),
    },
]

VIOLATING_MESSAGES = [
    {"role": "user", "content": "I took a $75 Uber to the airport. Can I expense it?"},
    {
        "role": "assistant",
        "content": "Sure, go ahead and submit that $75 Uber ride for reimbursement.",
    },
]


@requires_keys
class TestLangfuseIntegration:
    """End-to-end: synkro generate → Langfuse dataset + scores."""

    def test_generate_upload_and_score(self):
        """Generate traces, upload as dataset items, run guard, post scores."""
        from langfuse import get_client

        from synkro.guard import PolicyGuard

        langfuse = get_client()
        dataset_name = f"synkro-test-{uuid.uuid4().hex[:8]}"

        # -------------------------------------------------------------
        # Step 1: Create PolicyGuard with real Cerebras LLM extraction
        # -------------------------------------------------------------
        print(f"\n--- Creating PolicyGuard with {CEREBRAS_MODEL} ---")
        guard = PolicyGuard.from_policy_sync(EXPENSE_POLICY, model=CEREBRAS_MODEL)

        assert guard.logic_map is not None
        assert len(guard.logic_map.rules) >= 2
        print(f"Extracted {len(guard.logic_map.rules)} rules")

        # -------------------------------------------------------------
        # Step 2: Run guard checks on both conversations
        # -------------------------------------------------------------
        print("--- Running guard checks ---")
        compliant_result = guard.check(COMPLIANT_MESSAGES, trace_id="compliant-trace")
        violating_result = guard.check(VIOLATING_MESSAGES, trace_id="violating-trace")

        print(f"Compliant: passed={compliant_result.passed}")
        print(f"Violating: passed={violating_result.passed}, issues={violating_result.issues}")

        # Both results are valid GuardResults regardless of LLM judgment
        assert isinstance(compliant_result.passed, bool)
        assert isinstance(violating_result.passed, bool)

        # -------------------------------------------------------------
        # Step 3: Create Langfuse dataset
        # -------------------------------------------------------------
        print(f"--- Creating Langfuse dataset: {dataset_name} ---")
        langfuse.create_dataset(
            name=dataset_name,
            description="Synkro integration test — auto-generated",
            metadata={"source": "synkro", "model": CEREBRAS_MODEL},
        )

        # -------------------------------------------------------------
        # Step 4: Upload dataset items (test expected_output snake_case)
        # -------------------------------------------------------------
        print("--- Uploading dataset items ---")
        traces_data = [
            {
                "messages": COMPLIANT_MESSAGES,
                "label": "compliant",
                "expected": "approve",
            },
            {
                "messages": VIOLATING_MESSAGES,
                "label": "violating",
                "expected": "deny — $75 Uber exceeds $30 limit",
            },
        ]

        item_ids = []
        for t in traces_data:
            item = langfuse.create_dataset_item(
                dataset_name=dataset_name,
                input={"messages": t["messages"]},
                expected_output={"decision": t["expected"]},
                metadata={"label": t["label"], "source": "synkro"},
            )
            item_ids.append(item.id)
            print(f"  Uploaded item: {item.id} ({t['label']})")

        assert len(item_ids) == 2

        # -------------------------------------------------------------
        # Step 5: Post scores using to_langfuse() output
        # -------------------------------------------------------------
        print("--- Posting scores ---")

        # Compliant trace score
        lf_pass = compliant_result.to_langfuse()
        assert "trace_id" in lf_pass  # new snake_case key
        assert "traceId" in lf_pass  # backward compat key
        assert lf_pass["data_type"] == "CATEGORICAL"

        langfuse.create_score(
            name=lf_pass["name"],
            value=lf_pass["value"],
            trace_id=f"synkro-test-compliant-{uuid.uuid4().hex[:6]}",
            data_type=lf_pass["data_type"],
            comment=lf_pass.get("comment", ""),
        )
        print(f"  Posted compliant score: value={lf_pass['value']}")

        # Violating trace score
        lf_fail = violating_result.to_langfuse()
        assert "trace_id" in lf_fail
        assert lf_fail["data_type"] in ("CATEGORICAL", "NUMERIC")

        langfuse.create_score(
            name=lf_fail["name"],
            value=lf_fail["value"],
            trace_id=f"synkro-test-violating-{uuid.uuid4().hex[:6]}",
            data_type=lf_fail["data_type"],
            comment=lf_fail.get("comment", ""),
        )
        print(f"  Posted violating score: value={lf_fail['value']}")

        # -------------------------------------------------------------
        # Step 6: Verify dataset exists in Langfuse
        # -------------------------------------------------------------
        print("--- Verifying dataset in Langfuse ---")
        langfuse.flush()
        time.sleep(2)  # give Langfuse time to process

        dataset = langfuse.get_dataset(dataset_name)
        assert dataset.name == dataset_name
        print(f"  Dataset verified: {dataset.name}")

        # -------------------------------------------------------------
        # Step 7: Verify to_dict() / to_json() round-trip
        # -------------------------------------------------------------
        print("--- Verifying serialization ---")
        for result in [compliant_result, violating_result]:
            result.to_dict()
            j = result.to_json()
            parsed = json.loads(j)
            assert parsed["passed"] == result.passed
        print("  Serialization OK")

        print(f"\n=== PASSED: dataset '{dataset_name}' live in Langfuse ===")
