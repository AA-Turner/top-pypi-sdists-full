"""Playwright E2E tests for the save_memory tool (#217).

Agent-initiated candidates must flow through the same promotion pipeline
as user-initiated ones, so they appear in the shipped #920 memory Review
tab and can be approved via the existing buttons without any tool-specific
UI. These tests exercise that parity end-to-end.

Two surfaces:

- **API smoke** — POST /api/memory/candidates with ``proposer="agent"`` and
  verify: lineage stamps actor="agent", provenance carries the conversation
  id, and the candidate is visible in the review queue.
- **Browser round trip** — candidate posted via API (simulating a tool call),
  then driven through the shipped Review tab to approve, asserting the
  memory moves to the Active tab.

The full browser path — stub an LLM turn, intercept the tool call, exercise
the in-chat approval modal — is deferred to the feature-parity eval suite
(#892). The tests below lock in the pipeline + UI contract the tool depends
on.

Requires playwright: ``pip install playwright && playwright install chromium``.
"""

from __future__ import annotations

import pytest

HAS_PLAYWRIGHT = True
try:
    from playwright.sync_api import Page, expect
except ImportError:
    HAS_PLAYWRIGHT = False

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed"),
]


CONV = "33333333-3333-4333-8333-333333333333"


class TestAgentProposalApi:
    """The API-level contract ``save_memory`` relies on."""

    def test_agent_proposal_lineage_and_provenance(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]

        proposed = client.post(
            "/api/memory/candidates",
            json={
                "content": "agent-seen preference",
                "scope": "user",
                "category": "preference",
                "name": "e2e-agent-lineage",
                "proposer": "agent",
                "provenance": {"conversation_id": CONV},
            },
        )
        assert proposed.status_code == 200, proposed.text

        mem = proposed.json()
        assert mem["metadata"]["memory_status"] == "candidate"
        lineage = mem["metadata"]["lineage"]
        assert lineage[0]["event"] == "proposed"
        assert lineage[0]["actor"] == "agent"
        prov = mem["metadata"].get("provenance") or {}
        assert prov.get("conversation_id") == CONV

    def test_agent_candidate_is_visible_in_review_queue(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]

        proposed = client.post(
            "/api/memory/candidates",
            json={
                "content": "queue-test",
                "scope": "user",
                "category": "workflow_hint",
                "name": "e2e-agent-queue",
                "proposer": "agent",
            },
        )
        assert proposed.status_code == 200
        fqn = proposed.json()["fqn"]

        queue = client.get("/api/memory/candidates")
        assert queue.status_code == 200
        assert any(m["fqn"] == fqn for m in queue.json())


class TestAgentCandidateBrowserApproval:
    """A candidate produced by ``save_memory`` must approve cleanly in the shipped UI."""

    def test_agent_candidate_approves_from_review_tab(
        self, authenticated_page: Page, api_client: object, base_url: str
    ) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]

        client.post(
            "/api/memory/candidates",
            json={
                "content": "agent approved via ui",
                "scope": "user",
                "category": "preference",
                "name": "e2e-agent-approve",
                "proposer": "agent",
                "provenance": {"conversation_id": CONV},
            },
        )

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.locator('.memory-tab[data-tab="review"]').click()
        expect(page.locator(".memory-review-item")).to_contain_text("@user/memory/e2e-agent-approve")
        page.locator('.memory-review-item:has-text("e2e-agent-approve") .memory-review-approve').click()
        page.wait_for_timeout(500)

        got = client.get("/api/memory/@user/memory/e2e-agent-approve")
        assert got.status_code == 200
        assert got.json()["metadata"]["memory_status"] == "active"
