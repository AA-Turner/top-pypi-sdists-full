"""E2E tests for workflow transcript rendering (#1112).

Verifies transcript API contract, HTML structure, and browser-level
transcript section behavior.
"""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.e2e]


class TestTranscriptAPIContract:
    """Verify transcript API endpoints from #1114 are preserved."""

    def test_events_endpoint_accepts_event_type_prefix_filter(self, api_client) -> None:
        """GET /workflow-runs/{id}/events?event_type=transcript returns 404 for missing run."""
        resp = api_client.get("/api/workflow-runs/nonexistent/events?event_type=transcript")
        assert resp.status_code == 404

    def test_step_transcript_endpoint_returns_404_for_missing_run(self, api_client) -> None:
        """GET /workflow-runs/{id}/steps/{sid}/transcript returns 404 for missing run."""
        resp = api_client.get("/api/workflow-runs/nonexistent/steps/step1/transcript")
        assert resp.status_code == 404


class TestTranscriptHTMLStructure:
    """Verify transcript-related HTML and assets are served correctly."""

    def test_index_serves_successfully(self, base_url: str) -> None:
        """GET / should serve the index page with workflows panel structure."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert resp.status_code == 200
        assert 'id="workflows-panel"' in resp.text

    def test_workflows_js_contains_transcript_rendering(self, base_url: str) -> None:
        """workflows.js should contain the transcript rendering functions."""
        import httpx

        resp = httpx.get(f"{base_url}/js/workflows.js", follow_redirects=True)
        assert resp.status_code == 200
        assert "_renderTranscript" in resp.text
        assert "_renderTranscriptEntry" in resp.text

    def test_css_has_transcript_styles(self, base_url: str) -> None:
        """style.css should contain transcript-specific CSS classes."""
        import httpx

        resp = httpx.get(f"{base_url}/css/style.css", follow_redirects=True)
        assert resp.status_code == 200
        assert "wf-transcript-stdout" in resp.text
        assert "wf-transcript-stderr" in resp.text
        assert "wf-transcript-usage" in resp.text


# ---------------------------------------------------------------------------
# Playwright browser interaction tests (#1112)
# ---------------------------------------------------------------------------

try:
    import playwright  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")


@requires_playwright
class TestTranscriptBrowser:
    """Browser-level tests for transcript rendering in the workflows panel."""

    def test_workflows_panel_opens(self, authenticated_page) -> None:
        """Clicking the workflows toggle should show the panel."""
        page = authenticated_page
        btn = page.locator("#btn-workflows-toggle")
        if btn.count() == 0:
            pytest.skip("Workflows toggle button not found")
        btn.click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)
        assert page.locator("#workflows-panel").is_visible()

    def test_transcript_container_renders_in_detail_view(self, authenticated_page) -> None:
        """Selecting a run should render the #workflow-transcript container.

        This closes the #1112 test gap: verifies transcript UI actually
        renders after selecting a run, not just that the panel opens.
        The container should show either transcript entries or an empty state.
        """
        page = authenticated_page
        btn = page.locator("#btn-workflows-toggle")
        if btn.count() == 0:
            pytest.skip("Workflows toggle button not found")
        btn.click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)

        # Need at least one run to test the detail view
        run_items = page.locator(".wf-run-item")
        if run_items.count() == 0:
            pytest.skip("No workflow runs available to test detail view")

        # Click the first run to open detail view
        run_items.first.click()

        # The detail view creates a #workflow-transcript div via _renderTranscript().
        # Wait for it to appear — it gets populated asynchronously after the
        # detail view renders.
        transcript_container = page.locator("#workflow-transcript")
        transcript_container.wait_for(state="attached", timeout=5000)

        # The container should have rendered: either transcript entries
        # (wf-transcript-step-header, wf-transcript-stdout, etc.) or
        # the empty state (wf-transcript-empty with "No transcript data.")
        has_entries = (
            page.locator(
                ".wf-transcript-step-header, .wf-transcript-stdout, .wf-transcript-stderr, .wf-transcript-entry"
            ).count()
            > 0
        )
        has_empty_state = page.locator(".wf-transcript-empty").count() > 0

        assert has_entries or has_empty_state, (
            "Expected #workflow-transcript to contain either transcript entries "
            "or the 'No transcript data.' empty state, but found neither"
        )
